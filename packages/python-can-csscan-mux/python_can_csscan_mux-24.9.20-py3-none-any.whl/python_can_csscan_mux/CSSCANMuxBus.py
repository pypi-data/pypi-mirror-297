import can

from can import CanInterfaceNotImplementedError, Message
from collections import deque
from time import sleep
from typing import Any, Optional, Tuple

from .CSSCANMux import CSSCANMux
from .Timeout import Timeout


class CSSCANMuxBus(can.BusABC):
    
    def __init__(self, channel: Any, can_filters: Optional[can.typechecking.CanFilters] = None, **kwargs: object):
        super(CSSCANMuxBus, self).__init__(channel, can_filters, **kwargs)
        
        # We need an underlying bus to feed data. If the channel is not such an instance, check for additional
        # arguments to instantiate a driver.
        if not isinstance(channel, can.BusABC):
            # Not a bus instance, attempt to instantiate a driver with this resource instead
            interface = kwargs.get("driver", None)

            if interface is None:
                raise ValueError("No driver supplied for the underlying interface")
            elif not isinstance(interface, str):
                raise TypeError("Interface supplied is not a string")
            
            # noinspection PyTypeChecker
            self._wrapped = can.Bus(channel=channel, interface=interface, **kwargs)
        else:
            self._wrapped = channel
        
        if self._wrapped is None:
            raise CanInterfaceNotImplementedError(f"Could not open {channel}")
        
        self.channel_info = f"CSSCAN mux on {channel}"
        self._mux = CSSCANMux(**kwargs)
        
        # NOTE: I would like to enable the following check, but it doesn't work with virtual buses
#        if self._mux._use_fd is True and self._wrapped.protocol == can.CanProtocol.CAN_20:
#            raise ValueError("FD enabled but underlying channel does not support it")
        
        # Event queue, contains parsed frames
        self._events = deque()
        
        return
    
    def _recv_internal(self, timeout: Optional[float]) -> Tuple[Optional[Message], bool]:
        result = None
        t = Timeout(timeout)
        
        # Check if there are any pending events in the queue. If so, return this
        while len(self._events) == 0 and t.expired() is False:
            # Receive new data from the serial interface and pass it to the parser
            message = self._wrapped.recv(timeout=t.time_left())
            
            if message is None:
                continue
            
            # Decode the message(s)
            # NOTE: The mux decoder forwards any unknown messages
            self._events.extend(self._mux.decode(message))
        
        if len(self._events) > 0:
            result = self._events.popleft()
        
        return result, False
    
    def send(self, msg: Message, timeout: Optional[float] = None) -> None:
        # Encode message
        # NOTE: The mux encoder forwards any unknown messages
        encoded_messages = list(self._mux.encode(msg))
        for encoded_message in encoded_messages:
            self._wrapped.send(encoded_message, timeout=timeout)
            
            if len(encoded_messages) > 1:
                # This seems to be required for socketcan
                sleep(0.001)
        
        return
    
    def shutdown(self) -> None:
        super().shutdown()
        
        self._wrapped.shutdown()
        
        return
    
    pass

import can
import copy

from collections import namedtuple
from typing import Any, Dict, Iterable, List, Optional, Union

from .Common import CSSCANMuxConfiguration, CSSCANMuxConfigurationEntry
from .ISO_TP import iso_tp_pack_frame, ISOTPDecoder
from .Message import decode_message, encode_message


MuxOutputMap = namedtuple("MuxOutputMap", ["id", "mux_channel", "output_channel"])
MapKey = namedtuple("MapKey", ["channel", "id"])

class CSSCANMux(object):
    """
    Class for handling configuration and mux/demuxing.
    """
    
    _unknown_channel = None
    _default_id_in = 0x010
    _default_id_out = 0x011
    
    @staticmethod
    def _cast_to_common(value: Any) -> Any:
        from can.util import cast_from_string
        if value is None:
            return None
        return cast_from_string(str(value))
    
    def __init__(self, **kwargs):
        # There are two ways to supply the multiplexing configuration:
        # - Through a dictionary in the "mux_can" argument (default)
        # - Through a series of strings in "mux_canX" arguments
        # The configuration has to be either/or. Both at the same time is not supported.
        # First, check for the dictionary configuration
        
        config = None
        
        for k in kwargs.keys():
            if k == "mux_can":
                # Primary configuration key found, check for the presence of string keys
                for k in kwargs.keys():
                    if k == "mux_can":
                        # Skip current key
                        continue
                    
                    if k.startswith("mux_can"):
                        raise ValueError("Configuration arguments supplied to both string and dictionary configuration")
                
                # Attempt to parse the dictionary config
                configuration_dict = kwargs.get("mux_can")
                
                if not isinstance(configuration_dict, dict):
                    break
                
                config = CSSCANMuxConfiguration()
                
                for k, v in configuration_dict.items():
                    if not isinstance(v, list):
                        raise TypeError(f"Configuration value {v} is not a list")
                    
                    for entry in v:
                        config.config[self._cast_to_common(k)].append(CSSCANMuxConfigurationEntry.from_dict(entry))
                
                break
        
        if config is None:
            # Dictionary entry not found, try looking for string configuration instead
            for k, v in kwargs.items():
                if not k.startswith("mux_can"):
                    continue
                
                if k == "mux_can":
                    channel = self._unknown_channel
                else:
                    channel = int(k[len("mux_can"):], 10)
                    
                # Expected format is "id_1:id_2:...#S1;S2;S3;S4"
                splits = v.split("#")
                if len(splits) != 2:
                    raise ValueError(f"Invalid pattern for mux string configuration: {v}")
                
                # Extract IDs from first elements
                ids_str = splits[0].split(":")
                if len(ids_str) < 1:
                    raise ValueError("Mux id configuration must contain at least one ID")
                
                ids = set()
                for value in ids_str:
                    if len(value) != 3 and len(value) != 8:
                        raise ValueError(
                            f"Could not parse mux ID \"{value}\". Entry must be either 3 or 8 characters long")
                    
                    parsed_id = int(value, 16)
                    if len(value) == 8:
                        parsed_id |= 0x80000000
                    
                    ids.add(parsed_id)
                
                if len(ids) != len(ids_str):
                    raise ValueError(f"Duplicate ID detected in {ids_str}")
                
                # Extract secondary channels from second elements
                secondary_channels_str = splits[1].split(":")
                if len(secondary_channels_str) != 4:
                    raise ValueError("Mux channel configuration must be 4 entries long")
                
                secondary_channels = []
                for value in secondary_channels_str:
                    parsed_secondary_channel = None
                    
                    if len(value) > 0:
                        parsed_secondary_channel = self._cast_to_common(value)
                    
                    secondary_channels.append(parsed_secondary_channel)
                
                if len(set(secondary_channels)) != len(secondary_channels_str):
                    raise ValueError(f"Duplicate channel detected in {secondary_channels_str}")
                
                if config is None:
                    config = CSSCANMuxConfiguration()
                
                entry = CSSCANMuxConfigurationEntry(
                    s1=secondary_channels[0],
                    s2=secondary_channels[1],
                    s3=secondary_channels[2],
                    s4=secondary_channels[3],
                    mux_ids=ids
                )
                config.config[channel].append(entry)
        
        if config is None:
            config = CSSCANMuxConfiguration()
        
        mux_rules = {}
        mux_output = {}
        
        # Flatten config
        for channel, mappings in config.config.items():
            for mapping in mappings:
                # Add all the mappings to the general configuration
                for mux_id in mapping.mux_ids:
                    key = self._generate_key(channel, mux_id)
                    
                    if key in mux_rules.keys():
                        raise ValueError(f"Mux ID {mux_id} is already configured for channel {channel}")
                    
                    mux_rules[key] = [mapping.s1, mapping.s2, mapping.s3, mapping.s4]
                
                # Extract the tx rule from the general rules if configured
                if mapping.mux_id_tx >= 0:
                    if mapping.mux_id_tx not in mapping.mux_ids:
                        raise ValueError("Mux Tx ID must be in mux network configuration")
                    
                    key_tx = self._generate_key(channel, mapping.mux_id_tx)
                    
                    if key_tx in mux_output.keys():
                        raise ValueError(f"Mux ID {mapping.mux_id_tx} is already configured for channel {channel}")
                    
                    mux_output[key_tx] = mux_rules.pop(key_tx)
        
        # Insert default arguments if necessary
        if len(mux_rules) == 0 and len(mux_output) == 0:
            mux_rules[self._generate_key(self._unknown_channel, self._default_id_in)] = [0, 1, 2, 3]
            mux_output[self._generate_key(self._unknown_channel, self._default_id_out)] = [0, 1, 2, 3]
        
        self._mux_input = mux_rules
        
        # Flip the mux output dictionary from "(channel:id):output channels" to "output channel:(channel:id)"
        self._mux_output: Dict[int, MuxOutputMap] = {}
        for key, values in mux_output.items():
            mapped_channel = key.channel
            if mapped_channel == self._unknown_channel:
                mapped_channel = None
            mapped_id = key.id
            
            for i, value in enumerate(values):
                if value is None:
                    continue
                
                self._mux_output[value] = MuxOutputMap(mapped_id, i, mapped_channel)
        
        # Determine output format
        self._use_fd = kwargs.get("mux_fd", True)
        self._use_brs = kwargs.get("mux_brs", self._use_fd)
        
        # Sanity check. If the underlying channel does not support FD/BRS and they are enabled, throw an error
        if self._use_brs is True and self._use_fd is False:
            raise ValueError("BRS enabled but FD is disabled")
        
        # ISO-TP decoder for each configuration
        self._iso_tp = {}
        for key in self._mux_input:
            self._iso_tp[key] = ISOTPDecoder()
        
        return

    @staticmethod
    def _generate_key(channel: Any, id: int) -> MapKey:
        return MapKey(channel, id & 0xFFFFFFFF)
    
    def decode(self, messages: Union[can.Message, Iterable[can.Message]]) -> Iterable[can.Message]:
        if isinstance(messages, can.Message):
            messages = [messages]
        elif not isinstance(messages, Iterable):
            raise TypeError(f"Unexpected type of messages:, {type(messages)}")
        
        if messages is None:
            raise ValueError("No messages (either through argument or initial argument)")
        
        for message in messages:
            message_id = message.arbitration_id
            if message.is_extended_id is True:
                message_id |= 0x80000000
            
            key = self._generate_key(message.channel, message_id)
            
            # Get mapped configuration
            configuration: Optional[List] = self._mux_input.get(key, None)
            if configuration is None:
                # Not mapped, yield the unaltered message
                yield message
                continue
            
            # Feed data through ISO-TP decoder
            data = self._iso_tp[key].parse(message)
            
            if data is None:
                continue
            
            timestamp = message.timestamp
            while len(data) > 0:
                # Feed data through frame parser
                data, frame = decode_message(data)
                
                if frame is None:
                    continue
                
                # Map channel (Suppress check since the decode_message always emits an integer)
                # noinspection PyTypeChecker
                frame.channel = configuration[frame.channel]
                if frame.channel is None:
                    continue
                
                # Preserve timestamp
                frame.timestamp = timestamp
                timestamp += 0.000000001
                
                yield frame
        
        return
    
    def encode(self, messages: Union[can.Message, Iterable[can.Message]]) -> Iterable[can.Message]:
        if isinstance(messages, can.Message):
            messages = [messages]
        elif not isinstance(messages, Iterable):
            raise TypeError(f"Unexpected type of messages:, {type(messages)}")
        
        if messages is None:
            raise ValueError("No messages (either through argument or initial argument)")
        
        for message in messages:
            # Get mapped configuration
            configuration = self._mux_output.get(message.channel, None)
            if configuration is None:
                # Not mapped, yield the unaltered message
                yield message
                continue
            
            # Encode data
            msg_to_encode = copy.deepcopy(message)
            
            # Set internal channel
            msg_to_encode.channel = configuration.mux_channel
            
            # Encode the cloned message
            encoded_message = encode_message(msg_to_encode)
            
            # Encode using ISO-TP
            mtu = 64 if self._use_fd else 8
            packed_messages = iso_tp_pack_frame(encoded_message, mtu)
            
            # Set common options
            for packed_message in packed_messages:
                packed_message.is_fd = self._use_fd
                packed_message.bitrate_switch = self._use_brs
                packed_message.arbitration_id = configuration.id & 0x1FFFFFFF
                packed_message.is_extended_id = (configuration.id & 0x80000000) == 0x80000000
                packed_message.channel = configuration.output_channel
            
                yield packed_message
        
        return
    
    pass

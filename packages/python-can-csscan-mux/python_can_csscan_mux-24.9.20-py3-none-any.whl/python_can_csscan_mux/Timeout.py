import datetime
import threading


class Timeout(object):
    def __init__(self, timeout: float):
        self._initial_time = datetime.datetime.now()
        
        if timeout is None:
            self._timeout = datetime.datetime.max
        elif timeout < 0:
            raise ValueError("Timeout must be positive")
        else:
            self._timeout = self._initial_time + datetime.timedelta(seconds=timeout)
        
        return
    
    def time_left(self) -> float:
        time_left = self._timeout - datetime.datetime.now()
        
        # NOTE: Some of the underlying implementation, e.g. the virtualbus from python-can, passes this to a
        #       threading element, which fails if the value is too large. Clip the value if required.
        result = min(time_left.total_seconds(), threading.TIMEOUT_MAX)
        
        if time_left < datetime.timedelta(0):
            result = 0
        return result
    
    def expired(self) -> bool:
        return datetime.datetime.now() > self._timeout
    
    pass

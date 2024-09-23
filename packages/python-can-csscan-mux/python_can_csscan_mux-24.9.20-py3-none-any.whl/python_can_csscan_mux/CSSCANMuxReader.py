import can

from can.io.generic import MessageReader
from typing import Iterable

from .CSSCANMux import CSSCANMux


class CSSCANMuxReader(MessageReader):
    
    def __init__(self, reader: Iterable[can.Message], **kwargs):
        # We do not support files, but rather readers
        if "file" in kwargs.keys():
            raise ValueError("Argument \"file\" is not supported")
        
        super(CSSCANMuxReader, self).__init__(file=None, **kwargs)
        
        self._reader = reader
        self._mux = CSSCANMux(**kwargs)
        
        return
    
    def __iter__(self):
        return self._mux.decode(iter(self._reader))
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return
    
    pass

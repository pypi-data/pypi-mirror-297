from collections import defaultdict
from dataclasses import field, dataclass
from dataclasses_json import dataclass_json
from typing import Any, List


# NOTE: The dataclasses below use BOTH the dataclass and dataclass_json annotation tags, since dataclass_json
#       provides the functionality to load from a dictionary.


@dataclass_json
@dataclass
class CSSCANMuxConfigurationEntry(object):
    s1: Any = -1
    s2: Any = -1
    s3: Any = -1
    s4: Any = -1
    mux_ids: set[int] = field(default_factory=set)
    mux_id_tx: int = -1
    
    pass


@dataclass_json
@dataclass
class CSSCANMuxConfiguration(object):
    # NOTE: See https://stackoverflow.com/a/71384386 for how to map a defaultdict to a dataclass
    config: defaultdict[Any, List[CSSCANMuxConfigurationEntry]] = field(default_factory=lambda: defaultdict(list))
    
    pass


def dlc_to_nob(dlc: int) -> int:
    if dlc <= 8:
        return dlc
    elif dlc == 9:
        return 12
    elif dlc == 10:
        return 16
    elif dlc == 11:
        return 20
    elif dlc == 12:
        return 24
    elif dlc == 13:
        return 32
    elif dlc == 14:
        return 48
    elif dlc == 15:
        return 64
    else:
        raise ValueError("Invalid DLC")


def nob_to_dlc(nob: int) -> int:
    if 0 <= nob <= 8:
        return nob
    elif 8 < nob <= 12:
        return 9
    elif 12 < nob <= 16:
        return 10
    elif 16 < nob <= 20:
        return 11
    elif 20 < nob <= 24:
        return 12
    elif 24 < nob <= 32:
        return 13
    elif 32 < nob <= 48:
        return 14
    elif 48 < nob <= 64:
        return 15
    else:
        raise ValueError("Invalid CAN byte length")
    pass

from enum import Enum, auto


class ErrorPolicy(Enum):
    FAIL_FAST = auto()
    ISOLATE = auto()
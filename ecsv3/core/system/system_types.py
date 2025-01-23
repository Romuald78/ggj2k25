from enum import Enum


class EventType(Enum):
    KEY_BUTTON   = 10,
    PAD_BUTTON   = 20,
    PAD_AXIS     = 21,
    MOUSE_BUTTON = 30,
    MOUSE_AXIS   = 31


class SystemGroup(Enum):
    UPDATE = 1,
    DRAW   = 2,
    EVENT  = 3


from ecsv3.core.component.input.input_axis import InputAxis
from ecsv3.core.system.system_types import EventType


class GamepadAxis(InputAxis):

    def __init__(self, name, axis_code, dead_zone=0.2, gamepad_id=None, priority=1):
        super().__init__(name, priority, EventType.PAD_AXIS, axis_code, gamepad_id, dead_zone=dead_zone)


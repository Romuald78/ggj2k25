from ecsv3.core.component.input.input_axis import InputAxis
from ecsv3.core.system.system_types import EventType


class MouseAxis(InputAxis):

    def __init__(self, name, axis_code, priority=1):
        super().__init__(name, priority, EventType.MOUSE_AXIS, axis_code)


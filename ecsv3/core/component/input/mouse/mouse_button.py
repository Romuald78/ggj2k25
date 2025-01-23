from ecsv3.core.component.input.input_switch import InputSwitch
from ecsv3.core.system.system_types import EventType

class MouseButton(InputSwitch):

    def __init__(self, name, button_code, priority=1):
        super().__init__(name, priority, EventType.MOUSE_BUTTON, button_code)

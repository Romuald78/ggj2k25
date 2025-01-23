from ecsv3.core.component.input.input_switch import InputSwitch
from ecsv3.core.system.system_types import EventType


class GamepadButton(InputSwitch):

    def __init__(self, name, button_code=None, gamepad_id=None, priority=1):
        super().__init__(name, priority, EventType.PAD_BUTTON, button_code, gamepad_id)


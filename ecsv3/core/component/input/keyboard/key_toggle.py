from ecsv3.core.component.input.input_comp import InputComponent
from ecsv3.core.component.input.input_switch import InputSwitch
from ecsv3.core.system.system_types import EventType


class KeyToggle(InputSwitch):

    def __init__(self, name, key_code=None, priority=1):
        super().__init__(name, priority, EventType.KEY_BUTTON, key_code)



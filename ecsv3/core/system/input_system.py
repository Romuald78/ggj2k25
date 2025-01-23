from ecsv3.core.component.input.gamepad.gamepad_axis import GamepadAxis
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.component.input.keyboard.key_toggle import KeyToggle
from ecsv3.core.component.input.mouse.mouse_axis import MouseAxis
from ecsv3.core.component.input.mouse.mouse_button import MouseButton
from ecsv3.core.system.system import System


class InputSystem(System):

    # typ is a dictionary containing each object class type that will be
    # handled in this system. The keys are the object types, and the values
    # are just string : comments about the type
    def __init__(self, name, priority: int = 1):
        types = {
            KeyToggle     : 'key',
            GamepadButton : 'gamepad button',
            MouseButton   : 'mouse button',
            GamepadAxis   : 'gamepad axis',
            MouseAxis     : 'mouse axis'
        }
        super().__init__(types, name, priority)

    def process_components(self, delta_time=1/60, data=None):
        if data is not None:
            for comp in self._components_order:
                # check if event type matches
                evt_typ = data[0]
                src     = data[1][0]
                code    = data[1][1]
                state   = data[1][2]
                if comp.event_type == evt_typ:
                    # check if source matches
                    if comp.source_id is None or comp.source_id == src:
                        # check if input code value matches
                        if comp.code_id == code or comp.code_id is None:
                            comp.update_value(src, code, state)


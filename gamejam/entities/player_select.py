import random

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.input.gamepad.gamepad_axis import GamepadAxis
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.entity import Entity
from gamejam.components.scripts.select_move_player import MovePlayer


class PlayerSelect(Entity):

    def getColor(self):
        return self[f"bubble_select_{self.__ctrlID}"]

    def __init__(self, name, ctrlID, x0, y0, limits, players, gfx_pos):
        super().__init__(name)
        self.__ctrlID  = ctrlID
        self.__players = players
        self.__gfx_pos = gfx_pos

        # gfx
        gfx_front = ArcadeFixed(f"bubble_select",
                                f"bubble_select_{ctrlID}",
                                priority=10)
        # resize bubble
        gfx_front.resize(width=200)
        # set in the middle of the screen
        gfx_front.x = random.randint(-100,100) + x0
        gfx_front.y = random.randint(-100,100) + y0
        gfx_front.color = (255,255,255,16)

        # axis X and Y to move
        x = GamepadAxis(f"axisX_{ctrlID}", 'X',gamepad_id=ctrlID)
        y = GamepadAxis(f"axisY_{ctrlID}", 'Y',gamepad_id=ctrlID)

        # button to select/deselect
        button_add = GamepadButton(f"button_add_{ctrlID}", 'A', gamepad_id=ctrlID)
        button_rmv = GamepadButton(f"button_rmv_{ctrlID}", 'B', gamepad_id=ctrlID)

        # script to move
        mv = MovePlayer(f"mvply_{ctrlID}", gfx_front,
                        x, y, limits, ctrlID, self.__players)

        # add all components
        self.add_component(x)
        self.add_component(y)
        self.add_component(gfx_front)
        self.add_component(mv)

    @property
    def ctrlID(self):
        return self.__ctrlID
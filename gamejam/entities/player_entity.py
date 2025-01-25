from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.input.gamepad.gamepad_axis import GamepadAxis
from ecsv3.core.entity import Entity
from gamejam.components.scripts.move1way import MoveOneWay


class PlayerCreation(Entity):

    def __init__(self, name, ctrlID, eltID, posID, w, h):
        super().__init__(name)

        # left right top down
        limits = [w/2 - h/2, w/2 + h/2, h, 0]

        #--------- VERTICAL MOVE ---------
        if posID[1] == 0:
            # GFX (fipped or not)
            flip = posID[0] == -1
            gfx_idle = ArcadeFixed(f"front_hero{eltID}",
                                   f"front_{eltID}_{ctrlID}",
                                   priority=50, flipH=flip)
            gfx_idle.x = (w / 2) + (h * posID[0] / 2)
            gfx_idle.y = (h / 2) * (1 + posID[1])
            gfx_idle.y = max(0, min(h-0, gfx_idle.y))
            # Move axis (vertical)
            axis = GamepadAxis(f"axisY_{ctrlID}", 'Y', gamepad_id=ctrlID)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idle,],
                                  limits, vertical=True)

            # add components
            self.add_component(axis)
            self.add_component(gfx_idle)
            self.add_component(move1way)


        #--------- HORIZONTAL MOVE ---------


        #--------- COMMON ---------

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.gfx.gfx_comp import GfxAnchor
from ecsv3.core.component.input.gamepad.gamepad_axis import GamepadAxis
from ecsv3.core.entity import Entity
from gamejam.components.scripts.move1way import MoveOneWay


class PlayerCreation(Entity):

    @property
    def limits(self):
        return self.__limits

    def __init__(self, name, ctrlID, eltID, posID, w, h):
        super().__init__(name)

        # left right top down
        self.__limits = [w/2 - h/2, w/2 + h/2, h, 0]

        #--------- VERTICAL MOVE ---------
        if posID[1] == 0:
            # GFX (fipped or not)
            flip = posID[0] == -1
            gfx_idle = ArcadeFixed(f"front_hero{eltID}",
                                   f"front_{eltID}_{ctrlID}",
                                   priority=50, flipH=flip)
            gfx_idle.anchor = GfxAnchor.BOTTOM
            gfx_idle.x = (w / 2) + (h * posID[0] / 2)
            gfx_idle.y = (h / 2) * (1 + posID[1])
            gfx_idle.y = max(0, min(h-0, gfx_idle.y))
            # Move axis (vertical)
            axis = GamepadAxis(f"axisY_{ctrlID}", 'Y', gamepad_id=ctrlID)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idle,],
                                  self.__limits, vertical=True)

            # add components
            self.add_component(axis)
            self.add_component(gfx_idle)
            self.add_component(move1way)

        #--------- HORIZONTAL MOVE (bottom) ---------
        elif posID[1] == -1:
            # GFX
            gfx_idle = ArcadeFixed(f"back_hero{eltID}",
                                   f"back_{eltID}_{ctrlID}",
                                   priority=60)
            gfx_idle.anchor = GfxAnchor.BOTTOM
            gfx_idle.y = (posID[1] +1) * (h/2)
            gfx_idle.x = (w / 2)
            # Move axis (vertical)
            axis = GamepadAxis(f"axisX_{ctrlID}", 'X', gamepad_id=ctrlID)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idle, ],
                                  self.__limits, vertical=False)

            # add components
            self.add_component(axis)
            self.add_component(gfx_idle)
            self.add_component(move1way)


        # --------- HORIZONTAL MOVE (top) ---------
        elif posID[1] == 1:
            # GFX (fipped or not)
            gfx_idleL = ArcadeFixed(f"front_hero{eltID}",
                                   f"back_{eltID}_{ctrlID}L",
                                   priority=40)
            gfx_idleL.anchor = GfxAnchor.BOTTOM
            gfx_idleL.y = (posID[1] + 1) * (h / 2)
            gfx_idleL.x = (w / 2)
            gfx_idleR = ArcadeFixed(f"front_hero{eltID}",
                                   f"back_{eltID}_{ctrlID}R",
                                   priority=40, flipH=True)
            gfx_idleR.anchor = GfxAnchor.BOTTOM
            gfx_idleR.y = (posID[1] + 1) * (h / 2)
            gfx_idleR.x = (w / 2)
            gfx_idleR.alpha = 0
            # Move axis (vertical)
            axis = GamepadAxis(f"axisX_{ctrlID}", 'X', gamepad_id=ctrlID)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idleL, gfx_idleR],
                                  self.__limits, vertical=False)

            # add components
            self.add_component(axis)
            self.add_component(gfx_idleL)
            self.add_component(gfx_idleR)
            self.add_component(move1way)

    #--------- COMMON ---------

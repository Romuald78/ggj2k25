from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.gfx.gfx_comp import GfxAnchor
from ecsv3.core.component.input.gamepad.gamepad_axis import GamepadAxis
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.entity import Entity
from gamejam.components.scripts.move1way import MoveOneWay


class PlayerCreation(Entity):


    @property
    def limits(self):
        return self.__limits

    def __init__(self, name, ctrlID, eltID, posID, w, h, playerH, playerMargin, yref):
        super().__init__(name)

        # left right top down
        self.__limits = [w/2 - h/2, w/2 + h/2, h+yref, yref]

        #--------- VERTICAL MOVE ---------
        if posID[1] == 0:
            # GFX (fipped or not)
            flip = posID[0] == -1
            gfx_idle = ArcadeFixed(f"front_hero{eltID}",
                                   f"front_{eltID}_{ctrlID}",
                                   priority=50, flipH=flip)
            gfx_idle.resize(height=playerH)
            gfx_idle.anchor = GfxAnchor.BOTTOM
            gfx_idle.x = (w / 2) + (h * posID[0] / 2)
            gfx_idle.y = (h / 2) * (1 + posID[1]) + yref
            gfx_idle.y = max(0, min(h-0, gfx_idle.y))

            shadow = ArcadeFixed(f"shadow",
                                   f"shadow_{eltID}_{ctrlID}",
                                   priority=20, )
            shadow.resize(height=playerH)
            shadow.x = gfx_idle.x
            shadow.y = gfx_idle.y
            shadow.resize(width=gfx_idle.width * 0.5)
            shadow.color = (0,0,0,128)

            # Move axis (vertical)
            axis = GamepadAxis(f"axisY_{ctrlID}", 'Y', gamepad_id=ctrlID)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idle, shadow],
                                  self.__limits, vertical=True,
                                  margin=playerMargin, flipH=flip)

            # add components
            self.add_component(axis)
            self.add_component(gfx_idle)
            self.add_component(shadow)
            self.add_component(move1way)

        #--------- HORIZONTAL MOVE (bottom) ---------
        elif posID[1] == -1:
            # GFX
            gfx_idle = ArcadeFixed(f"back_hero{eltID}",
                                   f"back_{eltID}_{ctrlID}",
                                   priority=60)
            gfx_idle.resize(height=playerH)
            gfx_idle.anchor = GfxAnchor.BOTTOM
            gfx_idle.y = (posID[1] +1) * (h/2) + yref
            gfx_idle.x = (w / 2)
            shadow = ArcadeFixed(f"shadow",
                                 f"shadow_{eltID}_{ctrlID}",
                                 priority=20 )
            shadow.resize(height=playerH)
            shadow.x = gfx_idle.x
            shadow.y = gfx_idle.y
            shadow.resize(width=gfx_idle.width * 0.5)

            # Move axis (vertical)
            axis = GamepadAxis(f"axisX_{ctrlID}", 'X', gamepad_id=ctrlID)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idle, shadow],
                                  self.__limits, vertical=False,
                                  margin=playerMargin)

            # add components
            self.add_component(axis)
            self.add_component(gfx_idle)
            self.add_component(shadow)
            self.add_component(move1way)


        # --------- HORIZONTAL MOVE (top) ---------
        elif posID[1] == 1:
            # GFX (fipped or not)
            gfx_idleL = ArcadeFixed(f"front_hero{eltID}",
                                   f"back_{eltID}_{ctrlID}L",
                                   priority=40)
            gfx_idleL.resize(height=playerH)
            gfx_idleL.anchor = GfxAnchor.BOTTOM
            gfx_idleL.y = (posID[1] + 1) * (h / 2) + yref
            gfx_idleL.x = (w / 2)
            gfx_idleR = ArcadeFixed(f"front_hero{eltID}",
                                   f"back_{eltID}_{ctrlID}R",
                                   priority=40, flipH=True)

            gfx_idleR.resize(height=playerH)
            gfx_idleR.anchor = GfxAnchor.BOTTOM
            gfx_idleR.y = (posID[1] + 1) * (h / 2) + yref
            gfx_idleR.x = (w / 2)
            gfx_idleR.alpha = 255
            shadow = ArcadeFixed(f"shadow",
                                 f"shadow_{eltID}_{ctrlID}",
                                 priority=20, )
            shadow.resize(height=playerH*0.5)
            shadow.x = gfx_idleL.x
            shadow.y = gfx_idleL.y
            shadow.resize(width=gfx_idleL.width * 0.5)

            # Move axis (vertical)
            axis = GamepadAxis(f"axisX_{ctrlID}", 'X', gamepad_id=ctrlID)



            # add components
            self.add_component(axis)
            self.add_component(gfx_idleL)
            self.add_component(gfx_idleR)
            self.add_component(shadow)

            # Move one way script
            move1way = MoveOneWay(f"move1way_{ctrlID}",
                                  axis, [gfx_idleL, gfx_idleR, shadow],
                                  self.__limits, vertical=False,
                                  margin=playerMargin)
            self.add_component(move1way)

        # BUTTONS
        buttA = GamepadButton(f"buttonA_{ctrlID}", 'A', gamepad_id=ctrlID)
        buttB = GamepadButton(f"buttonB_{ctrlID}", 'B', gamepad_id=ctrlID)
        buttX = GamepadButton(f"buttonX_{ctrlID}", 'X', gamepad_id=ctrlID)
        buttY = GamepadButton(f"buttonY_{ctrlID}", 'Y', gamepad_id=ctrlID)
        self.add_component(buttA)
        self.add_component(buttB)
        self.add_component(buttX)
        self.add_component(buttY)


    #--------- COMMON ---------

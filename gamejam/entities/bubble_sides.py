import random

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.gfx.gfx_comp import GfxAnchor
from ecsv3.core.component.input.gamepad.gamepad_axis import GamepadAxis
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.entity import Entity
from gamejam.components.scripts.gen_bubble_sides import MoveBubbleSides
from gamejam.components.scripts.move1way import MoveOneWay


class BubbleSide(Entity):


    def __init__(self, name, limits, bub_size):
        super().__init__(name)

        gfxs = []
        for i in range(20):
            bub = ArcadeFixed('bubble', f"{name}{i}", priority=3, flipH=random.choice(['True', 'False']))
            bub.resize(width=bub_size * (random.random()*0.5 + 0.5))
            bub.x = random.randint(limits[0], limits[1])
            bub.y = random.randint(limits[3], limits[2])
            gfxs.append(bub)
            self.add_component(bub)

        bubsid = MoveBubbleSides(f"{name}_side", gfxs, limits)
        self.add_component(bubsid)

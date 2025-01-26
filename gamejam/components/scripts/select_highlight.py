import random

from ecsv3.core.component.script.script_comp import ScriptComponent
from launchers.arcade.default_config import RATIO


class SelectHighLight(ScriptComponent):

    SPEED = 50 * RATIO

    COLORS = [(128,128,255),
              (255,255,128),
              (128,255,128),
              (255,128,128)]

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        # set slots transparent first
        for s in self.__slots:
            s.color = (255,255,255,140)
        for ctrlID in self.__players:
            ent = self.__players[ctrlID]['entity'][f"bubble_select_{ctrlID}"]
            # init color
            ent.color = (255,255,255,200)
            ent.angle += random.randint(0, 10) / 10
            for slot in self.__slots:
                idx = self.__slots.index(slot)
                dist = ent.distance2To(slot)
                if dist <= max(slot.width, slot.height)**2 / 4:
                    slot.color = (255,255,255,255)
                    ent.color  = SelectHighLight.COLORS[idx]
                    ent.alpha  = 192

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, players, slots):
        super().__init__(name)
        self.__players = players
        self.__slots   = slots

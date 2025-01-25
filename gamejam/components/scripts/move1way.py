
from ecsv3.core.component.script.script_comp import ScriptComponent


class MoveOneWay(ScriptComponent):

    SPEED = 50

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        # Move + limits
        value = self.__axis.value * MoveOneWay.SPEED
        for gfx in self.__gfxs:
            if self.__vertical:
                gfx.y += value
                gfx.y = min(self.__limits[2], max(self.__limits[3], gfx.y))
            else:
                gfx.x += value
                gfx.x = min(self.__limits[1], max(self.__limits[0], gfx.x))


    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, axis, gfxs, limits, vertical=False):
        super().__init__(name)
        self.__gfxs = gfxs
        self.__axis = axis
        self.__limits = limits
        self.__vertical = vertical


from ecsv3.core.component.script.script_comp import ScriptComponent


class MoveOneWay(ScriptComponent):

    SPEED = 30

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        # Move + limits
        value = self.__axis.value * MoveOneWay.SPEED * delta_time * 60
        for gfx in self.__gfxs:
            # turn until angle is 0
            gfx.angle *= 0.66
            if abs(gfx.angle) < 0.5:
                gfx.angle = 0
            if self.__vertical:
                # update position
                gfx.y += value
                gfx.y = min(self.__limits[2] - self.__margin,
                            max(self.__limits[3] + self.__margin, gfx.y))

            else:
                # update position
                gfx.x += value
                gfx.x = min(self.__limits[1] - self.__margin,
                            max(self.__limits[0] + self.__margin, gfx.x))

        # hide one gfx according to move way
        if len(self.__gfxs) > 2:
            if value > 0 :
                self.__gfxs[0].alpha = 0
                self.__gfxs[1].alpha = 255
            if value < 0 :
                self.__gfxs[0].alpha = 255
                self.__gfxs[1].alpha = 0
        # tilt horizontal movement sprites
        vpos = 10
        vneg = -10
        if self.__flipH:
            vpos = -10
            vneg = 10
        for gfx in self.__gfxs:
            if 'shadow' not in gfx.name:
                if value > 0:
                    gfx.angle = vpos
                if value < 0:
                    gfx.angle = vneg

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, axis, gfxs, limits, vertical=False, margin=75, flipH=False):
        super().__init__(name)
        self.__gfxs = gfxs
        self.__axis = axis
        self.__limits = limits
        self.__vertical = vertical
        self.__margin = margin
        self.__flipH = flipH
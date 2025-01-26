import math

from ecsv3.core.component.script.script_comp import ScriptComponent


class MoveBubble(ScriptComponent):

    SPEED = 10
    MAX_DST = 150

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        # print('--------------------------------------')
        # print(self)
        # print('--------------------------------------')
        for ent in self.__ent_lst:
            ang = 0
            gfx = None
            for comp in ent:
                if 'gfx_' in comp.name:
                    gfx = comp
                if 'ang_' in comp.name:
                    ang = comp.angle
            ang = ang * math.pi / 180
            gfx.move(math.cos(ang) * MoveBubble.SPEED,
                     math.sin(ang) * MoveBubble.SPEED)
            # check collision
            # TODO
            # check limits +
            v1 = [-gfx.x, gfx.x, gfx.y, -gfx.y]
            v2 = [-self.__limits[0], self.__limits[1], self.__limits[2], -self.__limits[3]]
            dst = 0
            for i in range(4):
                if v1[i] >= v2[i]:
                    dst = max(dst, abs(v1[i] - v2[i]))
            # update alpha
            gfx.alpha = int(255 * max(0, MoveBubble.MAX_DST-dst)/MoveBubble.MAX_DST)
            # Remove entity
            if dst > MoveBubble.MAX_DST:
                self.__ent_lst.remove(ent)
                ent.scene.remove_entity(ent.name)



    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, limits, ent_lst):
        super().__init__(name)
        self.__limits  = limits
        self.__ent_lst = ent_lst

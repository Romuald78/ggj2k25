
from ecsv3.core.component.script.script_comp import ScriptComponent


class MoveBubble(ScriptComponent):

    SPEED = 30

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
                    ang = comp
            # print(ang.angle, gfx)
        # print()
    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, limits, ent_lst):
        super().__init__(name)
        self.__limits  = limits
        self.__ent_lst = ent_lst

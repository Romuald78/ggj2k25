
from ecsv3.core.component.script.script_comp import ScriptComponent
from ecsv3.utils.logs import ECSv3


class Fade(ScriptComponent):

    FADE_TIME = 4

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        self.__timer += delta_time

        if self.__timer >= Fade.FADE_TIME:
            self.__timer -= Fade.FADE_TIME
            if self.__idx < len(self.__gfx):
                self.__gfx[self.__idx].alpha = 0
                self.__idx += 1

        if self.__idx < len(self.__gfx):
            hlf = Fade.FADE_TIME/2
            prc = 1.0 - abs(self.__timer - hlf) / hlf
            self.__gfx[self.__idx].alpha = int(255 * prc)
        else:
            self.entity.world.switch_to_scene('Splash')


    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, gfx_list, win_size):
        super().__init__(name)
        self.__gfx   = gfx_list
        self.__timer = 0
        self.__idx   = 0
        self.__W, self.__H = win_size

        for g in self.__gfx:
            g.x = self.__W // 2
            g.y = self.__H // 2
            g.resize(self.__W, self.__H)
            g.alpha = 0


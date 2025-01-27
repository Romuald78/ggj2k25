from ecsv3.arcade_layer.components.arcade_gfx import ArcadeText
from ecsv3.core.component.gfx.gfx_comp import GfxAnchor
from ecsv3.core.component.script.script_comp import ScriptComponent


class ShowScore(ScriptComponent):


    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        self.__timer += delta_time
        if self.__timer > 0.66:
            self.__timer -= 0.66
            heroes = ['ONDINE', 'SPARK', 'TINKER BELL', 'DOOM']
            names  = ['score1', 'score2', 'score3', 'score4']
            align  = [GfxAnchor.LEFT, GfxAnchor.RIGHT, GfxAnchor.LEFT, GfxAnchor.RIGHT]
            colors = [(0, 0, 220),(255, 255, 64),(0, 220, 0),(255, 0, 0)]
            posix  = [1/5, 4/5, 1/5, 4/5]
            posiy  = [4/5, 4/5, 1/5, 1/5]
            for name in names:
                for comp in self.__ent:
                    if comp.name == name:
                        print(comp, self.__ent)
                        self.__ent.remove_one_component(comp)
                        break
            for i in range(4):
                msg = f"{heroes[i]} : {self.__scores[i]}"
                score = ArcadeText(names[i], msg = msg,
                                   w=RATIO * 1920/5,
                                   size=32,
                                   anchor=align[i],
                                   font='Super Kinds',
                                   clr=colors[i],
                                   priority=95)
                score.x = posix[i]
                score.y = posiy[i]
                self.__ent.add_component(score)

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, ent_score, scores):
        super().__init__(name)
        self.__timer = 0
        self.__ent = ent_score
        self.__scores = scores

from ecsv3.core.component.script.script_comp import ScriptComponent


class GenBubbleScript(ScriptComponent):

    INTERVAL = 1

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        self.__timer += delta_time
        if self.__timer >= 1:
            self.__timer -= 1
            # create projectile entity using factory
            ent_bub = self.__factory.create()
            # add entity to property list
            self.__ents.append(ent_bub)
            # add entity to scene
            self.entity.scene.add_entity(ent_bub)


    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, bubfact, bubble_list):
        super().__init__(name)
        self.__timer   = 0
        self.__factory = bubfact
        self.__ents    = bubble_list

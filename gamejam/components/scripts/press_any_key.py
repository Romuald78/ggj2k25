
from ecsv3.core.component.script.script_comp import ScriptComponent


class PressAnyKey(ScriptComponent):

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        for key in self.__keys:
            if key.falling_edge:
                # process callback if needed
                res = True
                if self.__cb is not None:
                    res = self.__cb(key.last_source)
                # get controller id from key component
                if res:
                    self.entity.world.switch_to_scene(self.__next, enter_params={'source_id' : key.last_source})
                    break

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, keys, nxt_scn_name, callback=None):
        super().__init__(name)
        self.__keys = keys
        self.__next = nxt_scn_name
        self.__cb   = callback


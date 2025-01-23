from ecsv3.core.component.component import Component
from ecsv3.core.component.script.script_comp import ScriptComponent
from ecsv3.utils.logs import ECSv3


class InputCallback(ScriptComponent):

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        for btn in self.__btns:
            if btn.falling_edge:
                # print(self, btn, btn.last_source)
                self.__cb(btn.last_source)
                # self.__cb('gamepad_1')
                # self.__cb('gamepad_4')



    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, buttons, callback, priority=1):
        super().__init__(name, priority)
        self.__cb = callback
        self.__btns = buttons



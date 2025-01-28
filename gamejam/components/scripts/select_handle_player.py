
from ecsv3.core.component.script.script_comp import ScriptComponent


class HandlePlayer(ScriptComponent):


    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        if self.__buttAdd.falling_edge:
            # reset risingEdge
            dummy = self.__buttAdd.rising_edge
            # call callback add
            self.__cbAdd(self.__buttAdd.last_source)

        if self.__buttRmv.falling_edge:
            # reset risingEdge
            dummy = self.__buttRmv.rising_edge
            # print('last source REMOVE = ', )
            self.__cbRmv(self.__buttRmv.last_source)


    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, buttAdd, buttRmv, cbAdd, cbRmv):
        super().__init__(name)
        self.__buttAdd = buttAdd
        self.__buttRmv = buttRmv
        self.__cbAdd = cbAdd
        self.__cbRmv = cbRmv

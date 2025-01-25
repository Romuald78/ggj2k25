from ecsv3.core.component.data.data_comp import DataComponent
from ecsv3.core.component.script.script_comp import ScriptComponent
from ecsv3.utils.logs import ECSv3


class DataAngle(DataComponent):

    @property
    def angle(self):
        return self.__angle

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, angle):
        super().__init__(name)
        self.__angle = angle



from ecsv3.core.component.component import Component


class InputComponent(Component):

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, priority, evt_type):
        super().__init__(name, priority)
        self.__evt_type = evt_type

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def event_type(self):
        return self.__evt_type

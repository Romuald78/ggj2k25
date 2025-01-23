from ecsv3.core.component.input.input_comp import InputComponent


class InputAxis(InputComponent):

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, priority, event_type, code, source=None, dead_zone=0):
        super().__init__(name, priority, event_type)
        self.__value  = 0
        self.__delta  = 0
        self.__dead   = dead_zone
        self.__source = source
        self.__code   = code

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def source_id(self):
        return self.__source

    @property
    def code_id(self):
        return self.__code

    @property
    def value(self):
        return self.__value

    @property
    def delta(self):
        return self.__delta

    # -----------------------------------------
    # METHODS
    # -----------------------------------------
    def update_value(self, source, code, new_value):
        if abs(new_value) <= self.__dead:
            new_value = 0
        self.__delta = new_value - self.__value
        self.__value = new_value


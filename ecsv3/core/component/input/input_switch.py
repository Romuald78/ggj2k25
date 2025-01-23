from ecsv3.core.component.input.input_comp import InputComponent


class InputSwitch(InputComponent):

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, priority, event_type, code=None, source=None, init_state=False):
        super().__init__(name, priority, event_type)
        self.__value    = init_state
        self.__rise     = False
        self.__fall     = False
        self.__source   = source
        self.__code     = code
        self.__last_src = None
        self.__last_cd  = None

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
    def rising_edge(self):
        # WARNING : this property can be read only once before being reset.
        #           It is important for this component to be used by only
        #           one script at a time to avoid issues
        ret = self.__rise
        self.__rise = False
        return ret

    @property
    def falling_edge(self):
        # WARNING : this property can be read only once before being reset.
        #           It is important for this component to be used by only
        #           one script at a time to avoid issues
        ret = self.__fall
        self.__fall = False
        return ret

    @property
    def last_source(self):
        return self.__last_src

    @property
    def last_code(self):
        return self.__last_cd

    # -----------------------------------------
    # METHODS
    # -----------------------------------------
    def clear(self):
        self.__rise     = False
        self.__fall     = False
        self.__last_src = None
        self.__last_cd  = None

    def update_value(self, source, code, new_value):
        self.__last_src = source
        self.__last_cd  = code
        if new_value != self.__value:
            # update if any change
            self.__rise = self.__rise or new_value
            self.__fall = self.__fall or (not new_value)
        # update anyway
        self.__value = new_value


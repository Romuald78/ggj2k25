from ecsv3.core.scenes.loader_scene import LoaderScene
from ecsv3.utils.logs import ECSv3
from ecsv3.utils.structures import add_entry_with_name


# TODO : handle remove from memory (world, scene, system, entity, component, ...)

class World:

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name='world0', load_img={}, load_scn=[], load_fnt={}):
        self.__name            = name
        self.__scenes          = {}
        self.__current_scene   = None
        self.__next_scene      = None
        self.__switch_duration = None
        self.__enter_params    = None
        self.__exit_params     = None
        self.__load_scn        = load_scn
        self.__load_img        = load_img
        self.__load_fnt        = load_fnt
        self.__window_app      = None
        self.__debug           = False

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, value):
        self.__debug = value

    def set_window(self, win):
        self.__window_app = win

        # add Loader scene by default as the very first one
        # if there is something to run
        if len(self.__load_scn) > 0 and len(self.__load_img) > 0:
            first_scene_name = self.__load_scn[0][0]
            LoaderScene(self, first_scene_name, self.__load_img, self.__load_fnt)
        else:
            ECSv3.error("No scene to add to this world !")

    # load all scenes when loader has finished its job
    def load_all_scenes(self):
        # Load all scenes
        for scn in self.__load_scn:
            scn_name, scn_class = scn
            scn_class(self, scn_name)

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def name(self):
        return self.__name

    @property
    def window(self):
        return self.__window_app

    # -----------------------------------------
    # WORLD-SCENE LINK
    # -----------------------------------------
    def add_scene(self, scene):
        # common process to add an entry in a dictionary
        add_entry_with_name(self.__scenes, scene)
        # select scene if needed
        if len(self.__scenes) == 1:
            self.__current_scene = scene

    def switch_to_scene(self, scene_name, duration=0.0, enter_params=None, exit_params=None):
        if scene_name not in self.__scenes:
            ECSv3.warning(f"Impossible to switch to scene ({scene_name}) : not found!")
        # exit from previous scene
        self.__current_scene.exit(exit_params)
        # Store next scene and duration
        self.__next_scene = self.__scenes[scene_name]
        self.__switch_duration = duration
        # store next scene parameters
        self.__enter_params = enter_params
        self.__exit_params  = exit_params

    # TODO stop update when switching from one scene to another ???
    def update(self, delta_time=1/60):
        if self.__switch_duration is not None:
            if self.__switch_duration > 0.0:
                # switch between two scene is in progress
                self.__switch_duration -= delta_time
            else:
                # exit old scene
                self.__current_scene.exit(self.__exit_params)
                self.__exit_params     = None
                # switch is over
                self.__switch_duration = None
                self.__current_scene   = self.__next_scene
                self.__next_scene      = None
                # enter new scene
                self.__current_scene.enter(self.__enter_params)
                self.__enter_params    = None
        # UPDATE SCENE
        self.__current_scene.update(delta_time)

    def draw(self):
        # DRAW SCENE
        self.__current_scene.draw()

    # TODO avoid events when switching from one scene to another ???
    def event(self, evt_type, value):
        # EVENTS
        self.__current_scene.event(evt_type, value)

    # -----------------------------------------
    # UTILITY METHODS
    # -----------------------------------------
    def __str__(self):
        out  = 'World {\n'
        for scene_name in self.__scenes:
            cur = ' '
            if self.__current_scene == self.__scenes[scene_name]:
                cur = '>'
            out += f"  {cur} {self.__scenes[scene_name]}\n"
        out += '}'
        return out

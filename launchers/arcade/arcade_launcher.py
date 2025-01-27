
import arcade

from ecsv3.core.system.system_types import EventType
from launchers.arcade.default_config import *

GAMEPAD_XBOX = [
    'A', 'B', 'X', 'Y', 'LB', 'RB', 'BACK', 'START', '???', 'L', 'R'
]

GAMEPAD_GAMECUBE = [
    'X', 'A', 'B', 'Y', 'LB', '???', '???', 'BACK', '???', 'START'
]

class ArcadeApp(arcade.Window):

    @staticmethod
    def __getButtonName(ctrlr, buttonNum):
        result = '???'
        buttonValues = GAMEPAD_XBOX
        name = ctrlr.device.name.lower()
        # Check name of controller and adjust buttonValues list if needed
        if 'mayflash' in name and 'gamecube' in name:
            buttonValues = GAMEPAD_GAMECUBE
        # check if button number is in the list
        if buttonNum < len(buttonValues):
            result = buttonValues[buttonNum]
        # Return button name according to controller mapping
        return result

    def __init__(self, world, width=1920, height=1080, title = 'ECSv3 Arcade App'):
        super().__init__(width, height, title)
        self.__world      = world
        self.__game_ctrl  = {}
        self.__displayFPS = False
        self.__frame_time = 0.016666

        # get window and give access to world
        self.__world.set_window(self)


        # TODO
        # # Add camera
        # self.__main_camera = arcade.camera.Camera2D(
        #                                 viewport=LRBT(0, self.screen.width,
        #                                               0, self.screen.height),
        #                                 projection=LRBT(0, width, 0, height),
        #                                 position=(0, 0)
        #                                 )

        # get ___game controllers
        gamepads = arcade.get_game_controllers()
        i = 1
        if len(gamepads) == 0:
            print("[INFO] No gamepad connected.")
        for ctrl in gamepads:
            print(f"[INFO] found gamepad #{i} : {ctrl}")
            ctrl.on_joybutton_press   = self.on_button_pressed
            ctrl.on_joybutton_release = self.on_button_released
            ctrl.on_joyaxis_motion    = self.on_axis_move
            # Open each gamepad controller
            ctrl.open(self)
            self.__game_ctrl[ctrl] = i
            i += 1

        self.__world.set_controllers(self.__game_ctrl)

    def on_update(self, delta_time):
        self.__world.update(delta_time)
        self.__frame_time = delta_time

    def on_draw(self):
        self.clear()
        # TODO Camera
        # self.__main_camera.use()
        self.__world.draw()
        if self.__displayFPS:
            fps = ('00' + str(int(round(1/self.__frame_time, 0))))[-2:]
            arcade.draw_text(f"{fps}", font_size=30,
                             x=10, y=self.height-40,
                             color=(255,0,255))

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        elif symbol == arcade.key.F10:
            self.__displayFPS = not self.__displayFPS
            self.__world.debug = not self.__world.debug
        elif symbol == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        else:
            self.__world.event(EventType.KEY_BUTTON, ('keyboard', symbol, True))

    def on_key_release(self, symbol: int, modifiers: int):
        self.__world.event(EventType.KEY_BUTTON, ('keyboard', symbol, False))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.__world.event(EventType.MOUSE_BUTTON, ('mouse', button, True, x, y))

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.__world.event(EventType.MOUSE_BUTTON, ('mouse', button, False, x, y))

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.__world.event(EventType.MOUSE_AXIS, ('mouse', 'x', x))
        self.__world.event(EventType.MOUSE_AXIS, ('mouse', 'y', y))

    def on_button_pressed(self, ctrl, button_id):
        gamepad_id  = self.__game_ctrl[ctrl]
        button_name = ArcadeApp.__getButtonName(ctrl, button_id)
        self.__world.event(EventType.PAD_BUTTON, (f"gamepad_{gamepad_id}", button_name, True))

    def on_button_released(self, ctrl, button_id):
        gamepad_id  = self.__game_ctrl[ctrl]
        button_name = ArcadeApp.__getButtonName(ctrl, button_id)
        self.__world.event(EventType.PAD_BUTTON, (f"gamepad_{gamepad_id}", button_name, False))

    def on_axis_move(self, ctrl, axis_id, value):
        # invert y value to have
        # negative values downward and
        # positive values upward
        if axis_id == 'y' or axis_id == 'ry':
            value = -value
        # Get gamepad ID from controller reference
        gamepad_id = self.__game_ctrl[ctrl]
        # Send events
        self.__world.event(EventType.PAD_AXIS, (f"gamepad_{gamepad_id}", axis_id.upper(), value))


def run(world, config):

    w = arcade.get_screens()[0].width
    h = arcade.get_screens()[0].height
    ScreenRatio.set_ratio(w, h)

    # Create arcade app and configure it
    app = ArcadeApp(world,
                    width=w,
                    height=h,
                    title=config['title'])
    app.set_mouse_visible(config['mouse_visible'])
    app.set_fullscreen(config['full_screen'])
    # Show time !
    arcade.run()





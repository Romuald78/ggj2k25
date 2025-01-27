from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.entity import Entity
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem
from gamejam.components.scripts.press_any_key import PressAnyKey
from launchers.arcade.default_config import ScreenRatio


class Splash(Scene):

    def __init__(self, world, name):
        super().__init__(world, name)

        # =========================================
        # LOCALS
        # =========================================

        RATIO = float(ScreenRatio.get_ratio())

        # =========================================
        # SYSTEMS
        # =========================================
        # input system
        system = InputSystem('Inputs', priority=1)
        self.add_system(system, SystemGroup.EVENT)
        # script system
        system = ScriptSystem('Scripts', priority=2)
        self.add_system(system, SystemGroup.UPDATE)
        # gfx system (arcade here)
        system = ArcadeGfxSystem('Gfx', priority=3)
        self.add_system(system, SystemGroup.DRAW)

        # =========================================
        # CONTENT (entities + components)
        # =========================================
        # controls (go to next scene)
        self.__controls = Entity('splash_ctrls')
        button = GamepadButton('start_button')
        press = PressAnyKey('press_any_key', [button], 'Select')
        self.__controls.add_component(button)
        self.__controls.add_component(press)

        # Background
        self.__staticGfx = Entity('static_gfx')
        gfx_bg = ArcadeFixed('splash', 'background')
        gfx_bg.scale *= RATIO
        gfx_bg.x = self.width / 2
        gfx_bg.y = self.height / 2
        self.__staticGfx.add_component(gfx_bg)

        # Add all entities
        self.add_entity(self.__staticGfx)
        self.add_entity(self.__controls)


    def enter(self, params=None):
        pass

    def exit(self, params=None):
        pass



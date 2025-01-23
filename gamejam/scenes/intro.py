from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.component.input.keyboard.key_toggle import KeyToggle
from ecsv3.core.entity import Entity
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem
from gamejam.components.scripts.intro_fade import Fade
from gamejam.components.scripts.press_any_key import PressAnyKey


class Intro(Scene):

    def __init__(self, world, name):
        super().__init__(world, name)

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

        # Create gfx and script
        gfx_rph     = ArcadeFixed('rphstudio' , 'rphstudio')
        gfx_gamejam = ArcadeFixed('gamejam', 'gamejam')
        gfx_arcade  = ArcadeFixed('arcade' , 'arcade' )
        fade    = Fade('scr_fade', [gfx_gamejam, gfx_arcade, gfx_rph], self.world.window.viewport[-2:])

        # input (keyboard + script)
        key1 = KeyToggle('key_press_start')
        btn1 = GamepadButton('btn_press_start')
        scr_start = PressAnyKey('intro_start', [key1, btn1], 'Splash')

        # create entity and add scripts
        backgrounds = Entity('backgrounds')
        backgrounds.add_component(gfx_rph)
        backgrounds.add_component(gfx_gamejam)
        backgrounds.add_component(gfx_arcade)
        backgrounds.add_component(fade)
        backgrounds.add_component(key1)
        backgrounds.add_component(btn1)
        backgrounds.add_component(scr_start)

        # Add entities to scene
        self.add_entity(backgrounds)


    def enter(self, params=None):
        pass

    def exit(self, params=None):
        pass



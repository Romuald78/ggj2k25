from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.entity import Entity
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem


class InGame(Scene):


    def __init__(self, world, name):
        super().__init__(world, name)

        # =========================================
        # LOCALS
        # =========================================


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
        # GFX
        # =========================================
        self.__staticGfx = Entity('static_gfx')
        # Background
        gfx_bg = ArcadeFixed('ingame', 'background')
        gfx_bg.x = self.width / 2
        gfx_bg.y = self.height / 2
        self.__staticGfx.add_component(gfx_bg)



        self.add_entity(self.__staticGfx)

    def enter(self, params=None):
        pass

    def exit(self, params=None):
        pass



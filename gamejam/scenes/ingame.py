import random

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.entity import Entity
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem
from gamejam.entities.player_entity import PlayerCreation
from gamejam.entities.player_select import PlayerSelect


class InGame(Scene):

    SIZE = 350


    def __init__(self, world, name):
        super().__init__(world, name)

        # =========================================
        # LOCALS
        # =========================================
        self.__players = {}

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
        gfx_bg.resize(width=self.height, height=self.height, keepRatio=False)
        self.__staticGfx.add_component(gfx_bg)


        # Register entities
        self.add_entity(self.__staticGfx)

    def enter(self, params=None):
        # define player positions according to number of players
        # if only two players select left and right only
        positions = [(-1, 0), (1, 0)]
        if len(params) == 3:
            # select random up/down
            v = (random.randint(0,1) * 2) - 1
            positions.append((0, v))
        elif len(params) == 4:
            positions.append((0, -1))
            positions.append((0, 1))
        # shuffle positions
        random.shuffle(positions)

        self.__playerCfg = params
        # Create all player entities
        i = 0
        for ctrlID in self.__playerCfg:
            eltID = params[ctrlID]['elemental']
            pos   = positions[i]
            i += 1
            play_ent = PlayerCreation(f"play_ent_{ctrlID}",
                                      ctrlID, eltID, pos,
                                      self.width, self.height)
            self.__players[ctrlID] = play_ent
            self.add_entity(play_ent)

    def exit(self, params=None):
        pass



import random

import arcade

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.entity import Entity
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem
from gamejam.components.scripts.gen_bubble import GenBubbleScript
from gamejam.components.scripts.move_bubble import MoveBubble
from gamejam.entities.bubble_factory import BubbleFactory
from gamejam.entities.player_entity import PlayerCreation
from launchers.arcade.default_config import RATIO


class InGame(Scene):

    def getFactoryFromID(self, eltID, noEltID):
        while eltID not in self.__factories or eltID == noEltID:
            eltID = (eltID + 1)
            if eltID > 4:
                eltID = 1
        return self.__factories[eltID]

    SIZE = 150 * RATIO
    MARGIN = SIZE / 5

    def __init__(self, world, name):
        super().__init__(world, name)

        self.__music = arcade.Sound('resources/sounds/music.mp3')
        self.__music.play()

        # =========================================
        # LOCALS
        # =========================================
        self.__players   = {}
        self.__bubbles   = {}
        self.__factories = {}

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
        gfx_bg1 = ArcadeFixed('back_land1', 'back_land1', priority=5)
        gfx_bg1.color = (230,230,255)
        gfx_bg2 = ArcadeFixed('back_land2', 'back_land2', priority=5)
        gfx_bg2.color = (255,255,230)
        gfx_bg3 = ArcadeFixed('back_land3', 'back_land3', priority=5)
        gfx_bg3.color = (230,255,230)
        gfx_bg4 = ArcadeFixed('back_land4', 'back_land4', priority=5)
        gfx_bg4.color = (255,230,230)
        cross   = ArcadeFixed('cross', 'cross', priority=6)
        self.__allgfx_bg = [gfx_bg1, gfx_bg2, gfx_bg3, gfx_bg4, cross]
        for gfx in self.__allgfx_bg:
            gfx.x = 10000
            gfx.y = 10000
            self.__staticGfx.add_component(gfx)

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
        final_angles = []
        final_gfx    = []
        landW = self.width
        landH = self.height - InGame.SIZE
        for ctrlID in self.__playerCfg:

            # PLAYER
            eltID = params[ctrlID]['elemental']
            pos   = positions[i]
            i += 1
            play_ent = PlayerCreation(f"play_ent_{ctrlID}",
                                      ctrlID, eltID, pos,
                                      landW, landH,
                                      InGame.SIZE, InGame.MARGIN)
            self.__players[ctrlID] = play_ent

            # add entry into the bubble dictionary
            self.__bubbles[ctrlID] = []

            # Create bub factory (one per player)
            bub_fact = BubbleFactory(self.width, self.height - InGame.SIZE, ctrlID, pos, eltID)
            self.__factories[eltID] = bub_fact

            # create move bubble component for each player and add component to the player
            scrmov = MoveBubble(f"mvbub_{ctrlID}",
                                play_ent.limits,
                                self.__bubbles[ctrlID],
                                self.__players[ctrlID], ctrlID, eltID, pos, bub_fact, self.getFactoryFromID)
            play_ent.add_component(scrmov)

            # add player entity to scene
            self.add_entity(play_ent)

            # CREATE bubble generator entity
            bub_gen_ent = Entity(f"bub_gen_ent_{ctrlID}")
            gen_script  = GenBubbleScript(f"gen_bub_scr{ctrlID}", bub_fact, self.__bubbles[ctrlID])
            bub_gen_ent.add_component(gen_script)
            self.add_entity(bub_gen_ent)

            # resize, move, rotate
            land = self.__staticGfx[f"back_land{eltID}"]
            final_gfx.append(land)
            if pos == (-1, 0):
                # no rotation
                final_angles.append(0)
            elif pos == (1, 0):
                final_angles.append(180)
            elif pos == (0, -1):
                final_angles.append(270)
            elif pos == (0, 1):
                final_angles.append(90)

        for gfx in self.__allgfx_bg:
            if gfx not in final_gfx:
                final_gfx.append(gfx)
                for a in range(4):
                    if a*90 not in final_angles:
                        final_angles.append(a*90)
                        break
            gfx.x = landW / 2
            gfx.y = landH / 2
            gfx.resize(landW, landH)

        for i in range(4):
            final_gfx[i].angle = final_angles[i]
            # print(final_gfx[i], final_angles[i])


    def exit(self, params=None):
        pass


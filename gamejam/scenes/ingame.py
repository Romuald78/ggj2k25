import random

import arcade

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.entity import Entity
from ecsv3.core.loader.loader import ResourceLoader
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem
from gamejam.components.scripts.gen_bubble import GenBubbleScript
from gamejam.components.scripts.move_bubble import MoveBubble
from gamejam.entities.bubble_factory import BubbleFactory
from gamejam.entities.bubble_sides import BubbleSide
from gamejam.entities.player_entity import PlayerCreation
from gamejam.utils.path_utils import get_path
from launchers.arcade.default_config import ScreenRatio


SND_DIR = get_path('resources/sounds')

class InGame(Scene):

    def getFactoryFromID(self, eltID, noEltID):
        while eltID not in self.__factories or eltID == noEltID:
            eltID = (eltID + 1)
            if eltID > 4:
                eltID = 1
        return self.__factories[eltID]


    def __init__(self, world, name):
        super().__init__(world, name)

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

        # Score ENTITY
        self.__scores = [0, 0, 0, 0]



        # TODO run sound object (from loader)
        self.__music = ResourceLoader.getSoundReference('music')



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
        backing = ArcadeFixed('back_ingame', 'back_ingame')
        backing.resize(width=self.width, height=self.height, keepRatio=False)
        backing.x = self.width / 2
        backing.y = self.height / 2
        self.__staticGfx.add_component(backing)

        hro1 = ArcadeFixed('front_hero1', 'face1', priority=56)
        hro2 = ArcadeFixed('front_hero2', 'face2', priority=56)
        hro3 = ArcadeFixed('front_hero3', 'face3', priority=56)
        hro4 = ArcadeFixed('front_hero4', 'face4', priority=56)
        self.__staticGfx.add_component(hro1)
        self.__staticGfx.add_component(hro2)
        self.__staticGfx.add_component(hro3)
        self.__staticGfx.add_component(hro4)

        cross   = ArcadeFixed('cross', 'cross', priority=6)
        self.__allgfx_bg = [gfx_bg1, gfx_bg2, gfx_bg3, gfx_bg4, cross]
        for gfx in self.__allgfx_bg:
            gfx.x = 10000
            gfx.y = 10000
            self.__staticGfx.add_component(gfx)

        # Register entities
        self.add_entity(self.__staticGfx)

        self.__guipos = []
        self.__names  = ['ONDINE', 'SPARK', 'TINKER BELL', 'DOOM']
        self.__colors = [(128,128,255), (255,255,128), (128,255,128), (255,128,128)]

        self.__sprlst = None

        # BUBBLE SIDES
        RATIO = ScreenRatio.get_ratio()
        CHAR_SIZE = 150 * RATIO
        bandW = (self.width - (self.height - CHAR_SIZE)) / 2
        # Limits (Left Right Top Bottom)
        limitL = [0, bandW, self.height, 0]
        limitR = [self.width - bandW, self.width, self.height, 0]
        genbubL = BubbleSide('genbubL', limitL, 200 * RATIO)
        genbubR = BubbleSide('genbubR', limitR, 200 * RATIO)
        self.add_entity(genbubL)
        self.add_entity(genbubR)


    def enter(self, params=None):

        RATIO = ScreenRatio.get_ratio()
        SPEED = 30 * RATIO
        CHAR_SIZE = 150 * RATIO
        MARGIN = CHAR_SIZE / 5
        YREF = CHAR_SIZE / 10

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
        landH = self.height - CHAR_SIZE
        for ctrlID in self.__playerCfg:

            # PLAYER
            eltID = params[ctrlID]['elemental']
            pos   = positions[i]
            i += 1
            play_ent = PlayerCreation(f"play_ent_{ctrlID}",
                                      ctrlID, eltID, pos,
                                      landW, landH,
                                      CHAR_SIZE, MARGIN, YREF)
            self.__players[ctrlID] = play_ent

            # add entry into the bubble dictionary
            self.__bubbles[ctrlID] = []

            # Create bub factory (one per player)
            bub_fact = BubbleFactory(self.width, self.height - CHAR_SIZE, ctrlID, pos, eltID, YREF)
            self.__factories[eltID] = bub_fact

            # create move bubble component for each player and add component to the player
            scrmov = MoveBubble(f"mvbub_{ctrlID}",
                                play_ent.limits,
                                self.__bubbles[ctrlID],
                                self.__players[ctrlID], ctrlID, eltID, pos, bub_fact, self.getFactoryFromID, self.__scores)
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
                # left => BOTTOM LEFT
                self.__guipos.append({
                    'eltID' : eltID,
                    'x'     : 0.1,
                    'y'     : 0.1,
                    'gfx'   : self.__staticGfx[f"face{eltID}"]
                })

            elif pos == (1, 0):
                final_angles.append(180)
                # right => TOP RIGHT
                self.__guipos.append({
                    'eltID' : eltID,
                    'x'     : 0.9,
                    'y'     : 0.9
                })

            elif pos == (0, -1):
                final_angles.append(270)
                # bottom => BOTTOM RIGHT
                self.__guipos.append({
                    'eltID' : eltID,
                    'x'     : 0.9,
                    'y'     : 0.1
                })

            elif pos == (0, 1):
                final_angles.append(90)
                # top => TOP LEFT
                self.__guipos.append({
                    'eltID' : eltID,
                    'x'     : 0.1,
                    'y'     : 0.9,
                })

        for gfx in self.__allgfx_bg:
            if gfx not in final_gfx:
                final_gfx.append(gfx)
                for a in range(4):
                    if a*90 not in final_angles:
                        final_angles.append(a*90)
                        break
            gfx.x = landW / 2
            gfx.y = landH / 2 + YREF
            gfx.resize(landW, landH)

        for i in range(4):
            final_gfx[i].angle = final_angles[i]
            # print(final_gfx[i], final_angles[i])

        # Start music before playing
        self.__music.play(loop=True)


    def exit(self, params=None):
        pass

    def draw(self):
        super().draw()

        RATIO = ScreenRatio.get_ratio()

        self.__sprlst = arcade.SpriteList()

        # GUI (score)
        for i in range(1,5):
            self.__staticGfx[f"face{i}"].x = -10000
            self.__staticGfx[f"face{i}"].y = -10000
        for id in range(1,5):
            # Move character position
            for gui in self.__guipos:
                eltID = gui['eltID']
                if id == eltID:
                    scalex = RATIO * 1.5
                    scaley = RATIO * 1.5
                    graphics = self.__staticGfx[f"face{eltID}"]
                    msg = self.__names[eltID-1]

                    if gui['x'] < 0.5:
                        msg += ' : ' + str(self.__scores[eltID-1])
                        xt = 1/20
                        xg = 1/10
                        algn = 'left'
                        scalex = -scalex
                    else:
                        msg = str(self.__scores[eltID-1]) + ' : ' + msg
                        xt = 19/20
                        xg = 9/10
                        algn = 'right'
                    if gui['y'] < 0.5:
                        yg = 1/5
                        yt = 2/5
                    else:
                        yg = 4/5
                        yt = 3/5

                    self.__staticGfx[f"face{eltID}"].gfx_object.scale   = scaley
                    self.__staticGfx[f"face{eltID}"].gfx_object.scale_x = scalex
                    self.__staticGfx[f"face{eltID}"].x = xg * self.width
                    self.__staticGfx[f"face{eltID}"].y = yg * self.height

                    spr = arcade.create_text_sprite(msg,
                                                    color=self.__colors[eltID-1],
                                                    font_size=30 * RATIO,
                                                    font_name='Super Kinds')
                    spr.center_x = (xt * self.width)
                    spr.center_y = (yt * self.height)

                    if algn == 'right':
                        spr.center_x -= spr.width / 2
                    else:
                        spr.center_x += spr.width / 2

                    self.__sprlst.append(spr)
        self.__sprlst.draw()

        # hro1.x = self.width * 1/10
        # hro2.x = self.width * 9/10
        # hro3.x = self.width * 1/10
        # hro4.x = self.width * 9/10
        # hro1.y = self.height * 4/5
        # hro2.y = self.height * 4/5
        # hro3.y = self.height * 1/5
        # hro4.y = self.height * 1/5


        # arcade.draw_text(f"ONDINE : {self.__scores[0]}", font_size=15,
        #                  x=self.width * 1/20 * RATIO  ,
        #                  y=self.height* 9/10 *RATIO,
        #                  color=(128, 128, 255),
        #                  align='left')
        #
        # arcade.draw_text(f"{self.__scores[1]} : SPARK", font_size=15,
        #                  x=self.width * 19/20 * RATIO  ,
        #                  y=self.height* 9/10 *RATIO,
        #                  color=(255, 255, 128),
        #                  align='right')
        #
        # arcade.draw_text(f"TINKER BELL : {self.__scores[2]}", font_size=15,
        #                  x=self.width * 1/20 * RATIO  ,
        #                  y=self.height* 6/10 *RATIO,
        #                  color=(128, 255, 128),
        #                  align='left')
        # arcade.draw_text(f"{self.__scores[3]} : DOOM", font_size=15,
        #                  x=self.width * 19/20 * RATIO  ,
        #                  y=self.height* 6/10 *RATIO,
        #                  color=(255, 128, 128),
        #                  align='right')


# colors = [,(255, 255, 64),(0, 220, 0),(255, 0, 0)]
#
# heroes = ['ONDINE', 'SPARK', 'TINKER BELL', 'DOOM']
# for hero in heroes:

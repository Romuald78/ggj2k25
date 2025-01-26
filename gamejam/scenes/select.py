from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.component.input.gamepad.gamepad_button import GamepadButton
from ecsv3.core.entity import Entity
from ecsv3.core.scenes.scene import Scene, SystemGroup
from ecsv3.arcade_layer.systems.arcade_gfx_system import ArcadeGfxSystem
from ecsv3.core.system.input_system import InputSystem
from ecsv3.core.system.script_system import ScriptSystem
from gamejam.components.scripts.select_handle_player import HandlePlayer
from gamejam.components.scripts.select_highlight import SelectHighLight
from gamejam.entities.player_select import PlayerSelect


class Select(Scene):

    SIZE = 400

    def add_player(self, ctrlID):

        if ctrlID not in self.__players:
            # player has just arrived
            # add entity to the world (and list)
            ent = PlayerSelect(f"player_{ctrlID}", ctrlID,
                               self.width / 2, self.height / 2,
                               [100, self.width-100, self.height-100, 100],
                               self.__players, self.__gfx_pos)
            self.add_entity(ent)
            # add player to the list
            self.__players[ctrlID] = {'entity'   : ent,
                                      'selected' : False,
                                      'elemental': None
                                      }

        elif not self.__players[ctrlID]['selected']:
            # Select player if it is in a correct place
            ent = self.__players[ctrlID]['entity']
            gfx_bubble = ent[f"bubble_select_{ctrlID}"]
            # check if position is near a valid selection
            # print("position bubble ", gfx_bubble.x, gfx_bubble.y)
            for gp in self.__gfx_pos:
                # print(gp.name, gp.x, gp.y)
                dst2 = gfx_bubble.distance2To(gp)
                if dst2 <= Select.SIZE**2 / 4:
                    # we can select it : check if there is no another player
                    ok2select = True
                    for p in self.__players:
                        if p != ctrlID :
                            if self.__players[p]['selected'] and self.__players[p]['elemental'] == self.__gfx_pos.index(gp) + 1:
                                ok2select = False
                                break
                    if ok2select:
                        # now select this player to this hero
                        self.__players[ctrlID]['selected'] = True
                        self.__players[ctrlID]['elemental'] = self.__gfx_pos.index(gp) + 1
                        gfx_bubble.scale *= 2.0
                        gfx_bubble.x = gp.x
                        gfx_bubble.y = gp.y

        else:
            next = len(self.__players) > 1
            for p in self.__players:
                if not self.__players[p]['selected']:
                    next = False
            if next:
                self.world.switch_to_scene('InGame', enter_params=self.__players)


        # print("After ADD")
        # for ctrlID in self.__players:
        #     print(ctrlID, self.__players[ctrlID])

    def remove_player(self, ctrlID):
        if ctrlID in self.__players:
            if not self.__players[ctrlID]['selected']:
                # remove entity from scene
                self.remove_entity(self.__players[ctrlID]['entity'].name)
                # remove player from list
                del self.__players[ctrlID]
            else:
                # just deselect
                self.__players[ctrlID]['selected'] = False
                ent = self.__players[ctrlID]['entity']
                gfx_bubble = ent[f"bubble_select_{ctrlID}"]
                gfx_bubble.scale /= 2
        elif len(self.__players) == 0:
            # we can go back to previous scene
            self.world.switch_to_scene('Splash')

        print("After REMOVE")
        for ctrlID in self.__players:
            print(ctrlID, self.__players[ctrlID])

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
        # CONTENT (entities + components)
        # =========================================
        # Controls
        self.__controls = Entity  ('controls')
        button_add = GamepadButton('button_add', 'A')
        button_rmv = GamepadButton('button_rmv', 'B')
        handle_ply = HandlePlayer ('handle_player',
                                   button_add, button_rmv,
                                   self.add_player, self.remove_player)
        self.__controls.add_component(button_add)
        self.__controls.add_component(button_rmv)
        self.__controls.add_component(handle_ply)


        self.__staticGfx = Entity('static_gfx')
        # Background
        gfx_bg = ArcadeFixed('select', 'background')
        gfx_bg.x = self.width / 2
        gfx_bg.y = self.height / 2
        self.__staticGfx.add_component(gfx_bg)
        # hero select
        gfx_h1 = ArcadeFixed('front_hero1', 'front_hero1', flipH=True)
        gfx_h2 = ArcadeFixed('front_hero2', 'front_hero2')
        gfx_h3 = ArcadeFixed('front_hero3', 'front_hero3')
        gfx_h4 = ArcadeFixed('front_hero4', 'front_hero4')
        gfx_h1.resize(height=Select.SIZE)
        gfx_h2.resize(height=Select.SIZE)
        gfx_h3.resize(height=Select.SIZE)
        gfx_h4.resize(height=Select.SIZE)
        gfx_h1.color = (255,255,255,192)
        gfx_h2.color = (255,255,255,192)
        gfx_h3.color = (255,255,255,192)
        gfx_h4.color = (255,255,255,192)
        dw = (self.width - (4 * Select.SIZE)) / 5
        gfx_h1.x = dw + Select.SIZE/2
        gfx_h2.x = gfx_h1.x + Select.SIZE + dw
        gfx_h3.x = gfx_h2.x + Select.SIZE + dw
        gfx_h4.x = gfx_h3.x + Select.SIZE + dw
        gfx_h1.y = 2 * self.height / 3.5
        gfx_h2.y = self.height / 4.1
        gfx_h3.y = self.height / 4.1
        gfx_h4.y = 2 * self.height / 3.5
        self.__staticGfx.add_component(gfx_h1)
        self.__staticGfx.add_component(gfx_h2)
        self.__staticGfx.add_component(gfx_h3)
        self.__staticGfx.add_component(gfx_h4)

        # store select positions
        self.__gfx_pos = [gfx_h1, gfx_h2, gfx_h3, gfx_h4]

        # add highligh script to controls
        highlight = SelectHighLight('highlight', self.__players, self.__gfx_pos)
        self.__controls.add_component(highlight)

        # Add all entities
        self.add_entity(self.__staticGfx)
        self.add_entity(self.__controls)




    def enter(self, params=None):
        pass

    def exit(self, params=None):
        pass




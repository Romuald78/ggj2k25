import math
import random

from ecsv3.core.component.script.script_comp import ScriptComponent
from ecsv3.utils.logs import ECSv3
from launchers.arcade.default_config import ScreenRatio


class MoveBubble(ScriptComponent):

    COLORS = [(0, 0, 220), 
              (255, 255, 64),
              (0, 220, 0),
              (255, 0, 0)
            ]

    POS = [(-1,0), (1, 0), (0, 1), (0, -1)]

    def __collision(self, x1, y1, x2, y2, minok):
        dx = x1 - x2
        dy = y1 - y2
        return (dx*dx + dy*dy) <= (minok*minok)

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):

        # Store button list in order to use them in the following script
        if len(self.__buttons) == 0:
            # order = LEFT RIGHT TOP BOTTOM
            # (some gamepads have different physical button positions) :
            # (the reference is the xbox controller)
            id = int(self.__ctrlID.replace('gamepad_', ''))
            name = self.entity.scene.world.getGamepadName(id)

            if 'gamecube' in name and 'mayflash' in name:
                # GAMECUBE config
                self.__buttons.append(self.__player[f"buttonB_{self.__ctrlID}"])
                self.__buttons.append(self.__player[f"buttonX_{self.__ctrlID}"])
                self.__buttons.append(self.__player[f"buttonY_{self.__ctrlID}"])
                self.__buttons.append(self.__player[f"buttonA_{self.__ctrlID}"])
            else:
                # XBOX config (default)
                self.__buttons.append(self.__player[f"buttonX_{self.__ctrlID}"])
                self.__buttons.append(self.__player[f"buttonB_{self.__ctrlID}"])
                self.__buttons.append(self.__player[f"buttonY_{self.__ctrlID}"])
                self.__buttons.append(self.__player[f"buttonA_{self.__ctrlID}"])

        RATIO = ScreenRatio.get_ratio()
        SPEED = 10 * RATIO
        MAX_DST = 0.1 * RATIO

        first_big_ent = None
        first_big_gfx = None
        x1 = self.__shadow.x
        y1 = self.__shadow.y

        destroy_distance =MAX_DST * abs(self.__limits[1] - self.__limits[0])

        self.__shadow.color = (0, 0, 0, 128)

        for ent in self.__ent_lst:
            ang = 0
            gfx = None
            for comp in ent:
                if 'gfx_' in comp.name:
                    gfx = comp
                if 'ang_' in comp.name:
                    ang = comp.angle
            ang = ang * math.pi / 180
            gfx.move(math.cos(ang) * SPEED,
                     math.sin(ang) * SPEED)
            # check collision
            x2 = gfx.x
            y2 = gfx.y
            colliding = self.__collision(x1, y1, x2, y2, self.__shadow.width / 2)

            if tuple(gfx.color)[:3] != (255,255,255) and first_big_gfx is None:
                first_big_gfx = gfx
                first_big_ent = ent

            if colliding and tuple(gfx.color)[:3] == (255,255,255):
                # ========= GET SMALL BUBBLE ===========
                self.__ent_lst.remove(ent)
                ent.scene.remove_entity(ent.name)
                # add small score
                self.__scores[self.__eltID-1] += 1
            else:
                # check limits +
                v1 = [-gfx.x, gfx.x, gfx.y, -gfx.y]
                v2 = [-self.__limits[0], self.__limits[1], self.__limits[2], -self.__limits[3]]
                dst = 0
                for i in range(4):
                    if v1[i] >= v2[i]:
                        dst = max(dst, abs(v1[i] - v2[i]))
                # update alpha
                gfx.alpha = int(255 * max(0, destroy_distance-dst)/destroy_distance)

                # Remove entity
                if dst > destroy_distance :
                    # ========= MISS BUBBLE ===========
                    self.__ent_lst.remove(ent)
                    ent.scene.remove_entity(ent.name)


        if first_big_ent is not None:
            x2 = first_big_gfx.x
            y2 = first_big_gfx.y
            colliding = self.__collision(x1, y1, x2, y2, self.__shadow.width / 2)

            if not colliding:

                self.__shadow.scale = self.__shadow_scale

                # consume all button press
                rising_flag = False
                for button in self.__buttons:
                    rising_flag = rising_flag or button.rising_edge
                if rising_flag:
                    # ========== FAIL FIRST BIG  ==========
                    # pressed a button too early or too late
                    # remove first big (if needed : may be it has been removed
                    # because of the distance (it may appear sometimes but very rarely
                    try:
                        self.__ent_lst.remove(first_big_ent)
                        first_big_ent.scene.remove_entity(first_big_ent.name)
                    except :
                        ECSv3.info('impossible to remove big bubble !')
            else:

                self.__shadow.color = (255,255,255,128)
                self.__shadow.scale = self.__shadow_scale * 1.25

                # check buttons according to color
                bubclr = tuple(first_big_gfx.color)[:3]
                idxclr = MoveBubble.COLORS.index(bubclr) + 1  # player number
                idxpos = MoveBubble.POS.index(self.__pos)
                button = self.__buttons[idxpos]

                if button.rising_edge:
                    # ========= SUCCESS BIG BUBBLE ===========
                    # remove first big
                    self.__ent_lst.remove(first_big_ent)
                    first_big_ent.scene.remove_entity(first_big_ent.name)
                    # generate new
                    eltIDs = [1,2,3,4]
                    eltIDs.remove(self.__eltID)
                    otherEltID = random.choice(eltIDs)
                    otherFact = self.__getOtherFact(otherEltID, self.__eltID)
                    otherFact.add_big_bubble(self.__ctrlID, self.__eltID)
                    # add BIG score
                    self.__scores[self.__eltID-1] += 6
                else:
                    # consume all button press
                    rising_flag = False
                    for button in self.__buttons:
                        rising_flag = rising_flag or button.rising_edge
                    if rising_flag:
                        # ========== FAIL FIRST BIG  ==========
                        # pressed a bad button while colliding
                        self.__ent_lst.remove(first_big_ent)
                        first_big_ent.scene.remove_entity(first_big_ent.name)
        else:
            # consume all button press
            rising_flag = False
            for button in self.__buttons:
                rising_flag = rising_flag or button.rising_edge

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, limits, ent_lst, player, ctrlID, eltID, pos, bubFactory, cbgetFac, scores):
        super().__init__(name)
        self.__limits  = limits
        self.__scores  = scores
        self.__ent_lst = ent_lst
        self.__player = player
        self.__loaded = False
        self.__ctrlID = ctrlID
        # store colors
        self.__eltID = eltID
        self.__pos = pos
        self.__shadow = self.__player[f"shadow_{self.__eltID}_{self.__ctrlID}"]
        self.__factory = bubFactory
        self.__getOtherFact = cbgetFac
        self.__shadow_scale = self.__shadow.scale
        self.__buttons = []




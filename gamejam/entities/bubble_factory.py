import math
import random

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.entity import Entity
from gamejam.components.data.data_bub_ang import DataAngle
from launchers.arcade.default_config import ScreenRatio


class BubbleFactory:
    COLORS = [
        (0, 0, 220),
        (255, 255, 64),
        (0, 220, 0),
        (255, 0, 0)
    ]

    @property
    def limits(self):
        return self.__limits

    @property
    def counter(self):
        return self.__count

    def __init__(self, w, h, ctrlID, vec_dir, eltID, yref):
        # left right top down
        limits = [w/2 - h/2, w/2 + h/2, h + yref, yref]
        self.__limits     = limits
        # parameters
        self.__ctrlID     = ctrlID
        self.__vec_dir    = vec_dir
        # Locals
        self.__bub2send   = []
        self.__count      = 0
        self.__dest_angle = 0   # variation destination
        self.__last_angle = 0    # last variation

        self.__color      = BubbleFactory.COLORS[eltID-1]

    def add_big_bubble(self, ctrlID, eltID):
        # add value at the end of self.__bub2send.
        clr = BubbleFactory.COLORS[eltID-1]
        self.__bub2send.append((clr))

    def create(self):
        RATIO = float(ScreenRatio.get_ratio())
        big_color = self.__color
        # increase count for bubble name
        self.__count += 1
        big = False
        if self.__count % 2 == 0 and self.__count % 12 != 0 and len(self.__bub2send) > 0:
                big = True
                big_color = self.__bub2send[0]
                self.__bub2send = self.__bub2send[1:]
        if self.__count % 12 == 0:
            big = True
        # check if we have to create a big bubble
        size = 32 * RATIO
        clr  = (255,255,255)
        if big:
            size = 65 * RATIO
            clr = big_color

        # Entity
        ent = Entity(f"bub_ent_{self.__ctrlID}_{self.__count}")
        # GFX
        texture_ref = 'bubble'
        if big:
            texture_ref += '_big'
        gfx = ArcadeFixed(texture_ref, f"gfx_{self.__ctrlID}_{self.__count}",
                          priority=55)
        gfx.x = (self.__limits[0] + self.__limits[1]) / 2
        gfx.y = (self.__limits[2] + self.__limits[3]) / 2
        gfx.resize(width=size)
        gfx.color = clr
        ent.add_component(gfx)
        # compile direction angle (random)
        MAX_ANGLE = 40
        STEP = 4.325
        angle0  = math.atan2(self.__vec_dir[1], self.__vec_dir[0]) * 180 / math.pi
        if self.__dest_angle > self.__last_angle:
            self.__last_angle += STEP
        if self.__dest_angle < self.__last_angle:
            self.__last_angle -= STEP

        diff = abs(self.__dest_angle - self.__last_angle)
        diff = max(-MAX_ANGLE, min(MAX_ANGLE, diff))

        if abs(diff) <= STEP:
            diff = 0
            if self.__dest_angle >= 0:
                self.__dest_angle = random.randint(-MAX_ANGLE, int(MAX_ANGLE/2))
            else:
                self.__dest_angle = random.randint(int(-MAX_ANGLE/2), MAX_ANGLE)

        # set new angle
        angle = angle0 + self.__last_angle
        # Add data component
        dataang = DataAngle(f"ang_{self.__ctrlID}_{self.__count}", angle)
        ent.add_component(dataang)

        return ent



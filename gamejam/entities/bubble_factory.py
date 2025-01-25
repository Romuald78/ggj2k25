import math
import random

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.entity import Entity
from gamejam.components.data.data_bub_ang import DataAngle


class BubbleFactory:

    @property
    def limits(self):
        return self.__limits

    @property
    def counter(self):
        return self.__count

    def __init__(self, w, h, pos, ctrlID, vec_dir):
        # left right top down
        limits = [w/2 - h/2, w/2 + h/2, h, 0]
        self.__limits     = limits
        # parameters
        self.__pos0       = pos
        self.__ctrlID     = ctrlID
        self.__vec_dir    = vec_dir
        # Locals
        self.__count      = 0
        self.__dest_angle = 0
        self.__last_angle = 0


    def add_big_bubble(self, ctrlID, vec_dir):
        pass
        # self.__enemy_bub.append()

    def create(self):
        # increase count for bubble name
        self.__count += 1
        # check if we have to create a big bubble
        size = 25
        if self.__count % 10 == 0:
            size = 50
        # maxangle
        MAX_ANGLE = 40


        # Entity
        ent = Entity(f"bub_ent_{self.__ctrlID}_{self.__count}")
        # GFX
        gfx = ArcadeFixed(f"bubble", f"gfx_{self.__ctrlID}_{self.__count}",
                          priority=90)
        gfx.x = (self.__limits[0] + self.__limits[1]) / 2
        gfx.y = (self.__limits[2] + self.__limits[3]) / 2
        gfx.resize(width=size)
        ent.add_component(gfx)
        # compile direction angle (random)
        angle0  = math.atan2(self.__vec_dir[1], self.__vec_dir[0]) * 180 / math.pi
        angle0 -= MAX_ANGLE
        angle1  = angle0 + (2 * MAX_ANGLE)

        angle = self.__last_angle
        angle += random.randint(-20, 20)
        angle  = min(angle1, max(angle0, angle))
        # print(angle0, angle, angle1)
        # Add data component
        dataang = DataAngle(f"ang_{self.__ctrlID}_{self.__count}", angle)
        ent.add_component(dataang)

        return ent



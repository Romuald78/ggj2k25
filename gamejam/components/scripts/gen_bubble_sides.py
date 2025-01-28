import random

from ecsv3.core.component.script.script_comp import ScriptComponent


class MoveBubbleSides(ScriptComponent):

    MIN_SPEED = 0.4
    MAX_SPEED = 4.0
    RNG_SPEED = MAX_SPEED - MIN_SPEED

    def __get_rand_params(self):
        vx  = (random.random() * MoveBubbleSides.RNG_SPEED + MoveBubbleSides.MIN_SPEED) * random.choice([1, -1])
        vy  = (random.random() * MoveBubbleSides.RNG_SPEED + MoveBubbleSides.MIN_SPEED) * random.choice([1, -1])
        clr = (random.randint(32, 255), random.randint(32, 255), random.randint(32, 255), random.randint(200, 255))
        ang = random.randint(1, 7) * random.choice([1, -1])
        return [vx, vy, clr, ang]


    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        for i in range(len(self.__gfxs)):
            g = self.__gfxs[i]
            v = self.__vect[i]
            g.x += delta_time * 60 * v[0]
            g.y += delta_time * 60 * v[1]
            if g.x < self.__limits[0] or g.x > self.__limits[1]:
                if g.x < self.__limits[0]:
                    g.x = self.__limits[0]
                if g.x > self.__limits[1]:
                    g.x = self.__limits[1]
                vect = self.__get_rand_params()
                sign1 = self.__vect[i][0] >= 0
                self.__vect[i] = vect
                sign2 = self.__vect[i][0] >= 0
                if sign1 == sign2:
                    self.__vect[i][0] = -self.__vect[i][0]
            if g.y < self.__limits[3] or g.y > self.__limits[2]:
                if g.y < self.__limits[3]:
                    g.y = self.__limits[3]
                if g.y > self.__limits[2]:
                    g.y = self.__limits[2]
                vect = self.__get_rand_params()
                sign1 = self.__vect[i][1] >= 0
                self.__vect[i] = vect
                sign2 = self.__vect[i][1] >= 0
                if sign1 == sign2:
                    self.__vect[i][1] = -self.__vect[i][1]
            # color
            r1, g1, b1, a1 = g.color
            r2, g2, b2, a2 = self.__vect[i][2]
            k = 0.90
            r3 = r1 * k + r2 * (1-k)
            g3 = g1 * k + g2 * (1-k)
            b3 = b1 * k + b2 * (1-k)
            a3 = a1 * k + a2 * (1-k)
            g.color = (r3, g3, b3, a3)
            g.angle += self.__vect[i][3]
            if abs(r3-r2) < 0.1 and abs(g3-g2) and abs(b3-b2):
                self.__vect[i][2] = self.__get_rand_params()[2]



    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, gfxs, limits):
        super().__init__(name)
        self.__limits = limits
        self.__gfxs   = gfxs
        self.__vect   = []
        for i in range(len(gfxs)):
            vect = self.__get_rand_params()
            self.__vect.append(vect)



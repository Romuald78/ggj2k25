from enum import Enum

from ecsv3.core.component.component import Component
from ecsv3.utils.logs import ECSv3


class GfxAnchor(Enum):
    TOP_LEFT     = (-1,  1)
    TOP          = ( 0,  1)
    TOP_RIGHT    = ( 1,  1)
    RIGHT        = ( 1,  0)
    BOTTOM_RIGHT = ( 1, -1)
    BOTTOM       = ( 0, -1)
    BOTTOM_LEFT  = (-1, -1)
    LEFT         = (-1,  0)
    CENTER       = ( 0,  0)

    @property
    def dx(self):
        return self.value[0]

    @property
    def dy(self):
        return self.value[1]



class GfxComponent(Component):

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, priority, anchor = GfxAnchor.CENTER):
        super().__init__(name, priority)
        self.__anchor  = anchor
        self.__visible = True
        self.__old_alpha = 255

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def gfx_object(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @property
    def x(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @x.setter
    def x(self, value):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")

    @property
    def y(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @y.setter
    def y(self, value):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")

    @property
    def angle(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @angle.setter
    def angle(self, value):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")

    @property
    def scale(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @scale.setter
    def scale(self, value):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")

    @property
    def width(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @property
    def height(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @property
    def anchor(self):
        return self.__anchor

    @anchor.setter
    def anchor(self, value):
        self.__anchor = value

    @property
    def offset_x(self):
        return (self.anchor.dx * self.width) / 2

    @property
    def offset_y(self):
        return (self.anchor.dy * self.height) / 2

    @property
    def color(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @color.setter
    def color(self, value):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")

    @property
    def alpha(self):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")
        return 0

    @alpha.setter
    def alpha(self, value):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")

    @property
    def visible(self):
        return self.alpha > 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy



    # -----------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------
    def resize(self, width=None, height=None, keepRatio=True):
        ECSv3.error(f"Property has not been implemented yet for object {type(self)}")






import arcade

from ecsv3.arcade_layer.components.arcade_gfx import ArcadeFixed
from ecsv3.core.system.system import System
from ecsv3.utils.structures import *


class ArcadeGfxSystem(System):

    # typ is a dictionary containing each object class type that will be
    # handled in this system. The keys are the object types, and the values
    # are just string : comments about the type
    def __init__(self, name, priority: int = 1):
        types = {
            ArcadeFixed : 'Fixed image to display'
        }
        super().__init__(types, name, priority)
        # add new field for sprites
        self.__sprite_list = arcade.SpriteList()

    def _register_component(self, comp):
        # parent register
        index = super()._register_component(comp)
        # specific sprite list management
        # Sprite order should be managed by the Sprite.depth property : it seems to be buggy
        # sort it manually
        self.__sprite_list.append(comp.gfx_object)
        self.__sprite_list.sort(key=lambda x: x.prio)

    def _unregister_component(self, comp):
        # parent unregister
        super()._unregister_component(comp)
        # Remove sprite
        self.__sprite_list.remove(comp.gfx_object)

    def update_component_priority(self, comp, new_prio):
        # check component already exists
        if not comp.name in self._components:
            ECSv3.error(f"Impossible to update component priority ({comp.name}) in system ({self.name}) : component does not exist !")
        # Remove component from sorted list
        remove_entry_with_priority(self._components_order, comp)
        # update priority (for specific gfx arcade components depth property shall update sprite list automatically
        comp.set_new_priority_value(new_prio)
        # reinsert component in sorted list
        index = add_entry_with_priority(self._components_order, comp)


    def process_components(self, delta_time=None, data=None):
        if delta_time is not None:
            self.__sprite_list.update_animation(delta_time)
        else:
            self.__sprite_list.draw()


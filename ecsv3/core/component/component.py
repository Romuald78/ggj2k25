
from ecsv3.utils.logs import ECSv3

# TODO update priority of scripts and update sorted lists in related-system !!
# TODO handle remove from memory
# TODO add subclasses for GFX
#   Fixed sprite
#   Animated sprite
#   Text sprite
# TODO add subclasses for SFX
#   Sound/Music
#   loops / cursors / callbacks when reached a milestone / ...
# TODO Subclass PHYSICS
#   sensor only (collisions do not apply) or full physics
#   static / dynamic / kinetic
#   circle / rectangle bodies


class Component:

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name = 'comp0', priority = 1):
        self.__name = name
        self.__prio = priority
        self.__entity = None
        self.__system = None

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def name(self):
        return self.__name

    @property
    def priority(self):
        return self.__prio

    @priority.setter
    def priority(self, new_prio):
        if self.__system is not None:
            self.__system.update_component_priority(self, new_prio)
        else:
            self.set_new_priority_value(new_prio)

    @property
    def has_entity(self):
        return self.__entity is not None

    @property
    def entity(self):
        return self.__entity

    @property
    def has_system(self):
        return self.__system is not None

    @property
    def system(self):
        return self.__system

    # -----------------------------------------
    # COMPONENT-ENTITY LINK
    # -----------------------------------------
    def set_entity(self, ent):
        if self.__entity is not None and self.__entity != ent:
            ECSv3.error(f"Impossible to link a new entity ({ent.name})to this component ({self.name} -> {self.__entity.name})")
        self.__entity = ent

    # -----------------------------------------
    # COMPONENT-SYSTEM LINK (System)
    # -----------------------------------------
    def set_system(self, system):
        if self.__system is not None and self.__system != system:
            ECSv3.error(f"Impossible to link a new system ({system.name})to this component ({self.name} -> {self.__system.name})")
        self.__system = system

    def set_new_priority_value(self, new_prio):
        self.__prio = new_prio

    # -----------------------------------------
    # UTILITY METHODS
    # -----------------------------------------
    def __str__(self):
        out = 'Component{'
        out += f"name={self.name}, priority={self.priority}"
        out += '}'
        return out

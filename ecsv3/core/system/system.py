from ecsv3.utils.logs import ECSv3

# TODO : handle remove from memory (world, scene, system, entity, component, ...)
# TODO update priority of systems !!
from ecsv3.utils.structures import *


class System:

    # -----------------------------------------
    # PUBLIC ABSTRACT METHODS for subclasses
    # -----------------------------------------
    def process_components(self, delta_time=1/60, data=None):
        ECSv3.error(f"process_components() method has not been implemented yet in System '{self.name}' ({self.__class__}) ")

    # -----------------------------------------
    # PUBLIC ABSTRACT METHODS for subclasses
    # default implementations = store/remove into/from structures
    # -----------------------------------------
    def _register_component(self, comp):
        # Add component in the system dictionary
        add_entry_with_name(self._components, comp)
        index = add_entry_with_priority(self._components_order, comp)
        return index

    def _unregister_component(self, comp):
        # Forget component
        remove_entry_with_name(self._components, comp)
        remove_entry_with_priority(self._components_order, comp)

    def update_component_priority(self, comp, new_prio):
        # check component already exists
        if not comp.name in self._components:
            ECSv3.error(f"Impossible to update component priority ({comp.name}) in system ({self.name}) : component does not exist !")
        # Remove component from sorted list
        remove_entry_with_priority(self._components_order, comp)
        # update priority
        comp.set_new_priority_value(new_prio)
        # reinsert component in sorted list
        add_entry_with_priority(self._components_order, comp)

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    # typ is a dictionary containing each object class type that will be
    # handled in this system. The keys are the object types, and the values
    # are just string : comments about the type
    def __init__(self, typ, name, priority=1):
        self.__scene      = None
        self.__types      = typ
        self.__name       = name
        self.__priority   = priority
        # scripts _order MAY be used by subclasses in case of specific process (add/remove/...)
        self._components       = {}
        self._components_order = []

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def name(self):
        return self.__name

    @property
    def priority(self) -> int:
        return self.__priority

    @property
    def has_scene(self):
        return self.__scene is not None

    @property
    def scene(self):
        return self.__scene

    # -----------------------------------------
    # SYSTEM-SCENE LINK
    # -----------------------------------------
    def set_scene(self, scn):
        if self.__scene is not None and self.__scene != scn:
            ECSv3.error(f"Impossible to link a new scene ({scn.name})to this system ({self.name} -> {self.__scene.name})")
        self.__scene = scn

    # -----------------------------------------
    # SYSTEM-ENTITY/COMPONENT LINK
    # -----------------------------------------
    def link_component(self, comp):
        for typ in self.__types:
            if isinstance(comp, typ):
                # print(f"link {comp} to {self}")
                # Register component in the sorted list (this method may be overridden in the subclass)
                self._register_component(comp)
                # Component successfully registered
                return True
        return False

    def remove_component(self, comp):
        self._unregister_component(comp)

    # -----------------------------------------
    # UTILITY METHODS
    # -----------------------------------------
    def __str__(self):
        out = 'System{'
        out += f"name={self.name}"
        out += f", nb comps ={len(self._components)}"
        out += f", nb sorted={len(self._components_order)}"
        out += '}'
        return out

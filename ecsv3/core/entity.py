from ecsv3.core.component.component import Component
from ecsv3.utils.logs import ECSv3

# TODO : handle remove from memory (world, scene, system, entity, component, ...)


class Entity(Component):

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name='entity0'):
        super().__init__(name)
        self.__scene = None
        self.__components = {}

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def nb_components(self):
        return len(self.__components)

    @property
    def has_scene(self):
        return self.__scene is not None

    @property
    def scene(self):
        return self.__scene

    @property
    def world(self):
        return self.__scene.world

    # -----------------------------------------
    # ENTITY-SCENE LINK
    # -----------------------------------------
    def set_scene(self, scene):
        if self.__scene is not None and scene != self.__scene:
            ECSv3.error(f"Impossible to link a new scene ({scene.name})to this entity ({self.name} -> {self.__scene.name})")
        self.__scene = scene
        # actually the scripts for this entity have already been registered to systems

    # -----------------------------------------
    # ENTITY-COMPONENTS LINK
    # -----------------------------------------
    def add_component(self, comp):
        if comp.name in self.__components:
            ECSv3.error(f"Cannot add a component to an entity with an existing name (entity={self.name} / component={comp.name})")
        self.__components[comp.name] = comp
        # TODO register component if the entity is already linked to a scene
        #     else do nothing
        # link this component back to the entity
        comp.set_entity(self)


    def remove_all_components(self):
        for name in self.__components:
            comp = self.__components[name]
            if comp.has_system:
                comp.system.remove_component(comp)

    # -----------------------------------------
    # UTILITY METHODS
    # -----------------------------------------
    def __iter__(self):
        return self.__components.values().__iter__()

    def __getitem__(self, comp_name):
        # returns the component with the comp_name
        # or None if not found
        result = None
        if comp_name in self.__components:
            result = self.__components[comp_name]
        return result

from ecsv3.core.component.data.data_comp import DataComponent
from ecsv3.core.system.system_types import SystemGroup
from ecsv3.utils.logs import ECSv3
from ecsv3.utils.structures import add_entry_with_name, add_entry_with_priority, remove_entry_with_name


# TODO : handle remove from memory (scene, system, entity, component, ...)
# TODO update priority of system


class Scene:

    # -----------------------------------------
    # PUBLIC ABSTRACT METHODS for subclasses
    # -----------------------------------------
    # called when the world switches to this scene
    def enter(self, params=None):
        ECSv3.info(f"enter() method has not been implemented yet in Scene '{self.name}' ({self.__class__}) ")

    # called once each time the world switches to another scene
    def exit(self, params=None):
        ECSv3.info(f"exit() method has not been implemented yet in Scene '{self.name}' ({self.__class__}) ")

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, world, name:str='scene0'):
        self.__name         = name
        self.__world        = world
        self.__systems      = {SystemGroup.UPDATE: {}, SystemGroup.DRAW: {}, SystemGroup.EVENT: {}}
        self.__system_order = {SystemGroup.UPDATE: [], SystemGroup.DRAW: [], SystemGroup.EVENT: []}
        self.__entities     = {}
        self.__world.add_scene(self)

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def name(self):
        return self.__name

    @property
    def has_world(self):
        return self.__world is not None

    @property
    def world(self):
        return self.__world

    @property
    def width(self):
        return self.world.window.viewport[2]

    @property
    def height(self):
        return self.world.window.viewport[3]

    @property
    def has_systems(self):
        return (len(self.__systems[SystemGroup.UPDATE]) + len(self.__systems[SystemGroup.DRAW])) > 0

    @property
    def debug(self):
        res = False
        if self.has_world:
            res = self.world.debug
        return res

    @debug.setter
    def debug(self, value):
        if self.has_world:
            self.world.debug = value

    # -----------------------------------------
    # SCENE-SYSTEM LINK
    # -----------------------------------------
    def add_system(self, system, group):
        # check system name
        if system.name in self.__systems:
            ECSv3.error(f"Already existing system name '{system.name}'")
        if group not in self.__systems:
            ECSv3.error(f"Bad SystemGroup value '{group}'")
        # Store system in dictionary
        self.__systems[group][system.name] = system
        # Store system in the group priority list
        add_entry_with_priority(self.__system_order[group], system)
        # link the system back to this scene
        system.set_scene(self)

    def update(self, delta_time=1/60):
        group = SystemGroup.UPDATE
        for name in self.__systems[group]:
            system = self.__systems[group][name]
            # Process scripts from this system
            system.process_components(delta_time=delta_time)

        # some systems need an update phase (e.g.: DRAWING system and animated sprites)
        group = SystemGroup.DRAW
        for name in self.__systems[group]:
            system = self.__systems[group][name]
            # Process scripts from this system
            system.process_components(delta_time=delta_time)

    def draw(self):
        group = SystemGroup.DRAW
        for name in self.__systems[group]:
            system = self.__systems[group][name]
            # Process scripts from this system
            system.process_components(delta_time=None)

    def event(self, evt_type, value):
        # print(evt_type, value)
        group = SystemGroup.EVENT
        for name in self.__systems[group]:
            system = self.__systems[group][name]
            # Process scripts from this system
            system.process_components(data=(evt_type, value))

    # -----------------------------------------
    # SCENE-ENTITY LINK
    # -----------------------------------------
    def add_entity(self, entity):
        # common process to add an entry in a dictionary
        # print(f"Add entity {entity}")
        add_entry_with_name(self.__entities, entity)
        # link the entity back to this scene
        entity.set_scene(self)
        # Register entity scripts to correct system
        # each component will be registered to the first system encountered
        # if this limitation is not suitable, another design shall be made
        for comp in entity:
            linked = False
            if isinstance(comp, DataComponent):
                linked = True
            else:
                for group in self.__systems:
                    for system_name in self.__systems[group]:
                        system = self.__systems[group][system_name]
                        linked = system.link_component(comp)
                        if linked:
                            # link component back to system
                            comp.set_system(system)
                            break
                    if linked:
                        break
            if not linked:
                ECSv3.warning(f"add component in scene '{self.name}' failed : type '{type(comp)}' ")

    def remove_entity(self, entity_name_or_ref):
        ent1 = entity_name_or_ref
        if type(ent1) is str:
            ent1 = self.__entities[entity_name_or_ref]
        remove_entry_with_name(self.__entities, ent1)
        ent1.remove_all_components()



    # -----------------------------------------
    # UTILITY METHODS
    # -----------------------------------------
    def __str__(self):
        out = 'Scene{\n'
        out += f"    name={self.name}\n"
        for group in self.__systems:
            out += f"    {group} : "
            for name in self.__systems[group]:
                out += f"{name} / "
            out += '\n'
        out += '    }'
        return out

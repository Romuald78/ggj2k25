from ecsv3.core.component.script.script_comp import ScriptComponent
from ecsv3.core.system.system import System


class ScriptSystem(System):

    # typ is a dictionary containing each object class type that will be
    # handled in this system. The keys are the object types, and the values
    # are just string : comments about the type
    def __init__(self, name, priority: int = 1):
        types = {
            ScriptComponent : 'script class'
        }
        super().__init__(types, name, priority)

    def process_components(self, delta_time=1/60, data=None):
        for comp in self._components_order:
            comp.execute(delta_time)


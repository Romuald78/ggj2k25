from ecsv3.core.component.component import Component
from ecsv3.utils.logs import ECSv3


class ScriptComponent(Component):

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        ECSv3.error(f"execute() method has not been implemented yet for the script {self.name} (class={type(self)})")

    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name = 'script0', priority = 1):
        super().__init__(name, priority)



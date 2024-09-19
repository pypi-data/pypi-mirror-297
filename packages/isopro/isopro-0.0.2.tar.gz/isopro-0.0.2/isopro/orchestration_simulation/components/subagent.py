from .base_component import BaseComponent
from ..exceptions import ComponentException

class SubAgent(BaseComponent):
    def __init__(self, name, behavior, priority=0):
        super().__init__(name, priority)
        self.behavior = behavior

    def run(self, input_data=None):
        try:
            print(f"Running subagent: {self.name}")
            return self.behavior(input_data)
        except Exception as e:
            raise ComponentException(f"Exception in subagent {self.name}: {e}")
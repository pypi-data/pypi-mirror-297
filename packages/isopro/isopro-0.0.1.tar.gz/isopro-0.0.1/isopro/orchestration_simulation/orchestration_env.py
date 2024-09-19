import logging
from concurrent.futures import ThreadPoolExecutor
import heapq
from typing import List
from isopro.orchestration_simulation.components.base_component import BaseComponent
from isopro.orchestration_simulation.exceptions import ComponentException

logger = logging.getLogger(__name__)

class OrchestrationEnv:
    def __init__(self):
        self.components: List[BaseComponent] = []

    def add_component(self, component: BaseComponent):
        if not isinstance(component, BaseComponent):
            raise ValueError(f"Only BaseComponent instances can be added, got {type(component)}")
        self.components.append(component)

    def run_simulation(self, mode='sequence', input_data=None):
        if not self.components:
            logger.warning("No components to run")
            return
        if mode == 'sequence':
            return self.run_in_sequence(input_data)
        elif mode == 'parallel':
            return self.run_in_parallel(input_data)
        elif mode == 'node':
            return self.run_as_node(input_data)
        else:
            raise ValueError("Invalid execution mode")

    def run_in_sequence(self, input_data):
        logger.info("Running in sequence mode")
        results = []
        current_input = input_data
        for component in self.components:
            try:
                result = component.run(current_input)
                results.append(result)
                current_input = result  # Use the output as input for the next component
            except Exception as e:
                logger.error(f"Error: {e}")
                results.append(str(e))
        return results

    def run_in_parallel(self, input_data):
        logger.info("Running in parallel mode")
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(component.run, input_data) for component in self.components]
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error: {e}")
                    results.append(str(e))
        return results

    def run_as_node(self, input_data):
        logger.info("Running in node mode (priority-based)")
        results = []
        priority_queue = [(i, component) for i, component in enumerate(self.components)]
        heapq.heapify(priority_queue)
        
        while priority_queue:
            _, component = heapq.heappop(priority_queue)
            try:
                result = component.run(input_data)
                results.append(result)
            except Exception as e:
                logger.error(f"Error: {e}")
                results.append(str(e))
        return results
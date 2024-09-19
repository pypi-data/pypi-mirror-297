import logging
from typing import List
from .adversarial_simulator import AdversarialSimulator
from isopro.utils.analyze_adversarial_sim import analyze_adversarial_results, summarize_adversarial_impact
from isopro.agents.ai_agent import AI_Agent
import anthropic
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeAgent(AI_Agent):
    def __init__(self, name):
        super().__init__(name)
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def run(self, input_data):
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=100,
            messages=[{"role": "user", "content": input_data['text']}]
        )
        return response.content[0].text

    def step(self, sim_state):
        # This method is called by the AdversarialSimulator
        sim_state['output'] = self.run(sim_state)
        return sim_state

def setup_logging(log_dir: str, run_id: str) -> None:
    """
    Set up logging to both console and file.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"adv-{run_id}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def save_scores(output_dir: str, run_id: str, analysis_results: dict) -> None:
    """
    Save the analysis results to a JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"adv-{run_id}.json")
    
    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    logging.info(f"Saved analysis results to {output_file}")

def get_sample_inputs() -> List[str]:
    """
    Generate or load sample inputs for the simulation.
    """
    return [
        "What is the capital of France?",
        "How does photosynthesis work?",
        "Explain the theory of relativity."
    ]

def main():
    # Generate a unique run ID
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Set up logging
    log_dir = "logs"
    setup_logging(log_dir, run_id)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting adversarial simulation run {run_id}")

    # Initialize the Claude agent
    claude_agent = ClaudeAgent("Claude Agent")

    # Set up the adversarial simulator
    simulator = AdversarialSimulator(
        claude_agent,
        num_adversarial_agents=2,
        attack_types=["textbugger", "deepwordbug"],
        attack_targets=["input", "output"]
    )

    # Get sample inputs
    input_data = get_sample_inputs()

    # Run the simulation
    logger.info("Starting adversarial simulation...")
    simulation_results = simulator.run_simulation(input_data, num_steps=1)

    # Analyze the results
    logger.info("Analyzing simulation results...")
    analysis_results = analyze_adversarial_results(simulation_results)

    # Summarize the impact
    summary = summarize_adversarial_impact(analysis_results)

    # Print the summary
    print("\nAdversarial Simulation Summary:")
    print(summary)

    # Save the analysis results
    output_dir = "output"
    save_scores(output_dir, run_id, analysis_results)

    # Optionally, you can print more detailed results or save them to a file
    logger.info("Simulation complete.")

if __name__ == "__main__":
    main()


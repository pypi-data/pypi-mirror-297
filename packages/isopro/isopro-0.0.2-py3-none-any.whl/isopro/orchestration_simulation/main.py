import os
import json
import uuid
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.chains import LLMChain
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
import re
import logging
from langchain.agents import AgentExecutor
from isopro.orchestration_simulation.orchestration_env import OrchestrationEnv
from isopro.orchestration_simulation.utils import setup_logging
from isopro.orchestration_simulation.components.base_component import BaseComponent

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Access API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

if not openai_api_key or not serpapi_api_key:
    raise ValueError("API keys not found. Please check your .env file.")

# Custom tools
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="Useful for when you need to answer questions about current events or general knowledge. You should ask targeted questions"
)

memory = ConversationBufferMemory(memory_key="chat_history")

class CustomResearchTool(Tool):
    def __init__(self, name, description):
        super().__init__(name=name, func=self.research, description=description)

    def research(self, query: str) -> str:
        # Simulate a more complex research process
        search_result = search.run(query)
        summary = f"Research on {query}:\n{search_result[:500]}..."  # Truncate for brevity
        memory.chat_memory.add_user_message(query)
        memory.chat_memory.add_ai_message(summary)
        return summary

research_tool = CustomResearchTool(
    name="Detailed Research",
    description="Useful for when you need to conduct detailed research on a specific topic. Provide a focused research question."
)

summarize_tool = Tool(
    name="Summarize",
    func=lambda x: OpenAI().predict(f"Summarize the following in 2-3 sentences: {x}"),
    description="Use this to summarize long pieces of text."
)

# Define custom prompt template
template = """You are an expert research assistant. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""

# Set up the prompt template
tools = [search_tool, research_tool, summarize_tool]
tool_names = ", ".join([tool.name for tool in tools])
tool_descriptions = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])

prompt = PromptTemplate(
    template=template,
    input_variables=["input", "agent_scratchpad"],
    partial_variables={"tools": tool_descriptions, "tool_names": tool_names}
)

# Set up the agent
llm = OpenAI(temperature=0)
agent = create_react_agent(llm, tools, prompt)

class AgentComponent(BaseComponent):
    def __init__(self, agent, tools):
        super().__init__("AgentComponent")
        self.agent = agent
        self.tools = tools
        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=self.agent, tools=self.tools, verbose=True)

    def run(self, input_data):
        try:
            logger.info(f"Running AgentComponent with input: {input_data}")
            result = self.agent_executor.invoke({"input": input_data})
            logger.info(f"AgentComponent result: {result}")
            return {"result": result.get('output', 'No output generated')}
        except Exception as e:
            logger.error(f"Error in AgentComponent: {str(e)}", exc_info=True)
            return {"error": str(e)}

def generate_unique_id():
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"

def save_results(results, run_type, unique_id):
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.join(output_dir, f"run_{unique_id}.json")
    
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        data = {}
    
    data[run_type] = results
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    unique_id = generate_unique_id()
    logger = setup_logging(log_file=f"logs_{unique_id}.log")
    
    # Create the SimulationEnvironment
    sim_env = OrchestrationEnv()

    # Create and add LangChain agents with different tasks
    for i in range(3):
        sim_env.add_component(AgentComponent(agent, tools))
        logger.info(f"Added AgentComponent {i+1} to SimulationEnvironment")

    # Run the simulation in different modes
    logger.info("\nRunning in sequence mode:")
    sequence_results = sim_env.run_simulation(mode='sequence', input_data="What are the potential impacts of artificial intelligence on healthcare, education, and transportation?")
    logger.info(f"Sequence mode results: {sequence_results}")
    save_results(sequence_results, "sequence", unique_id)
    logger.info("Sequence mode results saved.")

    logger.info("\nRunning in parallel mode:")
    parallel_results = sim_env.run_simulation(mode='parallel', input_data="Compare and contrast the economic policies of the USA, China, and the European Union in response to climate change.")
    logger.info(f"Parallel mode results: {parallel_results}")
    save_results(parallel_results, "parallel", unique_id)
    logger.info("Parallel mode results saved.")

    logger.info("\nRunning in node mode:")
    node_results = sim_env.run_simulation(mode='node', input_data="Analyze the global impact of remote work on urban development, real estate, and transportation infrastructure.")
    logger.info(f"Node mode results: {node_results}")
    save_results(node_results, "node", unique_id)
    logger.info("Node mode results saved.")

    logger.info(f"All results saved with unique ID: {unique_id}")

if __name__ == "__main__":
    main()
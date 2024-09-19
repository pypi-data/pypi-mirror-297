import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .subagent import SubAgent
import logging

logger = logging.getLogger(__name__)

class LLaMAAgent(SubAgent):
    def __init__(self, name, task, model_name="facebook/opt-350m", priority=0):
        super().__init__(name, self.llama_behavior, priority)
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.task = task
        
    def llama_behavior(self, input_data=None):
        prompt = f"""
        You are an AI assistant named {self.name}. Your task is to {self.task}

        Input: {input_data}

        Please provide a concise and informative response.
        
        Response:"""

        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = response.split("Response:")[-1].strip()

        logger.info(f"LLaMA Agent {self.name} response:\n{answer}")
        return answer
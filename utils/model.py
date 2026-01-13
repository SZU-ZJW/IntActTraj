import os
import random
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from utils.log import get_logger
from vllm import LLM,SamplingParams
from transformers import AutoTokenizer

logger = get_logger()
RUN_SEED = int(os.getenv("RUN_SEED", 773815))

class OfflinevLLMModel:
    def __init__(self, args, quantization: str = 'fp8', VLLM_TENSOR_PARALLEL_SIZE=2):
        random.seed(RUN_SEED)
        self.model_name = args.model
        self.llm = LLM(
            self.model_name,
            tensor_parallel_size=VLLM_TENSOR_PARALLEL_SIZE,
            #quantization= quantization,
            gpu_memory_utilization = 0.95,
            trust_remote_code=True,
            enforce_eager=True
        )
        #self.tokenizer = self.llm.get_tokenizer()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
    
    def reformat_prompt(self, msg):
        signal = False
        try:
            format_prompt = self.tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        except AttributeError as e:
            logger.error(f"{e}. Ensure that your tokenizer supports 'apply_chat_template")
            signal = True
        return format_prompt, signal
    
    def query(self, args, prompt):
        responses = self.llm.generate(
            prompt,
            SamplingParams(
                temperature=args.temperature,
                top_p = args.top_p,
                seed=26,
                skip_special_tokens=True,
                stop=self.tokenizer.eos_token,
                max_tokens=1024,
            ),
            use_tqdm=False
        )
        for response in responses:
            batch_response = self.process_response(response.outputs[0].text) 
        return batch_response

    def process_response(self, generation: str) -> str:
        generation = generation.strip()
        generation = self.extract_content(generation).strip()
        return generation
    
    @staticmethod
    def extract_content(s: str) -> str:
        start_tag = "<answer>"
        start_index = s.find(start_tag)
        if start_index == -1:
            return s
        else:
            return s[start_index + len(start_tag):]

class MutilOfflinevLLMModel:
    def __init__(self, args, seed, quantization: str = 'fp8', VLLM_TENSOR_PARALLEL_SIZE=4):
        random.seed(RUN_SEED)
        self.model_name = args.model
        self.llm = LLM(
            self.model_name,
            tensor_parallel_size=VLLM_TENSOR_PARALLEL_SIZE,
            #quantization= quantization,
            trust_remote_code=True,
            enforce_eager=True,
            gpu_memory_utilization=0.95,
            seed=seed,
        )
        self.tokenizer = self.llm.get_tokenizer()

    def reformat_prompt(self, msg):
        signal = False
        try:
            format_prompt = self.tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
        except AttributeError as e:
            logger.error(f"{e}. Ensure that your tokenizer supports 'apply_chat_template")
            signal = True
        return format_prompt, signal
    
    def query(self, args, prompt):
        batch_response = []
        responses = self.llm.generate(
            prompt,
            SamplingParams(
                temperature=args.temperature,
                top_p = args.top_p,
                skip_special_tokens=True,
                stop=self.tokenizer.eos_token,
                max_tokens=1024,
            ),
            use_tqdm=False,
        )
        for response in responses:
            response_content = self.process_response(response.outputs[0].text)
            batch_response.append(response_content) 
        return batch_response

    def process_response(self, generation: str) -> str:
        generation = generation.strip()
        generation = self.extract_content(generation).strip()
        return generation
    
    @staticmethod
    def extract_content(s: str) -> str:
        start_tag = "<answer>"
        start_index = s.find(start_tag)
        if start_index == -1:
            return s
        else:
            return s[start_index + len(start_tag):]

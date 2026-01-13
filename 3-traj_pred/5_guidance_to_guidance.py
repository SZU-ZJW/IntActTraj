import os
import re
import json
import argparse
from openai import OpenAI
import sys
import yaml
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from utils.log import get_logger

logger = get_logger()

def load_yaml(file_path: str):
    with open(file_path,'r') as file:
        return yaml.safe_load(file)

def generate_prompt(args, fileds):
    config = load_yaml(args.prompt)
    text = config.get(fileds, '')
    if fileds == 'system_template':
        role = 'system'
    else:
        role = 'user'

    message = {"role": role,"content": text,}
    return message

def contains_triple_quote_pairs(text):
    """
    检测字符串中是否包含成对的三单引号内容。

    :param text: 输入字符串
    :return: 如果包含成对的三单引号内容，返回 True; 否则返回 False
    """
    triple_quote_pattern = r"```([\s\S]*?)```"
    matches = re.findall(triple_quote_pattern, text, re.DOTALL)
    return len(matches) > 0

def end_of_edit(text):
    if "end_of_edit" in text:
        return True
    else:
        return False

def process_text(input_text):
    """
    Processes the input text by removing the phrase 'The next step is to ' followed by any word and converting the first letter of the next word to uppercase.

    :param input_text: The original text to process.
    :return: Processed text.
    """
    # Remove the specified pattern
    processed_text1 = re.sub(r'The next step is to ', '', input_text, count=1)

    # Capitalize the first word after the removed section
    processed_text = re.sub(r'\b(\w)', lambda match: match.group(1).upper(), processed_text1, count=1)
    
    return processed_text

def query(args, message):
    try:
        client = OpenAI(api_key=args.api_key, base_url=args.base_url)
        response = client.chat.completions.create(
            model=args.model,
            messages=message,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error during API request: {e}")
        return None

def main(args):
    message = []

    system_prompt = generate_prompt(args, 'system_template')
    message.append(system_prompt)

    demonstrate_prompt = generate_prompt(args, 'Demonstrate')
    message.append(demonstrate_prompt)
    
    if not os.path.exists(os.path.dirname(args.save_path)):
        os.makedirs(os.path.dirname(args.save_path))

    with open(args.save_path, 'w') as savef:
        with open(args.data_path, 'r') as infile:
            for idx, line in enumerate(infile, start=1):
                #if idx < 3070:
                #    continue
                data = json.loads(line)
                signal1 = False
                signal2 = False
                response = data['response']
                if '.\n' in response:
                    response = response.split('.\n')[0] + '.'
                response = process_text(response)
                if response and isinstance(response, str):
                    signal1 = contains_triple_quote_pairs(response)
                    signal2 = end_of_edit(response)
                    if signal1 or signal2:
                        logger.info(f"📀 Original content:\n{response}")
                        # instance prompt
                        instance_template = load_yaml(args.prompt).get('instance_template', '')
                        response_prompt = instance_template.format(
                            original = response,
                        )
                        message.append(
                            {"role":"user", "content":response_prompt}
                        )
                        answer = query(args, message)
                        if answer:
                            logger.info(f"⚙️ Updated content:\n{answer}\n\n")
                            if message:
                                message.pop()
                            data['response'] = answer
                            json.dump(data, savef)
                            savef.write('\n')
                        else:
                            logger.info(f"❌ Wrong!\n\n")
                            json.dump(data, savef)
                            savef.write('\n')
                    else:
                        json.dump(data, savef)
                        savef.write('\n')
                else:
                    json.dump(data, savef)
                    savef.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and normalize model guidance predictions")

    parser.add_argument("--model", type=str, default="gpt-4", help="The model used for optional refinement")
    parser.add_argument("--prompt", type=str, default="./3-traj_pred/config/default.yaml", help="Prompt template list")
    parser.add_argument(
        "--data_path",
        type=str,
        default="./3-traj_pred/result/pred_result/qwen25-7B/prediction_para2.jsonl",
        help="Path to raw predictions from step 4 for a single model",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="./3-traj_pred/result/pred_result/qwen25-7B/prediction_final.jsonl",
        help="Path to save cleaned predictions for this model",
    )
    parser.add_argument("--api_key", type=str, required=True, help="Your OpenAI API key")
    parser.add_argument("--base_url", type=str, default="none", help="The base URL for the OpenAI API")

    args = parser.parse_args()
    main(args)

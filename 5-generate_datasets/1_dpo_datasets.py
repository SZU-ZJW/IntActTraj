import json
import yaml
from tqdm import tqdm
from transformers import AutoTokenizer

# 加载本地分词器
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-3.1-8B-Instruct')

def load_yaml(file_path: str):
    with open(file_path,'r') as file:
        return yaml.safe_load(file)
    
def count_token_distribution_and_format(file_path, special_line):
    more_than_6k_idx = []

    with open(file_path, 'r') as file:
        with tqdm(total=482507, desc="Processing lines", unit="line") as pbarp:
            for idx, line in enumerate(file, start=0):
                obj = json.loads(line)
                if idx in special_line:
                    value = obj.get("conversations", [{}])[0].get("value", "")
                    value_token = tokenizer.tokenize(value)
                    value_len = len(value_token)
                    if value_len > 6000:
                        more_than_6k_idx.append(idx)
                pbarp.update(1)

    return more_than_6k_idx


def extract_matching_lines(jsonl_file):
    matching_lines = []

    with open(jsonl_file, 'r', encoding='utf-8') as file:
        data = file.readlines()

    split_index = 0
    total_lines = len(data)
    with tqdm(total=total_lines, desc="Processing Lines", unit="line") as pbar:
        while split_index < total_lines - 1:
            current_line = json.loads(data[split_index])
            next_line = json.loads(data[split_index + 1])
            current_value = current_line.get("conversations", [{}])[0].get("value", "")
            next_value = next_line.get("conversations", [{}])[0].get("value", "")
            
            if "***END_OF_ISSUE***" in next_value and "***STEP_AND_EXECUTION_RESULTS-1***" not in next_value:
                if "***END_OF_ISSUE***" in current_value and "***STEP_AND_EXECUTION_RESULTS-1***" in current_value:
                    matching_lines.append(split_index)
            
            split_index += 1
            pbar.update(1)
    
    return matching_lines


def up_and_save(data, idx):
    save_line = []
    i = idx
    while i != 0:
        current_line = json.loads(data[i])
        up_line = json.loads(data[i-1])
        current_line_value = current_line.get("conversations", [{}])[0].get("value", "")
        up_line_value = up_line.get("conversations", [{}])[0].get("value", "")

        if "***END_OF_ISSUE***" in current_line_value and "***STEP_AND_EXECUTION_RESULTS-1***" not in current_line_value:
            if "***END_OF_ISSUE***" in up_line_value and "***STEP_AND_EXECUTION_RESULTS-1***" in up_line_value:
                break
            else:
                save_line.append(i)
                i -= 1
        else:
            save_line.append(i)
            i -= 1
    save_line.reverse()
    return save_line


def delate_some_content(data, lines_idx):
    query = ''
    save_line = []
    for line_idx in lines_idx:
        current_line = json.loads(data[line_idx])
        current_query = current_line.get("conversations", [{}])[0].get("value", "")
        if current_query == query:
            continue
        else:
            save_line.append(line_idx)
            query = current_query
    return save_line


def extract_6k_instance(file_path, save_path, system_prompt, lines_idx):
    system_prompt_token = tokenizer.tokenize(system_prompt)
    system_prompt_num = len(system_prompt_token)
    with open(file_path, 'r') as infile:
        data = infile.readlines()
    with open(save_path, 'w') as savef:
        with tqdm(total=len(lines_idx), desc="Processing", unit='line') as pber:
            for line_idx in lines_idx:
                related_lines = up_and_save(data, line_idx)
                save_lines = delate_some_content(data, related_lines)
                for save_line in save_lines:
                    current_line = json.loads(data[save_line])
                    query = current_line.get("conversations", [{}])[0].get("value", "")
                    #instance_content = query.split("two numbers.")[1].strip('\n')
                    answer = current_line.get("chosen", "").get("value", "")
                    #instance_prompt_token = tokenizer.tokenize(instance_content)
                    #instance_prompt_num = len(instance_prompt_token)
                    #if instance_prompt_num + system_prompt_num < 14000:
                    meta_data = {
                        "conversations": [
                            {
                                "from": "human",
                                "value": query
                            },
                        ],
                        "answer":{
                            "from": "gpt",
                            "value": answer
                        },
                    }
                    json.dump(meta_data, savef)
                    savef.write('\n')
                pber.update(1)


file_path = './5-generate_datasets/acc_rej.jsonl'
config_path = './5-generate_datasets/template.yaml'
save_path = './5-generate_datasets/long_context_SFT_special.jsonl'

match = extract_matching_lines(file_path)
token_than_6k = count_token_distribution_and_format(file_path, match)
system_prompt = load_yaml(config_path).get('template', '')
extract_6k_instance(file_path, save_path, system_prompt, token_than_6k)

import os
import re
from tqdm import tqdm
import json
import numpy as np
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from utils.log import get_logger
from Levenshtein import distance as levenshtein_distance

logger = get_logger()

def string_similarity(str1: str, str2: str) -> float:
    """
    Calculate the similarity between two strings using Levenshtein distance.

    Args:
        str1 (str): The first string.
        str2 (str): The second string.

    Returns:
        float: A similarity score between 0 and 1, where 1 means identical and 0 means completely different.
    """
    # Calculate the Levenshtein distance
    distance = levenshtein_distance(str1, str2)
    
    # Calculate the maximum possible length (for normalization)
    max_len = max(len(str1), len(str2))
    
    # If both strings are empty, they are identical
    if max_len == 0:
        return 1.0
    
    # Calculate similarity
    similarity = 1 - (distance / max_len)
    return similarity

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

def rename_key(data):
    exist_keys = set()
    exist_keys = [key for key in data if key.startswith('guidance_')]
    num = 1
    if exist_keys:
        for key_i in exist_keys:
            if key_i == 'guidance_0':
                continue
            else:
                guidance = data[key_i]
                key_name = f"pred_{num}"
                data[key_name] = guidance
                del data[key_i]
                num += 1
    return data

def calculate_combinations(n):
    # 计算C^2_n = n * (n - 1) / 2
    if n < 2:
        return 0
    return n * (n - 1) // 2

def read_jsonl(file_path):
    """
    Reads a jsonl file and returns a list of dictionaries.
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def merge_files(reference_file, generated_files, model_list):
    reference_data = read_jsonl(reference_file)
    results = []
    generated_data_list = [read_jsonl(file) for file in tqdm(generated_files, desc=f"Reading generated files")]

    # Iterate over the reference data
    for ref in reference_data:
        merged_entry = {
            "instance_id": ref["instance_id"],
            "issue_and_prestep": ref["issue_and_prestep"],
            "guidance_0": ref.get("guidance", ref.get("label", "")),
        }
        
        # Add the corresponding commands from each generated file
        for i, gen_data in enumerate(generated_data_list):
            for gen in gen_data:
                if gen["instance_id"] == ref["instance_id"] and gen["issue_and_prestep"] == ref["issue_and_prestep"]:
                    if gen['response']:
                        merged_entry[f"guidance_{i+1}"] = gen["response"]
                        break
                    else:
                        merged_entry[f"guidance_{i+1}"] = 'null'
                        break

        results.append(merged_entry)

    return results

def save_to_jsonl(data, output_file):
    """
    Saves a list of dictionaries to a JSONL file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

# 处理每行数据
def process_data(input_file, output_file):
    total_combinations = 0

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # 读取每行数据
        lines = infile.readlines()
        processed_lines = []
        
        # 使用tqdm显示进度条
        for line in tqdm(lines, desc="Processing", unit="line"):
            data = json.loads(line.strip())  # 解析json行
            guidance_keys = [key for key in data if key.startswith('guidance_')]
            
            # 先删除值为null的guidance项
            keys_to_delete = set()
            for key in guidance_keys:
                if data.get(key) is None:  # 如果值为None，则删除该键
                    keys_to_delete.add(key)

            # 用于存储要删除的guidance键
            for key in keys_to_delete:
                if key in data:
                    del data[key]
            
            guidance_keys = [key for key in data if key.startswith('guidance_')]
            for i, key_i in enumerate(guidance_keys):
                guidance_i = data[key_i]
                if '.\n' in guidance_i:
                    response_new = guidance_i.split('.\n')[0] + '.'
                else:
                    response_new = guidance_i
                data[key_i] = process_text(response_new)

            # 重新计算guidance之间的相似度并删除重复项
            guidance_keys = [key for key in data if key.startswith('guidance_')]  # 更新guidance_keys
            for i, key_i in enumerate(guidance_keys):
                if key_i in keys_to_delete:
                    continue  # 如果已经标记为删除，则跳过
                guidance_i = data[key_i]
                if key_i == 'guidance_0':
                    for j, key_j in enumerate(guidance_keys):
                        if key_j != 'guidance_0' and key_j not in keys_to_delete:
                            guidance_j = data[key_j]
                            similarity = string_similarity(guidance_i, guidance_j)
                            if similarity > 0.9:
                                keys_to_delete.add(key_j)
                                logger.info(f"A:\n{guidance_i}")
                                logger.info(f"B:\n{guidance_j}\n\n")
                else:
                    for j, key_j in enumerate(guidance_keys):
                        if j > i and key_j not in keys_to_delete:
                            guidance_j = data[key_j]
                            similarity = string_similarity(guidance_i, guidance_j)
                            if similarity > 0.9:
                                keys_to_delete.add(key_j)
                                logger.info(f"A:\n{guidance_i}")
                                logger.info(f"B:\n{guidance_j}\n\n")
            # 删除标记为删除的guidance项
            for key in keys_to_delete:
                if key in data:
                    del data[key]
            zhengli_data = rename_key(data)
            # 将处理后的数据写入输出文件
            processed_lines.append(json.dumps(zhengli_data, ensure_ascii=False))
            remaining_guidance_keys = [key for key in zhengli_data if key.startswith('guidance_') or key.startswith('pred_')]
            remaining_count = len(remaining_guidance_keys)
            combination_count = calculate_combinations(remaining_count)

            # 累加C^2_n值
            total_combinations += combination_count
        
        # 写入最终的处理结果
        outfile.write("\n".join(processed_lines) + "\n")
        # 打印所有行的C^2_n总和
        print(f"Total C^2_n: {total_combinations}")

def main():
    predicte_model_list = [
        "Deepseek",
        "llama3.1-8b-instruct",
        "Mixtral-8x7b",
        "phi-3.5-MoE",
        "qwen2.5-32b-instruct",
        "qwen2.5-7b-instruct",
        "qwen2.5-coder-32b",
    ]

    # Reference file comes from step 3 (issue_and_prestep + gold next-step guidance)
    reference_file = "./3-traj_pred/result/interaction_data/interaction_data_for_Train.jsonl"
    # Each model's cleaned predictions from step 5
    generated_files = [
        f"./3-traj_pred/result/pred_result/{lm_model}/prediction_final.jsonl"
        for lm_model in predicte_model_list
    ]
    merge_file = "./3-traj_pred/result/datasets/merged_output.jsonl"
    output_file = "./3-traj_pred/result/datasets/final_RM.jsonl"

    merged_data = merge_files(reference_file, generated_files, predicte_model_list)
    save_to_jsonl(merged_data, merge_file)
    print(f"Merged data saved to {merge_file}")
    process_data(merge_file, output_file)

if __name__ == "__main__":
    main()

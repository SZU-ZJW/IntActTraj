import re
import os
import yaml
import json
import sys
import argparse
from tqdm import tqdm
from typing import List
sys.path.append('/home/zjw/zhengli/IntActTraj/')
from utils.log import get_logger
from utils.model import MutilOfflinevLLMModel

logger = get_logger()

def load_yaml(file_path: str):
    with open(file_path,'r') as file:
        return yaml.safe_load(file)

def generate_demo_prompt(file_path:str):
    config = load_yaml(file_path)

    # 提取 Demonstrate 部分和 demonstrate 的文件路径列表
    demonstration_text = config.get('Demonstrate', '')
    demonstrate_paths = config.get('demonstrate', [])

    # 存储读取的内容
    demonstration_contents = []

    # 读取每个 YAML 文件
    for path in demonstrate_paths:
        try:
            demonstration_contents.append(load_yaml(path).get('demonstrate', ''))
        except FileNotFoundError:
            print(f"文件未找到: {path}")
        except Exception as e:
            print(f"读取文件时出错: {e}")

    # 构建最终提示内容
    final_prompt = f"{demonstration_text}\n"
    for i, content in enumerate(demonstration_contents, start=1):
        final_prompt += f"Demo {i}:\n{content}\n"

    final_prompt += "--- END OF DEMONSTRATION ---"

    return final_prompt

def label_and_predicted(data):
    label = data.get('guidance_0', '')
    predicts = {k:v for k,v in data.items() if k.startswith('pred_')}
    predict_list = []
    idx = 1

    if predicts:
        for key in predicts:
            key_value = data.get(key, '')
            predict_content = f'{idx}: {key_value}'
            predict_list.append(predict_content)
            idx += 1
    predict_message = '\n'.join(predict_list)
    return label, predict_message

def issue_and_part_solution(data):
    text = data.get('issue_and_prestep', '')
    
    # 提取issue部分
    issue_pattern = r'(?<=\*\*\*ISSUE\*\*\*\s)(.*?)(?=\*\*\*END_OF_ISSUE\*\*\*)'
    issue_match = re.search(issue_pattern, text, re.DOTALL)
    issue = issue_match.group(0).strip() if issue_match else ""

    # 提取step and feedback部分
    step_feedback_pattern = r'(?<=\*\*\*END_OF_ISSUE\*\*\*\n\n\n)(.*?)(?=\*\*\*END_OF_STEP_AND_EXECUTION_RESULTS\*\*\*|$)'
    step_feedback_matches = re.findall(step_feedback_pattern, text, re.DOTALL)
    step_feedback = [match.strip() for match in step_feedback_matches]
    
    if len(step_feedback) == 0:
        return issue, None
    else:
        return issue, step_feedback[0]

def transfer_format(model, history_batch):
    format_content: List[str]=[]
    signal = False

    for batch in history_batch:
        content,signal = model.reformat_prompt(batch)
        format_content.append(content)
        if signal:
            logger.error(f"Worng application in Template")
            break
    
    return format_content, signal

def processing(args, model, seed, sign, history_batch_formate, data_list, outfile, history_batch):
    idx = 0
    if sign:
        for metadata in data_list:
            meta_data = {
                "instance_id": metadata.get("instance_id", ''),
                "issue_and_prestep": metadata.get("issue_and_prestep", ''),
                "response": None
            }
            json.dump(meta_data, outfile)
            outfile.write('\n')

            instance_prompt = history_batch[idx][2].get('content', '')
            part_instance_prompt = tiqu(instance_prompt)
            logger.info(f"🎥 INSTANCE PROMPT\n{part_instance_prompt}")
            logger.info(f"📈 RANK \n none\n\n")

            idx += 1
        history_batch = []
        data_list = []
    else:
        answers = model.query(args, seed, history_batch_formate)
        for answer in answers:
            meta_data = {
                "instance_id": data_list[idx].get("instance_id", ''),
                "issue_and_prestep": data_list[idx].get("issue_and_prestep", ''),
                "response": answer
            }
            json.dump(meta_data, outfile)
            outfile.write('\n')

            instance_prompt = history_batch[idx][2].get('content', '')
            part_instance_prompt = tiqu(instance_prompt)
            logger.info(f"🎥 INSTANCE PROMPT\n{part_instance_prompt}")
            logger.info(f"📈 RANK \n {answer}\n\n")

            idx += 1
        history_batch = []
        data_list = []
    return history_batch, data_list

def tiqu(text):
    pattern = r"(Standard Next Step Solution:.*?Predicted Solutions:.*?)(?=\n\n|\Z)"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        extracted_part = match.group(0)
        return extracted_part
    else:
        return text

def main(args, seed_list):
    history: List[str] = []
    sign = False
    Model = MutilOfflinevLLMModel(args)

    system_prompt = load_yaml(args.config).get('system_template', '')
    history.append(
        {"role":"system", "content":system_prompt}
    )
    logger.info(f"🤖 SYSTEM PROMPT\n{system_prompt}")

    demo_prompt = generate_demo_prompt(args.config)
    history.append(
        {"role":"user", "content":demo_prompt}
    )
    logger.info(f"🍪 DEMONSTRATION \n \t READY!")
    for seed in seed_list:
        history_batch = []
        data_list = []
        save_filename = f"rank_seed_{seed}-final.jsonl"
        os.makedirs(args.save_path, exist_ok=True)
        save_path = os.path.join(args.save_path, save_filename)

        with open(save_path, 'w') as outfile:
            with open(args.data_path, 'r', encoding='utf-8') as infile:
                total_lines = sum(1 for _ in infile)  # 计算总行数
                infile.seek(0)
                with tqdm(total=total_lines, desc=f"({seed})Processing", unit="line") as pbar:
                    for line in infile:
                        data =json.loads(line)
                        current_history = []
                        issue_statement, prestep = issue_and_part_solution(data)
                        label, prediction_solution = label_and_predicted(data)
                        instance_template = load_yaml(args.config).get('instance_template', '')
                        message = instance_template.format(
                            issue = issue_statement,
                            prestep = prestep,
                            label = label,
                            predicted_solution = prediction_solution
                        )
                        current_history = history.copy()
                        current_history.append(
                            {"role":"user", "content":message}
                        )
                        history_batch.append(current_history)
                        data_list.append(
                            {"instance_id": data["instance_id"], "issue_and_prestep":data["issue_and_prestep"]}
                        )
                        
                        if len(history_batch) == args.batch_size:
                            history_batch_formate, sign = transfer_format(Model, history_batch)

                            history_batch, data_list = processing(args, Model, seed, sign, history_batch_formate, data_list, outfile, history_batch)
                        pbar.update(1)

                    if history_batch:
                        history_batch_formate, sign = transfer_format(Model, history_batch)
                        history_batch, data_list = processing(args, Model, seed, sign, history_batch_formate, data_list, outfile, history_batch)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank the SUMMARY")

    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen2.5-32B-Instruct",
        help="The model which ranks the summaries",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="4-rank/prompt/config.yaml",
        help="Prompt template list",
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="./3-traj_pred/result/datasets/final_RM.jsonl",
        help="Path to merged RM data from step 6",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="./4-rank/save",
        help="Directory to save ranking results",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[128, 512, 1024],
        help="Random seeds to use for ranking runs",
    )
    parser.add_argument("--temperature", type=float, default=0.8, help="The temperature of model")
    parser.add_argument("--top_p", type=float, default=0.95, help="The top p of model")
    parser.add_argument("--batch_size", type=int, default=20, help="The batch size of input")

    args = parser.parse_args()
    main(args, args.seeds)

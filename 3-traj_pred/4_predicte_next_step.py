import re
import os
import yaml
import json
import argparse

from typing import List
import sys
from tqdm import tqdm
sys.path.append('/home/zjw/zhengli/IntActTraj/')
from utils.model import MutilOfflinevLLMModel
from utils.log import get_logger

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

def processing(args, model, sign, history_batch_formate, data_list, outfile, history_batch):
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
            #logger.info(f"🎥 INSTANCE PROMPT\n{instance_prompt}")
            logger.info(f"📈 PREDICTION \n none")

            idx += 1
        history_batch = []
        data_list = []
    else:
        answers = model.query(args, history_batch_formate)
        for answer in answers:
            meta_data = {
                "instance_id": data_list[idx].get("instance_id", ''),
                "issue_and_prestep": data_list[idx].get("issue_and_prestep", ''),
                "response": answer
            }
            json.dump(meta_data, outfile)
            outfile.write('\n')

            instance_prompt = history_batch[idx][2].get('content', '')
            #logger.info(f"🎥 INSTANCE PROMPT\n{instance_prompt}")
            logger.info(f"📈 PREDICTION \n {answer}")

            idx += 1
        history_batch = []
        data_list = []
    return history_batch, data_list


def main(args):
    history: List[str] = []
    sign = False
    Model = MutilOfflinevLLMModel(args)

    system_prompt = load_yaml(args.config).get('system_template', '')
    history.append(
        {"role":"user", "content":system_prompt}
    )
    logger.info(f"🤖 SYSTEM PROMPT\n{system_prompt}")
    history.append({"role":"assistant", "content":'Sure! Please provide the ISSUE and the STEP_AND_EXECUTION_RESULTS, and I will generate the next step guidance for you.'})
    demo_prompt = generate_demo_prompt(args.config)
    history.append(
        {"role":"user", "content":demo_prompt}
    )
    logger.info(f"🍪 DEMONSTRATION \n \t READY!")
    history.append({"role":"assistant", "content":'I understand now. Please give me the issue and partial solution, and I will give you the next step guidance.'})
    history_batch = []
    data_list = []
    save_filename = "prediction_para2.jsonl"
    os.makedirs(args.save_path, exist_ok=True)
    save_path = os.path.join(args.save_path, save_filename)
    with open(save_path, 'w') as outfile:
        with open(args.data_path, 'r') as infile:
            # Wrap the file iterator with tqdm to show progress
            total_lines = sum(1 for _ in infile)  # Get total number of lines in the file
            infile.seek(0)  # Reset the file pointer to the beginning
            
            # Using tqdm to show progress bar
            for idx, line in tqdm(enumerate(infile, start=1), total=total_lines, desc="Processing", unit="line"):
                #if idx < 131:
                #    continue
                data = json.loads(line)
                current_history = []
                issue_and_prestep = data['issue_and_prestep']
                instance_template = load_yaml(args.config).get('instance_template', '')
                message = instance_template.format(
                    issue_and_prestep=issue_and_prestep,
                )
                current_history = history.copy()
                current_history.append(
                    {"role": "user", "content": message}
                )
                history_batch.append(current_history)
                data_list.append(
                    {"instance_id": data["instance_id"], "issue_and_prestep": data["issue_and_prestep"]}
                )
                
                if len(history_batch) == args.batch_size:
                    history_batch_formate, sign = transfer_format(Model, history_batch)

                    history_batch, data_list = processing(args, Model, sign, history_batch_formate, data_list, outfile, history_batch)
            
            if history_batch:
                history_batch_formate, sign = transfer_format(Model, history_batch)
                history_batch, data_list = processing(args, Model, sign, history_batch_formate, data_list, outfile, history_batch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PREDICTION")

    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct", help="The model which predicts the next step")
    parser.add_argument("--config", type=str, default="./3-traj_pred/config/default-guid.yaml", help="Prompt template")
    parser.add_argument(
        "--data_path",
        type=str,
        default="./3-traj_pred/result/interaction_data/interaction_data_for_Train.jsonl",
        help="Input interaction data for training/prediction",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="./3-traj_pred/result/pred_result/qwen25-7B",
        help="Directory to save raw predictions for this model",
    )
    parser.add_argument("--temperature", type=float, default=0, help="The temperature of model")
    parser.add_argument("--top_p", type=float, default=0.95, help="The top p of model")
    parser.add_argument("--batch_size", type=int, default=10, help="The batch size of input")

    args = parser.parse_args()
    main(args)

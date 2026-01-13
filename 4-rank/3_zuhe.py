import os
import json
import yaml
import argparse
from tqdm import tqdm


def load_yaml(file_path: str):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def acc_rej(data):
    acc_rej_list = []
    command_list = []
    commands = {k: v for k, v in data.items() if k.startswith('pred')}
    label = data['guidance_0']

    for key in commands:
        rej_content = data.get(key, '')
        acc_rej_list.append(
            [label, rej_content]
        )
        command_list.append(rej_content)

    rate_list = list(data['average_rate'])
    command_rate_pairs = list(zip(command_list, rate_list))
    sort_command_rate = sorted(command_rate_pairs, key=lambda x: x[1], reverse=True)

    for i in range(len(commands)):
        for j in range(i, len(commands)):
            if sort_command_rate[i][1] == 0:
                continue
            else:
                if sort_command_rate[i][1] != sort_command_rate[j][1]:
                    acc_rej_list.append(
                        [sort_command_rate[i][0], sort_command_rate[j][0]]
                    )

    return acc_rej_list


def main(args):
    input_file = args.input_file
    save_file = args.save_file
    config_path = args.config_path

    instance_template = load_yaml(config_path).get('template', '')
    os.makedirs(os.path.dirname(save_file), exist_ok=True)

    num = 0
    with open(save_file, 'w') as savef:
        with open(input_file, 'r') as infile:
            total_lines = sum(1 for _ in infile)  # 计算总行数
            infile.seek(0)
            with tqdm(total=total_lines, desc=f"Processing", unit="line") as pbar:
                for idx, line in enumerate(infile, start=1):
                    data = json.loads(line)
                    acc_rej_list = acc_rej(data)
                    for ar in acc_rej_list:
                        acc = ar[0]
                        rej = ar[1]
                        issue_and_prestep = data.get('issue_and_prestep', '')
                        message = instance_template.format(
                            issue_and_prestep=issue_and_prestep,
                        )

                        meta_data = {
                            "conversations": [
                                {
                                    "from": "human",
                                    "value": message
                                }
                            ],
                            "chosen": {
                                "from": "gpt",
                                "value": acc
                            },
                            "rejected": {
                                "from": "gpt",
                                "value": rej
                            },
                        }
                        json.dump(meta_data, savef)
                        savef.write('\n')
                        num += 1
                    pbar.update(1)

    print(f"Total line is : {num}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate DPO-style acc/rej pairs from ranked data")
    parser.add_argument(
        "--input_file",
        type=str,
        default="./4-rank/save/rate.jsonl",
        help="Path to rate.jsonl with average_rate and predictions",
    )
    parser.add_argument(
        "--save_file",
        type=str,
        default="./5-generate_datasets/acc_rej.jsonl",
        help="Path to save generated acc/rej pairs",
    )
    parser.add_argument(
        "--config_path",
        type=str,
        default="./5-generate_datasets/template.yaml",
        help="Template config for building the conversation prompt",
    )
    args = parser.parse_args()
    main(args)

import re
import os
import json
import argparse


def extract_rates(rates_string):
    rate_list = []

    rate = re.findall(r'(?<=Rate: )\d+\.\d+', rates_string)
    if rate:  # 如果找到匹配的值
        for item in rate:
            score_i = float(item)
            rate_list.append(score_i)
        return rate_list
    else:
        print(f"Warning: No rate found in string: {rates_string}")
        return []

def average(response1, response2, response3, line_number):
    if response1 and response2 and response3:
        rates1 = extract_rates(response1)
        rates2 = extract_rates(response2)
        rates3 = extract_rates(response3)
    else:
        print("Some response missing!")
        print(f'{line_number}:\n{response1}\n{response2}\n{response3}\n\n')
        return 0

    if len(rates1) == len(rates2) == len(rates3):
        average_rates = [(a + b + c) / 3 for a, b, c in zip(rates1, rates2, rates3)]
    else:
        print("Some data missing!")
        print(f'{line_number}:\n{rates1}\n{rates2}\n{rates3}\n\n')
        return 0

    return average_rates

def main(args):
    data_path = args.data_path
    seeds = args.seeds
    path = args.save_dir
    if not seeds or not path:
        print('Wrong! Refuse to exec!!!')
        return

    os.makedirs(path, exist_ok=True)
    save_file_name = 'rate.jsonl'
    save_path = os.path.join(path, save_file_name)
    path1 = f'rank_seed_{seeds[0]}-final.jsonl'
    data_path1 = os.path.join(path, path1)
    path2 = f'rank_seed_{seeds[1]}-final.jsonl'
    data_path2 = os.path.join(path, path2)
    path3 = f'rank_seed_{seeds[2]}-final.jsonl'
    data_path3 = os.path.join(path, path3)

    with open(save_path, 'w') as savefile:
        with open(data_path1, 'r') as infile1, open(data_path2, 'r') as infile2, open(data_path3, 'r') as infile3, open(data_path, 'r') as dataf:
            for line_number, (line1, line2, line3, line4) in enumerate(zip(infile1, infile2, infile3, dataf), start=1):
                data1 = json.loads(line1)
                data2 = json.loads(line2)
                data3 = json.loads(line3)
                data = json.loads(line4)
                
                response1 = data1['response']
                response2 = data2['response']
                response3 = data3['response']

                rate_list = average(response1, response2, response3, line_number)
                data['average_rate'] = rate_list
                json.dump(data, savefile)
                savefile.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Average ranking scores across multiple seeds")
    parser.add_argument(
        "--data_path",
        type=str,
        default="./3-traj_pred/result/datasets/final_RM.jsonl",
        help="Path to RM data used as reference (same as ranking input)",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        default="./4-rank/save",
        help="Directory containing rank_seed_* files and where rate.jsonl will be saved",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[128, 512, 1024],
        help="Seeds corresponding to rank_seed_{seed}-final.jsonl files",
    )
    args = parser.parse_args()
    main(args)

import json
from tqdm import tqdm

a_r_path = './5-generate_datasets/acc_rej.jsonl'
filter_path = './5-generate_datasets/long_context_SFT_special.jsonl'
dpo_save_path = './5-generate_datasets/dpo_datasets.jsonl'

queries = []
num = 0
# 逐行读取 JSONL 文件并提取 query
with open(filter_path, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line.strip())
        query = data.get("conversations", [{}])[0].get("value", "")
        queries.append(query)

with open(dpo_save_path, 'w') as savef:
    with open(a_r_path, 'r', encoding='utf-8') as infile:
        total_lines = sum(1 for _ in infile)  # 计算总行数
        infile.seek(0) 
        with tqdm(total=total_lines, desc="Processing lines", unit="line") as pbarp:
            for line in infile:
                data = json.loads(line)
                pbarp.update(1)
                query_content = data.get("conversations", [{}])[0].get("value", "")
                if query_content in queries:
                    continue
                else:
                    num += 1
                    json.dump(data, savef)
                    savef.write('\n')
                
print(f"total line: {num}")

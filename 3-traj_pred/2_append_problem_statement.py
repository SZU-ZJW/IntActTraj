import json
import os

interaction_file = '3-traj_pred/result/interaction_data/interaction_data.jsonl'
data_path = '2-SWE-agent/datasets/python__mypy_final.jsonl'
save_path = '3-traj_pred/result/interaction_data/interaction_data_final.jsonl'

os.makedirs(os.path.dirname(save_path), exist_ok=True)

with open(save_path, 'w') as outfile:
    with open(interaction_file, 'r') as inter_file:
        for line in inter_file:
            data = json.loads(line)
            instance_id = data['instance_id']
            problem_statement = None
            with open(data_path, 'r') as dataf:
                for dline in dataf:
                    ddata = json.loads(dline)
                    dins = ddata['instance_id']
                    if dins == instance_id:
                        problem_statement = ddata['problem_statement']
            if problem_statement is not None:
                data["problem_statement"] = problem_statement
                json.dump(data, outfile)
                outfile.write('\n')
            else:
                print(instance_id)
            

import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from utils.log import get_logger
from utils.utils import get_all_files_in_directory, get_instance_id

from tqdm import tqdm


def main():
    traj_path = './2-SWE-agent/traj_collector'
    history_path = '3-traj_pred/result/traj_history'
    save_path = '3-traj_pred/result/interaction_data/interaction_data.jsonl'
    
    os.makedirs(history_path, exist_ok=True)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    file_path = get_all_files_in_directory(traj_path)
    with tqdm(total=len(file_path), desc='Processing') as pbar:
        with open(save_path, 'w') as outfile:
            for path in file_path:
                # accquire the history content in traj
                with open(path, 'r') as infile:
                    traj_content = infile.read()
                traj_json = json.loads(traj_content)
                history_traj_content = traj_json.get('history', [])
                
                # save the history content into history_traj
                instance_id = get_instance_id(path)
                file_name = f'{instance_id}_history.traj'
                save_file_path = os.path.join(history_path, file_name)
                with open(save_file_path, 'w') as savefile:
                    for entry in history_traj_content:
                        savefile.write(json.dumps(entry)+'\n')
                
                steps_data = {}
                j = 1
                for i in range(3, len(history_traj_content), 2):
                    if i + 2 < len(history_traj_content):  
                        batch = history_traj_content[i:i+2]
                        for batch_item in batch:
                            if batch_item['role'] == 'assistant':
                                action_content = batch_item['action']
                            if batch_item['role'] == 'user':
                                feedback_content = batch_item['content']
                    else:
                        action_content = history_traj_content[i]['action']
                        feedback_content = None
                    
                    step_key = f"step_{j}"
                    steps_data[step_key]={
                        "action":action_content,
                        "feedback":feedback_content
                    }
                    j = j + 1
                interaction_data = {
                    "instance_id":instance_id,
                    **steps_data
                }
                outfile.write(json.dumps(interaction_data) + '\n')

if __name__ == "__main__":
    main()

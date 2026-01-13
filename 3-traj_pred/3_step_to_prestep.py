# plan B: 提取所有步骤
import json

def clean_trailing_newline(input_str):
    # 如果字符串没有换行符，直接返回原内容
    if not input_str.endswith('\n'):
        return input_str
    
    # 如果有一个换行符，删除它
    if input_str.endswith('\n') and not input_str.endswith('\n\n'):
        return input_str[:-1]
    
    # 如果有多个换行符，删除一个
    return input_str.rstrip('\n') + '\n'

interaction_file_path = f"./3-traj_pred/result/interaction_data/interaction_data_final.jsonl"
dataset_for_RM = f"./3-traj_pred/result/interaction_data/interaction_data_for_Train.jsonl"
with open (dataset_for_RM, 'w') as dataset_for_RM_file:
    with open (interaction_file_path, 'r') as inter_file:
        for line in inter_file:
            instance_item = json.loads(line)
            last_step_key = None
            # 遍历字典的键，寻找step的轮数step_number
            for key in instance_item.keys():
                if key.startswith('step_'):
                    last_step_key = key
            if last_step_key is None:
                print("没有找到'step_'开头的键")
                continue
            else:
                count = 1
                step_number = last_step_key.split('_')[1]
                issue_content = f"\n ***ISSUE*** \n {instance_item.get('problem_statement')} \n ***END_OF_ISSUE***\n"
                label_content = f"\n {instance_item.get('step_1').get('action')}"
                clean_label_content = clean_trailing_newline(label_content)
                prestep_content_tail = f"\n ***END_OF_STEP_AND_EXECUTION_RESULTS***"
                meta_dataset_list = {
                    "instance_id":instance_item.get('instance_id'),
                    "issue_and_prestep":issue_content,
                    "label":clean_label_content
                }
                json.dump(meta_dataset_list, dataset_for_RM_file)
                dataset_for_RM_file.write(f'\n')
                prestep_content_1 = '\n'
                for step_idx in range(1, int(step_number)): 
                    prestep_content_head = f"\n ***STEP_AND_EXECUTION_RESULTS-{count}***"
                    prestep_content_body_1 = f"\n STEP:\n {instance_item.get(f'step_{step_idx}').get('action')} \n EXECUTION_RESULTS:\n {instance_item.get(f'step_{step_idx}').get('feedback')}"
                    prestep_content_1 =  prestep_content_1 + prestep_content_head + prestep_content_body_1
                    prestep_content = prestep_content_1 + prestep_content_tail
                    issue_and_prestep_content = issue_content + prestep_content
                    label_content = instance_item.get(f'step_{step_idx + 1}', {}).get('action', [])
                    clean_label_content = clean_trailing_newline(label_content)
                    meta_dataset_list={
                        "instance_id":instance_item.get('instance_id'),
                        "issue_and_prestep":issue_and_prestep_content,
                        "label":clean_label_content
                    }
                    count = count + 1
                    json.dump(meta_dataset_list,dataset_for_RM_file)
                    dataset_for_RM_file.write(f'\n')
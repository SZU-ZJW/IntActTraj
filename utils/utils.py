import os
import re
import json
import yaml
import requests
import subprocess

from tool.log import get_logger

logger  = get_logger()
# GitHub API token is read from environment variable to avoid hard-coding secrets
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def load_yaml(file_path: str):
    with open(file_path,'r') as file:
        return yaml.safe_load(file)

def get_pr_title(repo_path, pr_id):
    try:
        # 确保在正确的路径下执行命令
        os.chdir(repo_path)  # 替换为你的代码库路径
        
        result = subprocess.run(
            ['gh', 'pr', 'view', str(pr_id), "--json", "title"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ,  # 确保使用当前环境
            encoding='utf-8',
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return None
    except FileNotFoundError:
        logger.error("PRT-The specified path does not exist.")
        return None
    
def get_pr_body(repo_path, pr_id):
    try:
        # 确保在正确的路径下执行命令
        os.chdir(repo_path)  # 替换为你的代码库路径
        
        result = subprocess.run(
            ['gh', 'pr', 'view', str(pr_id), "--json", "body"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ,  # 确保使用当前环境
            encoding='utf-8',
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return None
    except FileNotFoundError:
        logger.error("PRB-The specified path does not exist.")
        return None

def get_pr_content(repo_path, pr_id):
    pr_title = get_pr_title(repo_path, pr_id)
    pr_body = get_pr_body(repo_path, pr_id)

    if pr_title is None and pr_body is None:
        return None
    else:
        if pr_title is None:
            pr_title = ''
        if pr_body is None:
            pr_body = ''
        pullrequest_statement = pr_title + '\n' + pr_body
        
        return pullrequest_statement
    
def get_issue_title(repo_path, issue_id):
    try:
        # 确保在正确的路径下执行命令
        os.chdir(repo_path)  # 替换为你的代码库路径
        
        result = subprocess.run(
            ['gh', 'issue', 'view', str(issue_id), "--json", "title"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ,  # 确保使用当前环境
            encoding='utf-8',
        )
        if result.stdout is not None:
            title_content = json.loads(result.stdout)['title']
        else:
            title_content = None
        return title_content
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return None
    except FileNotFoundError:
        logger.error("GIT-The specified path does not exist.")
        return None
    
def get_issue_body(repo_path, issue_id):
    try:
        # 确保在正确的路径下执行命令
        os.chdir(repo_path)  # 替换为你的代码库路径
        
        result = subprocess.run(
            ['gh', 'issue', 'view', str(issue_id), "--json", "body"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ,  # 确保使用当前环境
            encoding='utf-8',
        )
        if result.stdout is not None:
            body_content = json.loads(result.stdout)['body']
        else:
            body_content = None
        return body_content
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return None
    except FileNotFoundError:
        logger.error("GIB-The specified path does not exist.")
        return None

def get_issue_content(repo_path, issue_id):
    issue_title = get_issue_title(repo_path, issue_id)
    issue_body = get_issue_body(repo_path, issue_id)

    if issue_title is None and issue_body is None:
        return None
    else:
        if issue_title is None:
            issue_title = ''
        if issue_body is None:
            issue_body = ''
        issue_statement = issue_title + '\n' + issue_body
        
        return issue_statement

def merge_state(repo_path, pr_id):
    '''
    检查某个PR是否被合并，即MERGED状态。
    执行 'gh pr view <pr_id> --json state' 命令
    '''
    try:
        os.chdir(repo_path)  # 替换为你的代码库路径
        
        result = subprocess.run(
            ['gh', 'pr', 'view', str(pr_id), "--json", "state"],
            capture_output=True,
            text=True,
            check=True,
            env=os.environ,  # 确保使用当前环境
            encoding='utf-8',
        )
        state_content = json.loads(result.stdout)['state']
        if state_content == "MERGED":
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return False
    except FileNotFoundError:
        logger.error("MS-The specified path does not exist.")
        return False

def git_reset_hard(repo_path, commit_hash):
    """
    执行 `git reset --hard {hash}` 命令以重置仓库到指定提交。
    """
    try:
        # 切换到仓库目录
        os.chdir(repo_path)
        # 执行 git reset --hard {hash}
        result = subprocess.run(
            ["git", "reset", "--hard", commit_hash],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"执行 git reset 时出错:{e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("未找到 Git。请确保已安装 Git 并且在系统 PATH 中。")
        return False

def extract_version(file_paths, re_express):
    '''
    通过使用正则表达式，提取某个PR的base_commit的版本
    re_express: r'*****'
    file_paths: 存在表明代码库版本文字的文件
    '''
    for path in file_paths:
        if os.path.exists(path):
            with open(path, 'r') as file:
                content = file.read()
                version_pattern = r"{}".format(re_express)
                
                # 使用正则表达式进行匹配
                match = re.search(version_pattern, content)
                if match:
                    return match.group(1)
    
    return None  # 未找到版本信息时返回None

def git_describe_version():
        try:
            result = subprocess.run(
                ["git", "describe", "--always"],
                capture_output=True,
                text=True,
                check=True,
                env=os.environ,  # 确保使用当前环境
                encoding='utf-8',
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Error retrieving PR description: {e}")
            return None
        except FileNotFoundError:
            logger.error("MS-The specified path does not exist.")
            return None

def chang_file(repo_path, pr_id):
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ['gh', 'pr', 'view', str(pr_id), '--json', 'changedFiles'],
            capture_output=True,
            check=True,
            env=os.environ,
            encoding='utf-8',
        )
        changed_file_num = json.loads(result.stdout)['changedFiles']
        return changed_file_num
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return 0
    except FileNotFoundError:
        logger.error("CF-The specified path does not exist.")
        return 0

def sum_line(data):
    sum_changed_line = 0
    add_line = 0
    delet_line = 0
    for meta_data in data['files']:
        add_line = meta_data['additions']
        delet_line = meta_data['deletions']
        sum_changed_line = sum_changed_line + add_line + delet_line
        add_line = 0
        delet_line = 0
    return sum_changed_line

def chang_file_line(repo_path, pr_id):
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ['gh', 'pr', 'view', str(pr_id), '--json', 'files'],
            capture_output=True,
            check=True,
            env=os.environ,
            encoding='utf-8',
        )
        data = json.loads(result.stdout)
        return sum_line(data)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving PR description: {e}")
        return 0
    except FileNotFoundError:
        logger.error("CFL-The specified path does not exist.")
        return 0

def cross_refer_issue_statement(data):
    issue_sum = 0
    for meta_data in data:
        if "event" in meta_data:
            if meta_data['event'] == 'cross-referenced':
                if "issue" in meta_data['source']:
                    if "pull_request" in meta_data['source']['issue']:
                        pr_data = meta_data['source']['issue']['pull_request']
                        if pr_data["merged_at"] is not None:
                            issue_sum += 1
                            problem_title = meta_data['source']['issue']['title']
                            problem_body = meta_data['source']['issue']['body']
                            if problem_title is not None or problem_body is not None:
                                problem_statement = problem_title + '\n' + problem_body
    if issue_sum >1 or issue_sum == 0:
        logger.error(f'{issue_sum} - Too Much or Too Low!')
        return None
    else: 
        return problem_statement

def cross_refer_pr_id(data):
    issue_sum = 0
    for meta_data in data:
        if "event" in meta_data:
            if meta_data['event'] == 'cross-referenced':
                if "issue" in meta_data['source']:
                    if "pull_request" in meta_data['source']['issue']:
                        pr_data = meta_data['source']['issue']['pull_request']
                        if pr_data["merged_at"] is not None:
                            issue_sum += 1
                            pr_id = meta_data['source']['issue']['number']
    if issue_sum >1 or issue_sum == 0:
        logger.error(f'{issue_sum} - Too Much or Too Low!')
        return None
    else: 
        return pr_id

def issue_id_to_statement(repo_name, issue_id):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{issue_id}'
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        try:
            detail = response.json()
        except ValueError:
            logger.error("Error: Response content is not valid JSON.")
            return None

        issue_title = detail['title']
        issue_body = detail['body']
        if issue_title is not None or issue_body is not None:
            problem_statement = issue_title + '\n' + issue_body
        return problem_statement

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")

    return None

def time_to_detail(repo_name, pr_id):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{pr_id}/timeline'
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        try:
            timeline = response.json()
        except ValueError:
            logger.error("Error: Response content is not valid JSON.")
            return None

        problem_statement = cross_refer_issue_statement(timeline)
        return problem_statement

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")

    return None

def time_to_pr_id(repo_name, issue_id):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{issue_id}/timeline'
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        try:
            timeline = response.json()
        except ValueError:
            logger.error("Error: Response content is not valid JSON.")
            return None

        problem_statement = cross_refer_pr_id(timeline)
        return problem_statement

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")

    return None

def extract_base_commit(data):
    if "base" in data:
        return data['base']['sha']
    else:
        logger.error('base not found')
        return None

def get_base_commit(repo_name, pr_id):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/pulls/{pr_id}'
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        try:
            timeline = response.json()
        except ValueError:
            logger.error("Error: Response content is not valid JSON.")
            return None

        base_commit = extract_base_commit(timeline)
        if base_commit:
            return base_commit
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")

    return None

def split_patch(patch_text):
    patch = []
    test_patch = []
    
    current_chunk = []
    is_test_file = False

    # 定义测试相关的关键字
    test_keywords = [
        "test", "testing", "tests", "unittest", "spec", "mock", "fixture",
        "assert", "pytest", "junit", "karma", "mocha", "chai", 
        "cypress", "selenium", "scenario", "integration", "e2e", 
        "benchmark", "coverage"
    ]

    for line in patch_text.splitlines():
        if line.startswith("diff --git"):
            # Save the previous chunk
            if current_chunk:
                if is_test_file:
                    test_patch.extend(current_chunk)
                else:
                    patch.extend(current_chunk)
                current_chunk = []

            # Check if this file is a test-related file
            match = re.search(r' a/([^ ]+)', line)
            if match:
                file_path = match.group(1).lower()
                is_test_file = any(keyword in file_path for keyword in test_keywords)

        current_chunk.append(line)

    # Save the last chunk
    if current_chunk:
        if is_test_file:
            test_patch.extend(current_chunk)
        else:
            patch.extend(current_chunk)

    return "\n".join(patch), "\n".join(test_patch)

def get_patch_test_patch(repo_name, pr_id):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://patch-diff.githubusercontent.com/raw/{re_repo_name}/pull/{pr_id}.diff'
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        patch_content = response.text
        patch, test_patch= split_patch(patch_content)

        return patch, test_patch
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")

    return None, None

def get_releases(repo_name):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues?state=closed'
    issue_id_list = []
    headers = {'Authorization': f'token {TOKEN}'}
    page_sum= 0
    while url:
        response = requests.get(url, headers=headers)
        page_sum += 1
        if page_sum%10 == 0:
            logger.info(f"{page_sum}")
            
        # 检查请求是否成功
        if response.status_code != 200:
            logger.error(f"Error fetching releases: {response.status_code} - {response.text}")
            break
        
        releases = response.json()
        for release in releases:
            if "pull_request" not in release:
                state = release['state']
                if state == 'closed':
                    issue_id = release['number']
                    issue_id_list.append(issue_id)

        if 'Link' in response.headers:
            links = response.headers['Link']
            if 'prev' not in links:
                next_link = re.search(r'<(.*?)>; rel="next"', links)
                url = next_link.group(1) if next_link else None
            elif 'next' not in links:
                url = None
            else:
                match = re.search(r'<([^>]+)>;.*?<([^>]+)>', links)
                url = match.group(2) if match else None

    return issue_id_list

def get_pr_create_time(repo_name, pr_id):
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{pr_id}'
    headers = {'Authorization': f'token {TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        try:
            detail = response.json()
        except ValueError:
            logger.error("Error: Response content is not valid JSON.")
            return None

        create_at = detail['created_at']
        if create_at:
            return create_at
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")

    return None

# ==========================================================================================

def get_all_files_in_directory(directory_path):
    '''
    Get the paths of all files under the traj_collector path
    '''
    file_list = []
    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # 检查是否为文件（排除子目录）
        if os.path.isfile(file_path):
            file_list.append(file_path)
    
    return file_list

def get_instance_id(path):

    filename = path.split('/')[-1]
    base_name = filename.rsplit('.', 1)[0]

    return base_name

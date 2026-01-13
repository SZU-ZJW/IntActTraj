import json
import os
import asyncio
import httpx
from tqdm import tqdm
import sys
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from utils.utils import git_reset_hard, merge_state
from utils.log import get_logger

logger = get_logger()
TOKENS = [
    'ghp_**********YourFirstToken********',  # 替换为你的第一个 token
    'ghp_**********YourSecondToken********',  # 替换为你的第二个 token
]
current_token_index = 0

async def switch_token():
    """切换到下一个可用的 TOKEN"""
    global current_token_index
    current_token_index = (current_token_index + 1) % len(TOKENS)
    logger.info(f"Switching to token {current_token_index + 1}")
    return TOKENS[current_token_index]

async def fetch_with_retries(client, url, headers, max_retries=3):
    """带重试的异步请求，支持 TOKEN 轮换"""
    global current_token_index
    original_token = headers['Authorization'].split(' ')[1]
    
    for attempt in range(max_retries):
        try:
            # 每次请求前添加短暂延迟
            await asyncio.sleep(0.5)  # 添加 0.5 秒延迟
            
            response = await client.get(url, headers=headers, follow_redirects=True)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.error(f"Resource not found: {url}")
                return None
            elif response.status_code == 403:
                logger.error(f"Rate limit exceeded, trying next token...")
                new_token = await switch_token()
                headers['Authorization'] = f'token {new_token}'
                # 切换 TOKEN 时等待更长时间
                await asyncio.sleep(5)  # 切换 TOKEN 后等待 5 秒
                continue
            else:
                logger.error(f"HTTP {response.status_code} for {url}")
                await asyncio.sleep(1)  # 其他错误等待 2 秒
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts: {url}, error: {e}")
                return None
            await asyncio.sleep(1)
    
    headers['Authorization'] = f'token {original_token}'
    return None

async def get_releases_async(client, repo_name):
    """异步获取所有closed issues"""
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues?state=closed&per_page=100'
    headers = {'Authorization': f'token {TOKENS[current_token_index]}'}
    issue_id_list = []
    page = 1
    
    while True:
        page_url = f"{url}&page={page}"
        data = await fetch_with_retries(client, page_url, headers)
        if not data or len(data) == 0:
            break
            
        for issue in data:
            if "pull_request" not in issue and issue['state'] == 'closed':
                issue_id_list.append(issue['number'])
        
        page += 1
        if page % 10 == 0:
            logger.info(f"Processed {page} pages")
    
    return issue_id_list

async def process_single_issue(client, repo_name, issue_id, repo_path):
    """处理单个issue的异步函数"""
    try:
        pr_id = await time_to_pr_id_async(client, repo_name, issue_id)
        if not pr_id or not merge_state(repo_path, pr_id):
            return None

        problem_statement = await issue_id_to_statement_async(client, repo_name, issue_id)
        if not problem_statement:
            return None

        instance_id = f"{repo_name}-{pr_id}"
        logger.info(f'▶️ {instance_id}')

        base_commit = await get_base_commit_async(client, repo_name, pr_id)
        if not base_commit:
            return None

        patch, test_patch = await get_patch_test_patch_async(client, repo_name, pr_id)
        if not patch or 'diff' not in patch:
            return None

        signal = git_reset_hard(repo_path, base_commit)
        if not signal:
            return None

        pr_create_time = await get_pr_create_time_async(client, repo_name, pr_id)
        if not pr_create_time:
            return None

        return {
            "repo": repo_name.replace('__', '/'),
            "instance_id": instance_id,
            "base_commit": base_commit,
            "problem_statement": problem_statement,
            "patch": patch,
            "test_patch": test_patch,
            "created_at": pr_create_time
        }
    except Exception as e:
        logger.error(f"Error processing issue {issue_id}: {e}")
        return None

async def process_issues_batch(client, repo_name, issue_ids, repo_path, batch_size=5):  # 减小批处理大小
    """批量处理issues"""
    results = []
    
    with tqdm(total=len(issue_ids), desc=f"Processing {repo_name}", unit="issue") as pbar:
        for i in range(0, len(issue_ids), batch_size):
            batch = issue_ids[i:i + batch_size]
            tasks = [process_single_issue(client, repo_name, issue_id, repo_path) 
                    for issue_id in batch]
            batch_results = await asyncio.gather(*tasks)
            valid_results = [r for r in batch_results if r is not None]
            results.extend(valid_results)
            
            # 更新进度条
            pbar.update(len(batch))
            pbar.set_postfix({
                'success': len(valid_results),
                'total_success': len(results)
            })
            
            # 每个批次处理完后等待
            await asyncio.sleep(2)  # 批次间等待 2 秒
    
    return results

async def time_to_pr_id_async(client, repo_name, issue_id):
    """异步版本的time_to_pr_id"""
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{issue_id}/timeline'
    headers = {'Authorization': f'token {TOKENS[current_token_index]}'}
    
    data = await fetch_with_retries(client, url, headers)
    if not data:
        return None
        
    issue_sum = 0
    pr_id = None
    for event in data:
        if event.get("event") == "cross-referenced":
            if "issue" in event.get("source", {}):
                if "pull_request" in event["source"]["issue"]:
                    pr_data = event["source"]["issue"]["pull_request"]
                    if pr_data.get("merged_at"):
                        issue_sum += 1
                        pr_id = event["source"]["issue"]["number"]
    
    if issue_sum == 1:
        return pr_id
    #logger.error(f'{issue_sum} - Too Much or Too Low!')
    return None

async def issue_id_to_statement_async(client, repo_name, issue_id):
    """异步版本的issue_id_to_statement"""
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{issue_id}'
    headers = {'Authorization': f'token {TOKENS[current_token_index]}'}
    
    data = await fetch_with_retries(client, url, headers)
    if not data:
        return None
        
    issue_title = data.get('title')
    issue_body = data.get('body')
    if issue_title is not None or issue_body is not None:
        return f"{issue_title or ''}\n{issue_body or ''}"
    return None

async def get_base_commit_async(client, repo_name, pr_id):
    """异步版本的get_base_commit"""
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/pulls/{pr_id}'
    headers = {'Authorization': f'token {TOKENS[current_token_index]}'}
    
    data = await fetch_with_retries(client, url, headers)
    if data and "base" in data:
        return data['base'].get('sha')
    return None

async def get_patch_test_patch_async(client, repo_name, pr_id):
    """异步版本的get_patch_test_patch"""
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://patch-diff.githubusercontent.com/raw/{re_repo_name}/pull/{pr_id}.diff'
    headers = {'Authorization': f'token {TOKENS[current_token_index]}'}
    
    try:
        response = await client.get(url, headers=headers, follow_redirects=True)
        if response.status_code != 200:
            return None, None
        
        patch_content = response.text
        
        patch = []
        test_patch = []
        current_chunk = []
        is_test_file = False
        
        test_keywords = [
            "test", "testing", "tests", "unittest", "spec", "mock", "fixture",
            "assert", "pytest", "junit", "karma", "mocha", "chai",
            "cypress", "selenium", "scenario", "integration", "e2e",
            "benchmark", "coverage"
        ]
        
        for line in patch_content.splitlines():
            if line.startswith("diff --git"):
                if current_chunk:
                    if is_test_file:
                        test_patch.extend(current_chunk)
                    else:
                        patch.extend(current_chunk)
                    current_chunk = []
                
                import re
                match = re.search(r' a/([^ ]+)', line)
                if match:
                    file_path = match.group(1).lower()
                    is_test_file = any(keyword in file_path for keyword in test_keywords)
            
            current_chunk.append(line)
        
        if current_chunk:
            if is_test_file:
                test_patch.extend(current_chunk)
            else:
                patch.extend(current_chunk)
        
        return "\n".join(patch), "\n".join(test_patch)
    except Exception as e:
        logger.error(f"Error fetching patch: {e}")
        return None, None

async def get_pr_create_time_async(client, repo_name, pr_id):
    """异步版本的get_pr_create_time"""
    re_repo_name = repo_name.replace('__', '/')
    url = f'https://api.github.com/repos/{re_repo_name}/issues/{pr_id}'
    headers = {'Authorization': f'token {TOKENS[current_token_index]}'}
    
    data = await fetch_with_retries(client, url, headers)
    if data:
        return data.get('created_at')
    return None

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=str, required=True, help="Base directory where repositories are located")
    parser.add_argument("--save-root", type=str, required=True, help="Base directory where results will be saved")
    parser.add_argument(
        "--repos",
        nargs="*",
        default=[
            "comfyanonymous__ComfyUI",
            "xtekky__gpt4free",
            "sherlock-project__sherlock",
            "localstack__localstack",
            "meta-llama__llama",
            "apache__airflow",
            "vllm-project__vllm",
            "mitmproxy__mitmproxy",
            "lm-sys__FastChat",
            "ultralytics__ultralytics",
            "OpenBB-finance__OpenBB",
            "httpie__cli",
            "sqlmapproject__sqlmap",
            "certbot__certbot",
            "open-mmlab__mmdetection",
            "unclecode__crawl4ai",
            "Lightning-AI__pytorch-lightning",
            "ManimCommunity__manim",
            "StevenBlack__hosts",
            "huggingface__diffusers",
            "mindsdb__mindsdb",
        ],
        help="List of repositories in 'owner__name' format",
    )
    return parser.parse_args()


async def main(args):
    repo_list = args.repos

    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    async with httpx.AsyncClient(timeout=30.0, limits=limits, verify=False) as client:
        for repo_name in repo_list:
            save_dir = os.path.join(args.save_root, repo_name)
            save_path = os.path.join(save_dir, f"{repo_name}.jsonl")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            repo_path = os.path.join(args.repo_root, repo_name)

            logger.info('⏳ Getting the closed ISSUE_ID ... ...')
            issue_id_list = await get_releases_async(client, repo_name)
            logger.info(f'📜 ISSUE ID List:\n{issue_id_list}')

            if issue_id_list:
                results = await process_issues_batch(client, repo_name, issue_id_list, repo_path)
                
                with open(save_path, 'w') as savef:
                    for result in results:
                        json.dump(result, savef)
                        savef.write('\n')

if __name__ == "__main__":
    cli_args = parse_args()
    asyncio.run(main(cli_args))

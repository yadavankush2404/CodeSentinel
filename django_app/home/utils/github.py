import requests
import base64
import uuid
from urllib.parse import urlparse

from .ai_agent import code_analysis_llm


def parse_url(url):
    pass_url = urlparse(url)
    path_parts = pass_url.path.strip('/').split("/")
    if len(path_parts) >=2:
        owner,repo = path_parts[0],path_parts[1]
        return owner, repo
    return None, None

def fetch_pr_files(repo_url, pr_num, git_token=None):
    owner, repo = parse_url(repo_url)
    url =f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/files"
    headers = {"Authorization": f"token {git_token}"} if git_token else {}
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_file_content(repo_url, file_path, git_token=None):
    owner, repo = parse_url(repo_url)
    url =f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token {git_token}"} if git_token else {}
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    content = response.json()
    encoded_data = content.get('content')
    print(encoded_data)
    base64_str = base64.b64decode(encoded_data)
    return base64_str.decode('utf-8')


def analyze_pr(repo_url,pr_num, git_token= None):
    task_id = str(uuid.uuid4())
    try:
        pr_files = fetch_pr_files(repo_url,pr_num,git_token)
        analyze_pr_res = []
        for file in pr_files:
            file_name = file['filename']
            raw_content = fetch_file_content(repo_url, file_name, git_token)
            analysis_result = code_analysis_llm(raw_content,file_name)
            analyze_pr_res.append({
                "result": analysis_result,
                "file_name": file_name
            })

        return ({
            "task_id": task_id, 
            "result": analyze_pr_res,
            "status": "success"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return {"task_id" : task_id, "result": [], "status": "failed"}
    

# def analyze_pr(repo_url, pr_num, git_token=None):
#     # ... setup ...
#     # 1. Get PR details first to find the 'head sha'
#     pr_details = fetch_pr_details(repo_url, pr_num, git_token) 
#     head_sha = pr_details['head']['sha'] # This is the "magic" ID for the PR code
    
#     pr_files = fetch_pr_files(repo_url, pr_num, git_token)
    
#     for file in pr_files:
#         file_name = file['filename']
#         # 2. Pass the head_sha to fetch_file_content
#         raw_content = fetch_file_content(repo_url, file_name, git_token, ref=head_sha)
#         # ... rest of your code ...




# def fetch_file_content(repo_url, file_path, git_token=None, ref=None):
#     owner, repo = parse_url(repo_url)
#     url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
#     # Add the 'ref' parameter to the URL
#     params = {"ref": ref} if ref else {}
#     headers = {"Authorization": f"token {git_token}"} if git_token else {}
    
#     response = requests.get(url, headers=headers, params=params)
#     response.raise_for_status()
    
#     content_b64 = response.json().get('content', '')
#     return base64.b64decode(content_b64).decode('utf-8')




# github raw
# def fetch_file_content_raw(repo_url, file_path, git_token=None, ref=None):
#     owner, repo = parse_url(repo_url)
#     url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    
#     headers = {
#         "Authorization": f"token {git_token}" if git_token else "",
#         "Accept": "application/vnd.github.v3.raw" # <--- THIS asks for the raw text
#     }
#     params = {"ref": ref} if ref else {}

#     response = requests.get(url, headers=headers, params=params)
#     response.raise_for_status()
    
#     return response.text # No decoding needed!
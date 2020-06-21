import requests
import git
import json
import re
import uuid
import os

repo_name = input('Enter repo name: ')
search_string = input('Enter search string: ')

repo_api = "https://api.github.com/repos/{}/git/refs/tags".format(repo_name)

dir_name = repo_name.split('/')[1]

local_repo = "repos/{}".format(dir_name)
full_local_path = os.path.abspath(local_repo)

repo_clone_url = "https://github.com/{}".format(repo_name)

repo = git.Repo.clone_from(repo_clone_url, local_repo)

response = requests.get(repo_api)
final_res = response.json()

dictionary = {}
i = 0

for record in final_res:
    url = record['url']
    tag = url.replace(repo_api,'')[1:]
    git.Git(local_repo).checkout(tag)

    commit_id = git.Git(full_local_path).execute(['git','rev-parse','--short','HEAD'])
    
    url = repo_clone_url + "/blob/"+"{}/".format(commit_id)

    grep_result = git.Git(full_local_path).execute(['git','grep','-nA3',search_string])
    
    
    for multi_line in grep_result.split('--'):
        parts = multi_line.split(':')
        if len(parts) < 1:
            print(parts)
        if len(parts) > 1:
            file_path = parts[0].strip()
            code_line = parts[1].strip()
        
        parsed_result = ""   
        file_url = url + file_path +"#L{}".format(code_line)   
        
        # parse multiline results into a single line
        for line in multi_line.split('\n'):
            if file_path+':' in line:
                line_parts = re.split(":[0-9]+:", line)
            else:
                line_parts = re.split("-[0-9]+-", line)
            
            if len(line_parts) > 1:
                parsed_result += line_parts[1].strip()
  
        each_json = {
                    "uuid":str(uuid.uuid4()),
                    "component": dir_name,
                    "search_string": search_string,
                    "result": parsed_result,
                    "file_path": file_path,
                    "reference": file_url
                    }
        
        dictionary[i] = each_json
        i = i + 1
                    
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, indent=4)


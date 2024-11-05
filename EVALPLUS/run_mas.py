#from evalplus.data import get_human_eval_plus,get_mbpp_plus#, write_jsonl
import requests
import json
import os
import time
import random
import re
import numpy as np
import logging
import traceback
import time
from openai import OpenAI
from os import system
import concurrent.futures
import sys
sys.path.append("/Users/a11/Desktop/MetaAgent/MetaAgent_release")
from baseclass.MultiAgent import MultiAgentSystem
from tqdm import tqdm


def parse_content_between_backticks(s):
    # Split the string by backticks
    if "```" in s:
        code = s.split("```")[1]
        code=code.replace("python","")
    else:
        code=s
    if "<STATE_TRANS>" in code: 
        code=code.split("<STATE_TRANS>")[0]

    # Check if there are at least two backtick blocks
    return code
    
def generate_one_completion(task, agent_dict,state_dict):
    MAS=MultiAgentSystem(agent_dict,state_dict)
    #MAS.reset()
    for _ in range(1):
        try:
            print("Task", task)
            response = MAS.start(f"Complete the coding task:\n{task}")
            print("Response: ",response)
            try:
                answer = parse_content_between_backticks(response)
            except:
                answer = ''
            answer = answer.replace("python", '')
            return answer
        except:
            print(traceback.format_exc())
            time.sleep(3)
    return task + '''\nprint("Error")'''
def get_dataset():
    data_path="/Users/a11/Desktop/MetaAgent/MetaAgent/Dataset/humaneval.jsonl"
    task_dict={}
    with open(data_path,'r') as f:
        for line in f:
            task=json.loads(line)
            task_dict[task['task_id']]=task['problem']
    return task_dict
            
import json

def write_jsonl(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in data:
            # 确保每个字典都转换为JSON字符串，并确保有一个换行符
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
'''
def run(output,meta):
    samples = [
    dict(task_id=task_id, solution=generate_one_completion(problem["prompt"],meta))
    for task_id, problem in get_dataset().items()
    ]
    write_jsonl(output, samples)
    command=f/data/yiwei_zhang/safeagent/MASBenchmark/evalplus/evalplus/evaluate.py --dataset mbpp --samples {output}
    system(command)
'''

import concurrent.futures

def run(agent_dict, state_dict, output):
    dataset = get_dataset()
    samples = []
    print("Generation Start")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_task = {
            executor.submit(generate_one_completion, problem["prompt"], agent_dict, state_dict): task_id
            for task_id, problem in dataset.items()
        }

        for future in tqdm(concurrent.futures.as_completed(future_to_task), total=len(future_to_task), desc="处理任务"):
            task_id = future_to_task[future]
            try:
                solution = future.result()
                samples.append({'task_id': task_id, 'solution': solution})
            except Exception as exc:
                print(traceback.format_exc())
                print(f'{task_id} 生成时出现异常: {exc}')

    write_jsonl(output, samples)
    print("Evaluation Start")
    command = f'''python3 /Users/a11/Desktop/MetaAgent/MetaAgent_release/EVALPLUS/evalplus/evaluate.py --dataset humaneval --samples {output}'''
    system(command)
'''python3 /Users/a11/Desktop/MetaAgent/MetaAgent/EVALPLUS/evalplus/evaluate.py --dataset mbpp --samples /Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/Code/CodeMBPP_HARD_HARD_L3_v2.jsonl'''

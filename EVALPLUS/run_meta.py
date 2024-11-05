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

def parse_content_between_backticks(s):
    # Split the string by backticks
    if "```" in s:
        code = s.split("```")[-2]
        code=code.replace("python","")
    else:
        code=s

    # Check if there are at least two backtick blocks
    return code
    
def generate_one_completion(task,MetaAgent):
    #print("Task\n",task)
    system_prompt='''Solve the python code problems, you answer should follow this format strictly: 
    Final Answer is:
    ```python
    <The whole function>
    ```
    '''
    
    
    
    for _ in range(1):
        try:
            print("Start")
            #print(result)
            response=MetaAgent.infer(system_prompt=system_prompt,message=f"Complete the coding task:\n{task}")
            try:
                answer=response.split("Final Answer")[-1]
                answer=parse_content_between_backticks(response)
            except:
                answer=''
            answer=answer.replace("python",'')
            print("Answer: \n",answer)

                    
            return answer
        except:
            print(traceback.format_exc())
            time.sleep(3)
            #print("CheckPoint",response)
            
            #return task+'''\nprint("hello world")'''
    return task+'''\nprint("Error")'''

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
    command=f/data/yiwei_zhang/safeagent/MetaAgentBenchmark/evalplus/evalplus/evaluate.py --dataset mbpp --samples {output}
    system(command)
'''

def run(output, meta):
    dataset = get_dataset()
    
    # 准备一个列表来收集future对象
    futures = []
    samples = []
    
    # 初始化ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交所有任务
        for task_id, problem in dataset.items():
            # 提交任务到线程池并保存future对象
            future = executor.submit(generate_one_completion, problem["prompt"], meta)
            futures.append((task_id, future))
        
        # 等待所有任务完成并收集结果
        for task_id, future in futures:
            try:
                solution = future.result()  # 获取结果，这里会阻塞直到任务完成
                samples.append({'task_id': task_id, 'solution': solution})
            except Exception as exc:
                print(f'{task_id} generated an exception: {exc}')
    
    # 所有任务完成后，写入文件
    write_jsonl(output, samples)
    
    # 执行系统命令
    command = f'''python3 /Users/a11/Desktop/MetaAgent/MetaAgent/EVALPLUS/evalplus/evaluate.py --dataset humaneval --samples {output}'''
    system(command)

# 注意：确保你的generate_one_completion函数是线程安全的

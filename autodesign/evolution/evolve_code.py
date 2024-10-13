from evo_prompts import *
import json
import sys
sys.path.append("..")
from LLM import LLM
from MetaAgent_release.baseclass.prompts import * # import original prompts
import os
import re
# Step 1. Load Previous Json:
os.environ["OPENAI_API_KEY"] = "sk-JN3JpGrAFt82do4UT7I64uD6BFCIs6Yp0NQywaYPdGCyJABk"
#"sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.org/v1"
mas_path="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/Code/Humaneval_round3.json"
with open(mas_path,"r") as f:
    mas_dict=json.load(f)
eval_task_path="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/Code/HumanEval_round1_eval_results.json"
with open(eval_task_path,"r") as f:
    tasks=json.load(f)

failed_tasks =[]
for task in tasks['eval'].values():
    task_data=task[0]
    if task_data['base_status'] ==  'fail' and len(task_data['base_fail_tests']) > 0:
        print("Task Number",task_data['task_id'])
        failed_tasks.append("Your solution:\n "+task_data['solution']+"\n\n\n\nFailed inputs:\n"+str(task_data['base_fail_tests']))

#print(failed_tasks)
agent_json = mas_dict['agents']
states_json = mas_dict['states']
#print(mas_dict)
'''
origin_task_desc = humaneval_origin
evolution_prompt = evolution_prompt.format(MAS=mas_dict,bad_cases=failed_tasks,task_description=origin_task_desc)
llm=LLM()
rsp=llm.chat(evolution_prompt)
print(rsp)


pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
match = pattern.search(rsp)

if match:
    new_mas = match.group(1)
else:
    new_mas = ""
 

# 将 new_mas 转换为字典
try:
    data_dict = json.loads(new_mas)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    data_dict = {}

#print(data_dict)  
with open("../Code/Humaneval_round3.json","w") as f:
    json.dump(data_dict, f)
'''
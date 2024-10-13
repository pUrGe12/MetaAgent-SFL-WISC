from evo_prompts import *
import json
import sys
sys.path.append("..")
from LLM import LLM
from MetaAgent_release.baseclass.prompts import * # import original prompts
import os
import re
# Step 1. Load Previous Json:
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"
mas_path="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/sde/sde_round1.json"
with open(mas_path,"r") as f:
    mas_dict=json.load(f)
#print(failed_tasks)
failed_tasks='''The sde task is not completed because the tester alwasy failed to know that the file is written and how to start it's test via command line'''
agent_json = mas_dict['agents']
states_json = mas_dict['states']
#print(mas_dict)

origin_task_desc = mlbench_origin
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
with open("../sde/sde_round2.json","w") as f:
    json.dump(data_dict, f)

import sys
sys.path.append("..")
#sys.path.append("/data/yiwei_zhang/safeagent/MetaAgentBenchmark")
#from EVALPLUS.run_mas import run
from mlbench.prompts import *
from MultiAgent import MultiAgentSystem
import json
import os
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"


with open("../sde/sde_round2wotraceback.json", "r") as f:
    mas_dict = json.load(f)

agent_json = mas_dict['agents']
states_json = mas_dict['states']
mas=MultiAgentSystem(agent_json,states_json)
# Load /Users/a11/Desktop/MetaAgent/MetaAgent/Dataset/SoftwareDev.jsonl
import json

# 加载SoftwareDev.jsonl文件
with open("/Users/a11/Desktop/MetaAgent/MetaAgent/Dataset/SoftwareDev.jsonl", "r") as f:
    software_dev_data = [json.loads(line) for line in f]

# 从加载的数据中提取提示信息
prompts = [item["prompt"] for item in software_dev_data]

for prompt in prompts:
    ans=mas.start(prompt)
    print(prompt)
    print("SDE ",ans,prompt)
    print("================================================END OF ONE TASK==================================================")
    mas.reset()
    


'''
def file_write(string, file_path):
    with open(file_path, 'w') as file:
        file.write(string)
'''

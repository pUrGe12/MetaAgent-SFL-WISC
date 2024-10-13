import sys
sys.path.append("..")
sys.path.append("/Users/a11/Desktop/MetaAgent/MetaAgent")
#from EVALPLUS.run_mas import run
from MetaAgent.evaluate.run_trivial_meta import run
from MultiAgent import MultiAgentSystem
import json
import os
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"

def test_writing(mas_path,validation=False,json_path=None):
    with open(mas_path,"r") as f:
        mas_dict=json.load(f)

    agent_json=mas_dict['agents']
    states_json=mas_dict['states']
    #mas=MultiAgentSystem(agent_json,states_json)
    if not validation:
        failed_tasks=run(agent_json,states_json,output="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/writing_answrers.jsonl")
    else:
        failed_tasks=run(agent_json,states_json,output="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/writing_answrers.jsonl",json_path=json_path)
    #meta=mas,output="/data/yiwei_zhang/safeagent/MetaAgentBenchmark/MetaAgent/Code/CodeMBPP_HARD_L0.jsonl")
    #mas.start("a pythpn function return prime numbers under 10000")
    return failed_tasks


mas_path = "/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/writing/writing_round1_1.json"
failed_tasks = test_writing(mas_path=mas_path,validation=False,json_path=None)

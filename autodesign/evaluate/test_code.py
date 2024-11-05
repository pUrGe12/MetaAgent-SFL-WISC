import sys
sys.path.append("..")
sys.path.append("/Users/a11/Desktop/MetaAgent/MetaAgent_release")
from EVALPLUS.run_mas import run
from baseclass.MultiAgent import MultiAgentSystem
import json
import os
os.environ["API_VERSION"]="2024-07-01-preview"
os.environ["AZURE_OPENAI_API_KEY"]="d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"]="https://yaolun-west.openai.azure.com/"  

#os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#"sk-JN3JpGrAFt82do4UT7I64uD6BFCIs6Yp0NQywaYPdGCyJABk"
#
#"sk-fj5OMr9qOnd18U6eIvgflJrmd9HeVBefWFO6u7nlD3O8lwYu"
#
#"sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#os.environ["OPENAI_API_BASE"]="https://api.openai-proxy.org/v1"
with open("/Users/a11/Desktop/MetaAgent/MetaAgent_release/autodesign/HumanEvalMas1028_v2.json","r") as f:
    mas_dict=json.load(f)

agent_json=mas_dict['agents']
states_json=mas_dict['states']
#mas=MultiAgentSystem(agent_json,states_json)
run(agent_json,states_json,output="../HumanEval1028_Result_v2.jsonl")
#meta=mas,output="/data/yiwei_zhang/safeagent/MetaAgentBenchmark/MetaAgent/Code/CodeMBPP_HARD_L0.jsonl")
#mas.start("a pythpn function return prime numbers under 10000")
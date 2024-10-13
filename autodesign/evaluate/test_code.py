import sys
sys.path.append("..")
sys.path.append("/Users/a11/Desktop/MetaAgent/MetaAgent")
from EVALPLUS.run_mas import run
from MultiAgent import MultiAgentSystem
import json
import os
os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#"sk-JN3JpGrAFt82do4UT7I64uD6BFCIs6Yp0NQywaYPdGCyJABk"
#
#"sk-fj5OMr9qOnd18U6eIvgflJrmd9HeVBefWFO6u7nlD3O8lwYu"
#
#"sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#os.environ["OPENAI_API_BASE"]="https://api.openai-proxy.org/v1"
with open("../Code/Humaneval_round3.json","r") as f:
    mas_dict=json.load(f)

agent_json=mas_dict['agents']
states_json=mas_dict['states']
#mas=MultiAgentSystem(agent_json,states_json)
run(agent_json,states_json,output="../Code/HumanEval_round3.jsonl")
#meta=mas,output="/data/yiwei_zhang/safeagent/MetaAgentBenchmark/MetaAgent/Code/CodeMBPP_HARD_L0.jsonl")
#mas.start("a pythpn function return prime numbers under 10000")
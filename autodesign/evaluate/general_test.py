import sys
sys.path.append("..")
sys.path.append("../baseclass")

from MultiAgent import MultiAgentSystem
import json
import os
#os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"

def run_mas_test(mas_json_path, test):
    with open(mas_json_path, "r") as f:
        mas_dict = json.load(f)
    
    agent_json = mas_dict['agents']
    states_json = mas_dict['states']
    
    mas = MultiAgentSystem(agent_json, states_json)
    
    result = mas.start(test)
    
    return result


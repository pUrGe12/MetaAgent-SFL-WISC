# Step 1. Initial Build
import sys
sys.path.append("../baseclass")
from FSM_Gen import gen as generate_MAS 
from MultiAgent import MultiAgentSystem
from prompts import *
import json
from CaseGen import case_gen
from evolution.general_evolve import update_mas
#from evaluate.test_writing import test_writing
#mas_path = "/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/sde/sde_round1.json"
# Step 1. Initial MAS Generation, clarify the Multi-Agent System Saving Path and Cases Saving Path
mas_saving_path = "test_mas.json"
cases_saving_path = "test_cases_debug.jsonl"
generate_MAS(sde_origin,mas_saving_path) #  Initial MAS Generation
# Step 2. Cases Generation
cases = case_gen(sde_origin,mas_saving_path) # Cases Generation
with open(cases_saving_path,"w") as f:
    for case in cases:
        f.write(json.dumps(case)+"\n")
# Step 3. Test on cases
with open(mas_saving_path, "r") as f:
    mas_dict = json.load(f)
agents_json = mas_dict["agents"]
states_json = mas_dict['states']
multi_agent = MultiAgentSystem(agents_json,states_json)
failed_log = [] 
# Get the failed cases log
for case in cases:
    multi_agent.start(user_input=case)
    log = multi_agent.get_running_log()
    if "|completed|" not in log:
        failed_log.append(log)
#print(failed_tasks)
# Step 4. Evolution

update_mas(mas_saving_path,failed_log)
     


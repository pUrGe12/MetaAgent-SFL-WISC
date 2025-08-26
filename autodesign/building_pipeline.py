# Step 1. Initial Build
import sys
sys.path.append("../baseclass")
from FSM_Gen import gen as generate_MAS 
from MultiAgent import MultiAgentSystem
from prompts import *
import json
from CaseGen import case_gen
from evolution.general_evolve import update_mas
from Optimization import optimize_fsm
#from evaluate.test_writing import test_writing
#mas_path = "/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/sde/sde_round1.json"
# Step 1. Initial MAS Generation, clarify the Multi-Agent System Saving Path and Cases Saving Path
mas_saving_path = "test_mas.json"
cases_saving_path = "test_cases_debug.jsonl"
mas_description = ""
generate_MAS(mas_description,mas_saving_path) #  Initial MAS Generation
# Step 2. Optimize
new_fsm = optimize_fsm(mas_saving_path) # Cases Generation

print(new_fsm)


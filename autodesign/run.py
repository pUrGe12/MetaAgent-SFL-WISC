# Step 1. Initial Build
import sys
import argparse
import json
from colorama import init, Fore, Style
sys.path.append("../baseclass")
from FSM_Gen import gen as generate_MAS 
from MultiAgent import MultiAgentSystem
from prompts import *
from CaseGen import case_gen
from evolution.general_evolve import update_mas
  

# 初始化 colorama
init(autoreset=True)

def log(message, level="info"):
    if level == "info":
        print(Fore.CYAN + message)
    elif level == "success":
        print(Fore.GREEN + message)
    elif level == "warning":
        print(Fore.YELLOW + message)
    elif level == "error":
        print(Fore.RED + message)
    else:
        print(message)

def main(mas_saving_path, cases_saving_path, task_description):
    try:
        log("=== Step 1: Initial MAS Generation ===", "info")
        agent_dict, fsm, token_cost = generate_MAS(task_description, mas_saving_path)
        if agent_dict is None or fsm is None:
            log("MAS Generation failed.", "error")
            sys.exit(1)
        log(f"MAS Generation completed. Token Cost: {token_cost}", "success")
        
        log("=== Step 2: Cases Generation ===", "info")
        cases = case_gen(task_description, mas_saving_path)
        with open(cases_saving_path, "w") as f:
            for case in cases:
                f.write(json.dumps(case) + "\n")
        log(f"Cases Generation completed. {len(cases)} cases generated.", "success")
        
        log("=== Step 3: Testing on Cases ===", "info")
        with open(mas_saving_path, "r") as f:
            mas_dict = json.load(f)
        agents_json = mas_dict["agents"]
        states_json = mas_dict['states']
        multi_agent = MultiAgentSystem(agents_json, states_json)
        failed_log = []
        
        for case in cases:
            log(f"Testing case: {case}", "info")
            multi_agent.start(user_input=case)
            log_entry = multi_agent.get_running_log()
            if "|completed|" not in log_entry:
                failed_log.append(log_entry)
                log("A case has failed.", "warning")
        
        log(f"Testing completed. {len(failed_log)} cases failed.", "success")
        
        log("=== Step 4: Evolution ===", "info")
        update_mas(mas_saving_path, failed_log)
        log("Evolution step completed.", "success")
        
    except Exception as e:
        log(f"An unexpected error occurred: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MetaAgent pipeline.")
    parser.add_argument(
        "--mas_path",
        type=str,
        default="test_mas.json",
        help="Path to save the Multi-Agent System JSON file."
    )
    parser.add_argument(
        "--cases_path",
        type=str,
        default="test_cases_debug.jsonl",
        help="Path to save the generated test cases."
    )
    parser.add_argument(
        "--task_description",
        type=str,
        default="Build a Multi-Agent System for software development",
        help="Path to save the generated test cases."  
    )
    
    args = parser.parse_args()
    main(args.mas_path, args.cases_path, args.task_description)

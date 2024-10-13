#from evo_prompts import *
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
def evo_writing(failed_tasks,mas_path):
    evolution_prompt='''
You are a Multi-Agent System Designer. Your task is to modify the Multi-Agent System based on the existing failed task cases.

The goal that this Multi-Agent System needs to solve is: {task_description}

The current structure of the Multi-Agent System is as follows:

Part 1: Agent Design:

Each agent contains three features:

1. name: <The name of the agent>
2. system_prompt: <The system prompt for the agent, describing the overall goal, its name and role, and its responsibility and constraints.>
3. tools: <The equipped tool name, a list>
Part 2: Communication System Design:

We use a finite state machine (FSM) to manage the cooperation of agents. Specifically:

Each state in the FSM should include:

1. state_id: A unique identifier for the state
2. agent_id: The ID of the agent associated with this state
3. instruction: What the agent should do in this state
4. is_initial: Boolean indicating if this is the initial state
5. is_final: Boolean indicating if this is a final state
6. listener: The agent who will save this state's output information in their memory
Notice: Make sure the listener covers all related agents. The agents not listed as a listener would not receive the information (which may cause the failure of cooperation). Hence, some important milestones like a new version of code/answer should be broadcast to all related agents!
The FSM should also include transition functions between states. Each transition function should specify:

1. from_state: The ID of the state this transition is from
2. to_state: The ID of the state this transition goes to
3. condition: A description of the condition that triggers this transition
Both parts are represented in JSON, forming a Multi-Agent System.

The current goal for the Multi-Agent System is: \n {task_description}

The existing Multi-Agent System is: \n {MAS}

While using this Multi-Agent System to solve the problem, it failed: \n {bad_cases}

Please think step by step to optimize the existing Multi-Agent System.
Gradually output your thought process.

WARNING: The number of agents and the number of states should be minimized as much as possible. For saving the token cost!

What are the specific reasons for the failure in the above bad cases? What aspects were not considered, and how can we improve them from the following aspects?
Is the current role positioning of the agents reasonable? Are these agents necessary to solve this task, or do we need to create new agents? (DO NOT ADD AGENT UNLESS IT IS NECESSARY)
Is the current communication structure optimized to reduce the cost of information exchange? (DO NOT ADD STATE UNLESS IT IS NECESSARY)
Are the instructions for each state specific and feasible, and how can they be optimized?
Use add examples in the prompts to optimize the multi-agent system! 
Now, output your thought process and output the new Multi-Agent System design in JSON format.

Please consider: 1. Whether the functionalities of multiple Agents can be integrated into a single Agent to reduce unnecessary communication exchanges. For example, Reasoning and Action should be placed within the same Agent. Please note that the essence of multi-Agent systems is to provide diverse perspectives, not to split task processes and forcibly create Agents. States should also be streamlined as much as possible; one state can accomplish many specific actions, rather than just one action. HOWEVER, THERE MUST BE A FINAL STATE SPECIALLY FOR SUBMITTION , where the agent shold use <|submit|> to submit the final answer. Beacuse when the states transfer to final state, the finite states machine will be shut down. So the final states should contain and only contain the 'sbumit' 

```json
<fill in your Multi-Agent System Design (Agents and FSM)>
```
'''
    #mas_path="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/mlbench/ml_round2.json"
    with open(mas_path,"r") as f:
        mas_dict=json.load(f)
    #print(failed_tasks)

    agent_json = mas_dict['agents']
    states_json = mas_dict['states']
    #print(mas_dict)

    origin_task_desc = writing_origin
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
    # Add "_1" before the suffix of mas_path (save to a new file)
    with open(f"{mas_path[:-5]}_1.json","w") as f:
        json.dump(data_dict, f)

'''
Step 1. Generate Role Description
Step 2. Select Tools
Step 3. Generate DAG
'''
#from llmcenter import ChatClient
import networkx as nx
import matplotlib.pyplot as plt
from LLM import LLM
import json
import networkx as nx
from MultiAgent import MultiAgentSystem
from prompts import *
import os
#os.environ["OPENAI_API_KEY"]="sk-JN3JpGrAFt82do4UT7I64uD6BFCIs6Yp0NQywaYPdGCyJABk"
#os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#os.environ["OPENAI_API_BASE"]="https://api.openai-proxy.org/v1"
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"



def Generate_Role_Description(task):
    prompt_template='''You are the designer of an multi-agent system. Given a general task description, you need generate several roles that could act cooperatively to solve the task. 
    Make sure the role is actually necessary. There is no need to define a role for too trivial functions.
    Before your answer, you should first think step by step to think what role you will design and verify whether the role is necessary.
    You answer should obey the following format:
    Reasoning:<Your reasoning process>
    Answer:
    ```json
    [{"name":<fill in role0 name>,"description":<fill in role0 description>},
    {"name":<fill in role1 name>,"description":<fill in role1 description>},
    ...]
    ```
    Here are some requirements:
    1. There must be an agent who give formal response to the user question, with the <|submit|> token.
        Example:
        User: Calculate 1+10
        ...
        The final output agent: <|submit|>The answer is 11

    4. There must be a agent submit the final answer (use the pattern: \n <|submit|>: <fill in the final answer> \n),clarify this in Instruction

    '''
    role_generator=LLM(prompt_template)
    roles=role_generator.chat(message=f"The task is: {task}\n, now generate the role")
    #print(roles)
    role_json=roles.split("```")[-2].replace("json","")
    role_dict=json.loads(role_json)
    #print(role_dict)
    return role_dict,role_generator

    

def Generate_Agent_Description(task,tools):
    prompt_template='''You are the designer of a multi-agent system. Given a general task description, you first need to design several agents that can cooperately solve this type of task.  
    Each agent contain three features:
    - name: <The name of the agent>
    - system_prompt: <The system prompt for agent, describe the overall goal, its name and role, and its responsibility and constrain.> 
    - tools: <The equiped tool name, a list>
    You are required to define an agent in json format.  
    You answer should obey the following format:
    Task Analyse: What specific scenarios the task covers? How to design agents that can adapt to these scenarios
    System Goal Design: 
    Agents Define: 
    ```json
    [{{"agent_id":"0","name":<fill in agent0's name>,"system_prompt":<fill in agent1's system_prompt>,"tools":[<tool1>,<tool2>,...]}},
    {{"agent_id":"1","name":<fill in agent1's name>,"system_prompt":<fill in agent2's system_prompt>,"tools":[..]}},
    ...]
    ```

    WARNING: The Agent you design should be autonomous agents, which can not ask humanfeedback or wait for human answer!
    You can't design too many redundant agents. More Agents means more cost!  Agents need to cooperate efficiently
    '''

    
    agent_generator=LLM(prompt_template)
    agents=agent_generator.chat(message=f"The General Task is {task} and the tools you can select are {tools}. One agent can equipped with various tools and it can also act without tools. Not every tool is necessary for the task! \n Now design several agents that could act cooperatively to solve these kind of task. Obey the format strictly!")
    
    agent_json=agents.split("```")[-2].replace("json","")
    #print(agents)
    agent_dict=json.loads(agent_json)
    #print(agent_dict)
    
    return agent_dict,agent_generator


tool_list=["code_interpreter","web_search","calculator","none"]  

tools = [
    {
        "name": "execute_python",
        "description": "Execute python code and get code feedback",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code need to be executed"
                }
            },
            "required": ["code"]
        }
    },
    {
        "name": "web_search",
        "description": "Perform a web search and return the results",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to be executed"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": "Perform a calculation and return the result",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to be evaluated"
                }
            },
            "required": ["expression"]
        }
    }
]
tool_list=["code_interpreter","search_engine"]

import json
from LLM import LLM

def Generate_FSM(task, agent_dict):
    prompt_template = '''
    You are the designer of a multi-agent system. Given a general task description and a list of agents, you need to generate a Finite State Machine (FSM) to manage the process of solving the task.
    
    WARNING: You are good at controlling costs, too many agents and too complex cooperation structure can lead to excessive costs of information exchange
    Each state in the FSM should include:
    1. state_id: A unique identifier for the state
    2. agent_id: The ID of the agent associated with this state
    3. instruction: What the agent should do in this state
    4. is_initial: Boolean indicating if this is the initial state
    5. is_final: Boolean indicating if this is a final state
    6. listener: The agent who will save this state output information in their memory
                 Notice : Make sure the listener covers all related agents. The agents not listed as a listener would not received the information(which may cause the failure of cooperation)
                 Hence, some important milestone like a new version of code/answer should be broadcast all related agent！

    The FSM should also include transition functions between states. Each transition function should specify:
    1. from_state: The ID of the state this transition is from
    2. to_state: The ID of the state this transition goes to
    3. condition: A description of the condition that triggers this transition

    Your answer should follow this format:
    Reasoning: <Your step-by-step reasoning process>
    Answer:
    ```json
    {{
      "states": [
        {{
          "state_id": "1",
          "agent_id": "0",
          "instruction": "Perform task X",
          "is_initial": true,
          "is_final": false,
          "listener":["1","2"]
        }},
        ...
      ],
      "transitions": [
        {{
          "from_state": "1",
          "to_state": "2",
          "condition": "If task X is completed successfully"
        }},
        {{
          "from_state": "2",
          "to_state": "1",
          "condition": "If the previous task needs to be re-done."
        }},
        ...
      ]
    }}
    ```

    Rules:
    1. Ensure there is exactly one initial state and at least one final state.
    2. Every non-final state should have at least one outgoing transition.
    3. The FSM should be able to handle loops and complex interactions between agents.
    4. Include a transition to a final state that submits the final answer (use <|submit|> in the instruction).
    5. Make sure all agent_ids in the states correspond to the provided agent_dict.
    6. The transitions should consider as many as possible situations. Which consisit a roadmap for Multi-Agent System in deployment stage.
    '''

    fsm_generator = LLM(prompt_template)
    fsm_response = fsm_generator.chat(message=f"The task is: {task}\nThe agents are: {json.dumps(agent_dict, indent=2)}\nNow generate the FSM")

    # Extract the JSON part from the response
    fsm_json = fsm_response.split("```")[1].strip()
    if fsm_json.startswith("json"):
        fsm_json = fsm_json[4:].strip()

    # Parse the JSON
    try:
        fsm = json.loads(fsm_json)
    except json.JSONDecodeError:
        print("Error: Unable to parse FSM JSON. Raw response:")
        #print(fsm_response)
        return None, fsm_generator

    # Validate the FSM
    if validate_fsm(fsm, agent_dict):
        return fsm, fsm_generator
    else:
        print("Error: Generated FSM is invalid. Raw response:")
        #print(fsm_response)
        return None, fsm_generator

def validate_fsm(fsm, agent_dict):
    # Check if there's exactly one initial state
    initial_states = [state for state in fsm['states'] if state['is_initial']]
    if len(initial_states) != 1:
        print(f"Error: There should be exactly one initial state. Found {len(initial_states)}.")
        return False

    # Check if there's at least one final state
    final_states = [state for state in fsm['states'] if state['is_final']]
    if not final_states:
        print("Error: There should be at least one final state.")
        return False

    # Check if all agent_ids are valid
    valid_agent_ids = set(agent['agent_id'] for agent in agent_dict)
    for state in fsm['states']:
        if state['agent_id'] not in valid_agent_ids:
            print(f"Error: Invalid agent_id {state['agent_id']} in state {state['state_id']}.")
            return False

    # Check if all non-final states have at least one outgoing transition
    state_ids = set(state['state_id'] for state in fsm['states'])
    outgoing_transitions = {state_id: 0 for state_id in state_ids}
    for transition in fsm['transitions']:
        if transition['from_state'] not in state_ids or transition['to_state'] not in state_ids:
            print(f"Error: Invalid state ID in transition {transition}.")
            return False
        outgoing_transitions[transition['from_state']] += 1

    for state in fsm['states']:
        if not state['is_final'] and outgoing_transitions[state['state_id']] == 0:
            print(f"Error: Non-final state {state['state_id']} has no outgoing transitions.")
            return False

    return True

# Update the gen function to use Generate_FSM instead of Generate_DAG
def gen(task,mas_saving_path):
    #role_dict, llm_1 = Generate_Role_Description(task)
    agent_dict, llm_2 = Generate_Agent_Description(task=task, tools=tool_list)
    fsm, llm_3 = Generate_FSM(task=task, agent_dict=agent_dict)
    #print(agent_dict)
    #print(fsm)
    
    if fsm is None:
        print("Failed to generate valid FSM.")
        return None, None, None

    # You might want to implement a function to visualize the FSM here
    # visualize_fsm(fsm)

    token_cost =  llm_2.get_token_cost() + llm_3.get_token_cost()
    #+ llm_1.get_token_cost() +
    with open(mas_saving_path,"w") as f:
        json.dump({"agents":agent_dict,"states":fsm},f)
    return agent_dict, fsm, token_cost

#gen("Design a multi-agent system to solve the following task: \n1. Given a list of numbers, find the sum of all the numbers.\n2. Given the sum, find the product of all the numbers.\n3. Print the product.")
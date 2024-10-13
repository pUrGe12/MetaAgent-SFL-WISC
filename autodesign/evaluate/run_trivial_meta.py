'''
Run Trivial MAS, 
(Run in MASAgent Bench Framework)

'''
import json
import os
from os import system
import sys
sys.path.append("../baseclass")
from MultiAgent import MultiAgentSystem

#from LLM import LLM
'''
def test(rsp,keys):
    total_score=len(keys)
    score=0
    print("Keys: ========",keys)
    is_find=0
    for answers in keys:
        for a in answers:
            a_list=a.split(" ")
            # if any element of a list in rsp, then score+=1
            for a_i in a_list:
                if a_i in rsp:
                    score+=1
                    is_find = 1
                    break
        if is_find:
            is_find= 0
            break
    print("Score:========= ",score)
    return float(score)/total_score
'''
def test(rsp,keys):
    total_score=len(keys)
    score=0
    print("Keys: ========",keys)
    for answers in keys:
        for a in answers:
            if a in rsp:
                score+=1
                is_find=1
                break
    print("Score:========= ",score)
    return float(score)/total_score





def run(agent_json,state_json,output,json_path= "/Users/a11/Desktop/MetaAgent/MetaAgent/Dataset/trivia_creative_writing_100_n_5.jsonl"):
    prompt_template= '''Write a short and coherent story about {topic} that incorporates the answers to the following {n} questions: {questions}
'''
    
    
    MAS=MultiAgentSystem(agent_json,state_json)
    scores=[]
    failed_tasks=[]
    with open(json_path, "r") as f, open(output, "w") as out_f:

        for line in f:
            # 将每行的文本转换为JSON对象
            task = json.loads(line)
            
            # 格式化prompt字符串
            prompt = prompt_template.format(topic=task['topic'], n=len(task['questions']), questions=task['questions'])
            #Model=LLM()
            rsp=MAS.start(prompt)
            # 使用模型生成回应
            #try:
            #    rsp = Model.chat(prompt)
            #except:
            #    continue
            
            # 使用测试函数计算得分
            score = test(rsp, task['answers'])
            print("Score: ",score)  # 打印得分
            
            scores.append(score)
            print(scores)
            print("CurrentAverage: ",sum(scores)/len(scores))

            if score < 0.5:
                failed_tasks.append({"topic":task['topic'],"questions":task['questions'],"answers":task['answers'],"score":score,"current_answer":rsp})
            json.dump({"topic":task['topic'],"questions":task['questions'],"answers":task['answers'],"score":score,"current_answer":rsp}, out_f)
            out_f.write('\n')  # 确保每个任务后面都有换行符
                
    print("Average: ",sum(scores)/len(scores))
    return failed_tasks
                
        

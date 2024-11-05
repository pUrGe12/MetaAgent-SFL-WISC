import json
from evalplus.data import get_human_eval_plus,get_mbpp_plus, write_jsonl


with open("/Users/a11/Desktop/MetaAgent/MetaAgent/outputs/nonembpphard_gpt-4o_811_eval_results.json","r") as f:
    result=json.loads(f.read())
    
print(result["eval"]['Mbpp/590'])
fail_list=[]
for ids in result['eval'].keys():
    if result['eval'][ids][0]['base_status']=='fail':
        fail_list.append(result['eval'][ids][0]['task_id'])
        
print(len(fail_list))

# 获取MBPP数据集的所有任务
mbpp_tasks = get_mbpp_plus()

samples = []
# 对于每个失败的任务ID，如果它在MBPP数据集中，则添加到samples列表
for task_id,problem in mbpp_tasks.items():
    if task_id in fail_list:
        samples.append(dict(task_id=task_id, problem=problem))
else:
    print(f"Task ID {task_id} not found in MBPP dataset.")  # 如果找不到任务ID，打印警告

print(samples[0].keys())
with open("hard_hard_mbpp.jsonl","w") as file:
    for prob in samples: 
        try:
            json_str=json.dumps(prob)
            file.write(json_str+'\n')
        except:
            continue
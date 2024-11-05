import json
from evalplus.data import get_human_eval_plus,get_mbpp_plus, write_jsonl


# 获取MBPP数据集的所有任务
human_eval_tasks = get_human_eval_plus()

samples = []
# 对于每个失败的任务ID，如果它在MBPP数据集中，则添加到samples列表
for task_id,problem in human_eval_tasks.items():
    
    samples.append(dict(task_id=task_id, problem=problem))
with open("humaneval.jsonl","w") as file:
    for prob in samples: 
        try:
            json_str=json.dumps(prob)
            file.write(json_str+'\n')
        except:
            continue
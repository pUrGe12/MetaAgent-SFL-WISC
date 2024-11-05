from evalplus.data import get_human_eval_plus, get_mbpp_plus, write_jsonl
import requests
import json
import os
import time
import random
import re
import numpy as np
import logging
import traceback
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

os.environ["OPENAI_API_KEY"] = "sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"


def parse_content_between_backticks(s):
    # Split the string by backticks
    if "```" in s:
        code = s.split("```")[1]
    else:
        code = s

    # Check if there are at least two backtick blocks
    return code


def generate_one_completion(task):
    print("Task\n", task)
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
    )
    result = [{"role": "system", "content": '''Follow the format:

    ```python
    <The whole function>
    ```                  
                         '''}, {"role": "user", "content": f"{task}"}]

    for _ in range(1):
        try:
            print("Start")
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=result,
                temperature=0,
            )
            print("End")

            role = completion.choices[0].message.role
            content = completion.choices[0].message.content
            rsp = content
            print("RSP", rsp)

            response = rsp
            try:
                answer = parse_content_between_backticks(response)
            except:
                continue
            answer = answer.replace("python", '')
            print("Answer: \n", answer)

            return answer
        except:
            print(traceback.format_exc())
            time.sleep(3)
    return task + '''\nprint("Error")'''


def process_task(task_id, problem):
    return dict(task_id=task_id, solution=generate_one_completion(problem["prompt"]))


def main():
    tasks = get_mbpp_plus().items()
    samples = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_task = {executor.submit(process_task, task_id, problem): (task_id, problem) for task_id, problem in tasks}
        for future in as_completed(future_to_task):
            task_id, problem = future_to_task[future]
            try:
                result = future.result()
                samples.append(result)
            except Exception as exc:
                print(f'Task {task_id} generated an exception: {exc}')
                samples.append(dict(task_id=task_id, solution=problem["prompt"] + '''\nprint("Error")'''))

    write_jsonl("mbppsamples.jsonl", samples)


if __name__ == "__main__":
    main()

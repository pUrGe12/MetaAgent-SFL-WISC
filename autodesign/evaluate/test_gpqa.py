import pandas as pd
import sys
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  # 添加进度条支持
import os
import random
sys.path.append("/Users/a11/Desktop/MetaAgent/MetaAgent_release/autodesign/evaluate")
from general_test import run_mas_test
# 搜索工具提供干扰信息，代码工具应该改成notebook形式
# if we use gpt3.5-turbo, can we enhance the performance by adding tools? 
# use gpt-4o to design and gpt3.5 to evaluate? 
os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"

def create_prompt(question, correct_answer, wrong_answers):
    """
    创建带有随机位置正确答案的提示
    """
    # 将所有答案放入列表并随机打乱
    all_answers = wrong_answers.copy()
    all_answers.append(correct_answer)
    random.shuffle(all_answers)
    
    # 记录正确答案的位置
    correct_position = all_answers.index(correct_answer)
    
    # 构建提示
    prompt = f"{question}\n"
    options = ['(a)', '(b)', '(c)', '(d)']
    for idx, answer in enumerate(all_answers):
        prompt += f"{options[idx]} {answer}\n"
    
    return prompt, options[correct_position]

def get_correct_option_label(answers, correct_answer):
    """
    获取正确答案对应的选项标签，例如 (a), (b), ...
    """
    options = ['(a)', '(b)', '(c)', '(d)']
    for idx, answer in enumerate(answers):
        if answer.strip() == correct_answer.strip():
            return options[idx]
    return None

def process_row(row,mas_json_path):
    """处理单个问题并返回是否正确"""
    question = row['Pre-Revision Question']
    correct_answer = row['Pre-Revision Correct Answer']
    wrong_answers = [
        row['Pre-Revision Incorrect Answer 1'],
        row['Pre-Revision Incorrect Answer 2'],
        row['Pre-Revision Incorrect Answer 3']
    ]
    
    # 创建随机顺序的提示和正确答案标签
    prompt, correct_label = create_prompt(question, correct_answer, wrong_answers)
     
    # 使用 run_mas_test 进行测试
    model_answer = run_mas_test(mas_json_path, prompt)
    print("=====ANSWER=====")
    print(model_answer)
    print("=====\\ANSWER=====")
    print(f"=====ANSWER=====")
    print(f"Question: {question}")
    print(f"Correct answer: {correct_answer} ({correct_label})")
    print(f"Model response: {model_answer}")
    print("=========================")
    
    is_correct = correct_label in model_answer
    return is_correct

def evaluate_model(mas_json_path, max_workers=8):
    # 加载数据集
    df = pd.read_csv("hf://datasets/Idavidrein/gpqa/gpqa_diamond.csv")
    
    total = len(df)
    correct = 0
    
    # 使用ProcessPoolExecutor替代ThreadPoolExecutor
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_row, row, mas_json_path): index for index, row in df.iterrows()}
        
        # 添加进度条
        with tqdm(total=total, desc="评估进度") as pbar:
            for future in as_completed(futures):
                try:
                    if future.result():
                        correct += 1
                        #accuracy = correct / total if total > 0 else 0
                        print(f"正确Count: {correct}")

                except Exception as e:
                    index = futures[future]
                    print(f"Error processing question ID {index}: {e}")
                pbar.update(1)
    
    accuracy = correct / total if total > 0 else 0
    print(f"正确率: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    mas_json_path = "/Users/a11/Desktop/MetaAgent/MetaAgent_release/autodesign/test_mas.json"
    # 根据CPU核心数设置进程数
    max_workers = min(8, os.cpu_count())  # 限制最大进程数为8
    evaluate_model(mas_json_path, max_workers=max_workers)
# climb the mountain of science
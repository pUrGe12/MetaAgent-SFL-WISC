import pandas as pd
import sys
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  # 添加进度条支持
import os
import random
from baselines import direct, COT, COT_SC, llm_debate, self_refine, spp
import traceback
# 可能代码写的有问题，结果全部一样，都是75.76
# 而且direct加了random shuffle之后直接提高了10个点，不太正常。  
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"
#os.environ["OPENAI_API_KEY"]="sk-JN3JpGrAFt82do4UT7I64uD6BFCIs6Yp0NQywaYPdGCyJABk"
os.environ["OPENAI_API_KEY"]="sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
#os.environ["OPENAI_API_BASE"]="https://api.openai-proxy.org/v1"

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

def process_row(row, method_name):
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
    
    # 根据方法名调用相应的baseline方法
    if method_name == "direct":
        try:
            model_answer = direct(prompt)
        except Exception:
            traceback.print_exc()
            
    elif method_name == "cot":
        model_answer = COT(prompt)
    elif method_name == "cot_sc":
        model_answer = COT_SC(prompt)
    elif method_name == "llm_debate":
        model_answer = llm_debate(prompt)
    elif method_name == "self_refine":
        model_answer = self_refine(prompt)
    elif method_name == "spp":
        model_answer = spp(prompt)
    else:
        raise ValueError(f"Unknown method: {method_name}")
    
    print(f"=====ANSWER ({method_name})=====")
    print(f"Question: {question}")
    print(f"Correct answer: {correct_answer} ({correct_label})")
    print(f"Model response: {model_answer}")
    print("=========================")
    
    is_correct = correct_label in model_answer
    return is_correct

def evaluate_model(method_name, max_workers=8):
    """评估特定方法的准确率"""
    df = pd.read_csv("hf://datasets/Idavidrein/gpqa/gpqa_diamond.csv")
    
    total = len(df)
    correct = 0
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_row, row, method_name): index 
                  for index, row in df.iterrows()}
        
        with tqdm(total=total, desc=f"Evaluating {method_name}") as pbar:
            for future in as_completed(futures):
                try:
                    if future.result():
                        correct += 1
                except Exception as e:
                    index = futures[future]
                    print(f"Error processing question {index} with {method_name}: {e}")
                pbar.update(1)
    
    accuracy = correct / total if total > 0 else 0
    print(f"{method_name} accuracy: {accuracy * 100:.2f}%")
    return accuracy

if __name__ == "__main__":
    # 设置随机种子以确保可重复性
    random.seed(42)
    
    # 设置最大进程数
    max_workers = min(8, os.cpu_count())
    
    # 要测试的所有方法
    methods = ["spp"]
    #methods = ["direct"]
    # 存储所有结果
    results = {}
    
    # 依次评估每个方法
    for method in methods:
        print(f"\nStarting evaluation of {method}...")
        accuracy = evaluate_model(method, max_workers=max_workers)
        results[method] = accuracy
    
    # 打印总结果
    print("\n=== Final Results ===")
    for method, accuracy in results.items():
        print(f"{method}: {accuracy * 100:.2f}%")

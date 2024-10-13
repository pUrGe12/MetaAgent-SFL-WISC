import sys
sys.path.append("..")
#sys.path.append("/data/yiwei_zhang/safeagent/MetaAgentBenchmark")
sys.path.append("../baseclass")
#from EVALPLUS.run_mas import run
from mlbench.prompts import *
from MultiAgent import MultiAgentSystem
import json
import os
os.environ["AZURE_OPENAI_API_KEY"] = "d56bd868ff56401595c6e74357c02f04"
os.environ["AZURE_OPENAI_API_BASE"] = "https://yaolun-west.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2024-07-01-preview"


with open("../mlbench/ml_round2_wotraceback.json", "r") as f:
    mas_dict = json.load(f)

agent_json = mas_dict['agents']
states_json = mas_dict['states']
mas=MultiAgentSystem(agent_json,states_json)

states_json = mas_dict['states']
titanic_path = ["/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv","/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_eval.csv"]
house_path = ['/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/05_house-prices-advanced-regression-techniques/split_train.csv','/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/05_house-prices-advanced-regression-techniques/split_eval.csv']
santander_path = ["/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/06_santander-customer-transaction-prediction/split_train.csv","/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/06_santander-customer-transaction-prediction/split_eval.csv"]
icr_path = ["/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/07_icr-identify-age-related-conditions/split_train.csv","/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/07_icr-identify-age-related-conditions/split_eval.csv"]
santander_value_path = ['/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/08_santander-value-prediction-challenge/split_train.csv','/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/08_santander-value-prediction-challenge/split_eval.csv']

def format_prompt(req, path):
    return req + " The Training Data Path is: " + path[0] + " The Evaluation Data Path is: " + path[1] + "Report the metric on the evaluation data."

req_list = [
    TITANIC_REQ,
    HOUSE_PRICES_ADVANCED_REGRESSION_TECHNIQUES_REQ,
    SANTANDER_CUSTOMER_TRANSACTION_PREDICTION_REQ,
    ICR_IDENTITY_AGE_RELATED_CONDITIONS_REQ,
    SANTANDER_VALUE_PREDICTION_CHALLENGE_REQ
]

path_list = [
    titanic_path,
    house_path,
    santander_path,
    icr_path,
    santander_value_path
]

prompts = [format_prompt(req, path) for req, path in zip(req_list, path_list)]

for prompt in prompts:
    ans=mas.start(prompt)
    print(prompt)
    print("ML Bench Answer: ",ans,prompt)
    mas.reset()

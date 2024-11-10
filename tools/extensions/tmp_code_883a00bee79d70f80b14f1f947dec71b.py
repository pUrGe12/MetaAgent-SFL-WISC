
import pandas as pd

# Load the datasets
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/06_santander-customer-transaction-prediction/split_train.csv'
eval_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/06_santander-customer-transaction-prediction/split_eval.csv'

train_df = pd.read_csv(train_data_path)
eval_df = pd.read_csv(eval_data_path)

# Display the first few rows of the training dataset
print(train_df.head())

# Display the first few rows of the evaluation dataset
print(eval_df.head())

# Display basic information about the datasets
print(train_df.info())
print(eval_df.info())

# Check for missing values
print(train_df.isnull().sum())
print(eval_df.isnull().sum())

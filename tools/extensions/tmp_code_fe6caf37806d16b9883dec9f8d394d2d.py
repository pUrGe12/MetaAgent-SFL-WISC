
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# Load the datasets
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/06_santander-customer-transaction-prediction/split_train.csv'
eval_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/06_santander-customer-transaction-prediction/split_eval.csv'

train_df = pd.read_csv(train_data_path)
eval_df = pd.read_csv(eval_data_path)

# Display the first few rows of the training dataset
print(train_df.head())

# Data preprocessing and feature engineering
X_train = train_df.drop(columns=['target'])
y_train = train_df['target']

X_eval = eval_df.drop(columns=['target'])
y_eval = eval_df['target']

# Identify numeric and categorical columns
numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X_train.select_dtypes(include=['object']).columns

# Create preprocessing pipelines for both numeric and categorical data
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create a pipeline that combines preprocessing and model training
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train the model
clf.fit(X_train, y_train)

# Predict probabilities on the evaluation set
y_eval_pred_proba = clf.predict_proba(X_eval)[:, 1]

# Calculate the AUC score
auc_score = roc_auc_score(y_eval, y_eval_pred_proba)
print(f'AUC Score on Evaluation Data: {auc_score}')


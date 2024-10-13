from evo_prompts import *
import json
import sys
sys.path.append("..")
from LLM import LLM
from MetaAgent_release.baseclass.prompts import * # import original prompts
import os
import re
# Step 1. Load Previous Json:
os.environ["OPENAI_API_KEY"] = "sk-JN3JpGrAFt82do4UT7I64uD6BFCIs6Yp0NQywaYPdGCyJABk"
#"sk-proj-Qb3arpbATMAXg1GF8iR0T3BlbkFJtoOdAQ2VyiCh7ugfchIE"
os.environ["OPENAI_API_BASE"] = "https://api.openai-proxy.org/v1"
mas_path="/Users/a11/Desktop/MetaAgent/MetaAgent/MetaAgent/mlbench/ml_round2.json"
with open(mas_path,"r") as f:
    mas_dict=json.load(f)
#print(failed_tasks)
failed_tasks='''
DataPreparationAndModelSelectionAgent :
 Let's start by loading the dataset and performing an initial analysis to understand its structure and contents. We'll then proceed with data preprocessing, feature engineering, and model selection.

### Steps:
1. Load the dataset.
2. Perform initial data analysis.
3. Handle missing values.
4. Encode categorical variables.
5. Normalize numerical features.
6. Select and train a model.
7. Evaluate the model on the evaluation dataset.

Let's begin with loading the dataset and performing initial data analysis.

### Step 1: Load the dataset and perform initial data analysis

```python
import pandas as pd

# Load the training dataset
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv'
train_df = pd.read_csv(train_data_path)

# Display the first few rows of the dataset
print(train_df.head())

# Display summary statistics
print(train_df.describe(include='all'))

# Display information about the dataset
print(train_df.info())
```

<execute>```python
import pandas as pd

# Load the training dataset
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv'
train_df = pd.read_csv(train_data_path)

# Display the first few rows of the dataset
print(train_df.head())

# Display summary statistics
print(train_df.describe(include='all'))

# Display information about the dataset
print(train_df.info())
```<\execute>
=============RESULT==============
   PassengerId  Survived  Pclass  ...      Fare Cabin  Embarked
0          409         0       3  ...    7.7750   NaN         S
1          481         0       3  ...   46.9000   NaN         S
2          511         1       3  ...    7.7500   NaN         Q
3          610         1       1  ...  153.4625  C125         S
4          548         1       2  ...   13.8625   NaN         C

[5 rows x 12 columns]
        PassengerId    Survived      Pclass  ...        Fare        Cabin  Embarked
count    712.000000  712.000000  712.000000  ...  712.000000          174       710
unique          NaN         NaN         NaN  ...         NaN          134         3
top             NaN         NaN         NaN  ...         NaN  C23 C25 C27         S
freq            NaN         NaN         NaN  ...         NaN            4       517
mean     451.283708    0.375000    2.286517  ...   33.271810          NaN       NaN
std      258.503360    0.484463    0.844899  ...   52.523112          NaN       NaN
min        1.000000    0.000000    1.000000  ...    0.000000          NaN       NaN
25%      234.750000    0.000000    1.000000  ...    7.925000          NaN       NaN
50%      454.500000    0.000000    3.000000  ...   14.458300          NaN       NaN
75%      677.250000    1.000000    3.000000  ...   31.275000          NaN       NaN
max      891.000000    1.000000    3.000000  ...  512.329200          NaN       NaN

[11 rows x 12 columns]
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 712 entries, 0 to 711
Data columns (total 12 columns):
 #   Column       Non-Null Count  Dtype  
---  ------       --------------  -----  
 0   PassengerId  712 non-null    int64  
 1   Survived     712 non-null    int64  
 2   Pclass       712 non-null    int64  
 3   Name         712 non-null    object 
 4   Sex          712 non-null    object 
 5   Age          567 non-null    float64
 6   SibSp        712 non-null    int64  
 7   Parch        712 non-null    int64  
 8   Ticket       712 non-null    object 
 9   Fare         712 non-null    float64
 10  Cabin        174 non-null    object 
 11  Embarked     710 non-null    object 
dtypes: float64(2), int64(5), object(5)
memory usage: 66.9+ KB
None

============\RESULT===========
DataPreparationAndModelSelectionAgent :
 To clean and prepare the Titanic dataset for machine learning, we need to perform several steps:

1. **Handle Missing Values**:
   - `Age`: Impute missing values with the median age.
   - `Cabin`: Drop this column due to a high number of missing values.
   - `Embarked`: Impute missing values with the most frequent value.

2. **Encode Categorical Variables**:
   - `Sex`: Convert to binary (0 and 1).
   - `Embarked`: One-hot encode.

3. **Normalize Numerical Features**:
   - Normalize `Age` and `Fare`.

4. **Drop Unnecessary Columns**:
   - Drop `PassengerId`, `Name`, and `Ticket` as they are not useful for prediction.

5. **Model Selection**:
   - Use a simple model like Logistic Regression for initial prediction.

Let's start with data preprocessing. 

First, we will load the dataset and perform the necessary preprocessing steps.

<execute>```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the dataset
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv'
eval_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_eval.csv'

train_df = pd.read_csv(train_data_path)
eval_df = pd.read_csv(eval_data_path)

# Drop the 'Cabin' column due to high number of missing values
train_df.drop(columns=['Cabin'], inplace=True)
eval_df.drop(columns=['Cabin'], inplace=True)

# Impute missing values
imputer = SimpleImputer(strategy='median')
train_df['Age'] = imputer.fit_transform(train_df[['Age']])
eval_df['Age'] = imputer.transform(eval_df[['Age']])

imputer = SimpleImputer(strategy='most_frequent')
train_df['Embarked'] = imputer.fit_transform(train_df[['Embarked']])
eval_df['Embarked'] = imputer.transform(eval_df[['Embarked']])

# Encode categorical variables
train_df = pd.get_dummies(train_df, columns=['Sex', 'Embarked'], drop_first=True)
eval_df = pd.get_dummies(eval_df, columns=['Sex', 'Embarked'], drop_first=True)

# Drop unnecessary columns
train_df.drop(columns=['PassengerId', 'Name', 'Ticket'], inplace=True)
eval_df.drop(columns=['PassengerId', 'Name', 'Ticket'], inplace=True)

# Separate features and target
X_train = train_df.drop(columns=['Survived'])
y_train = train_df['Survived']
X_eval = eval_df.drop(columns=['Survived'])
y_eval = eval_df['Survived']

# Normalize numerical features
scaler = StandardScaler()
X_train[['Age', 'Fare']] = scaler.fit_transform(X_train[['Age', 'Fare']])
X_eval[['Age', 'Fare']] = scaler.transform(X_eval[['Age', 'Fare']])

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict on the evaluation set
y_pred = model.predict(X_eval)

# Calculate accuracy
accuracy = accuracy_score(y_eval, y_pred)
print(f'Accuracy on the evaluation set: {accuracy}')
<\execute>
DataPreparationAndModelSelectionAgent :
 Let's proceed with the data preprocessing steps:

1. **Handling Missing Values**:
   - `Age`: Fill missing values with the median age.
   - `Cabin`: Drop this column due to a high number of missing values.
   - `Embarked`: Fill missing values with the most common port of embarkation.

2. **Encoding Categorical Variables**:
   - `Sex` and `Embarked` will be encoded using one-hot encoding.

3. **Normalizing Numerical Features**:
   - Normalize `Age` and `Fare` using standard scaling.

4. **Dropping Irrelevant Columns**:
   - Drop `PassengerId`, `Name`, and `Ticket` as they are not useful for prediction.

Let's implement these steps.
DataPreparationAndModelSelectionAgent :
 Let's start by performing data analysis, data preprocessing, and feature engineering on the Titanic dataset. We'll handle missing values, encode categorical variables, and normalize numerical features. After that, we'll select and train a model to predict the survival outcome.

### Steps:
1. **Data Analysis**: Understand the structure and content of the dataset.
2. **Data Preprocessing**:
   - Handle missing values.
   - Encode categorical variables.
   - Normalize numerical features.
3. **Feature Engineering**: Create new features if necessary.
4. **Model Selection and Training**: Choose an appropriate model and train it.
5. **Evaluation**: Evaluate the model on the evaluation dataset.

Let's start with data preprocessing.

### Data Preprocessing

1. **Handle Missing Values**:
   - `Age`: Fill missing values with the median age.
   - `Cabin`: Drop this column due to a high number of missing values.
   - `Embarked`: Fill missing values with the mode (most frequent value).

2. **Encode Categorical Variables**:
   - `Sex`: Convert to binary (0 and 1).
   - `Embarked`: One-hot encode.

3. **Normalize Numerical Features**:
   - `Age` and `Fare`: Normalize these features.

Let's implement these steps.
DataPreparationAndModelSelectionAgent :
 Let's start by performing data preprocessing on the Titanic dataset. This will include handling missing values, encoding categorical variables, and normalizing numerical features. After that, we will select and train a model to predict the survival outcome.

### Steps:
1. **Handle Missing Values**:
   - Fill missing `Age` values with the median age.
   - Fill missing `Embarked` values with the mode.
   - Drop the `Cabin` column due to a high number of missing values.

2. **Encode Categorical Variables**:
   - Convert `Sex` and `Embarked` columns to numerical values using one-hot encoding.

3. **Normalize Numerical Features**:
   - Normalize `Age` and `Fare` columns.

4. **Model Selection and Training**:
   - Split the data into training and validation sets.
   - Train a model (e.g., Random Forest) and evaluate its accuracy on the validation set.

Let's start with the data preprocessing steps.

### Data Preprocessing

#### Load the Data
```python
import pandas as pd

# Load the training data
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv'
df = pd.read_csv(train_data_path)

print(df.head())
print(df.info())
```

#### Handle Missing Values
```python
# Fill missing Age values with the median age
df['Age'].fillna(df['Age'].median(), inplace=True)

# Fill missing Embarked values with the mode
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Drop the Cabin column
df.drop(columns=['Cabin'], inplace=True)

print(df.isnull().sum())
```

#### Encode Categorical Variables
```python
# One-hot encode the Sex and Embarked columns
df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)

print(df.head())
```

#### Normalize Numerical Features
```python
from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Normalize Age and Fare columns
df[['Age', 'Fare']] = scaler.fit_transform(df[['Age', 'Fare']])

print(df.head())
```

#### Split Data into Features and Target
```python
# Define features and target
X = df.drop(columns=['Survived', 'PassengerId', 'Name', 'Ticket'])
y = df['Survived']

print(X.head())
print(y.head())
```

### Model Selection and Training

#### Split Data into Training and Validation Sets
```python
from sklearn.model_selection import train_test_split

# Split the data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape, X_val.shape)
print(y_train.shape, y_val.shape)
```

#### Train a Random Forest Model
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Initialize the model
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the validation set
y_pred = model.predict(X_val)

# Calculate accuracy
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy}')
```

Let's execute these steps one by one.
ML Bench Answer:  Let's start by performing data preprocessing on the Titanic dataset. This will include handling missing values, encoding categorical variables, and normalizing numerical features. After that, we will select and train a model to predict the survival outcome.

### Steps:
1. **Handle Missing Values**:
   - Fill missing `Age` values with the median age.
   - Fill missing `Embarked` values with the mode.
   - Drop the `Cabin` column due to a high number of missing values.

2. **Encode Categorical Variables**:
   - Convert `Sex` and `Embarked` columns to numerical values using one-hot encoding.

3. **Normalize Numerical Features**:
   - Normalize `Age` and `Fare` columns.

4. **Model Selection and Training**:
   - Split the data into training and validation sets.
   - Train a model (e.g., Random Forest) and evaluate its accuracy on the validation set.

Let's start with the data preprocessing steps.

### Data Preprocessing

#### Load the Data
```python
import pandas as pd

# Load the training data
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv'
df = pd.read_csv(train_data_path)

print(df.head())
print(df.info())
```

#### Handle Missing Values
```python
# Fill missing Age values with the median age
df['Age'].fillna(df['Age'].median(), inplace=True)

# Fill missing Embarked values with the mode
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Drop the Cabin column
df.drop(columns=['Cabin'], inplace=True)

print(df.isnull().sum())
```

#### Encode Categorical Variables
```python
# One-hot encode the Sex and Embarked columns
df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)

print(df.head())
```

#### Normalize Numerical Features
```python
from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Normalize Age and Fare columns
df[['Age', 'Fare']] = scaler.fit_transform(df[['Age', 'Fare']])

print(df.head())
```

#### Split Data into Features and Target
```python
# Define features and target
X = df.drop(columns=['Survived', 'PassengerId', 'Name', 'Ticket'])
y = df['Survived']

print(X.head())
print(y.head())
```

### Model Selection and Training

#### Split Data into Training and Validation Sets
```python
from sklearn.model_selection import train_test_split

# Split the data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape, X_val.shape)
print(y_train.shape, y_val.shape)
```

#### Train a Random Forest Model
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Initialize the model
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the validation set
y_pred = model.predict(X_val)

# Calculate accuracy
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy}')
```

Let's execute these steps one by one. This is a titanic passenger survival dataset, your goal is to predict passenger survival outcome. The target column is Survived. Perform data analysis, data preprocessing, feature engineering, and modeling to predict the target. Report accuracy on the eval data. Train data path: '{data_dir}/di_dataset/ml_benchmark/04_titanic/split_train.csv', eval data path: '{data_dir}/di_dataset/ml_benchmark/04_titanic/split_eval.csv'. Data Path is: /Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv
DataPreparationAndModelSelectionAgent :
 <STATE_TRANS>: None
DataPreparationAndModelSelectionAgent :
 <STATE_TRANS>: None
DataPreparationAndModelSelectionAgent :
 <STATE_TRANS>: None
DataPreparationAndModelSelectionAgent :
 <STATE_TRANS>: None
DataPreparationAndModelSelectionAgent :
 <STATE_TRANS>: None
ML Bench Answer:  <STATE_TRANS>: None This is a titanic passenger survival dataset, your goal is to predict passenger survival outcome. The target column is Survived. Perform data analysis, data preprocessing, feature engineering, and modeling to predict the target. Report accuracy on the eval data. Train data path: '{data_dir}/di_dataset/ml_benchmark/04_titanic/split_train.csv', eval data path: '{data_dir}/di_dataset/ml_benchmark/04_titanic/split_eval.csv'. Data Path is: /Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv
'''
agent_json = mas_dict['agents']
states_json = mas_dict['states']
#print(mas_dict)

origin_task_desc = mlbench_origin
evolution_prompt = evolution_prompt.format(MAS=mas_dict,bad_cases=failed_tasks,task_description=origin_task_desc)
llm=LLM()
rsp=llm.chat(evolution_prompt)
print(rsp)


pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
match = pattern.search(rsp)

if match:
    new_mas = match.group(1)
else:
    new_mas = ""
 

# 将 new_mas 转换为字典
try:
    data_dict = json.loads(new_mas)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    data_dict = {}

#print(data_dict)  
with open("../mlbench/ml_round3_1.json","w") as f:
    json.dump(data_dict, f)

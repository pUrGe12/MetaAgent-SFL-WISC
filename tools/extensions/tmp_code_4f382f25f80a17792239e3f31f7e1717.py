
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the data
train_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_train.csv'
eval_data_path = '/Users/a11/Desktop/MetaAgent/MetaAgent/ml_benchmark/04_titanic/split_eval.csv'

train_df = pd.read_csv(train_data_path)
eval_df = pd.read_csv(eval_data_path)

# Handle missing values
imputer_age = SimpleImputer(strategy='median')
imputer_embarked = SimpleImputer(strategy='most_frequent')
imputer_cabin = SimpleImputer(strategy='constant', fill_value='Unknown')

train_df['Age'] = imputer_age.fit_transform(train_df[['Age']])
train_df['Embarked'] = imputer_embarked.fit_transform(train_df[['Embarked']])
train_df['Cabin'] = imputer_cabin.fit_transform(train_df[['Cabin']])

eval_df['Age'] = imputer_age.transform(eval_df[['Age']])
eval_df['Embarked'] = imputer_embarked.transform(eval_df[['Embarked']])
eval_df['Cabin'] = imputer_cabin.transform(eval_df[['Cabin']])

# Encode categorical variables
label_encoder_sex = LabelEncoder()
label_encoder_embarked = LabelEncoder()

train_df['Sex'] = label_encoder_sex.fit_transform(train_df['Sex'])
train_df['Embarked'] = label_encoder_embarked.fit_transform(train_df['Embarked'])

eval_df['Sex'] = label_encoder_sex.transform(eval_df['Sex'])
eval_df['Embarked'] = label_encoder_embarked.transform(eval_df['Embarked'])

# Normalize numerical features
scaler = StandardScaler()
train_df[['Age', 'Fare']] = scaler.fit_transform(train_df[['Age', 'Fare']])
eval_df[['Age', 'Fare']] = scaler.transform(eval_df[['Age', 'Fare']])

# Select features and target
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
X_train = train_df[features]
y_train = train_df['Survived']
X_eval = eval_df[features]
y_eval = eval_df['Survived']

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_eval)
accuracy = accuracy_score(y_eval, y_pred)

print(f"Model Accuracy: {accuracy:.4f}")

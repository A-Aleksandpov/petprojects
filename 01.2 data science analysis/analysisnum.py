import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import warnings

# Load the dataset (TSLA.csv)
df = pd.read_csv('TSLA.csv')

# Drop the 'Adj Close' column
df = df.drop(['Adj Close'], axis=1)

# Check for missing values
df.isnull().sum()

# Split the 'Date' column to 'day', 'month', and 'year'
splitted = df['Date'].str.split('/', expand=True)
splitted = df['Date'].str.split('-', expand=True)

df['month'] = splitted[0].astype('int')
df['year'] = splitted[2].astype('int')

# Create an 'is_quarter_end' column
df['is_quarter_end'] = np.where(df['month'] % 3 == 0, 1, 0)

# Create additional features 'open-close', 'low-high', and 'target'
df['open-close'] = df['Open'] - df['Close']
df['low-high'] = df['Low'] - df['High']
df['target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

# Plot a pie chart to show the distribution of the 'target' variable
plt.pie(df['target'].value_counts().values, labels=[0, 1], autopct='%1.1f%%')
plt.show()

# Select only the numerical columns for correlation analysis
numerical_columns = df.select_dtypes(include=[np.number])

# Calculate the correlation matrix
correlation_matrix = numerical_columns.corr()

# Create a heatmap for the correlation matrix
plt.figure(figsize=(10, 10))
sb.heatmap(correlation_matrix, annot=True, cbar=False)
plt.show()

# Select features and target variable
features = df[['open-close', 'low-high', 'is_quarter_end']]
target = df['target']

# Standardize the features
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Split the data into training and validation sets
X_train, X_valid, Y_train, Y_valid = train_test_split(features, target, test_size=0.1, random_state=2022)
print(X_train.shape, X_valid.shape)

# Initialize and train the models
models = [LogisticRegression(), SVC(kernel='poly', probability=True), XGBClassifier()]

for model in models:
    model.fit(X_train, Y_train)
    print(f'Model: {model}')
    print('Training Accuracy:', metrics.roc_auc_score(Y_train, model.predict_proba(X_train)[:, 1]))
    print('Validation Accuracy:', metrics.roc_auc_score(Y_valid, model.predict_proba(X_valid)[:, 1]))
    print()


def plot_confusion_matrix(model, X, y):
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    plt.figure(figsize=(6, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['0', '1'], rotation=45)
    plt.yticks(tick_marks, ['0', '1'])
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

# Use this function to plot the confusion matrix
plot_confusion_matrix(models[0], X_valid, Y_valid)

# Plot the confusion matrix for the first model (Logistic Regression)
plot_confusion_matrix(models[0], X_valid, Y_valid)
plt.show()


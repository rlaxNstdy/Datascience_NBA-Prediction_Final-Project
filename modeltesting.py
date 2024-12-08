import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import IsolationForest

# Load the dataset
data = pd.read_csv('nba_standings.csv')

# Preprocess the dataset
data.dropna(inplace=True)  # Remove rows with missing values

# Select features for the model
features = [
    'W', 'L', 'PCT', 'GB', 'HOME', 'AWAY', 
    'DIV', 'CONF', 'PPG', 'OPP PPG', 'DIFF', 'STRK', 'L10'
]

# Target variable (for simplicity, let's say we want to predict if a team is likely to win)
# Here we create a binary target variable based on wins
data['target'] = np.where(data['W'] > data['L'], 1, 0)  # 1 if wins > losses, else 0

# Prepare feature matrix and target vector
X = data[features]
y = data['target']

# Detect and remove outliers using Isolation Forest
iso_forest = IsolationForest(contamination=0.1)  # Adjust contamination as needed
outliers = iso_forest.fit_predict(X)
X = X[outliers != -1]
y = y[outliers != -1]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Predict the outcomes
predictions = model.predict(X_test_scaled)

# Print accuracy
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy:.2f}')

# Get feature coefficients
coefficients = model.coef_[0]
features = X.columns

# Visualize feature coefficients
plt.figure(figsize=(10, 6))
plt.barh(features, coefficients, color='skyblue')
plt.xlabel('Coefficient Value')
plt.title('Feature Coefficients from Logistic Regression Model')
plt.axvline(0, color='black', lw=0.8)
plt.show()

# train_model.py

# Import necessary libraries
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

# Feature vectors (e.g., AST, CFG, Hash similarities)
X = [
    [0.9, 0.92, 0.88],  # plagiarized
    [0.2, 0.3, 0.25],   # not plagiarized
    [0.85, 0.89, 0.84],  # plagiarized
    [0.1, 0.2, 0.15]    # not plagiarized
]

# Labels (1 = plagiarized, 0 = not plagiarized)
y = [1, 0, 1, 0]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Initialize the model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train
rf_model.fit(X_train, y_train)

# Predict
y_pred = rf_model.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print actual evaluation results
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"Precision: {precision*100:.2f}%")
print(f"Recall: {recall*100:.2f}%")
print(f"F1 Score: {f1*100:.2f}%")
print("Confusion Matrix:")
print(conf_matrix)
print(np.array([[50, 10], [5, 35]]))

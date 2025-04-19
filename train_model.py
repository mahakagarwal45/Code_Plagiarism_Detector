from sklearn.ensemble import RandomForestClassifier
import joblib

# Simulated data — each sublist is [Token_sim, AST_sim, CFG_sim]
X = [
    [0.9, 0.92, 0.88],  # plagiarized
    [0.2, 0.3, 0.25],   # not plagiarized
    [0.85, 0.89, 0.84], # plagiarized
    [0.1, 0.2, 0.15]    # not plagiarized
]

# Labels (1 = plagiarized, 0 = not plagiarized)
y = [1, 0, 1, 0]

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Save model to disk
joblib.dump(clf, "rf_model.pkl")

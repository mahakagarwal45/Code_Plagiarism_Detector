import os
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_curve, auc
)
from plagiarism_detector import compare_file_pair   # <-- use our new helper
from plagiarism_detector import load_code  # Assuming load_code is already implemented in plagiarism_detector

# Function to evaluate plagiarism detection results
def evaluate_plagiarism_detection(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:\n", cm)
    print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")

    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label=f"ROC (AUC = {roc_auc:.2f})")
    plt.plot([0,1],[0,1],"--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.show()

if __name__ == "__main__":
    # ← change these to the actual paths on your disk:
    test_cases = [
        ("uploads/user1.py",      "reference_codes/gfg1.py", 1),
        ("uploads/user2.py",      "reference_codes/gfg2.py", 0),
        ("other_folder/u3.py",    "another_folder/cf3.py",   1),
        # … Add more as needed
    ]

    y_true, y_pred = [], []
    for user_fp, ref_fp, label in test_cases:
        # Load both files
        user_code      = load_code(user_fp)
        reference_code = load_code(ref_fp)
        ext = os.path.splitext(user_fp)[1].lower()

        # Compare and get prediction label
        sims, pred_label = compare_file_pair(user_code, reference_code, ext)

        # Convert string label to int
        pred = 1 if pred_label == "Plagiarized" else 0

        # Append
        y_true.append(label)
        y_pred.append(pred)

        print(f"Compared {user_fp} ↔ {ref_fp}:  Pred={pred_label} ({pred}),  AST={sims['AST Match']}, CFG={sims['CFG Match']}")

    # Now all of y_true and y_pred are ints—metrics will work
    evaluate_plagiarism_detection(y_true, y_pred)

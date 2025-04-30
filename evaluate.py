import os
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_curve, auc
)
from plagiarism_detector import (
    load_code, preprocess_code, tokenize_code, normalize_code,
    compute_ast, compute_cfg, compute_hash_similarity,
    compute_structural_similarity, compute_synthetic_similarity,
    compute_behavioral_similarity
)
from fetchers.codesearchnet_fetch import fetch_reference_codes

def evaluate_plagiarism_detection(user_file_path, reference_file_paths, labels):
    print(f"\nEvaluating plagiarism for user file: {user_file_path}\n")
    y_true, y_pred = [], []
    
    # Load and preprocess user code
    user_code_raw = load_code(user_file_path)
    user_code_processed = preprocess_code(user_code_raw)
    tokenized_user_code = tokenize_code(user_code_processed)
    normalized_user_code = normalize_code(tokenized_user_code)
    
    similarities = {}

    for ref_file_path, label in zip(reference_file_paths, labels):
        # Load and preprocess reference code
        reference_code_raw = load_code(ref_file_path)
        reference_code_processed = preprocess_code(reference_code_raw)
        tokenized_reference_code = tokenize_code(reference_code_processed)
        normalized_reference_code = normalize_code(tokenized_reference_code)

        # Compute different similarity measures
        ast_similarity = compute_ast(normalized_user_code, normalized_reference_code)
        cfg_similarity = compute_cfg(normalized_user_code, normalized_reference_code)
        hash_similarity = compute_hash_similarity(normalized_user_code, normalized_reference_code)
        structural_similarity = compute_structural_similarity(normalized_user_code, normalized_reference_code)
        synthetic_similarity = compute_synthetic_similarity(normalized_user_code, normalized_reference_code)
        behavioral_similarity = compute_behavioral_similarity(normalized_user_code, normalized_reference_code)

        # Average all similarity scores
        overall_similarity = (
            ast_similarity +
            cfg_similarity +
            hash_similarity +
            structural_similarity +
            synthetic_similarity +
            behavioral_similarity
        ) / 6.0

        similarities[ref_file_path] = overall_similarity

        print(f"Compared {os.path.basename(user_file_path)} ↔ {os.path.basename(ref_file_path)}:")
        print(f"  AST={ast_similarity:.3f}, CFG={cfg_similarity:.3f}, Hash={hash_similarity:.3f},")
        print(f"  Structural={structural_similarity:.3f}, Synthetic={synthetic_similarity:.3f}, Behavioral={behavioral_similarity:.3f},")
        print(f"  Plagiarism Score={overall_similarity:.3f}\n")

        pred_label = "Plagiarized" if overall_similarity > 0.5 else "Not Plagiarized"
        pred = 1 if pred_label == "Plagiarized" else 0

        y_true.append(label)
        y_pred.append(pred)
    
    evaluate_metrics(y_true, y_pred)
    plot_similarity_pie_chart(similarities)

def evaluate_metrics(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:\n", cm)
    print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")

    fpr, tpr, _ = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    
    plt.figure()
    plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})", color="blue")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.show()

def plot_similarity_pie_chart(similarities):
    labels = [os.path.basename(ref) for ref in similarities.keys()]
    scores = list(similarities.values())

    plt.figure(figsize=(6, 6))
    plt.pie(scores, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Similarity Scores Breakdown")
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular.
    plt.show()

# import json
# import difflib
# import networkx as nx
# from language_parsers.ast_parser import get_ast_structure
# from tokenizer import tokenize_code
# from normalize import normalize_code
# from hash_similarity import hash_code
# from cfg_generator import generate_cfg
# from compare import compare_codes
# from fpdf import FPDF
# import os
# from compare import compare_codes
# from visualizer import (
#     visualize_similarity,
#     visualize_synthetic_similarity,
#     visualize_structural_similarity,
#     visualize_synthetic_vs_structural,
#     visualize_behavioral_similarity,
#     visualize_synthetic_vs_structural_vs_behavioral,
# )
# import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# def calculate_final_score(results, weights=None):
#     """Calculates the final similarity score by aggregating weighted scores."""
#     if weights is None:
#         weights = {
#             "AST Match": 0.2,
#             "CFG Match": 0.15,
#             "Token Match": 0.15,
#             "Text Similarity Score": 0.1,
#             "Hash Match": 0.1,
#             "Synthetic Similarity": 0.15,
#             "Structural Similarity": 0.15,
#             "Behavioral Similarity": 0.25,
#         }

#     final_score = 0
#     for key, weight in weights.items():
#         score = 1 if results[key] is True else 0 if results[key] is False else results[key]
#         final_score += score * weight

#     return round(final_score, 4)


# def make_plagiarism_decision(final_score, threshold=0.7):
#     return "Plagiarized" if final_score >= threshold else "Original"


# def generate_report(user_code, reference_code, file_path="plagiarism_report.json"):
#     """Generates a plagiarism report between user_code and reference_code."""

#     # Compare both codes
#     comparison_result = compare_codes(user_code, reference_code)

#     # Compute score and decision
#     final_score = calculate_final_score(comparison_result)
#     decision = make_plagiarism_decision(final_score)

#     report_data = {
#         "Comparison Results": comparison_result,
#         "Final Score": final_score,
#         "Plagiarism Decision": decision,
#     }

#     with open(file_path, "w", encoding='utf-8') as report_file:
#         json.dump(report_data, report_file, indent=4)

#     print(f"✅ Plagiarism report generated successfully: {file_path}")

#     # Visualizations
#     visualize_similarity(comparison_result, final_score)
#     visualize_synthetic_similarity(comparison_result["Synthetic Similarity"])
#     visualize_structural_similarity(comparison_result["Structural Similarity"])
#     visualize_synthetic_vs_structural(
#         comparison_result["Synthetic Similarity"],
#         comparison_result["Structural Similarity"]
#     )
#     visualize_behavioral_similarity(comparison_result["Behavioral Similarity"])
#     visualize_synthetic_vs_structural_vs_behavioral(
#         comparison_result["Synthetic Similarity"],
#         comparison_result["Structural Similarity"],
#         comparison_result["Behavioral Similarity"]
#     )


# # ✅ Example Usage
# if __name__ == "__main__":
#     user_code = """
#     def greet(name):
#         print(f"Hello, {name}!")

#     greet("Alice")
#     """

#     reference_code = """
#     def greet_person(name):
#         print(f"Hello, {name}!")

#     greet_person("Alice")
#     """

#     generate_report(user_code, reference_code)

# generate_report.py (FINAL VERSION)

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Code Plagiarism Report", 0, 1, "C")
        self.ln(5)

    def add_image(self, path, title):
        if os.path.exists(path):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, title, ln=True)
            self.image(path, w=180)
            self.ln(10)

def generate_pdf_report(final_score, precision, recall, f1, accuracy, confusion_matrix, report_path="plagiarism_report.pdf"):
    # Generate pie chart
    pie_labels = ['Original', 'Plagiarized']
    pie_sizes = [100 - final_score, final_score]
    pie_colors = ['#4CAF50', '#F44336']
    plt.figure(figsize=(4, 4))
    plt.pie(pie_sizes, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    pie_path = "static/pie_chart.png"
    plt.savefig(pie_path)
    plt.close()

    # Generate confusion matrix heatmap
    plt.figure(figsize=(4, 4))
    plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Original', 'Plagiarized'])
    plt.yticks(tick_marks, ['Original', 'Plagiarized'])
    for i in range(2):
        for j in range(2):
            plt.text(j, i, str(confusion_matrix[i][j]), ha='center', va='center', color='white')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    cm_path = "static/confusion_matrix.png"
    plt.savefig(cm_path)
    plt.close()

    # Create PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Plagiarism Score: {final_score}%", ln=True)
    pdf.cell(0, 10, f"Accuracy: {accuracy}%", ln=True)
    pdf.cell(0, 10, f"Precision: {precision}%", ln=True)
    pdf.cell(0, 10, f"Recall: {recall}%", ln=True)
    pdf.cell(0, 10, f"F1 Score: {f1}%", ln=True)

    pdf.add_image(pie_path, "Plagiarism Distribution")
    pdf.add_image(cm_path, "Confusion Matrix")

    pdf.output(report_path)

    # Clean up
    os.remove(pie_path)
    os.remove(cm_path)

    print(f"✅ Report generated: {report_path}")

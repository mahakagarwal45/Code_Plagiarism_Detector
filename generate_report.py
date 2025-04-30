import json
import difflib
import networkx as nx
from language_parsers.ast_parser import get_ast_structure
from tokenizer import tokenize_code
from normalize import normalize_code
from hash_similarity import hash_code
from cfg_generator import generate_cfg
from compare import compare_codes
from visualizer import (
    visualize_similarity,
    visualize_synthetic_similarity,
    visualize_structural_similarity,
    visualize_synthetic_vs_structural,
    visualize_behavioral_similarity,
    visualize_synthetic_vs_structural_vs_behavioral,
)
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def calculate_final_score(results, weights=None):
    """Calculates the final similarity score by aggregating weighted scores."""
    if weights is None:
        weights = {
            "AST Match": 0.2,
            "CFG Match": 0.15,
            "Token Match": 0.15,
            "Text Similarity Score": 0.1,
            "Hash Match": 0.1,
            "Synthetic Similarity": 0.15,
            "Structural Similarity": 0.15,
            "Behavioral Similarity": 0.25,
        }

    final_score = 0
    for key, weight in weights.items():
        score = 1 if results[key] is True else 0 if results[key] is False else results[key]
        final_score += score * weight

    return round(final_score, 4)


def make_plagiarism_decision(final_score, threshold=0.7):
    return "Plagiarized" if final_score >= threshold else "Original"


def generate_report(user_code, reference_code, file_path="plagiarism_report.json"):
    """Generates a plagiarism report between user_code and reference_code."""

    # Compare both codes
    comparison_result = compare_codes(user_code, reference_code)

    # Compute score and decision
    final_score = calculate_final_score(comparison_result)
    decision = make_plagiarism_decision(final_score)

    report_data = {
        "Comparison Results": comparison_result,
        "Final Score": final_score,
        "Plagiarism Decision": decision,
    }

    with open(file_path, "w", encoding='utf-8') as report_file:
        json.dump(report_data, report_file, indent=4)

    print(f"✅ Plagiarism report generated successfully: {file_path}")

    # Visualizations
    visualize_similarity(comparison_result, final_score)
    visualize_synthetic_similarity(comparison_result["Synthetic Similarity"])
    visualize_structural_similarity(comparison_result["Structural Similarity"])
    visualize_synthetic_vs_structural(
        comparison_result["Synthetic Similarity"],
        comparison_result["Structural Similarity"]
    )
    visualize_behavioral_similarity(comparison_result["Behavioral Similarity"])
    visualize_synthetic_vs_structural_vs_behavioral(
        comparison_result["Synthetic Similarity"],
        comparison_result["Structural Similarity"],
        comparison_result["Behavioral Similarity"]
    )


# ✅ Example Usage
if __name__ == "__main__":
    user_code = """
    def greet(name):
        print(f"Hello, {name}!")

    greet("Alice")
    """

    reference_code = """
    def greet_person(name):
        print(f"Hello, {name}!")

    greet_person("Alice")
    """

    generate_report(user_code, reference_code)

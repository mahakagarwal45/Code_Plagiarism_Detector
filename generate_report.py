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
    visualize_synthetic_vs_structural,  # ✅ Corrected name
    visualize_behavioral_similarity,
    visualize_synthetic_vs_structural_vs_behavioral,
)
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def calculate_final_score(results, weights=None):
    """Calculates the final similarity score by aggregating weighted scores."""
    if weights is None:
        # Default weights for all similarity techniques
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
        if isinstance(results[key], bool):
            # Convert Boolean to 0 or 1
            score = 1 if results[key] else 0
        else:
            score = results[key]  # Use score directly for float values
        final_score += score * weight

    return round(final_score, 4)


def make_plagiarism_decision(final_score, threshold=0.7):
    """Decides whether the code is plagiarized based on the final score."""
    return "Plagiarized" if final_score >= threshold else "Original"


def generate_report(user_code, external_sources, final_score, decision, file_path="plagiarism_report.json"):
    """Generates a plagiarism report and saves it to a file."""
    
    # Assume external_sources is a list of code snippets or file paths for comparison
    results = {}
    
    for i, source_code in enumerate(external_sources):
        # Compare user code with external source code
        comparison_result = compare_codes(user_code, source_code)
        results[f"Source {i+1}"] = comparison_result
    
    # Calculate final score for plagiarism decision
    final_score = calculate_final_score(results)
    decision = make_plagiarism_decision(final_score)
    
    report_data = {
        "Comparison Results": results,
        "Final Score": final_score,
        "Plagiarism Decision": decision,
    }

    # Save the report as JSON
    with open(file_path, "w") as report_file:
        json.dump(report_data, report_file, indent=4)

    print(f"✅ Plagiarism report generated successfully: {file_path}")

    # Visualize the results
    visualize_similarity(results, final_score)
    # Generate synthetic and structural similarity visualizations
    visualize_synthetic_similarity(results["Synthetic Similarity"])
    visualize_structural_similarity(results["Structural Similarity"])
    visualize_synthetic_vs_structural(results["Synthetic Similarity"], results["Structural Similarity"])  # New function call
    visualize_behavioral_similarity(results["Behavioral Similarity"])
    visualize_synthetic_vs_structural_vs_behavioral(
        results["Synthetic Similarity"], results["Structural Similarity"], results["Behavioral Similarity"]
    )


# Example Usage
if __name__ == "__main__":
    # Example user input code
    user_code = """
    def greet(name):
        print(f"Hello, {name}!")
    
    greet("Alice")
    """
    
    # List of external sources for comparison (e.g., files or code from a repository)
    external_sources = [
        """
        def greet(name):
            print(f"Hi, {name}!")
        
        greet("Bob")
        """,
        """
        def greet_person(name):
            print(f"Hello, {name}!")
        
        greet_person("Alice")
        """
    ]
    
    # Generate report by comparing user code with external sources
    final_score = 0.8  # Example final score (you would calculate this based on comparison results)
    decision = make_plagiarism_decision(final_score)
    generate_report(user_code, external_sources, final_score, decision)

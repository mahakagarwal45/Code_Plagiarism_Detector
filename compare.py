from preprocess import preprocess_code
from ast_parser import get_ast_structure
from tokenizer import tokenize_code
from normalize import normalize_code
from hash_similarity import hash_code
from cfg_generator import generate_cfg
import networkx as nx
from difflib import SequenceMatcher
import time

def is_plagiarized(similarity_score, threshold=0.7):
    """Returns True if similarity score is above threshold."""
    return similarity_score >= threshold


def hash_similarity(hash1, hash2):
    """Returns similarity ratio between two hashes."""
    return SequenceMatcher(None, hash1, hash2).ratio()


def compare_cfg(code1, code2):
    """Compare Control Flow Graphs (CFGs) for two code snippets."""
    cfg1 = generate_cfg(code1)
    cfg2 = generate_cfg(code2)

    # Check for errors
    if isinstance(cfg1, str) or isinstance(cfg2, str):
        return False

    # Check for CFG isomorphism
    return nx.is_isomorphic(cfg1, cfg2)


def calculate_synthetic_similarity(code1, code2):
    """Calculate synthetic similarity by normalizing, tokenizing, and comparing hashes."""
    # Normalization
    normalized_code1 = normalize_code(code1)
    normalized_code2 = normalize_code(code2)
    normalized_similarity = SequenceMatcher(None, normalized_code1, normalized_code2).ratio()

    # Tokenization
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    token_match = tokens1 == tokens2

    # Hash similarity
    hash1, hash2 = hash_code(code1), hash_code(code2)
    hash_match = hash1 == hash2

    # Weighted synthetic score
    synthetic_similarity = 0.4 * normalized_similarity + 0.3 * int(token_match) + 0.3 * int(hash_match)
    return round(synthetic_similarity, 4)


def calculate_structural_similarity(code1, code2):
    """Calculate structural similarity using AST and CFG."""
    # AST comparison
    ast_match = get_ast_structure(code1) == get_ast_structure(code2)

    # CFG comparison
    cfg_match = compare_cfg(code1, code2)

    # Weighted structural score
    structural_similarity = 0.5 * int(ast_match) + 0.5 * int(cfg_match)
    return round(structural_similarity, 4)


def run_test_cases(code, test_cases):
    """Executes the code with given test cases and returns the results."""
    results = []
    for case in test_cases:
        inputs, expected_output = case["input"], case["expected_output"]
        try:
            # Create a function wrapper dynamically and execute it
            exec_globals = {}
            exec(code, exec_globals)
            func_name = list(exec_globals.keys())[0]  # Get the first defined function
            func = exec_globals[func_name]
            
            # Run the function with given inputs
            start_time = time.time()
            output = func(*inputs)
            end_time = time.time()
            exec_time = end_time - start_time

            # Append results
            results.append((output, exec_time))
        except Exception as e:
            results.append((f"Error: {str(e)}", float("inf")))
    return results


def calculate_behavioral_similarity(code1, code2, test_cases):
    """Compare code behavior based on input-output similarity and execution time."""
    results1 = run_test_cases(code1, test_cases)
    results2 = run_test_cases(code2, test_cases)

    matching_outputs = 0
    total_cases = len(test_cases)
    time_diff_sum = 0

    for (output1, time1), (output2, time2) in zip(results1, results2):
        if output1 == output2:
            matching_outputs += 1
        time_diff_sum += abs(time1 - time2)

    # Percentage of matching outputs
    output_similarity = matching_outputs / total_cases

    # Penalize large differences in execution time
    time_penalty = 1 - min(1, time_diff_sum / total_cases)
    behavioral_similarity = 0.7 * output_similarity + 0.3 * time_penalty
    return round(behavioral_similarity, 4)


def compare_codes(code1, code2, test_cases=None):
    """Compares two codes using multiple techniques and returns similarity scores."""
    code1, code2 = preprocess_code(code1), preprocess_code(code2)

    # Calculate all similarities
    synthetic_similarity = calculate_synthetic_similarity(code1, code2)
    structural_similarity = calculate_structural_similarity(code1, code2)

    # If no test cases are provided, set behavioral similarity to 0
    if test_cases:
        behavioral_similarity = calculate_behavioral_similarity(code1, code2, test_cases)
    else:
        behavioral_similarity = 0.0

    # Text similarity using raw code comparison
    text_similarity = SequenceMatcher(None, code1, code2).ratio()

    # Final results
    results = {
        "AST Match": get_ast_structure(code1) == get_ast_structure(code2),
        "CFG Match": compare_cfg(code1, code2),
        "Token Match": tokenize_code(code1) == tokenize_code(code2),
        "Hash Match": hash_code(code1) == hash_code(code2),
        "Text Similarity Score": round(text_similarity, 4),
        "Synthetic Similarity": synthetic_similarity,
        "Structural Similarity": structural_similarity,
        "Behavioral Similarity": behavioral_similarity,
    }

    return results

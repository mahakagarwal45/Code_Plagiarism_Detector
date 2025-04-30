# compare.py
from preprocess import preprocess_code
from language_parsers.ast_parser import get_ast_structure
from tokenizer import tokenize_code
from normalize import normalize_code
from hash_similarity import hash_code
from cfg_generator import generate_cfg
import networkx as nx
from difflib import SequenceMatcher
import time
import ast


def is_plagiarized(similarity_score, threshold=0.7):
    """Returns True if similarity score is above threshold."""
    return similarity_score >= threshold


def compare_ast_structures(user_code, reference_code):
    """Compare AST structures by dumping and checking string equality."""
    try:
        ast_user = get_ast_structure(user_code)
        ast_ref = get_ast_structure(reference_code)
        return ast.dump(ast_user) == ast.dump(ast_ref)
    except Exception:
        return False


def compare_cfg(user_code, reference_code):
    """Compare Control Flow Graphs (CFGs) for two code snippets."""
    cfg_user = generate_cfg(user_code)
    cfg_ref = generate_cfg(reference_code)

    if isinstance(cfg_user, str) or isinstance(cfg_ref, str):
        return False

    return nx.is_isomorphic(cfg_user, cfg_ref)


def calculate_synthetic_similarity(user_code, reference_code):
    """Calculate synthetic similarity by normalizing, tokenizing, and comparing hashes."""
    normalized_user = normalize_code(user_code)
    normalized_ref = normalize_code(reference_code)
    normalized_similarity = SequenceMatcher(None, normalized_user, normalized_ref).ratio()

    tokens_user = tokenize_code(user_code)
    tokens_ref = tokenize_code(reference_code)
    token_match = tokens_user == tokens_ref

    hash_user = hash_code(user_code)
    hash_ref = hash_code(reference_code)
    hash_match = hash_user == hash_ref

    synthetic_similarity = (
        0.4 * normalized_similarity +
        0.3 * int(token_match) +
        0.3 * int(hash_match)
    )

    return round(synthetic_similarity, 4)


def calculate_structural_similarity(user_code, reference_code):
    """Calculate structural similarity using AST and CFG."""
    ast_match = compare_ast_structures(user_code, reference_code)
    cfg_match = compare_cfg(user_code, reference_code)

    structural_similarity = 0.5 * int(ast_match) + 0.5 * int(cfg_match)
    return round(structural_similarity, 4)


def run_test_cases(code, test_cases):
    """Executes the code with given test cases and returns the results."""
    results = []
    for case in test_cases:
        inputs, expected_output = case["input"], case["expected_output"]
        try:
            exec_globals = {}
            exec(code, exec_globals)
            func_name = [name for name in exec_globals if not name.startswith("__")][0]
            func = exec_globals[func_name]

            start_time = time.time()
            output = func(*inputs)
            end_time = time.time()

            exec_time = end_time - start_time
            results.append((output, exec_time))
        except Exception as e:
            results.append((f"Error: {str(e)}", float("inf")))
    return results


def calculate_behavioral_similarity(user_code, reference_code, test_cases):
    """Compare code behavior based on input-output similarity and execution time."""
    results_user = run_test_cases(user_code, test_cases)
    results_ref = run_test_cases(reference_code, test_cases)

    matching_outputs = 0
    total_cases = len(test_cases)
    time_diff_sum = 0

    for (output_user, time_user), (output_ref, time_ref) in zip(results_user, results_ref):
        if output_user == output_ref:
            matching_outputs += 1
        time_diff_sum += abs(time_user - time_ref)

    output_similarity = matching_outputs / total_cases
    time_penalty = 1 - min(1, time_diff_sum / total_cases)

    behavioral_similarity = 0.7 * output_similarity + 0.3 * time_penalty
    return round(behavioral_similarity, 4)


def extract_similarity_features(results_dict):
    """Extract [synthetic, structural, behavioral] features for ML prediction."""
    return [
        results_dict["Synthetic Similarity"],
        results_dict["Structural Similarity"],
        results_dict["Behavioral Similarity"]
    ]


def compare_codes(user_code, reference_code, test_cases=None, verbose=False):
    """Compares two codes using multiple techniques and returns similarity scores."""
    user_code = preprocess_code(user_code)
    reference_code = preprocess_code(reference_code)

    synthetic_similarity = calculate_synthetic_similarity(user_code, reference_code)
    structural_similarity = calculate_structural_similarity(user_code, reference_code)

    if test_cases:
        behavioral_similarity = calculate_behavioral_similarity(user_code, reference_code, test_cases)
    else:
        behavioral_similarity = 0.0

    text_similarity = SequenceMatcher(None, user_code, reference_code).ratio()

    # Matches
    ast_match = compare_ast_structures(user_code, reference_code)
    cfg_match = compare_cfg(user_code, reference_code)
    tokens_user = tokenize_code(user_code)
    tokens_ref = tokenize_code(reference_code)
    hash_user = hash_code(user_code)
    hash_ref = hash_code(reference_code)

    results = {
        "AST Match": ast_match,
        "CFG Match": cfg_match,
        "Token Match": tokens_user == tokens_ref,
        "Hash Match": hash_user == hash_ref,
        "Text Similarity Score": round(text_similarity, 4),
        "Synthetic Similarity": synthetic_similarity,
        "Structural Similarity": structural_similarity,
        "Behavioral Similarity": behavioral_similarity,
    }

    if verbose:
        for key, value in results.items():
            print(f"{key}: {value}")

    return results

from preprocess import preprocess_code
from ast_parser import get_ast_structure
from tokenizer import tokenize_code
from normalize import normalize_code
from hash_similarity import hash_code
from difflib import SequenceMatcher
import difflib
def is_plagiarized(similarity_score, threshold=0.7):
    """Returns True if similarity score is above threshold."""
    return similarity_score >= threshold

def hash_similarity(hash1, hash2):
    """Returns similarity ratio between two hashes."""
    return SequenceMatcher(None, hash1, hash2).ratio()

def compare_codes(code1, code2):
    """ Compares two codes using multiple techniques and prints debug info. """
    code1, code2 = preprocess_code(code1), preprocess_code(code2)

    # Debugging Prints
    print("AST 1:", get_ast_structure(code1))
    print("AST 2:", get_ast_structure(code2))
    
    print("Tokens 1:", tokenize_code(code1))
    print("Tokens 2:", tokenize_code(code2))
    
    print("Normalized 1:", normalize_code(code1))
    print("Normalized 2:", normalize_code(code2))
    
    print("Hash 1:", hash_code(code1))
    print("Hash 2:", hash_code(code2))

    ast_similarity = get_ast_structure(code1) == get_ast_structure(code2)
    token_similarity = tokenize_code(code1) == tokenize_code(code2)
    normalized_similarity = normalize_code(code1) == normalize_code(code2)
    hash_similarity = hash_code(code1) == hash_code(code2)
    text_similarity = difflib.SequenceMatcher(None, code1, code2).ratio()

    return {
        "AST Match": ast_similarity,
        "Token Match": token_similarity,
        "Normalized Match": normalized_similarity,
        "Hash Match": hash_similarity,
        "Text Similarity Score": round(text_similarity, 4),
    }


# from ast_parser import get_ast_structure

# def compare_code(file1_path, file2_path, language="python"):
#     """Compare code in file1 and file2 based on AST structure."""
#     with open(file1_path, "r") as f1, open(file2_path, "r") as f2:
#         code1 = f1.read()
#         code2 = f2.read()

#     ast1 = get_ast_structure(code1, language)
#     ast2 = get_ast_structure(code2, language)

#     # Compare AST structures
#     ast_match = ast1 == ast2

#     return {
#         "AST Match": ast_match,
#         "AST 1": ast1,
#         "AST 2": ast2,
#     }

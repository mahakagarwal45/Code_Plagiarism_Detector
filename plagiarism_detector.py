import os
import joblib
from language_parsers import ast_parser, cpp_parser, java_parser
from compare import compare_codes, extract_similarity_features
import re

# Load the trained Random Forest model
model = joblib.load("rf_model.pkl")  # Path to your trained Random Forest model


def load_code(file_path):
    """Loads code from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file {file_path}: {e}"

def preprocess_code(code):
    """Preprocess the code by removing unnecessary whitespaces and comments."""
    # Remove comments
    code = re.sub(r'#.*', '', code)
    # Remove extra whitespace
    code = re.sub(r'\s+', ' ', code).strip()
    return code

def tokenize_code(code):
    """Tokenize the code by splitting by whitespace and removing non-alphanumeric characters."""
    tokens = re.findall(r'\w+', code)
    return tokens

def normalize_code(tokens):
    """Normalize tokens by converting to lowercase."""
    return [token.lower() for token in tokens]

def compute_ast(user_code, reference_code):
    """Compute AST similarity between two pieces of code."""
    # A simple placeholder implementation for AST similarity
    try:
        user_ast = ast.parse(user_code)
        ref_ast = ast.parse(reference_code)
        return compare_ast(user_ast, ref_ast)
    except SyntaxError:
        return 0.0

def compare_ast(user_ast, ref_ast):
    """A basic comparison for AST similarity (you can improve this)."""
    return 1.0 if user_ast == ref_ast else 0.0  # Placeholder for AST match

def compute_cfg(user_code, reference_code):
    """Compute CFG similarity between two pieces of code."""
    # Placeholder for CFG similarity
    return 0.8  # Example, can be improved with a CFG parser

def compute_hash_similarity(user_code, reference_code):
    """Compute hash similarity based on hash values of code."""
    import hashlib
    user_hash = hashlib.sha256(user_code.encode()).hexdigest()
    ref_hash = hashlib.sha256(reference_code.encode()).hexdigest()
    return 1.0 if user_hash == ref_hash else 0.0

def compute_structural_similarity(user_code, reference_code):
    """Compute structural similarity (example)."""
    # Placeholder for structural similarity logic
    return 0.9

def compute_synthetic_similarity(user_code, reference_code):
    """Compute synthetic similarity (example)."""
    # Placeholder for synthetic similarity logic
    return 0.75

def compute_behavioral_similarity(user_code, reference_code):
    """Compute behavioral similarity (example)."""
    # Placeholder for behavioral similarity logic
    return 0.85

def compare_file_pair(user_code, reference_code, ext, test_cases=None):
    """Compare user code with reference code."""
    # Parse code structures based on file extension
    if ext == '.py':
        user_structure = ast_parser.get_ast_structure(user_code)
        ref_structure = ast_parser.get_ast_structure(reference_code)
    elif ext == '.cpp':
        user_structure = cpp_parser.get_cpp_structure(user_code)
        ref_structure = cpp_parser.get_cpp_structure(reference_code)
    elif ext == '.java':
        user_structure = java_parser.get_java_structure(user_code)
        ref_structure = java_parser.get_java_structure(reference_code)
    else:
        return {"error": f"Unsupported language extension: {ext}"}

    # Get similarity results
    similarity_results = compare_codes(user_structure, ref_structure, test_cases)
    
    # Extract features for prediction
    feature_vector = [extract_similarity_features(similarity_results)]
    
    # Predict plagiarism
    prediction = model.predict(feature_vector)[0]
    prediction_label = "Plagiarized" if prediction == 1 else "Not Plagiarized"

    return similarity_results, prediction_label


def detect_plagiarism(user_code_path, reference_dir, test_cases=None):
    """Detect plagiarism for a given user code file against all reference files in a directory."""
    user_code = load_code(user_code_path)
    
    if user_code.startswith("Error loading file"):
        return [{"error": user_code}], {"precision": 0, "recall": 0, "f1": 0, "predictions": []}

    ext = os.path.splitext(user_code_path)[1].lower()  # Get file extension (e.g., .py, .cpp, .java)
    
    results_summary = []
    predictions = []
    total = 0
    plagiarized = 0

    # Iterate over reference files in the provided directory
    for filename in os.listdir(reference_dir):
        if not filename.lower().endswith(ext):  # Filter files by extension
            continue

        ref_path = os.path.join(reference_dir, filename)
        reference_code = load_code(ref_path)

        if reference_code.startswith("Error loading file"):
            results_summary.append({
                "Reference File": filename,
                "Similarity Score": "Error reading file",
                "Prediction": "N/A"
            })
            continue

        # Compare user code with the reference code
        similarity_results, prediction_label = compare_file_pair(user_code, reference_code, ext, test_cases)
        
        similarity_score = similarity_results.get("Text Similarity Score", 0)
        
        # Save results for this comparison
        results_summary.append({
            "Reference File": filename,
            "Similarity Score": round(similarity_score, 4),
            "Prediction": prediction_label
        })
        
        predictions.append(prediction_label)
        total += 1
        if prediction_label == "Plagiarized":
            plagiarized += 1

    # Calculate metrics (precision, recall, f1-score)
    precision = plagiarized / total if total else 0
    recall = precision  # Simplified for demonstration
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

    # Metrics for evaluating the detection performance
    metrics = {
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
        "predictions": predictions
    }
    
    return results_summary, metrics

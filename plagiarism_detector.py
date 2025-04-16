import os
from language_parsers import ast_parser, cpp_parser, java_parser
from compare import compare_codes

def load_code(file_path):
    """Reads the code from a given file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file {file_path}: {e}"

def detect_plagiarism(user_code_path, reference_dir, test_cases=None):
    user_code = load_code(user_code_path)
    if user_code.startswith("Error loading file"):
        return [{"error": user_code}]
    
    ext = os.path.splitext(user_code_path)[1].lower()  # Normalize extension

    if ext == '.py':
        user_structure = ast_parser.get_ast_structure(user_code)
    elif ext == '.cpp':
        user_structure = cpp_parser.get_cpp_structure(user_code)
    elif ext == '.java':
        user_structure = java_parser.get_java_structure(user_code)
    else:
        return [{"error": f"Unsupported language extension: {ext}"}]

    results_summary = []

    for filename in os.listdir(reference_dir):
        if not filename.lower().endswith(ext):
            continue

        ref_path = os.path.join(reference_dir, filename)
        reference_code = load_code(ref_path)

        if reference_code.startswith("Error loading file"):
            results_summary.append({
                "Reference File": filename,
                "Similarity Score": "Error reading file"
            })
            continue

        print(f"Comparing {user_code_path} with {filename}...")  # Log progress

        if ext == '.py':
            ref_structure = ast_parser.get_ast_structure(reference_code)
        elif ext == '.cpp':
            ref_structure = cpp_parser.get_cpp_structure(reference_code)
        elif ext == '.java':
            ref_structure = java_parser.get_java_structure(reference_code)

        similarity = compare_codes(user_structure, ref_structure, test_cases)

        # Optional: Uncomment if you want to skip low similarity scores
        # if similarity < 0.1:
        #     continue

        results_summary.append({
            "Reference File": filename,
            "Similarity Score": round(similarity, 4)
        })

    return results_summary

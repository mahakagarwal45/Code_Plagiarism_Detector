import re
def preprocess_code(code):
    """Removes comments, extra spaces, and standardizes the code format."""
    code = re.sub(r'#.*', '', code)  # Python single-line comments
    code = re.sub(r'//.*', '', code)  # C++/Java single-line comments
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)  # C++/Java multi-line comments
    code = re.sub(r'"""[\s\S]*?"""', '', code)  # Python docstrings
    code = re.sub(r"'''[\s\S]*?'''", '', code)  # Python single-quote docstrings
    code = re.sub(r'\s+', ' ', code)  # Normalize whitespace
    return code.strip()

# language_parsers/cpp_parser.py
import re

def get_cpp_structure(code):
    try:
        # Remove comments
        code = re.sub(r'//.*?$|/\*.*?\*/', '', code, flags=re.DOTALL | re.MULTILINE)

        # Replace variable names and literals
        code = re.sub(r'\bint\b|\bfloat\b|\bdouble\b|\bchar\b|\bstring\b', 'TYPE', code)
        code = re.sub(r'\".*?\"|\'.*?\'|\b\d+\b', 'CONST', code)
        code = re.sub(r'\b\w+\s*(?=\()', 'FUNC', code)  # function calls
        code = re.sub(r'\b\w+\b', 'VAR', code)  # replace remaining words with VAR

        return code
    except Exception as e:
        return f"Error in C++ structure parsing: {str(e)}"

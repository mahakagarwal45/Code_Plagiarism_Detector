# language_parsers/java_parser.py
import re

def get_java_structure(code):
    try:
        # Remove single-line and multi-line comments
        code = re.sub(r'//.*?$|/\*.*?\*/', '', code, flags=re.DOTALL | re.MULTILINE)

        # Replace types and literals
        code = re.sub(r'\bint\b|\bfloat\b|\bString\b|\bdouble\b|\bchar\b', 'TYPE', code)
        code = re.sub(r'\".*?\"|\'.*?\'|\b\d+\b', 'CONST', code)
        code = re.sub(r'\b\w+\s*(?=\()', 'FUNC', code)  # function calls
        code = re.sub(r'\b\w+\b', 'VAR', code)

        return code
    except Exception as e:
        return f"Error in Java structure parsing: {str(e)}"

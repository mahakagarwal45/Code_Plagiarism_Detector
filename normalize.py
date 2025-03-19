import re

def normalize_code(code):
    """ Replaces variable names, numbers, and function names with placeholders. """
    code = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'VAR', code)  # Replace all variable names
    code = re.sub(r'\b\d+\b', 'NUM', code)  # Replace numbers
    return code

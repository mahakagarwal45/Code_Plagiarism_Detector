import re

def preprocess_code(code):
    """ Removes comments, extra spaces, and standardizes the code format. """
    code = re.sub(r'#.*', '', code)  # Remove comments
    code = re.sub(r'"""[\s\S]*?"""', '', code)  # Remove docstrings
    code = re.sub(r"'''[\s\S]*?'''", '', code)  # Remove multi-line docstrings
    code = re.sub(r'\s+', ' ', code).strip()  # Normalize spaces
    return code


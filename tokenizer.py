import tokenize
from io import BytesIO

def tokenize_code(code):
    """ Tokenizes the given code and removes variable names. """
    try:
        tokens = []
        for tok in tokenize.tokenize(BytesIO(code.encode('utf-8')).readline):
            if tok.type == tokenize.NAME:  
                tokens.append("VAR")  # Replace all variable names with VAR
            elif tok.type == tokenize.NUMBER:
                tokens.append("NUM")  # Replace all numbers with NUM
            elif tok.type == tokenize.STRING:
                tokens.append("STR")  # Replace all strings with STR
            else:
                tokens.append(tok.string)
        return " ".join(tokens)
    except Exception as e:
        return f"Error in Tokenization: {str(e)}"

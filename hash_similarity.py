import hashlib

def hash_code(code):
    """ Returns the hash fingerprint of the code. """
    return hashlib.sha256(code.encode()).hexdigest()

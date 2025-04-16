from difflib import SequenceMatcher

def calculate_similarity(code1, code2):
    return round(SequenceMatcher(None, code1, code2).ratio() * 100, 2)

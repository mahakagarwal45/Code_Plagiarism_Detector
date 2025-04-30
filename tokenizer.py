import nltk
from nltk.tokenize import word_tokenize

# Download the 'punkt' tokenizer models if not already downloaded
nltk.download('punkt')

# Function to tokenize text into words
def tokenize_code(code):
    return word_tokenize(code)

# Example usage
if __name__ == "__main__":
    text = input("Enter some text: ")
    tokens = tokenize_code(code)
    print("Tokens:", tokens)

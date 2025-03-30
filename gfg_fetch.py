import requests
from bs4 import BeautifulSoup

def fetch_code_from_gfg(problem_url="https://www.geeksforgeeks.org/reverse-an-array/"):
    """Fetch code from a GeeksforGeeks article."""
    response = requests.get(problem_url)
    if response.status_code != 200:
        return ""

    soup = BeautifulSoup(response.text, 'html.parser')
    code_blocks = soup.find_all("pre")

    # Concatenate all code blocks for comparison
    extracted_code = "\n".join(block.text.strip() for block in code_blocks)

    return extracted_code

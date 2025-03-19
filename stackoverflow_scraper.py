import requests
from bs4 import BeautifulSoup

# URL for Stack Overflow Python questions
url = "https://stackoverflow.com/questions/tagged/python"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract question titles
for post in soup.find_all("a", class_="question-hyperlink"):
    print(post.text)

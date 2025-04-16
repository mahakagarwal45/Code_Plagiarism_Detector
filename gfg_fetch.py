import requests
from bs4 import BeautifulSoup

def fetch_gfg_code(username):
    url = f"https://auth.geeksforgeeks.org/user/{username}/practice/"
    res = requests.get(url)
    
    if res.status_code != 200:
        print("❌ GFG user not found!")
        return

    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.find_all('span', class_='score_card_problem_name')

    print(f"✅ {len(titles)} problems fetched for {username}")
    for t in titles[:5]:
        print("📘", t.text.strip())

# fetch_gfg_code("mahak_123")

import requests

def fetch_cf_info(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    res = requests.get(url).json()

    if res["status"] != "OK":
        print("❌ Codeforces user not found!")
        return

    user = res["result"][0]
    print(f"🎖️ Handle: {user['handle']}")
    print(f"🏅 Rating: {user.get('rating', 'Unrated')}")
    print(f"📈 Max Rating: {user.get('maxRating', 'N/A')}")
    print(f"⚔️ Rank: {user.get('rank', 'N/A')}")

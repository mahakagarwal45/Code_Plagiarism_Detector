# github_fetch.py
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()  
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ Please create a .env file with GITHUB_TOKEN=<your‑token>")
    exit(1)

LANGUAGES = {
    "python": ".py",
    "java":   ".java",
    "cpp":    ".cpp",
}
SEARCH_URL = "https://api.github.com/search/repositories?q=language:{}&sort=stars&per_page=5"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept":        "application/vnd.github.v3+json"
}

def download_code_files(repo_full_name, lang, ext, max_files=3):
    url = f"https://api.github.com/repos/{repo_full_name}/contents"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"  ⚠️ Couldn't list {repo_full_name}: HTTP {r.status_code}")
        return
    files = r.json()
    saved = 0
    save_dir = os.path.join("reference_codes", lang)
    os.makedirs(save_dir, exist_ok=True)

    for f in files:
        if saved >= max_files:
            break
        if f["type"] == "file" and f["name"].endswith(ext):
            try:
                content = requests.get(f["download_url"], headers=HEADERS).text
                local_name = f"{repo_full_name.replace('/', '_')}_{f['name']}"
                local_path = os.path.join(save_dir, local_name)
                with open(local_path, "w", encoding="utf-8") as out:
                    out.write(content)
                print(f"    ✅ Saved {local_name}")
                saved += 1
            except Exception as e:
                print(f"    ❌ Error saving {f['name']}: {e}")
            time.sleep(0.5)

def fetch_github_code():
    for lang, ext in LANGUAGES.items():
        print(f"\n🔍 Fetching top repos for {lang}")
        r = requests.get(SEARCH_URL.format(lang), headers=HEADERS)
        if r.status_code != 200:
            print(f"❌ Search failed for {lang}: HTTP {r.status_code}")
            continue
        for repo in r.json().get("items", []):
            print("📦", repo["full_name"])
            download_code_files(repo["full_name"], lang, ext)
        time.sleep(2)

if __name__ == "__main__":
    fetch_github_code()

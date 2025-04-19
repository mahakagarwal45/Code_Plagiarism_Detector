import requests, os, time, sys
try:
    GITHUB_TOKEN = os.environ["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"]
except KeyError:
    sys.exit("❌ Please run: set GITHUB_TOKEN=<your‑token>")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
SEARCH_URL = "https://api.github.com/search/repositories"
LANGUAGES = {
    "python": ".py",
    "java":   ".java",
    "c++":    ".cpp",
}

def download_code_files(repo_full, lang, ext, max_files=5):
    """Recursively download up to `max_files` code files of extension `ext`."""
    save_dir = os.path.join("reference_codes", lang)
    os.makedirs(save_dir, exist_ok=True)
    stack = [""]
    fetched = 0

    while stack and fetched < max_files:
        path = stack.pop()
        url = f"https://api.github.com/repos/{repo_full}/contents/{path}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        for item in r.json():
            if fetched >= max_files:
                break
            if item["type"] == "dir":
                stack.append(item["path"])
            elif item["type"] == "file" and item["name"].endswith(ext):
                try:
                    raw = requests.get(item["download_url"], headers=HEADERS, timeout=10).text
                    fn = f"{repo_full.replace('/', '_')}_{item['name']}"
                    with open(os.path.join(save_dir, fn), "w", encoding="utf-8") as f:
                        f.write(raw)
                    fetched += 1
                    print(f"  ✅ Saved: {lang}/{fn}")
                except Exception as e:
                    print(f"  ❌ Error saving {item['name']}: {e}")
        time.sleep(0.3)


def fetch_github_code(per_lang_repos=5, per_repo_files=3):
    """Search top repos by stars, then grab a few files from each."""
    for lang, ext in LANGUAGES.items():
        print(f"\n🔍 Fetching top {per_lang_repos} {lang!r} repos…")
        params = {
            "q":      f"language:{lang}",
            "sort":   "stars",
            "order":  "desc",
            "per_page": per_lang_repos
        }
        r = requests.get(SEARCH_URL, headers=HEADERS, params=params)
        if r.status_code != 200:
            print(f"❌ GitHub search failed for {lang}: {r.status_code}")
            continue
        for repo in r.json().get("items", []):
            full = repo["full_name"]
            print(f"📦 Repo: {full}")
            download_code_files(full, lang, ext, max_files=per_repo_files)
        time.sleep(1)


if __name__ == "__main__":
    fetch_github_code(per_lang_repos=5, per_repo_files=3)

import requests
import json
import time

def fetch_github_code():
    # List of languages you want to search for
    languages = ["python", "javascript", "java", "c++", "c", "go", "ruby", "php", "typescript", "rust"]

    # GitHub API base URL
    base_url = "https://api.github.com/search/repositories?q=language:{}&sort=stars&per_page=20"

    # Your GitHub Personal Access Token
    headers = {
        "Authorization": "token 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"
    }

    for lang in languages:
        print(f"🔍 Fetching top repositories for: {lang}")
        url = base_url.format(lang)
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Error fetching for {lang}. HTTP {response.status_code}")
            print(f"⚠️ Response: {response.text}")
            continue
        
        data = response.json()
        
        if "items" not in data:
            print(f"⚠️ No 'items' found for {lang}. Skipping.")
            continue
        
        repo_urls = [repo["html_url"] for repo in data["items"]]
        
        # Save to file
        filename = f"github_repos_{lang}.txt"
        with open(filename, "w") as file:
            for url in repo_urls:
                file.write(url + "\n")
        
        print(f"✅ {len(repo_urls)} repos for {lang} saved to {filename}")
        
        # Respect GitHub rate limits - small delay
        time.sleep(1)

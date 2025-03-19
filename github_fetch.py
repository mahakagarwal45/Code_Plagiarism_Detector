import requests

# import json

# GitHub API URL to search for Python repositories
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
headers = {
    "Authorization": "token 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"
}

response = requests.get(url, headers=headers)
data = response.json()

# Extract repo URLs
repo_urls = [repo["html_url"] for repo in data["items"]]

# Save to file
with open("github_repos.txt", "w") as file:
    for url in repo_urls:
        file.write(url + "\n")

print("✅ Fetched repository URLs saved to 'github_repos.txt'")

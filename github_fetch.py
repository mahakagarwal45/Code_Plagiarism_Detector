# import requests
# # import json

# # GitHub API URL to search for Python repositories
# url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
# headers = {
#     "Authorization": "token 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"
# }

# response = requests.get(url, headers=headers)
# data = response.json()

# # Extract repo URLs
# repo_urls = [repo["html_url"] for repo in data["items"]]

# # Save to file
# with open("github_repos.txt", "w") as file:
#     for url in repo_urls:
#         file.write(url + "\n")

# print("✅ Fetched repository URLs saved to 'github_repos.txt'")


import requests
import json

# GitHub API URL to search for Python repositories
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
headers = {
    "Authorization": "token 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"
}

response = requests.get(url, headers=headers)

# Check HTTP response status
if response.status_code != 200:
    print(f"❌ Error: Unable to fetch data. HTTP Status: {response.status_code}")
    print(f"⚠️ Response: {response.json()}")
    exit()

# Parse JSON response
data = response.json()

# Check if 'items' is in the response
if "items" not in data:
    print("⚠️ No 'items' key found in response. Check your GitHub API token or query.")
    print(f"💡 Response: {json.dumps(data, indent=2)}")
    exit()

# Extract repo URLs
repo_urls = [repo["html_url"] for repo in data["items"]]

# Save to file
with open("github_repos.txt", "w") as file:
    for url in repo_urls:
        file.write(url + "\n")

print(f"✅ Fetched {len(repo_urls)} repository URLs saved to 'github_repos.txt'")

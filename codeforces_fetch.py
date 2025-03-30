import requests

# Replace 'tourist' with any top CodeForces user handle
url = "https://codeforces.com/api/user.status?handle=tourist"

response = requests.get(url)
data = response.json()

# Extract problem names and programming languages
for submission in data['result'][:10]:  # Limit to 10 submissions
    print(f"Problem: {submission['problem']['name']} | Language: {submission['programmingLanguage']}")
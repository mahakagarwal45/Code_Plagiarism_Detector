# # # services/gemini_api.py

# # import google.generativeai as genai

# # # Configure Gemini with your API Key
# # API_KEY = "AIzaSyCnIu-AcZYjTPoOzuMVSAETWDEoww4B5JA"

# # genai.configure(api_key=API_KEY)

# # # Function to generate content from Gemini
# # def generate_gemini_response(prompt_text: str) -> str:
# #     try:
# #         model = genai.GenerativeModel('gemini-pro')
# #         response = model.generate_content(prompt_text)
# #         return response.text
# #     except Exception as e:
# #         return f"Error occurred: {str(e)}"

# # fetchers/gemini_fetch.py

# import os
# import requests
# MODEL = "chat-bison-001"

# # def fetch_gemini_code(language: str, max_snippets: int = 5, save_dir: str = "reference_codes/gemini"):
#     """
#     Fetch code snippets from Gemini for the specified programming language.
#     Saves them under `save_dir` and returns a list of code snippet strings.
#     """
#     os.makedirs(save_dir, exist_ok=True)
#     # Determine file extension
#     ext_map = {"py": ".py", "cpp": ".cpp", "java": ".java"}
#     ext = ext_map.get(language, f".{language}")

#     url = (
#         f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateMessage"
#         f"?key={GEMINI_API_KEY}"
#     )
#     headers = {"Content-Type": "application/json"}

#     system_message = f"You are a helpful assistant generating {language} code examples."
#     user_message = (
#         f"Provide {max_snippets} concise {language} code snippets "
#         "for reference in plagiarism detection, each enclosed in triple backticks."
#     )

#     body = {
#         "prompt": {
#             "messages": [
#                 {"author": "system", "content": system_message},
#                 {"author": "user", "content": user_message},
#             ]
#         },
#         "temperature": 0.5,
#         "maxOutputTokens": 512
#     }

#     resp = requests.post(url, headers=headers, json=body)
#     resp.raise_for_status()
#     data = resp.json()

#     # Extract content
#     candidates = data.get("candidates", [])
#     content = candidates[0].get("content", "") if candidates else ""

#     # Split on code fences
#     snippets = []
#     parts = content.split("```")
#     for part in parts:
#         part = part.strip()
#         # Look for a fence like ```py or ```python
#         if part.startswith(language) or part.startswith(language + "\n"):
#             # drop language label
#             lines = part.split("\n")[1:]
#             snippets.append("\n".join(lines))
#     # Fallback: whole content as one snippet
#     if not snippets and content:
#         snippets = [content]

#     # Save snippets to files
#     for idx, code in enumerate(snippets[:max_snippets]):
#         filename = f"gemini_{idx}{ext}"
#         path = os.path.join(save_dir, filename)
#         with open(path, "w", encoding="utf-8") as f:
#             f.write(code)

#     return snippets

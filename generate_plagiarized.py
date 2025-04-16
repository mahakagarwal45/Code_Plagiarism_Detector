from openai import OpenAI
import os
openai.api_key = os.getenv("sk-QpabguAmdr7EzfzEeXe7TxBvByOkulXVpq_vlEM0llT3BlbkFJUkuinrIuRV50If9G-ViPU5vrRUUqIJiQcvQqVzjWIA")
def generate_plagiarized_code(original_code):
    """Generate a plagiarized version of the original code with modifications."""
    prompt = f"Rewrite the following code with different variable names, loop structures, and formatting:\n\n{original_code}"
    
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=500  # You can adjust max_tokens as needed
        )
        return response.choices[0].text.strip()  # Return the modified code
    except openai.Error as e:
        return f"Error: {str(e)}"
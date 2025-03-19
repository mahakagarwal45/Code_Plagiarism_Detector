from openai import OpenAI

client = OpenAI(api_key="sk-QpabguAmdr7EzfzEeXe7TxBvByOkulXVpq_vlEM0llT3BlbkFJUkuinrIuRV50If9G-ViPU5vrRUUqIJiQcvQqVzjWIA")

def generate_plagiarized_code(original_code):
    prompt = f"Rewrite the following code with different variable names, loop structures, and formatting:\n\n{original_code}"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

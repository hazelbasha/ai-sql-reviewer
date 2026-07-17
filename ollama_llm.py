import ollama
from ollama import chat

response = chat(
    model="qwen2.5-coder:7b",
    messages=[
        {
            "role": "user",
            "content": "Review this SQL: SELECT * FROM UserAccount"
        }
    ]
)

print(response["message"]["content"])
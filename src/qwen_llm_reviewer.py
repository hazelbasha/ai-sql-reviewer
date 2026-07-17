from ollama import chat

def qwen_review_sql_with_llm(sql):

    prompt = f"""
You are a Senior Database Architect.

Review this SQL.

Focus on:
- Performance
- Security
- Maintainability
- SQL Best Practices

SQL:
{sql}
"""

    response = chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
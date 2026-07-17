import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('/Users/z003xsjz/Documents/ScalarAI/ai-sql-reviewer/openai_key.env')  # reads .env file in the current directory

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found! "
        "Make sure you have a .env file with: OPENAI_API_KEY=sk-..."
    )

print("API key loaded successfully.")

client = OpenAI(api_key=api_key)
print("OpenAI client ready.")

def review_sql_with_llm(sql):

    prompt = f"""
You are a Principal Database Architect.

Review the SQL script.

Focus on:

1. Query performance
2. Index utilization
3. Full table scans
4. Join efficiency
5. Security risks
6. Data integrity
7. Production deployment risks
8. SQL anti-patterns

Severity:
CRITICAL
HIGH
MEDIUM
LOW

Provide:

- Summary
- Findings
- Recommendations

SQL:

{sql}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text
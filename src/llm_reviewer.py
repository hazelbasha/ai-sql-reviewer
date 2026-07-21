import os
from openai import OpenAI
from dotenv import load_dotenv

#load_dotenv('/Users/z003xsjz/Documents/ScalarAI/ai-sql-reviewer/openai_key.env')  # reads .env file in the current directory
load_dotenv()


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
You are a Principal Database Architect performing a production-grade SQL review.

Review the SQL script for:

1. Query performance
2. Index utilization
3. Full table scans
4. Join efficiency
5. Security risks
6. Data integrity
7. Production deployment risks
8. SQL anti-patterns
9. Schema adherence
10. Naming accuracy and typo detection

Validation requirements:
- Check for invalid, suspicious, inconsistent, or misspelled table names, column names, aliases, and views.
- Detect likely typos such as transposed, missing, extra, or substituted characters.
- Do not treat syntactically valid identifiers as correct automatically.
- If an identifier appears wrong, suggest the most likely intended identifier.
- If schema is unavailable, mark findings as "possible typo" or "possible schema mismatch".
- If schema is provided, validate strictly against it.

For each issue found, provide:
- Category
- Severity (CRITICAL, HIGH, MEDIUM, LOW)
- Issue description
- Affected SQL fragment
- Why it matters
- Recommended fix
- Suggested corrected identifier if applicable

Output structure:

Summary:
- Overall review summary

Findings:
- Detailed issues grouped by severity

Recommendations:
- Actionable improvements
- Corrected SQL where useful

SQL Script:
{sql}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text
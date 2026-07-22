import os
import json
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

def format_schema(schema):
    if not schema:
        return "No schema provided."

    return json.dumps(schema, indent=2)

def format_list(items):
    if not items:
        return "None"
    return ", ".join(items)

def format_findings(findings):
    if not findings:
        return "No local findings available."

    return json.dumps(findings, indent=2)

def review_sql_with_llm(sql, schema=None, extracted_tables=None, extracted_columns=None, existing_findings=None):
    schema_text = format_schema(schema)
    tables_text = format_list(extracted_tables)
    columns_text = format_list(extracted_columns)
    findings_text = format_findings(existing_findings)

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

Known schema:
{schema_text}

Extracted tables:
{tables_text}

Extracted columns:
{columns_text}

Existing local findings:
{findings_text}

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
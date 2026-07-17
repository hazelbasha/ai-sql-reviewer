from openai import OpenAI

client = OpenAI()

def review_sql(sql):

    prompt = f"""
    You are a Senior Database Architect.

    Review this SQL.

    Check:

    1. Performance
    2. Security
    3. Maintainability
    4. Index usage

    SQL:

    {sql}

    Return findings.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
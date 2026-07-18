import os
from dotenv import load_dotenv
from langfuse import Langfuse
#load_dotenv("/Users/z003xsjz/Documents/ScalarAI/ai-sql-reviewer/langfuse_key.env")
load_dotenv()
#print(f"   Langfuse host: {os.environ.get('LANGFUSE_BASE_URL')} (local Docker)")
#load_dotenv()
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

#print(os.getenv("LANGFUSE_PUBLIC_KEY"))
#print(os.getenv("LANGFUSE_HOST"))

def log_sql_review(sql, review):
    try:

        span = langfuse.start_span(
            name="sql-review"
        )

        span.update(
            input={"sql": sql},
            output={"review": review}
        )

        span.end()

        langfuse.flush()
        pass
    except Exception as e:
        print(f"Langfuse logging skipped: {e}")
from src.langfuse_logger import log_sql_review

sql = """
SELECT *
FROM UserAccount
"""

review = """
SELECT * detected.
Use explicit columns.
"""

log_sql_review(sql, review)

print("Trace sent")
from src.llm_reviewer import review_sql_with_llm
from src.qwen_llm_reviewer import qwen_review_sql_with_llm


sql = """
SELECT *
FROM UserAccount
"""

review = review_sql_with_llm(sql)

print(review)


sql = """
DELETE FROM UserAccount;
"""

qwen_review = qwen_review_sql_with_llm(sql)
print("########## QWEN review starts from here ##########")
print(qwen_review)
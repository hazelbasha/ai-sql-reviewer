from src.qwen_llm_reviewer import qwen_review_sql_with_llm

from src.evaluation import accuracy_metric

from deepeval.test_case import (
    LLMTestCase
)

sql = """
SELECT *
FROM UserAccount;
"""

expected_review = """
SELECT * detected.

Use explicit column names.
"""

actual_review = review_sql_with_llm(sql)

test_case = LLMTestCase(
    input=sql,
    actual_output=actual_review,
    expected_output=expected_review
)

accuracy_metric.measure(test_case)

print("Score:", accuracy_metric.score)
print("Reason:", accuracy_metric.reason)
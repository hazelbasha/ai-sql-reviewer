from src.pr_sql_reviewer import review_pr
from pr_comment_generator import generate_pr_comment
from src.github_client import post_pr_comment

OWNER = "hazelbasha"
REPO = "ai-sql-reviewer"
PR_NUMBER = 1

reviews = review_pr(
    OWNER,
    REPO,
    PR_NUMBER
)

for item in reviews:

    comment = generate_pr_comment(
        item["report"]
    )

    post_pr_comment(
        OWNER,
        REPO,
        PR_NUMBER,
        comment
    )

    print(
        f"Posted review for "
        f"{item['file']}"
    )
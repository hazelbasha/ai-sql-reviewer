from pr_reviewer import review_folder
from pr_comment_generator import generate_pr_comment

reports = review_folder(
    "sqlfiles"
)

for report in reports:

    print(
        report["file"]
    )

    print(
        report["report"]["recommendation"]
    )

    print(
        generate_pr_comment(report["report"])
    )

    print("=" * 50)
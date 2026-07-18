# test_github_pr.py

from src.github_client import get_pr_files

files = get_pr_files(
    "hazelbasha",
    "ai-sql-reviewer",
    1
)

for f in files:
    #print(type(f), f)
    print(f["filename"])
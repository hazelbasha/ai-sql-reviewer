# src/pr_sql_reviewer.py

from src.github_client import get_pr_files
from sql_reviewer import review_sql
import requests

def review_pr(owner, repo, pr_number):

    files = get_pr_files(
        owner,
        repo,
        pr_number
    )

    results = []

    for file in files:

        if not file["filename"].endswith(".sql"):
            continue

        raw_url = file["raw_url"]

        sql = requests.get(raw_url).text

        report = review_sql(sql)

        results.append({
            "file": file["filename"],
            "report": report
        })

    return results
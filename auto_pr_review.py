#auto_pr_review.py
import os
import json
import requests

from src.github_client import (
    get_pr_files,
    post_pr_comment
)

from src.sql_reviewer import review_sql
from pr_comment_generator import generate_pr_comment


with open(os.environ["GITHUB_EVENT_PATH"]) as f:
    event = json.load(f)

owner = event["repository"]["owner"]["login"]
repo = event["repository"]["name"]
pr_number = event["pull_request"]["number"]

print(f"Owner: {owner}")
print(f"Repo: {repo}")
print(f"PR Number: {pr_number}")

files = get_pr_files(
    owner,
    repo,
    pr_number
)

for file in files:

    filename = file["filename"]

    if not filename.endswith(".sql"):
        continue

    sql = requests.get(
        file["raw_url"]
    ).text

    report = review_sql(sql)

    comment = generate_pr_comment(
        report
    )

    post_pr_comment(
        owner,
        repo,
        pr_number,
        comment
    )
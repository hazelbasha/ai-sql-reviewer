#auto_pr_review.py
import os
import json
import requests

from src.github_client import (
    get_pr_files,
    post_pr_comment
)

from sql_reviewer import review_sql
from pr_comment_generator import generate_pr_comment
from src.schema_loader import load_schema_from_json


with open(os.environ["GITHUB_EVENT_PATH"]) as f:
    event = json.load(f)

owner = event["repository"]["owner"]["login"]
repo = event["repository"]["name"]
pr_number = event["pull_request"]["number"]

print(f"Owner: {owner}")
print(f"Repo: {repo}")
print(f"PR Number: {pr_number}")

# Load local schema file once
schema_file_path = "src/overture_schema.json"
schema = load_schema_from_json(schema_file_path)

files = get_pr_files(
    owner,
    repo,
    pr_number
)
all_comments = []
for file in files:

    filename = file["filename"]

    if not filename.endswith(".sql"):
        continue

    print(f"Reviewing SQL file: {filename}")

    try:
        #sql = requests.get(
        #   file["raw_url"]
        #).text 
        response = requests.get(file["raw_url"])
        response.raise_for_status()
        sql = response.text

        report = review_sql(sql, schema=schema)

        comment = generate_pr_comment(
            report
        )
        all_comments.append(f"## Review for `{filename}`\n\n{comment}")
    except Exception as e:
        error_comment = (
            f"## Review for `{filename}`\n\n"
            f"Failed to review this SQL file.\n\n"
            f"Error: `{str(e)}`"
        )
        all_comments.append(error_comment)

if all_comments:
    final_comment = "# AI SQL Review Report\n\n" + "\n\n---\n\n".join(all_comments)

    post_pr_comment(
        owner,
        repo,
        pr_number,
        final_comment
    )
else:
    print("No SQL files found in PR.")
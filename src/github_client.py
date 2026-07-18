import os
import requests
from dotenv import load_dotenv

#load_dotenv("/Users/z003xsjz/Documents/ScalarAI/ai-sql-review-git/ai-sql-reviewer/github_key.env")
load_dotenv()
TOKEN = os.getenv("TOKEN_GITHUB")
headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }



def get_pr_files(owner, repo, pr_number):

    print("TOKEN:",TOKEN)

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/pulls/{pr_number}/files"
    )

   
    print("TOKEN:",TOKEN,url,headers)

    response = requests.get(
        url,
        headers=headers
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
        return []

    return response.json()


def post_pr_comment(
    owner,
    repo,
    pr_number,
    comment
):

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/issues/{pr_number}/comments"
    )

    payload = {
        "body": comment
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )
    print("Comment URL:", url)
    print(f"Comment Status: {response.status_code}")
    print(response.text)

    return response.json()
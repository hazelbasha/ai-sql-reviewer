import os

from sql_reviewer import review_sql


def review_folder(folder):

    reports = []

    for file in os.listdir(folder):

        if file.endswith(".sql"):

            path = os.path.join(
                folder,
                file
            )

            with open(path) as f:
                sql = f.read()

            report = review_sql(sql)

            reports.append({
                "file": file,
                "report": report
            })

    return reports
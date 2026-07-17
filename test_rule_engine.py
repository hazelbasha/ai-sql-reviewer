from src.rule_engine import run_rules
from src.review_score import calculate_score

files = [
    "test_data/select_star.sql",
    "test_data/delete_without_where.sql",
    "test_data/update_without_where.sql"
]

for file in files:
    print(f"\nTesting: {file}")

    with open(file) as f:
        sql = f.read()

    findings = run_rules(sql)

    for finding in findings:
         score = calculate_score(findings)
         print(score)
         print(findings)
    
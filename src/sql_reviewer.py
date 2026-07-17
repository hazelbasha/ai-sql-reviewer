from rule_engine import run_rules
from review_score import calculate_score
from review_report import build_report



def review_sql(sql):

    findings = []

    findings.extend(run_rules(sql))

    score = calculate_score(findings)

    report = build_report(score, findings)

    return report
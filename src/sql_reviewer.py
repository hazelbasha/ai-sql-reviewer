from rule_engine import run_rules
from review_score import calculate_score
from review_report import build_report
from alter_reviewer import review_alter_statements



def review_sql(sql):

    findings = []

    findings.extend(run_rules(sql))
    # New ALTER checks added as extra layer
    findings.extend(review_alter_statements(sql))


    score = calculate_score(findings)

    report = build_report(score, findings)

    return report
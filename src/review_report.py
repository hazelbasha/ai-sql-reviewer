def generate_recommendation(score):

    if score >= 90:
        return "APPROVE"

    elif score >= 70:
        return "APPROVE_WITH_COMMENTS"

    return "REJECT"


def build_report(score, findings):

    recommendation = generate_recommendation(score)

    report = {
        "score": score,
        "recommendation": recommendation,
        "findings": findings
    }

    return report

def print_report(report):

    print("\nSQL REVIEW REPORT")
    print("=" * 50)

    print(f"Score: {report['score']}")

    print(
        f"Recommendation: {report['recommendation']}"
    )

    print("\nFindings:")

    if not report["findings"]:
        print("No issues found")

    for finding in report["findings"]:

        print(
            f"[{finding['severity']}] "
            f"{finding['issue']}"
        )
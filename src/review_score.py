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

def calculate_score(findings):

    score = 100

    for finding in findings:

        if finding["severity"] == "CRITICAL":
            score -= 40

        elif finding["severity"] == "HIGH":
            score -= 20

        elif finding["severity"] == "MEDIUM":
            score -= 10

        elif finding["severity"] == "LOW":
            score -= 5

    return max(score, 0)

def generate_pr_comment(report):

    comment = []

    comment.append(
        f"Recommendation: "
        f"{report['recommendation']}"
    )

    comment.append("")

    for finding in report["findings"]:

        comment.append(
            f"- [{finding['severity']}] "
            f"{finding['issue']}"
        )

    return "\n".join(comment)
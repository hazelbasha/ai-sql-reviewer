def generate_pr_comment(report):

    comment = []

   #comment.append(
    #    f"Recommendation: "
    #    f"{report['recommendation']}"
   # )

    comment.append(
        f"Recommendation: {report.get('recommendation', 'No recommendation available')}"
    )

    comment.append("")

    #for finding in report["findings"]:

     #   comment.append(
     #       f"- [{finding['severity']}] "
      #      f"{finding['issue']}"
     #   )
    for finding in report.get("findings", []):
        issue_text = finding.get("issue") or finding.get("problem") or "No issue description"

        comment.append(
            f"- [{finding.get('severity', 'UNKNOWN')}] {issue_text}"
        )
    return "\n".join(comment)
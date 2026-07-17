def run_rules(sql):

    findings = []

    sql_upper = sql.upper()

    if "SELECT *" in sql_upper:
        findings.append({
            "severity": "HIGH",
            "issue": "SELECT * detected"
        })

    if "DELETE" in sql_upper and "WHERE" not in sql_upper:
        findings.append({
            "severity": "CRITICAL",
            "issue": "DELETE without WHERE"
        })

    if "UPDATE" in sql_upper and "WHERE" not in sql_upper:
        findings.append({
            "severity": "CRITICAL",
            "issue": "UPDATE without WHERE"
        })

    return findings
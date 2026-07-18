from src.rule_engine import run_rules
from src.review_score import calculate_score
from src.review_report import build_report
from src.sql_parser import (
    extract_tables,
    extract_columns,
    count_joins
)
from src.llm_reviewer import review_sql_with_llm
from src.langfuse_logger import log_sql_review






def review_sql(sql):

    findings = []

    findings.extend(run_rules(sql))

    score = calculate_score(findings)

    report = build_report(score, findings)

    tables = extract_tables(sql)

    columns = extract_columns(sql)

    joins = count_joins(sql)

    ai_review = review_sql_with_llm(sql)  

    report["metadata"] = {
    "tables": tables,
    "columns": columns,
    "joins": joins
    }
    report["ai_review"] = ai_review
    try:
        # Langfuse Logging
        log_sql_review(
            sql,
            ai_review
        )
    except Exception as e:
        print(f"Langfuse error: {e}")


    return report
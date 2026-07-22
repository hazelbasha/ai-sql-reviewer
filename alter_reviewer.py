import json
import re
from pathlib import Path

def load_schema_metadata():
    """
    Loads schema metadata JSON from src/overture_schema_v2.json
    Adjust path if your project structure is different.
    """
    schema_path = Path(__file__).resolve().parent / "src" / "overture_schema_v2.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def review_alter_statements(sql_text, schema=None):
    """
    Reviews ALTER TABLE statements only.
    Existing SQL review flow can call this as an additional step.
    """
    if schema is None:
        schema = load_schema_metadata()

    findings = []
    tables = schema.get("tables", {})
    statements = split_sql_statements(sql_text)

    for stmt in statements:
        if not re.search(r"^\s*ALTER\s+TABLE\s+", stmt, re.IGNORECASE):
            continue

        findings.extend(analyze_alter_statement(stmt, tables))

    return findings

def split_sql_statements(sql_text):
    """
    Basic SQL splitter for POC.
    Splits by semicolon.
    """
    return [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]

def analyze_alter_statement(stmt, tables):
    findings = []

    match = re.search(
        r"ALTER\s+TABLE\s+`?([A-Za-z0-9_]+)`?\s+(.*)",
        stmt,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        findings.append(make_finding(
            "medium",
            "Could not parse ALTER TABLE statement.",
            stmt
        ))
        return findings

    table_name = match.group(1)
    alter_body = match.group(2).strip()

    if table_name not in tables:
        findings.append(make_finding(
            "high",
            f"Table '{table_name}' not found in schema metadata.",
            stmt,
            table_name=table_name
        ))
        return findings

    table_meta = tables[table_name]
    row_count = int(table_meta.get("row_count", 0) or 0)
    columns = table_meta.get("columns", {})
    foreign_keys = table_meta.get("foreign_keys", [])

    if row_count > 100000:
        findings.append(make_finding(
            "medium",
            f"Table '{table_name}' has estimated row count {row_count}. ALTER may be expensive or locking.",
            stmt,
            table_name=table_name
        ))

    findings.extend(check_add_column(table_name, alter_body, columns, row_count, stmt))
    findings.extend(check_drop_column(table_name, alter_body, columns, foreign_keys, stmt))
    findings.extend(check_modify_column(table_name, alter_body, columns, foreign_keys, row_count, stmt))
    findings.extend(check_change_column(table_name, alter_body, columns, foreign_keys, row_count, stmt))

    return findings

def check_add_column(table_name, alter_body, columns, row_count, stmt):
    findings = []

    matches = re.findall(
        r"ADD\s+COLUMN\s+`?([A-Za-z0-9_]+)`?\s+([A-Za-z0-9(),]+)(.*?)(?=,\s*(ADD|DROP|MODIFY|CHANGE)\b|$)",
        alter_body,
        re.IGNORECASE | re.DOTALL
    )

    for match in matches:
        col_name = match[0]
        col_type = match[1]
        remainder = match[2] or ""

        if col_name in columns:
            findings.append(make_finding(
                "high",
                f"Column '{col_name}' already exists in table '{table_name}'.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))

        is_not_null = bool(re.search(r"NOT\s+NULL", remainder, re.IGNORECASE))
        has_default = bool(re.search(r"\bDEFAULT\b", remainder, re.IGNORECASE))

        if row_count > 0 and is_not_null and not has_default:
            findings.append(make_finding(
                "high",
                f"Adding NOT NULL column '{col_name}' to populated table '{table_name}' without DEFAULT may fail or require backfill.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))

    return findings

def check_drop_column(table_name, alter_body, columns, foreign_keys, stmt):
    findings = []

    matches = re.findall(
        r"DROP\s+COLUMN\s+`?([A-Za-z0-9_]+)`?",
        alter_body,
        re.IGNORECASE
    )

    for col_name in matches:
        if col_name not in columns:
            findings.append(make_finding(
                "high",
                f"Column '{col_name}' does not exist in table '{table_name}'.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))
            continue

        fk_refs = [fk for fk in foreign_keys if fk.get("column") == col_name]
        if fk_refs:
            findings.append(make_finding(
                "high",
                f"Column '{col_name}' in table '{table_name}' is part of a foreign key and dropping it is risky.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))

        if col_name in table_name:
            pass

    return findings

def check_modify_column(table_name, alter_body, columns, foreign_keys, row_count, stmt):
    findings = []

    matches = re.findall(
        r"MODIFY\s+COLUMN\s+`?([A-Za-z0-9_]+)`?\s+([A-Za-z0-9(),]+)(.*?)(?=,\s*(ADD|DROP|MODIFY|CHANGE)\b|$)",
        alter_body,
        re.IGNORECASE | re.DOTALL
    )

    for match in matches:
        col_name = match[0]
        new_type = match[1].strip().lower()
        remainder = match[2] or ""

        if col_name not in columns:
            findings.append(make_finding(
                "high",
                f"Column '{col_name}' does not exist in table '{table_name}' for MODIFY.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))
            continue

        old_type = str(columns[col_name].get("type", "")).strip().lower()
        old_nullable = bool(columns[col_name].get("nullable", True))

        if old_type != new_type:
            findings.append(make_finding(
                "medium",
                f"Column '{col_name}' type change in table '{table_name}': '{old_type}' -> '{new_type}'. Review for compatibility and data truncation risk.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))

        new_not_null = bool(re.search(r"NOT\s+NULL", remainder, re.IGNORECASE))
        if old_nullable and new_not_null and row_count > 0:
            findings.append(make_finding(
                "high",
                f"Changing nullable column '{col_name}' to NOT NULL in populated table '{table_name}' may fail if null values exist.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))

        fk_refs = [fk for fk in foreign_keys if fk.get("column") == col_name]
        if fk_refs:
            findings.append(make_finding(
                "high",
                f"Column '{col_name}' in table '{table_name}' is part of a foreign key. Type or nullability changes require careful validation.",
                stmt,
                table_name=table_name,
                column_name=col_name
            ))

    return findings

def check_change_column(table_name, alter_body, columns, foreign_keys, row_count, stmt):
    findings = []

    matches = re.findall(
        r"CHANGE\s+COLUMN\s+`?([A-Za-z0-9_]+)`?\s+`?([A-Za-z0-9_]+)`?\s+([A-Za-z0-9(),]+)(.*?)(?=,\s*(ADD|DROP|MODIFY|CHANGE)\b|$)",
        alter_body,
        re.IGNORECASE | re.DOTALL
    )

    for match in matches:
        old_col_name = match[0]
        new_col_name = match[1]
        new_type = match[2].strip().lower()
        remainder = match[3] or ""

        if old_col_name not in columns:
            findings.append(make_finding(
                "high",
                f"Column '{old_col_name}' does not exist in table '{table_name}' for CHANGE COLUMN.",
                stmt,
                table_name=table_name,
                column_name=old_col_name
            ))
            continue

        if old_col_name != new_col_name and new_col_name in columns:
            findings.append(make_finding(
                "high",
                f"Cannot rename column '{old_col_name}' to '{new_col_name}' in table '{table_name}' because target column already exists.",
                stmt,
                table_name=table_name,
                column_name=old_col_name
            ))

        old_type = str(columns[old_col_name].get("type", "")).strip().lower()
        old_nullable = bool(columns[old_col_name].get("nullable", True))

        if old_type != new_type:
            findings.append(make_finding(
                "medium",
                f"Column '{old_col_name}' type change in table '{table_name}': '{old_type}' -> '{new_type}'. Review for compatibility and data truncation risk.",
                stmt,
                table_name=table_name,
                column_name=old_col_name
            ))

        new_not_null = bool(re.search(r"NOT\s+NULL", remainder, re.IGNORECASE))
        if old_nullable and new_not_null and row_count > 0:
            findings.append(make_finding(
                "high",
                f"Changing nullable column '{old_col_name}' to NOT NULL in populated table '{table_name}' may fail if null values exist.",
                stmt,
                table_name=table_name,
                column_name=old_col_name
            ))

        fk_refs = [fk for fk in foreign_keys if fk.get("column") == old_col_name]
        if fk_refs:
            findings.append(make_finding(
                "high",
                f"Column '{old_col_name}' in table '{table_name}' is part of a foreign key. Renaming or modifying it is risky.",
                stmt,
                table_name=table_name,
                column_name=old_col_name
            ))

    return findings

def make_finding(severity, message, statement, table_name=None, column_name=None):
    return {
        "severity": severity,
        "message": message,
        "table": table_name,
        "column": column_name,
        "statement": statement.strip()
    }
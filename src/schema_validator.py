from difflib import get_close_matches

def flatten_schema_columns(schema):
    table_columns = {}
    all_columns = set()

    for table_name, table_meta in schema.items():
        columns = table_meta.get("columns", {})
        col_names = set(columns.keys())
        table_columns[table_name] = col_names
        all_columns.update(col_names)

    return table_columns, all_columns

def find_closest_match(name, candidates, cutoff=0.8):
    matches = get_close_matches(name, list(candidates), n=1, cutoff=cutoff)
    return matches[0] if matches else None

def validate_identifiers_against_schema(tables, columns, schema):
    findings = []

    if not schema:
        return findings

    table_columns, all_columns = flatten_schema_columns(schema)
    valid_tables = set(schema.keys())

    for table in tables:
        if table not in valid_tables:
            suggestion = find_closest_match(table, valid_tables)
            findings.append({
                "category": "Schema Adherence",
                "severity": "HIGH",
                "problem": f"Unknown table name '{table}'",
                "affected_object": table,
                "explanation": (
                    f"Table '{table}' does not exist in schema."
                    + (f" Did you mean '{suggestion}'?" if suggestion else "")
                ),
                "suggested_correction": suggestion
            })

    for column in columns:
        if column not in all_columns:
            suggestion = find_closest_match(column, all_columns)
            findings.append({
                "category": "Schema Adherence",
                "severity": "MEDIUM",
                "problem": f"Unknown column name '{column}'",
                "affected_object": column,
                "explanation": (
                    f"Column '{column}' does not exist in schema."
                    + (f" Did you mean '{suggestion}'?" if suggestion else "")
                ),
                "suggested_correction": suggestion
            })

    return findings
from sqlglot import parse_one
from sqlglot.expressions import Table
from sqlglot.expressions import Column
from sqlglot.expressions import Join

def parse_sql(sql):

    try:

        tree = parse_one(sql)

        return {
            "valid": True,
            "tree": tree
        }

    except Exception as e:

        return {
            "valid": False,
            "error": str(e)
        }
def extract_tables(sql):

    tree = parse_one(sql)

    tables = []

    for table in tree.find_all(Table):
        tables.append(table.name)

    return tables
def extract_columns(sql):

    tree = parse_one(sql)

    columns = []

    for column in tree.find_all(Column):
        columns.append(column.name)

    return columns

def count_joins(sql):

    tree = parse_one(sql)

    joins = list(tree.find_all(Join))

    return len(joins)

def run_ast_rules(sql):

    findings = []

    join_count = count_joins(sql)

    if join_count > 5:

        findings.append({
            "severity": "MEDIUM",
            "issue": f"Query contains {join_count} joins"
        })

    return findings
from sqlglot import parse_one
from sqlglot.expressions import Table


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
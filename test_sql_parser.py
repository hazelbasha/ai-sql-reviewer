from src.sql_parser import parse_sql,extract_tables,extract_columns,count_joins,run_ast_rules


sql = """
SELECT UserId,
       Email
FROM UserAccount
WHERE UserId = 100
"""

sql2 = """
SELECT *
FROM Orders o
JOIN Customers c
ON o.CustomerId = c.CustomerId
"""
sql3="""SELECT *
FROM A
JOIN B ON A.id=B.id
JOIN C ON B.id=C.id
JOIN D ON C.id=D.id
JOIN E ON D.id=E.id
JOIN F ON E.id=F.id
JOIN G ON F.id=G.id"""
result = parse_sql(sql)

print(result["valid"])

print(result["tree"])

print("Table:",extract_tables(sql))

print("columns:",extract_columns(sql))
print("Joins:",count_joins(sql2))
print("Joins3:",run_ast_rules(sql3))
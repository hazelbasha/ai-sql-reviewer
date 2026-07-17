from sql_reviewer import review_sql
from src.review_report import print_report


#sql = """ DELETEvFROM UserAccountv"""

#sql="""SELECT UserId, Email FROM UserAccount WHERE UserId = 100;"""
#sql= """UPDATE UserAccount SET Status='ACTIVE' """;
sql= """DELETE FROM UserAccount  """;

report = review_sql(sql)

print(report)
print_report(report)

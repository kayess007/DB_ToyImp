import sqlite3
import pandas as pd

conn = sqlite3.connect("toy_las_system.db")

print("\n=== Wells Table ===")
print(pd.read_sql_query("SELECT * FROM Wells", conn))

print("\n=== First 10 rows of LogData ===")
print(pd.read_sql_query("SELECT * FROM LogData LIMIT 10", conn))

print("\n=== Count rows in LogData ===")
print(pd.read_sql_query("SELECT COUNT(*) AS row_count FROM LogData", conn))

conn.close()
import sqlite3
import pandas as pd

conn = sqlite3.connect("toy_las_system.db")

query = "SELECT * FROM LogData LIMIT 1;"
print(pd.read_sql_query(query, conn))

conn.close()    
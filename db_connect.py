import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname="welllogs",
        user="admin",
        password="admin",
        host="localhost",
    )
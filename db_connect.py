import psycopg2
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import uuid

def get_cluster():
    return Cluster(['127.0.0.1'], port=9042)

def get_session(cluster):
    session = cluster.connect()
    session.set_keyspace('well_logs')
    return session

def get_conn():
    return psycopg2.connect(
        dbname="welllogs",
        user="admin",
        password="admin",
        host="localhost",
    )
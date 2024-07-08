from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
from typing import List
from cc_fraud_detector.api.models.transaction import Transaction

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "fraud_detector")

try:
    cluster = Cluster([CASSANDRA_HOST], port=9042)
    session = cluster.connect(CASSANDRA_KEYSPACE)
    print("Connected to Cassandra")
except Exception as e:
    print(f"Failed to connect to Cassandra: {e}")


async def add_transaction(transaction_id: str, status: str):
    query = """
    INSERT INTO transactions (transaction_id, status)
    VALUES (%s, %s)
    """
    session.execute(query, (transaction_id, status))
                            

async def get_transactions():
    query = "SELECT * FROM transactions"
    rows = session.execute(query)
    transactions = [row._asdict() for row in rows]
    return transactions

async def get_transaction(transaction_id: str):
    query = "SELECT * FROM transactions WHERE transaction_id=%s"
    row = session.execute(query, (transaction_id,))
    transaction = Transaction(**row.one()._asdict())
    return transaction

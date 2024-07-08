import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
    CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "my_keyspace")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

settings = Settings()

from kafka import KafkaProducer
import json
from cc_fraud_detector.api.core.config import settings

producer = KafkaProducer(bootstrap_servers=settings.KAFKA_BROKER)

def send_transaction(transaction):
    producer.send('transactions', json.dumps(transaction.dict()).encode('utf-8'))
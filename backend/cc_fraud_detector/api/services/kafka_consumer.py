# kafka_consumer.py

import asyncio
import json
from kafka import KafkaConsumer
from cc_fraud_detector.api.services.cassandra_service import add_transaction
from cc_fraud_detector.api.services.prediction_service import predict_fraud
from cc_fraud_detector.api.models.transaction import Transaction
from cc_fraud_detector.api.core.config import settings

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=settings.KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detection-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

async def process_transaction(transaction):
    transaction_model = Transaction(**transaction)
    transaction_dict = transaction_model.dict()
    prediction = await predict_fraud(transaction_dict)
    transaction['status'] = prediction
    prediction = 'fraud' if prediction == 1 else 'not_fraud'
    print(f"Prediction for transaction {transaction['TransactionID']}: {prediction}")
    try:
        await add_transaction(transaction['TransactionID'], prediction)
    except Exception as e:
        print(f"Failed to add transaction to Cassandra: {e}")
        return {"error": str(e)}
    
    
def consume():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for message in consumer:
        transaction = message.value
        loop.run_until_complete(process_transaction(transaction))

if __name__ == "__main__":
    consume()

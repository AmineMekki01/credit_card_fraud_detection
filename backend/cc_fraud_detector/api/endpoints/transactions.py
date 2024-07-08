from fastapi import APIRouter, UploadFile, File
from cc_fraud_detector.api.models.transaction import Transaction
from cc_fraud_detector.api.services.cassandra_service import add_transaction, get_transactions, get_transaction
from cc_fraud_detector.api.services.kafka_service import send_transaction
from cc_fraud_detector.api.services.prediction_service import predict_fraud, predict_batch
import subprocess
import os
from pathlib import Path

router = APIRouter()

@router.post("/simulate")
async def simulate_transactions():
    script_path = Path(__file__).resolve().parent.parent.parent / 'simulate_transaction.py'
    
    if not script_path.exists():
        return {"error": f"simulate_transaction.py not found at {script_path}"}
    
    try:
        process = subprocess.Popen(["python", str(script_path)])
    except Exception as e:
        print(f"Failed to start subprocess: {e}")
        return {"error": str(e)}
    
    return {"status": "Simulation started"}


@router.post("/transactions")
async def create_transaction(transaction: Transaction):
    send_transaction(transaction)
    return {"status": "Transaction sent to Kafka"}

@router.get("/transactions")
async def read_transactions():
    transactions = await get_transactions()
    return transactions

@router.get("transactions/{transaction_id}")
async def read_transaction(transaction_id: str):
    transaction = await get_transaction(transaction_id)
    return transaction

@router.post("/predict_batch")
async def predict_batch_endpoint(transaction_file: UploadFile = File(...), identity_file: UploadFile = File(...)):
    transaction_data_path = f"/tmp/{transaction_file.filename}"
    identity_data_path = f"/tmp/{identity_file.filename}"

    with open(transaction_data_path, "wb") as f:
        f.write(transaction_file.file.read())
    
    with open(identity_data_path, "wb") as f:
        f.write(identity_file.file.read())
    
    predictions = await predict_batch(transaction_data_path, identity_data_path)
    return {"predictions": predictions.tolist()}

@router.post("/predict_single")
async def predict_single(transaction: Transaction):
    prediction = await predict_fraud(transaction)
    return {"prediction": prediction}


from cc_fraud_detector.api.models.transaction import Transaction

from cc_fraud_detector_model.src.components.inference import Inference


inference = Inference()

async def predict_fraud(transaction: Transaction):
    prediction = inference.predict_single(transaction)
    return prediction

async def predict_batch(transaction_data_path, identity_data_path):
    predictions = inference.predict(transaction_data_path, identity_data_path)
    return predictions

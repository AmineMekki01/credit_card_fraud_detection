import pandas as pd
import requests
import random
import time
import numpy as np

CSV_FILE_PATH = '/media/WORK/Projects/credit_card_fraud_detection/artifacts/data/raw/test/test_transaction.csv'
API_URL = 'http://localhost:8000/transactions'



def clean_transaction(transaction):
    for key, value in transaction.items():
        if pd.isnull(value):
            transaction[key] = None 
        elif isinstance(value, float) and (np.isinf(value) or np.isnan(value)):
            transaction[key] = None 
    return transaction

def simulate_transactions():
    df = pd.read_csv(CSV_FILE_PATH)
    count = 1
    
    while count > 0:
        random_transaction = df.sample(1).to_dict(orient='records')[0]
        clean_transaction(random_transaction)
        response = requests.post(API_URL, json=random_transaction)
        print(response.json())
        time.sleep(5)
        count -= 1

if __name__ == "__main__":
    simulate_transactions()
# cc_fraud_detector_model/components/inference.py
import pandas as pd
import joblib
import numpy as np
import json
import os
from cc_fraud_detector_model.src.components.data_processing import process_v_columns
from cc_fraud_detector_model.src.configuration.configuration_manager import ConfigurationManager
from cc_fraud_detector_model.src.pipelines.feature_engineering_pipeline import FeatureEngineeringPipeline
from cc_fraud_detector_model.src import logger

class Inference:
    
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.data_processing_config = self.config_manager.get_data_processing_params()
        self.inference_params = self.config_manager.get_inference_params()
        self.model_name = self.inference_params.model_name
        self.model_path = os.path.join(self.inference_params.trained_model_directory_path, f"{self.model_name}_model.joblib")
        
        self.model = None        
        with open(self.data_processing_config.column_features_file_path , 'r') as f:
            self.v_columns_to_keep = json.load(f)
    
    def load_model(self):
        self.model = joblib.load(self.model_path)
        logger.info(f"Model loaded from {self.model_path}")

    
    def process_csv_data(self, transaction_data_path, identity_data_path):
        transaction_data = pd.read_csv(transaction_data_path)
        identity_data = pd.read_csv(identity_data_path)
        transaction_data = transaction_data[self.v_columns_to_keep]
        transaction_data = transaction_data.set_index('TransactionID')
        transaction_data = transaction_data.merge(identity_data, how='left', left_index=True, right_index=True)
        return transaction_data, self.v_columns_to_keep
    
    
    def process_data(self, transaction_data):
        if isinstance(transaction_data, dict):
            transaction_data = pd.DataFrame([transaction_data])

        transaction_data = transaction_data[self.v_columns_to_keep]
        return transaction_data
    
    
    def predict_csv(self, transaction_data_path, identity_data_path):
        transaction_data, v_columns_to_keep = self.process_data(transaction_data_path, identity_data_path)
        if self.model is None:
            self.load_model()

        feature_engineer = FeatureEngineeringPipeline()
        transaction_data_processed = feature_engineer.run(transaction_data)
        
        y_pred = self.model.predict_proba(transaction_data_processed[v_columns_to_keep])[:,1]
        y_pred = (y_pred > 0.5).astype(int)
        return y_pred
    
    def predict(self, transaction_data):
        if self.model is None:
            self.load_model()

        feature_engineer = FeatureEngineeringPipeline()
        transaction_data_processed = feature_engineer.run(transaction_data)
        
        y_pred = self.model.predict_proba(transaction_data_processed[self.v_columns_to_keep])[:,1]
        y_pred = (y_pred > 0.5).astype(int)
        return y_pred

    def predict_single(self, transaction):
        transaction_data = pd.DataFrame([transaction])
        transaction_data_processed = self.process_data(transaction_data)
        prediction = self.predict(transaction_data_processed)
        return prediction[0]

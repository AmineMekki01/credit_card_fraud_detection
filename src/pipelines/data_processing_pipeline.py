import yaml
import pandas as pd
import json
from src.configuration.configuration_manager import ConfigurationManager
from src import logger
from src.components.data_processing import process_v_columns


STAGE1 = 'Data Processing'


class DataProcessingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.data_processing_config = self.config_manager.get_data_processing_params()

    def run(self):
        transaction_data = pd.read_csv(self.data_processing_config.transaction_data_path)
        identity_data = pd.read_csv(self.data_processing_config.identity_data_path)

        v_columns_to_keep = process_v_columns(transaction_data, self.data_processing_config.threshold)
        
        with open(self.data_processing_config.column_features_file_path, 'w') as f:
            json.dump(v_columns_to_keep, f)
        
        
        transaction_data = transaction_data[v_columns_to_keep+['isFraud']]
        transaction_data = transaction_data.set_index('TransactionID')
        transaction_data = transaction_data.merge(identity_data, how='left', left_index=True, right_index=True)
        y_train = transaction_data['isFraud'].copy()
        X_train = transaction_data.drop('isFraud', axis=1)

        return X_train, y_train, v_columns_to_keep
    

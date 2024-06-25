# src/configuration/configuration_manager.py
from pathlib import Path
import json
from src.configuration.entity import DataProcessingParams, ModelParams, TrainingParams, InferenceParams
from src.utils.common_functions import read_yaml

class ConfigurationManager:
    def __init__(self):
        self.configs = read_yaml(Path("./config/config.yaml"))
    
    def get_data_processing_params(self) -> DataProcessingParams:
        data_processing_params = self.configs['data_processing_params']
        return DataProcessingParams(
            threshold=data_processing_params['threshold'],
            transaction_data_path=data_processing_params['transaction_data_path'],
            identity_data_path=data_processing_params['identity_data_path'],
            column_features_file_path=data_processing_params['column_features_file_path']
        )
        
    def get_feature_engineering_params(self) -> None:
        pass
    
    def get_model_params(self) -> ModelParams:
        model_params = self.configs['model_params']
        return ModelParams(
            n_estimators=model_params['n_estimators'],
            max_depth=model_params['max_depth'],
            learning_rate=model_params['learning_rate'],
            subsample=model_params['subsample'],
            col_sample_by_tree=model_params['col_sample_by_tree'],
            missing=model_params['missing'],
            eval_metric=model_params['eval_metric'],
            tree_method=model_params['tree_method'],
            device=model_params['device'],
            enable_categorical=model_params['enable_categorical'],
            early_stopping_rounds=model_params['early_stopping_rounds']
        )

    def get_training_params(self) -> TrainingParams:
        training_params = self.configs['training_params']
        return TrainingParams(
            trained_model_directory_path=training_params.trained_model_directory_path,
            model_name=training_params.model_name
        )
        
    
    def get_inference_params(self) -> InferenceParams:
        inference_params = self.configs['inference_params']
        return InferenceParams(
            model_name=inference_params['model_name'],
            trained_model_directory_path=inference_params['trained_model_directory_path']
        )
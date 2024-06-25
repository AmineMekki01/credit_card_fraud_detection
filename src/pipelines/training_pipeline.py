# src/pipelines/training_pipeline.py
import pandas as pd
import numpy as np
import joblib

from src.components.models import Models
from src.components.trainer import ModelTrainer
from src.configuration.configuration_manager import ConfigurationManager
from src import logger

class TrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.model_params = self.config_manager.get_model_params()
        self.training_params = self.config_manager.get_training_params()
        self.model_name = self.training_params.model_name

    def run(self, X_train: pd.DataFrame, y_train: pd.Series, model_name: str, v_columns_to_keep: list):
        """
        Run the model training pipeline.
        
        Args:
            X_train (pd.DataFrame): Features.
            y_train (pd.Series): Target variable.
            model_name (str): Model to train.
        
        Returns:
            model: Trained model.
            metrics: Evaluation metrics.
        """
        
        if model_name is None:
            model_name = self.model_name
        
        X_train = X_train.astype(np.float32)
        y_train = y_train.astype(np.float32)
        
        model_instance = Models()
        model = model_instance.get_model(model_name, self.model_params.__dict__)
        
        trainer = ModelTrainer(model, X_train, y_train, v_columns_to_keep=v_columns_to_keep)
        
        trained_model = trainer.train()
        metrics = trainer.evaluate()

        model_path = f"{self.training_params.trained_model_directory_path}{model_name}_model.joblib"
        
        joblib.dump(trained_model, model_path)
        logger.info(f"Model saved to {model_path}")
        return trained_model, metrics

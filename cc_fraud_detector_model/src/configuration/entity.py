# cc_fraud_detector/configuration/entity.py
from dataclasses import dataclass

@dataclass
class ModelParams:
    n_estimators : int
    max_depth : int
    learning_rate : float 
    subsample : float
    col_sample_by_tree : float
    missing : float
    eval_metric : str
    tree_method  : str
    device  : str
    enable_categorical : bool
    early_stopping_rounds : int


@dataclass
class DataProcessingParams:
    threshold : float
    transaction_data_path : str
    identity_data_path : str
    column_features_file_path : str


@dataclass
class TrainingParams:
    trained_model_directory_path : str
    model_name : str
    
@dataclass
class InferenceParams:
    trained_model_directory_path : str
    model_name : str
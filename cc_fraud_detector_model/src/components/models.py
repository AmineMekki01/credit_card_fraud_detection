# cc_fraud_detector_model/components/models.py
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

class Models:
    def __init__(self):
        pass
    
    def get_model(self, model_name, params):
        """
        Returns a model with the given parameters.
        
        Args:
            model_name (str): Name of the model.
            params (dict): Parameters for the model.
        
        Returns:
            model: Configured model.
        """
        if model_name == 'xgboost':
            return self.get_xgboost_model(params)
        elif model_name == 'random_forest':
            return self.get_random_forest_model(params)
        else:
            raise ValueError(f"Model {model_name} is not supported.")
    
    def get_xgboost_model(self, params):
        """
        Returns an XGBoost model with the given parameters.
        
        Args:
            params (dict): Parameters for the XGBoost model.
        
        Returns:
            XGBClassifier: Configured XGBoost classifier.
        """
        return xgb.XGBClassifier(**params)

    def get_random_forest_model(self, params):
        """
        Returns a RandomForest model with the given parameters.
        
        Args:
            params (dict): Parameters for the RandomForest model.
        
        Returns:
            RandomForestClassifier: Configured RandomForest classifier.
        """
        return RandomForestClassifier(**params)

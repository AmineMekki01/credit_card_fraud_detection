# src/components/trainer.py
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score

class ModelTrainer:
    def __init__(self, model, X, y, v_columns_to_keep, test_size=0.2, random_state=42, ):
        """
        Initializes the ModelTrainer with the specified model and parameters.
        
        Args:
            model: The model to train.
            X (pd.DataFrame): Features.
            y (pd.Series): Target variable.
            test_size (float): Proportion of the dataset to include in the validation split. Default is 0.2.
            random_state (int): Random state for reproducibility. Default is 42.
        """
        self.model = model
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.X_train, self.X_valid, self.y_train, self.y_valid = train_test_split(X, y, test_size=test_size, random_state=random_state)
        self.trained_model = None
        self.v_columns_to_keep = v_columns_to_keep

    def train(self):
        """
        Trains the model and returns the trained model.
        
        Returns:
            model: Trained model.
        """
        self.trained_model = self.model
        self.trained_model.fit(self.X_train[self.v_columns_to_keep], self.y_train, 
                               eval_set=[(self.X_valid[self.v_columns_to_keep], self.y_valid)],
                               verbose=50)
        return self.trained_model

    def evaluate(self):
        """
        Evaluates the model and returns the evaluation metrics.
        
        Returns:
            dict: Evaluation metrics.
        """
        preds = self.trained_model.predict_proba(self.X_valid[self.v_columns_to_keep])[:, 1]
        auc_score = roc_auc_score(self.y_valid, preds)
        accuracy = accuracy_score(self.y_valid, preds > 0.5)
        
        metrics = {
            'auc_score': auc_score,
            'accuracy': accuracy
        }
        return metrics

# main.py
from pathlib import Path
from sklearn.model_selection import train_test_split

from src import logger
from src.pipelines.data_processing_pipeline import DataProcessingPipeline
from src.pipelines.feature_engineering_pipeline import FeatureEngineeringPipeline
from src.pipelines.training_pipeline import TrainingPipeline

STAGE_NAME1 = "Data Processing"
STAGE_NAME2 = "Feature Engineering"
STAGE_NAME3 = "Model Training"

if __name__ == "__main__":
    try:
        logger.info(f">>>>> Stage {STAGE_NAME1} started <<<<<")
        data_processor = DataProcessingPipeline()
        X_train, y_train, v_columns_to_keep = data_processor.run()
        logger.info(f">>>>> Stage {STAGE_NAME1} completed. <<<<< \n")
    except Exception as e:
        logger.exception(e)
        raise e

    try:
        logger.info(f">>>>> Stage {STAGE_NAME2} started <<<<<")
        feature_engineer = FeatureEngineeringPipeline()
        X_train_processed = feature_engineer.run(X_train)
        logger.info(f">>>>> Stage {STAGE_NAME2} completed. <<<<< \n")
    except Exception as e:
        logger.exception(e)
        raise e

    try:
        logger.info(f">>>>> Stage {STAGE_NAME3} started <<<<<")
        trainer = TrainingPipeline()
        trained_model, metrics = trainer.run(X_train_processed, y_train, 'xgboost', v_columns_to_keep=v_columns_to_keep)
        logger.info(f"Metrics: {metrics}")
        logger.info(f">>>>> Stage {STAGE_NAME3} completed. <<<<< \n")
    except Exception as e:
        logger.exception(e)
        raise e

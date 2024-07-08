# cc_fraud_detector/utils/common_functions.py

from pathlib import Path
import yaml
from box.exceptions import BoxValueError
from box import ConfigBox
from ensure import ensure_annotations

import os 
from cc_fraud_detector_model.src import logger


@ensure_annotations
def read_yaml(path_to_yaml : Path) -> ConfigBox:
    """
    This function reads a yaml file and returns a ConfigBox object. 

    Parameters
    ----------
    path_to_yaml : Path
        path to yaml file.

    Raises:
        ValueError: if yaml file is empty.
        e: if any other error occurs.
    
    Returns:
    -------
        ConfigBox : ConfigBox object.
    """
    try: 
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Yaml file : {os.path.normpath(path_to_yaml)} loaded successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty.")
    except Exception as e:
        raise e  

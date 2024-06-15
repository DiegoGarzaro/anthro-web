import os
import json
from pydantic import BaseModel
from typing import List
from logger import Logger

class VirtualEnvironment(BaseModel):
    weight_for_age: dict
    length_for_age: dict
    weight_for_length: dict
    bmi_for_age: dict
    head_circumference_for_age: dict
    arm_circumference_for_age: dict
    subscapular_skinfold_for_age: dict
    triceps_skinfold_for_age: dict
    weight_velocity: dict
    length_velocity: dict
    head_circumference_velocity: dict

def load_virtual_environment(logger: Logger, config_file: str = 'config.json') -> VirtualEnvironment:
    """
    Loads environment variables from a JSON file into the application's environment.

    Args:
        logger (Logger): Logger instance for logging.
        config_file (str): Path to the JSON config file. Defaults to 'config.json'.
    
    Returns:
        VirtualEnvironment: Object containing loaded environment variables.
    """
    logger.info(f"Loading environment variables from {config_file}")

    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the configuration file {config_file}.")
        raise

    required_keys = [
        'weight-for-age', 'length-for-age', 'weight-for-length', 'bmi-for-age',
        'head-circumference-for-age', 'arm-circumference-for-age', 'subscapular-skinfold-for-age',
        'triceps-skinfold-for-age', 'weight-velocity', 'length-velocity', 'head-circumference-velocity'
    ]
    
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        logger.error(f"The following keys are missing in the config file: {', '.join(missing_keys)}")
        raise ValueError("Some keys are missing in the config file. Please check the config file.")
    
    virtual_env = VirtualEnvironment(
        weight_for_age=config.get('weight-for-age', {}),
        length_for_age=config.get('length-for-age', {}),
        weight_for_length=config.get('weight-for-length', {}),
        bmi_for_age=config.get('bmi-for-age', {}),
        head_circumference_for_age=config.get('head-circumference-for-age', {}),
        arm_circumference_for_age=config.get('arm-circumference-for-age', {}),
        subscapular_skinfold_for_age=config.get('subscapular-skinfold-for-age', {}),
        triceps_skinfold_for_age=config.get('triceps-skinfold-for-age', {}),
        weight_velocity=config.get('weight-velocity', {}),
        length_velocity=config.get('length-velocity', {}),
        head_circumference_velocity=config.get('head-circumference-velocity', {})
    )
    
    logger.info("Environment variables loaded successfully")
    return virtual_env

if __name__ == "__main__":
    logger = Logger()
    env = load_virtual_environment(logger, '..\\..\\config.json')
    print(env.weight_for_age["boys"]["z-score-birth-to-5-years"])

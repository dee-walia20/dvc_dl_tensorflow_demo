from src.utils.all_utils import read_yaml, create_directory
import argparse
import os
import logging
import joblib
from src.utils.models import load_full_model
from src.utils.callbacks import get_callbacks
from src.utils.data_management import train_valid_generator


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir,"running_logs.log"), level=logging.INFO, format=logging_str, filemode='a')

def train_model(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts = config["artifacts"]
    artifacts_dir = artifacts["ARTIFACTS_DIR"]

    train_model_dir_path = os.path.join(artifacts_dir, artifacts["TRAINED_MODEL_DIR"])
    create_directory([train_model_dir_path])

    untrained_full_model_path = os.path.join(artifacts_dir, artifacts["BASE_MODEL_DIR"], artifacts["UPDATED_BASE_MODEL_NAME"])

    model = load_full_model(untrained_full_model_path)

    callback_dir_path = os.path.join(artifacts_dir, artifacts["CALLBACKS_DIR"])
    callbacks = get_callbacks(callback_dir_path)

    train_generator, valid_generator = train_valid_generator(
        data_dir =artifacts["DATA_DIR"], 
        IMAGE_SIZE=tuple(params["INPUT_SIZE"][:-1]),
        BATCH_SIZE=params["BATCH_SIZE"],
        do_data_augmentation=params["AUGMENTATION"]
    )




if __name__ == "__main__":
    args =  argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    try:
        logging.info(">>>> stage four started")
        train_model(config_path=parsed_args.config, params_path= parsed_args.params)
        logging.info("stage four completed training is done <<<< \n\n")
    except Exception as e:
        logging.exception(e)
        raise e

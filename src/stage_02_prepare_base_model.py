from src.utils.all_utils import read_yaml, create_directory
from src.utils.models import get_VGG_16_model, prepare_model
import argparse
import os
import io
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir,"running_logs.log"), level=logging.INFO, format=logging_str, filemode='a')

def prepare_base_model(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    
    artifacts = config["artifacts"]
    artifacts_dir = artifacts["ARTIFACTS_DIR"]

    base_model_dir = artifacts["BASE_MODEL_DIR"]
    base_model_name = artifacts["BASE_MODEL_NAME"]

    base_model_dir_path = os.path.join(artifacts_dir, base_model_dir)
    create_directory([base_model_dir_path])

    base_model_path = os.path.join(base_model_dir_path, base_model_name)
    model = get_VGG_16_model(input_shape=params["INPUT_SIZE"], model_path= base_model_path)

    full_model = prepare_model(
        model,
        CLASSES=params["CLASSES"],
        freeze_all=True,
        freeze_till=None,
        learning_rate=params["LEARNING_RATE"]
    )
    
    updated_base_model_path = os.path.join(
        base_model_dir_path,
        artifacts["UPDATED_BASE_MODEL_NAME"]
    )

    def _log_model_summary(model):
        with io.StringIO() as stream:
            model.summary(print_fn=lambda x: stream.write(f"{x}\n"))
            summary_str=stream.getvalue()
        return summary_str
    
    logging.info(f"full model summary: \n{_log_model_summary(full_model)}")
    full_model.save(updated_base_model_path)      

    

if __name__ == "__main__":
    args =  argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    try:
        logging.info(">>>> stage two started")
        prepare_base_model(config_path=parsed_args.config, params_path= parsed_args.params)
        logging.info("stage two completed base model is created <<<<")
    except Exception as e:
        logging.exception(e)
        raise e

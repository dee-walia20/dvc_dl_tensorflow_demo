from src.utils.all_utils import read_yaml, create_directory
import argparse
import pandas as pd
import os
import shutil
from tqdm import tqdm
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(logs_dir,"running_logs.log"), level=logging.INFO, format=logging_str, filemode='a')

def copy_file(source_download_dir, local_data_dir):
    list_of_files = os.listdir(source_download_dir)
    N = len(list_of_files)
    for file in tqdm(list_of_files, total=N, colour="green", desc= f"copying files from {source_download_dir} to {local_data_dir}"):
        src = os.path.join(source_download_dir, file)
        dest = os.path.join(local_data_dir, file)
        shutil.copy(src, dest)

def get_data(config_path):
    config = read_yaml(config_path)
    
    source_download_dirs = config["source_download_dirs"]
    local_data_dirs = config["local_data_dirs"]

    for source_download_dir, local_data_dir in tqdm(zip(source_download_dirs, local_data_dirs), colour='red', total=2, desc= "list of folders"):
        create_directory([local_data_dir])
        copy_file(source_download_dir, local_data_dir)
    

if __name__ == "__main__":
    args =  argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    try:
        logging.info(">>>> stage one started")
        get_data(config_path=parsed_args.config)
        logging.info("stage one completed all data are saved in local <<<<")
    except Exception as e:
        logging.exception(e)
        raise e

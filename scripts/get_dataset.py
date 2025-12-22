from pathlib import Path

from src.configuraciones.config_params import conf, logger
from src.datos.descarga_dataset import DatasetDownloader

#from src.data.download_dataset import DatasetDownloader
#from src.utils.paths import paths

if __name__ == "__main__":
    dataset_id = conf["download"]["dataset_id"]
    raw_file = conf["data"]["raw_data_file"]
    downloader = DatasetDownloader(dataset_id, raw_file)
    
    downloader.run()
    logger.info("Dataset descargado correctamente")


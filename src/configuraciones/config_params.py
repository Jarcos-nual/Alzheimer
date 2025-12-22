from omegaconf import OmegaConf
from loguru import logger
import sys

# Carga de Configuración
try:
    conf_params = OmegaConf.load("config/params.yaml")
    conf_logging = OmegaConf.load("config/logging.yaml")
except FileNotFoundError as e:
    logger.error(f"Archivo de configuración no encontrado: {e}")
    sys.exit(1)

# Fusionar configuraciones en un solo objeto
conf = OmegaConf.merge(conf_params, conf_logging)

# Resolver interpolaciones (ej. ${var})
conf = OmegaConf.to_container(conf, resolve=True)

# Configurar logger según YAML
if "logging" in conf:
    sinks = conf["logging"].get("sinks", [])
    logger.remove()  # elimina configuración por defecto

    for sink in sinks:
        if sink["type"] == "stderr":
            logger.add(
                sys.stderr,
                level=sink.get("level", "INFO"),
                colorize=sink.get("colorize", True),
                format=sink.get("format"),
                enqueue=sink.get("enqueue", True),
                backtrace=sink.get("backtrace", True),
                diagnose=sink.get("diagnose", False),
            )
        elif sink["type"] == "file":
            logger.add(
                sink.get("path", "./logs/app.log"),
                level=sink.get("level", "DEBUG"),
                colorize=sink.get("colorize", False),
                format=sink.get("format"),
                rotation=sink.get("rotation", "00:00"),
                retention=sink.get("retention", "7 days"),
                compression=sink.get("compression", "zip"),
                enqueue=sink.get("enqueue", True),
                backtrace=sink.get("backtrace", True),
                diagnose=sink.get("diagnose", False),
            )

    logger.info("Logger inicializado con configuración desde logging.yaml")

# Ejemplo de uso: accede a claves que sí existen
#logger.debug(f"Ruta de datos RAW: {conf['paths']['raw']}")
#logger.debug(f"Dataset ID: {conf['download']['dataset_id']}")
#logger.debug(f"Autor: {conf['metadata']['author']}")
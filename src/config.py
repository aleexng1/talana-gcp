import os
from dotenv import load_dotenv
import logging

# Cargar variables de entorno desde archivo .env (solo en entorno local)
load_dotenv()

# --- TALANA API ---
TALANA_USERNAME = os.getenv("TALANA_USERNAME")
TALANA_PASSWORD = os.getenv("TALANA_PASSWORD")

# --- GCP / BigQuery / GCS ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

# Detectar si estamos en un entorno local o en GCP
IS_LOCAL = os.getenv("ENVIRONMENT") == "local"

# Cargar credenciales solo si estamos en local
if IS_LOCAL:
    load_dotenv()
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
else:
    # En GCP no necesitas asignar manualmente la variable
    GOOGLE_APPLICATION_CREDENTIALS = None

# --- Logging ---
def get_logger(name="talana-gcp", level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger

logger = get_logger()

import json
from google.cloud import storage

from config import GCP_PROJECT_ID, logger
from utils.sanitize import remove_user_defined_fields


def write_to_ndjson(data: list, filename: str) -> None:
    """
    Escribe una lista de diccionarios en un archivo NDJSON.

    Args:
        data (list): Lista de registros (dict) a guardar.
        filename (str): Nombre del archivo destino.
    """
    logger.info(f"Escribiendo datos en archivo NDJSON: {filename}")
    with open(filename, "w", encoding="utf-8") as json_file:
        for item in data:
            remove_user_defined_fields(item)
            json.dump(item, json_file, ensure_ascii=False)
            json_file.write("\n")
    logger.info(f"Archivo generado exitosamente: {filename}")


def upload_to_gcs(local_filename: str, bucket_name: str, remote_filename: str) -> None:
    """
    Sube un archivo local a un bucket de GCS.

    Args:
        local_filename (str): Ruta local al archivo.
        bucket_name (str): Nombre del bucket en GCS.
        remote_filename (str): Nombre del archivo destino en el bucket.
    """
    logger.info(f"Subiendo archivo a GCS: {remote_filename}")
    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_filename)
    blob.upload_from_filename(local_filename)
    logger.info(f"Archivo '{remote_filename}' subido correctamente a '{bucket_name}'")

from config import TALANA_USERNAME, TALANA_PASSWORD, GCP_BUCKET_NAME, logger
from utils.auth import get_auth_token
from utils.fetch import fetch_data
from utils.storage import write_to_ndjson, upload_to_gcs
from utils.dates import get_last_month


def process_data(url: str, output_filename: str, remote_filename: str):
    """
    Procesa un endpoint: obtiene los datos, guarda como NDJSON y sube a GCS.

    Args:
        url (str): URL del endpoint Talana.
        output_filename (str): Nombre del archivo local temporal.
        remote_filename (str): Nombre del archivo en GCS.
    """
    logger.info(f"Procesando endpoint: {url}")
    token = get_auth_token(TALANA_USERNAME, TALANA_PASSWORD)
    if not token:
        logger.error("No se pudo obtener el token de autenticación.")
        return

    data = fetch_data(url, token)
    if not data:
        logger.warning("No se obtuvo información desde el endpoint.")
        return

    write_to_ndjson(data, output_filename)
    upload_to_gcs(output_filename, GCP_BUCKET_NAME, remote_filename)
    logger.info(f"Finalizado: {remote_filename}")


def main(data=None, context=None):
    """
    Función principal para obtener las liquidaciones del mes anterior.
    """
    last_year, last_month = get_last_month()

    endpoint = f"https://talana.com/es/api/liquidaciones/?periodo__mes={last_month}&periodo__ano={last_year}"
    output_filename = "liquidaciones_output.ndjson"
    remote_filename = "Liquidaciones.ndjson"

    try:
        process_data(endpoint, output_filename, remote_filename)
    except Exception as e:
        logger.error(f"Error procesando liquidaciones: {e}")

    logger.info("Liquidaciones procesadas correctamente.")


def procesar():
    """
    Función de entrada para ejecución desde `main.py`.
    """
    logger.info("=== Ejecutando talana_liquidaciones.procesar() ===")
    main()

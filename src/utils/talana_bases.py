from src.config import TALANA_USERNAME, TALANA_PASSWORD, GCP_BUCKET_NAME, logger
from src.utils.auth import get_auth_token
from src.utils.fetch import fetch_data
from src.utils.storage import write_to_ndjson, upload_to_gcs
from src.utils.dates import get_yesterday_date, get_last_month


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
    Función principal que define y ejecuta los endpoints de bases (catálogos).
    """
    yesterday = get_yesterday_date()
    last_year, last_month = get_last_month()

    endpoints = [
        ("https://talana.com/es/api/workShiftPersonRange/", "workShiftPersonRange_output.ndjson", "AsignacionTurnos.ndjson"),
        ("https://talana.com/es/api/tipoAusencia/", "tipoAusencia_output.ndjson", "TipoAusencia.ndjson"),
        ("https://talana.com/es/api/job-title/", "job_titles_output.ndjson", "Cargos.ndjson"),
        ("https://talana.com/es/api/centroCosto/", "centroCosto_output.ndjson", "CentroCosto.ndjson"),
        ("https://talana.com/es/api/tipoContrato/", "tipoContrato_output.ndjson", "TipoContrato.ndjson"),
        ("https://talana.com/es/api/cuentaContable/", "cuentaContable_output.ndjson", "CuentaContable.ndjson"),
        ("https://talana.com/es/api/formas-de-pago", "formapago_output.ndjson", "FormaPago.ndjson"),
        ("https://talana.com/es/api/unidadOrganizacional/", "unidadOrganizacional_output.ndjson", "UnidadOrganizacional.ndjson"),
        ("https://talana.com/es/api/afp", "AFP_output.ndjson", "AFP.ndjson"),
        ("https://talana.com/es/api/institucionAPV/", "institucionAPV_output.ndjson", "APV.ndjson"),
        ("https://talana.com/es/api/banco/", "banco_output.ndjson", "Banco.ndjson"),
        ("https://talana.com/es/api/cajaCompensacion/", "cajaCompensacion_output.ndjson", "CajaCompensacion.ndjson"),
        ("https://talana.com/es/api/mutualSeguridad/", "mutualSeguridad_output.ndjson", "MutualSeguridad.ndjson"),
        ("https://talana.com/es/api/prevision/", "prevision_output.ndjson", "Prevision.ndjson"),
        ("https://talana.com/es/api/jornadaLaboral/", "jornadaLaboral_output.ndjson", "JornadaLaboral.ndjson"),
        ("https://talana.com/es/api/pais/", "pais_output.ndjson", "Pais.ndjson"),
        ("https://talana.com/es/api/razonSocial/", "razon_social_output.ndjson", "RazonSocial.ndjson"),
        ("https://talana.com/es/api/sucursal/", "sucursal_output.ndjson", "Sucursal.ndjson"),
        ("https://talana.com/es/api/ubicacionGeografica/", "ubicacionGeografica_output.ndjson", "UbicacionGeografica.ndjson"),
        ("https://talana.com/es/api/specificDay/", "specificDay_output.ndjson", "TurnosManuales.ndjson"),
        ("https://talana.com/es/api/rotativeDay", "rotary_output.ndjson", "TurnosRotativos.ndjson"),
        ("https://talana.com/es/api/workShift/", "work_shift_output.ndjson", "Turnos.ndjson"),
        ("https://talana.com/es/api/enrolments", "enrolamiento_output.ndjson", "Enrolamiento.ndjson"),
        ("https://talana.com/es/api/persona", "personas_output.ndjson", "Personas.ndjson")
    ]

    for url, output_filename, remote_filename in endpoints:
        try:
            process_data(url, output_filename, remote_filename)
        except Exception as e:
            logger.error(f"Error procesando {url}: {e}")

    logger.info("Todos los endpoints de bases han sido procesados.")


def procesar():
    """
    Función de entrada para integración con `main.py`.
    """
    logger.info("=== Ejecutando talana_bases.procesar() ===")
    main()

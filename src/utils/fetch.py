import time

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config import logger


def get_session_with_retries() -> requests.Session:
    """
    Crea una sesión de requests con lógica de reintentos configurada.

    Returns:
        requests.Session: Sesión lista para hacer peticiones con retry.
    """
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session


def fetch_data(url: str, token: str) -> list:
    """
    Obtiene datos paginados desde una URL utilizando token de Talana.

    Args:
        url (str): URL base del endpoint.
        token (str): Token de autenticación.

    Returns:
        list: Lista de todos los registros obtenidos.
    """
    results = []
    session = get_session_with_retries()

    while url:
        intentos_429 = 0
        while intentos_429 < 3:
            try:
                logger.info(f"Obteniendo datos desde: {url}")
                response = session.get(
                    url,
                    headers={"Authorization": f"Token {token}"},
                    timeout=500  # Aumentado para endpoints pesados
                )

                # Manejo explícito de Rate Limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"HTTP 429 detectado. Esperando {retry_after}s antes de reintentar (Intento {intentos_429 + 1}/3)...")
                    time.sleep(retry_after)
                    intentos_429 += 1
                    continue

                response.raise_for_status()
                data = response.json()

                # Extracción de datos
                if isinstance(data, list):
                    results.extend(data)
                    url = None
                elif 'results' in data:
                    results.extend(data.get('results', []))
                    url = data.get('next')
                else:
                    logger.warning(f"Estructura de datos inesperada desde {url}. Respuesta parcial: {str(data)[:500]}")
                    url = None

                # Pausa obligatoria entre páginas (Throttle)
                time.sleep(1.0)
                break  # Salir del bucle de reintentos 429 y pasar a la siguiente página

            except requests.RequestException as e:
                logger.error(f"Error fatal al obtener datos desde {url}: {e}")
                raise e
        else:
            # Si agota los 3 reintentos de 429
            logger.error(f"Se agotaron los reintentos para manejar el error 429 en {url}")
            raise requests.exceptions.HTTPError("Max retries for HTTP 429 reached.", response=response)

    logger.info(f"Total de registros obtenidos: {len(results)}")
    return results

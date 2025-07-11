import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from src.config import logger

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
        try:
            logger.info(f"Obteniendo datos desde: {url}")
            response = session.get(url, headers={"Authorization": f"Token {token}"}, timeout=60)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                results.extend(data)
                break
            else:
                results.extend(data.get('results', []))
                url = data.get('next')

        except requests.RequestException as e:
            logger.error(f"Error al obtener datos desde {url}: {e}")
            break

    logger.info(f"Total de registros obtenidos: {len(results)}")
    return results

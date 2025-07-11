from src.utils.fetch import get_session_with_retries
from src.config import logger

import requests

def get_auth_token(username: str, password: str) -> str | None:
    """
    Obtiene el token de autenticación desde la API de Talana.
    
    Args:
        username (str): Usuario Talana.
        password (str): Contraseña Talana.
    
    Returns:
        str | None: Token de autenticación o None si falla.
    """
    url = "https://talana.com/es/api/api-token-auth/"
    session = get_session_with_retries()
    
    try:
        logger.info(f"Solicitando token de autenticación desde {url}")
        response = session.post(url, json={"username": username, "password": password}, timeout=30)
        response.raise_for_status()
        logger.info("Token obtenido correctamente")
        return response.json().get("token")
    
    except requests.RequestException as e:
        logger.error(f"Error al obtener token: {e}")
        return None

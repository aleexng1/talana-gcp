import re
import unicodedata

from config import logger


def sanitize_field_name(name: str) -> str:
    """
    Sanitiza un nombre de campo para que cumpla con las reglas de Google Cloud.
    
    Reemplaza caracteres especiales, acentos, y asegura que el campo no comience con número.

    Args:
        name (str): Nombre original del campo.

    Returns:
        str: Nombre sanitizado.
    """
    name = unicodedata.normalize('NFC', name)
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = name.replace("ñ", "n")

    name = re.sub(r'[^\w]', '_', name)

    if name and name[0].isdigit():
        name = '_' + name

    return name[:300]


def rename_duplicate_sueldo_mensual(data: dict):
    """
    Renombra el campo 'Sueldo Mensual' si está duplicado para evitar conflictos de claves.
    
    Args:
        data (dict): Diccionario a analizar y modificar.
    """
    if isinstance(data, dict):
        lower_case_keys = {k.lower(): k for k in data.keys()}
        if 'sueldo mensual' in lower_case_keys:
            original_key = lower_case_keys['sueldo mensual']
            new_key = 'Sueldo_mensual_duplicated'
            while new_key in data:
                new_key += '_1'
            data[new_key] = data.pop(original_key)
        for key, value in data.items():
            rename_duplicate_sueldo_mensual(value)


def remove_user_defined_fields(data):
    """
    Elimina campos personalizados y aplica sanitización recursiva a los nombres de campo.

    Args:
        data (dict or list): Estructura de datos a procesar.
    """
    if isinstance(data, dict):
        data.pop("user_defined_fields", None)
        rename_duplicate_sueldo_mensual(data)
        keys_to_update = list(data.keys())

        for key in keys_to_update:
            new_key = sanitize_field_name(key)
            if new_key != key:
                data[new_key] = data.pop(key)
            remove_user_defined_fields(data[new_key])

    elif isinstance(data, list):
        for item in data:
            remove_user_defined_fields(item)

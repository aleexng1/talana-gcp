from datetime import datetime, timedelta


def get_yesterday_date() -> str:
    """
    Retorna la fecha de ayer en formato YYYY-MM-DD.

    Returns:
        str: Fecha de ayer (ej: '2025-07-10').
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_last_month() -> tuple[str, str]:
    """
    Retorna el año y mes anterior al actual.

    Returns:
        tuple[str, str]: Año y mes anteriores (ej: ('2025', '06')).
    """
    today = datetime.today()
    first_day = today.replace(day=1)
    last_month = first_day - timedelta(days=1)
    return last_month.strftime('%Y'), last_month.strftime('%m')

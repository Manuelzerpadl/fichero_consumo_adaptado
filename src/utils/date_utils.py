from datetime import datetime
import pandas as pd


def get_formatted_date(date_type: str, fmt: str, custom_value: str = "") -> str:
    """
    Devuelve una fecha formateada según la configuración.

    Args:
        date_type: Tipo de fecha (ej. "last_day_current_month").
        fmt: Formato de fecha en notación estilo Excel (DD/MM/YYYY).
        custom_value: Valor personalizado (si aplica).

    Returns:
        str con la fecha formateada.
    """
    today = datetime.today()

    if date_type == "last_day_current_month":
        next_month = today.replace(day=28) + pd.Timedelta(days=4)
        last_day = next_month - pd.Timedelta(days=next_month.day)
        date_value = last_day
    elif date_type == "today":
        date_value = today
    elif date_type == "custom" and custom_value:
        return custom_value
    else:
        date_value = today

    # Mapear tokens de estilo Excel a formato strftime de Python
    format_map = {
        "DD": "%d",
        "MM": "%m",
        "YYYY": "%Y",
        "YY": "%y"
    }
    for token, py_fmt in format_map.items():
        fmt = fmt.replace(token, py_fmt)

    return date_value.strftime(fmt)
from pathlib import Path
from datetime import datetime


def get_dated_folder(base_dir: str, date: datetime | None = None) -> Path:
    """
    Devuelve una carpeta basada en año/mes de la fecha dada (o la fecha actual si es None).
    Crea la carpeta si no existe.
    
    Ejemplo:
        base_dir="data/input", fecha=2025-09-10 → data/input/2025/09
    """
    date = date or datetime.today()
    year = str(date.year)
    month = f"{date.month:02d}"
    folder = Path(base_dir) / year / month
    folder.mkdir(parents=True, exist_ok=True)
    return folder

import json
import os
from typing import List
from pathlib import Path


def load_company_ids() -> List[str]:
    """
    Carga los company_ids desde config/company_ids.json (fuera de src).
    Si no existe el archivo, intenta leerlos de la variable de entorno COMPANY_IDS.
    Valida que el contenido sea una lista de strings.
    """
    base_dir = Path(__file__).resolve().parents[2]  # subimos 2 niveles desde utils/
    config_path = base_dir / "config" / "company_ids.json"

    if config_path.exists():
        data = json.loads(config_path.read_text(encoding="utf-8"))
        companies = data.get("companies", [])

        if not isinstance(companies, list) or not all(isinstance(c, str) for c in companies):
            raise ValueError(
                f"Formato inválido en {config_path}: se esperaba una lista de strings en 'companies'."
            )
        return companies

    env_value = os.getenv("COMPANY_IDS", "")
    if env_value:
        return [cid.strip() for cid in env_value.split(",") if cid.strip()]

    return []

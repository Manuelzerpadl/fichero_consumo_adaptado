import json
import os
from typing import List
from pathlib import Path


def load_company_ids(path="config/company_ids.json"):
    import json
    from pathlib import Path

    with open(Path(path), encoding="utf-8") as f:
        data = json.load(f)

    companies = data.get("companies")
    if not isinstance(companies, list):
        raise ValueError(f"Formato inválido en {path}: 'companies' debe ser una lista")

    # Detectar si son objetos o strings
    if all(isinstance(c, dict) and "id" in c for c in companies):
        return [c["id"] for c in companies]
    elif all(isinstance(c, str) for c in companies):
        return companies
    else:
        raise ValueError(f"Formato inválido en {path}: se esperaba lista de strings o de objetos con 'id'")

def get_config_for_file(input_file, companies):
    """Dado un input_file, detecta el CIF y devuelve el config_path."""
    filename = Path(input_file).name
    for company in companies:
        if company["cif"] in filename:
            return company["config_path"]
    raise ValueError(f"No se encontró configuración para el fichero: {filename}")

def load_company_configs(path="config/company_ids.json"):
    """Devuelve la metadata completa (cif, config_path, etc.) para el transformer/pipeline."""
    with open(Path(path), encoding="utf-8") as f:
        data = json.load(f)

    companies = data.get("companies")
    if not isinstance(companies, list):
        raise ValueError(f"Formato inválido en {path}: 'companies' debe ser una lista")

    if all(isinstance(c, dict) and "id" in c for c in companies):
        return companies
    else:
        raise ValueError(
            f"Formato inválido en {path}: se esperaba lista de objetos con 'id'"
        )
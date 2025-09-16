import pandas as pd
from pathlib import Path
import json
from typing import Dict, Any


def load_config_excel(config_file: str) -> Dict[str, Any]:
    """
    Lee un Excel de configuración y devuelve un dict JSON-ready
    con info básica, mappings y output_config.
    """
    path = Path(config_file)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {config_file}")

    # 1) Información básica
    basic_df = pd.read_excel(path, sheet_name="2. Información Básica").fillna("")
    basic_info = dict(zip(basic_df["Campo"], basic_df["Valor"]))

    # 🔎 Validar que incluya ID empresa
    if "ID empresa" not in basic_info:
        raise ValueError(
            f"❌ El archivo {config_file} no contiene 'ID empresa' en la hoja '2. Información Básica'"
        )

    # 2) Mapeo de columnas
    mappings_df = pd.read_excel(path, sheet_name="3. Columnas y Mapeo").fillna("")

    # Validación de columnas mínimas requeridas
    required_cols = {"Columna del CSV Original", "Columna de Salida"}
    missing = required_cols - set(mappings_df.columns)
    if missing:
        raise ValueError(
            f"❌ Faltan columnas obligatorias en la hoja '3. Columnas y Mapeo': {missing}"
        )

    mappings = mappings_df.to_dict(orient="records")

    # 3) Configuración de salida
    output_df = pd.read_excel(path, sheet_name="4. Config Excel y Fecha").fillna("")
    output_config = dict(zip(output_df["Configuración"], output_df["Valor"]))

    return {
        "basic_info": basic_info,
        "mappings": mappings,
        "output_config": output_config,
    }

def export_config_to_json(config_file: str, json_file: str) -> None:
    """
    Convierte un Excel de configuración en un JSON estandarizado.
    """
    config = load_config_excel(config_file)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

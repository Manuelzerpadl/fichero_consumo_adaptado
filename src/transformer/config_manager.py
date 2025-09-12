import json
from pathlib import Path
from typing import Dict, Any

from transformer.config_loader import load_config_excel
from transformer.config_schema import ConfigSchema


def load_company_config(config_base: str) -> Dict[str, Any]:
    """
    Carga la configuración de una empresa.
    - Si existe el JSON, se usa directamente.
    - Si no existe el JSON pero existe el Excel, se genera y valida.
    - Si no existe ninguno, error.
    
    Args:
        config_base: ruta base del archivo sin extensión, 
                     ej: "data/config/fhecor" (sin .xlsx ni .json)

    Returns:
        dict con la configuración validada
    """
    json_path = Path(f"{config_base}.json")
    excel_path = Path(f"{config_base}.xlsx")

    # 1) Si ya existe el JSON → usarlo
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            config = json.load(f)
        ConfigSchema(**config)  # valida
        return config

    # 2) Si no existe JSON pero sí Excel → generar y validar
    if excel_path.exists():
        config = load_config_excel(str(excel_path))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        ConfigSchema(**config)  # valida
        return config

    # 3) Si no existe ninguno → error
    raise FileNotFoundError(
        f"No se encontró ni {json_path} ni {excel_path}. "
        "Debes proporcionar al menos uno."
    )

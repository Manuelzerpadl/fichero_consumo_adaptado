from pathlib import Path
import json
from typing import Union
from transformer.config_schema import BasicInfo


def update_companies_registry(
    config_path: Path,
    config: dict,
    registry_path: Path = Path("config/company_ids.json"),
) -> None:
    """
    Añade o actualiza la empresa en el JSON maestro de company_ids.json.
    Soporta tanto dicts como objetos BasicInfo.
    """
    basic_info: Union[dict, BasicInfo] = config.get("basic_info", {})

    # 🔎 Si viene como BasicInfo -> usar atributos pythonicos (ya normalizados)
    if isinstance(basic_info, BasicInfo):
        company_entry = {
            "id": basic_info.id_empresa,
            "cif": basic_info.cif,
            "name": basic_info.empresa,
            "config_path": str(config_path),
            "input_pattern": f"data/input/{basic_info.cif}_*.csv",
            "emails": basic_info.correos,  # ✅ ya es lista
        }
    elif isinstance(basic_info, dict):
        # fallback si aún viene como dict sin normalizar
        emails = basic_info.get("Correos", [])
        if isinstance(emails, str):
            emails = [e.strip() for e in emails.split(";") if e.strip()]
        company_entry = {
            "id": basic_info["ID empresa"],
            "cif": basic_info["CIF de la empresa"],
            "name": basic_info["Nombre completo de la empresa"],
            "config_path": str(config_path),
            "input_pattern": f"data/input/{basic_info['CIF de la empresa']}_*.csv",
            "emails": emails,
        }
    else:
        raise ValueError(f"❌ basic_info inválido en {config_path}")

    # 1) Crear el JSON si no existe
    if not registry_path.exists():
        registry = {"companies": []}
    else:
        with open(registry_path, encoding="utf-8") as f:
            try:
                registry = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ {registry_path} corrupto, regenerando...")
                registry = {"companies": []}

    # 2) Asegurar que companies es lista
    if not isinstance(registry.get("companies"), list):
        registry["companies"] = []

    # 3) Actualizar o añadir
    updated = False
    for c in registry["companies"]:
        if c.get("id") == company_entry["id"]:
            c.update(company_entry)
            updated = True
            break

    if not updated:
        registry["companies"].append(company_entry)

    # 4) Guardar
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"✅ company_ids.json actualizado con {company_entry['name']} ({company_entry['cif']})")


def load_companies_registry(registry_path: Path = Path("config/company_ids.json")) -> dict:
    """Carga el JSON maestro con todas las empresas."""
    if not registry_path.exists():
        return {"companies": []}
    with open(registry_path, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ {registry_path} corrupto, devolviendo vacío")
            return {"companies": []}
    if not isinstance(data.get("companies"), list):
        data["companies"] = []
    return data

import json
from pathlib import Path

from transformer.config_loader import load_config_excel
from utils.companies_registry import update_companies_registry
from transformer.config_schema import ConfigSchema


def main() -> None:
    config_file = Path("data/config/fhecor_config_v2.xlsx")
    json_file = config_file.with_suffix(".json")

    # 1) Cargar Excel
    config = load_config_excel(str(config_file))

    # 2) Exportar a JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Configuración exportada a {json_file}")

    # 3) Validar JSON con Pydantic
    try:
        validated = ConfigSchema(**config)
        print("✅ Configuración validada correctamente con Pydantic")

        # 4) Actualizar el registry maestro de companies
        update_companies_registry(json_file, config)

    except Exception as e:
        print("❌ Error de validación en la configuración:")
        print(e)


if __name__ == "__main__":
    main()

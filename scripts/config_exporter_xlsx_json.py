import json
from pathlib import Path

from transformer.config_loader import load_config_excel
from transformer.config_schema import ConfigSchema


def main() -> None:
    config_file = Path("data/config/plantilla_empresa.xlsx")
    json_file = config_file.with_suffix(".json")

    # 1) Cargar Excel
    config = load_config_excel(str(config_file))

    # 2) Exportar a JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Configuración exportada a {json_file}")

    # 3) Validar JSON con Pydantic
    try:
        validated = ConfigSchema(**config)
        print("Configuración validada correctamente con Pydantic")
    except Exception as e:
        print("Error de validación en la configuración:")
        print(e)


if __name__ == "__main__":
    main()

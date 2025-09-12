import json
from transformer.config_loader import load_config_excel


def main() -> None:
    config_file = "data/config/fhecor_config.xlsx"

    # Cargar configuración desde Excel
    config = load_config_excel(config_file)

    print("=== Basic Info ===")
    print(json.dumps(config["basic_info"], indent=2, ensure_ascii=False))

    print("\n=== First 3 mappings ===")
    print(json.dumps(config["mappings"][:3], indent=2, ensure_ascii=False))

    print("\n=== Output Config ===")
    print(json.dumps(config["output_config"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

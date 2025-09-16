from pathlib import Path
import json
from transformer.a3_payroll_transformer import transform_payroll
from transformer.exporter import export_with_config


def main():
    # OJO: cambia estos paths por los tuyos reales
    input_file = "data/input/2025/09/2025-08-31T065203-ajustes-nomina-A78379518 (1).csv"
    config_json = "C:/Users/Manuel Zerpa/Desktop/fichero_consumo_adaptado/data/config/fhecor_config_v2.json"
    output_folder = Path("data/output")

    # 1) Cargar configuración
    with open(config_json, encoding="utf-8") as f:
        config = json.load(f)

    # 2) Transformar -> obtenemos DataFrame
    df_out = transform_payroll(input_file, config_json)

    # 3) Construir ruta de salida
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / f"{Path(input_file).stem}_transformed.xlsx"

    # 4) Exportar Excel con formato definido en config
    export_with_config(df_out, config, output_file)

    print(f"Archivo transformado en: {output_file}")


if __name__ == "__main__":
    main()

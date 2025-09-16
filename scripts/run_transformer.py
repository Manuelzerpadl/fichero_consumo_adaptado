from transformer.a3_payroll_transformer import transform_payroll
from transformer.exporter import export_with_config
from pathlib import Path
from datetime import datetime
import json


def main():
    input_file = "data/input/2025/09/2025-08-31T065203-ajustes-nomina-A78379518 (1).csv"
    config_json = "data/config/fhecor_config_v2.json"
    base_output = Path("data/output")

    # 1) Transformar
    df_out = transform_payroll(input_file, config_json)

    # 2) Cargar configuración
    with open(config_json, encoding="utf-8") as f:
        config = json.load(f)

    # 3) Construir carpeta de salida YYYY/MM
    now = datetime.today()
    out_dir = base_output / str(now.year) / f"{now.month:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 4) Definir nombre de archivo final
    out_format = config["output_config"].get("OUTPUT - Formato archivo", "xlsx").lower()
    output_file = out_dir / f"{Path(input_file).stem}_transformed.{out_format}"

    # 5) Exportar con configuración
    export_with_config(df_out, config, output_file)

    print(f"✅ Archivo transformado en: {output_file}")


if __name__ == "__main__":
    main()

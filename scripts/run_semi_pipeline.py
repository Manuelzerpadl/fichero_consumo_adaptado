from downloader.payroll_downloader import download_files
from transformer.a3_payroll_transformer import transform_payroll
from transformer.exporter import export_with_config
from utils.company_loader import load_company_configs, get_config_for_file
from pathlib import Path
from datetime import datetime
import json

def main():
    # 1) Cargar metadata empresas (con cif y config_path)
    companies = load_company_configs()

    # 2) Descargar ficheros
    downloaded_files = download_files()
    if not downloaded_files:
        print("⚠️ No se descargaron ficheros.")
        return
    
    for input_file in downloaded_files:
        print(f"Procesando {input_file}...")

        # 3) Detectar config automáticamente por CIF
        config_json = get_config_for_file(str(input_file), companies)

        # 4) Transformar (espera str)
        df_out = transform_payroll(str(input_file), str(config_json))

        # 5) Cargar configuración
        with open(str(config_json), encoding="utf-8") as f:
            config = json.load(f)

        # 6) Carpeta salida con Path (seguimos usando Path aquí)
        now = datetime.today()
        out_dir = Path("data/output") / str(now.year) / f"{now.month:02d}"
        out_dir.mkdir(parents=True, exist_ok=True)

        # 7) Nombre archivo final (Path sin problema)
        out_format = config["output_config"].get("OUTPUT - Formato archivo", "xlsx").lower()
        output_file = out_dir / f"{Path(input_file).stem}_transformed.{out_format}"

        # 8) Exportar (si espera str, casteamos)
        export_with_config(df_out, config, output_file)

        print(f"✅ Archivo transformado en: {output_file}")

if __name__ == "__main__":
    main()

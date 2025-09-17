from src.downloader.payroll_downloader import download_files
from src.transformer.a3_payroll_transformer import transform_payroll
from src.transformer.exporter import export_with_config
from src.utils.company_loader import load_company_configs, get_config_for_file
from src.utils.sendgrid_utils import send_with_sendgrid
from src.utils.logging_config import setup_logging
from config.settings import settings

from pathlib import Path
from datetime import datetime
import json


def main():
    logger = setup_logging()

    # 1) Cargar metadata empresas
    companies = load_company_configs()
    logger.info(f"Empresas cargadas: {len(companies)}")

    # 2) Descargar ficheros
    downloaded_files = download_files()
    if not downloaded_files:
        logger.warning("No se descargaron ficheros.")
        return
    
    for input_file in downloaded_files:
        logger.info(f"Procesando {input_file}...")

        # 3) Detectar config automáticamente por CIF
        config_json = get_config_for_file(str(input_file), companies)

        # 4) Transformar
        df_out = transform_payroll(str(input_file), str(config_json))

        # 5) Cargar configuración
        with open(str(config_json), encoding="utf-8") as f:
            config = json.load(f)

        # 6) Carpeta de salida YYYY/MM
        now = datetime.today()
        out_dir = Path("data/output") / str(now.year) / f"{now.month:02d}"
        out_dir.mkdir(parents=True, exist_ok=True)

        # 7) Nombre archivo final
        out_format = config["output_config"].get("OUTPUT - Formato archivo", "xlsx").lower()
        output_file = out_dir / f"{Path(input_file).stem}_transformed.{out_format}"

        # 8) Exportar
        export_with_config(df_out, config, output_file)
        logger.info(f"✅ Archivo transformado en: {output_file}")

        # 9) Buscar correos y enviar
        company = next(c for c in companies if c["cif"] in str(input_file))
        emails = company.get("emails", [])

        if emails:
            dynamic_data = {
                "company_name": company["name"],
                "cif": company["cif"],
                "month_year": now.strftime("%m/%Y"),
                "email-subject": f"Nómina transformada - {company['name']} ({company['cif']}) - {now.strftime('%m/%Y')}"
            }
            send_with_sendgrid(emails, output_file, dynamic_data)
            logger.info(f"📨 Archivo enviado a: {', '.join(emails)} usando plantilla {settings.TEMPLATE_ID_PAYROLLS}")
        else:
            logger.warning(f"No se encontraron emails para CIF {company['cif']}")


if __name__ == "__main__":
    main()

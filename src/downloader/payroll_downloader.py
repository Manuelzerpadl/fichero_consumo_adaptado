import logging
from pathlib import Path

from utils.company_loader import load_company_ids
from db.clickhouse_client import ClickHouseClient
from api.retool_client import RetoolClient
from utils.path_utils import get_dated_folder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main(base_dir: str = "data/input") -> None:
    logging.info("Iniciando payroll downloader...")

    # 1) Cargar company_ids
    company_ids = load_company_ids()
    if not company_ids:
        logging.warning("No se encontraron company_ids en config/company_ids.json ni en .env")
        return

    logging.info(f"Company IDs cargados: {company_ids}")

    # 2) Consultar en ClickHouse
    clickhouse_client = ClickHouseClient()
    documents_df = clickhouse_client.query_adjustment_documents_for_ids(company_ids)

    if documents_df.empty:
        logging.info("No se encontraron documentos de ajustes para descargar.")
        return

    logging.info(f"Se encontraron {len(documents_df)} documentos de ajustes.")

    # 3) Autenticarse en la API
    retool_client = RetoolClient(base_url="https://api.cobee.io/v1/back-office")
    retool_client.authenticate()

    # 4) Carpeta de salida basada en año/mes
    output_folder: Path = get_dated_folder(base_dir)

    for _, row in documents_df.iterrows():
        company_id: str = row["companyId"]
        document_id: str = row["documentId"]
        filename: str = row["filename"]

        logging.info(f"Descargando documento {document_id} para company {company_id}...")

        output_path = retool_client.download_payroll_adjustment(
            company_id=company_id,
            payroll_document_id=document_id,
            output_folder=str(output_folder),
            filename=filename,
        )

        if output_path:
            logging.info(f"Documento guardado en {output_path}")
        else:
            logging.error(f"Falló la descarga de {document_id} (company {company_id})")

    logging.info("Proceso completado.")


if __name__ == "__main__":
    main()

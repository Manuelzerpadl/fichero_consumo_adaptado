"""
Script manual para probar la autenticación y descarga de documentos
desde la API de Cobee/Retool usando RetoolClient.
"""

import logging
from pathlib import Path
from api.retool_client import RetoolClient
from config.settings import settings

# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,  # 👈 DEBUG en vez de INFO
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main() -> None:
    logging.debug("🔍 Iniciando script de prueba RetoolClient...")

    company_id = settings.TEST_COMPANY_ID
    payroll_document_id = settings.TEST_PAYROLL_DOCUMENT_ID

    logging.debug(f"TEST_COMPANY_ID={company_id}")
    logging.debug(f"TEST_PAYROLL_DOCUMENT_ID={payroll_document_id}")

    if not company_id or not payroll_document_id:
        print("❌ Falta TEST_COMPANY_ID o TEST_PAYROLL_DOCUMENT_ID en el .env")
        return

    client = RetoolClient(base_url="https://api.cobee.io/v1/back-office")
    client.authenticate()

    output_dir = Path("output_test")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = client.download_payroll_adjustment(
        company_id=company_id,
        payroll_document_id=payroll_document_id,
        output_folder=str(output_dir),
        filename="ajuste_nomina_test",
    )

    if file_path:
        print(f"✅ Archivo descargado en: {file_path}")
    else:
        print("❌ La descarga falló")


if __name__ == "__main__":
    main()

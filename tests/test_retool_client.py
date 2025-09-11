import pytest
from pathlib import Path
from api.retool_client import RetoolClient
from config.settings import settings


@pytest.mark.integration
def test_authenticate_real_env():
    """Prueba la autenticación real contra Auth0 usando variables del .env"""
    client = RetoolClient(base_url="https://api.cobee.io/v1/back-office")
    client.authenticate()

    assert client._token is not None
    assert "Authorization" in client._session.headers


@pytest.mark.integration
def test_download_real_env(tmp_path):
    """
    ⚠️ Este test hace una request real a la API de Cobee.
    Necesita:
      - TEST_COMPANY_ID y TEST_PAYROLL_DOCUMENT_ID en el .env
      - Credenciales de Auth0 válidas
    """
    company_id = settings.TEST_COMPANY_ID
    payroll_document_id = settings.TEST_PAYROLL_DOCUMENT_ID

    if not company_id or not payroll_document_id:
        pytest.skip("❌ TEST_COMPANY_ID o TEST_PAYROLL_DOCUMENT_ID no definidos en .env")

    client = RetoolClient(base_url="https://api.cobee.io/v1/back-office")
    client.authenticate()

    output_file = client.download_payroll_adjustment(
        company_id=company_id,
        payroll_document_id=payroll_document_id,
        output_folder=str(tmp_path),
        filename="ajuste_nomina",
    )

    assert output_file != ""
    assert Path(output_file).exists()
    assert Path(output_file).stat().st_size > 0  # archivo no vacío

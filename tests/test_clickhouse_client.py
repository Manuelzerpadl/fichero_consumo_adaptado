import os
import pandas as pd
import pytest
from unittest.mock import MagicMock
from db.clickhouse_client import ClickHouseClient


# -------------------------------
# UNIT TESTS (con mocks)
# -------------------------------
def test_run_query_with_mock():
    client = ClickHouseClient()
    # Simulamos la respuesta de client.query
    client.client.query = MagicMock(
        return_value=MagicMock(
            result_rows=[[1, "hola"]],
            column_names=["id", "msg"]
        )
    )

    rows = client.run_query("SELECT 1, 'hola'")
    assert rows == [(1, "hola")]


def test_query_adjustment_documents_for_ids_empty():
    client = ClickHouseClient()
    client.client.query = MagicMock(
        return_value=MagicMock(result_rows=[], column_names=["col1", "col2"])
    )

    df = client.query_adjustment_documents_for_ids(["company1"])
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# -------------------------------
# INTEGRATION TESTS (requieren ClickHouse real)
# -------------------------------
@pytest.mark.integration
def test_connection_to_clickhouse():
    client = ClickHouseClient()
    rows = client.test_connection()

    assert isinstance(rows, list)
    assert len(rows[0]) >= 2  # debería traer versión y timezone


@pytest.mark.integration
def test_query_adjustment_with_real_clickhouse():
    company_ids = os.getenv("TEST_COMPANY_IDS", "").split(",")
    if not any(company_ids):
        pytest.skip("No se pasaron company_ids de prueba en TEST_COMPANY_IDS")

    client = ClickHouseClient()
    df = client.query_adjustment_documents_for_ids(company_ids)

    assert isinstance(df, pd.DataFrame)
    assert "companyId" in df.columns

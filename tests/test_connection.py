import os
import pytest
import requests
from clickhouse_connect import get_client
from dotenv import load_dotenv
load_dotenv()

def test_sanity():
    assert 2 + 2 == 4

@pytest.fixture
def clickhouse_client():
    host = os.getenv("CLICKHOUSE_HOST")
    port = int(os.getenv("CLICKHOUSE_PORT", 9000))
    user = os.getenv("CLICKHOUSE_USER")
    password = os.getenv("CLICKHOUSE_PASSWORD")

    return get_client(host=host, port=port, user=user, password=password)

def test_clickhouse_connection(clickhouse_client):
    """Testea que ClickHouse responda a un simple SELECT"""
    result = clickhouse_client.query("SELECT 1")
    rows = result.result_rows
    assert rows == [(1,)], "La conexión a ClickHouse no funciona correctamente"

def test_auth_token():
    """Testea que Auth0 devuelva un token válido"""
    url = os.getenv("AUTH_URL_PROD")
    payload = {
        "username": os.getenv("AUTH_USERNAME"),
        "password": os.getenv("AUTH_PASSWORD"),
        "realm": os.getenv("AUTH_REALM"),
        "audience": os.getenv("AUTH_AUDIENCE"),
        "scope": os.getenv("AUTH_SCOPE"),
        "grant_type": os.getenv("AUTH_GRANT_TYPE"),
        "client_id": os.getenv("AUTH_CLIENT_ID"),
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Error en Auth: {response.text}"
    
    data = response.json()
    assert "access_token" in data, "No se recibió un access_token en la respuesta"

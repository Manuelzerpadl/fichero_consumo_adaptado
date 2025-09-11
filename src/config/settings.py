import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class Settings:
    # Auth0
    AUTH_URL = os.getenv("AUTH_URL_PROD")
    AUTH_USERNAME = os.getenv("AUTH_USERNAME")
    AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
    AUTH_REALM = os.getenv("AUTH_REALM")
    AUTH_AUDIENCE = os.getenv("AUTH_AUDIENCE")
    AUTH_SCOPE = os.getenv("AUTH_SCOPE")
    AUTH_GRANT_TYPE = os.getenv("AUTH_GRANT_TYPE")
    AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
    AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")

    # ClickHouse
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

    # SendGrid
    SENDGRID_KEY = os.getenv("SENDGRID_KEY")
    TEMPLATE_ID_PAYROLLS = os.getenv("SENDGRID_TEMPLATE_ID_PAYROLLS")

settings = Settings()

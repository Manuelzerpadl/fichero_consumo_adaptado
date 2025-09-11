import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Auth0 ---
    AUTH_URL: str
    AUTH_USERNAME: str
    AUTH_PASSWORD: str
    AUTH_REALM: str
    AUTH_AUDIENCE: str
    AUTH_SCOPE: str
    AUTH_GRANT_TYPE: str
    AUTH_CLIENT_ID: str

    # --- ClickHouse ---
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str

    # --- SendGrid ---
    SENDGRID_KEY: str | None
    TEMPLATE_ID_PAYROLLS: str | None

    # --- Tests ---
    TEST_COMPANY_ID: str | None
    TEST_PAYROLL_DOCUMENT_ID: str | None

    def __init__(self) -> None:
        # Auth (obligatorios)
        self.AUTH_URL = self._require("AUTH_URL_PROD")
        self.AUTH_USERNAME = self._require("AUTH_USERNAME")
        self.AUTH_PASSWORD = self._require("AUTH_PASSWORD")
        self.AUTH_REALM = self._require("AUTH_REALM")
        self.AUTH_AUDIENCE = self._require("AUTH_AUDIENCE")
        self.AUTH_SCOPE = self._require("AUTH_SCOPE")
        self.AUTH_GRANT_TYPE = self._require("AUTH_GRANT_TYPE")
        self.AUTH_CLIENT_ID = self._require("AUTH_CLIENT_ID")

        # ClickHouse
        self.CLICKHOUSE_HOST = self._require("CLICKHOUSE_HOST")
        self.CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))
        self.CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
        self.CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

        # SendGrid
        self.SENDGRID_KEY = os.getenv("SENDGRID_KEY")
        self.TEMPLATE_ID_PAYROLLS = os.getenv("SENDGRID_TEMPLATE_ID_PAYROLLS")

        # Testing
        self.TEST_COMPANY_ID = os.getenv("TEST_COMPANY_ID")
        self.TEST_PAYROLL_DOCUMENT_ID = os.getenv("TEST_PAYROLL_DOCUMENT_ID")

    @staticmethod
    def _require(env_var: str) -> str:
        value = os.getenv(env_var)
        if not value:
            raise ValueError(f"❌ La variable de entorno {env_var} es obligatoria y no está definida en .env")
        return value


settings = Settings()

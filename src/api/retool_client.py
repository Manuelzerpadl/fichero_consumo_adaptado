import logging
import re
import requests
from pathlib import Path
from typing import Any, Dict, Optional
from config.settings import settings


class RetoolClient:
    def __init__(self, base_url: str) -> None:
        """
        Cliente para la API de Retool/Cobee.
        :param base_url: URL base de la API (ej: https://api.cobee.io/v1/back-office).
        """
        self._auth_url: str = settings.AUTH_URL
        self._base_url: str = base_url.rstrip("/")
        self._auth_payload: Dict[str, Any] = {
            "username": settings.AUTH_USERNAME,
            "password": settings.AUTH_PASSWORD,
            "realm": settings.AUTH_REALM,
            "audience": settings.AUTH_AUDIENCE,
            "scope": settings.AUTH_SCOPE,
            "grant_type": settings.AUTH_GRANT_TYPE,
            "client_id": settings.AUTH_CLIENT_ID,
        }
        self._session: requests.Session = requests.Session()
        self._token: Optional[str] = None

    def authenticate(self) -> None:
        """Obtiene el token de autenticación y actualiza los headers de la sesión."""
        try:
            response = self._session.post(self._auth_url, json=self._auth_payload, timeout=30)
            response.raise_for_status()
            token: Optional[str] = response.json().get("access_token")

            if not token:
                raise ValueError("No se recibió 'access_token' en la autenticación")

            self._token = token
            self._session.headers.update({
                "Authorization": f"Bearer {self._token}",
                "Accept": "application/json",
            })

            logging.info("Autenticación exitosa.")
        except requests.RequestException as exc:
            logging.error(f"Error en la autenticación: {exc}")
            raise SystemExit(f"Error en la autenticación: {exc}") from exc

    def download_payroll_adjustment(
        self,
        company_id: str,
        payroll_document_id: str,
        output_folder: str,
        filename: str,
    ) -> str:
        """
        Descarga el archivo CSV o XLSX de ajustes de nómina para una empresa y documento específico.
        Guarda el archivo en la carpeta `output_folder` y devuelve el path.
        """
        url: str = f"{self._base_url}/companies/{company_id}/payroll-documents/{payroll_document_id}"
        payload: Dict[str, Any] = {
            "email": settings.AUTH_USERNAME,  # usamos el usuario del .env como email
            "dataPersists": False,
            "useDefaultFileType": True,
        }

        try:
            response = self._session.get(url, json=payload, timeout=100)
            response.raise_for_status()

            content_type: str = response.headers.get("Content-Type", "")
            logging.info(f"Content-Type recibido: {content_type}")

            # Limpieza del nombre
            safe_filename: str = re.sub(r'[<>:"/\\|?*]', "_", filename)

            # Asegurar extensión correcta
            if "spreadsheetml" in content_type and not safe_filename.endswith(".xlsx"):
                safe_filename += ".xlsx"
            elif "text/csv" in content_type and not safe_filename.endswith(".csv"):
                safe_filename += ".csv"
            elif not (safe_filename.endswith(".csv") or safe_filename.endswith(".xlsx")):
                safe_filename += ".bin"  # fallback

            Path(output_folder).mkdir(parents=True, exist_ok=True)
            output_path: Path = Path(output_folder) / safe_filename

            output_path.write_bytes(response.content)

            logging.info(f"📄 Archivo descargado exitosamente: {output_path}")
            return str(output_path)

        except requests.RequestException as exc:
            logging.error(
                f"Error al descargar el archivo para company_id={company_id}, "
                f"document_id={payroll_document_id}: {exc}"
            )
            return ""

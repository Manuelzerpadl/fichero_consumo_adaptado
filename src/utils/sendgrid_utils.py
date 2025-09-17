import base64
from pathlib import Path
from typing import List, Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from config.settings import settings


def send_with_sendgrid(to_emails: List[str], file_path: Path, dynamic_data: Dict):
    """
    Envía un email usando una plantilla de SendGrid con adjunto.
    - to_emails: lista de destinatarios
    - file_path: ruta del fichero adjunto
    - dynamic_data: variables dinámicas para la plantilla
    """
    message = Mail(
        from_email="procesos@cobee.io",  # ⚠️ debe ser validado en SendGrid
        to_emails=to_emails,
    )

    # Usar template dinámico
    message.template_id = settings.TEMPLATE_ID_PAYROLLS
    message.dynamic_template_data = dynamic_data

    # Adjuntar fichero
    with open(file_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    attachment = Attachment(
        FileContent(encoded),
        FileName(file_path.name),
        FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        Disposition("attachment"),
    )
    message.attachment = attachment

    sg = SendGridAPIClient(settings.SENDGRID_KEY)
    response = sg.send(message)
    return response

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_dir: str = "logs", log_file: str = "app.log"):
    """Configura logging global para consola y fichero rotativo."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / log_file

    # Formato estándar
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Fichero rotativo (5 MB x 5 backups)
    file_handler = RotatingFileHandler(log_path, maxBytes=5_000_000, backupCount=5)
    file_handler.setFormatter(formatter)

    # Logger raíz
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler],
        force=True,  # asegura que sobrescribe config previa
    )

    logging.getLogger("sendgrid").setLevel(logging.WARNING)  # bajar verbosidad
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logging.getLogger("a3_payroll")

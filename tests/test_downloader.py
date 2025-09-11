import pytest
from pathlib import Path
from downloader.payroll_downloader import main


@pytest.mark.integration
def test_downloader_creates_files(tmp_path):
    """
    Test de integración del payroll_downloader.
    Verifica que al ejecutarlo se crean carpetas de año/mes
    y que dentro hay al menos un archivo descargado.
    """
    # Ejecutar el downloader en un directorio temporal
    main(base_dir=str(tmp_path))

    # Verificar estructura año/mes
    year_dirs = list(tmp_path.iterdir())
    assert year_dirs, "No se creó ninguna carpeta de año"

    month_dirs = list(year_dirs[0].iterdir())
    assert month_dirs, "No se creó ninguna carpeta de mes"

    files = list(month_dirs[0].iterdir())
    assert files, "No se descargó ningún archivo"

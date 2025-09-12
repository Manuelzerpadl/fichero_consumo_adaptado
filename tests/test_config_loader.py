import pytest
from pathlib import Path
from transformer.config_loader import load_config_excel

@pytest.mark.unit
def test_load_config_excel(tmp_path: Path):
    # Crear un Excel mínimo de prueba
    import pandas as pd

    excel_file = tmp_path / "empresa.xlsx"

    # Pestaña 2. Información Básica
    df_basic = pd.DataFrame({"Campo": ["CIF de la empresa", "Nombre completo de la empresa", "Tipo de transformador"],
                             "Valor": ["B123", "Test SA", "a3"]})
    # Pestaña 3. Columnas y Mapeo
    df_mappings = pd.DataFrame({"Columna del CSV Original": ["dni"], "Uso": ["Identificación"], "Nombre Final": ["DNI"]})
    # Pestaña 4. Config Excel y Fecha
    df_output = pd.DataFrame({"Configuración": ["OUTPUT - Formato archivo"], "Valor": ["xlsx"]})

    with pd.ExcelWriter(excel_file) as writer:
        df_basic.to_excel(writer, sheet_name="2. Información Básica", index=False)
        df_mappings.to_excel(writer, sheet_name="3. Columnas y Mapeo", index=False)
        df_output.to_excel(writer, sheet_name="4. Config Excel y Fecha", index=False)

    # Ejecutar loader
    config = load_config_excel(str(excel_file))

    assert "basic_info" in config
    assert "mappings" in config
    assert "output_config" in config
    assert config["basic_info"]["CIF de la empresa"] == "B123"

import pytest
import json
from pathlib import Path
from transformer.config_manager import load_company_config

@pytest.mark.unit
def test_load_from_json(tmp_path: Path):
    json_file = tmp_path / "empresa.json"
    config_data = {
        "basic_info": {
            "CIF de la empresa": "B123",
            "Nombre completo de la empresa": "Test SA",
            "Tipo de transformador": "a3",
        },
        "mappings": [
            {"Columna del CSV Original": "dni", "Uso": "Identificación", "Nombre Final": "DNI",
             "Concepto Final": "", "Operación": "", "Signo": "", "Notas": ""}
        ],
        "output_config": {"OUTPUT - Formato archivo": "xlsx"}
    }
    json_file.write_text(json.dumps(config_data), encoding="utf-8")

    config = load_company_config(str(json_file.with_suffix("")))
    assert config["basic_info"]["CIF de la empresa"] == "B123"

@pytest.mark.unit
def test_load_from_excel(tmp_path: Path):
    import pandas as pd
    excel_file = tmp_path / "empresa.xlsx"

    df_basic = pd.DataFrame({"Campo": ["CIF de la empresa", "Nombre completo de la empresa", "Tipo de transformador"],
                             "Valor": ["B123", "Test SA", "a3"]})
    df_mappings = pd.DataFrame({"Columna del CSV Original": ["dni"], "Uso": ["Identificación"], "Nombre Final": ["DNI"]})
    df_output = pd.DataFrame({"Configuración": ["OUTPUT - Formato archivo"], "Valor": ["xlsx"]})

    with pd.ExcelWriter(excel_file) as writer:
        df_basic.to_excel(writer, sheet_name="2. Información Básica", index=False)
        df_mappings.to_excel(writer, sheet_name="3. Columnas y Mapeo", index=False)
        df_output.to_excel(writer, sheet_name="4. Config Excel y Fecha", index=False)

    config = load_company_config(str(excel_file.with_suffix("")))
    assert config["basic_info"]["Tipo de transformador"] == "a3"
    assert (excel_file.with_suffix(".json")).exists()

@pytest.mark.unit
def test_missing_files(tmp_path: Path):
    base = tmp_path / "empresa"
    with pytest.raises(FileNotFoundError):
        load_company_config(str(base))

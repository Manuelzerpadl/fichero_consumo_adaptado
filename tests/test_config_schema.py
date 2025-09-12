import pytest
from transformer.config_schema import ConfigSchema

@pytest.mark.unit
def test_valid_config_schema():
    config = {
        "basic_info": {
            "CIF de la empresa": "B123",
            "Nombre completo de la empresa": "Test SA",
            "Tipo de transformador": "a3",
        },
        "mappings": [
            {
                "Columna del CSV Original": "dni",
                "Uso": "Identificación",
                "Nombre Final": "DNI",
                "Concepto Final": "",
                "Operación": "",
                "Signo": "",
                "Notas": "",
            }
        ],
        "output_config": {
            "OUTPUT - Formato archivo": "xlsx"
        }
    }

    validated = ConfigSchema(**config)
    assert validated.basic_info["CIF de la empresa"] == "B123"

@pytest.mark.unit
def test_invalid_config_schema():
    config = {
        "basic_info": {},  # Falta todo
        "mappings": [],
        "output_config": {}
    }
    with pytest.raises(Exception):
        ConfigSchema(**config)

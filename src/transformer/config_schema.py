from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator


class BasicInfo(BaseModel):
    id_empresa: str = Field(..., alias="ID empresa")
    cif: str = Field(..., alias="CIF de la empresa")
    empresa: str = Field(..., alias="Nombre completo de la empresa")
    tipo_transformador: str = Field(..., alias="Tipo de transformador")


class Mapping(BaseModel):
    input_column: str = Field(..., alias="Columna del CSV Original")
    uso: str = Field(..., alias="Uso")
    output_column: str = Field(..., alias="Columna de Salida")
    operacion: str = Field("", alias="Operación")
    signo: str = Field("", alias="Signo")
    notas: str = Field("", alias="Notas")


class OutputConfig(BaseModel):
    formato: str = Field(..., alias="OUTPUT - Formato archivo")
    celda_c2: str = Field("", alias="EXCEL - Celda C2")
    celda_j2: str = Field("", alias="EXCEL - Celda J2")


class ConfigSchema(BaseModel):
    basic_info: Dict[str, Any]
    mappings: List[Dict[str, Any]]
    output_config: Dict[str, Any]

    @validator("basic_info")
    def validate_basic_info(cls, v):
        BasicInfo(**v)  # validamos con el modelo
        return v

    @validator("mappings")
    def validate_mappings(cls, v):
        for mapping in v:
            Mapping(**mapping)
        return v

    @validator("output_config")
    def validate_output_config(cls, v):
        OutputConfig(**v)
        return v

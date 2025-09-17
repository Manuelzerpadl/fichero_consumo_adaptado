import re
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

class BasicInfo(BaseModel):
    id_empresa: str = Field(..., alias="ID empresa")
    cif: str = Field(..., alias="CIF de la empresa")
    empresa: str = Field(..., alias="Nombre completo de la empresa")
    tipo_transformador: str = Field(..., alias="Tipo de transformador")
    correos: Optional[List[EmailStr]] = Field(default_factory=list, alias="Correos")

    @field_validator("correos", mode="before")
    def split_and_validate_emails(cls, value):
        if isinstance(value, str):
            value = [email.strip() for email in value.split(";") if email.strip()]
        if not value:
            return []
        for email in value:
            if not EMAIL_REGEX.match(email):
                raise ValueError(f"Correo inválido: {email}")
        return value


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
    basic_info: BasicInfo
    mappings: List[Mapping]
    output_config: OutputConfig

import json
import pandas as pd
from datetime import datetime
from pathlib import Path

from utils.date_utils import get_formatted_date


def transform_payroll(input_file: str, config_json: str) -> pd.DataFrame:
    """
    Transforma un fichero de nómina bruto en base a la configuración de la empresa (JSON).
    Devuelve un DataFrame con columnas renombradas, operaciones, signos y fecha.
    """
    # 1) Cargar configuración
    with open(config_json, encoding="utf-8") as f:
        config = json.load(f)

    # 2) Leer fichero bruto
    sep = config["basic_info"].get("Separador del CSV", ";")
    decimal = config["basic_info"].get("Símbolo decimal", ".")
    if input_file.endswith(".csv"):
        df_raw = pd.read_csv(input_file, sep=sep, decimal=decimal)
    else:
        df_raw = pd.read_excel(input_file)

    # Normalizar cabeceras
    df_raw.columns = df_raw.columns.str.strip().str.lower()

    # 🔹 Normalización global de columnas numéricas
    for col in df_raw.columns:
        if df_raw[col].dtype == "object":
            cleaned = (
                df_raw[col]
                .astype(str)
                .str.replace(".", "", regex=False)   # elimina separador de miles
                .str.replace(",", ".", regex=False)  # convierte coma decimal a punto
                .str.strip()
            )
            try:
                df_raw[col] = pd.to_numeric(cleaned)
            except Exception:
                # si no se puede convertir, dejamos la columna como texto limpio
                df_raw[col] = cleaned

    # 3) Aplicar mappings
    mappings = config["mappings"]
    df_out = pd.DataFrame()

    for m in mappings:
        col_orig = m["Columna del CSV Original"].strip().lower()
        col_salida = m.get("Columna de Salida", "").strip()
        operacion = m.get("Operación", "").strip().lower()
        signo = m.get("Signo", "").strip().lower()

        if col_orig not in df_raw.columns:
            raise ValueError(
                f"Columna '{col_orig}' no existe en el input. "
                f"Columnas disponibles: {list(df_raw.columns)}"
            )

        serie = df_raw[col_orig].copy()

        # aplicar signo
        if signo == "positivo":
            serie = pd.to_numeric(serie, errors="coerce").abs()
        elif signo == "negativo":
            serie = -pd.to_numeric(serie, errors="coerce").abs()

        destino = col_salida or col_orig

        # aplicar operación
        if operacion == "renombrar":
            df_out[destino] = serie
        elif operacion == "sumar":
            if destino in df_out:
                df_out[destino] += serie
            else:
                df_out[destino] = serie
        else:
            df_out[destino] = serie

    # 4) Añadir columna de fecha si aplica
    output_cfg = config["output_config"]
    if output_cfg.get("FECHA - Incluir columna", "").upper() == "SI":
        date_value = get_formatted_date(
            output_cfg.get("FECHA - Tipo", "today"),
            output_cfg.get("FECHA - Formato", "DD/MM/YYYY"),
            output_cfg.get("FECHA - Valor personalizado", "")
        )

        fecha_col = output_cfg.get("FECHA - Nombre columna", "Fecha")
        fecha_pos = output_cfg.get("FECHA - Posición columna")

        if fecha_pos:  # insertar en posición específica
            pos = int(fecha_pos) - 1  # JSON usa 1-based, pandas usa 0-based
            df_out.insert(pos, fecha_col, date_value)
        else:  # añadir al final
            df_out[fecha_col] = date_value

    return df_out

import logging
import pandas as pd
from clickhouse_connect import get_client
from config.settings import settings
from typing import Optional, Any


class ClickHouseClient:
    def __init__(self) -> None:
        """Inicializa un cliente de ClickHouse usando la configuración de settings"""
        self.client = get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            username=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
        )

    def test_connection(self) -> list[tuple[Any, ...]]:
            """Valida que la conexión a ClickHouse funcione"""
            result = self.client.query("SELECT version(), timezone()")
            return [tuple(row) for row in result.result_rows]

    def run_query(
        self, query: str, params: Optional[dict[str, Any]] = None
    ) -> list[tuple[Any, ...]]:
        """
        Ejecuta una query y devuelve los resultados como lista de tuplas.
        :param query: SQL a ejecutar
        :param params: parámetros opcionales para queries parametrizadas
        """
        result = self.client.query(query, parameters=params or {})
        return [tuple(row) for row in result.result_rows]

    def query_adjustment_documents_for_ids(
        self, company_ids: list[str]
    ) -> pd.DataFrame:
        """
        Ejecuta la consulta de documentos 'adjustment' para los company_ids indicados,
        filtrando por mes y año actuales (today()).
        """
        if not company_ids:
            logging.warning("No hay company_ids para consultar.")
            return pd.DataFrame()

        query = """
        WITH
            {allowed_companies:Array(String)} AS allowed_companies,
            toDateTime(pdv.lastUpdatedMs / 1000) AS raw_last_updated,
            coalesce(tupleElement(pdv.storageProvider, 1), '') AS path,
            arrayElement(splitByString('/', path), -1) AS raw_filename
        SELECT
            pc.companyId AS companyId,
            c.legalId,
            argMax(pdv.id, raw_last_updated)      AS documentId,
            argMax(pdv.storageProvider, raw_last_updated) AS storageProvider,
            argMax(raw_filename, raw_last_updated)        AS filename,
            pc.id                                  AS cycleId,
            c.autoCloseDay                         AS CloseDay,
            pc.fiscalYear,
            pc.payrollMonth,
            argMax(pdv.`type`, raw_last_updated)  AS type,
            formatDateTime(max(raw_last_updated), '%d') AS payroll_last_updated_day
        FROM operations_silver_mongo_backenddb.payroll_documents_v2 AS pdv
        LEFT JOIN operations_silver_mongo_backenddb.payroll_cycles AS pc
            ON pdv.payrollCycleId = pc.id
        LEFT JOIN operations_silver_mongo_backenddb.companies AS c
            ON pc.companyId = c.companyId
        WHERE
            pdv.`type` = 'adjustment'
            AND pc.reported = 'true'
            AND toMonth(today()) = toInt32(pc.payrollMonth)
            AND toYear(today())  = toInt32(pc.fiscalYear)
            AND has(allowed_companies, pc.companyId)
            AND (
                (endsWith(raw_filename, '.csv') OR endsWith(raw_filename, '.xlsx'))
                AND NOT match(raw_filename, '-v2\\.(csv|xlsx)$')
            )
            AND toDate(raw_last_updated) = today()
            AND c.autoCloseDay = toDayOfMonth(raw_last_updated)
        GROUP BY
            pc.companyId,
            c.legalId,
            pc.id,
            c.autoCloseDay,
            pc.fiscalYear,
            pc.payrollMonth
        """

        try:
            result = self.client.query(
                query, parameters={"allowed_companies": company_ids}
            )
            df = pd.DataFrame(result.result_rows, columns=result.column_names)
            logging.info(f"[STATS] Obtenidos {len(df)} registros de documentos ‘adjustment’")
            if df.empty:
                logging.warning("La consulta devolvió 0 filas.")
            return df

        except Exception as e:
            logging.error(
                f"Error al ejecutar query_adjustment_documents_for_ids: {e}"
            )
            return pd.DataFrame()

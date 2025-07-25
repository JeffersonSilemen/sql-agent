from db.init_db import engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from observability import setup_tracer

tracer = setup_tracer("sql-executor")

def sql_executor_node(data):
    with tracer.start_as_current_span("sql_executor") as span:
        sql = data.get("sql", "")
        parserd_sql = sql.lower()
        try:
            with engine.connect() as conn:
                query = text(parserd_sql)
                result = conn.execute(query)
                rows = result.fetchall()
                colunas = result.keys()
                data["resultado"] = [dict(zip(colunas, row)) for row in rows]
        except SQLAlchemyError as e:
            data["erro"] = f"Erro ao executar SQL: {e}"
        span.set_attribute("sql", parserd_sql)
        return data

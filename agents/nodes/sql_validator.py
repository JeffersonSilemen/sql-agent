import re
from observability import setup_tracer

tracer = setup_tracer("sql-validator")

def sql_validator_node(data):
    with tracer.start_as_current_span("sql_validator") as span:
        sql = data.get("sql", "")
        sql_limpo = sql.strip().lower()

        if not sql_limpo.startswith("select"):
            return {**data, "erro": "Apenas SELECTs são permitidos."}

        proibidas = [
            "insert", "update", "delete", "drop", "alter", "create",
            ";", "--", "/*", "*/", "exec", "union"
        ]

        for palavra in proibidas:
            pattern = r"\b" + re.escape(palavra) + r"\b"
            if re.search(pattern, sql_limpo):
                return {**data, "erro": f"Uso proibido da palavra-chave '{palavra}' na query."}

        if ";" in sql_limpo[:-1]:
            return {**data, "erro": "Múltiplas queries não são permitidas."}

        if len(sql_limpo) > 1000:
            return {**data, "erro": "Query muito grande, tamanho máximo permitido: 1000 caracteres."}

        span.set_attribute("sql", sql)
        span.set_attribute("validacao", "sucesso")
        return data

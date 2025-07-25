import re
from langchain_core.messages import HumanMessage
from observability import setup_tracer

tracer = setup_tracer("sql-generator")

def sql_generator_node(data, llm):
    with tracer.start_as_current_span("sql_generator") as span:
        pergunta = data.get("pergunta", "")
        estrutura = data.get("estrutura_nlp", {})
        contexto_rag = data.get("contexto_rag", "")

        prompt = f"""
        Você é um gerador de queries SQL para o seguinte esquema de banco de dados PostgreSQL:

        - clientes(id, nome, email, saldo)
        - transacoes(id, cliente_id, produto_id, data)
        - produtos(id, nome, preco)

        Contexto adicional para auxiliar na geração da query:
        {contexto_rag}

        Baseado na pergunta: "{pergunta}"

        Gere apenas a query SQL correta que usa essas tabelas.

        Responda somente com a query SQL entre ```sql e ``` sem explicações.
        """

        resposta = llm.invoke([HumanMessage(content=prompt)])
        sql_completo = resposta.content

        match = re.search(r"```sql(.*?)```", sql_completo, re.DOTALL)
        sql_query = match.group(1).strip() if match else sql_completo.strip()

        span.set_attribute("pergunta", pergunta)
        span.set_attribute("sql", sql_query)

        return {
            **data,
            "sql": sql_query,
        }

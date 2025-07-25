import json
from langchain_core.messages import HumanMessage
from observability import setup_tracer
from utils.retriever import get_contexto_banco 

tracer = setup_tracer("nlp-parser")

def nlp_parser_node(data, llm):
    pergunta = data.get("pergunta", "")
    contexto = get_contexto_banco()

    with tracer.start_as_current_span("nlp_parser") as span:
        prompt = f"""
        Use o contexto abaixo sobre as tabelas do banco de dados para interpretar a pergunta.

        CONTEXTO:
        {contexto}

        Agora, transforme a pergunta em uma estrutura JSON semântica:

        Pergunta: "{pergunta}"

        Responda SOMENTE com um JSON válido neste formato:
        {{
            "tabela_principal": "clientes",
            "filtros": [{{"coluna": "produto", "valor": "Notebook"}}],
            "tipo_consulta": "select"
        }}

        Se não for possível interpretar a pergunta, retorne um JSON vazio: {{}}
        """

        resposta = llm.invoke([HumanMessage(content=prompt)])
        resposta_bruta = resposta.content.strip()

        try:
            if not resposta_bruta:
                estrutura_nlp = {}
                erro = "Resposta vazia do LLM"
            else:
                inicio_json = resposta_bruta.find('{')
                fim_json = resposta_bruta.rfind('}') + 1

                if inicio_json != -1 and fim_json > inicio_json:
                    json_limpo = resposta_bruta[inicio_json:fim_json]
                    estrutura_nlp = json.loads(json_limpo)
                    erro = None
                else:
                    estrutura_nlp = {}
                    erro = "Não foi possível encontrar JSON válido na resposta"

        except json.JSONDecodeError as e:
            estrutura_nlp = {}
            erro = f"Falha ao interpretar JSON: {e}"
        except Exception as e:
            estrutura_nlp = {}
            erro = f"Falha ao interpretar NLP: {e}"

        span.set_attribute("pergunta", pergunta)
        span.set_attribute("erro", erro if erro else "nenhum")
        span.set_attribute("estrutura_nlp_detectada", bool(estrutura_nlp))
        return {
            **data,
            "estrutura_nlp": estrutura_nlp,
            "erro": erro
        }

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Optional, List, Dict, Any
from agents.nodes.nlp_parser import nlp_parser_node
from agents.nodes.sql_generator import sql_generator_node
from agents.nodes.sql_validator import sql_validator_node
from agents.nodes.sql_executor import sql_executor_node
from agents.nodes.formatter import formatter_node
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Optional, List, Dict, Any

load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model="deepseek-coder",
    openai_api_key=os.getenv("LLM_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

nlp_node = RunnableLambda(lambda state: nlp_parser_node(state, llm))
sql_gen_node = RunnableLambda(lambda state: sql_generator_node(state, llm))
sql_validator = RunnableLambda(sql_validator_node)
sql_executor = RunnableLambda(sql_executor_node)
formatter = RunnableLambda(formatter_node)

class AgentState(TypedDict, total=False):
    pergunta: str
    estrutura_nlp: Optional[Dict[str, Any]]
    sql: Optional[str]
    resultado: Optional[List[Dict[str, Any]]]
    resposta_final: Optional[str]
    erro: Optional[str]

def build_graph():
    graph = StateGraph(state_schema=AgentState)

    graph.add_node("NLP", nlp_node)
    graph.add_node("SQLGen", sql_gen_node)
    graph.add_node("Validate", sql_validator)
    graph.add_node("Execute", sql_executor)
    graph.add_node("Format", formatter)

    graph.set_entry_point("NLP")
    graph.add_edge("NLP", "SQLGen")
    graph.add_edge("SQLGen", "Validate")
    graph.add_edge("Validate", "Execute")
    graph.add_edge("Execute", "Format")
    graph.add_edge("Format", END)

    return graph.compile()

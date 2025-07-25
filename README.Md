# 🧠 SQL Agent Inteligente

Este projeto implementa um agente inteligente capaz de interpretar perguntas em linguagem natural, convertê-las em consultas SQL seguras e executá-las em um banco de dados PostgreSQL. A solução foi construída com foco em modularidade, observabilidade e segurança.

---

## 🚀 Funcionalidades

- ✅ Interpretação de linguagem natural (NLP)
- ✅ Geração de queries SQL com validação
- ✅ Execução segura contra SQL Injection
- ✅ Uso de múltiplos agentes especializados via LangGraph
- ✅ Observabilidade com OpenTelemetry (logs no console)
- ✅ Suporte a RAG (Retrieval-Augmented Generation) via contexto local

---

## 🧱 Arquitetura

```bash
SQL-AGENT/
│
├── main.py                     # Interface via Streamlit
│
├── db/
│   └── db_init.py              # Criação das tabelas e dados iniciais
│
├── agents/
│   ├── main_graph.py           # Orquestração dos agentes com LangGraph
│   └── nodes/
│       ├── nlp_parser_node.py      # Interpreta perguntas (NLP + RAG)
│       ├── sql_generator_node.py  # Gera queries SQL
│       ├── sql_validator_node.py  # Garante segurança das queries
│       ├── sql_executor_node.py   # Executa as queries no PostgreSQL
│       └── formatter_node.py      # Formata a resposta para exibição
│
├── docs/
│   └── contexto.txt            # Contexto usado no RAG local
│
├── utils/
│   └── retriever.py            # Função para carregar o contexto RAG
│
├── observability.py            # Logs com OpenTelemetry
│
└── requirements.txt            # Dependências do projeto

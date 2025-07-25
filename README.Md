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
```

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- LangChain
- LangGraph
- Streamlit
- PostgreSQL
- OpenTelemetry
- DeepSeek (LLM usado)

---

## 📦 Como executar o projeto localmente

### 1. Clone o repositório
Para colar no terminal use (ctrl + shit + v)
```bash
git clone git@github.com:JeffersonSilemen/sql-agent.git
```

- Abra a pasta criada
```bash
cd sql-agent
```


### 2. Criação do ambiente virtual
- É altamente recomendada a criação de um ambiente virtual para executar o projeto. Para não atrapalhar os ambientes de desenvolvimento de outros projetos.
```bash
python3 -m venv venv 
```

- Ative o ambiente virtual
```bash
# Caso esteja usando Linux, use:
source venv/bin/activate  
# Caso esteja usando Windows, use: 
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

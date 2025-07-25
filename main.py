import streamlit as st
import pandas as pd
from agents.main_graph import build_graph
from observability import setup_tracer

tracer = setup_tracer("sql-agent")

agent = build_graph()

if "historico" not in st.session_state:
    st.session_state.historico = []

def main():
    st.set_page_config(page_title="SQL Agent", page_icon="🧠", layout="centered")
    st.title("🧠 SQL Agent Inteligente")
    st.sidebar.title("📚 Exemplos de perguntas")
    exemplos = [
        "Quais clientes compraram um notebook?",
        "Quanto cada cliente gastou no total?",
        "Qual o total de vendas por categoria?",
        "Quem tem saldo suficiente para comprar um Smartphone?"
    ]
    for exemplo in exemplos:
        if st.sidebar.button(exemplo):
            st.session_state["pergunta"] = exemplo

    pergunta = st.text_input("Digite sua pergunta em linguagem natural:", value=st.session_state.get("pergunta", ""))

    if st.button("Consultar") and pergunta.strip():
        with st.spinner("Processando a pergunta..."):
            estado_inicial = {"pergunta": pergunta}
            resultado = agent.invoke(estado_inicial)

        st.session_state.historico.insert(0, {
            "pergunta": pergunta,
            "resultado_completo": resultado,
            "resultado": resultado.get("resultado", []),
            "resposta": resultado.get("resposta_final", ""),
            "sql": resultado.get("sql", ""),
            "erro": resultado.get("erro", None)
        })

    if st.session_state.historico:
        ultimo = st.session_state.historico[0]
        resultado = ultimo["resultado_completo"]

        st.subheader("🧾 Resultado da última pergunta")

        aba = st.tabs(["📦 Estado", "🧾 SQL", "📊 Resultado"])

        with aba[0]:
            st.markdown("#### Estado completo retornado")
            st.json(resultado)

        with aba[1]:
            st.markdown("#### SQL gerado")
            if ultimo["sql"]:
                st.code(ultimo["sql"], language="sql")
            else:
                st.warning("Nenhum SQL gerado.")
            if ultimo["erro"]:
                st.error(f"❌ Erro: {ultimo['erro']}")

        with aba[2]:
            st.markdown("#### Resultado formatado")
            if ultimo["erro"]:
                st.error(f"❌ Erro: {ultimo['erro']}")
            elif ultimo["resultado"]:
                df = pd.DataFrame(ultimo["resultado"])
                st.dataframe(df, use_container_width=True)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Baixar resultado como CSV", data=csv, file_name="resultado.csv", mime="text/csv")
            else:
                st.warning("Nenhum resultado encontrado.")

    if len(st.session_state.historico) > 1:
        st.subheader("🕓 Histórico de consultas anteriores")
        for i, item in enumerate(st.session_state.historico[1:], start=1):
            with st.expander(f"{i}. {item['pergunta']}"):
                aba_hist = st.tabs(["📦 Estado", "🧾 SQL", "📊 Resultado"])
                with aba_hist[0]:
                    st.json(item["resultado_completo"])
                with aba_hist[1]:
                    if item["sql"]:
                        st.code(item["sql"], language="sql")
                    if item["erro"]:
                        st.error(f"Erro: {item['erro']}")
                with aba_hist[2]:
                    if item["resultado"]:
                        df_hist = pd.DataFrame(item["resultado"])
                        st.dataframe(df_hist, use_container_width=True)
                    else:
                        st.warning("Nenhum resultado.")

if __name__ == "__main__":
    main()

def get_contexto_banco():
    with open("docs/contexto.txt", "r", encoding="utf-8") as f:
        return f.read()

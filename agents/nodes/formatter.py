def formatter_node(data):
    erro = data.get("erro")
    if erro: 
        return {"resposta_final": f"Erro: {erro}"}

    resultados = data.get("resultado", [])
    if not resultados:
        return {"resposta_final": "Nenhum resultado encontrado."}

    linhas = []
    for row in resultados:
        linha = ", ".join(f"{k}: {v}" for k, v in row.items())
        linhas.append(linha)

    return {"resposta_final": "\n".join(linhas)}

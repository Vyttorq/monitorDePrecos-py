# ============================================================
# storage.py — Armazenamento do histórico de preços
# Salva e lê dados em CSV (como uma planilha simples)
# ============================================================

import csv
import os
from datetime import datetime


CAMPOS = ["data_hora", "produto", "url", "preco"]


def salvar_preco(arquivo_csv, nome_produto, url, preco):
    """
    Adiciona uma linha no CSV com o preço coletado agora.
    Se o arquivo não existir, cria com cabeçalho automaticamente.
    """
    arquivo_novo = not os.path.exists(arquivo_csv)

    with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CAMPOS)

        if arquivo_novo:
            writer.writeheader()
            print(f"   📁 Arquivo '{arquivo_csv}' criado.")

        writer.writerow({
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "produto":   nome_produto,
            "url":       url,
            "preco":     f"{preco:.2f}",
        })

    print(f"   💾 Salvo: {nome_produto} — R$ {preco:.2f}")


def carregar_historico(arquivo_csv):
    """
    Lê todo o histórico do CSV e retorna como lista de dicionários.
    Retorna lista vazia se o arquivo ainda não existir.
    """
    if not os.path.exists(arquivo_csv):
        return []

    with open(arquivo_csv, mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ultimo_preco(arquivo_csv, nome_produto):
    """
    Busca o último preço registrado de um produto específico.
    Útil para comparar se o preço subiu ou caiu desde a última vez.

    Retorna:
        float — último preço registrado
        None  — se nunca foi registrado
    """
    historico = carregar_historico(arquivo_csv)
    registros = [r for r in historico if r["produto"] == nome_produto]

    if registros:
        return float(registros[-1]["preco"])

    return None

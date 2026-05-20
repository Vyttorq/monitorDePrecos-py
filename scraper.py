# ============================================================
# scraper.py — Coleta de preços via API oficial do Mercado Livre
#
# Muito mais confiável que Selenium para este caso:
# - Sem Chrome, sem bloqueios
# - Resposta em JSON limpo
# - API pública e gratuita
# ============================================================

import requests


def coletar_preco(busca, nome_produto):
    """
    Consulta a API do Mercado Livre e retorna o menor preço encontrado.

    Parâmetros:
        busca (str)        — termo de busca (ex: "teclado aula hero68")
        nome_produto (str) — nome amigável para exibir no log

    Retorna:
        float — menor preço encontrado
        None  — se não conseguir coletar
    """
    print(f"\n🔍 Buscando: {nome_produto}")

    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {
        "q":     busca,
        "limit": 20       # Pega os 20 primeiros resultados
    }

    try:
        resposta = requests.get(url, params=params, timeout=10)
        resposta.raise_for_status()  # Lança erro se status != 200

        dados = resposta.json()
        resultados = dados.get("results", [])

        if not resultados:
            print(f"   ⚠️ Nenhum resultado encontrado.")
            return None

        # Extrai todos os preços válidos
        precos = [
            item["price"]
            for item in resultados
            if "price" in item and item["price"] > 0
        ]

        if precos:
            menor = min(precos)
            print(f"   ✅ Menor preço: R$ {menor:.2f} ({len(precos)} ofertas analisadas)")
            return menor

        print(f"   ⚠️ Nenhum preço encontrado.")
        return None

    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout — API demorou demais para responder.")
        return None

    except requests.exceptions.RequestException as erro:
        print(f"   ❌ Erro na requisição: {erro}")
        return None

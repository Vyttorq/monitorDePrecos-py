# ============================================================
# scraper.py — Coleta de preços via API oficial do Mercado Livre
# Autenticação via OAuth 2.0 (Client Credentials)
# ============================================================

import requests


def obter_token(client_id, client_secret):
    """
    Autentica na API do Mercado Livre e retorna o access token.
    O token expira em 6 horas — gerado a cada execução do bot.
    """
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type":    "client_credentials",
        "client_id":     client_id,
        "client_secret": client_secret,
    }

    resposta = requests.post(url, data=payload, timeout=10)
    resposta.raise_for_status()
    token = resposta.json()["access_token"]
    print("🔑 Token obtido com sucesso!")
    return token


def coletar_preco(busca, nome_produto, token):
    """
    Busca o menor preço de um produto via API do ML.

    Parâmetros:
        busca (str)        — termo de busca
        nome_produto (str) — nome para exibir no log
        token (str)        — access token OAuth

    Retorna:
        float — menor preço encontrado
        None  — se não encontrar
    """
    print(f"\n🔍 Buscando: {nome_produto}")

    url = "https://api.mercadolibre.com/sites/MLB/search"
    headers = {"Authorization": f"Bearer {token}"}
    params  = {"q": busca, "limit": 20}

    try:
        resposta = requests.get(url, headers=headers, params=params, timeout=10)
        resposta.raise_for_status()

        resultados = resposta.json().get("results", [])

        if not resultados:
            print(f"   ⚠️ Nenhum resultado encontrado.")
            return None

        precos = [
            item["price"]
            for item in resultados
            if "price" in item and item["price"] > 0
        ]

        if precos:
            menor = min(precos)
            print(f"   ✅ Menor preço: R$ {menor:.2f} ({len(precos)} ofertas)")
            return menor

        print(f"   ⚠️ Nenhum preço encontrado.")
        return None

    except requests.exceptions.RequestException as erro:
        print(f"   ❌ Erro na requisição: {erro}")
        return None

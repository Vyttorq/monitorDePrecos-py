# ============================================================
# scraper.py — Coleta de preços via API pública do Kabum
# Sem autenticação necessária, funciona perfeitamente na nuvem
# ============================================================

import requests

BASE_URL = "https://servicespub.prod.api.btgpactual.kabum.com.br/product/v1/products"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept":     "application/json",
}


def coletar_preco(busca, nome_produto):
    """
    Busca o menor preço de um produto na API pública do Kabum.

    Parâmetros:
        busca (str)        — termo de busca (ex: "teclado aula hero68")
        nome_produto (str) — nome amigável para exibir no log

    Retorna:
        float — menor preço encontrado
        None  — se não encontrar
    """
    print(f"\n🔍 Buscando: {nome_produto}")

    params = {
        "page_number": 1,
        "page_size":   20,
        "smart_filter": busca,
        "sort_by":     "lower_price",   # Já retorna do menor pro maior
    }

    try:
        resposta = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
        resposta.raise_for_status()

        dados      = resposta.json()
        produtos   = dados.get("data", [])

        if not produtos:
            print(f"   ⚠️ Nenhum resultado encontrado.")
            return None

        precos = [
            p["vlr_preco_desconto"] if p.get("vlr_preco_desconto") else p["vlr_preco"]
            for p in produtos
            if p.get("vlr_preco") and p.get("des_indisponivel") is False
        ]

        if precos:
            menor = min(precos)
            print(f"   ✅ Menor preço: R$ {menor:.2f} ({len(precos)} ofertas)")
            return menor

        print(f"   ⚠️ Nenhum preço disponível.")
        return None

    except requests.exceptions.RequestException as erro:
        print(f"   ❌ Erro na requisição: {erro}")
        return None

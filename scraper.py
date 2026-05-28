# ============================================================
# scraper.py — Coleta de preços do Kabum
# Usa requests + BeautifulSoup para fazer web scraping
# ============================================================

import requests
from bs4 import BeautifulSoup
import time
import random
import re
import json

# Headers que simulam um navegador real
# Sem isso, o site pode bloquear a requisição
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


def coletar_preco(url, nome_produto):
    """
    Coleta o preço de um produto diretamente da página do Kabum.

    Estratégia em 3 etapas (da mais confiável pra menos):
      1. Lê o JSON embutido no HTML (__NEXT_DATA__) — mais preciso
      2. Tenta seletores CSS modernos do Kabum
      3. Busca qualquer padrão "R$ 000,00" na página — fallback geral

    Parâmetros:
        url (str)          — link direto do produto no Kabum
        nome_produto (str) — nome para exibir no terminal

    Retorna:
        float — preço encontrado
        None  — se não conseguir coletar
    """
    print(f"\n🔍 Buscando: {nome_produto}")
    print(f"   URL: {url}")

    # Delay aleatório entre 2 e 5 segundos
    # Imita comportamento humano e evita bloqueio por excesso de requisições
    time.sleep(random.uniform(2, 5))

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # ── Estratégia 1: JSON embutido (__NEXT_DATA__) ──────────────────
        # O Kabum é feito em Next.js e injeta todos os dados da página
        # em uma tag <script id="__NEXT_DATA__"> no HTML.
        # Essa é a forma mais confiável de pegar o preço.
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag and script_tag.string:
            try:
                dados = json.loads(script_tag.string)

                # Caminho dentro do JSON onde o preço fica
                props = dados.get("props", {}).get("pageProps", {})
                produto = props.get("productData", props.get("initialState", {}))

                preco_desconto = produto.get("priceWithDiscount")
                preco_normal   = produto.get("vlr_preco") or produto.get("price")

                # Prefere o preço com desconto se existir
                preco = preco_desconto or preco_normal
                if preco and float(preco) > 1:
                    print(f"   ✅ Preço encontrado no JSON: R$ {float(preco):.2f}")
                    return float(preco)

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"   ⚠️  JSON não trouxe o preço ({e}), tentando seletores CSS...")

        # ── Estratégia 2: Seletores CSS modernos do Kabum ────────────────
        # Atributos data-testid são mais estáveis que classes CSS
        seletores = [
            '[data-testid="product-price"]',
            '[data-testid="priceCard"]',
            "h4.sc-5492faee-2",       # Preço principal atual do Kabum
            "span.sc-5492faee-0",     # Preço alternativo
            ".finalPrice",
            ".regularPrice",
        ]

        for seletor in seletores:
            elemento = soup.select_one(seletor)
            if elemento:
                texto = elemento.get_text(strip=True)
                match = re.search(r"[\d]+(?:[.,]\d+)*", texto.replace(".", "").replace(",", "."))
                if match:
                    try:
                        preco = float(match.group())
                        if preco > 1:
                            print(f"   ✅ Preço encontrado via CSS '{seletor}': R$ {preco:.2f}")
                            return preco
                    except ValueError:
                        continue

        # ── Estratégia 3: Busca por padrão R$ no texto da página ─────────
        # Último recurso: varre o HTML inteiro procurando "R$ 000,00"
        texto_pagina = soup.get_text()
        matches = re.findall(r"R?\$\s*(\d{1,5}(?:[.,]\d{3})*(?:[.,]\d{2})?)", texto_pagina)

        precos = []
        for m in matches:
            try:
                valor = float(m.replace(".", "").replace(",", "."))
                if valor > 1:
                    precos.append(valor)
            except ValueError:
                continue

        if precos:
            preco = min(precos)
            print(f"   ✅ Preço encontrado por busca geral: R$ {preco:.2f}")
            return preco

        print(f"   ⚠️  Preço não encontrado na página.")
        return None

    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout — página demorou demais para responder.")
        return None
    except requests.exceptions.RequestException as erro:
        print(f"   ❌ Erro na requisição: {erro}")
        return None

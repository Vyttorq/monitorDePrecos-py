import requests
from bs4 import BeautifulSoup
import time
import random
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
}

def coletar_preco(url, nome_produto):
    """
    Coleta o preço de um produto diretamente do site do Kabum usando BeautifulSoup.
    """
    print(f"\n🔍 Buscando: {nome_produto}")
    print(f"   URL: {url}")
    
    try:
        # Adiciona delay aleatório
        time.sleep(random.uniform(2, 5))
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tenta múltiplos seletores comuns do Kabum
        selectors = [
            'meta[property="product:price:amount"]',
            'div.preco_desconto_avista',
            'span.preco_desconto',
            'div.preco_promocao',
            'div.preco',
            'span.preco_por',
            'div.preco_a_vista',
            'div.price',
            'span.price',
            '[data-testid="product-price"]',
            '.price-current'
        ]
        
        preco = None
        
        # Tenta cada seletor
        for selector in selectors:
            elemento = soup.select_one(selector)
            if elemento:
                preco_text = elemento.get_text(strip=True)
                print(f"   Elemento encontrado com seletor: {selector}")
                print(f"   Texto encontrado: {preco_text}")
                
                # Extrai números e vírgulas
                preco_match = re.search(r'[\d,]+(?:\.\d+)?', preco_text)
                if preco_match:
                    preco_str = preco_match.group().replace('.', '').replace(',', '.')
                    preco = float(preco_str)
                    print(f"   ✅ Preço encontrado: R$ {preco:.2f}")
                    return preco
        
        # Se não encontrou com seletores específicos, tenta buscar por texto
        if not preco:
            # Procura por texto que contenha "R$" ou "preço"
            textos = soup.get_text()
            preco_match = re.search(r'R?\$?\s*([\d,]+(?:\.\d+)?)', textos)
            if preco_match:
                preco_str = preco_match.group(1).replace('.', '').replace(',', '.')
                preco = float(preco_str)
                print(f"   ✅ Preço encontrado por busca textual: R$ {preco:.2f}")
                return preco
        
        print(f"   ⚠️  Preço não encontrado na página")
        print(f"   📋 Conteúdo da página (primeiros 500 caracteres): {response.text[:500]}")
        return None
        
    except Exception as erro:
        print(f"   ❌ Erro ao coletar preço: {erro}")
        import traceback
        traceback.print_exc()
        return None

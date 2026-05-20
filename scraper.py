# ============================================================
# scraper.py — Coleta de preços via scraping direto do Kabum
# ============================================================

import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def coletar_preco(url, nome_produto):
    """
    Coleta o preço de um produto diretamente do site do Kabum usando BeautifulSoup.
    
    Parâmetros:
        url (str)          — URL completa do produto
        nome_produto (str) — nome amigável para exibir no log

    Retorna:
        float — preço encontrado
        None  — se não encontrar
    """
    print(f"\n🔍 Buscando: {nome_produto}")
    print(f"   URL: {url}")
    
    try:
        # Adiciona um pequeno delay aleatório para evitar bloqueios
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tenta encontrar o preço principal
        preco_elemento = soup.find('meta', {'property': 'product:price:amount'})
        
        if preco_elemento:
            preco_text = preco_elemento.get('content', '')
            preco = float(preco_text.replace(',', '.'))
            print(f"   ✅ Preço encontrado: R$ {preco:.2f}")
            return preco
        else:
            # Tenta outros seletores comuns
            preco_elemento = soup.find('div', class_='preco_desconto_avista')
            if not preco_elemento:
                preco_elemento = soup.find('span', class_='preco_desconto')
            if not preco_elemento:
                preco_elemento = soup.find('div', class_='preco_promocao')
            
            if preco_elemento:
                preco_text = preco_elemento.get_text(strip=True)
                # Extrai apenas os números e vírgulas
                import re
                preco_match = re.search(r'[\d,]+', preco_text)
                if preco_match:
                    preco_str = preco_match.group().replace(',', '.')
                    preco = float(preco_str)
                    print(f"   ✅ Preço encontrado: R$ {preco:.2f}")
                    return preco
        
        print(f"   ⚠️  Preço não encontrado na página")
        return None
        
    except Exception as erro:
        print(f"   ❌ Erro ao coletar preço: {erro}")
        return None


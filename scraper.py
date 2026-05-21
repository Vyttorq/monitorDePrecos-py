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
        
        # Tenta encontrar o preço principal (mais comum no Kabum)
        preco = None
        
        # Seletores específicos para Kabum
        selectors = [
            'span.preco_desconto_avista',
            'div.preco_desconto',
            'span.preco_promocao',
            'div.preco_a_vista',
            'div.preco',
            'span.preco_por',
            'div.price-current',
            '[data-testid="product-price"]',
            'meta[property="product:price:amount"]'
        ]
        
        # Primeiro tenta os seletores específicos
        for selector in selectors:
            elementos = soup.select(selector)
            if elementos:
                for elemento in elementos:
                    texto = elemento.get_text(strip=True)
                    # Procura por valores monetários
                    preco_match = re.search(r'R?\$?\s*([\d,]+(?:\.\d+)?)', texto)
                    if preco_match:
                        preco_str = preco_match.group(1).replace('.', '').replace(',', '.')
                        try:
                            preco = float(preco_str)
                            print(f"   ✅ Preço encontrado com seletor '{selector}': R$ {preco:.2f}")
                            return preco
                        except:
                            continue
        
        # Se não encontrou com seletores específicos, faz busca mais ampla
        if not preco:
            # Procura por todos os elementos que contêm "R$" ou "preço"
            textos = soup.get_text()
            # Busca por padrão de preço: R$ 1.234,56 ou R$ 1234.56
            preco_matches = re.findall(r'R?\$\s*(\d+(?:\.\d+)?(?:,\d+)?)', textos)
            
            if preco_matches:
                # Pega o primeiro preço maior que 1 (evita preços muito baixos)
                for match in preco_matches:
                    try:
                        preco_str = match.replace('.', '').replace(',', '.')
                        preco = float(preco_str)
                        if preco > 1:  # Evita preços muito baixos
                            print(f"   ✅ Preço encontrado por busca ampla: R$ {preco:.2f}")
                            return preco
                    except:
                        continue
        
        # Se ainda não encontrou, tenta encontrar o preço mais alto (que é o preço real)
        if not preco:
            # Busca todos os números que parecem preços
            all_numbers = re.findall(r'\d+(?:\.\d+)?(?:,\d+)?', textos)
            if all_numbers:
                # Converte todos para float e encontra o maior
                precos = []
                for num in all_numbers:
                    try:
                        cleaned = num.replace('.', '').replace(',', '.')
                        preco_num = float(cleaned)
                        if preco_num > 1:  # Apenas preços razoáveis
                            precos.append(preco_num)
                    except:
                        continue
                
                if precos:
                    # Pega o maior preço (geralmente o preço real)
                    preco = max(precos)
                    print(f"   ✅ Preço encontrado como maior valor: R$ {preco:.2f}")
                    return preco
        
        print(f"   ⚠️  Preço não encontrado na página")
        return None
        
    except Exception as erro:
        print(f"   ❌ Erro ao coletar preço: {erro}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================
# scraper.py — Coleta de preços com Selenium
# ============================================================

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def criar_driver():
    """
    Cria o driver uma única vez.
    Ele será reutilizado para todos os produtos.
    """
    opcoes = uc.ChromeOptions()
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=opcoes, use_subprocess=True)
    return driver


def coletar_preco(driver, url, nome_produto):
    """
    Acessa a URL e retorna o menor preço encontrado.
    Recebe o driver já criado — não abre janela nova.
    """
    try:
        print(f"\n🔍 Buscando: {nome_produto}")
        driver.get(url)

        # Espera os preços aparecerem (máx 10 segundos)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "andes-money-amount__fraction")
            )
        )

        time.sleep(1)  # Pausa curta após carregamento

        elementos = driver.find_elements(
            By.CLASS_NAME, "andes-money-amount__fraction"
        )

        precos = []
        for el in elementos:
            try:
                texto = el.text.strip()
                if not texto:
                    continue
                preco = float(texto.replace(".", "").replace(",", "."))
                if preco > 1:
                    precos.append(preco)
            except ValueError:
                continue

        if precos:
            menor = min(precos)
            print(f"   ✅ Menor preço: R$ {menor:.2f}")
            return menor

        # Debug: salva HTML se não encontrar preços
        print(f"   ⚠️ Nenhum preço encontrado. Salvando HTML para debug...")
        with open(f"debug_{nome_produto[:20].replace(' ', '_')}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return None

    except Exception as erro:
        print(f"   ❌ Erro: {erro}")
        return None

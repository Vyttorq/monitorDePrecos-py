# ============================================================
# scraper.py — Coleta de preços com Selenium
# Versão cloud: usa Selenium padrão (Chrome já vem no GitHub Actions)
# ============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def criar_driver():
    """
    Configura o Chrome para rodar na nuvem (sem interface gráfica).
    O GitHub Actions já tem o Chrome instalado na máquina virtual.
    """
    opcoes = Options()
    opcoes.add_argument("--headless")                # Sem janela (obrigatório na nuvem)
    opcoes.add_argument("--no-sandbox")              # Obrigatório no Linux da nuvem
    opcoes.add_argument("--disable-dev-shm-usage")   # Evita erros de memória
    opcoes.add_argument("--window-size=1920,1080")
    opcoes.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=opcoes)
    return driver


def coletar_preco(driver, url, nome_produto):
    """
    Navega até a URL e retorna o menor preço encontrado.
    Reutiliza o driver já aberto — não abre novo Chrome.
    """
    try:
        print(f"\n🔍 Buscando: {nome_produto}")
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "andes-money-amount__fraction")
            )
        )

        time.sleep(1)

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

        print(f"   ⚠️ Nenhum preço encontrado.")
        return None

    except Exception as erro:
        print(f"   ❌ Erro: {erro}")
        return None

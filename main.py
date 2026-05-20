# ============================================================
# main.py — Ponto de entrada do Bot
# Execute: python main.py
# ============================================================

import schedule
import time
from datetime import datetime

from config import (
    PRODUTOS,
    EMAIL_REMETENTE,
    EMAIL_SENHA,
    EMAIL_DESTINATARIO,
    INTERVALO_SEGUNDOS,
    ARQUIVO_CSV,
)
from scraper import criar_driver, coletar_preco
from storage import salvar_preco
from notifier import enviar_alerta


def verificar_precos(driver):
    """
    Percorre todos os produtos usando o mesmo driver já aberto.
    """
    print(f"\n{'=' * 52}")
    print(f"  🤖 Verificação iniciada — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'=' * 52}")

    for produto in PRODUTOS:
        nome   = produto["nome"]
        url    = produto["url"]
        limite = produto["preco_alerta"]

        preco_atual = coletar_preco(driver, url, nome)  # ← passa o driver existente

        if preco_atual is None:
            print(f"   ⚠️  Pulando '{nome}' — não foi possível coletar.\n")
            continue

        salvar_preco(ARQUIVO_CSV, nome, url, preco_atual)

        if preco_atual <= limite:
            print(f"   🚨 ALERTA! Preço abaixo do limite!")
            enviar_alerta(
                remetente    = EMAIL_REMETENTE,
                senha        = EMAIL_SENHA,
                destinatario = EMAIL_DESTINATARIO,
                nome_produto = nome,
                preco_atual  = preco_atual,
                preco_limite = limite,
                url          = url,
            )
        else:
            diferenca = preco_atual - limite
            print(f"   📊 R$ {preco_atual:.2f} | Faltam R$ {diferenca:.2f} pro alerta\n")

    print(f"\n  ✅ Verificação concluída!")
    print(f"  ⏳ Próxima em {INTERVALO_SEGUNDOS // 60} minuto(s)...\n")


if __name__ == "__main__":
    print("🚀 Bot de Monitoramento de Preços iniciado!")
    print(f"📋 {len(PRODUTOS)} produto(s) na lista")
    print("🌐 Abrindo navegador...\n")

    driver = criar_driver()  # ← Chrome abre UMA vez só

    try:
        verificar_precos(driver)

        schedule.every(INTERVALO_SEGUNDOS).seconds.do(verificar_precos, driver)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Bot encerrado pelo usuário.")

    finally:
        driver.quit()  # ← Fecha o Chrome ao sair

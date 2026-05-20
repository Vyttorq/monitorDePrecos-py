# ============================================================
# main.py — Ponto de entrada do Bot (versão simplificada)
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
from scraper import coletar_preco
from storage import salvar_preco
from notifier import enviar_alerta


def verificar_precos():
    """Verifica preços de todos os produtos."""
    print(f"\n{'=' * 52}")
    print(f"  🤖 Verificação iniciada — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'=' * 52}")

    for produto in PRODUTOS:
        nome   = produto["nome"]
        url    = produto["url"]
        limite = produto["preco_alerta"]

        preco_atual = coletar_preco(url, nome)

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
            diferenca = limite - preco_atual
            print(f"   📊 R$ {preco_atual:.2f} | Faltam R$ {diferenca:.2f} pro alerta\n")

    print(f"\n  ✅ Verificação concluída!")
    print(f"  ⏳ Próxima em {INTERVALO_SEGUNDOS // 60} minuto(s)...\n")


if __name__ == "__main__":
    print("🚀 Bot de Monitoramento de Preços iniciado!")
    print(f"📋 {len(PRODUTOS)} produto(s) na lista")
    print("🌐 Iniciando verificação...\n")

    try:
        verificar_precos()
        schedule.every(INTERVALO_SEGUNDOS).seconds.do(verificar_precos)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Bot encerrado pelo usuário.")

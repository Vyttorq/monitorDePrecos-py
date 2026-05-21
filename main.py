# ============================================================
# main.py — Ponto de entrada do Bot
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
    BLACKLIST  # Adicionado
)
from scraper import coletar_preco
from storage import salvar_preco
from notifier import enviar_alerta

def verificar_precos():
    """
    Percorre todos os produtos e verifica os preços.
    """
    print(f"\n{'=' * 52}")
    print(f"  🤖 Verificação iniciada — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'=' * 52}")

    for produto in PRODUTOS:
        nome   = produto["nome"]
        url    = produto["url"]
        limite = produto["preco_alerta"]

        # Verifica se produto está na blacklist
        if any(termo.lower() in nome.lower() for termo in BLACKLIST):
            print(f"   ⚠️  Produto '{nome}' está na blacklist - pulando")
            continue

        preco_atual = coletar_preco(url, nome)

        if preco_atual:
            # Salva no CSV
            print(f"   💾 Salvo: {nome} — R$ {preco_atual:.2f}")
            salvar_preco(nome, preco_atual)
            
            # Verifica se está abaixo do limite
            if preco_atual <= limite:
                print(f"   🚨 ALERTA! {nome} está abaixo do preço limite de R$ {limite:.2f}")
                print(f"   📈 Preço atual: R$ {preco_atual:.2f}")
                try:
                    enviar_alerta(nome, preco_atual, limite, url)
                except Exception as e:
                    print(f"   ❌ Falha ao enviar e-mail: {e}")
        else:
            print(f"   ⚠️  Não foi possível coletar preço para '{nome}'")

    print(f"  ✅ Verificação concluída!")
    print(f"  📊 Produtos verificados: {len(PRODUTOS)}")

# ... resto do código


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

# ============================================================
# run_once.py — Ponto de entrada para a nuvem (GitHub Actions)
#
# Diferente do main.py (que fica em loop infinito),
# este roda UMA verificação e encerra — perfeito para
# execuções agendadas pelo GitHub Actions.
# ============================================================

from datetime import datetime
from scraper import criar_driver, coletar_preco
from storage import salvar_preco
from notifier import enviar_alerta
from config import (
    PRODUTOS,
    EMAIL_REMETENTE,
    EMAIL_SENHA,
    EMAIL_DESTINATARIO,
    ARQUIVO_CSV,
)


def main():
    print(f"\n{'=' * 52}")
    print(f"  🤖 Verificação iniciada — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  ☁️  Rodando na nuvem via GitHub Actions")
    print(f"{'=' * 52}")

    driver = criar_driver()

    try:
        for produto in PRODUTOS:
            nome   = produto["nome"]
            url    = produto["url"]
            limite = produto["preco_alerta"]

            preco_atual = coletar_preco(driver, url, nome)

            if preco_atual is None:
                print(f"   ⚠️  Pulando '{nome}'\n")
                continue

            salvar_preco(ARQUIVO_CSV, nome, url, preco_atual)

            if preco_atual <= limite:
                print(f"   🚨 ALERTA! Enviando e-mail...")
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

    finally:
        driver.quit()

    print(f"\n  ✅ Verificação concluída!\n")


if __name__ == "__main__":
    main()

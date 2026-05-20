# ============================================================
# run_once.py — Entrada para a nuvem (GitHub Actions)
# ============================================================

from datetime import datetime
from scraper import obter_token, coletar_preco
from storage import salvar_preco
from notifier import enviar_alerta
from config import (
    PRODUTOS,
    ML_CLIENT_ID, ML_CLIENT_SECRET,
    EMAIL_REMETENTE, EMAIL_SENHA, EMAIL_DESTINATARIO,
    ARQUIVO_CSV,
)


def main():
    print(f"\n{'=' * 52}")
    print(f"  🤖 Verificação iniciada — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  ☁️  Rodando na nuvem via GitHub Actions")
    print(f"{'=' * 52}\n")

    # Autentica uma vez e reutiliza o token para todos os produtos
    token = obter_token(ML_CLIENT_ID, ML_CLIENT_SECRET)

    for produto in PRODUTOS:
        nome   = produto["nome"]
        busca  = produto["busca"]
        limite = produto["preco_alerta"]

        preco_atual = coletar_preco(busca, nome, token)

        if preco_atual is None:
            print(f"   ⚠️  Pulando '{nome}'\n")
            continue

        salvar_preco(ARQUIVO_CSV, nome, busca, preco_atual)

        if preco_atual <= limite:
            print(f"   🚨 ALERTA! Enviando e-mail...")
            enviar_alerta(
                remetente    = EMAIL_REMETENTE,
                senha        = EMAIL_SENHA,
                destinatario = EMAIL_DESTINATARIO,
                nome_produto = nome,
                preco_atual  = preco_atual,
                preco_limite = limite,
                url          = f"https://lista.mercadolivre.com.br/{busca.replace(' ', '-')}",
            )
        else:
            diferenca = preco_atual - limite
            print(f"   📊 R$ {preco_atual:.2f} | Faltam R$ {diferenca:.2f} pro alerta\n")

    print(f"\n  ✅ Verificação concluída!\n")


if __name__ == "__main__":
    main()

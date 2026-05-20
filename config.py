# ============================================================
# config.py — Configurações do Bot
# ============================================================

import os

# Produtos para monitorar
# "busca" é o termo enviado pra API do Mercado Livre
PRODUTOS = [
    {
        "nome":         "Teclado Aula Hero68HE",
        "busca":        "teclado aula hero68 he",
        "preco_alerta": 500.00
    },
    {
        "nome":         "Mouse Attack Shark X3",
        "busca":        "mouse attack shark x3",
        "preco_alerta": 200.00
    },
]

# Credenciais lidas das variáveis de ambiente (GitHub Secrets na nuvem)
EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA", "")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "")

INTERVALO_SEGUNDOS = 3600
ARQUIVO_CSV        = "historico_precos.csv"

# ============================================================
# config.py — Configurações do Bot
# ============================================================

import os

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

# Credenciais do app Mercado Livre (developers.mercadolivre.com.br)
ML_CLIENT_ID     = os.getenv("ML_CLIENT_ID", "")
ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET", "")

# Credenciais de e-mail
EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA", "")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "")

INTERVALO_SEGUNDOS = 3600
ARQUIVO_CSV        = "historico_precos.csv"

# ============================================================
# config.py — Configurações do Bot
#
# As credenciais de e-mail são lidas das variáveis de ambiente.
# - Localmente: defina as variáveis no seu terminal ou use um .env
# - Na nuvem: cadastre nos Secrets do GitHub (Settings > Secrets)
# ============================================================

import os

PRODUTOS = [
    {
        "nome": "Teclado Aula Hero68HE",
        "url": "https://lista.mercadolivre.com.br/teclado-aula-hero68he",
        "preco_alerta": 200.00
    },
    {
        "nome": "Mouse Attack Shark X3",
        "url": "https://lista.mercadolivre.com.br/mouse-attack-shark-x3",
        "preco_alerta": 100.00
    },
    {
        "nome": "Notebook Dell Inspiron 15",
        "url": "https://lista.mercadolivre.com.br/notebook-dell-inspiron-15",
        "preco_alerta": 3500.00
    },
    {
        "nome": "Smartphone Samsung Galaxy S25",
        "url": "https://lista.mercadolivre.com.br/smartphone-samsung-galaxy-s25",
        "preco_alerta": 3500.00
    }
]

# Lê as credenciais das variáveis de ambiente (seguro — nunca no código!)
EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA", "")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "")

INTERVALO_SEGUNDOS = 3600
ARQUIVO_CSV        = "historico_precos.csv"

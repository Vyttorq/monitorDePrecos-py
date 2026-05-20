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
        "nome": "Teclado Mecânico",
        "url": "https://lista.mercadolivre.com.br/teclado-mecanico",
        "preco_alerta": 200.00
    },
    {
        "nome": "Mouse Gamer",
        "url": "https://lista.mercadolivre.com.br/mouse-gamer",
        "preco_alerta": 100.00
    },
]

# Lê as credenciais das variáveis de ambiente (seguro — nunca no código!)
EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA", "")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "")

INTERVALO_SEGUNDOS = 3600
ARQUIVO_CSV        = "historico_precos.csv"

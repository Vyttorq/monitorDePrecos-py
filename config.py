# ============================================================
# config.py — Configurações do Bot
# ============================================================

import os

PRODUTOS = [
    {
        "nome":         "Teclado MCHOSE Ace 68HE",
        "url":          "https://www.kabum.com.br/produto/730018/teclado-magnetico-gamer-mchose-ace-68-hall-effect-rgb-switch-magnetico-uranus-esports-topografico-branco-mc-ace68-16",
        "preco_alerta": 269.99
    },
    {
        "nome":         "Mouse Attack Shark X3",
        "url":          "https://www.kabum.com.br/produto/904358/mouse-gamer-sem-fio-attack-shark-x3-tri-mode-26-000-dpi-sensor-optico-paw3395-6-botoes-programaveis-preto",
        "preco_alerta": 199.99
    },
]

EMAIL_REMETENTE    = os.getenv("EMAIL_REMETENTE", "")
EMAIL_SENHA        = os.getenv("EMAIL_SENHA", "")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "")

INTERVALO_SEGUNDOS = 3600
ARQUIVO_CSV        = "historico_precos.csv"


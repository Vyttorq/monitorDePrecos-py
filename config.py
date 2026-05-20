# ============================================================
# config.py — Configurações do Bot
# Edite este arquivo para adicionar seus produtos e e-mail
# ============================================================

# Lista de produtos para monitorar
# Adicione quantos quiser seguindo o mesmo padrão
PRODUTOS = [
    {
        "nome": "Teclado Magnético Aula Hero68 HE",
        "url": "https://lista.mercadolivre.com.br/teclado-hero68-he",
        "preco_alerta": 260.00  # Avisa se o preço cair abaixo disso
    },
    {
        "nome": "Mouse Attack Shark X3",
        "url": "https://lista.mercadolivre.com.br/mouse-attack-shark-x3",
        "preco_alerta": 230.00
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

# ⚠️ IMPORTANTE: Use uma "Senha de App" do Gmail, não sua senha normal
# Como gerar: myaccount.google.com > Segurança > Senhas de app
EMAIL_REMETENTE    = "seu_email@gmail.com"
EMAIL_SENHA        = "sua_senha_de_app_aqui"
EMAIL_DESTINATARIO = "seu_email@gmail.com"

# Intervalo entre verificações (em segundos)
# 3600 = 1 hora | 1800 = 30 min | 600 = 10 min
INTERVALO_SEGUNDOS = 3600

# Nome do arquivo onde o histórico será salvo
ARQUIVO_CSV = "historico_precos.csv"

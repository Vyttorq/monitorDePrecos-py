# ============================================================
# notifier.py — Envio de alertas por e-mail
# Usa Gmail via SMTP para notificar quando o preço cai
# ============================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_alerta(remetente, senha, destinatario, nome_produto, preco_atual, preco_limite, url):
    """
    Envia um e-mail de alerta quando o preço atingiu o limite desejado.

    Parâmetros:
        remetente    (str) — seu e-mail Gmail
        senha        (str) — senha de app do Gmail
        destinatario (str) — quem vai receber o alerta
        nome_produto (str) — nome do produto
        preco_atual  (float) — preço coletado agora
        preco_limite (float) — seu limite configurado
        url          (str) — link do produto

    Retorna:
        True  — e-mail enviado com sucesso
        False — falhou
    """
    assunto = f"🔔 Alerta de Preço: {nome_produto} por R$ {preco_atual:.2f}!"

    corpo = f"""Olá!

O preço do produto que você monitora atingiu seu limite!

📦 Produto : {nome_produto}
💰 Preço   : R$ {preco_atual:.2f}
🎯 Limite  : R$ {preco_limite:.2f}
🔗 Link    : {url}

Corra antes que acabe! 🚀

---
Bot de Monitoramento de Preços 🤖
"""

    msg = MIMEMultipart()
    msg["From"]    = remetente
    msg["To"]      = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatario, msg.as_string())

        print(f"   📧 Alerta enviado para {destinatario}!")
        return True

    except Exception as erro:
        print(f"   ❌ Falha ao enviar e-mail: {erro}")
        return False

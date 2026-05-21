def enviar_alerta(nome_produto, preco_atual, preco_limite, url_produto):
    """
    Envia alerta por e-mail quando o preço está abaixo do limite
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # Configuração do e-mail
    remetente = os.getenv('EMAIL_REMETENTE')
    senha = os.getenv('EMAIL_SENHA')
    destinatario = os.getenv('EMAIL_DESTINATARIO')
    
    # Criação da mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"ALERTA: {nome_produto} - Preço Abaixo do Limite!"
    
    # Conteúdo do e-mail
    corpo = f"""
    ⚠️  ALERTA DE PREÇO - {nome_produto}
    
    📉 Preço Atual: R$ {preco_atual:.2f}
    🎯 Preço Limite: R$ {preco_limite:.2f}
    📊 Diferença: R$ {preco_limite - preco_atual:.2f}
    
    🔗 Link do produto: {url_produto}
    
    ⚠️  Este é o preço com desconto. O preço á vista pode ser diferente.
    
    Atenciosamente,
    Bot de Monitoramento
    """
    
    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
    
    # Envio do e-mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        text = msg.as_string()
        server.sendmail(remetente, destinatario, text)
        server.quit()
        print(f"   ✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"   ❌ Falha ao enviar e-mail: {e}")
        raise

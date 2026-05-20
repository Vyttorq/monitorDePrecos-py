# 🤖 Bot de Monitoramento de Preços

Bot em Python que monitora preços no Mercado Livre e envia alertas por e-mail quando o preço cai abaixo de um limite configurado.

## 🚀 Tecnologias

- **Python 3.10+**
- **Selenium** — automação do navegador (RPA)
- **schedule** — agendamento de tarefas
- **smtplib** — envio de e-mails (nativo do Python)
- **csv** — armazenamento de histórico (nativo do Python)

## 📁 Estrutura do Projeto

```
price-monitor/
│
├── main.py          # Ponto de entrada — execute este arquivo
├── scraper.py       # Coleta de preços com Selenium
├── storage.py       # Leitura e escrita do histórico CSV
├── notifier.py      # Envio de alertas por e-mail
├── config.py        # Produtos, e-mail e configurações
├── requirements.txt # Dependências do projeto
└── README.md        # Este arquivo
```

## ⚙️ Como usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/price-monitor.git
cd price-monitor
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o `config.py`
- Adicione os produtos que quer monitorar
- Configure seu e-mail e senha de app do Gmail
  - Como gerar senha de app: [myaccount.google.com](https://myaccount.google.com) → Segurança → Senhas de app

### 4. Rode o bot
```bash
python main.py
```

## 📊 Histórico de preços

Cada execução salva os preços coletados em `historico_precos.csv`:

| data_hora | produto | url | preco |
|---|---|---|---|
| 20/05/2026 10:00 | Teclado Mecânico | https://... | 189.90 |

## 💡 Como adicionar um novo produto

No `config.py`, adicione um item à lista `PRODUTOS`:

```python
{
    "nome": "Headset Gamer",
    "url": "https://lista.mercadolivre.com.br/headset-gamer",
    "preco_alerta": 150.00
}
```

## 🔮 Próximas melhorias (roadmap)

- [ ] Suporte a outros sites (Amazon, Kabum)
- [ ] Gráfico de evolução de preços com matplotlib
- [ ] Interface web simples com Flask
- [ ] Notificação via WhatsApp (Twilio)
- [ ] Deploy em servidor para rodar 24/7

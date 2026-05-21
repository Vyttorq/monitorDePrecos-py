# 🤖 Bot de Monitoramento de Preços

Bot em Python que monitora preços no **Kabum** e envia alertas por e-mail quando o preço cai abaixo de um limite configurado. Roda automaticamente na nuvem via **GitHub Actions** — sem precisar deixar o computador ligado.

## 🚀 Tecnologias

- **Python 3.11**
- **requests + BeautifulSoup4** — coleta de preços via web scraping
- **GitHub Actions** — agendamento e execução na nuvem (CI/CD)
- **smtplib** — envio de alertas por e-mail (nativo do Python)
- **csv** — histórico de preços (nativo do Python)

## 📁 Estrutura do Projeto

```
monitorDePrecos-py/
│
├── .github/
│   └── workflows/
│       └── monitor.yml  # Agendamento automático na nuvem
│
├── run_once.py          # Entrada para a nuvem — roda 1 ciclo e encerra
├── main.py              # Entrada local — roda em loop contínuo
├── scraper.py           # Coleta de preços com requests + BeautifulSoup
├── storage.py           # Leitura e escrita do histórico em CSV
├── notifier.py          # Envio de alertas por e-mail
├── config.py            # Produtos monitorados e configurações
└── requirements.txt     # Dependências do projeto
```

## ⚙️ Como funciona

```
GitHub Actions (a cada 1h)
        │
        ▼
   run_once.py
        │
        ├── scraper.py  →  Acessa o Kabum e coleta o preço atual
        ├── storage.py  →  Salva no histórico (historico_precos.csv)
        └── notifier.py →  Envia e-mail se o preço atingir o limite
```

## 🚀 Deploy no GitHub Actions

### 1. Clone o repositório
```bash
git clone https://github.com/Vyttorq/monitorDePrecos-py.git
cd monitorDePrecos-py
```

### 2. Instale as dependências (para rodar localmente)
```bash
pip install -r requirements.txt
```

### 3. Configure os Secrets no GitHub
Vá em **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|---|---|
| `EMAIL_REMETENTE` | seu_email@gmail.com |
| `EMAIL_SENHA` | senha de app do Gmail |
| `EMAIL_DESTINATARIO` | email que vai receber o alerta |

> 💡 Como gerar senha de app: [myaccount.google.com](https://myaccount.google.com) → Segurança → Senhas de app

### 4. Pronto!
O bot vai rodar automaticamente a cada hora.
Para rodar manualmente: **Actions → 🤖 Monitor de Preços → Run workflow**

## 💡 Como adicionar um produto

No `config.py`, adicione um item à lista `PRODUTOS`:

```python
{
    "nome": "Headset Gamer HyperX",
    "url": "https://www.kabum.com.br/produto/XXXXX/nome-do-produto",
    "preco_alerta": 250.00  # Avisa se o preço cair abaixo disso
}
```

## 📊 Histórico de preços

A cada execução, os preços coletados são salvos em `historico_precos.csv` e commitados automaticamente no repositório:

| data_hora | produto | url | preco |
|---|---|---|---|
| 20/05/2026 10:00 | Teclado MCHOSE Ace 68HE | https://kabum.com.br/... | 259.90 |

## 🔮 Roadmap

- [x] Scraping de preços com BeautifulSoup
- [x] Alertas por e-mail
- [x] Histórico em CSV
- [x] Execução automática via GitHub Actions
- [ ] Gráfico de evolução de preços com matplotlib
- [ ] Suporte a múltiplos sites (Amazon, Pichau)
- [ ] Dashboard web com Flask
- [ ] Notificação via WhatsApp (Twilio)

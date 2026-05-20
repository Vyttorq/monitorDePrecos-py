# 🤖 Bot de Monitoramento de Preços

Bot em Python que monitora preços no Mercado Livre e envia alertas por e-mail quando o preço cai abaixo de um limite. Roda automaticamente na nuvem via **GitHub Actions** — sem precisar deixar computador ligado.

## 🚀 Tecnologias

- **Python 3.11**
- **Selenium** — automação do navegador (RPA)
- **GitHub Actions** — agendamento e execução na nuvem (DevOps/CI-CD)
- **smtplib** — envio de e-mails (nativo do Python)
- **csv** — histórico de preços (nativo do Python)

## 📁 Estrutura

```
price-monitor/
│
├── .github/
│   └── workflows/
│       └── monitor.yml  # Agendamento na nuvem (GitHub Actions)
│
├── run_once.py          # Entrada para a nuvem — roda 1 ciclo e encerra
├── main.py              # Entrada local — roda em loop contínuo
├── scraper.py           # Coleta de preços com Selenium
├── storage.py           # Histórico em CSV
├── notifier.py          # Alertas por e-mail
├── config.py            # Produtos e configurações
└── requirements.txt
```

## ⚙️ Deploy no GitHub Actions (nuvem)

### 1. Suba o projeto no GitHub
```bash
git init
git add .
git commit -m "primeiro commit"
git remote add origin https://github.com/SEU-USUARIO/price-monitor.git
git push -u origin main
```

### 2. Cadastre as credenciais de e-mail como Secrets
No GitHub: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|---|---|
| `EMAIL_REMETENTE` | seu_email@gmail.com |
| `EMAIL_SENHA` | senha de app do Gmail |
| `EMAIL_DESTINATARIO` | email que vai receber o alerta |

> Como gerar senha de app: [myaccount.google.com](https://myaccount.google.com) → Segurança → Senhas de app

### 3. Pronto!
O bot vai rodar automaticamente a cada hora. Para rodar na hora: **Actions → Monitor de Preços → Run workflow**

## 📊 Histórico de preços

O histórico é salvo em `historico_precos.csv` e commitado automaticamente no repositório a cada execução.

## 💡 Como adicionar um produto

Em `config.py`:
```python
{
    "nome": "Headset Gamer",
    "url": "https://lista.mercadolivre.com.br/headset-gamer",
    "preco_alerta": 150.00
}
```

## 🔮 Roadmap

- [ ] Suporte a outros sites (Amazon, Kabum)
- [ ] Gráfico de histórico com matplotlib
- [ ] Dashboard web com Flask
- [ ] Notificação via WhatsApp

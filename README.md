# 🤖 Bot de Monitoramento de Preços

> ⚠️ **Projeto em andamento** — funcional, mas em constante melhoria. Veja o [Roadmap](#-roadmap) para os próximos passos.

Bot em Python que monitora preços de produtos no **Kabum** e envia alertas por e-mail quando o preço cai abaixo de um limite configurado. Roda automaticamente na nuvem a cada hora via **GitHub Actions** — sem precisar deixar o computador ligado.

---

## 🚀 Tecnologias

- **Python 3.11**
- **requests + BeautifulSoup4** — web scraping para coleta de preços
- **GitHub Actions** — agendamento e execução automática na nuvem (CI/CD)
- **smtplib** — envio de alertas por e-mail (biblioteca nativa do Python)
- **csv** — armazenamento do histórico de preços (biblioteca nativa do Python)

---

## 📁 Estrutura do Projeto

```
monitorDePrecos-py/
│
├── .github/
│   └── workflows/
│       └── monitor.yml  # Define quando e como o bot roda na nuvem
│
├── run_once.py          # Entrada para a nuvem: roda 1 ciclo e encerra
├── main.py              # Entrada local: roda em loop contínuo
├── scraper.py           # Web scraping com requests + BeautifulSoup
├── storage.py           # Salva e lê o histórico em CSV
├── notifier.py          # Envia alertas por e-mail via Gmail
├── config.py            # Lista de produtos e configurações
└── requirements.txt     # Dependências do projeto
```

---

## ⚙️ Como funciona

```
GitHub Actions (toda hora)
         │
         ▼
    run_once.py
         │
         ├─► scraper.py   →  Acessa o Kabum e coleta o preço atual
         ├─► storage.py   →  Salva o preço no histórico (CSV)
         └─► notifier.py  →  Envia e-mail se o preço atingiu o limite
```

O `scraper.py` tenta extrair o preço em 3 etapas, da mais confiável pra menos:
1. Lê o JSON embutido no HTML (`__NEXT_DATA__`) — mais preciso
2. Tenta seletores CSS modernos da página
3. Busca qualquer padrão `R$ 000,00` no texto — fallback geral

---

## 🛠️ Como usar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/Vyttorq/monitorDePrecos-py.git
cd monitorDePrecos-py
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz (não sobe pro GitHub — já está no `.gitignore`):
```
EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA=sua_senha_de_app
EMAIL_DESTINATARIO=destino@gmail.com
```

> 💡 Como gerar senha de app do Gmail: [myaccount.google.com](https://myaccount.google.com) → Segurança → Senhas de app

### 4. Rode o bot
```bash
python run_once.py    # Uma verificação e encerra
python main.py        # Loop contínuo (uso local)
```

---

## ☁️ Deploy no GitHub Actions (nuvem)

### 1. Faça o fork ou clone e suba no GitHub

### 2. Cadastre os Secrets
Vá em **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|---|---|
| `EMAIL_REMETENTE` | seu_email@gmail.com |
| `EMAIL_SENHA` | senha de app do Gmail |
| `EMAIL_DESTINATARIO` | email que vai receber o alerta |

### 3. Pronto!
O bot roda automaticamente a cada hora. Para rodar na hora:
**Actions → 🤖 Monitor de Preços → Run workflow**

---

## ➕ Como adicionar um novo produto

Abra o `config.py` e adicione um item à lista `PRODUTOS`:

```python
PRODUTOS = [
    {
        "nome": "Nome do produto",                          # Nome para exibir nos logs e e-mails
        "url":  "https://www.kabum.com.br/produto/XXXXX/", # URL direta do produto no Kabum
        "preco_alerta": 250.00                             # Avisa quando o preço cair abaixo disso
    },
]
```

**Como pegar a URL certa:**
1. Acesse o produto desejado no [Kabum](https://www.kabum.com.br)
2. Copie a URL completa da página do produto
3. Cole no campo `"url"` acima

---

## 📊 Histórico de preços

A cada execução bem-sucedida, os preços são salvos em `historico_precos.csv` e commitados automaticamente no repositório:

| data_hora | produto | url | preco |
|---|---|---|---|
| 20/05/2026 10:00 | Teclado MCHOSE Ace 68HE | https://kabum.com.br/... | 259.90 |
| 21/05/2026 10:00 | Teclado MCHOSE Ace 68HE | https://kabum.com.br/... | 249.90 |

---

## 🔮 Roadmap

- [x] Web scraping com BeautifulSoup
- [x] Alertas por e-mail
- [x] Histórico de preços em CSV
- [x] Execução automática na nuvem via GitHub Actions
- [x] Delay aleatório para evitar bloqueios
- [ ] Gráfico de evolução de preços com `matplotlib`
- [ ] Suporte a outros sites (Amazon BR, Pichau)
- [ ] Dashboard web simples com Flask
- [ ] Notificação via WhatsApp (Twilio)
- [ ] Testes automatizados

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Abra uma [Issue](https://github.com/Vyttorq/monitorDePrecos-py/issues) ou um Pull Request.

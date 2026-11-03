# 📧 Handler de Emails

**Status:** `🟢 PRONTO PARA CONFIGURAÇÃO SMTP`  
**Criado:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  

---

## 🎯 **OBJETIVO PRINCIPAL**

Agent especializado em **processamento e gestão de emails**:
- ✅ Receber emails via SMTP (webhook ou polling)
- ✅ Categorizar por assunto/prioridade/cliente
- ✅ Responder automaticamente a emails padrão (FAQ)
- ✅ Alertar admin sobre emails urgentes/reclamações

---

## 📂 **ESTRUTURA DO AGENTE**

```
PROJETOS/Emails/
├── README.md                              ← Este arquivo
├── config/                                # Configurações do agente
│   ├── smtp-settings.json                 → SMTP server + credenciais (via Vault)
│   ├── categories.json                    → Categorias de emails (vendas, suporte, feedback, etc.)
│   ├── auto-responses.md                  → Respostas automáticas para FAQ
│   └── alert-rules.yaml                   → Regras para alertar admin (urgente/reclamação)
├── scripts/                               # Scripts Python de automação
│   ├── email-fetcher.py                   → Fetch emails via IMAP/SMTP webhook
│   ├── categorize-emails.py               → Categorizar por assunto/cliente/prioridade
│   ├── auto-responder.py                  → Responder automaticamente a FAQ
│   ├── sentiment-analyzer.py              → Análise de sentimento (positive/negative)
│   └── archive-manager.py                 → Arquivar emails antigos (>90 dias)
├── data/                                  # Dados brutos dos emails
│   ├── raw/                               ← Emails brutos recebidos
│   │   ├── 2026-11-02/
│   │   │   ├── email1.eml
│   │   │   └── email2.eml
│   │   └── ...
│   ├── categorized/                       ← Emails categorizados por tipo
│   │   ├── 2026-11-02/
│   │   │   ├── vendas/
│   │   │   ├── suporte/
│   │   │   ├── feedback/
│   │   │   └── urgentes/
│   │   └── ...
├── reports/                              # Relatórios gerados
│   ├── daily/                            ← Relatórios diários (09:00)
│   │   └── 2026-11-02/daily-report.md
│   └── weekly/                          ← Relatórios semanais (domingo 18:00)
├── memory.md                              ← Memória persistente do agente (isolada)
└── logs/                                  # Logs do agente
    ├── fetch/
    ├── categorization/
    └── responses/
```

---

## 🔄 **FLUXO DE PROCESSAMENTO AUTOMATIZADO**

### **Cronograma de Fetch + Processamento:**

```yaml
Fetch cycle: a cada 15 minutos (configurável)
  ├─ IMAP/SMTP → Pull novos emails da caixa de entrada
  └─ Webhook → Receber emails via endpoint HTTP POST
  
Processamento imediato:
  ├─ Categorizar por assunto (vendas, suporte, feedback, reclamação, etc.)
  ├─ Analisar sentimento (positive/negative/neutral)
  ├─ Aplicar regras de auto-resposta (FAQ padrão)
  ├─ Alertar admin sobre emails urgentes/reclamações
  └─ Arquivar automaticamente (>90 dias sem resposta)

Auto-resposta automática:
  ├─ FAQ técnica → Responder automaticamente
  ├─ Obrigado por contato → Responder com template predefinido
  └─ Pedido de orçamento → Alertar admin imediatamente
```

---

## 📋 **CATEGORIZAÇÃO DE EMAILS**

### **Categorias principais:**

| Categoria | Padrão de Assunto | Ação Automática |
|-----------|------------------|-----------------|
| **Vendas** | "Orçamento", "Preço", "Quanto custa" | Responder template vendas + alertar admin para follow-up |
| **Suporte Técnico** | "Erro", "Problema", "Não funciona" | Alertar admin imediatamente (não auto-responder) |
| **Feedback Positivo** | "Obrigado", "Muito bom", "Excelente" | Responder agradecimento + oferta adicional |
| **Feedback Negativo** | "Reclamação", "Não gostei", "Pior serviço" | Alertar admin imediatamente (urgente!) |
| **FAQ Técnico** | Perguntas sobre produto/serviço | Responder automaticamente com FAQ predefinida |
| **Parceiros/Marketing** | "Colaboração", "Parceria", "Newsletter" | Arquivar automaticamente (não priorizar) |

---

## 🤖 **AUTOMATIZAÇÃO DE RESPOSTAS**

### **Respostas Pré-aprovadas (admin pode adicionar mais):**

```yaml
FAQ Técnica:
  - "Como configurar X?" → Responder template de configuração
  - "Qual a diferença entre plano A e B?" → Responder comparação de planos
  - "Tem desconto para empresas?" → Responder política de preços
  
Obrigado por contato:
  - "Obrigado pelo seu interesse" → Template padrão de agradecimento
  
Reclamação/Urgente:
  - Alertar admin imediatamente (não responder automático)
```

---

## 📊 **ANÁLISE DE SENTIMENTO**

### **Classificação Automática:**

```python
def analisar_sentimento(email_texto: str) -> Dict[str, Any]:
    """
    Classifica sentimento do email
    
    Retorna:
    {
        "sentiment": "positive" | "negative" | "neutral",
        "confidence": 0.82,
        "keywords": ["satisfeito", "ótimo", "excelente"],
        "action_required": False,
        "recommendation": "Responder com agradecimento + oferta adicional"
    }
    """
```

**Thresholds de Ação:**
- **Positive** (confidence > 0.7) → Responder automaticamente com template
- **Neutral** → Arquivar (não requer ação imediata)
- **Negative** (confidence > 0.6) → Alertar admin imediatamente

---

## 🔔 **REGRAS DE ALERTA PARA ADMIN**

### **Condições que exigem atenção imediata:**

```yaml
Emails que alertam admin:
  - 🚨 Assunto com palavras "URGENTE", "IMEDIATAMENTE", "ERRO CRÍTICO"
  - 🚨 Sentimento negativo (confidence > 0.6) + palavra "reclamação"
  - 🚨 Pedido de reembolso ou cancelamento
  - 🚨 Reclamação sobre qualidade de serviço
  - 🚰 Feedback positivo importante (cliente VIP, referência)

Prioridades de alerta:
  🔴 CRÍTICO → Responder em <1 hora (reclamação, erro crítico)
  🟠 ALERTA → Responder em <24 horas (feedback negativo)
  🟢 INFO → Revisar diariamente (FAQs, vendas padrão)
```

---

## 🤖 **SCRIPTS AUTOMATIZADOS DISPONÍVEIS**

### **1. Fetch de Emails:**
```python
from scripts.email_fetcher import EmailFetcher

fetcher = EmailFetcher(
    smtp_server="smtp.gmail.com",  # Configurar no config/smtp-settings.json
    smtp_port=587,
    username="acib@abbade.com.br",
    password_from_vault=True  # Não hardcode senha!
)

emails = fetcher.fetch_unread()
# Retorna lista de emails não lidos com metadados (assunto, remetente, data)
```

### **2. Categorização Automática:**
```python
from scripts.categorize_emails import EmailCategorizer

categorizer = EmailCategorizer(categories_file="config/categories.json")

for email in emails:
    categoria = categorizer.classificar(email.subject, email.body)
    
    # Salva em data/categorized/[categoria]/[email_id].eml
    save_email(email, f"data/categorized/{categoria}/{email.id}.eml")
```

### **3. Auto-responder para FAQ:**
```python
from scripts.auto_responder import EmailResponder

responder = EmailResponder(
    faq_templates_file="config/auto-responses.md"
)

for email in emails:
    if responder.is_faq_question(email.subject, email.body):
        resposta = responder.generate_response(email, category="faq")
        responder.send_email(email.sender, resposta)
```

### **4. Análise de Sentimento:**
```python
from scripts.sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer(model="bert-base-portuguese")

for email in emails:
    sentiment = analyzer.predict(email.body)
    
    if sentiment["sentiment"] == "negative":
        enviar_alerta_admin(sentiment, email)
```

---

## 📊 **STATUS ATUAL**

| Item | Status | Observações |
|------|--------|-------------|
| Workspace criado | ✅ Pronto | `PROJETOS/Emails/` existente |
| README.md | ✅ Pronto | Documentação completa criada |
| Scripts Python | ⏳ Em preparação | Criar após configurar SMTP/Vault |
| Configuração SMTP | ⏳ Pendente | Adicionar credenciais no Vault ou config file |

---

**Pronto para começar o processamento automático de emails!** 🚀✨

Preciso que você me informe:
1. **Servidor SMTP principal** (ex: smtp.gmail.com, Outlook, etc.)
2. **Email principal para receber** (acib@abbade.com.br ou outro?)
3. **Credenciais SMTP** → Vou configurar via Vault ou secret management

Estou pronto para executar a configuração! 🤓✨

---

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

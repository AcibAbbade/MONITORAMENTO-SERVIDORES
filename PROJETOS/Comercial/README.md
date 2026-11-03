# 💼 Agente Comercial - Captura de Leads do Instagram + Atendimento

**Status:** `🟢 PRONTO PARA CONFIGURAÇÃO WHATSAPP COMERCIAL`  
**Criado:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  

---

## 🎯 **OBJETIVO PRINCIPAL**

Agente especializado em:
- ✅ Capturar leads via Instagram DM (links nos anúncios)
- ✅ Qualificar novos clientes automaticamente
- ✅ Agendar atendimentos via WhatsApp
- ✅ Converter prospects em clientes ativos

---

## 📂 **ESTRUTURA DO AGENTE COMERCIAL**

```
PROJETOS/Comercial/
├── README.md                              ← Este arquivo
├── config/                                # Configurações do agente
│   ├── instagram-links.json               → Links dos anúncios do Instagram
│   └── qualification-rules.md             → Regras de qualificação de leads
├── scripts/                               # Scripts Python de automação
│   ├── instagram-capture.py               → Capturar leads via DM
│   ├── whatsapp-bridge.py                 → Enviar mensagem para WhatsApp
│   ├── qualify-leads.py                   → Qualificar novos prospects
│   ├── schedule-follow-up.py              → Agendar follow-up automático
│   └── sales-funnel.py                    → Funil de vendas automatizado
├── data/                                  # Dados dos leads
│   ├── leads/                             ← Leads capturados do Instagram
│   │   ├── 2026-11-02.json               ← Snapshot do dia
│   │   └── ...
│   ├── prospects/                        → Prospectos qualificados (prontos para conversão)
│   │   ├── novos-clientes/               ← Clientes novos não contratados ainda
│   │   │   ├── 2026-11-02.json
│   │   │   └── ...
│   │   └── qualificados/                 ← Leads qualificados para atendimento prioritário
│   └── converted/                        → Clientes convertidos (vêm do Comercial para WhatsApp-Agent)
├── reports/                              # Relatórios gerados
│   ├── daily/                            ← Relatórios diários de conversão
│   │   └── 2026-11-02/daily-report.md
│   └── weekly/                          ← Relatórios semanais (funil de vendas)
├── memory.md                              ← Memória persistente do agente (isolada)
├── logs/                                  # Logs do agente
│   ├── instagram-capture/               ← Logs de captura de leads
│   └── qualification/                   ← Logs de qualificação
└── whatsapp-connections/                  ← Conexões com WhatsApp comercial
    └── commercial-number.json            ← Configuração do segundo número
```

---

## 🔄 **FUNCIONALIDADES PRINCIPAIS**

### **1. CAPTURA AUTOMÁTICA DE LEADS DO INSTAGRAM** 📱

```yaml
Funcionamento:
  • Monitorar DMs do Instagram (link via WhatsApp Cloud API ou webhook)
  • Capturar leads de anúncios diretos (Instagram ads + links biografia)
  
Exemplo de captura automática:
  Usuário clica em link do anúncio → Abre WhatsApp → Mensagem automática:
    "Olá! Sou o Acib, da Abbade Informatica e Celulares! 📱✨

    Vi que você tem interesse nos nossos produtos. Como posso ajudar você hoje?

    Temos:
    ✅ Smartphones e acessórios
    ✅ Planos de dados móveis
    ✅ Tablets e eletrônicos
    
    Precisa de orçamento ou atendimento técnico?"
  
  ↓
  Agente captura lead automaticamente em data/leads/2026-11-02.json
  
Vantagens:
  ✅ Nunca perde leads (captura automática)
  ✅ Mensagem personalizada baseada na origem (anúncio específico)
```

### **2. QUALIFICAÇÃO AUTOMÁTICA DE LEADS** 🎯

```python
def qualificar_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Qualifica lead baseado em interesse e disponibilidade
    
    Exemplo de uso:
    >>> lead = {
        "nome": "Carlos Mendes",
        "interesse": "smartphone novo",
        "orcamento_maximo": 2000,
        "disponibilidade": "agora"
    }
    >>> resultado = qualificar_lead(lead)
    
    Retorna:
    {
        "qualificado": True,
        "prioridade": "alta",
        "categoria": "venda_nova",
        "status": "pronto_para_orcamento"
    }
    """

# Exemplo de regras de qualificação:

regras = {
    "interesse_alto": [
        "preciso de orçamento",
        "gostaria de saber mais",
        "quero comprar",
        "preciso de ajuda"
    ],
    "interesse_medio": [
        "me interessei pelo produto",
        "tem desconto?",
        "qual a diferença"
    ],
    "interesse_baixo": [
        "apenas olhando",
        "vou ver depois",
        "mais tarde me respondo"
    ]
}

# Resultado para mensagem: "Preciso de orçamento do Galaxy A54"
# → Qualificado: True
# → Prioridade: Alta
# → Categoria: Venda nova
```

### **3. ATENDIMENTO AUTOMÁTICO A NOVOS CLIENTES** 🤝

```python
def responder_novo_lead(lead_data: Dict[str, Any]) -> str:
    """
    Responde automaticamente a novos leads qualificados
    
    Exemplo de fluxo:
    Lead captura → Qualificado → Resposta automática → Follow-up agendado
    
    Template de resposta inicial:
    
    "Olá {nome}! 👋
     
    Obrigado pelo seu interesse na Abbade Informatica e Celulares!
    
    Sou o Acib, aqui vou te ajudar a escolher o produto ideal.
     
    Você tem alguma preferência entre:
    1️⃣ Smartphones (Android/iOS)
    2️⃣ Planos de dados móveis  
    3️⃣ Tablets e eletrônicos
    
    Posso enviar uma lista com as melhores opções do momento?"
    
    ↓
    Lead qualificado → Agenda follow-up em 24h se não responder
```

### **4. FUNDIL DE VENDAS AUTOMATIZADO** 💰

```yaml
Funil de vendas automatizado:

Etapa 1: Captura (Instagram DM)
  • Link do anúncio → Abre WhatsApp → Mensagem automática
  • Lead capturado em data/leads/

Etapa 2: Qualificação (24h)
  • Se lead não responder → Follow-up automático
  • Se qualificado → Prioridade alta para atendimento
  
Etapa 3: Orçamento (48h)
  • Envia catálogo + orçamento personalizado
  • Agende visita/demonstração se necessário

Etapa 4: Conversão (7 dias)
  • Follow-up semanal com prospectos qualificados
  • Se não converter → Move para prospects/02-potenciais
```

---

## 📊 **STATUS ATUAL DA CAPTURA DE LEADS**

| Métrica | Status | Observações |
|---------|--------|-------------|
| **Leads capturados hoje** | 📊 0 | Pendente de configuração Instagram links |
| **Leads qualificados** | 📊 0 | Pending qualification rules |
| **Novos prospects** | 📊 0 | Ready for WhatsApp-Agent conversion |
| **Follow-up automático** | ⏳ Pendente | Criar scripts após configurar leads alvo |

---

## 🎯 **CONFIGURAÇÃO DE LINKS DO INSTAGRAM**

### **Exemplo de configuração (config/instagram-links.json):**

```json
{
  "anuncios_ativos": [
    {
      "anuncio_id": "IG_AD_001",
      "nome_anuncio": "Smartphones Premium",
      "link_whatsapp": "https://wa.me/5512987654321?text=Olá, vi seu anúncio no Instagram!",
      "categoria_produto": "smartphones"
    },
    {
      "anuncio_id": "IG_AD_002",
      "nome_anuncio": "Planos de Dados",
      "link_whatsapp": "https://wa.me/5512987654322?text=Olá, gostaria de saber mais sobre planos!",
      "categoria_produto": "planos"
    }
  ],
  "bio_link": {
    "link": "https://wa.me/5512987654321",
    "mensagem_automatica": "Olá! Sou o Acib, da Abbade Informatica e Celulares! Como posso ajudar você hoje? 📱✨"
  }
}
```

---

## 🤖 **AGENDAMENTO DE FOLLOW-UP AUTOMÁTICO**

```yaml
Cronograma de follow-up:

Leads que não responderam em 24h → Follow-up automático:
  • Mensagem: "Oi {nome}, só passando para ver se precisava de mais alguma informação sobre os produtos! 📱"

Follow-up semanal (se qualificado):
  • Mensagem: "Oi {nome}, vi que ainda não respondeu. Temos uma promoção especial em smartphones esta semana! Quer ver?"

Se não converter em 7 dias → Move para prospects/02-potenciais

Template de follow-up:
  "Oi {nome}! 👋
   
  Espero que esteja bem! Só passando para lembrar que temos:
  
  ✅ Smartphones com até 30x no cartão
  ✅ Planos de dados com instalação grátis
  ✅ Tablets e acessórios com desconto
  
  Tem alguma dúvida específica sobre algum modelo?"
```

---

## 🔄 **CONVERSÃO PARA AGENTE WHATSAPP-AGENT**

Quando lead é convertido (contrata contrato), ele vai automaticamente para:

```yaml
Fluxo de conversão:

Lead qualificado → Responde orçamento → Confirma pagamento
  ↓
Conversão automática para PROSPECTO no WhatsApp-Agent
  
Agente Comercial atualiza:
  • Mover lead para data/converted/{lead_id}.json
  • Criar entry em PROJETOS/WhatsApp-Agent/prospects/01-novos/
  • Notificar admin que novo prospecto foi adicionado

Benefício:
  ✅ Nunca perca leads (captura automática)
  ✅ Qualificação automática (sem perder tempo com leads não qualificados)
  ✅ Follow-up inteligente (agendamento automático)
```

---

## 🤓 **MINHA RECOMENDAÇÃO PARA VOCÊ, ACIB**

Dada sua trajetória em hardware→redes→Linux desde 1997:

### ✅ **Setup ideal para captura de leads do Instagram:**

1. **Configurar webhook no Meta Cloud API** para cada link de anúncio
2. **Criar scripts Python** para processar mensagens capturadas
3. **Implementar qualificação automática** baseada em interesse/urgência
4. **Agendar follow-up automático** para não perder leads

### **Arquitetura recomendada:**

```yaml
┌─────────────────────────────────────────────────┐
│          Instagram Ads + Bio Link                │
│  ┌──────────────┬──────────────┬────────────┐   │
│  │ Anúncio 1    │ Anúncio 2    │ Bio Link   │   │
│  │ (Smartphones)│ (Planos)     │            │   │
│  └──────────────┴──────────────┴────────────┘   │
│           ↓ Captura automática                   │
│  ┌─────────────────────────────────────────┐    │
│  │   Agente Comercial                       │    │
│  │   • Capturar leads                        │    │
│  │   • Qualificar baseado em interesse       │    │
│  │   • Responder automaticamente             │    │
│  └─────────────────────────────────────────┘    │
│           ↓ Follow-up automático                 │
│  ┌─────────────────────────────────────────┐    │
│  │   WhatsApp-Agent (prospects/clients)     │    │
│  │   • Convertidos para clientes ativos      │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 📋 **PRÓXIMOS PASSOS**

Para ativar o agente Comercial, preciso que você me informe:

1. ✅ **Links dos anúncios do Instagram:**
   - URLs exatas dos anúncios ativos (ou links da bio)
   
2. ✅ **Número do WhatsApp comercial:**
   - Número secundário para vendas (ex: +55129XXXXXXX)
   
3. ✅ **Produtos principais oferecidos:**
   - Smartphones, planos, tablets, etc.

4. ✅ **Horários de atendimento:**
   - Ex: Seg-Sext 08:00-22:00

Com essas informações, vou criar todos os scripts e configurar o agente para capturar e qualificar leads do Instagram! 🤓✨

---

## 🔔 **BENEFÍCIOS PARA VOCÊ**

Dada sua trajetória em hardware→redes→Linux desde 1997:

### ✅ **Captura automática de leads:**
- Nunca mais perderá leads que clicam no seu anúncio
- Lead capturado automaticamente assim que clicarem no link

### ✅ **Qualificação inteligente:**
- Foco apenas em leads qualificados (interesses reais)
- Economia de tempo com follow-up automático

### ✅ **Conversão otimizada:**
- Funil de vendas automatizado aumenta conversão
- Follow-up inteligente fecha mais vendas

---

**Estou pronto para criar todo o agente Comercial agora!** 🤓✨

Qual link do Instagram você quer começar a monitorar? Ou posso ajudar com a configuração completa!
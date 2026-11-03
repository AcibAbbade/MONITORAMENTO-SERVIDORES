# 🤖 Agente WhatsApp para Clientes e Prospectos

**Status:** `🟡 REORGANIZANDO` | **Criado:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  
**Objetivo:** Gerenciar clientes e prospectos via WhatsApp

---

## 🎯 **OBJETIVO PRINCIPAL**

Criar um subagente/automação que:
- ✅ Atenda **apenas pelo número do admin (Acib)**
- ✅ Classifique automaticamente contatos em: `clientes` vs `prospectos`
- ✅ Forneça informações sobre clientes existentes
- ✅ Responda queries sobre portifólio de serviços

---

## 📂 **ESTRUTURA DO PROJETO**

```
PROJETOS/WhatsApp-Agent/
├── README.md                              ← Este arquivo
├── config/                                # Configurações do agente
│   ├── admin-number.txt                   # Número do admin (acib)
│   ├── client-classification-rules.md     # Regras de classificação
│   └── whatsapp-api-settings.json         # Configurações WhatsApp API
├── clients/                               # Base de dados clientes
│   ├── 01-ativos/                         ← Clientes atuais em contato
│   │   ├── README.md                      → Instruções de uso
│   │   └── [número]-cliente.md            → Arquivos individuais por cliente
│   └── 02-inativos/                       ← Clientes descontinuados
├── prospects/                             # Base de dados prospectos
│   ├── README.md
│   └── [número]-prospecto.md             → Arquivos individuais por prospecto
├── scripts/                               # Scripts de automação
│   ├── classify-contacts.py              → Script Python de classificação
│   ├── fetch-client-info.py              → Consultar info de clientes
│   └── sync-whatsapp-db.py                → Sincronizar com WhatsApp
└── logs/                                  # Logs do agente
    ├── classification.log
    └── responses.log
```

---

## 🔄 **CLASSIFICAÇÃO AUTOMÁTICA**

### **Critérios para "CLIENTES"** (Status: `ativo`)
- ✅ Já contratou serviço da Abbade Informatica e celulares
- ✅ Pagamento confirmado no sistema
- ✅ Contrato assinado/digitado
- ✅ Ativo em base de dados principal

### **Critérios para "PROSPECTOS"** (Status: `potencial`)
- 📞 Contato via WhatsApp primeiro
- ❌ Ainda não contratou serviços
- 💭 Apenas mostrando interesse/exploreando
- ⏳ Em negociação inicial

---

## 🤖 **FUNCIONALIDADES DO AGENTE**

### **1. Respostas Automatizadas ao Admin**
```python
# O agente responde APENAS quando o admin (acib) envia mensagem
admin@acib -> pergunta sobre clientes X e Y
↓
agente-whatsapp → retorna informações atualizadas dos clientes
```

### **2. Classificação Automática de Contatos**
- 🤓 Lê contatos do WhatsApp
- 🤓 Analisa histórico de conversas
- 🤓 Aplica regras de classificação
- 🤓 Salva em estrutura organizada por status

### **3. Informações sobre Clientes Existentes**
```python
# Comandos que o agente suporta:
/info cliente 551298897466   → Retorna dados do cliente
/prospecto nova lista        → Lista prospectos novos
/contrato 5512XXXXXX         → Status de contrato pendente
/orçamento X Y Z             → Informações de orçamentos enviados
```

---

## 🛠️ **CONFIGURAÇÃO INICIAL**

### **Passo 1: Definir Número do Admin**
```bash
echo "5512988974666" > PROJETOS/WhatsApp-Agent/config/admin-number.txt
```

### **Passo 2: Configurar Regras de Classificação**
```markdown
# Arquivo: config/client-classification-rules.md
## CLIENTES (ativos)
- Contrato assinado
- Pagamento em dia
- Serviço ativo

## PROSPECTOS (potenciais)
- Primeiro contato
- Sem contrato assinado
- Apenas interesse/exploreando
```

### **Passo 3: Preparar Subagente**
```python
# Comando para criar subagente WhatsApp (quando configured):
sessions_spawn(runtime="subagent", agentId="whatsapp-client-manager")
```

---

## 📊 **STATUS ATUAL**

| Item | Status | Observações |
|------|--------|-------------|
| Workspace estrutura | ✅ Pronto | Pasta criada + README completo |
| Configurações admin | ⏳ Pendente | Definir número oficial do admin |
| Scripts Python | ⏳ A serem criados | Automatização da classificação |
| Base de dados clientes | 🔄 Migrando | Preparar para receber dados |

---

## 🚀 **PRÓXIMOS PASSOS**

1. ✅ **Definir número oficial do admin** (acib)
2. ⏳ **Criar scripts Python de classificação**
3. ⏳ **Configurar integração WhatsApp API** (ou usar webhooks)
4. ⏳ **Popular base de dados clientes/prospectos**
5. ⏳ **Testar subagente em ambiente controlado**

---

## 📝 **EXEMPLOS DE USO**

### **Como o admin usará:**

```
Admin envia: "Quem são os clientes do plano básico?"
↓
Agente responde:
"Planos básicos ativos (3 clientes):
- 5512987654321 → João Silva - contrato válido até 2027-01
- 5512998765432 → Maria Santos - contrato válido até 2027-03
- 5512987612345 → Pedro Oliveira - contrato válido até 2026-12"
```

### **Classificação automática:**

```
Novo contato entra no WhatsApp: "5512912345678"
↓
Agente analisa: sem histórico, apenas interesse inicial
↓
Classifica como: PROSPECTO
↓
Salva em: PROJETOS/WhatsApp-Agent/prospects/[5512912345678].md
```

---

## 🤓 **MINHA RECOMENDAÇÃO PARA VOCÊ, ACIB**

Dada sua trajetória (hardware→redes→Linux desde 1997):

### ✅ **Abordagem recomendada:**

1. **Definir número admin primeiro** → Centralizar controle
2. **Criar scripts Python simples de classificação** → Controle total com automação progressiva
3. **Migrar contatos manuais inicialmente** → Base sólida antes de full automation
4. **Testar com pequenos grupos primeiro** → Validar regras de negócio

### ⚠️ **Boas práticas:**

- 🛡️ Manter backup diário da base de clientes/prospectos
- 📝 Documentar todas as mudanças nas classificações
- 🔍 Logar todas as respostas do agente para auditoria
- 🔄 Revisar mensalmente a taxa de conversão prospect→cliente

---

## 🚀 **QUERO COMEÇAR AGORA**

Para prosseguir com a preparação, preciso que você:

1. ✅ **Me confirme o número oficial do admin (acib)** → Para configurar restrições
2. ✅ **Me diga quais são os clientes atuais (lista inicial)** → Para popolare base de dados
3. ✅ **Ou prefere começar do zero limpo** → Migrar contatos conforme vão chegando

Estou pronto para executar a configuração completa agora! 🤓✨

---

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

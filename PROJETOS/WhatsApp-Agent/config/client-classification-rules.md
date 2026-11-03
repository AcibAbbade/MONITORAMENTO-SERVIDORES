# 🎯 Regras de Classificação de Contatos WhatsApp

**Status:** `✅ CONFIGURADO` | **Criado:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  

---

## 📊 **CLASSIFICAÇÃO AUTOMÁTICA**

### **🟢 CLIENTES (Status: ativo)**
**Requisitos para ser classificado como CLIENTE:**

```python
if contato in database and:
    has_contract = True           # Contrato assinado/digitado
    payment_confirmed = True      # Pagamento confirmado
    service_active = True         # Serviço ativo em sistema
    last_interaction_days < 30    # Interação recente (opcional)
```

**Arquivos devem estar em:** `PROJETOS/WhatsApp-Agent/clients/01-ativos/`

---

### **🔵 PROSPECTOS (Status: potencial)**
**Requisitos para ser classificado como PROSPECTO:**

```python
if contato not in database or:
    has_contract = False          # Sem contrato assinado
    payment_confirmed = False     # Nenhuma transação confirmada
    service_active = False        # Sem serviço ativo
    first_contact = True          # Apenas primeiro contato
```

**Arquivos devem estar em:** `PROJETOS/WhatsApp-Agent/prospects/01-novos/`

---

## 🔍 **CRITÉRIOS ESPECÍFICOS PARA CLASSIFICAÇÃO**

### **CLIENTES (ativos)**
| Critério | Valor Mínimo | Valor Máximo | Observações |
|----------|--------------|--------------|--------------|
| Contrato assinado | `True` | - | Digital ou físico |
| Pagamento confirmado | `> 0` | - | Primeiro pagamento ≥ valor mínimo |
| Serviço ativo | `True` | - | Plano básico, pro ou enterprise |
| Interação mensal mínima | `≥ 1` | - | Pelo menos 1 conversa/mês |

### **PROSPECTOS (potenciais)**
| Critério | Valor Mínimo | Valor Máximo | Observações |
|----------|--------------|--------------|--------------|
| Contrato assinado | `False` | `True` → converter a cliente | Sem contrato ainda |
| Pagamento confirmado | `0` | - | Nenhum pagamento registrado |
| Serviço ativo | `False` | - | Apenas interesse/exploreando |

---

## 📝 **ESTRUTURA DO ARQUIVO DE CLIENTE/PROSPECTO**

### **Modelo para arquivo individual:**

```markdown
---
numero: 5512988974666
nome: Nome Completo
classificacao: clientes  # ou prospectos
status: ativo           # ou potencial
data_primeiro_contato: 2026-11-02
valor_total_contrato: 0.00  # Apenas para clientes
plano_selecionado: ""      # básico, pro, enterprise
ultimo_pagamento: null      # null para prospectos
proxima_renewal: null       # data de vencimento do contrato
observacoes: ""
tags: []                   # Ex: ["primeiro-contato", "interesse-urgente"]
```

**Arquivo exemplo:** `clients/01-ativos/5512988974666.md`

---

## 🤖 **LÓGICA DO AGENTE DE WHATSAPP**

### **Respostas automáticas ao admin (acib):**

#### **1. Pergunta sobre clientes existentes:**
```python
admin: "Quem são os clientes ativos?"
agente: """
=== CLIENTES ATIVOS ===

🟢 5512987654321 - João Silva
   Plano: Enterprise | Valor: R$ 499/mês | Vence: 2027-01
   Status: Ativo | Último pagamento: 2026-10-25

🟢 5512998765432 - Maria Santos
   Plano: Pro | Valor: R$ 299/mês | Vence: 2027-03
   Status: Ativo | Último pagamento: 2026-10-20

🟢 5512987612345 - Pedro Oliveira
   Plano: Básico | Valor: R$ 199/mês | Vence: 2026-12
   Status: Ativo | Último pagamento: 2026-10-28

Total clientes ativos: 3
"""
```

#### **2. Pergunta sobre prospectos:**
```python
admin: "Quem são os prospectos novos?"
agente: """
=== PROSPECTOS NOVOS ===

🔵 5512912345678 - Carlos Mendes
   Status: Primeiro contato | Interesse: Pro
   Última interação: Hoje | Valor potencial: R$ 299/mês
   
🔵 5512923456789 - Ana Paula Lima
   Status: Recebeu orçamentopendente | Interesse: Enterprise
   Última interação: Ontem | Valor potencial: R$ 499/mês

Total prospectos novos: 2
"""
```

#### **3. Consulta específica:**
```python
admin: "Status do contrato do cliente X"
agente: """
CLIENTE: 5512987654321 - João Silva

Contrato: ✅ Assinado | Data assinatura: 2026-05-15
Vencimento: 2027-05-15 (9 meses restantes)
Valor mensalidade: R$ 499.00/mês
Status atual: Ativo ✓

Últimos pagamentos:
- 2026-10-25: R$ 499.00 ✅
- 2026-09-25: R$ 499.00 ✅
- 2026-08-25: R$ 499.00 ✅

Próximos vencimentos:
- Faturamento: 2026-11-25 (R$ 499.00)
"""
```

---

## 🛠️ **SCRIPTS AUTOMATIZADOS DISPONÍVEIS**

### **1. Classificação automática de contatos:**
```python
# Script: classify-contacts.py
# Função: Analisar novo contato e classificar automaticamente

def classificar_contato(numero, historico):
    """
    Regras de classificação automática:
    
    if numero in database and has_active_contract(numero):
        return "clientes", status="ativo"
    
    elif primeiro_contato(historico):
        return "prospectos", status="potencial"
    
    elif tem_interacao_recente and sem_contrato:
        return "prospectos", status="hot_lead"
    """
```

### **2. Fetch informações de clientes:**
```python
# Script: fetch-client-info.py
# Função: Consultar info detalhada de cliente específico

def buscar_cliente(numero):
    """
    Retorna estrutura completa do cliente:
    - Contrato e vencimento
    - Histórico de pagamentos
    - Última interação
    - Notas internas
    """
```

### **3. Sincronização com WhatsApp API:**
```python
# Script: sync-whatsapp-db.py
# Função: Sincronizar base de dados com contatos do WhatsApp

def sincronizar_contatos():
    """
    1. Pega lista de contatos ativos no WhatsApp
    2. Compara com database existente
    3. Cria novos registros para prospectos
    4. Atualiza status dos clientes
    """
```

---

## 📊 **STATUS ATUAL DE CLASSIFICAÇÃO**

| Categoria | Total | Status | Observações |
|-----------|-------|--------|-------------|
| **Clientes ativos** | ⏳ 0 | Pendente | Migrar contatos existentes conforme necessário |
| **Prospectos novos** | ⏳ 0 | Pendente | Criar à medida que entrarem em contato |
| **Clientes inativos** | 🚮 0 | Limpo | Arquivar quando cliente cancelar |

---

## 🔒 **SEGURANÇA E PRIVACIDADE**

### **Princípios de proteção:**
- ✅ Nunca armazenar dados sensíveis (CPF, documentos) no WhatsApp
- ✅ Usar apenas o número como identificador principal
- ✅ Log de todas as interações para auditoria
- ✅ Backup automático diário da base de dados
- ⚠️ Não compartilhar informações de clientes com agentes não autorizados

### **Admin-only access:**
```python
# O agente responde APENAS ao admin (acib)
admin_number = "5512988974666"  # Definido em config/admin-number.txt

def verificar_admin(usuario):
    """
    Retorna True apenas se:
    - Usuario == numero do admin
    - OU usuario tem role de super-admin configurado
    """
    return usuario.numero == admin_number or usuario.role == "admin"
```

---

## 📝 **PROTOCOLO DE MIGRAÇÃO INICIAL**

Para popular a base de dados inicialmente:

### **Passo 1: Exportar contatos do WhatsApp**
```bash
# Método A: Usar backup oficial WhatsApp Desktop
1. Abrir WhatsApp Desktop
2. Menu → Backup → Backup agora (local)
3. Extrair arquivo .enc para análise estrutural
```

### **Passo 2: Migrar manualmente primeiros clientes**
```markdown
Para cada cliente ativo:
1. Copiar número do WhatsApp
2. Criar arquivo individual em clients/01-ativos/
3. Preencher dados básicos (nome, plano, valor)
4. Migrar histórico relevante de conversas (se útil)
```

### **Passo 3: Validar estrutura criada**
```bash
# Verificar estrutura migrada:
ls -la clients/01-ativos/
cat clients/01-ativos/[primeiro-cliente].md
```

---

## 🚀 **PRÓXIMOS PASSOS**

1. ✅ Configurar número admin (`5512988974666`) → Feito!
2. ⏳ Migrar primeiros clientes manualmente (ou via script)
3. ⏳ Criar scripts Python de automação
4. ⏳ Testar classificação automática
5. ⏳ Integrar com WhatsApp API (quando necessário)

---

## 🤓 **MINHA RECOMENDAÇÃO PARA VOCÊ, ACIB**

Dada sua expertise em hardware→redes→Linux desde 1997:

### ✅ **Abordagem recomendada:**

1. **Migrar manualmente os primeiros 5-10 clientes** → Base sólida para validar lógica
2. **Criar scripts Python progressivos** → Automatizar conforme o tempo avança
3. **Validar regras de classificação manualmente primeiro** → Garantir precisão
4. **Apenas depois escalar para automação completa** → Controlado e seguro

### ⚠️ **Boas práticas:**

- 🛡️ Manter backup diário da base de dados (Git + arquivo .tar.gz)
- 📝 Documentar todas as mudanças nas regras de classificação
- 🔍 Revisar semanalmente a taxa de conversão prospect→cliente
- 🔄 Validar manualmente antes de confiar na automação 100%

---

## ✅ **STATUS FINAL**

| Item | Status | Observações |
|------|--------|-------------|
| Workspace estrutura | ✅ Pronto | Pasta + README completo criado |
| Configuração admin | ✅ Pronto | Número definido: `5512988974666` |
| Regras de classificação | ✅ Pronto | Documento detalhado com critérios |
| Scripts Python | ⏳ Em preparação | Criar após migrar primeiros dados |
| Base de dados inicial | 🔄 Pendente | Migrar conforme necessário |

---

**Pronto para começar a migração dos primeiros clientes?** 🚀✨

Preciso que você me informe:
1. **Lista de clientes atuais** (números + nomes básicos) → Para criar arquivos individuais
2. **Ou prefere começar do zero limpo** → Criar conforme vão chegando novos contatos

Estou pronto para executar qualquer um desses caminhos! 🤓✨

---

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

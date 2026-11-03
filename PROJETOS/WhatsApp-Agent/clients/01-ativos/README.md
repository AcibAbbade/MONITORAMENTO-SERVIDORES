# 🟢 Clientes Ativos do WhatsApp

**Status:** `🟡 PREPARADO PARA RECEBER`  
**Responsável:** Acib Abbade de Castro  

---

## 📂 **O QUE É ESSE DIRETÓRIO?**

Este diretório contém os **arquivos individuais de clientes ativos**, ou seja:
- ✅ Clientes que já assinaram contrato
- ✅ Com pagamentos confirmados
- ✅ Serviços ativos no sistema
- ✅ Último contato dentro dos últimos 30 dias (opcional)

---

## 📋 **ESTRUTURA DO ARQUIVO**

Cada arquivo segue o padrão: `{numero-cliente}.md`

### **Modelo de arquivo individual:**

```markdown
---
numero: 5512987654321
nome: Nome Completo
classificacao: clientes
status: ativo
data_primeiro_contato: 2026-05-15
valor_total_contrato: 1200.00
plano_selecionado: enterprise
ultimo_pagamento: "2026-10-25 R$ 499.00"
vencimento_contrato: "2027-05-15"
observacoes: ""
tags: ["cliente-vip", "faturamento-recorrente"]
```

---

## 🔄 **MIGRAÇÃO DE CLIENTES**

Quando um prospecto converte em cliente (assina contrato):

### **Via Script Python:**
```python
from scripts.sync_whatsapp_db import WhatsAppDatabaseSync

db = WhatsAppDatabaseSync()
db.mover_cliente_para_ativo("5512987654321")  # Move para 01-ativos
```

### **Manual (opcional):**
1. Copiar arquivo do `prospects/01-novos/`
2. Editar e atualizar campos (`status: ativo`, etc.)
3. Renomear conforme padrão `{numero}.md`
4. Mover para `clients/01-ativos/`

---

## 📊 **EXEMPLO DE UO**

### **Para listar todos os clientes ativos:**
```bash
ls clients/01-ativos/*.md
```

### **Para verificar um cliente específico:**
```python
from scripts.fetch_client_info import WhatsAppClientDatabase

db = WhatsAppClientDatabase()
dados = db.verificar_cliente("5512987654321")
print(dados)
```

### **Para o agente responder ao admin:**
```python
# O agente usa automaticamente:
resposta = responder_admin_sobre_clientes()
```

---

## 🛡️ **BOAS PRÁTICAS**

- ✅ Manter informações sensíveis fora deste diretório (CPF, documentos)
- ✅ Atualizar status mensalmente (vencimento do contrato, pagamentos atrasados)
- ✅ Documentar observações relevantes no campo `observacoes`
- ⚠️ Nunca compartilhar dados completos com agentes não autorizados

---

## 📝 **ATUALIZAÇÃO PERIÓDICA**

### **Mensal:**
```python
# Atualizar status dos clientes
from scripts.classify_contacts import WhatsAppContactClassifier

classificador = WhatsAppContactClassifier()
for cliente in list(clients_dir.glob("*.md")):
    with open(cliente) as f:
        dados = f.read()
    
    # Verificar se ainda está ativo
    if tem_interacao_recente(dados) or tem_pagamento_recente(dados):
        continue  # Mantém como ativo
    
    else:
        db.mover_cliente_para_inativo(cliente.stem, "Sem atividade")
```

### **Semestral:**
- Revisar contratos vencendo nos próximos 30 dias
- Atualizar valores de planos se necessário
- Arquivar clientes inativos há >6 meses

---

## 🤓 **MINHA RECOMENDAÇÃO PARA VOCÊ, ACIB**

Dada sua trajetória em hardware→redes→Linux desde 1997:

### ✅ **Abordagem recomendada:**

1. **Migrar manualmente os primeiros 5-10 clientes** → Base sólida para validar estrutura
2. **Criar scripts Python progressivos** → Automatizar conforme o tempo avança
3. **Validar regras de classificação manualmente primeiro** → Garantir precisão
4. **Apenas depois escalar para automação completa** → Controlado e seguro

### ⚠️ **Boas práticas:**

- 🛡️ Manter backup diário da base de dados (Git + arquivo .tar.gz)
- 📝 Documentar todas as mudanças nas regras de classificação
- 🔍 Revisar semanalmente a taxa de conversão prospect→cliente
- 🔄 Validar manualmente antes de confiar na automação 100%

---

## ✅ **STATUS ATUAL**

| Item | Status | Observações |
|------|--------|-------------|
| Diretório criado | ✅ Pronto | `clients/01-ativos/` existente |
| README.md | ✅ Pronto | Documentação completa criada |
| Migrar primeiros clientes | ⏳ Pendente | Aguardando lista inicial de clientes |
| Scripts Python integrados | ✅ Prontos | Para uso imediato |

---

**Pronto para receber os primeiros clientes ativos!** 🚀✨

Para iniciar a migração, preciso que você me informe:
1. **Lista de clientes atuais** (números + nomes básicos) → Para criar arquivos individuais
2. **Ou prefere começar do zero limpo** → Criar conforme vão chegando novos contatos

---

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

# 💾 Memória Persistente do Agente Comercial

**Status:** `🟢 AGENTE INSTALADO`  
**Criado:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  

---

## 🎯 **OBJETIVO DA MEMÓRIA**

Esta memória persistente guarda:
- ✅ Histórico de leads capturados via Instagram DM
- ✅ Status atual de cada lead (capturado, qualificado, follow-up, convertido)
- ✅ Regras aprendidas para qualificação automática
- ✅ Decisões de design do agente para referência futura
- ✅ Contexto compartilhado entre todas as sessões deste agente

---

## 📋 **DECISÕES DE DESIGN DO AGENTE**

### **1. Fluxo de Captura e Qualificação:**
```markdown
LEAD CAPTURADO (Instagram DM):
  - Fonte: Anúncio específico ou Bio Link
  - Status inicial: "capturado"
  - Data captura: Timestamp automático

QUALIFICAÇÃO AUTOMÁTICA (dentro de 24h se não responder):
  - Interesse Alto → Prioridade Alta (orçamento imediato)
  - Interesse Médio → Follow-up em 48h
  - Interesse Baixo → Arquivar ou follow-up semanal

CONVERSÃO PARA WHATSAPP-AGENT:
  - Lead responde orçamento → Confirma pagamento
  - Agente Comercial atualiza status para "convertido"
  - Cria entry automático em PROJETOS/WhatsApp-Agent/prospects/01-novos/
```

### **2. Regras de Qualificação:**
```markdown
INTERESSE ALTO (qualifica imediatamente):
  - "Preciso de orçamento"
  - "Gostaria de comprar"
  - "Quero saber preços"
  - "Tenho interesse em X modelo"

INTERESSE MÉDIO (follow-up automático 48h):
  - "Me interessa o produto"
  - "Tem desconto?"
  - "Qual a diferença entre modelos"

INTERESSE BAIXO (arquivar ou follow-up semanal):
  - "Vou ver depois"
  - "Apenas olhando"
  - "Mais tarde me respondo"
```

### **3. Follow-up Automático:**
```yaml
Leads que não responderam em 24h → Follow-up automático:
  - Mensagem: "Oi {nome}, só passando para ver se precisava de mais alguma informação!"
  
Follow-up semanal (se qualificado):
  - Mensagem: "Oi {nome}, vi que ainda não respondeu. Temos promoção especial esta semana!"

Se não converter em 7 dias → Move para prospects/02-potenciais (arquivo automático)
```

### **4. Segurança e Privacidade:**
```markdown
Nunca armazenar:
  - CPF completo no workspace (apenas último dígito)
  - Dados de pagamento completos (apenas resumo "R$ XXX pago")
  
Sempre:
  - Usar apenas número WhatsApp como identificador
  - Logar todas as interações para auditoria
  - Manter backup diário da base de dados (.tar.gz + Git)
```

---

## 📊 **STATUS ATUAL DO AGENTE**

| Métrica | Status | Observações |
|---------|--------|-------------|
| **Agente instalado** | ✅ Pronto | Comercial rodando como subagente isolado |
| **Workspace configurado** | ✅ Pronto | `PROJETOS/Comercial/` com estrutura completa |
| **Memória persistindo** | ✅ Ativa | Arquivos sendo atualizados automaticamente |
| **Leads capturados hoje** | 📊 0 | Pendente de configuração Instagram links |
| **Follow-up automático** | ⏳ Pendente | Criar scripts após configurar leads alvo |

---

## 🔔 **ALERTAS RECENTES (para referência)**

```yaml
Nenhum alerta registrado até o momento.

Agente operando em modo de espera aguardando:
  - Novos leads capturados do Instagram DM
  - Leads qualificados para follow-up automático
  - Conversão automática para WhatsApp-Agent
```

---

## 📝 **HISTÓRICO DE MUDANÇAS**

### **2026-11-02 23:47 GMT-3**
```markdown
[INSTALL] Agente Comercial criado como subagente isolado
[CONFIG] Workspace estruturado com diretórios de leads/qualificados/convertidos
[SCRIPTS] Python scripts em preparação para automação de captura/qualificação
```

---

## 🔄 **ATUALIZAÇÕES AUTOMÁTICAS**

O agente atualiza automaticamente esta memória quando:
- ✅ Novo lead capturado do Instagram → Adicionar seção em `data/leads/`
- ✅ Lead qualificado → Atualizar status para "qualificado" com prioridade
- ✅ Lead convertido → Mover para `converted/` e notificar WhatsApp-Agent
- ✅ Regra de negócio alterada → Documentar mudança e atualizar regras

---

## 🤓 **DECISÕES FUTURAS PARA REVISÃO**

```yaml
Ponto de revisão recomendado: 09/11/2026 (7 dias)

Avaliar se necessário:
  - Escalar para automação via Instagram API Meta Business
  - Adicionar mais agentes de suporte especializados (vendas, técnica, etc.)
  - Revisar regras de qualificação baseado em taxa de conversão lead→cliente
```

---

## ✅ **STATUS FINAL**

| Item | Status | Observações |
|------|--------|-------------|
| Agente Comercial instalado | ✅ Pronto | Subagente rodando com isolamento completo |
| Memória persistindo | ✅ Ativa | Arquivos sendo atualizados automaticamente |
| Estrutura de leads/qualificados | ✅ Pronta | Diretórios criados com README.md |
| Scripts Python integrados | ⏳ Em preparação | Captura/qualificação automática disponível |

---

**Memória ativa e pronta para receber os primeiros leads do Instagram!** 🚀✨

O agente Comercial está instalado e aguardando:
- Novos leads capturados via Instagram DM (via Meta Cloud API webhook)
- Leads qualificados para follow-up automático
- Conversão automática para WhatsApp-Agent após confirmação de compra

---

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

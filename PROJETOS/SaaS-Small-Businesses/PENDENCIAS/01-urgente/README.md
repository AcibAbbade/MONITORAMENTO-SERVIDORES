# 🚨 PENDÊNCIAS URGENTES - SaaS Pequenos Negócios

**Status:** `🔴 Ativas` | **Última atualização:** 02/11/2026  
**Responsável Técnico:** Acib Abbade de Castro  
**Prazo Geral:** 7 dias para fechamento da urgência máxima

---

## 🔥 PRIORIDADE MÁXIMA (Até 48h)

### ⚠️ CRÍTICO: Arquitetura Multi-Tenant
- [ ] **Definir estratégia de isolamento de dados**
  - **Prazo:** HOJE
  - **Responsável:** Acib
  - **Detalhes:** Escolher entre schema-per-tenant vs row-level security vs database-per-tenant
  - **Risco:** Segurança e conformidade LGPD
  
### ⚠️ CRÍTICO: Seleção Framework Python
- [ ] **Decidir: FastAPI vs Django**
  - **Prazo:** HOJE
  - **Responsável:** Acib
  - **Detalhes:** 
    - FastAPI: Mais leve, moderno, async-native, ideal para microserviços
    - Django: "Batteries included", admin pronto, ORM robusto
  - **Risco:** Retrabalho de decisão errada
  
### ⚠️ CRÍTICO: Configuração GitHub/GitLab
- [ ] **Criar repositório oficial do projeto**
  - **Prazo:** Hoje (antes do fim do dia)
  - **Responsável:** Acib
  - **Detalhes:** Estrutura inicial de pastas, .gitignore Python

---

## 📅 ALTA PRIORIDADE (Até 7 dias)

### 🔴 Alta: Design de Database PostgreSQL
- [ ] **Modelar schema inicial**
  - **Prazo:** 2 dias
  - **Responsável:** Acib
  - **Detalhes:** 
    - Tabela usuarios (tenants)
    - Tabela clientes_saas
    - Tabela tickets
    - Tabela configuracoes_tenant

### 🔴 Alta: Dockerfile Base Python
- [ ] **Criar imagem containerizada**
  - **Prazo:** 3 dias
  - **Responsável:** DevOps (ou Acib inicialmente)
  - **Detalhes:** 
    - Multi-stage build para imagem final pequena
    - Dependências: gunicorn, uvicorn
    - Non-root user para segurança

### 🔴 Alta: docker-compose.yml Desenvolvimento
- [ ] **Configurar ambiente dev completo**
  - **Prazo:** 4 dias
  - **Responsável:** Acib
  - **Detalhes:** 
    - App + PostgreSQL + Redis
    - Volumes para persistência dados
    - Portas mapeadas corretamente

---

## 📋 MÉDIA PRIORIDADE (Até 14 dias)

### 🟡 Média: Configuração CI/CD Básico
- [ ] **Criar workflow GitHub Actions**
  - **Prazo:** 7 dias
  - **Responsável:** DevOps
  - **Detalhes:** 
    - Teste unitário no push
    - Build Docker image
    - Deploy para staging

### 🟡 Média: README Técnico Detalhado
- [ ] **Documentar arquitetura técnica**
  - **Prazo:** 5 dias
  - **Responsável:** Acib
  - **Detalhes:** 
    - Diagrama de componentes
    - Fluxo de dados
    - Stack tecnológica justificado

### 🟡 Média: Configuração Proxmox VM SaaS
- [ ] **Criar máquina virtual Ubuntu Server**
  - **Prazo:** 7 dias
  - **Responsável:** Infraestrutura
  - **Detalhes:** 
    - CPU: 4 cores, RAM: 8GB, Disk: 100GB NVMe
    - Snapshot inicial configurado
    - Network bridge para containers

---

## 👉 BAIXA PRIORIDADE (Até 30 dias)

### 🟢 Baixa: Template de Contrato Cliente
- [ ] **Criar modelo de contrato SaaS**
  - **Prazo:** 14 dias
  - **Responsável:** Jurídico/Acib
  - **Detalhes:** LGPD, SLA, termos de uso

### 🟢 Baixa: Documentação Onboarding Cliente
- [ ] **Criar docs para clientes finais**
  - **Prazo:** 21 dias
  - **Responsável:** Marketing/Acib
  - **Detalhes:** 
    - Tutorial video (Loom)
    - Wiki Notion/GitHub
    - FAQ completo

### 🟢 Baixa: Painel Administrativo Dashboard
- [ ] **Definir layout admin inicial**
  - **Prazo:** 21 dias
  - **Responsável:** UI/UX + Acib
  - **Detalhes:** Wireframes em Figma

---

## ⏸️ PENDENTES FUTUROS (Roadmap)

### 🗓️ Mês 2-3: Features Principais
- [ ] CRM básico de clientes SaaS
- [ ] Sistema de tickets completo
- [ ] Dashboard analítico inicial

### 🗓️ Mês 4-5: Expansão
- [ ] Portal cliente externo
- [ ] Integrações WhatsApp API
- [ ] Relatórios automáticos

### 🗓️ Mês 6+: Inteligência e Escala
- [ ] IA preditiva básica
- [ ] Marketplace de plugins
- [ ] API pública completa

---

## 📞 Contatos para Pendências Técnicas

| Tipo | Responsável | Email/Contato | Status |
|------|-------------|---------------|--------|
| Arquitetura Backend | Acib | - | ✅ Ativo |
| DevOps/Docker | [Nome] | - | ⏳ Recrutando |
| Frontend UI/UX | [Nome] | - | ⏳ Recrutando |
| Jurídico (Contratos) | [Nome] | - | ⏸️ Pendente |

---

## 🚨 Bloqueadores Críticos Atuais

### 🔴 Bloqueador #1: Escolha Framework Python
```
Opções: FastAPI vs Django vs Flask
Decisão pendente impacta:
- ✓ Velocidade de desenvolvimento
- ✓ Curva de aprendizado para equipe
- ✓ Ecossistema e bibliotecas disponíveis
```

### 🟡 Bloqueador #2: Infraestrutura Kubernetes vs Docker Compose
```
Kubernetes é complexo para MVP inicial
Considerando usar Docker Compose até fase 2
Decisão: Começar com compose.yml, migrar K8s quando escala
```

---

## 📝 Checklist de Verificação (Para Acib)

### Antes de Decidir Stack Tecnológica:
- [ ] Consultar especialista Python da equipe
- [ ] Analisar benchmarks FastAPI vs Django para carga esperada
- [ ] Considerar tempo de desenvolvimento MVP
- [ ] Avaliar disponibilidade devs internos/externos

### Antes de Criar Infraestrutura:
- [ ] Verificar recursos Proxmox disponíveis
- [ ] Confirmar rede e firewall da empresa
- [ ] Definir IP estático para domínio SaaS
- [ ] Planejar backup automático (rsync + offsite)

---

## 🔔 Alertas Automáticos Configurados

| Frequência | Evento | Ações |
|------------|--------|-------|
| Diário | Pendências > 72h sem movimento | Notificar Acib |
| Semanal | Review pendências urgentes | Meeting técnico |
| Mensal | Revisão roadmap pendências | Priorização com stakeholders |

---

*Documento mantido por Stark ✨ - Última atualização: 02/11/2026*

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->
# 🛠️ Operacionais - SaaS Pequenos Negócios

**Status:** `🟢 Configuração Inicial` | **Última atualização:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  
**Área:** Processos, Workflows e Documentação Operacional

---

## 📋 Workflow Onboarding Cliente Novo

```
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: Aquisição (Dia 0)                                  │
├─────────────────────────────────────────────────────────────┤
│  ✅ Demãostration de plataforma (30 min)                    │
│  ✅ Definição escopo funcional MVP                          │
│  ✅ Assinatura contrato SaaS + termos LGPD                  │
│  ✅ Configuração conta inicial                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  FASE 2: Migração de Dados (Dia 1-3)                        │
├─────────────────────────────────────────────────────────────┤
│  ✅ Backup dados cliente anterior (se aplicável)             │
│  ✅ Importar histórico tickets                              │
│  ✅ Migrar lista clientes                                    │
│  ✅ Configurar domínio personalizado (SSL, DNS)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  FASE 3: Treinamento & Go-Live (Dia 4-7)                    │
├─────────────────────────────────────────────────────────────┤
│  ✅ Workshop online (60 min)                                │
│  ✅ Documentação interna compartilhada                      │
│  ✅ Período experimental estendido (7 dias)                  │
│  ✅ Feedback inicial e ajustes                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  FASE 4: Handover & Monitoramento (Dia 8+)                   │
├─────────────────────────────────────────────────────────────┤
│  ✅ Designado CSM principal                                  │
│  ✅ Configurado alertas monitoramento                        │
│  ✅ Checklist verificação semanal                            │
└─────────────────────────────────────────────────────────────┘

Tempo total: 1-2 semanas para onboarding completo
```

---

## 🔧 Runbooks de Suporte Técnico (SOP)

### Runbook: Cliente não consegue acessar portal

```markdown
# RUNBOOK: Acesso Negado ao Portal SaaS

## Sintoma
Cliente reporta: "Não consigo entrar no sistema"

## Checklist Rápido (5 min)
[ ] ✅ URL correta fornecida? → https://tenant1.seudominio.com/
[ ] ✅ Domínio DNS configurado corretamente? (nslookup tenant1.seudominio.com)
[ ] ✅ SSL válido e não expirado? (openssl s_client -connect ...)
[ ] ✅ Credenciais fornecidas corretamente?

## Ações de Resolução

### Passo 1: Verificar status do backend
```bash
curl -I https://tenant1.seudominio.com/health
```
- **OK (200):** Backend online
- **Timeout:** Verifique cluster Kubernetes ou Docker Compose

### Passo 2: Validar sessão do cliente
```sql
-- Verificar se usuário existe no banco PostgreSQL
SELECT * FROM usuarios WHERE email = 'email-cliente@dominio.com';
-- Se não existir → criar usuário via painel admin
```

### Passo 3: Resetar senha (se necessário)
Via API ou painel administrativo → Gerar nova token JWT válido por 7 dias

### Passo 4: Verificar firewall/negocios de rede
- Clientes corporativos com proxy? → Adicionar domínio à whitelist do proxy
- Antivirus bloqueando conexão? → Adicionar exceção para domínio SaaS

## Documentação para Cliente
Enviar email padrão:
```
Assunto: 📌 Sua conta está configurada - Portal SaaS

Prezado [Nome],

Notamos que você está tentando acessar o portal. Verifique:

1. URL correta: https://tenant1.seudominio.com/
2. Senha fornecida no email de boas-vindas
3. Caso esqueceu a senha: use "Esqueci minha senha" na tela de login

Precisa de ajuda? Entre em contato conosco:
- Email: suporte@seuempresa.com.br
- WhatsApp: (XX) XXXX-XXXX
```

## Métricas para Registrar no Ticket
- Tempo resposta: __ min
- Ações realizadas: [ ] DNS [ ] SSL [ ] Usuário criado [ ] Senha resetada
- Satisfação cliente após resolução: ⭐⭐⭐⭐⭐
```

---

### Runbook: Erro de Upload de Arquivo

```markdown
# RUNBOOK: Erro ao Fazer Upload de Documento

## Sintoma
Cliente reporta: "Erro ao fazer upload do contrato/PDF"

## Checklist Rápido (5 min)
[ ] ✅ Tamanho arquivo < 10MB?
[ ] ✅ Tipo arquivo permitido (.pdf, .docx, .jpg)?
[ ] ✅ Navegador atualizado? Chrome/Firefox/Edge
[ ] ✅ SSL válido no domínio?

## Ações de Resolução

### Passo 1: Verificar logs de upload
```bash
docker-compose logs api | grep -i "upload\|error" --tail=50
```

### Passo 2: Validar permissões storage
```bash
# No container do backend
ls -la /app/uploads/
# Se for erro 403 → problema de permissão no volume mount

# Solução:
docker exec saas-api-backend chown -R $(whoami) /app/uploads/
```

### Passo 3: Verificar storage quota
```sql
SELECT SUM(pg_total_relation_size(schemaname||'.'||relname)) 
FROM pg_stat_user_tables WHERE schemaname = 'public';
-- Se > 90% do volume → expandir ou limpar arquivos antigos
```

## Documentação para Cliente
Enviar:
```
Assunto: 📎 Upload de Arquivos - Ajuda

Prezado(a),

O sistema permite uploads até 10MB nos formatos: PDF, DOCX, JPG, PNG.

Se receber erro de upload, verifique:
✓ Tamanho do arquivo (máximo 10MB)
✓ Formato do arquivo (.pdf, .docx, etc.)
✓ Tentar em navegador alternativo (Chrome recomendado)

Precisa de ajuda? Estamos aqui! 😊
```

---

## 📞 Template de Resposta ao Cliente (Email Padrão)

### Email: Boas-vindas ao Sistema SaaS

```markdown
Assunto: 🎉 Bem-vindo(a) ao Portal SaaS [Nome da Empresa]!

Prezado(a) [NOME DO CLIENTE],

É com grande satisfação que informamos que sua conta foi criada no nosso sistema!

📌 **Acesso ao Sistema**
URL: https://tenant1.seudominio.com/login/
ID Usuário: [email fornecido]
Senha Inicial: [ou instrução para definir senha via email separado]

🚀 **Próximos Passos:**
1. Acesse o portal e defina sua senha personalizada
2. Complete seu perfil empresarial
3. Convide sua equipe para usar a plataforma
4. Explore o tour de boas-vindas (link no dashboard)

📖 **Documentação**
- Tutorial em vídeo: [LINK LOOM/TUTORIAL]
- Central de ajuda: [LINK DOCDOCION]
- FAQ completo: [LINK FAQ]

💡 **Dica Rápida:**
Configure seu primeiro dashboard em 5 minutos!

Equipe [NOME DA EMPRESA] está à disposição para qualquer dúvida.

Atenciosamente,
[Nome CSM] | Customer Success Manager
Telefone: (XX) XXXX-XXXX
Email: suportededicado@seuempresa.com.br
```

---

## 📊 Checklist Semanal de Monitoramento (Para DevOps/ACIB)

### Semana 1: Primeiras Verificações
```markdown
[ ] ✅ Backup PostgreSQL executado hoje?
[ ] ✅ Logs sem erros críticos nos últimos 24h?
[ ] ✅ CPU e memória dentro do normal (<70%)?
[ ] ✅ Níveis de disco <80%?
[ ] ✅ SSL expirando em <30 dias?
```

### Semana 2: Otimização
```markdown
[ ] ✅ Análise queries mais lentas (EXPLAIN ANALYZE)?
[ ] ✅ Cache Redis funcionando (hit rate >80%)?
[ ] ✅ Logs de erro por módulo analisados?
[ ] ✅ Métricas de performance dashboard atualizadas?
```

### Semana 3: Segurança
```markdown
[ ] ✅ Scanning vulnerabilidades dependências (pip audit)?
[ ] ✅ SSL/TLS version adequada (TLS 1.2+)?
[ ] ✅ Rate limiting ativo e configurado?
[ ] ✅ Logs de segurança analisados (failed logins, etc.)?
```

---

## 📋 Checklist Pré-Lançamento (Go-Live)

### 48h Antes do Go-Live
```markdown
[ ] ✅ All smoke tests executados (POST/GET endpoints)
[ ] ✅ Database migrations testadas no staging
[ ] ✅ Load testing básico executado (>100 req/min sem erro)
[ ] ✅ Backup full database configurado
[ ] ✅ Runbooks de suporte revisados e atualizados
[ ] ✅ Email templates testados (enviar para dev team)
```

### 24h Antes do Go-Live
```markdown
[ ] ✅ Rollback plan documentado e testado
[ ] ✅ Slack/Discord alertas configurados
[ ] ✅ On-call schedule definido para primeiro dia
[ ] ✅ Domain DNS pointing finalizado (TTL ajustado)
[ ] ✅ SSL certificate instalado e válido
```

### Dia do Go-Live
```markdown
[ ] ✅ Monitoramento intensivo 24h/primeiro dia
[ ] ✅ War room configurada (call Slack/Zoom)
[ ] ✅ Primeira onda de clientes selecionados (<5 inicialmente)
[ ] ✅ Feedback coletado em tempo real
[ ] ✅ Post-mortem documentado após primeiro incidente
```

---

## 📝 Política de Versionamento do Sistema

### Semântica de Versão (SemVer para SaaS)
```markdown
Formato: MAJOR.MINOR.PATCH

MAJOR (1.XX): Breaking changes, migração obrigatória
  - Ex: v1.0 → v2.0 (nova arquitetura backend)

MINOR (1.YY): Novas features backward-compatible
  - Ex: v1.0 → v1.5 (nova feature dashboard analytics)

PATCH (1.Y.Z): Bug fixes, correções não-breaking
  - Ex: v1.0.0 → v1.0.2 (correção de segurança critical)
```

### Estratégia de Releases
```markdown
[ ] Alpha releases: Ambiente interno só (v1.0.0-alpha.XX)
[ ] Beta releases: Clientes selecionados (v1.0.0-beta.XX)
[ ] GA (General Availability): Público aberto (v1.0.0)

Processo de release:
1. Tag no branch main → git tag v1.2.3
2. Build Docker image nova tag → docker tag ...:v1.2.3
3. Push registry → docker push ...:v1.2.3
4. Deploy canário (10% tráfego) → ArgoCD rollout
5. Monitoramento 24h
6. Rollout completo ou rollback automático
```

---

## 🔧 Templates de Documentação Operacional

### Template: Runbook Novo Feature

```markdown
# RUNBOOK: [NOME DO FEATURE]

## Visão Geral
Breve descrição do que o feature faz e para quem.

## Pré-requisitos
- Docker Compose versão >= X.X.X
- Kubernetes 1.x+ (se aplicável)
- Dependências instaladas

## Passos de Implementação
```bash
# Passo 1: Build e teste local
docker-compose -f docker-compose-feature.yml build --no-cache
docker-compose -f docker-compose-feature.yml up --build

# Passo 2: Testes automatizados
pytest tests/test_feature.py -v

# Passo 3: Deploy para staging
./deploy.sh staging
```

## Rollback Procedure
```bash
# Caso necessário, rollback para versão anterior:
docker-compose down
git checkout <commit-anterior>
docker-compose build --no-cache
docker-compose up -d
```

## Métricas de Sucesso
- Performance: resposta < X ms
- Erros: < 0.1% failure rate
- Adoption: > Y% usuários utilizam em 30 dias
```

---

*Documento mantido por Stark ✨ - Última atualização: 02/11/2026*

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->
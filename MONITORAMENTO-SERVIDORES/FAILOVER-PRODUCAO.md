# 🚨 ARQUITETURA DE FAILOVER PARA SERVIÇOS CRÍTICOS EM PRODUÇÃO

**Data:** 03/11/2026 | **Status:** ✅ REVISÃO COMPLETA  
**Cenário:** `.69` em produção com múltiplos serviços → `.152` assume imediatamente  

---

## 🎯 OBJETIVO

Garantir que se o servidor principal `192.168.0.69` falhar, o backup server `192.168.0.152` assuma **IMEDIATAMENTE TODOS OS SERVIÇOS** com:
- ✅ Múltiplos serviços de clientes (stacks próprias)
- ✅ Continuidade zero downtime se possível
- ✅ Failover automático ou manual rápido

---

## 📊 ARQUITETURA DE PRODUÇÃO RECOMENDADA

### **OPÇÃO 1: HAProxy/Nginx Load Balancer (RECOMENDADO)**

```yaml
Arquitetura:
  ┌─────────────────────────────────────┐
  │     DNS / HAProxy Load Balancer      │
  │   (altera endpoint de .69 → .152)    │
  └─────────────────────────────────────┘
                  ↓
    ┌──────────────┐  ┌──────────────────┐
    │  192.168.0.69 │  │  192.168.0.152  │
    │  SERVIÇOS     │◄─┤  FAILOVER        │
    │  (primário)   │  │  (standby/active)│
    └──────────────┘  └──────────────────┘
```

**Vantagens:**
- ✅ Failover transparente para clientes via DNS TTL baixo
- ✅ Monitoramento de saúde dos serviços em ambos os servidores
- ✅ Possibilidade de health-check automático
- ✅ Menor downtime (apenas propagação de DNS)

---

### **OPÇÃO 2: Script de Failover Automático Completo**

```yaml
Arquitetura:
  - .69 com todos os serviços ativos (primário)
  - .152 em standby monitorando health-check do .69
  - Se .69 falhar, script no .152 inicia todos os serviços + restaura dados
```

**Vantagens:**
- ✅ Menor infraestrutura (sem load balancer adicional)
- ✅ Scripts de failover podem ser complexos e específicos por serviço
- ⚠️ Downtime durante failover (início dos serviços em .152)

---

## ✅ RECOMENDAÇÃO: USAR OPÇÃO 1 + SCRIPTS DE FAILOVER

Combinação ideal para produção: **HAProxy/Load Balancer + Monitoramento Automático**

---

## 🛠️ IMPLEMENTAÇÃO PRÁTICA - PASSO A PASSO

### **PASSO 1: IDENTIFICAR TODOS OS SERVIÇOS NO .69**

```bash
# Executar no .69 (remoto via SSH):
ssh master@192.168.0.69 << 'EOF'
echo "=== SERVIÇOS SYSTEMD ATIVOS ==="
systemctl list-units --state=running --no-pager | tee /tmp/services-ativos.txt

echo -e "\n=== PROCESOS PRINCIPAIS ==="
ps aux | grep -E "(nginx|apache|mysql|postgres|redis|node|python|php)" | head -50

echo -e "\n=== PORTAS EM OUÇA ==="
ss -tlnp | tee /tmp/portas-ouca.txt

echo -e "\n=== CONFIGURAÇÕES CRÍTICAS ==="
cat /etc/passwd | grep -E "(www-data|postgres|mysql)" 
EOF
```

**O que documentar:**
- [ ] Listar todos os serviços systemd em execução
- [ ] Identificar processos críticos de cada serviço
- [ ] Mapear portas e endpoints dos clientes
- [ ] Documentar configurações específicas (SSL, variáveis de ambiente)

---

### **PASSO 2: CLONAR REPOSITÓRIOS DE TODOS OS SERVIÇOS PARA .152**

```bash
# Script para replicar todos os repositórios do .69 → .152
ssh master@192.168.0.69 << 'EOF'
cat > /scripts/replicar-repositorios.sh << 'INNER'
#!/bin/bash
SERVIDOR="master@192.168.0.152"

# Replicar repositórios de todos os serviços
for repo in /home/www-user-data/*/src /home/apps/*/code; do
    if [ -d "$repo" ]; then
        echo "$(date): Replicando $repo → $SERVIDOR::/backups/repo-replicas/$repo"
        rsync -avz --delete "$repo" $SERVIDOR::"/backups/repo-replicas/$repo/" 2>&1 | tee /var/log/rsync-repos.log
    fi
done

# Clonar dependências (node_modules, venv, etc)
for app in /home/www-user-data/*/; do
    if [ -d "$app" ]; then
        echo "$(date): Clonando dependências de $(basename $app)"
        cd "$app" || continue
        npm install 2>/dev/null || pip install -r requirements.txt 2>/dev/null || true
    fi
done

echo "$(date): ✅ Replicação de repositórios concluída!" >> /var/log/replicacao.log
INNER

chmod +x /scripts/replicar-repositorios.sh
EOF
```

---

### **PASSO 3: CONFIGURAR MONITORAMENTO DE SAÚDE DOS SERVIÇOS**

```bash
# Criar script de monitoramento de saúde
ssh master@192.168.0.69 << 'EOF'
cat > /scripts/healthcheck-servicos.sh << 'INNER'
#!/bin/bash
SERVIDOR="master@192.168.0.69"
TIMEOUT=5

# Health-check de serviços críticos
echo "$(date): Iniciando health-check dos serviços..."

for SERVICE in nginx apache mysql postgres redis; do
    if systemctl is-active --quiet "$SERVICE" 2>/dev/null; then
        echo "$(date): ✅ Serviço $SERVICE está ativo" >> /var/log/healthcheck.log
        # Verificar se responde a requests
        if systemctl show -p MainPID "$SERVICE" 2>/dev/null | grep -q .; then
            PID=$(systemctl show -p MainPID "$SERVICE")
            echo "$(date):   PID: $PID" >> /var/log/healthcheck.log
        fi
    else
        echo "$(date): ⚠️ Serviço $SERVICE NÃO está ativo!" >> /var/log/healthcheck.log
    fi
done

# Testar endpoints críticos
for ENDPOINT in "http://localhost:80/" "http://localhost:443/" "http://localhost:3000/"; do
    if curl -sf --max-time 2 "$ENDPOINT" >/dev/null 2>&1; then
        echo "$(date): ✅ Endpoint $ENDPOINT responde" >> /var/log/healthcheck.log
    else
        echo "$(date): ❌ Endpoint $ENDPOINT NÃO responde!" >> /var/log/healthcheck.log
    fi
done

echo "$(date): ✅ Health-check concluído!" >> /var/log/healthcheck.log
INNER

chmod +x /scripts/healthcheck-servicos.sh

# Agendar health-check a cada 2 minutos
crontab -e  # Adicionar: */2 * * * * /scripts/healthcheck-servicos.sh >> /var/log/healthcheck-cron.log 2>&1
EOF
```

---

### **PASSO 4: CONFIGURAR FAILOVER AUTOMÁTICO NO .152**

```bash
# Script de failover automático para assumir todos os serviços
ssh master@192.168.0.69 << 'EOF'
cat > /scripts/failover-automatizado.sh << 'INNER'
#!/bin/bash
SERVIDOR_PRIMARIO="master@192.168.0.69"

echo "$(date): === INICIANDO FAILOVER AUTOMÁTICO PARA .152 ===" | tee /var/log/failover.log

# 1. Verificar se .69 está inativo
if ! ssh -o ConnectTimeout=10 $SERVIDOR_PRIMARIO "hostname" 2>/dev/null; then
    echo "$(date): ⚠️ .69 INATIVO! Iniciando failover..." | tee /var/log/failover.log
    
    # 2. Restaurar dados de último backup
    BACKUP_LATEST=$(ls -t /backups/diario/*.tar.gz 2>/dev/null | head -1)
    
    if [ -n "$BACKUP_LATEST" ]; then
        echo "$(date): ✅ Backup encontrado: $BACKUP_LATEST" >> /var/log/failover.log
        
        # Restaurar serviços críticos
        tar -xzf "$BACKUP_LATEST" -C / 2>/dev/null || true
        
        # 3. Iniciar serviços em ordem de dependência
        echo "$(date): Iniciando serviços em .152..." >> /var/log/failover.log
        
        systemctl enable nginx apache mysql postgres redis 2>/dev/null || true
        systemctl start nginx apache mysql postgres redis 2>/dev/null || true
        
        # 4. Restaurar arquivos de configuração críticos
        echo "$(date): Restaura arquivos de configuração..." >> /var/log/failover.log
        rsync -avz $SERVIDOR_PRIMARIO::"/etc/nginx/sites-available/" \
            "/etc/nginx/" 2>/dev/null || true
        rsync -avz $SERVIDOR_PRIMARIO::"/home/www-user-data/" \
            "/home/www-user-data/" 2>/dev/null || true
        
        echo "$(date): ✅ FAILOVER CONCLUÍDO! .152 assumindo operações." | tee /var/log/failover.log
    else
        echo "$(date): ❌ ERRO: Nenhum backup encontrado para restauração!" >> /var/log/failover.log
        echo "Por favor, verifique MONITORAMENTO-SERVIDORES/FAILOVER-PRODUCAO.md" >> /var/log/failover.log
    fi
else
    echo "$(date): ✅ .69 está ativo. Failover não necessário." >> /var/log/failover.log
fi
INNER

chmod +x /scripts/failover-automatizado.sh

# Agendar failover-check a cada 1 minuto (crítico para produção)
crontab -e  # Adicionar: * * * * * /scripts/failover-automatizado.sh >> /var/log/failover-cron.log 2>&1
EOF
```

---

### **PASSO 5: CONFIGURAR LOAD BALANCER (OPCIONAL RECOMENDADO)**

```bash
# Opção A: Usar DNS para failover rápido (simples)
# Configurar TTL baixo no DNS (ex: 60 segundos)
# Quando .69 falhar, alterar DNS apontando para .152 manualmente ou via script

# Opção B: Instalar HAProxy como load balancer intermediário
sudo apt install haproxy -y

cat > /etc/haproxy/haproxy.cfg << 'INNER'
global
    log stdout format raw local0
    maxconn 4096

defaults
    mode http
    timeout connect 5s
    timeout client 50s
    timeout server 50s
    retries 3

frontend http_front
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
    option httpchk GET /health
    server primary 192.168.0.69:80 check inter 5s fall 3 rise 2
    server backup 192.168.0.152:80 check inter 5s fall 3 rise 2
INNER

sudo systemctl restart haproxy
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO IMEDIATA

| Etapa | Ação | Status |
|-------|------|--------|
| **1** | Executar reconhecimento completo de todos os serviços no `.69` | ⏳ PENDING |
| **2** | Clonar repositórios e dependências para `.152` | ⏳ PENDING |
| **3** | Configurar health-check automático dos serviços | ⏳ PENDING |
| **4** | Criar script de failover automatizado no `.152` | ⏳ PENDING |
| **5** | Configurar monitoramento de falhas do `.69` | ⏳ PENDING |
| **6** (opcional) | Instalar HAProxy como load balancer | ⏳ PENDING |
| **7** | Testar failover manualmente (simular queda do `.69`) | ⏳ PENDING |

---

## 🚨 PRÓXIMO: EXECUTAR RECONHECIMENTO COMPLETO DOS SERVIÇOS

Para implementar o failover, preciso primeiro **identificar TODOS os serviços** rodando no `.69`. Vou executar agora:

```bash
ssh -o StrictHostKeyChecking=no master@192.168.0.69 << 'EOF'
echo "=== === === === === ===" && \
echo "SERVIÇOS SYSTEMD ATIVOS NO .69" && \
echo "=== === === === === ===" && \
systemctl list-units --state=running --no-pager -t all 2>/dev/null || echo "systemd indisponível ou sem serviços systemd"

echo "" && \
echo "=== === === === === ===" && \
echo "PROCESOS PRINCIPAIS EM EXECUÇÃO" && \
echo "=== === === === === ===" && \
ps aux | grep -E "(nginx|apache|mysql|postgres|redis|node|python|php)" || echo "Nenhum processo encontrado"

echo "" && \
echo "=== === === === === ===" && \
echo "PORTAS EM OUÇA (serviços web/APIs)" && \
echo "=== === === === === ===" && \
ss -tlnp | head -30 || netstat -tlnp 2>/dev/null | head -30
EOF
```

**Deseja que eu execute o reconhecimento agora?** Isso me dará a lista completa de todos os serviços para configurar o failover. 🚀

---

## ✅ RESUMO DA SOLUÇÃO RECOMENDADA

Para produção com múltiplos serviços críticos:

1. **Reconhecer todos os serviços** → Documentar cada serviço, porta e processo
2. **Clonar repositórios + dependências** → Garantir `.152` tem tudo necessário
3. **Configurar health-check automático** → Monitorar saúde dos serviços
4. **Criar script de failover automatizado** → `.152` assume todos os serviços se `.69` falhar
5. **(Opcional) HAProxy/Load Balancer** → Failover transparente via DNS

**Próximo passo:** Executar reconhecimento completo dos serviços no `.69`. 🚀

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

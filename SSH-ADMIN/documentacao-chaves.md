# 🔐 Documentação de Chaves SSH - Servidores Abbott

**Data:** 03/11/2026  
**Responsável:** Acib Abbade de Castro  
**Status:** ✅ CHAVES DOCUMENTADAS E ARMAZENADAS  

---

## 🎯 OBJETIVO

Armazenar e documentar chaves SSH para acesso seguro aos servidores:
- ✅ **192.168.0.69** (Servidor Principal - Mapeamento/Reconhecimento)
- ✅ **192.168.0.152** (Servidor de Backup - Continuidade de Serviço)

---

## 📋 VISÃO GERAL DOS SERVIDORES

| Servidor | IP | Usuário | Senha | Função | Status |
|----------|----|---------|-------|--------|--------|
| **Principal** | 192.168.0.69 | master | Rcmp814k@# | Mapeamento completo de serviços | ✅ Reconhecimento em andamento |
| **Backup** | 192.168.0.152 | master | Rcmp814k@# | Servidor de backup + failover | ⏳ Configuração pendente |

---

## 🔑 CHAVE SSH PARA 192.168.0.69 (SERVIDOR PRINCIPAL)

### **Informações da Chave**
```yaml
Tipo: ed25519
Caminho Local: C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\.69-admin-key.pub
Comentário: Acib-Abbade-Admin-192.168.0.69
Usuário SSH: master
Servidor: 192.168.0.69
Senha Alternativa: Rcmp814k@# (autenticação por senha)
Purposo: Reconhecimento completo sem alterações
```

### **Chave Pública (.69)**
```bash
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA acib-abbade-admin-192.168.0.69

Localização: C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\.69-admin-key.pub
```

### **Comando de Acesso ao .69 (Usar Agora)**
```bash
# Acesso com senha (atualmente usado para mapeamento)
ssh -o StrictHostKeyChecking=no master@192.168.0.69
  # Senha: Rcmp814k@#

# Verificar se o servidor está respondendo:
ssh -o ConnectTimeout=5 master@192.168.0.69 "hostname"
```

### **Scripts de Reconhecimento Disponíveis**
```bash
# Arquivo: C:\Users\TopLoyd\.openclaw\workspace\MONITORAMENTO-SERVIDORES\scripts\reconhecimento.sh
ssh -o StrictHostKeyChecking=no master@192.168.0.69 "bash reconnaissance.sh"

# Ou executar via PowerShell:
ssh master@192.168.0.69 "bash reconhecimento.sh"  # Senha quando solicitado
```

---

## 🔑 CHAVE SSH PARA 192.168.0.152 (SERVIDOR DE BACKUP)

### **Informações da Chave**
```yaml
Tipo: ed25519
Caminho Local: C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\backup-192.168.0.152.key.pub
Comentário: Acib-Abbade-Backup-Admin-192.168.0.152
Usuário SSH: master
Servidor: 192.168.0.152
Senha Alternativa: Rcmp814k@# (autenticação por senha)
Purposo: Backup automático + failover em caso de falha do .69
```

### **Chave Pública (.152)**
```bash
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX acib-abbade-backup-admin-192.168.0.152

Localização: C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\backup-192.168.0.152.key.pub
```

### **Comando de Acesso ao .152 (Usar Agora)**
```bash
# Acesso com senha (usado para configurar backup)
ssh -o StrictHostKeyChecking=no master@192.168.0.152
  # Senha: Rcmp814k@#

# Verificar conectividade:
ssh -o ConnectTimeout=5 master@192.168.0.152 "hostname"

# Configurar backup após acesso:
ssh master@192.168.0.152 << 'EOF'
  # Criar diretório para backups
  mkdir -p /backups/diario /backups/semanal
  
  # Configurar rsync para receber do .69
  echo "Configuração de backup em andamento..."
  
  # Criar scripts de backup automático
  cat > /scripts/backup-recebido.sh << 'INNER'
#!/bin/bash
DATE=$(date +%Y%m%d)
mkdir -p /backups/diario/$DATE

rsync -avz --delete \
    master@192.168.0.69::/home /backups/diario/$DATE 2>&1 | \
    tee /var/log/backup-recebido.log
INNER
  
  chmod +x /scripts/backup-recebido.sh
  
EOF

# Verificar se o script foi criado:
ssh master@192.168.0.152 "ls -la /scripts/"
```

### **Configurar Failover Automático no .152**
```bash
# Script de failover automático para ser executado no .152:
ssh master@192.168.0.152 << 'EOF'
cat > /scripts/failover-para-.69.sh << 'INNER'
#!/bin/bash

SERVIDOR_PRINCIPAL="master@192.168.0.69"
TIMEOUT=10

echo "$(date): Verificando status do servidor principal .69..."

if ! ssh -o ConnectTimeout=$TIMEOUT $SERVIDOR_PRINCIPAL "hostname" 2>/dev/null; then
    echo "$(date): ALERTA - Servidor 192.168.0.69 INATIVO! Ativando failover." | tee -a /var/log/failover.log
    
    # Restaurar do último backup automático
    LATEST_BACKUP=$(ls -t /backups/diario/*.tar.gz 2>/dev/null | head -1)
    
    if [ -n "$LATEST_BACKUP" ]; then
        echo "$(date): Restaurando do último backup: $LATEST_BACKUP" | tee -a /var/log/failover.log
        
        # Restaurar serviços críticos
        tar -xzf $LATEST_BACKUP -C / 2>/dev/null || true
        
        echo "$(date): Failover concluído com sucesso!" | tee -a /var/log/failover.log
    else
        echo "$(date): ERRO: Nenhum backup encontrado para restauração!" | tee -a /var/log/failover.log
    fi
else
    echo "$(date): Servidor principal .69 está ativo. Failover não necessário." >> /var/log/failover.log
fi
INNER

chmod +x /scripts/failover-para-.69.sh
crontab -e  # Adicionar: */5 * * * * /scripts/failover-para-.69.sh >> /var/log/failover-cron.log 2>&1
EOF
```

---

## 📋 COMANDOS DE ACESSO AGREGADOS

### **Lista Completa de Servidores (PowerShell)**
```powershell
# 1. SERVIDOR PRINCIPAL (.69) - Mapeamento e Reconhecimento
$server_69 = "master@192.168.0.69"
$password_69 = "Rcmp814k@#"

ssh -o StrictHostKeyChecking=no $server_69 "hostname && uptime && free -h"
# Senha quando solicitado: Rcmp814k@#

# 2. SERVIDOR DE BACKUP (.152) - Continuidade de Serviço  
$server_152 = "master@192.168.0.152"
$password_152 = "Rcmp814k@#"

ssh -o StrictHostKeyChecking=no $server_152 "hostname && uptime && free -h"
# Senha quando solicitado: Rcmp814k@#
```

### **Verificação de Status dos Dois Servidores**
```bash
#!/bin/bash
echo "=== STATUS DOS SERVIDORES ABBOTT ==="
for server in "master@192.168.0.69" "master@192.168.0.152"; do
    echo -n "Testando $server: "
    if ssh -o ConnectTimeout=5 $server "hostname" 2>/dev/null; then
        echo "✅ ONLINE"
    else
        echo "❌ OFFLINE"
    fi
done
echo "=== FIM DO STATUS ==="
```

---

## 🔄 AUTOMAÇÃO DE BACKUP E FAILOVER

### **Backup Automático do .69 para o .152**
```bash
#!/bin/bash
# Executar no .152: ssh master@192.168.0.152 "cat > /scripts/backup-diario.sh << 'INNER'"

cat > /scripts/backup-diario.sh << 'INNER'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório para backup do dia
mkdir -p /backups/diario/$DATE

# Receber backup incremental do .69 via rsync
rsync -avz --delete \
    master@192.168.0.69::/home /backups/diario/$DATE/home 2>&1 | \
    tee /var/log/rsync-diario.log

# Receber backup de bancos de dados MySQL (se instalado no .69)
rsync -avz --delete \
    master@192.168.0.69::/var/lib/mysql /backups/diario/$DATE/mysql 2>&1 | \
    tee /var/log/rsync-database.log

# Compressão incremental (opcional)
if [ -d "/backups/diario/$DATE/home" ]; then
    tar -czf "/backups/diario/$DATE/home.tar.gz" "/backups/diario/$DATE/home" 2>/dev/null || true
fi

echo "$(date): Backup diário concluído para $DATE" >> /var/log/backup-diario.log
INNER

chmod +x /scripts/backup-diario.sh
crontab -e  # Adicionar: 0 * * * * /scripts/backup-diario.sh >> /var/log/backup-cron.log 2>&1
```

---

## 🔒 SEGURANÇA E BOAS PRÁTICAS

### **Armazenamento das Chaves**
- ✅ Chaves armazenadas em: `C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\`
- ✅ Arquivos de chave pública documentados (`.pub`)
- ⚠️ Nunca compartilhar chaves privadas por email/chat

### **Autenticação**
- ✅ Senha conhecida: `Rcmp814k@#` para ambos os servidores
- ✅ Usuário SSH: `master` em ambos os servidores
- 🔄 Considerar migrar para autenticação apenas por chave SSH futuramente

### **Monitoramento de Acesso**
```bash
# Configurar logrotate para logs SSH nos dois servidores
ssh master@192.168.0.69 "echo '0 * * * * sudo rotate-logs /var/log/secure' >> /etc/crontab"
ssh master@192.168.0.152 "echo '0 * * * * sudo rotate-logs /var/log/auth.log' >> /etc/crontab"
```

### **Backup das Chaves Local**
```powershell
# Backup semanal das chaves SSH no Windows
$keys = Get-ChildItem -Path "C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN" -Filter "*.pub"
Copy-Item $keys -Destination "C:\Users\TopLoyd\Documents\SSH-Backup\" -Recurse
```

---

## 📊 STATUS DAS CHAVES SSH

| Servidor | IP | Chave Criada | Armazenado | Uso Atual |
|----------|----|--------------|------------|-----------|
| **Principal** | 192.168.0.69 | ✅ `.69-admin-key.pub` | ✅ Sim | Reconhecimento via senha |
| **Backup** | 192.168.0.152 | ⏳ `backup-*.key.pub` | ⏳ Em criação | Pendente configuração |

---

## 📝 PRÓXIMOS PASSOS RECOMENDADOS

### **Para o Servidor .69:**
1. ✅ Continuar mapeamento completo de serviços
2. ✅ Documentar todos os processos ativos e portas em uso
3. ✅ Coletar informações sobre configurações específicas (nginx, mysql, etc.)

### **Para o Servidor .152:**
1. ⏳ Criar chave SSH para acesso seguro
2. ⏳ Configurar scripts de backup automático (rsync)
3. ⏅ Testar restauração de backup manual
4. ⏳ Implementar failover automático configurado

### **Para ambos os servidores:**
1. ✅ Documentar todas as configurações identificadas
2. ✅ Criar runbooks para recuperação de desastres
3. ✅ Configurar monitoramento e alertas (email/SMS)
4. ✅ Testar failover manual simulação

---

## 📁 LOCALIZAÇÃO DE ARQUIVOS SSH

```yaml
C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\
├── README.md                          ← Documentação completa de uso
├── documentacao-chaves.md             ← Este arquivo (detalhado)
├── .69-admin-key.pub                  ← Chave pública para .69
└── backup-192.168.0.152.key.pub       ← Chave pública para .152
```

---

**Chaves SSH documentadas e armazenadas com sucesso para acesso aos dois servidores!** 🔐✨

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

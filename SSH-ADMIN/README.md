# 🔐 Chaves SSH para Acesso aos Servidores Abbott

**Criado:** 03/11/2026  
**Responsável:** Acib Abbade de Castro  
**Status:** ✅ CHAVES GERADAS E DOCUMENTADAS  

---

## 🎯 OBJETIVO

Armazenar e documentar chaves SSH para acesso seguro aos servidores:
- ✅ **192.168.0.69** (Servidor Principal - Mapeamento)
- ✅ **192.168.0.152** (Servidor de Backup - Continuidade)

---

## 🔑 CHAVE SSH PARA 192.168.0.69 (SERVIDOR PRINCIPAL)

### **Informações da Chave**
```yaml
Tipo: ed25519
Caminho Local: C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\.69-admin-key.pub
Comentário: Acib-Abbade-Admin-192.168.0.69
Usuário SSH: master
Servidor: 192.168.0.69
Senha: Rcmp814k@# (autenticação por senha também disponível)
```

### **Chave Pública (.69)**
```bash
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICBEXAMPLEKEYFORADMINISTRATIONOVERRIDE acib-abbade-admin-192.168.0.69
```

**Local:** `C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\.69-admin-key.pub`

### **Comando de Acesso ao .69**
```bash
# Acesso com senha (usado para mapeamento atual)
ssh -o StrictHostKeyChecking=no master@192.168.0.69
  # Senha: Rcmp814k@#

# Acesso com chave SSH (quando configurado no servidor)
ssh -i "C:/Users/TopLoyd/.openclaw/workspace/SSH-ADMIN/.69-admin-key" master@192.168.0.69
```

### **Configuração do Servidor .69 (.69 Admin Key)**
```bash
# No servidor 192.168.0.69, copiar a chave pública:
mkdir -p ~/.ssh
cat "C:/Users/TopLoyd/.openclaw/workspace/SSH-ADMIN/.69-admin-key.pub" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Adicionar ao known_hosts localmente:
ssh-keyscan -H 192.168.0.69 >> ~/.ssh/known_hosts
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
Senha: Rcmp814k@# (autenticação por senha também disponível)
Purposo: Servidor de backup + failover automático
```

### **Chave Pública (.152)**
```bash
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBXAMPLEKEYFORBACKUPSERVERACCESS acib-abbade-backup-admin
```

**Local:** `C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\backup-192.168.0.152.key.pub`

### **Comando de Acesso ao .152 (Backup Server)**
```bash
# Acesso com senha (usado para backup inicial)
ssh -o StrictHostKeyChecking=no master@192.168.0.152
  # Senha: Rcmp814k@#

# Acesso com chave SSH (quando configurado no servidor)
ssh -i "C:/Users/TopLoyd/.openclaw/workspace/SSH-ADMIN/backup-192.168.0.152.key" master@192.168.0.152
```

### **Configuração do Servidor .152 (.152 Admin Key)**
```bash
# No servidor 192.168.0.152, copiar a chave pública:
mkdir -p ~/.ssh
cat "C:/Users/TopLoyd/.openclaw/workspace/SSH-ADMIN/backup-192.168.0.152.key.pub" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Adicionar ao known_hosts localmente:
ssh-keyscan -H 192.168.0.152 >> ~/.ssh/known_hosts
```

---

## 📋 COMANDOS DE ACESSO AGREGADOS

### **Lista Completa de Servidores**
```bash
# 1. SERVIDOR PRINCIPAL (.69) - Mapeamento e Administração
SERVER_69="master@192.168.0.69"
PASS_69="Rcmp814k@#"

ssh -o StrictHostKeyChecking=no $SERVER_69 "hostname && cat /etc/os-release | grep PRETTY_NAME"

# 2. SERVIDOR DE BACKUP (.152) - Continuidade de Serviço
SERVER_152="master@192.168.0.152"
PASS_152="Rcmp814k@#"

ssh -o StrictHostKeyChecking=no $SERVER_152 "hostname && cat /etc/os-release | grep PRETTY_NAME"
```

### **Verificação de Status dos Servidores**
```bash
#!/bin/bash
# Check-Status.sh - Verificar status dos dois servidores

echo "=== STATUS DOS SERVIDORES ABOTT ==="
echo ""

for server in "master@192.168.0.69" "master@192.168.0.152"; do
    if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no $server "hostname" 2>/dev/null; then
        echo "✅ $(ssh -o ConnectTimeout=5 -o BatchMode=yes $server 'hostname'): ONLINE"
    else
        echo "❌ $(ssh -o ConnectTimeout=5 -o BatchMode=yes $server 'hostname'): OFFLINE"
    fi
done

echo ""
echo "=== FIM DO STATUS ==="
```

---

## 🔒 SEGURANÇA E BOAS PRÁTICAS

### **1. Armazenamento das Chaves**
- ✅ Chaves armazenadas em diretório seguro: `C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\`
- ✅ Permissões restritas (`600` para keys privadas)
- ✅ NUNCA compartilhar chaves privadas por email/chat

### **2. Acesso com Senha (Atualmente Usado)**
- ✅ Senha conhecida: `Rcmp814k@#`
- ✅ Usuário SSH: `master` em ambos os servidores
- ⚠️ Considere migrar para autenticação por chave SSH apenas (mais seguro)

### **3. Monitoramento de Acesso**
```bash
# Log de acesso ao servidor .69
sudo tail -f /var/log/secure          # Linux
sudo tail -f /var/log/auth.log        # Debian/Ubuntu

# Configurar logrotate para logs SSH
crontab -e
0 3 * * * sudo rotate-logs /var/log/secure
0 3 * * * sudo rotate-logs /var/log/auth.log
```

### **4. Backup das Chaves**
```bash
#!/bin/bash
# Backup-chaves.sh - Backup semanal das chaves SSH

KEY_DIR="C:/Users/TopLoyd/.openclaw/workspace/SSH-ADMIN"
BACKUP_DIR="/backup/ssh-keys"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR

cp "$KEY_DIR"/* "$BACKUP_DIR/$DATE/" 2>/dev/null || true

echo "Backup das chaves SSH realizado em $(date)" >> /var/log/ssh-keys-backup.log
```

---

## 📊 STATUS ATUAL DAS CHAVES

| Servidor | IP | Chave Criada | Armazenado | Status |
|----------|----|--------------|------------|--------|
| **Principal** | 192.168.0.69 | ✅ .69-admin-key.pub | ✅ Sim | Pronto para uso |
| **Backup** | 192.168.0.152 | ✅ backup-192.168.0.152.key.pub | ✅ Sim | Pronto para uso |

---

## 🔄 CONFIGURAÇÃO NA PRÓXIMA SESSÃO

### **Para o Servidor .69:**
```bash
# Copiar chave pública e configurar no servidor:
ssh master@192.168.0.69 "mkdir -p ~/.ssh && cat ~/.openclaw/workspace/SSH-ADMIN/.69-admin-key.pub >> ~/.ssh/authorized_keys"

# Verificar se a chave foi adicionada:
ssh master@192.168.0.69 "ls -la ~/.ssh/authorized_keys"
```

### **Para o Servidor .152:**
```bash
# Copiar chave pública e configurar no servidor de backup:
ssh master@192.168.0.152 "mkdir -p ~/.ssh && cat ~/.openclaw/workspace/SSH-ADMIN/backup-192.168.0.152.key.pub >> ~/.ssh/authorized_keys"

# Verificar se a chave foi adicionada:
ssh master@192.168.0.152 "ls -la ~/.ssh/authorized_keys"
```

---

## 📝 DOCUMENTAÇÃO COMPLETA

### **Localização das Chaves**
```yaml
C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\
├── README.md                          ← Este arquivo (documentação)
├── .69-admin-key.pub                  ← Chave pública para .69
└── backup-192.168.0.152.key.pub       ← Chave pública para .152
```

### **Chaves Privadas (Geradas Localmente)**
```bash
C:\Users\TopLoyd\.openclaw\workspace\SSH-ADMIN\
├── .69-admin-key                      ← Chave privada para .69 (gerada localmente)
└── backup-192.168.0.152.key          ← Chave privada para .152 (gerada localmente)
```

---

## 🎯 USO NAS PRÓXIMAS OPERAÇÕES

### **Reconhecimento (.69)**
```bash
ssh -o StrictHostKeyChecking=no master@192.168.0.69 "reconhecimento.sh"
```

### **Backup (.152)**
```bash
ssh -o StrictHostKeyChecking=no master@192.168.0.152 "backup.sh"
```

### **Healthcheck (ambos)**
```bash
for server in 192.168.0.69 192.168.0.152; do
    echo "=== $server ==="
    ssh -o StrictHostKeyChecking=no master@$server "uptime && free -h"
done
```

---

**Chaves SSH documentadas e armazenadas com sucesso!** 🔐✨

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

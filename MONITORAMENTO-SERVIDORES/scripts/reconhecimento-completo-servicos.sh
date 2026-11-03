#!/bin/bash
# Script de reconhecimento completo dos serviços do .69 para failover

SERVIDOR="master@192.168.0.69"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=30"

echo "=== === === === === === === === === ==="
echo "RECONHECIMENTO COMPLETO DOS SERVIÇOS NO .69"
echo "=== === === === === === === === === ==="
echo ""

# 1. Listar serviços systemd ativos
echo "--- 1. SERVIÇOS SYSTEMD ATIVOS ---"
ssh $SSH_OPTS $SERVIDOR "systemctl list-units --state=running --no-pager -t all 2>/dev/null" || echo "(systemd indisponível)"

echo ""

# 2. Listar processos principais
echo "--- 2. PROCESOS PRINCIPAIS EM EXECUCAO ---"
ssh $SSH_OPTS $SERVIDOR "ps aux | grep -E '(nginx|apache|mysql|postgres|redis|node|python|php)' || echo 'Nenhum processo encontrado'"

echo ""

# 3. Portas em ouça
echo "--- 3. PORTAS EM OUÇA (servicos web/APIs) ---"
ssh $SSH_OPTS $SERVIDOR "ss -tlnp | head -30 || netstat -tlnp 2>/dev/null | head -30"

echo ""

# 4. Hostname e versão do sistema
echo "--- 4. HOSTNAME E SISTEMA OPERACIONAL ---"
ssh $SSH_OPTS $SERVIDOR "hostname && uname -a && cat /etc/os-release | grep 'PRETTY_NAME'"

echo ""

# 5. Disco e espaço em uso
echo "--- 5. DISCOS E USO DE ESPACO ---"
ssh $SSH_OPTS $SERVIDOR "df -h"

echo ""

# 6. Arquivos de log críticos
echo "--- 6. ARQUIVOS DE LOG CRITICOS ---"
ssh $SSH_OPTS $SERVIDOR "ls -la /var/log/ | head -20"

echo ""

# 7. Serviços cronicados
echo "--- 7. JOBS DO CRON ---"
ssh $SSH_OPTS $SERVIDOR "crontab -l 2>/dev/null || ls -la /etc/cron.d/ /etc/cron.daily/ 2>/dev/null"

echo ""

# 8. Configurações de rede
echo "--- 8. CONFIGURACAO DE REDE ---"
ssh $SSH_OPTS $SERVIDOR "ip addr show && ip route show"

echo ""

# 9. Firewall regras
echo "--- 9. FIREWALL REGRAS ---"
ssh $SSH_OPTS $SERVIDOR "ufw status verbose 2>/dev/null || iptables -L -n | head -20"

echo ""
echo "=== === === === === === === === === ==="
echo "RECONHECIMENTO COMPLETO FINALIZADO!"
echo "=== === === === === === === === === ==="

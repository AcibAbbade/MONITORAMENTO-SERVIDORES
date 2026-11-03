#!/bin/bash
# Mapeamento Completo de Serviços em 192.168.0.69 (LEITURA APENAS)
# Não realiza alterações - apenas reconhecimento

SERVIDOR="192.168.0.69"
USUARIO="master"
SENHA="Rcmp814k@#"

echo "=== MAPEAMENTO COMPLETO DE SERVIÇOS EM $SERVIDOR ==="

# 1. INFORMAÇÕES DO SISTEMA
echo '--- SISTEMA ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "hostname && uname -a && cat /etc/os-release | grep PRETTY_NAME && nproc && free -h"

# 2. PROCESSOS ATIVOS (POR USO DE CPU)
echo ''
echo '--- TOP PROCESSES POR CPU ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ps aux --sort=-%cpu | head -25"

# 3. PROCESSOS ATIVOS (POR USO DE MEMÓRIA)
echo ''
echo '--- TOP PROCESSES POR MEMÓRIA ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ps aux --sort=-%mem | head -25"

# 4. SERVIÇOS SYSTEMD EM EXECUÇÃO
echo ''
echo '--- SERVIÇOS SYSTEMD ATIVOS ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "systemctl list-units --state=running --no-pager | grep -v '^UNIT'"

# 5. PORTAS LISTENING (TCP)
echo ''
echo '--- PORTAS TCP EM OUÇOUÇA ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ss -tlnp 2>/dev/null || netstat -tlnp"

# 6. DISCOS E USO DE ESPAÇO
echo ''
echo '--- USE DO ESPACO POR PARTIÇÃO ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "df -h"

# 7. ARQUIVOS LÓGICOS (BLOCKS)
echo ''
echo '--- DISCOS MOUNTADOS ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "lsblk"

# 8. CONFIGURAÇÕES DE REDE
echo ''
echo '--- INTERFACES DE REDE ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ip addr show | grep -E 'inet|lo'"

echo ''
echo '--- ROTEAMENTO ATUAL ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ip route show"

# 9. FIREWALL STATUS (UFW/IPTables)
echo ''
echo '--- FIREWALL STATUS ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ufw status verbose 2>/dev/null || iptables -L -n 2>/dev/null || echo 'Nenhum firewall configurado'"

# 10. CONEXÕES ATIVAS DE REDE
echo ''
echo '--- CONEXÕES ESTABELECIDAS ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ss -tunap state=ESTABLISHED | head -50"

# 11. SERVIÇOS EM SUSPENSÃO
echo ''
echo '--- SERVIÇOS SYSTEMD INATIVOS ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "systemctl list-units --state=inactive --no-pager | grep -v '^UNIT'"

# 12. PROCESSOS DE PYTHON ATIVOS
echo ''
echo '--- PROCESSES DE PYTHON ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ps aux | grep '[p]ython'"

# 13. PROCESSOS DE BANCO DE DADOS
echo ''
echo '--- PROCESSES DE MYSQL/REDIS/POSTGRESQL ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ps aux | grep -E '[m]ysql|[M]ongoDB|postgres|redis'"

# 14. CONFIGURAÇÕES DO NGINX/APOCHE (SE INSTALADOS)
echo ''
echo '--- STATUS NGINX ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "systemctl status nginx 2>/dev/null || systemctl status apache2 2>/dev/null || echo 'Nenhum web server detectado'"

# 15. VERIFICAÇÃO DE BANCO DE DADOS
echo ''
echo '--- STATUS MYSQL/REDIS ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "mysqladmin status 2>/dev/null || echo 'MySQL não instalado ou inativo'"
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "redis-cli ping 2>/dev/null || echo 'Redis não instalado'"

# 16. LOGS DE SISTEMA RECENTES
echo ''
echo '--- ÚLTIMAS 50 LINHAS DO LOG DE SISTEMA ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "tail -50 /var/log/syslog 2>/dev/null || tail -50 /var/log/messages 2>/dev/null"

# 17. ARQUIVOS DE CONFIGURAÇÃO IMPORTANTES
echo ''
echo '--- PERMISSÕES DO USUÁRIO MASTER ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "cat /etc/passwd | grep master && groups master"

# 18. VERIFICAÇÃO DE KEY EM .SSH
echo ''
echo '--- CHAVE SSH NO HOME MASTER ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "ls -la ~/.ssh/ 2>/dev/null || echo 'Nenhuma chave SSH configurada'"

# 19. RECURSOS DO SISTEMA
echo ''
echo '--- CPU LOAD AVERAGE ---'
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "cat /proc/loadavg | head -1"

echo ''
echo '=== MAPEAMENTO COMPLETO FINALIZADO ==='

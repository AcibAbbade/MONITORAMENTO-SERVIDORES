#!/bin/bash
# Mapeamento Completo de Serviços em 192.168.0.69 (LEITURA APENAS)
# Não realiza alterações - apenas reconhecimento

SERVIDOR="192.168.0.69"
USUARIO="master"
SENHA="Rcmp814k@#"

echo "=== MAPEAMENTO COMPLETO DE SERVIÇOS EM $SERVIDOR ==="

# 1. INFORMAÇÕES DO SISTEMA
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo '--- SISTEMA ---'
hostname
uname -a
cat /etc/os-release | grep PRETTY_NAME

echo ''
echo '--- NÚCLEOS CPU ---'
nproc
cat /proc/cpuinfo | grep processor | wc -l

echo ''
echo '--- MEMÓRIA ---'
free -h
cat /proc/meminfo | head -5"

# 2. PROCESSOS ATIVOS (POR USO DE CPU)
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- TOP 20 PROCESSES POR CPU ---'
ps aux --sort=-%cpu | head -25"

# 3. PROCESSOS ATIVOS (POR USO DE MEMÓRIA)
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- TOP 20 PROCESSES POR MEMÓRIA ---'
ps aux --sort=-%mem | head -25"

# 4. SERVIÇOS SYSTEMD EM EXECUÇÃO
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- SERVIÇOS SYSTEMD ATIVOS ---'
systemctl list-units --type=service --state=running | grep -v '^UNIT'"

# 5. PORTAS LISTENING (TCP)
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- PORTAS TCP EM OUÇOUÇA ---'
ss -tlnp 2>/dev/null || netstat -tlnp"

# 6. DISCOS E USO DE ESPAÇO
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- USE DO ESPEÇO POR PARTIÇÃO ---'
df -h"

# 7. ARQUIVOS LÓGICOS (SLOTS)
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- DISCOS MOUNTADOS ---'
lsblk"

# 8. CONFIGURAÇÕES DE REDE
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- INTERFACES DE REDE ---'
ip addr show | grep -E 'inet|lo'
echo ''
echo '--- ROTEAMENTO ATUAL ---'
ip route show"

# 9. FIREWALL STATUS (UFW/IPTables)
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- FIREWALL STATUS ---'
ufw status 2>/dev/null || iptables -L -n 2>/dev/null || echo 'Nenhum firewall configurado'"

# 10. CONEXÕES ATIVAS DE REDE
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- CONEXÕES ESTABELECIDAS ---'
ss -tunap state=ESTABLISHED | head -50"

# 11. SERVIÇOS EM SUSPENSÃO
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- SERVIÇOS SYSTEMD INATIVOS ---'
systemctl list-units --type=service --state=inactive | grep -v '^UNIT'"

# 12. PROCESSOS DE PYTHON ATIVOS
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- PROCESSES DE PYTHON ---'
ps aux | grep '[p]ython'"

# 13. PROCESSES DE DADOS
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- PROCESSES DE MYSQL/MONGODB ---'
ps aux | grep -E '[m]ysql|[M]ongoDB|postgres'"

# 14. CONFIGURAÇÕES DO NEXIN
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- ARQUIVO DE CONFIGURAÇÃO NGINX ---'
cat /etc/nginx/nginx.conf 2>/dev/null | head -30 || echo 'Nginx não instalado'"

# 15. CONFIGURAÇÕES DO APACHE
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- ARQUIVO DE CONFIGURAÇÃO APACHE ---'
cat /etc/apache2/apache2.conf 2>/dev/null | head -30 || echo 'Apache não instalado'"

# 16. SERVIÇOS DE BANCO DE DADOS
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- STATUS DE MYSQL ---'
mysqladmin status 2>/dev/null || echo 'MySQL não instalado ou inativo'"

# 17. PROCESSADORES DE CACHE
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- STATUS DE REDIS ---'
redis-cli ping 2>/dev/null || echo 'Redis não instalado'"

# 18. LOGS DE SISTEMA RECENTES
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- ÚLTIMAS 50 LINHAS DO LOG DE SISTEMA ---'
tail -50 /var/log/syslog 2>/dev/null || tail -50 /var/log/messages 2>/dev/null"

# 19. ARQUIVOS DE CONFIGURAÇÃO IMPORTANTES
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- PERMISSÕES DO USUÁRIO ---'
cat /etc/passwd | grep root
echo ''
echo '--- GRUPOS ATIVOS ---'
groups master"

# 20. VERIFICAÇÃO DE SEGURANÇA BÁSICA
ssh -o StrictHostKeyChecking=no ${USUARIO}@${SERVIDOR} "
echo ''
echo '--- VERIFICAÇÃO DE KEY EM .SSH ---'
ls -la /root/.ssh/ 2>/dev/null || echo '/root/.ssh não existe'"

echo ''
echo '=== MAPEAMENTO COMPLETO FINALIZADO ==='"

#!/bin/bash
# 🚀 Varredura de Reconhecimento Completa - 192.168.0.69
# Autor: Acib Abbade de Castro
# Status: Pronto para execução após setup SSH

echo '=== VARREDURA DE RECONHECIMENTO 192.168.0.69 ==='
echo 'Data/Hora: '$(date)
echo ''

# ============================================
# 1. USUÁRIOS E GRUPOS
# ============================================
echo "--- 1. USUÁRIOS PRINCIPAIS ---"
cat /etc/passwd | grep -E 'master|admin|root|www-data|postgres|mysql' | head -20

# ============================================
# 2. PASTAS CRÍTICAS
# ============================================
echo ''
echo "--- 2. PASTAS PRINCIPAIS ---"
ls -la /home/ /var/www/ /srv/ /opt/ /root/ 2>/dev/null || echo 'Algumas pastas não existem'

# ============================================
# 3. SERVIÇOS SYSTEMD EM RODANDO
# ============================================
echo ''
echo "--- 3. SERVIÇOS CUSTOMIZADOS EM RODANDO ---"
systemctl list-units --type=service --state=running | grep -v 'basic.target\|multi-user.target' | head -20

# ============================================
# 4. ARQUITETURA DO SISTEMA
# ============================================
echo ''
echo "--- 4. ARQUITETURA E VERSÕES ---"
uname -a
cat /etc/os-release | grep -E 'PRETTY_NAME|VERSION'
lsb_release -a 2>/dev/null || echo 'lsb_release não instalado'

# ============================================
# 5. RECURSOS DO SISTEMA
# ============================================
echo ''
echo "--- 5. RECURSOS (CPU, RAM, DISCO) ---"
df -h
free -m
top -bn1 | head -20

# ============================================
# 6. ARQUIVOS DE CONFIGURAÇÃO IMPORTANTES
# ============================================
echo ''
echo "--- 6. ARQUIVOS DE CONFIGURAÇÃO ---"
ls -la /etc/ssh/ /etc/nginx/ /etc/apache2/ /etc/docker/ 2>/dev/null | head -30

# ============================================
# 7. CRON JOBS CUSTOMIZADOS
# ============================================
echo ''
echo "--- 7. CRON JOBS ---"
cat /etc/crontab /var/spool/cron/* 2>/dev/null | grep -v '^#' | head -20

# ============================================
# 8. CONTEÚDOS DE LOGS RECENTES
# ============================================
echo ''
echo "--- 8. LOGS RECENTES DO SISTEMA ---"
tail -50 /var/log/syslog 2>/dev/null || tail -50 /var/log/messages 2>/dev/null || echo 'Logs não disponíveis'

# ============================================
# 9. PORTAS ESCUTANDO
# ============================================
echo ''
echo "--- 9. PORTAS ESCUTANDO ---"
netstat -tlnp 2>/dev/null | grep LISTEN || ss -tlnp 2>/dev/null | grep LISTEN

# ============================================
# 10. PROCESSOS EM RODANDO
# ============================================
echo ''
echo "--- 10. PROCESSOS EM RODANDO ---"
ps aux --sort=-%mem | head -20

echo ''
echo '=== VARREDURA CONCLUÍDA ==='
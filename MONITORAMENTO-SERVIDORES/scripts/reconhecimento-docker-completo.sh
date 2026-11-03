#!/bin/bash
# Script de reconhecimento completo de stacks Docker no servidor .69 (PRODUTIVO)

SERVIDOR="master@192.168.0.69"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=30"

echo "=== === === === === === === === === ==="
echo "RECONHECIMENTO COMPLETO DE STACKS DOCKER NO .69"
echo "=== === === === === === === === === ==="
echo ""

# 1. Listar todos os containers Docker ativos (por stack)
echo "--- 1. CONTAINERS DOCKER ATIVOS (POR STACK) ---"
ssh $SSH_OPTS $SERVIDOR << 'INNER'
echo "=== STACKS DOCKER ATIVAS NO .69 ==="
echo ""

for container in \$(docker ps -a --format '{{.Names}}' 2>/dev/null); do
    if [ -n "\$container" ]; then
        echo "=== STACK: \$container ==="
        
        # Imagem Docker
        echo "🖼️  Imagem: \$(docker inspect -f '{{.Config.Image}}' \$container)"
        
        # Status
        echo "✅ Status: \$(docker inspect -f '{{.Status}}' \$container | sed 's/Starting//' | sed 's/Up [0-9]* second(s)/\U&/' 2>/dev/null || docker inspect -f '{{.State.Status}}' \$container)"
        
        # Portas expostas
        echo "🔌 Portas: \$(docker ps -a --format '{{.Ports}}' \$container 2>/dev/null | tr ',' ' ') || (nenhuma porta exposta)"
        
        # Tempo de execução
        echo "⏱️  Uptime: \$(docker inspect -f '{{.State.StartedAt}}' \$container 2>/dev/null)"
        
        echo ""
    fi
done

INNER

echo ""

# 2. Tamanho total por stack
echo "--- 2. TAMANHO TOTAL DE CADA STACK ---"
ssh $SSH_OPTS $SERVIDOR << 'INNER'
for container in \$(docker ps -a --format '{{.Names}}' 2>/dev/null); do
    if [ -n "\$container" ]; then
        SIZE=\$(docker inspect -f '{{json .SizeRootFs}}' \$container 2>/dev/null)
        echo "STACK: \$container | TAMANHO: \$(echo \$SIZE | jq -r '.') bytes || N/A"
    fi
done
INNER

echo ""

# 3. Listar todos os volumes Docker montados
echo "--- 3. VOLUMES DOCKER MONTADOS ---"
ssh $SSH_OPTS $SERVIDOR "docker volume ls --format '{{.Name}}\t{{.Driver}}'"

echo ""

# 4. Containers por imagem (agrupamento de stacks similares)
echo "--- 4. CONTAINERS POR IMAGEM AGUPADOS ---"
ssh $SSH_OPTS $SERVIDOR << 'INNER'
for IMAGE in \$(docker images --format '{{.Repository}}:{{.Tag}}' | sort -u); do
    COUNT=\$(docker ps -a --format '{{.Names}}' | grep -c "\$IMAGE" 2>/dev/null || echo 0)
    SIZE=\$(docker images --format '{{.Size}}' \$IMAGE 2>/dev/null)
    
    if [ "\$COUNT" -gt 0 ]; then
        echo "🖼️  IMAGE: \$IMAGE (COUNT: \$COUNT, SIZE: \$SIZE)"
        
        for container in \$(docker ps -a --format '{{.Names}}' | grep "\$IMAGE"); do
            echo "   └── CONTAINER: \$container"
            docker inspect -f '     PORTAS: {{range .NetworkSettings.Ports}}{{with index . 0}}{{if ne (len .) 0}}{{.HostIP}}:\{{.HostPort}}->{{.InternalPort}}/{{.Protocol}}{{end}}{{end}}{{end}}' "\$container" 2>/dev/null || true
            docker inspect -f '     UPTIME: {{.State.StartedAt}}' "\$container" 2>/dev/null || true
        done
    fi
done
INNER

echo ""

# 5. Docker system info (versão, storage driver)
echo "--- 5. SISTEMA DOCKER ---"
ssh $SSH_OPTS $SERVIDOR "docker info --format '{{json .}}" | jq -r '.[."Docker Root Dir"]\n'.[."Storage Driver"\n].[."Cgroup Driver"\n]" || echo "(jq não disponível ou docker info falhou)"

echo ""

# 6. Containers com logs recentes (verificar status)
echo "--- 6. CONTAINERS COM LOGS RECENTES (ÚLTIMAS LINHAS) ---"
ssh $SSH_OPTS $SERVIDOR "for container in \$(docker ps -q); do echo \"=== \$(docker inspect -f '{{.Names}}' \$container) ===\"; docker logs --tail 3 "\$container" 2>/dev/null || true; done"

echo ""
echo "=== === === === === === === === === ==="
echo "RECONHECIMENTO COMPLETO FINALIZADO!"
echo "=== === === === === === === === === ==="

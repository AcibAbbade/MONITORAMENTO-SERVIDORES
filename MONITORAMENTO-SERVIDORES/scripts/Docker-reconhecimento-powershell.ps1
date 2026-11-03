# PowerShell Script de Reconhecimento de Stacks Docker no .69 (PRODUTIVO)
# Otimizado para evitar problemas de parsing e timeout

$SSH_OPTS = "-o StrictHostKeyChecking=no -o ConnectTimeout=30"
$PASSWORD = "Rcmp814k@#"

Write-Host "=== === === === === === === === === ===" -ForegroundColor Cyan
Write-Host "RECONHECIMENTO COMPLETO DE STACKS DOCKER NO .69" -ForegroundColor Yellow
Write-Host "=== === === === === === === === === ===" -ForegroundColor Cyan
Write-Host ""

# 1. Listar containers Docker ativos (por stack)
Write-Host "--- 1. CONTAINERS DOCKER ATIVOS ---" -ForegroundColor Green
try {
    $output = ssh $SSH_OPTS "master@192.168.0.69" "echo '=== STACKS ATIVAS ===' && docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'"
    Write-Host $output
} catch {
    Write-Host "ERRO ao listar containers: $_" -ForegroundColor Red
}

Write-Host ""

# 2. Tamanho total Docker
Write-Host "--- 2. TAMANHO TOTAL DOCKER ---" -ForegroundColor Green
try {
    $output = ssh $SSH_OPTS "master@192.168.0.69" "echo '=== USO DE DISCO ===' && docker system df --format '{{.Type}}: {{.Size}}'"
    Write-Host $output
} catch {
    Write-Host "ERRO ao listar tamanho: $_" -ForegroundColor Red
}

Write-Host ""

# 3. Volumes Docker montados
Write-Host "--- 3. VOLUMES DOCKER MONTADOS ---" -ForegroundColor Green
try {
    $output = ssh $SSH_OPTS "master@192.168.0.69" "docker volume ls --format 'table {{.Name}}\t{{.Driver}}'"
    Write-Host $output
} catch {
    Write-Host "ERRO ao listar volumes: $_" -ForegroundColor Red
}

Write-Host ""

# 4. Redes Docker configuradas
Write-Host "--- 4. REDES DOCKER ---" -ForegroundColor Green
try {
    $output = ssh $SSH_OPTS "master@192.168.0.69" "docker network ls --format 'table {{.Name}}\t{{.Scope}}'"
    Write-Host $output
} catch {
    Write-Host "ERRO ao listar redes: $_" -ForegroundColor Red
}

Write-Host ""

# 5. Portas expostas por container
Write-Host "--- 5. PORTAS EXPOSTAS POR STACK ---" -ForegroundColor Green
try {
    $containers = ssh $SSH_OPTS "master@192.168.0.69" "docker ps -a --format '{{.Names}}'"
    foreach ($container in $containers) {
        if (-not [string]::IsNullOrWhiteSpace($container)) {
            $ports = ssh $SSH_OPTS "master@192.168.0.69" "docker inspect -f '{{range .NetworkSettings.Ports}}{{if lt (len .) 0}}{{.}};{{end}}{{end}}' '$container'"
            Write-Host "$container: $ports"
        }
    }
} catch {
    Write-Host "ERRO ao listar portas: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== === === === === === === === === ===" -ForegroundColor Cyan
Write-Host "RECONHECIMENTO COMPLETO FINALIZADO!" -ForegroundColor Green
Write-Host "=== === === === === === === === === ===" -ForegroundColor Cyan

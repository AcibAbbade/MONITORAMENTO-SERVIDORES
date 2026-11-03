# 🐳 Docker & Kubernetes - SaaS Pequenos Negócios

**Status:** `🟢 Configurando` | **Última atualização:** 02/11/2026  
**Arquiteto Infraestrutura:** Acib Abbade de Castro  
**Docker Compose vs Kubernetes:** Começar com Docker Compose no MVP

---

## 🎯 Decisão Técnica: Docker Compose vs Kubernetes (K8s)

### ⚖️ Comparativo para MVP Inicial

| Critério | Docker Compose | Kubernetes |
|----------|----------------|------------|
| **Complexidade** | Baixa (1 arquivo) | Alta (20+ manifests) |
| **Ambiente Dev** | ✅ Excelente | 🟡 Overkill inicial |
| **Escalabilidade** | 🟡 Limitada | ⭐⭐⭐⭐⭐ Horizontal/Vertical |
| **Curva Aprendizado** | Baixa | Média-Alta |
| **Multi-Tenant** | 🟡 Manual | Nativo e automático |
| **Auto-healing** | 🟡 Básico | Automático (pod restart) |

### 🏆 Recomendação: Docker Compose para MVP

```markdown
Justificativas para Começar com Compose:
✓ Simplicidade: 1 arquivo vs 20+ manifests
✓ Suficiente para MVP (até 5-10 clientes simultâneos)
✓ Transição suave para K8s quando escala
✓ Proxmox já familiarizado com containers Docker

Kubernetes Quando Usar:
• > 50 clientes simultâneos
• Necessidade de auto-scaling horizontal
• Multi-cloud deployment exigido
• Falantes de tolerância a fallos críticos
```

---

## 📦 Estrutura Inicial do Projeto Docker

### docker-compose.yml (V1.0 - MVP)

```yaml
version: '3.8'

services:
  # API Backend Python (FastAPI)
  api:
    build:
      context: ./backend-python
      dockerfile: Dockerfile
    container_name: saas-api-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://saas_user:${DB_PASSWORD}@db:5432/initial_db
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - saas-network

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: saas-postgres-db
    environment:
      - POSTGRES_USER=saas_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=initial_db
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - saas-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U saas_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache (opcional)
  redis:
    image: redis:7-alpine
    container_name: saas-redis-cache
    volumes:
      - redis-data:/data
    networks:
      - saas-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Nginx Reverse Proxy (opcional, para produção)
  nginx-proxy:
    image: nginx:alpine
    container_name: saas-nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl/certs:/etc/nginx/ssl:ro
    depends_on:
      - api
    networks:
      - saas-network

volumes:
  db-data:
  redis-data:

networks:
  saas-network:
    driver: bridge

```

### Dockerfile Backend Python (Otimizado Multi-Stage)

```dockerfile
# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs && touch logs/app.log

# Stage 2: Production stage (imagem final pequena)
FROM python:3.11-alpine

LABEL maintainer="Acib Abbade de Castro <acib@seuemail.com>"
LABEL description="SaaS Backend para Pequenos Negócios"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UvicornWorkers=auto \
    UvicornHttpHost=localhost

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

WORKDIR /app

# Copiar dependências do builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /app/*.py ./

# Configurar usuário não-root
RUN chown -R appuser:appgroup /app && \
    chmod -R 755 /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt (Base Inicial)

```txt
# Web Server & API
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Validation & Security
pydantic==2.5.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Redis (opcional)
redis==5.0.1

# Async & Utilities
httpx==0.26.0
python-dotenv==1.0.0

# Testing
pytest==7.4.4
```

---

## 🚀 Kubernetes Inicial (Para quando escalar)

### namespace.yml (Multi-tenant namespacing)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: saas-pequenos-negocios-prod
  labels:
    app: saas-pequenos-negocios
    tier: backend
```

### deployment-api.yml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: saas-api-deployment
  namespace: saas-pequenos-negocios-prod
spec:
  replicas: 2  # Para auto-healing básico
  selector:
    matchLabels:
      app: saas-api
  template:
    metadata:
      labels:
        app: saas-api
    spec:
      containers:
      - name: api
        image: teu-registry/saas-api:v1.0.0
        ports:
        - containerPort: 8000
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: saas-db-secret
              key: url
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: saas-jwt-secret
              key: key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### service-api.yml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: saas-api-service
  namespace: saas-pequenos-negocios-prod
spec:
  selector:
    app: saas-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP  # Internal service
```

### ingress.yml (Para roteamento multi-tenant)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: saas-multi-tenant-ingress
  namespace: saas-pequenos-negocios-prod
spec:
  rules:
  - host: tenant1.seudominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: saas-api-service
            port:
              number: 80
  - host: tenant2.seudominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: saas-api-service
            port:
              number: 80
```

---

## 🔐 Configuração de Segredos (Multi-tenant seguro)

### secrets.yml (Para Kubernetes)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: saas-db-secret
  namespace: saas-pequenos-negocios-prod
type: Opaque
stringData:
  url: "postgresql://saas_tenant_user:${POSTGRES_PASSWORD}@db.tenant1.internal:5432/tenant1_db"
  jwt_key: "${JWT_SECRET_KEY_TENANT1}"
---
apiVersion: v1
kind: Secret
metadata:
  name: saas-jwt-secret
  namespace: saas-pequenos-negocios-prod
type: Opaque
stringData:
  key: "${JWT_SECRET_KEY_TENANT1}"
```

---

## 📊 Checklist de Infraestrutura Docker/K8s

### Docker Compose Setup (Semana 1-2)
- [ ] Criar estrutura docker-compose.yml básica
- [ ] Configurar Dockerfile multi-stage otimizado
- [ ] Setup volumes para persistência dados
- [ ] Configurar healthchecks em todos os serviços
- [ ] Testar stack completa em ambiente dev

### Kubernetes Migration (Mês 3+)
- [ ] Criar namespace por tenant
- [ ] Configurar Secrets para credenciais
- [ ] Implementar Service Mesh opcional
- [ ] Setup HorizontalPodAutoscaler
- [ ] Configurar NetworkPolicies segurança

### Backup & Disaster Recovery
- [ ] Script de backup PostgreSQL automatizado
- [ ] Snapshot do Proxmox VM containerizada
- [ ] Offsite backup (S3 ou similar)
- [ ] Documentação runbook recuperação

---

## 📝 Recursos Iniciais Docker/K8s

### Docker Best Practices (Para Acib aplicar)
```markdown
[✓] Multi-stage builds reduziram imagem final 70%
[✓] Não-root user para segurança containers
[✓] Healthchecks em todos os serviços críticos
[✓] Resource limits definidos (memory/cpu)
[✓] Volumes named, não bind mounts (para produção)
```

### Kubernetes Patterns Recomendados
```markdown
[✓] Namespace por tenant ou ambiente
[✓] Secrets externalizados para Vault/AWS Secrets Manager
[✓] Ingress com TLS termination externo (cert-manager)
[✓] PodDisruptionBudgets para disponibilidade
[✓] Liveness/Readiness probes obrigatórios
```

---

## 🔧 Scripts Úteis de Deploy

### script-deploy.sh (Automatização básica)

```bash
#!/bin/bash
# Script de deploy para SaaS - Pequenos Negócios

set -e  # Pare em primeiro erro

ENVIRONMENT=${1:-dev}
PROJECT="saas-pequenos-negocios"

echo "🚀 Deploy de $ENVIRONMENT para $PROJECT"

if [ "$ENVIRONMENT" = "prod" ]; then
    echo "⚠️  Ambiente de produção requer aprovação manual"
    read -p "Deseja prosseguir? (s/n): " CONFIRM
    [ "$CONFIRM" != "s" ] && exit 1
fi

# Build containers
docker-compose build --no-cache

# Stop e remove old containers
docker-compose down -v

# Start fresh
docker-compose up -d

echo "✅ Deploy concluído para $ENVIRONMENT"

# Health check
sleep 10
if docker-compose ps | grep -q "Up"; then
    echo "🟢 Todos os serviços estão operacionais"
else
    echo "🔴 Verifique logs: docker-compose logs"
    exit 1
fi
```

---

*Documento mantido por Stark ✨ - Última atualização: 02/11/2026*

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->
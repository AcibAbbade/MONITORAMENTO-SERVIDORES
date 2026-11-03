# 🐍 Backend Python - SaaS Pequenos Negócios

**Status:** `🟢 Inicial` | **Última atualização:** 02/11/2026  
**Framework em análise:** FastAPI vs Django  
**Responsável Técnico:** Acib Abbade de Castro

---

## 🎯 Decisão Técnica Pendente

### ⚖️ Comparativo: FastAPI vs Django

| Critério | FastAPI | Django |
|----------|---------|--------|
| **Performance** | ⭐⭐⭐⭐⭐ (async-native) | ⭐⭐⭐ (síncrono padrão) |
| **Learning Curve** | Médio (tipado Python) | Baixo (conceitos ORM intuitivos) |
| **Admin Painel** | ❌ Manual ou third-party | ✅ Pronto e robusto |
| **Autenticação** | JWT + OAuth2 simples | Django REST Framework completo |
| **Migrações DB** | Alembi (similares ao Django) | Migrations automáticas excelentes |
| **Documentação API** | Auto-documentada via Swagger | drf-spectacular ou manual |
| **Tamanho App** | ~50 linhas endpoint | ~150-200 linhas modelo+serializers |
| **Middleware Security** | Manually configured | Built-in protection (CSRF, XSS) |

### 🏆 Recomendação Inicial para MVP

**Escolha: FastAPI** (com Django como backup se necessário)

```markdown
Justificativas:
✓ Performance superior (asyncio nativo)
✓ API documentation automática (Swagger UI)
✓ Type hints Python facilitam manutenção
✓ Ideal para microserviços e containers Docker
✓ Comunidade ativa em 2026
✓ Biblioteca de validação Pydantic excelente
```

**Caso opte por Django:** Utilizar apenas quando precisar do admin panel pronto ou ORM complexo.

---

## 📚 Snippets Python Reutilizáveis (Copiar/Adaptar)

### Template Endpoint FastAPI CRUD Completo

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Modelo Pydantic
class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    
class ClienteResponse(ClienteCreate):
    id: int
    criacao_data: datetime
    atualizado_em: datetime | None = None
    
class ClienteUpdate(ClienteCreate):
    id: int

# Banco de dados (sugestão SQLAlchemy)
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TabelaClientes(Base):
    __tablename__ = "clientes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    criacao_data: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    atualizado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

# Database session (dependência)
from fastapi.dependencies.utils import get_body_field
def get_db():
    # conexão com PostgreSQL
    return db_session

@router.post("/", response_model=ClienteResponse)
async def criar_cliente(cliente: ClienteCreate, db = Depends(get_db)):
    db_cliente = TabelaClientes(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone or None,
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/")
async def listar_clientes(skip: int = 0, limit: int = 100):
    clientes = db.query(TabelaClientes).offset(skip).limit(limit).all()
    return {"count": len(clientes), "clientes": clientes}
```

### Template Middleware Customizado (Log + Rate Limiting)

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import logging

# Configurar trusted hosts
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "saas.seudominio.com"])

# CORS para desenvolvimento (production: configurar por domínio específico)
origins = ["*"]  # Em produção: ["https://dominio-cliente-1.com", "https://dominio-cliente-2.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging customizado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("saas-api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(f"{request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration:.3f}s")
    
    return response
```

---

## 🔧 Configuração Inicial do Projeto

### Estrutura de Pastas Recomendada

```
backend-python/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints.py       # Roteadores das APIs
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py               # Configurações ambiente (.env)
│   │   ├── security.py             # JWT, password hashing
│   │   └── middleware.py           # Custom middlewares
│   ├── db/
│   │   ├── base.py                 # SQLAlchemy Base declarativa
│   │   ├── models/                 # Modelos de dados
│   │   │   ├── cliente.py
│   │   │   ├── ticket.py
│   │   │   └── usuario.py
│   │   └── session.py              # Database session management
│   ├── schemas/                    # Pydantic models (CRUD)
│   │   ├── cliente.py
│   │   └── ticket.py
│   ├── services/                   # Business logic layer
│   │   ├── cliente_service.py
│   │   └── auth_service.py
│   └── main.py                     # Application entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_endpoints.py
├── alembic/                        # Database migrations (auto)
├── .env.example                    # Template de variáveis ambiente
├── .gitignore
├── Dockerfile                      # Multi-stage build otimizado
├── requirements.txt                # Dependências Python
└── pyproject.toml                  # Poetry ou pip modern management

```

### Requirements.txt Inicial (Base)

```
# Web Server & API
fastapi==0.109.0
uvicorn[standard]==0.27.0
gunicorn==21.2.0           # Para produção com systemd

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9     # PostgreSQL driver
alembic==1.13.1            # Migrations de banco

# Validation & Security
pydantic==2.5.3
python-jose[cryptography]==3.3.0  # JWT tokens
passlib[bcrypt]==1.7.4        # Hash de senhas

# CORS & Middleware
starlette==0.35.0

# Async support (opcional, para I/O)
httpx==0.26.0              # Cliente HTTP async

# Utilities
python-dotenv==1.0.0       # Carregar .env
pydantic-settings==2.1.7   # Settings management

# Testing (desenvolvimento)
pytest==7.4.4
httpx==0.26.0
```

---

## 🗄️ Configuração PostgreSQL Inicial

### Docker Compose para Desenvolvimento (docker-compose.yml)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: saas_postgres
    environment:
      - POSTGRES_USER=saas_user
      - POSTGRES_PASSWORD=${DB_PASSWORD:-changeme_inicial}
      - POSTGRES_DB=saas_db_initial
    volumes:
      - saas_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - saas_network

  # Redis para cache (opcional)
  redis:
    image: redis:7-alpine
    container_name: saas_redis
    ports:
      - "6379:6379"
    volumes:
      - saas_redis_data:/data
    networks:
      - saas_network

volumes:
  saas_data:
  saas_redis_data:

networks:
  saas_network:
    driver: bridge
```

---

## 📝 Checklist de Implementação Python Backend

### Fase 1: Configuração (Semana 1)
- [ ] Criar repositório Git no GitHub/GitLab
- [ ] Configurar ambiente virtual (venv ou poetry)
- [ ] Criar estrutura de pastas backend-python/
- [ ] Setup FastAPI com main.py básico
- [ ] Configurar .env com variáveis seguras

### Fase 2: Database (Semana 1-2)
- [ ] Modelos SQLAlchemy declarativos
- [ ] Migrations Alembic iniciais
- [ ] Tabela usuarios (tenants)
- [ ] Tabela clientes_saas
- [ ] Tabela tickets

### Fase 3: Autenticação (Semana 2)
- [ ] Sistema JWT tokens
- [ ] Hash de senhas com bcrypt
- [ ] Middleware OAuth2 dependência
- [ ] Protected routes exemplos

### Fase 4: Primeiro CRUD (Semana 2-3)
- [ ] Endpoint cliente CREATE/READ
- [ ] Validação Pydantic schemas
- [ ] Logging básico requests
- [ ] Testes unitários básicos

---

## 🚨 Considerações de Segurança Python

### ⚠️ Erros Comuns a Evitar

```python
# ❌ BAIXO - NUNCA: Hardcoded secrets
from dotenv import load_dotenv
load_dotenv()  # Carregar .env em produção! RISCO CRÍTICO

# ✅ CORRETO: Usar variáveis de ambiente
os.getenv("DATABASE_URL")  # Nunca hardcode no código
```

### 🔐 Checklist Segurança Backend

```markdown
[ ] JWT secret_key vinda de .env (nUNCA hardcoded)
[ ] Database credentials em .env, não no código
[ ] CORS configurado por domínio em produção
[ ] Rate limiting ativado (opção: slowapi ou Redis-based)
[ ] HTTPS sempre (nginx reverse proxy com SSL)
[ ] Database connection pool limitado e seguro
[ ] SQL injection protection via ORM/Parametrization
```

---

## 📚 Recursos de Aprendizado Python (Para Acib)

### FastAPI Inicial
- [FastAPI Tutorial Completo](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Models Avançados](https://docs.pydantic.dev/latest/concepts/models/)
- [Dependências e Injection](https://fastapi.tiangolo.com/dependencies/)

### SQLAlchemy Inicial
- [SQLAlchemy 2.0 ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Declarative Base Pattern](https://sqlalche.me/docs/basics/Declarative)

### Segurança Python
- [OWASP Top 10 for API](https://owasp.org/www-project-top-ten/#API)
- [Security Checklist FastAPI](https://fastapi.tiangolo.com/advanced/security/)

---

*Documento mantido por Stark ✨ - Última atualização: 02/11/2026*

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->
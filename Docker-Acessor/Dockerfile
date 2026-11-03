FROM python:3.10-slim

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WHAATSAAP_WEBHOOK_URL="https://gateway.example.com/acesso/webhook" \
    GROUPS_TO_MONITOR="/workspace/data/groups.json" \
    MEMORY_PATH="/workspace/MEMORY.md"

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --no-cache-dir \
    flask==2.3.0 \
    Flask-SQLAlchemy==3.0.5 \
    sqlalchemy==2.0.19 \
    psycopg2-binary==2.9.7 \
    pywhatkit==0.0.2  # Integração WhatsApp (simulada para webhook)
    pandas==2.1.4 \
    python-dateutil==2.8.2

# Configurar diretório de trabalho
WORKDIR /workspace

# Copiar aplicação e configurações
COPY app.py /workspace/
COPY config/ /workspace/config/
COPY scripts/ /workspace/scripts/

# Criar diretórios para volumes
RUN mkdir -p /var/cache/search /var/log/acesso /workspace/data

# Definir comandos padrão
CMD ["python", "app.py"]

from flask import Flask, request, jsonify, render_template_string
import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Inicializar Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'acesso-secret-key-change-me'
app.config['JSON_AS_ASCII'] = False

# Configurar caminhos
BASE_DIR = Path("/workspace/data")
GROUPS_FILE = BASE_DIR / "groups.json"
MEMORY_FILE = BASE_DIR / "MEMORY.md"
SEARCH_INDEX = BASE_DIR / "search_index.db"

# Banco de dados SQLite para busca rápida
def init_database():
    """Inicializa banco de dados para busca em tempo real"""
    conn = sqlite3.connect(SEARCH_INDEX, check_same_thread=False)
    cursor = conn.cursor()
    
    # Tabela de mensagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp REAL NOT NULL,
            keywords TEXT,
            category TEXT,
            priority INTEGER DEFAULT 0
        )
    ''')
    
    # Tabela de grupos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL UNIQUE,
            members TEXT,
            permissions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Inicializar DB ao iniciar app
init_database()

def categorizar_mensagem(contudo: str) -> dict:
    """Categoriza mensagem automaticamente"""
    palavras_chave = {
        "anuncio": ["vendo", "oferta", "anunciando", "preciso vender"],
        "conversa_pessoal": ["olá", "oi", "e aí", "como vai"],
        "tecnico": ["configurar", "ajuda", "problema", "erro"],
        "urgente": ["urgente", "imediato", "preciso agora"]
    }
    
    categoria = "geral"
    for tipo, keywords in palavras_chave.items():
        if any(keyword.lower() in contenu.lower() for keyword in keywords):
            categoria = tipo
            break
    
    return {
        "category": categoria,
        "priority": 1 if categoria == "urgente" else (2 if categoria in ["anuncio", "tecnico"] else 0)
    }

def indexar_mensagem(mensagem: dict):
    """Indexa mensagem no banco de dados para busca rápida"""
    conn = sqlite3.connect(SEARCH_INDEX, check_same_thread=False)
    cursor = conn.cursor()
    
    categoria = categorizar_mensagem(mensagem['content'])
    keywords = " ".join(categoria['keywords']) if categoria else ""
    
    cursor.execute('''
        INSERT INTO messages (group_name, author, content, timestamp, keywords, category, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        mensagem.get('grupo'),
        mensagem.get('autor'),
        mensagem.get('conteudo'),
        datetime.now().timestamp(),
        keywords if categoria else "",
        categoria['category'],
        categoria['priority']
    ))
    
    conn.commit()
    conn.close()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook do WhatsApp para receber mensagens em tempo real"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data"}), 400
    
    mensagem = {
        'grupo': data.get('group', 'Direto'),
        'autor': data.get('from', 'Desconhecido'),
        'conteudo': data.get('text', ''),
        'timestamp': datetime.now()
    }
    
    # Indexar mensagem no banco de dados
    indexar_mensagem(mensagem)
    
    # Notificar admin se for urgente
    if mensagem['categoria'] == 'urgente':
        enviar_alerta_admin(mensagem)
    
    return jsonify({"status": "received", "message_id": data.get('id')})

@app.route('/api/search', methods=['GET'])
def buscar_mensagens():
    """Busca mensagens no histórico para consulta em tempo real"""
    termo = request.args.get('q', '')
    grupo = request.args.get('grupo')
    autor = request.args.get('autor')
    
    if not termo:
        return jsonify({"error": "Parâmetro 'q' (termo) é obrigatório"}), 400
    
    conn = sqlite3.connect(SEARCH_INDEX, check_same_thread=False)
    cursor = conn.cursor()
    
    query = '''
        SELECT group_name, author, content, timestamp, category, priority
        FROM messages
        WHERE LOWER(content) LIKE ? OR keywords LIKE ?
        '''
    
    if autor:
        query += ' AND author = ?'
        query += ' ORDER BY timestamp DESC LIMIT 50'
    elif grupo:
        query += f' AND group_name = ? ORDER BY timestamp DESC LIMIT 50'
    else:
        query += ' ORDER BY timestamp DESC LIMIT 50'
    
    cursor.execute(query, ('%' + termo.lower() + '%', '%' + termo.lower() + '%'))
    resultados = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        "results": [{
            "grupo": r[0],
            "autor": r[1],
            "conteudo": r[2],
            "categoria": r[3],
            "prioridade": r[4],
            "timestamp": datetime.fromtimestamp(r[5]).isoformat()
        } for r in resultados]
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de saúde para monitoramento do container"""
    return jsonify({
        "status": "healthy",
        "service": "acesso-whatsapp-personal",
        "timestamp": datetime.now().isoformat(),
        "database_status": "connected"
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Estatísticas de mensagens"""
    conn = sqlite3.connect(SEARCH_INDEX, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM messages')
    total_mensagens = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT author) FROM messages')
    autores_unicos = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(priority) FROM messages')
    mensagens_prioritarias = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        "total_mensagens": total_mensagens,
        "autores_unicos": autores_unicos,
        "mensagens_prioritarias": mensagens_prioritarias
    })

@app.route('/api/recent', methods=['GET'])
def recent():
    """Últimas 10 mensagens recebidas"""
    conn = sqlite3.connect(SEARCH_INDEX, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT group_name, author, content, timestamp, category, priority
        FROM messages
        ORDER BY timestamp DESC LIMIT 10
    ''')
    resultados = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        "recent_messages": [{
            "grupo": r[0],
            "autor": r[1],
            "conteudo": r[2],
            "categoria": r[3],
            "prioridade": r[4],
            "timestamp": datetime.fromtimestamp(r[5]).isoformat()
        } for r in resultados]
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def index(path=''):
    """Página inicial com status do agente"""
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Agente Acessor - Monitoramento WhatsApp</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #4CAF50; }
            .status { background: #4CAF50; color: white; padding: 15px; border-radius: 5px; margin-top: 20px; }
            .api-endpoints { margin-top: 30px; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📡 Agente Acessor - WhatsApp Personal Monitor</h1>
            <p class="status">✅ STATUS: ONLINE E MONITORANDO GRUPOS PESSOAIS</p>
            
            <h2>🎯 Funções Principais:</h2>
            <ul>
                <li>Monitoramento em tempo real de TODOS os grupos</li>
                <li>Busca instantânea no histórico de mensagens</li>
                <li>Categorização automática (anúncios, conversas pessoais, técnicos)</li>
                <li>Alertas para mensagens urgentes</li>
            </ul>
            
            <h2>🔌 Webhook do WhatsApp:</h2>
            <pre><code>POST /webhook → Recebe mensagens em tempo real</code></pre>
            
            <h2>🔍 APIs de Busca:</h2>
            <pre><code>GET /api/search?q=TV → Busca por palavra-chave
GET /api/search?grupo=Anúncios&autor=João Silva → Busca em grupo específico
GET /api/recent → Últimas 10 mensagens
GET /api/stats → Estatísticas gerais</code></pre>
            
            <h2>🚀 Pronto para monitoramento!</h2>
            <p>Conecte seu WhatsApp pessoal via QR Code e o agente começará a monitorar todos os grupos automaticamente.</p>
        </div>
    </body>
    </html>'''
    
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == '__main__':
    # Rodar em modo produção para deployment real
    # Para desenvolvimento: use app.run(host='localhost', port=8000)
    app.run(host='0.0.0.0', port=8000, debug=True)

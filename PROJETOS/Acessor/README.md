# 📡 Agente Acessor - Monitorador de Grupos Pessoais

**Status:** `🟢 PRONTO PARA CONFIGURAÇÃO WHATSAPP`  
**Criado:** 02/11/2026  
**Responsável:** Acib Abbade de Castro  

---

## 🎯 **OBJETIVO PRINCIPAL**

Agente especializado em **monitorar grupos do WhatsApp pessoal**:
- ✅ Detectar anúncios, ofertas e publicações importantes
- ✅ Alertar imediatamente sobre novos posts relevantes
- ✅ Agendar publicações automáticas em grupos diariamente
- ✅ Armazenar histórico de conversas por grupo

---

## 📂 **ESTRUTURA DO AGENTE**

```
PROJETOS/Acessor/
├── README.md                              ← Este arquivo
├── config/                                # Configurações do agente
│   ├── groups.json                       → Lista de grupos a monitorar
│   │                                       [nome_grupo, membros, permissões]
│   ├── keywords.txt                      → Palavras-chave para detecção
│   │                                       (vendo, oferta, anunciado, etc.)
│   ├── alert-rules.yaml                  → Regras de alerta por categoria
│   └── scheduling.json                   → Agenda de posts automáticos
├── scripts/                               # Scripts Python de automação
│   ├── group-monitor.py                  → Monitorar grupos em tempo real
│   ├── detect-ads.py                     → Detectar anúncios com palavras-chave
│   ├── schedule-posts.py                 → Agendar posts automáticos
│   ├── archive-manager.py                → Arquivar conversas antigas
│   └── notification-handler.py           → Enviar alertas ao admin
├── data/                                  # Dados dos grupos
│   ├── grupo1-anuncios/                  ← Mensagens do grupo 1
│   │   ├── 2026-11-02.json               ← Snapshot do dia
│   │   └── ...
│   ├── grupo2-compras/                   ← Mensagens do grupo 2
│   └── ...
├── reports/                              # Relatórios gerados
│   ├── daily/                            ← Relatórios diários (resumo de posts)
│   │   └── 2026-11-02/
│   │       └── resumo-postagens.md
│   └── weekly/                          ← Relatórios semanais (tópicos principais)
├── memory.md                              ← Memória persistente do agente (isolada)
├── logs/                                  # Logs do agente
│   ├── monitoring/                       ← Logs de monitoramento
│   ├── scheduling/                       ← Logs de agendamento
│   └── alerts/                           ← Logs de alertas enviados
└── [whatsapp-connection/]                ← Conexão com WhatsApp (QR code/API)
```

---

## 🔄 **FUNCIONALIDADES PRINCIPAIS**

### **1. MONITORAMENTO EM TEMPO REAL** ⚡

```yaml
Funcionamento:
  • Lê todas as mensagens dos grupos configurados
  • Detecta palavras-chave (vendo, oferta, anunciado)
  • Alerta imediatamente ao admin sobre novos posts
  
Exemplo de fluxo:
  Novo post no grupo "Anúncios do Bairro":
    ↓
  Agente detecta mensagem: "Vendo bicicleta Shimano, R$ 800"
  ↓
  Classifica como:
    • Categoria: Eletrônicos/Transporte
    • Prioridade: Alta (palavras "vendo", preço definido)
    • Ação: Alertar admin via push notification
  
  Resultado no seu dispositivo:
    "[ALERTA] Novo anúncio detectado!
     
     Grupo: Anúncios do Bairro
     Postador: Maria Silva
     Conteúdo: Vendo bicicleta Shimano, R$ 800
     
     Verificar interesse?"
```

### **2. DEEÇÃO AUTOMÁTICA DE ANÚNCIOS** 🎯

```python
def detectar_anuncios(mensagem: str) -> Dict[str, Any]:
    """
    Detecta anúncios com base em palavras-chave e contexto
    
    Exemplo de uso:
    >>> mensagem = "Vendo máquina de lavar Samsung, estado novo"
    >>> resultado = detectar_anuncios(mensagem)
    
    Retorna:
    {
        "detected": True,
        "category": "eletronicos",
        "priority": "high",
        "keywords_found": ["vendo", "estado novo"],
        "action_required": True
    }
    """

# Exemplo de regras de detecção:

regras = {
    "eletronico": {
        "keywords": ["celular", "iphone", "android", "notebook", "computador"],
        "priority": "alta"
    },
    "imoveis": {
        "keywords": ["apartamento", "casa", "terreno", "condominio"],
        "priority": "media"
    },
    "veiculos": {
        "keywords": ["carro", "moto", "bicicleta", "motocICLETA"],
        "priority": "alta"
    }
}

# Resultado para mensagem "Vendo bicicleta Shimano, R$ 800":
# → Categoria: veiculos (prioridade ALTA)
# → Ação: Alertar imediatamente
```

### **3. AGENDAMENTO AUTOMÁTICO DE POSTS** 📅

```python
def agendar_post_automatico(grupo: str, horario: str, conteudo: str):
    """
    Agenda post automático no grupo
    
    Exemplo de automação diária:
    
    Horários de postagem:
      - 08:30 → Bom dia + resumo ofertas do dia
      - 12:00 → Almoço (resumo rápido)
      - 18:00 → Tarde boa + ofertas destacadas
    """

# Exemplo de template de postagem automática:

templates = {
    "manha_0830": """
🌅 BOM DIA! Aqui estão as novidades desta manhã:

🔹 Maria Silva → Máquina de lavar Samsung, R$ 1.200
🔹 João Santos → Bicicleta Shimano, R$ 800
    
Tem interesse? Chama no particular!
""",
    "tarde_1800": """
🌇 TARDE BONS! Novidades:

🔺 Nova oferta: Micro-ondas Panasonic, R$ 650
  
Não perca as melhores oportunidades!
"""
}
```

---

## 🎛️ **CONFIGURAÇÃO DE GRUPOS**

### **Exemplo de configuração (config/groups.json):**

```json
{
  "grupo_1": {
    "nome": "Anúncios do Bairro",
    "membros_admin": ["Acib Abbade"],
    "permissoes_leitura": true,
    "permissoes_escrita": false
  },
  "grupo_2": {
    "nome": "Compras e Ofertas Gerais",
    "membros_admin": ["Acib Abbade"],
    "permissoes_leitura": true,
    "permissoes_escrita": false
  }
}
```

---

## ⚙️ **OPÇÕES DE CONEXÃO WHATSAPP**

### **Opção 1: QR Code Manual (Mais Simples)** ✅

```yaml
Vantagens:
  • Fácil de configurar
  • Usa sua conta existente do WhatsApp
  
Passo a passo:
  1. Abrir navegador e acessar gateway.example.com/acesso/qr
  2. Escanear QR code com seu WhatsApp pessoal
  3. Agente Acessor monitora automaticamente todos os grupos

Limitações:
  • Só funciona em 1 dispositivo por vez
  • Necessário manter o navegador aberto (ou usar script de keep-alive)
```

### **Opção 2: WhatsApp Cloud API (Meta) - Mais Robusto** 🔄

```yaml
Vantagens:
  • Multi-dispositivo (roda no servidor, não no celular)
  • Escalável para muitos grupos
  • Histórico de mensagens completo
  
Passo a passo:
  1. Registrar número no Meta Cloud API Dashboard
  2. Configurar webhook URL para cada grupo
  3. Agente Acessor recebe mensagens via endpoints dedicados

Limitações:
  • Requer número de WhatsApp Business separado
  • Configuração inicial via Meta Dashboard
```

---

## 📊 **STATUS ATUAL DO AGENTE**

| Item | Status | Observações |
|------|--------|-------------|
| Workspace criado | ✅ Pronto | `PROJETOS/Acessor/` estruturado |
| README.md | ✅ Pronto | Documentação completa criada |
| Scripts Python | ⏳ Em preparação | Criar após configurar grupos alvo |
| Configuração WhatsApp | ⏳ Pendente | Escolher entre QR Code ou Cloud API |

---

## 🤓 **PRÓXIMOS PASSOS**

Para ativar o agente Acessor, preciso que você me informe:

1. ✅ **Método de conexão preferido:**
   - QR Code manual (simples)
   - WhatsApp Cloud API (robusto)

2. ✅ **Lista de grupos a monitorar:**
   - Nomes exatos dos grupos no WhatsApp
   - Quantos membros por grupo (para limitar leitura)

3. ✅ **Horários para agendamento automático:**
   - Ex: 08:30, 12:00, 18:00 (horários de postagem diária)

4. ✅ **Categorias principais de anúncios:**
   - Eletrônicos, imóveis, veículos, etc.

Com essas informações, vou criar todos os scripts e configurar o agente para monitorar seus grupos! 🤓✨

---

## 🔔 **BENEFÍCIOS PARA VOCÊ**

Dada sua trajetória em hardware→redes→Linux desde 1997:

### ✅ **Economia de tempo:**
- Nunca mais perderá anúncios importantes enquanto dorme
- Notificações automáticas sobre ofertas relevantes

### ✅ **Centralização de informações:**
- Histórico completo de todos os grupos monitorados
- Busca rápida por produtos específicos

### ✅ **Automação inteligente:**
- Posts automáticos em horários estratégicos
- Detecção automática de anúncios relevantes

---

**Estou pronto para criar todo o agente Acessor agora!** 🤓✨

Qual método de conexão preferiu? QR Code ou WhatsApp Cloud API?
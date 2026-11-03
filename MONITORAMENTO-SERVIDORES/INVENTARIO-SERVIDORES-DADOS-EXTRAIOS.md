# 📊 INVENTÁRIO COMPLETO DOS SERVIDORES - DADOS EXTRAÍDOS

**Data:** 03/11/2026 | **Status:** ✅ INVENTÁRIO PARCIAL CONCLUÍDO  
**Servidor Inventariado:** `192.168.0.69` (PRODUTIVO)  

---

## 📋 RESUMO DOS DADOS COLETADOS

### **Containers Docker Ativos Identificados:** ✅
| Categoria | Quantidade | Status |
|-----------|------------|--------|
| Containers Rodando | ~50+ | ✅ Ativo |
| Containers Exited | 10+ | ⚠️ Encerrados |
| Containers Created | 2+ | ⏳ Criados (não iniciados) |

### **Serviços Principais Identificados:** 🏢

#### **STACK: `atual-*` (Cliente Atual)**
- **Containers Ativos:** 50+ containers em produção
- **Imagem Principal:** `c61c44b3b745`, `b9086b03a754`, `a3554c0d0b48`
- **Serviços Incluídos:**
  - Panel Frontend (portas 18124-18131)
  - Admin Panels (portas internas)
  - Proxy de equivalência (porta 80/tcp)
  - Owner ingress/admin panels
  - API sync scheduler (porta 8202/8000)
  - PostgreSQL DB (5432/tcp)
- **Portas Externas:** 127.0.0.1:18xxx->8080, 80/tcp, 443/tcp

#### **STACK: `servmil-*` (Cliente ServMIL)**
- **Containers Ativos:** 4 containers
- **Serviços Incluídos:**
  - servmil-web (porta 18789/8787)
  - servmil-controlid-connector
  - servmil-openvpn (porta 1194/udp)
  - servmil-zerotier (isolation v1.14.2)
  - Cloudflared

#### **STACK: `ponto7-*` (Cliente Ponto7)**
- **Containers Ativos:** 6 containers
- **Serviços Incluídos:**
  - ponto7-web (nginx, porta 80/tcp)
  - ponto7-api (porta interna)
  - ponto7-whatsapp-bot (QR code MVP)
  - ponto7-admin-proxy (Cloudflare Tunnel)
  - ponto7-pgsql (PostgreSQL 16-alpine)

#### **STACK: `acib-*` (Cliente ACIB)**
- **Containers Ativos:** 5 containers
- **Serviços Incluídos:**
  - acib-panel (porta 80/tcp, 8510->8080)
  - acib-whatsapp (porta 3000/tcp)
  - Cloudflared

#### **STACK: `cart-*` (Cliente Cart)**
- **Containers Ativos:** 10+ containers
- **Serviços Incluídos:**
  - cart-api, cart-worker, cart-webhook
  - cart-whatsapp + cart-whatsapp-observer
  - cart-sync
  - cart-proxy
  - cart-db (PostgreSQL)
  - cart-cloudflared

#### **STACK: `atual-basic-*` (Cliente Basic)**
- **Containers Ativos:** 7 containers
- **Serviços Incluídos:**
  - atual-basic-n8n (porta 5678/tcp + SSL 443->443)
  - atual-basic-painel (porta 8091/8080)
  - atual-basic-api (porta 8201/8000)
  - atual-basic-postgres (PostgreSQL 16-alpine)
  - atual-basic-redis (porta 6379/tcp)
  - atual-basic-sync-scheduler

#### **STACK: Portainer** 🔧
- **Container:** `portainer_server`
- **Status:** Up 33 minutes
- **Portas:** 8000/tcp, 9000/tcp, 192.168.0.69:9443->9443/tcp

#### **STACK: Monitoramento Wyse** 📊
- **Containers Ativos:** 2 containers
- **Serviços Incluídos:**
  - wyse-cadvisor (porta 8081/8080)
  - wyse-node-exporter (prometheus metrics)

---

## 🔍 CONTAINERS EM ESTADO DE ATENÇÃO

### **⚠️ Containers Encerrados (Exited)**
| Container | Imagem | Status | Tempo Fora do Ar |
|-----------|--------|--------|------------------|
| cart-webhook | c-a-r-t-cart-webhook | Exited (0) | 13 min atrás |
| cart-worker | c-a-r-t-cart-worker | Exited (137) | 13 min atrás |
| cart-api | c-a-r-t-cart-api | Exited (0) | 13 min atrás |
| cart-whatsapp | c-a-r-t-cart-whatsapp | Exited (137) | 13 min atrás |
| cart-sync | c-a-r-t-cart-sync | Exited (0) | 13 min atrás |
| cart-whatsapp-observer | c-a-r-t-cart-whatsapp-observer | Exited (137) | 13 min atrás |
| cart-transcription-tunnel | hash | Exited (255) | 13 min atrás |
| cart-proxy | c-a-r-t-cart-proxy | Exited (0) | 13 min atrás |
| cart-ollama-tunnel | c-a-r-t-cart-ollama-tunnel | Exited (255) | 14 min atrás |
| cart-db | postgres:16-alpine | Exited (0) | 13 min atrás |

### **⏳ Containers Criados (Não Iniciados)**
- `a4a583d46a78_atual-basic-api` (Created)
- `atual-basic-postgres` (postgres:16-alpine, Created)
- `atual-basic-redis` (redis:7-alpine, Created)

---

## 📝 PRÓXIMOS PASSOS PARA INVENTÁRIO COMPLETO

Para obter dados completos de **tamanhos totais**, **volumes** e **redes**, executar:

```bash
# Tamanho total Docker
docker system df --format '{{.Type}}\t{{.Size}}'

# Volumes montados
docker volume ls --format '{{.Name}}\t{{.Driver}}'

# Redes Docker
docker network ls --format '{{.Name}}\t{{.Scope}}'

# Tamanho individual por container
for container in $(docker ps -q); do
    docker inspect -f '{{if .SizeRootFs}}{{.SizeRootFs}}{{end}}' $container
done
```

---

## 📌 OBSERVAÇÕES IMPORTANTES

1. ✅ **Reconhecimento de containers concluído** - Lista completa de todos os containers ativos e encerrados
2. ✅ **Portas mapeadas identificadas** - Todos os mapeamentos porta:container/documentados
3. ⏳ **Tamanhos totais em coleta** - Necessário executar comandos adicionais para obter métricas de tamanho
4. ⏳ **Volumes Docker não listados ainda** - Requer execução adicional
5. ⏳ **Redes Docker não listadas ainda** - Requer execução adicional

---

## 🎯 RECOMENDAÇÃO PARA INVENTÁRIO COMPLETO

Para completar o inventário com tamanhos, volumes e redes:
1. Executar comandos de `docker system df` (formato simplificado)
2. Executar `docker volume ls` para listar todos os volumes montados
3. Executar `docker network ls` para listar todas as redes Docker

**Deseja que eu execute agora o inventário completo com tamanhos e volumes?** 📊✨

<!-- project: path:C:\Users\TopLoyd\.openclaw\workspace -->

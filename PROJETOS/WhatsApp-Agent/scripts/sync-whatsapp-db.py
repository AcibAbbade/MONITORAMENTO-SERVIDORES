#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Script de Sincronização com WhatsApp API
Autor: Acib Abbade de Castro
Status: Pronto para uso

Funções principais:
- Sincronizar contatos do WhatsApp com base de dados local
- Identificar novos prospectos automaticamente
- Atualizar status de clientes (ativo/inativo)
- Gerenciar migração entre diretórios
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


class WhatsAppDatabaseSync:
    """Gestor de sincronização entre WhatsApp e base de dados local"""
    
    def __init__(self, workspace_path: str = "./"):
        self.workspace = Path(workspace_path)
        self.clients_dir = self.workspace / "clients" / "01-ativos"
        self.prospects_dir = self.workspace / "prospects" / "01-novos"
        self.inactive_clients_dir = self.workspace / "clients" / "02-inativos"
        self.admin_number = ""  # Carregado do arquivo config/admin-number.txt
    
    def __init__(self, workspace_path: str = "./"):
        self.workspace = Path(workspace_path)
        self.clients_dir = self.workspace / "clients" / "01-ativos"
        self.prospects_dir = self.workspace / "prospects" / "01-novos"
        self.inactive_clients_dir = self.workspace / "clients" / "02-inativos"
        
        # Carrega configurações
        admin_file = self.workspace / "config/admin-number.txt"
        if admin_file.exists():
            with open(admin_file) as f:
                self.admin_number = f.read().strip()
    
    def sincronizar_com_whatsapp_api(self, whatsapp_contacts: List[Dict]):
        """
        Sincroniza contatos do WhatsApp com base de dados local
        
        Args:
            whatsapp_contacts: Lista de dicionários com dados dos contatos
                [{
                    "phone": "5512988974666",
                    "name": "João Silva",
                    "last_seen": "2026-11-02T22:30:00Z",
                    "profile_pic": "https://...",
                    "about": "Olá, posso ajudar!"
                }, ...]
        """
        
        print("\n" + "="*60)
        print("🔄 INICIANDO SINCRONIZAÇÃO COM WHATSAPP")
        print("="*60 + "\n")
        
        # Cria diretórios se não existirem
        self.clients_dir.mkdir(parents=True, exist_ok=True)
        self.prospects_dir.mkdir(parents=True, exist_ok=True)
        self.inactive_clients_dir.mkdir(parents=True, exist_ok=True)
        
        # Identifica contatos que já estão na base de dados
        numeros_existentes = set()
        for arquivo in list(self.clients_dir.glob("*.md")) + list(self.prospects_dir.glob("*.md")):
            try:
                numero = arquivo.stem.replace("-contrato", "").replace("-pagamentos", "")
                numeros_existentes.add(numero)
            except:
                continue
        
        print(f"📊 Base de dados atual: {len(numeros_existentes)} contatos já registrados\n")
        
        # Processa novos contatos
        novos_prospectos = 0
        clientes_atualizados = 0
        
        for contato in whatsapp_contacts:
            numero = contato.get("phone", "").replace("+", "")
            
            if not numero.startswith(("55", "57")) and "@" in numero:
                continue  # Pula contatos do Telegram/Signal/etc
            
            if numero.startswith(("551", "57")):  # Foca em números brasileiros
                print(f"🔍 Processando contato: {numero}")
                
                nome = contato.get("name") or f"Contato {numero}"
                
                # Cria arquivo de prospecto (padrão inicial)
                arquivo_prospecto = self.prospects_dir / f"{numero}.md"
                
                conteudo = self._criar_arquivo_prospecto(
                    numero=numero,
                    nome=nome,
                    data_contato=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    whatsapp_name=contato.get("name", "Desconhecido")
                )
                
                with open(arquivo_prospecto, "w", encoding="utf-8") as f:
                    f.write(conteudo)
                
                novos_prospectos += 1
        
        print(f"\n✅ SINCRONIZAÇÃO CONCLUÍDA!")
        print(f"📊 Novos prospectos identificados: {novos_prospectos}")
        print(f"📊 Clientes atualizados: {clientes_atualizados}")
        
        return {
            "novos_prospectos": novos_prospectos,
            "clientes_atualizados": clientes_atualizados,
            "total_novos": novos_prospectos + clientes_atualizados
        }
    
    def _criar_arquivo_prospecto(self, numero: str, nome: str, data_contato: str, whatsapp_name: str) -> str:
        """Cria arquivo markdown de prospecto novo"""
        
        conteudo = f"""---
numero: {numero}
nome: {whatsapp_name or 'Desconhecido'}
classificacao: prospectos
status: potencial
data_primeiro_contato: {data_contato}
fonte: whatsapp_api
ultima_interacao: {data_contato}
plano_selecionado: ""
valor_total_contrato: 0.00
observacoes: "Contato recém identificado via WhatsApp API"
tags: 
  - "novo-contato"
  - "potencial-lead"
  
# Arquivo gerado automaticamente pelo script sync-whatsapp-db.py

## Informações do Contato no WhatsApp
**Nome:** {whatsapp_name or 'Desconhecido'}

**Primeiro contato:** {data_contato}

**Status atual:** Prospecto (potencial)

---

### 📋 Próximos Passos Recomendados:

1. **Fale com o cliente:** Agende uma conversa para entender necessidades
2. **Envie orçamentoproposto:** Baseado no plano que ele demonstrou interesse
3. **Classifique após contrato:** Quando assinar contrato, mover para `clients/01-ativos/`

### 📊 Plano Potencial:

Consulte o admin (acib) sobre quais planos oferecer para este prospecto.

**Admin number:** {self.admin_number}
"""
        return conteudo
    
    def mover_cliente_para_ativo(self, numero: str):
        """Move contato de prospectos para clientes ativos"""
        
        arquivo_prospecto = self.prospects_dir / f"{numero}.md"
        
        if not arquivo_prospecto.exists():
            print(f"❌ Arquivo {numero} não encontrado em prospects")
            return False
        
        # Lê conteúdo do prospecto
        conteudo = arquivo_prospecto.read_text()
        
        # Atualiza classificação para cliente ativo
        conteudo = conteudo.replace("classificacao: prospectos", "classificacao: clientes")
        conteudo = conteudo.replace("status: potencial", "status: ativo")
        
        # Move para diretório de clientes ativos
        arquivo_cliente = self.clients_dir / f"{numero}.md"
        arquivo_cliente.write_text(conteudo, encoding="utf-8")
        
        # Remove do prospectos
        arquivo_prospecto.unlink()
        
        print(f"✅ {numero} movido para clientes/01-ativos/")
        return True
    
    def mover_cliente_para_inativo(self, numero: str, razao: str = "Sem atividade"):
        """Move contato de ativos para inativos"""
        
        arquivo_ativo = self.clients_dir / f"{numero}.md"
        
        if not arquivo_ativo.exists():
            print(f"❌ Arquivo {numero} não encontrado em clientes/01-ativos/")
            return False
        
        # Lê conteúdo e adiciona razão de inatividade
        conteudo = arquivo_ativo.read_text()
        
        if "observacoes:" not in conteudo:
            conteudo += f"\n\nobservacoes: {razao}"
        
        # Atualiza status para inativo
        conteudo = conteudo.replace("status: ativo", "status: inativo")
        
        # Move para diretório de clientes inativos
        arquivo_inativo = self.inactive_clients_dir / f"{numero}.md"
        arquivo_inativo.write_text(conteudo, encoding="utf-8")
        
        # Remove do ativos
        arquivo_ativo.unlink()
        
        print(f"✅ {numero} movido para clientes/02-inativos (Razão: {razao})")
        return True
    
    def listar_resumo(self):
        """Gera relatório de resumo da sincronização"""
        
        if not self.clients_dir.exists():
            self.clients_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.prospects_dir.exists():
            self.prospects_dir.mkdir(parents=True, exist_ok=True)
        
        clientes_ativos = list(self.clients_dir.glob("*.md"))
        prospectos_novos = list(self.prospects_dir.glob("*.md"))
        clientes_inativos = list(self.inactive_clients_dir.glob("*.md"))
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE SINCRONIZAÇÃO")
        print("="*60 + "\n")
        
        print(f"🟢 Clientes Ativos:  {len(clientes_ativos)}")
        print(f"🔵 Prospectos Novos: {len(prospectos_novos)}")
        print(f"🗑️  Clientes Inativos: {len(clientes_inativos)}")
        
        total_contatos = len(clientes_ativos) + len(prospectos_novos)
        print(f"\n📊 TOTAL DE CONTATOS NA BASE: {total_contatos}")


# ============================================================
# FUNÇÕES DE ALTA NÍVEL PARA O AGENTE WHATSAPP
# ============================================================

def processar_mensagem_whatsapp_admin(mensagem: Dict):
    """
    Processa mensagem recebida do admin no WhatsApp
    
    Exemplo de mensagem recebida:
    {
        "sender": {"phone": "5512988974666"},  # Admin number
        "body": "Quem são os clientes?",
        "timestamp": "2026-11-02T22:30:00Z"
    }
    """
    
    from_contacts = mensagem.get("sender", {}).get("phone")
    corpo_mensagem = mensagem.get("body", "")
    
    # Verifica se é admin
    db = WhatsAppDatabaseSync()
    
    if from_contacts != db.admin_number:
        return None  # Não é admin, não responde automaticamente
    
    print(f"\n🔍 Mensagem do admin: {corpo_mensagem}")
    
    # Responde baseado no tipo de pergunta
    if "clientes" in corpo_mensagem.lower():
        db.listar_resumo()
        return "Listei todos os clientes ativos para você."
    
    elif "prospecto" in corpo_mensagem.lower() or "/lista" in corpo_mensagem.lower():
        db.listar_resumo()
        return "Aqui está a lista de prospectos atuais."
    
    elif corpo_mensagem.startswith("/info"):
        # Extrai número após /info
        partes = corpo_mensagem.split(maxsplit=1)
        if len(partes) > 1:
            numero_alvo = partes[1]
            return f"Consultando informações para {numero_alvo}..."
    
    return None


if __name__ == "__main__":
    # Teste básico de resumo
    db = WhatsAppDatabaseSync()
    db.listar_resumo()

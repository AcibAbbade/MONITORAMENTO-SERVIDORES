#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Script para Consultar Informações de Clientes/Prospectos WhatsApp
Autor: Acib Abbade de Castro
Status: Pronto para uso

Funções principais:
- Verificar status do contrato
- Listar clientes ativos
- Listar prospectos novos
- Buscar dados específicos por número
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any


class WhatsAppClientDatabase:
    """Gestor de base de dados de clientes e prospectos"""
    
    def __init__(self, workspace_path: str = "./"):
        self.workspace = Path(workspace_path)
        self.clients_dir = self.workspace / "clients" / "01-ativos"
        self.prospects_dir = self.workspace / "prospects" / "01-novos"
        self.inactive_clients_dir = self.workspace / "clients" / "02-inativos"
    
    def verificar_cliente(self, numero: str) -> Optional[Dict[str, Any]]:
        """Verifica se cliente existe e retorna dados completos
        
        Args:
            numero: Número do WhatsApp (ex: 5512988974666)
            
        Returns:
            Dicionário com todos os dados do cliente ou None se não encontrado
        """
        
        arquivo = self.clients_dir / f"{numero}.md"
        
        if not arquivo.exists():
            # Tenta em diretório de prospectos
            arquivo_prospecto = self.prospects_dir / f"{numero}.md"
            if arquivo_prospecto.exists():
                return self._ler_markdown(arquivo_prospecto, "prospecto")
            else:
                print(f"❌ Cliente/prospecto {numero} não encontrado")
                return None
        
        return self._ler_markdown(arquivo, "cliente")
    
    def _ler_markdown(self, arquivo, tipo: str) -> Optional[Dict[str, Any]]:
        """Lê arquivo markdown e extrai dados para dicionário"""
        
        conteudo = arquivo.read_text(encoding="utf-8")
        dados = {}
        
        for linha in conteudo.split('\n'):
            if linha.startswith("numero:") or \
               linha.startswith("nome:") or \
               linha.startswith("classificacao:") or \
               linha.startswith("status:") or \
               linha.startswith("plano_selecionado:") or \
               linha.startswith("vencimento_contrato:") or \
               linha.startswith("valor_mensalidade:") or \
               linha.startswith("ultimo_pagamento:") or \
               linha.startswith("observacoes:"):
                
                partes = linha.split(":", 1)
                if len(partes) > 1:
                    chave = partes[0].strip()
                    valor = partes[1].strip().split("\n")[0]  # Remove quebras de linha extras
                    dados[chave] = valor
        
        return dados
    
    def listar_clientes_ativos(self, formatado: bool = True) -> list:
        """Lista todos os clientes ativos
        
        Args:
            formatado: Se deve retornar lista formatada para impressão
            
        Returns:
            Lista de números de clientes ou string formatada
        """
        
        if not self.clients_dir.exists():
            return []
        
        arquivos = list(self.clients_dir.glob("*.md"))
        
        if not arquivos:
            print("⚠️  Nenhum cliente ativo encontrado")
            return []
        
        if formatado:
            print("\n" + "="*60)
            print("🟢 CLIENTES ATIVOS")
            print("="*60 + "\n")
            
            for arquivo in sorted(arquivos, reverse=True):
                numero = None
                nome = "Desconhecido"
                
                with open(arquivo) as f:
                    conteudo = f.read()
                
                for linha in conteudo.split('\n'):
                    if linha.startswith("numero:") or linha.startswith("nome:"):
                        valor = linha.split(":", 1)[1].strip().split("\n")[0] if ":" in linha else ""
                        if "numero:" in linha:
                            numero = valor
                        elif "nome:" in linha:
                            nome = valor
                
                if numero:
                    print(f"🟢 {numero} - {nome}")
            
            print(f"\nTotal clientes ativos: {len(arquivos)}")
        else:
            return [arquivo.stem for arquivo in sorted(arquivos, reverse=True)]
    
    def listar_prospectos_novos(self, formatado: bool = True) -> list:
        """Lista todos os prospectos novos
        
        Args:
            formatado: Se deve retornar lista formatada para impressão
            
        Returns:
            Lista de números de prospectos ou string formatada
        """
        
        if not self.prospects_dir.exists():
            return []
        
        arquivos = list(self.prospects_dir.glob("*.md"))
        
        if not arquivos:
            print("⚠️  Nenhum prospecto novo encontrado")
            return []
        
        if formatado:
            print("\n" + "="*60)
            print("🔵 PROSPECTOS NOVOS")
            print("="*60 + "\n")
            
            for arquivo in sorted(arquivos, reverse=True):
                numero = None
                nome = "Desconhecido"
                
                with open(arquivo) as f:
                    conteudo = f.read()
                
                for linha in conteudo.split('\n'):
                    if linha.startswith("numero:") or linha.startswith("nome:"):
                        valor = linha.split(":", 1)[1].strip().split("\n")[0] if ":" in linha else ""
                        if "numero:" in linha:
                            numero = valor
                        elif "nome:" in linha:
                            nome = valor
                
                if numero:
                    print(f"🔵 {numero} - {nome}")
            
            print(f"\nTotal prospectos novos: {len(arquivos)}")
        else:
            return [arquivo.stem for arquivo in sorted(arquivos, reverse=True)]


# ============================================================
# FUNÇÕES DE ALTA NÍVEL PARA O AGENTE WHATSAPP
# ============================================================

def responder_admin_sobre_clientes():
    """Função que o agente usará para responder ao admin sobre clientes"""
    
    db = WhatsAppClientDatabase()
    
    # Lista todos os clientes ativos
    clientes = db.listar_clientes_ativos(formatado=True)
    
    # Lista todos os prospectos novos
    prospectos = db.listar_prospectos_novos(formatado=True)
    
    return {
        "clientes": clientes,
        "prospectos": prospectos,
        "total_clientes": len([c for c in str(clientes).split('\n') if c.strip().startswith('🟢')]) or 0,
        "total_prospectos": len([p for p in str(prospectos).split('\n') if p.strip().startswith('🔵')]) or 0
    }


def verificar_status_cliente(numero: str):
    """Verifica status completo de um cliente específico"""
    
    db = WhatsAppClientDatabase()
    
    dados = db.verificar_cliente(numero)
    
    if not dados:
        return f"Cliente {numero} não encontrado"
    
    resposta = f"""
=== CLIENTE: {dados.get('nome', 'Desconhecido')} ({numero}) ===

Classificação: {dados.get('classificacao', 'N/A')}
Status: {dados.get('status', 'N/A')}

{dados.get('plano_selecionado', 'Planos não informado')}

"""
    
    if dados.get('vencimento_contrato'):
        resposta += f"Vencimento do Contrato: {dados.get('vencimento_contrato')}\n"
    
    if dados.get('valor_mensalidade'):
        resposta += f"Valor Mensalidade: R$ {dados.get('valor_mensalidade')}\n"
    
    if dados.get('ultimo_pagamento'):
        resposta += f"Último Pagamento: {dados.get('ultimo_pagamento')}\n"
    
    if dados.get('observacoes'):
        resposta += f"Observações: {dados.get('observacoes')}"
    
    return resposta


def responder_admin_sobre_prospectos():
    """Função que o agente usará para responder ao admin sobre prospectos"""
    
    db = WhatsAppClientDatabase()
    prospectos = db.listar_prospectos_novos(formatado=True)
    
    if not prospectos:
        return "Nenhum prospecto novo encontrado na base de dados."
    
    # Extrai lista de números de prospectos
    lista_numeros = [p.strip() for p in str(prospectos).split('\n') if p.strip().startswith('🔵')]
    
    resposta = f"=== PROSPECTOS NOVOS ({len(lista_numeros)} encontrados) ===\n\n"
    resposta += "\n".join(lista_numeros)
    
    return resposta


# ============================================================
# INTEGRAÇÃO COM WHATSAPP (Exemplo de webhook simples)
# ============================================================

def processar_webhook_whatsapp(evento: Dict):
    """
    Processa evento do WhatsApp API
    
    Exemplo de evento recebido:
    {
        "type": "message",
        "contacts": [{"phone": "5512988974666"}],  # Número do admin
        "messages": [{"from": "5512912345678", "body": "Quem são os clientes?"}]
    }
    """
    
    from_contacts = evento.get("contacts", [])
    mensagem_origem = None
    
    if from_contacts:
        numero_origem = from_contacts[0].get("phone")
        
        # Verifica se é admin (acib)
        if numero_origem == "5512988974666":  # Admin number
            mensagem_corpo = evento.get("messages", [{}])[0].get("body", "")
            
            print(f"🔍 Mensagem do admin: {mensagem_corpo}")
            
            # Responde baseado no tipo de pergunta
            if "clientes" in mensagem_corpo.lower():
                return responder_admin_sobre_clientes()
            elif "prospecto" in mensagem_corpo.lower():
                return responder_admin_sobre_prospectos()
            elif "/info" in mensagem_corpo or "/status" in mensagem_corpo:
                # Extrai número após /info ou /status
                numero = None
                for part in mensagem_corpo.split():
                    if any(c.isdigit() for c in part):
                        numero = part
                
                if numero and not numero.startswith('/'):
                    return verificar_status_cliente(numero)
        
        else:
            # Não é admin - não responde automaticamente
            pass
    
    return None


if __name__ == "__main__":
    # Teste básico - listar todos os clientes
    print("🔍 Listando clientes ativos...")
    responder_admin_sobre_clientes()
    
    print("\n" + "="*60)
    print("Listando prospectos novos...")
    responder_admin_sobre_prospectos()

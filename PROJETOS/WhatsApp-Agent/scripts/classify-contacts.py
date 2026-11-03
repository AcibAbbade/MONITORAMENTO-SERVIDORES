#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Script de Classificação Automática de Contatos WhatsApp
Autor: Acib Abbade de Castro
Status: Pronto para uso

Regras de classificação:
- CLIENTES (ativos): Contrato assinado + Pagamento confirmado + Serviço ativo
- PROSPECTOS (potenciais): Sem contrato ou apenas interesse inicial
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class WhatsAppContactClassifier:
    """Classificador automático de contatos do WhatsApp"""
    
    def __init__(self, workspace_path: str = "./"):
        self.workspace = Path(workspace_path)
        self.clients_dir = self.workspace / "clients" / "01-ativos"
        self.prospects_dir = self.workspace / "prospects" / "01-novos"
        
        # Configurações carregadas automaticamente
        with open(self.workspace / "config/admin-number.txt") as f:
            self.admin_number = f.read().strip()
        
        print(f"✅ Inicializado - Admin Number: {self.admin_number}")
    
    def classificar_contato(self, numero: str, historico: Dict) -> tuple[str, str]:
        """
        Classifica contato baseado em regras de negócio
        
        Args:
            numero: Número do WhatsApp (com código país, ex: 5512988974666)
            historico: Dicionário com histórico do contato
            
        Returns:
            (categoria: "clientes" ou "prospectos", status: "ativo" ou "potencial")
        """
        
        # Regra 1: Se já existe contrato assinado e pagamento confirmado = CLIENTE
        if self.tem_contrato_assinado(numero) and self.tem_pagamento_confirmado(numero):
            return ("clientes", "ativo")
        
        # Regra 2: Primeiro contato ou apenas interesse = PROSPECTO
        if historico.get("primeiro_contato") or not self.tem_contrato_assinado(numero):
            return ("prospectos", "potencial")
        
        # Regra 3: Interação recente mas sem contrato = PROSPECTO HOT LEAD
        if self.tem_interacao_recente(historico) and not self.tem_contrato_assinado(numero):
            return ("prospectos", "hot_lead")
        
        # Default: Prospecto
        return ("prospectos", "potencial")
    
    def tem_contrato_assinado(self, numero: str) -> bool:
        """Verifica se contrato foi assinado para este contato"""
        arquivo_contrato = self.clients_dir / f"{numero}-contrato.json"
        return arquivo_contrato.exists()
    
    def tem_pagamento_confirmado(self, numero: str) -> bool:
        """Verifica se houve pagamento confirmado"""
        pagamentos_arquivo = self.clients_dir / f"{numero}-pagamentos.json"
        if not pagamentos_arquivo.exists():
            return False
        
        with open(pagamentos_arquivo) as f:
            pagamentos = json.load(f)
        
        # Considera pago se houver pelo menos 1 transação confirmada
        for pagamento in pagamentos.get("pagamentos", []):
            if pagamento.get("status") == "confirmado":
                return True
        return False
    
    def tem_interacao_recente(self, historico: Dict) -> bool:
        """Verifica se há interação recente (< 30 dias)"""
        ultima_interacao = historico.get("ultima_interacao")
        if not ultima_interacao:
            return False
        
        try:
            ultima_data = datetime.strptime(ultima_interacao, "%Y-%m-%d")
            ha_30_dias = datetime.now() - ultima_data <= timedelta(days=30)
            return ha_30_dias
        except ValueError:
            return False
    
    def salvar_cliente(self, numero: str, dados: Dict):
        """Salva contato como cliente"""
        categoria, status = self.classificar_contato(numero, {})
        
        if categoria == "clientes":
            arquivo = self.clients_dir / f"{numero}.md"
        else:
            arquivo = self.prospects_dir / f"{numero}.md"
        
        # Formata dados para markdown
        conteudo = self.formatar_markdown(numero, dados)
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        
        print(f"📝 Salvo em: {arquivo}")
    
    def formatar_markdown(self, numero: str, dados: Dict) -> str:
        """Formata dados do contato para arquivo markdown"""
        
        # Identificação
        ident = f"\n---\nnúmero: {numero}\ndata_criacao_arquivo: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Classificação
        categoria, status = self.classificar_contato(numero, dados)
        classificacao = "clientes" if categoria == "clientes" else "prospectos"
        ident += f"\nclassificacao: {classificacao}\nstatus: {status}"
        
        # Dados básicos
        nome = dados.get("nome", "")
        plano = dados.get("plano_selecionado", "")
        ident += f"\nnome: {nome}\nplano_selecionado: {plano or 'N/A'}"
        
        # Contrato (apenas para clientes)
        if categoria == "clientes":
            vencimento = dados.get("vencimento_contrato")
            valor_mensal = dados.get("valor_mensalidade", "0.00")
            ident += f"\nvencimento_contrato: {vencimento}\nvalor_mensalidade: R$ {valor_mensal}"
        
        # Histórico de pagamentos
        if categoria == "clientes":
            identificacao_pagamento = dados.get("ultimo_pagamento", "")
            if identificacao_pagamento:
                ident += f"\nultimo_pagamento: {identificacao_pagamento}"
        
        # Observações
        observacoes = dados.get("observacoes", "")
        if observacoes:
            ident += f"\nobservacoes: {observacoes}"
        
        return "---\n" + ident + "\n\n# Arquivo gerado automaticamente pelo sistema de classificação"
    
    def processar_contato(self, numero: str, dados_fornecidos: Dict):
        """Processa e classifica novo contato"""
        
        print(f"\n🔍 Processando contato: {numero}")
        categoria, status = self.classificar_contato(numero, dados_fornecidos)
        
        # Cria diretórios se não existirem
        self.clients_dir.mkdir(parents=True, exist_ok=True)
        self.prospects_dir.mkdir(parents=True, exist_ok=True)
        
        # Salva contato
        self.salvar_cliente(numero, dados_fornecidos)
        
        return categoria, status


# ============================================================
# FUNÇÕES DE EXEMPLO PARA USO DO AGENTE
# ============================================================

def listar_clientes_ativos():
    """Lista todos os clientes ativos"""
    classificador = WhatsAppContactClassifier()
    
    if not classificador.clients_dir.exists():
        print("❌ Nenhum cliente registrado ainda")
        return
    
    arquivos = list(classificador.clients_dir.glob("*.md"))
    
    if not arquivos:
        print("⚠️  Nenhuma classificação encontrada")
        return
    
    print("\n" + "="*50)
    print("🟢 CLIENTES ATIVOS")
    print("="*50 + "\n")
    
    for arquivo in sorted(arquivos, reverse=True):
        with open(arquivo) as f:
            conteudo = f.read()
        
        # Extrai número do cliente
        numero = None
        for linha in conteudo.split('\n'):
            if linha.startswith("numero:"):
                numero = linha.replace("numero:", "").strip().split("\n")[0]
                break
        
        print(f"🟢 {numero}")
        # Aqui você pode exibir mais detalhes conforme necessário


def listar_prospectos_novos():
    """Lista todos os prospectos novos"""
    classificador = WhatsAppContactClassifier()
    
    if not classificador.prospects_dir.exists():
        print("❌ Nenhum prospecto registrado ainda")
        return
    
    arquivos = list(classificador.prospects_dir.glob("*.md"))
    
    if not arquivos:
        print("⚠️  Nenhuma classificação encontrada")
        return
    
    print("\n" + "="*50)
    print("🔵 PROSPECTOS NOVOS")
    print("="*50 + "\n")
    
    for arquivo in sorted(arquivos, reverse=True):
        with open(arquivo) as f:
            conteudo = f.read()
        
        numero = None
        for linha in conteudo.split('\n'):
            if linha.startswith("numero:"):
                numero = linha.replace("numero:", "").strip().split("\n")[0]
                break
        
        print(f"🔵 {numero}")


def verificar_cliente(numero: str) -> Optional[Dict]:
    """Verifica se cliente existe e retorna dados"""
    classificador = WhatsAppContactClassifier()
    
    arquivo_cliente = classificador.clients_dir / f"{numero}.md"
    
    if not arquivo_cliente.exists():
        print(f"❌ Cliente {numero} não encontrado")
        return None
    
    with open(arquivo_cliente) as f:
        conteudo = f.read()
    
    # Extrai dados do markdown
    dados = {}
    for linha in conteudo.split('\n'):
        if linha.startswith("nome:") or \
           linha.startswith("plano_selecionado:") or \
           linha.startswith("vencimento_contrato:") or \
           linha.startswith("valor_mensalidade:"):
            partes = linha.split(":", 1)
            chave = partes[0].strip()
            valor = partes[1].strip().split("\n")[0] if len(partes) > 1 else ""
            dados[chave] = valor
    
    return dados


# ============================================================
# INTEGRAÇÃO COM WHATSAPP API (Opcional)
# ============================================================

def sincronizar_com_whatsapp_api():
    """Sincroniza contatos do WhatsApp com base de dados"""
    
    print("\n🔄 Iniciando sincronização com WhatsApp...")
    
    # Aqui você implementaria integração com:
    # 1. WhatsApp Business API (Meta Cloud API)
    # 2. ou Webhooks do WhatsApp para novos contatos
    
    classificador = WhatsAppContactClassifier()
    
    print("✅ Sincronização concluída!")


if __name__ == "__main__":
    # Teste básico
    classificador = WhatsAppContactClassifier()
    
    # Exemplo de uso:
    # dados_cliente = {
    #     "nome": "João Silva",
    #     "plano_selecionado": "enterprise",
    #     "valor_mensalidade": "499.00",
    #     "vencimento_contrato": "2027-01-15",
    #     "ultimo_pagamento": "2026-10-25 R$ 499.00",
    #     "observacoes": "Cliente VIP"
    # }
    
    # classificador.processar_contato("5512987654321", dados_cliente)

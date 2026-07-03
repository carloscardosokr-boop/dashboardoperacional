#!/usr/bin/env python3
"""
Gerenciador de Dados do Dashboard Logístico
CLI para adicionar, alterar e deletar valores por unidade
"""

import json
import os
import subprocess
from datetime import datetime
from typing import Dict, List, Optional


def converter_para_float(valor_str: str) -> float:
    """Converte string para float, aceitando vírgula ou ponto como separador decimal"""
    if isinstance(valor_str, float):
        return valor_str
    # Substituir vírgula por ponto para conversão
    valor_str = valor_str.replace(',', '.').strip()
    try:
        return float(valor_str)
    except ValueError:
        print(f'❌ Valor inválido: {valor_str}')
        raise

# Arquivo de dados
DATA_FILE = 'data/dashboard-data.json'

# Filiais disponíveis
FILIAIS = {
    'ATM': 'ATM - Altamira',
    'APL': 'APL - Anápolis',
    'GYL': 'GYL - Goiânia',
    'PPY': 'PPY - Pouso Alegre',
    'APS': 'APS - Anápolis',
    'BSB': 'BSB - Brasília',
    'VIX': 'VIX - Serra',
    'DCX': 'DCX - Rio de Janeiro',
    'SPO': 'SPO - Guarulhos',
    'GYN': 'GYN - Goiânia'
}

# Meses disponíveis
MESES = [
    'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
    'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
]

# Tipos de dados
TIPOS = ['frete', 'peso', 'mercadoria', 'cte']


def carregar_dados() -> Dict:
    """Carrega os dados do arquivo JSON"""
    if not os.path.exists(DATA_FILE):
        # Criar estrutura inicial se não existir
        dados = {
            'dadosPorMes': {
                mes: {
                    'filiais': {sigla: {'frete': 0, 'peso': 0, 'mercadoria': 0, 'cte': 0}
                               for sigla in FILIAIS.keys()}
                }
                for mes in MESES
            },
            'ultima_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        salvar_dados(dados)
        return dados
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def salvar_dados(dados: Dict) -> None:
    """Salva os dados no arquivo JSON"""
    dados['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def listar_dados(dados: Dict, mes: Optional[str] = None, filial: Optional[str] = None) -> None:
    """Lista os dados de um mês/filial específico ou todos"""
    print('\n' + '='*80)
    print('DADOS DO DASHBOARD'.center(80))
    print('='*80)
    
    meses_para_mostrar = [mes] if mes else MESES
    
    for mes_atual in meses_para_mostrar:
        if mes_atual not in dados['dadosPorMes']:
            print(f'\nMês {mes_atual} não encontrado.')
            continue
        
        print(f'\n📅 Mês: {mes_atual}')
        print('-'*80)
        
        for sigla, nome in FILIAIS.items():
            if filial and filial != sigla:
                continue
            
            dados_filial = dados['dadosPorMes'][mes_atual]['filiais'][sigla]
            print(f'\n{nome} ({sigla}):')
            print(f'  CT-e:   {dados_filial["cte"]:,.0f}')
            print(f'  Frete:  R$ {dados_filial["frete"]:,.2f}')
            print(f'  Peso:   {dados_filial["peso"]:,.2f} kg')
            print(f'  Merc.:  R$ {dados_filial["mercadoria"]:,.2f}')


def adicionar_valor(dados: Dict, mes: str, filial: str, tipo: str, valor: float) -> Dict:
    """Adiciona um valor a uma filial em um mês específico"""
    if mes not in dados['dadosPorMes']:
        print(f'❌ Mês {mes} não encontrado.')
        return dados
    
    if filial not in FILIAIS:
        print(f'❌ Filial {filial} não encontrada.')
        return dados
    
    if tipo not in TIPOS:
        print(f'❌ Tipo {tipo} não encontrado. Tipos disponíveis: {", ".join(TIPOS)}')
        return dados
    
    dados['dadosPorMes'][mes]['filiais'][filial][tipo] += valor
    print(f'✅ Adicionado {tipo}: {valor} à filial {filial} no mês {mes}')
    
    return dados


def adicionar_registro_completo(dados: Dict, mes: str, filial: str, cte: float, frete: float, peso: float, mercadoria: float) -> Dict:
    """Adiciona todos os valores (CT-e, Frete, Peso, Mercadoria) a uma filial em um mês específico"""
    if mes not in dados['dadosPorMes']:
        print(f'❌ Mês {mes} não encontrado.')
        return dados
    
    if filial not in FILIAIS:
        print(f'❌ Filial {filial} não encontrada.')
        return dados
    
    dados['dadosPorMes'][mes]['filiais'][filial]['cte'] += cte
    dados['dadosPorMes'][mes]['filiais'][filial]['frete'] += frete
    dados['dadosPorMes'][mes]['filiais'][filial]['peso'] += peso
    dados['dadosPorMes'][mes]['filiais'][filial]['mercadoria'] += mercadoria
    
    print(f'✅ Adicionado registro completo à filial {filial} no mês {mes}:')
    print(f'   CT-e: {cte}')
    print(f'   Frete: R$ {frete}')
    print(f'   Peso: {peso} kg')
    print(f'   Mercadoria: R$ {mercadoria}')
    
    return dados


def alterar_valor(dados: Dict, mes: str, filial: str, tipo: str, valor: float) -> Dict:
    """Altera o valor de uma filial em um mês específico"""
    if mes not in dados['dadosPorMes']:
        print(f'❌ Mês {mes} não encontrado.')
        return dados
    
    if filial not in FILIAIS:
        print(f'❌ Filial {filial} não encontrada.')
        return dados
    
    if tipo not in TIPOS:
        print(f'❌ Tipo {tipo} não encontrado. Tipos disponíveis: {", ".join(TIPOS)}')
        return dados
    
    dados['dadosPorMes'][mes]['filiais'][filial][tipo] = valor
    print(f'✅ Alterado {tipo} para {valor} na filial {filial} no mês {mes}')
    
    return dados


def deletar_valor(dados: Dict, mes: str, filial: str, tipo: str) -> Dict:
    """Deleta (zera) o valor de uma filial em um mês específico"""
    if mes not in dados['dadosPorMes']:
        print(f'❌ Mês {mes} não encontrado.')
        return dados
    
    if filial not in FILIAIS:
        print(f'❌ Filial {filial} não encontrada.')
        return dados
    
    if tipo not in TIPOS:
        print(f'❌ Tipo {tipo} não encontrado. Tipos disponíveis: {", ".join(TIPOS)}')
        return dados
    
    dados['dadosPorMes'][mes]['filiais'][filial][tipo] = 0
    print(f'✅ Deletado {tipo} da filial {filial} no mês {mes}')
    
    return dados


def fazer_commit_push() -> bool:
    """Faz git add, commit e push"""
    try:
        print('\n🔄 Fazendo git add...')
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        
        print('🔄 Fazendo git commit...')
        mensagem = f"atualização diaria de valores - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', mensagem], check=True, capture_output=True)
        
        print('🔄 Fazendo git push...')
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        
        print('✅ Commit e push realizados com sucesso!')
        return True
    except subprocess.CalledProcessError as e:
        print(f'❌ Erro ao fazer commit/push: {e}')
        return False


def menu_principal():
    """Menu principal do CLI"""
    dados = carregar_dados()
    
    while True:
        print('\n' + '='*80)
        print('GERENCIADOR DE DADOS DO DASHBOARD'.center(80))
        print('='*80)
        print('\n1. Listar dados')
        print('2. Adicionar valor individual')
        print('3. Adicionar registro completo (CT-e, Frete, Peso, Mercadoria)')
        print('4. Alterar valor')
        print('5. Deletar valor')
        print('6. Fazer commit e push para o GitHub')
        print('7. Sair')
        
        opcao = input('\nEscolha uma opção (1-7): ').strip()
        
        if opcao == '1':
            # Listar dados
            print('\nFiltros:')
            mes = input('Mês (deixe em branco para todos): ').strip().upper()
            filial = input('Filial (deixe em branco para todas): ').strip().upper()
            listar_dados(dados, mes if mes else None, filial if filial else None)
        
        elif opcao == '2':
            # Adicionar valor individual
            print('\nAdicionar valor individual')
            mes = input(f'Mês ({", ".join(MESES[:6])}...): ').strip().upper()
            filial = input(f'Filial ({", ".join(list(FILIAIS.keys())[:5])}...): ').strip().upper()
            tipo = input(f'Tipo ({", ".join(TIPOS)}): ').strip().lower()
            valor = converter_para_float(input('Valor a adicionar: '))
            dados = adicionar_valor(dados, mes, filial, tipo, valor)
            salvar_dados(dados)
        
        elif opcao == '3':
            # Adicionar registro completo
            print('\nAdicionar registro completo')
            mes = input(f'Mês ({", ".join(MESES[:6])}...): ').strip().upper()
            filial = input(f'Filial ({", ".join(list(FILIAIS.keys())[:5])}...): ').strip().upper()
            cte = converter_para_float(input('CT-e: '))
            frete = converter_para_float(input('Frete (R$): '))
            peso = converter_para_float(input('Peso (kg): '))
            mercadoria = converter_para_float(input('Mercadoria (R$): '))
            dados = adicionar_registro_completo(dados, mes, filial, cte, frete, peso, mercadoria)
            salvar_dados(dados)
        
        elif opcao == '4':
            # Alterar valor
            print('\nAlterar valor')
            mes = input(f'Mês ({", ".join(MESES[:6])}...): ').strip().upper()
            filial = input(f'Filial ({", ".join(list(FILIAIS.keys())[:5])}...): ').strip().upper()
            tipo = input(f'Tipo ({", ".join(TIPOS)}): ').strip().lower()
            valor = converter_para_float(input('Novo valor: '))
            dados = alterar_valor(dados, mes, filial, tipo, valor)
            salvar_dados(dados)
        
        elif opcao == '5':
            # Deletar valor
            print('\nDeletar valor (zerar)')
            mes = input(f'Mês ({", ".join(MESES[:6])}...): ').strip().upper()
            filial = input(f'Filial ({", ".join(list(FILIAIS.keys())[:5])}...): ').strip().upper()
            tipo = input(f'Tipo ({", ".join(TIPOS)}): ').strip().lower()
            dados = deletar_valor(dados, mes, filial, tipo)
            salvar_dados(dados)
        
        elif opcao == '6':
            # Commit e push
            fazer_commit_push()
        
        elif opcao == '7':
            print('\n👋 Saindo...')
            break
        
        else:
            print('\n❌ Opção inválida. Tente novamente.')


if __name__ == '__main__':
    menu_principal()

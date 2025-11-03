import json
import os
import glob
from collections import defaultdict
import pandas as pd
import requests
from datetime import datetime

# Constantes
CLAN_TAG = '#9PJRJRPC'
API_KEY_ENV_VAR = 'CLASH_ROYALE_API_KEY'

def get_active_clan_members(api_key):
    """
    Busca a lista de membros ativos do clã diretamente da API do Clash Royale.
    Retorna um dicionário mapeando a tag do jogador para seu nome.
    """
    print("Buscando lista de membros ativos do clã...")

    # A URL da API precisa ter o '#' da tag codificado como '%23'
    url = f"https://api.clashroyale.com/v1/clans/%23{CLAN_TAG[1:]}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança um erro para respostas com código de status ruim (4xx ou 5xx)
        clan_data = response.json()

        member_list = clan_data.get('memberList', [])
        if not member_list:
            print("A lista de membros retornada pela API está vazia.")
            return {}

        active_members = {member['tag']: member['name'] for member in member_list}
        print(f"Encontrado {len(active_members)} membros ativos.")
        return active_members

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do clã da API: {e}")
        # Em caso de erro de API, retorna um dicionário vazio para não quebrar o resto do script
        return {}

def process_war_log():
    """
    Processa o arquivo de log de guerra, analisa a participação dos membros ativos
    e gera um relatório em Excel com resumo e histórico detalhado.
    """
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        print(f"Erro: A variável de ambiente '{API_KEY_ENV_VAR}' não foi definida.")
        print("Por favor, configure a chave da API para buscar os membros ativos.")
        return

    # Busca a lista de membros ativos primeiro
    active_members = get_active_clan_members(api_key)
    if not active_members:
        print("Não foi possível obter a lista de membros ativos. O relatório não será gerado.")
        return

    print("Iniciando o processamento dos dados de guerra...")

    # Encontra o arquivo de log mais recente de forma robusta
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, 'data')
        list_of_files = glob.glob(os.path.join(data_dir, 'war_log_full_*.json'))
        if not list_of_files:
            print(f"Nenhum arquivo de log de guerra encontrado no diretório: '{data_dir}'")
            return
        latest_file = max(list_of_files, key=os.path.getctime)
        print(f"Processando o arquivo: {os.path.basename(latest_file)}")
    except Exception as e:
        print(f"Erro ao encontrar o arquivo de log: {e}")
        return

    # Carrega os dados do arquivo JSON
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro ao ler ou decodificar o arquivo JSON: {e}")
        return

    all_wars = data.get('items', [])
    if not all_wars:
        print("Arquivo de log não contém dados de guerras ('items').")
        return

    # Estruturas para armazenar dados do relatório
    player_participation_summary = defaultdict(int)
    player_participation_history = defaultdict(lambda: ['-'] * 5) # Lista com 5 posições, default '-'

    wars_to_process = all_wars[:5]
    if len(wars_to_process) < 5:
        print(f"Aviso: Encontrado apenas {len(wars_to_process)} guerras no log para processar.")

    for i, war in enumerate(wars_to_process):
        our_clan_data = None
        for standing in war.get('standings', []):
            clan_info = standing.get('clan')
            if clan_info and clan_info.get('tag') == CLAN_TAG:
                our_clan_data = clan_info
                break

        if our_clan_data:
            for participant in our_clan_data.get('participants', []):
                player_tag = participant.get('tag')

                # Processa apenas se o jogador estiver na lista de membros ativos
                if player_tag in active_members:
                    decks_used = participant.get('decksUsed', 0)
                    player_participation_history[player_tag][i] = decks_used

                    if decks_used > 0:
                        player_participation_summary[player_tag] += 1

    # Prepara dados para as abas do Excel
    summary_data = []
    history_data = []

    for tag, name in active_members.items():
        participations = player_participation_summary.get(tag, 0)
        status = 'NOVATO' if participations == 1 else ''

        summary_data.append({
            'Nome': name,
            'Participações (últimas 5)': participations,
            'Status': status
        })

        history_row = {'Nome': name}
        col_names = ['Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5']
        for i, col_name in enumerate(col_names):
            history_row[col_name] = player_participation_history[tag][i]
        history_data.append(history_row)

    if not summary_data:
        print("Nenhum dado de membro ativo foi encontrado nas guerras processadas.")
        return

    # Ordena os dados de resumo por menor participação
    summary_data.sort(key=lambda x: x['Participações (últimas 5)'])

    # Cria o DataFrame e salva em Excel com duas abas
    try:
        df_summary = pd.DataFrame(summary_data)
        df_history = pd.DataFrame(history_data)

        output_path = os.path.join(project_root, 'relatorio_participacao_guerra.xlsx')

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_summary.to_excel(writer, index=False, sheet_name='Resumo')
            df_history.to_excel(writer, index=False, sheet_name='Historico')

        print(f"Relatório '{os.path.basename(output_path)}' gerado com sucesso em: {project_root}")
        print("O relatório contém as abas 'Resumo' e 'Historico'.")

    except Exception as e:
        print(f"Erro ao gerar o arquivo Excel: {e}")


if __name__ == '__main__':
    process_war_log()

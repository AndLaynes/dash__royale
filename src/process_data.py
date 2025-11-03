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
        response.raise_for_status()
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
        return {}

def calculate_player_status(decks_last_war, decks_war_minus_2):
    """
    Calcula o status de um jogador com base no número de decks usados nas duas últimas guerras.
    """
    # Garante que os valores sejam numéricos para comparação
    try:
        decks1 = int(decks_last_war)
        decks2 = int(decks_war_minus_2)
    except (ValueError, TypeError):
        # Se algum valor não for um número (ex: '-'), considera como "Verificar"
        return 'Verificar'

    if decks1 <= 11 or decks2 <= 11:
        return 'Verificar'

    if decks1 >= 16 and decks2 >= 16:
        return 'Campeão'

    return 'Ok'

def process_war_log():
    """
    Processa o log de guerra, analisa a participação dos membros ativos e gera um
    relatório em Excel com o histórico detalhado e o status do jogador.
    """
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        print(f"Erro: A variável de ambiente '{API_KEY_ENV_VAR}' não foi definida.")
        return

    active_members = get_active_clan_members(api_key)
    if not active_members:
        print("Não foi possível obter a lista de membros ativos. O relatório não será gerado.")
        return

    print("Iniciando o processamento dos dados de guerra...")

    # Encontra o arquivo de log mais recente
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

    player_participation_history = defaultdict(lambda: ['-'] * 5)
    wars_to_process = all_wars[:5]
    if len(wars_to_process) < 5:
        print(f"Aviso: Encontrado apenas {len(wars_to_process)} guerras no log para processar.")

    for i, war in enumerate(wars_to_process):
        our_clan_data = next((s['clan'] for s in war.get('standings', []) if s.get('clan', {}).get('tag') == CLAN_TAG), None)

        if our_clan_data:
            for participant in our_clan_data.get('participants', []):
                player_tag = participant.get('tag')
                if player_tag in active_members:
                    decks_used = participant.get('decksUsed', 0)
                    player_participation_history[player_tag][i] = decks_used

    # Prepara os dados para o relatório
    history_data = []
    for tag, name in active_members.items():
        decks_history = player_participation_history[tag]

        # Pega os decks das duas últimas guerras para o cálculo do status
        decks_last_war = decks_history[0] if len(decks_history) > 0 else '-'
        decks_war_minus_2 = decks_history[1] if len(decks_history) > 1 else '-'

        status = calculate_player_status(decks_last_war, decks_war_minus_2)

        history_row = {
            'Nome': name,
            'Player Status': status,
            'Última Guerra': decks_last_war,
            'Guerra -2': decks_war_minus_2,
            'Guerra -3': decks_history[2] if len(decks_history) > 2 else '-',
            'Guerra -4': decks_history[3] if len(decks_history) > 3 else '-',
            'Guerra -5': decks_history[4] if len(decks_history) > 4 else '-'
        }
        history_data.append(history_row)

    if not history_data:
        print("Nenhum dado de membro ativo foi encontrado nas guerras processadas.")
        return

    # Cria o DataFrame e salva em Excel
    try:
        df_history = pd.DataFrame(history_data)

        output_path = os.path.join(project_root, 'relatorio_participacao_guerra.xlsx')

        df_history.to_excel(output_path, index=False, sheet_name='Historico_Guerra')

        print(f"Relatório '{os.path.basename(output_path)}' gerado com sucesso em: {project_root}")

    except Exception as e:
        print(f"Erro ao gerar o arquivo Excel: {e}")


if __name__ == '__main__':
    process_war_log()

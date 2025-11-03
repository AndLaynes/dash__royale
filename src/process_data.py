import json
import os
import glob
from collections import defaultdict
import pandas as pd
from datetime import datetime

# Constante para a tag do clã
CLAN_TAG = '#9PJRJRPC'

def process_war_log():
    """
    Processa o arquivo de log de guerra mais recente, analisa a participação
    dos membros nas últimas 5 guerras e gera um relatório em Excel.
    """
    print("Iniciando o processamento dos dados de guerra...")

    # Encontra o arquivo de log mais recente de forma robusta
    try:
        # Constrói o caminho absoluto para a pasta 'data' a partir da localização do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, 'data')

        list_of_files = glob.glob(os.path.join(data_dir, 'war_log_full_*.json'))
        if not list_of_files:
            # Mensagem de erro melhorada para depuração
            print(f"Nenhum arquivo de log de guerra encontrado no diretório: '{data_dir}'")
            print("Verifique se a pasta 'data' está na raiz do projeto (no mesmo nível da pasta 'src') e se o arquivo de log existe.")
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

    # Dicionário para contar a participação de cada jogador
    player_participation = defaultdict(int)
    # Dicionário para mapear tag para o nome mais recente do jogador
    player_names = {}

    # Analisa as últimas 5 guerras
    wars_to_process = all_wars[:5]

    if len(wars_to_process) < 5:
        print(f"Aviso: Encontrado apenas {len(wars_to_process)} guerras no log para processar.")


    for war in wars_to_process:
        # Encontra o nosso clã nos standings da guerra
        our_clan_data = None
        for standing in war.get('standings', []):
            clan_info = standing.get('clan')
            if clan_info and clan_info.get('tag') == CLAN_TAG:
                our_clan_data = clan_info
                break

        if our_clan_data:
            for participant in our_clan_data.get('participants', []):
                player_tag = participant.get('tag')
                player_name = participant.get('name')

                # Armazena o nome mais recente do jogador
                if player_tag not in player_names:
                    player_names[player_tag] = player_name

                # Conta a participação se usou decks
                if participant.get('decksUsed', 0) > 0:
                    player_participation[player_tag] += 1

    # Prepara os dados para o relatório, focando apenas nos membros atuais
    report_data = []

    # Consideramos "membros atuais" todos que apareceram na guerra mais recente
    if not all_wars:
        print("Não há guerras no log para determinar os membros atuais.")
        return

    most_recent_war = all_wars[0]
    current_members = set()
    for standing in most_recent_war.get('standings', []):
        clan_info = standing.get('clan')
        if clan_info and clan_info.get('tag') == CLAN_TAG:
            for participant in clan_info.get('participants', []):
                current_members.add(participant.get('tag'))

    if not current_members:
        print("Não foi possível encontrar os dados do clã na guerra mais recente para gerar o relatório.")
        return

    for tag in current_members:
        participations = player_participation.get(tag, 0)
        # Define o status "NOVATO" para quem participou de apenas 1 das últimas 5 guerras
        status = 'NOVATO' if participations == 1 else ''

        report_data.append({
            'Nome': player_names.get(tag, tag),
            'Participações (últimas 5)': participations,
            'Status': status
        })

    if not report_data:
        print("Nenhum dado de participante do clã foi encontrado para gerar o relatório.")
        return

    # Ordena os dados por menor número de participações
    report_data.sort(key=lambda x: x['Participações (últimas 5)'])

    # Cria o DataFrame e salva em Excel
    try:
        df = pd.DataFrame(report_data)
        # Constrói o caminho para o arquivo de saída na pasta raiz do projeto
        output_path = os.path.join(project_root, 'relatorio_participacao_guerra.xlsx')
        df.to_excel(output_path, index=False, sheet_name='ParticipacaoGuerra')
        print(f"Relatório '{os.path.basename(output_path)}' gerado com sucesso em: {project_root}")
        print("O relatório está ordenado por jogadores com menor participação nas últimas 5 guerras.")

    except Exception as e:
        print(f"Erro ao gerar o arquivo Excel: {e}")


if __name__ == '__main__':
    process_war_log()

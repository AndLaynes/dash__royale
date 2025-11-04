import json
import pandas as pd
from datetime import datetime
import os
import sys

# Lista para armazenar mensagens de log
log_messages = []

def log_and_print(message):
    """Adiciona a mensagem a uma lista de logs e também a imprime no console."""
    log_messages.append(message)
    print(message)

# Define os caminhos de forma robusta
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')

def load_json_file(file_path):
    """Carrega um arquivo JSON, tratando erros e registrando logs."""
    if not os.path.exists(file_path):
        log_and_print(f"Diagnóstico: Arquivo '{os.path.basename(file_path)}' não encontrado.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log_and_print(f"Erro Crítico: Falha ao ler ou decodificar o arquivo '{os.path.basename(file_path)}'.")
        log_and_print(f"Detalhes: {e}")
        with open(os.path.join(data_dir, 'process_log.json'), 'w', encoding='utf-8') as f:
            json.dump(log_messages, f, ensure_ascii=False, indent=4)
        sys.exit(1)

def get_war_history_data():
    """Processa o histórico de guerras para extrair a participação de cada jogador."""
    history_file_path = os.path.join(data_dir, 'riverracelog.json')
    log_and_print(f"Analisando dados do histórico de guerras (`{os.path.basename(history_file_path)}`)...")

    warlog_data = load_json_file(history_file_path)
    if not warlog_data or not warlog_data.get('items'):
        log_and_print("-> Info: Histórico de guerras não encontrado ou vazio.")
        return {}

    items = warlog_data['items']
    log_and_print(f"-> Encontrados {len(items)} registros de guerra no histórico.")

    war_history = {}
    war_dates_found = set()
    clan_tag_env = os.environ.get('CLAN_TAG')
    if not clan_tag_env:
        log_and_print("-> Erro Crítico: A variável de ambiente CLAN_TAG não está definida.")
        return {}

    normalized_clan_tag_env = clan_tag_env.lstrip('#')
    log_and_print(f"-> Buscando pelo CLAN_TAG (normalizado): '{normalized_clan_tag_env}' no histórico...")

    for i, war in enumerate(items):
        try:
            # A API do riverracelog usa 'createdDate', que marca o início da semana da guerra.
            finish_time_str = war.get('createdDate')
            if not finish_time_str:
                log_and_print(f"-> Alerta: Registro de guerra de índice {i} não tem 'createdDate'. Pulando.")
                continue
            war_date = datetime.strptime(finish_time_str, '%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%d')
            war_dates_found.add(war_date)
        except (ValueError, TypeError) as e:
            log_and_print(f"-> Alerta: Formato de data inválido para a guerra de índice {i} ('{finish_time_str}'). Detalhes: {e}. Pulando.")
            continue

        standings = war.get('standings')
        if not standings:
            log_and_print(f"-> Info: A guerra de {war_date} não contém 'standings'.")
            continue

        normalized_clan_tag_env = clan_tag_env.lstrip('#')

        for standing in standings:
            clan_info = standing.get('clan', {})
            clan_tag_from_data = clan_info.get('tag', '')

            if clan_tag_from_data.lstrip('#') == normalized_clan_tag_env:
                participants = standing.get('participants', [])
                for participant in participants:
                    tag = participant.get('tag')
                    if not tag:
                        continue

                    if tag not in war_history:
                        war_history[tag] = {}

                    decks_used = participant.get('decksUsed', 0)
                    war_history[tag][war_date] = decks_used
                break

    log_and_print(f"-> Processados dados históricos de {len(war_history)} jogadores únicos de {len(war_dates_found)} guerras.")
    return war_history

def generate_report():
    """
    Gera o relatório de participação em guerras com diagnósticos detalhados.
    """
    global log_messages
    log_messages = []

    log_and_print("Iniciando processamento de dados...")

    participants = []
    data_source = ""

    # Etapa 1: Tenta obter dados da guerra atual
    log_and_print("Verificando dados da guerra atual (`current_war.json`)...")
    current_war_data = load_json_file(os.path.join(data_dir, 'current_war.json'))
    if current_war_data and current_war_data.get('state') != 'notInWar':
        participants = current_war_data.get('clan', {}).get('participants', [])
        if participants:
            log_and_print(f"-> Sucesso: {len(participants)} participantes encontrados na guerra atual.")
            data_source = "Guerra Atual"
        else:
            log_and_print("-> Info: Clã está em guerra, mas não há lista de participantes. Buscando no histórico.")
    else:
        log_and_print("-> Info: Clã não está em guerra (`notInWar`) ou arquivo não encontrado. Buscando no histórico.")

    # Etapa 2: Se não houver guerra atual, busca a última guerra VÁLIDA no histórico
    if not participants:
        history_file_path = os.path.join(data_dir, 'riverracelog.json')
        log_and_print(f"Verificando `{os.path.basename(history_file_path)}` para definir a lista de membros do clã...")
        warlog_data = load_json_file(history_file_path)

        if warlog_data and warlog_data.get('items'):
            clan_tag_env = os.environ.get('CLAN_TAG')
            if not clan_tag_env:
                log_and_print("-> Erro Crítico: A variável de ambiente CLAN_TAG não está definida.")
            else:
                normalized_clan_tag_env = clan_tag_env.lstrip('#')
                latest_war = warlog_data['items'][0]
                participants = []
                for standing in latest_war.get('standings', []):
                    clan_info = standing.get('clan', {})
                    clan_tag_from_data = clan_info.get('tag', '')
                    if clan_tag_from_data.lstrip('#') == normalized_clan_tag_env:
                        participants = standing.get('participants', [])
                        break

                if participants:
                    war_date = datetime.strptime(latest_war['createdDate'], '%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%d')
                    log_and_print(f"-> Sucesso: Usando a guerra de {war_date} com {len(participants)} participantes como base para a lista de membros.")
                    data_source = f"Histórico ({war_date})"
                else:
                    log_and_print("-> Alerta: O clã não foi encontrado na guerra mais recente do histórico.")
        else:
            log_and_print("-> Alerta: Histórico de guerras não encontrado ou vazio.")

    # Etapa 3: Gera o relatório
    if not participants:
        log_and_print("\nConclusão: Nenhuma fonte de dados com participantes encontrada. O relatório de jogadores estará vazio.")
        df = pd.DataFrame(columns=['Nome', 'Player Status', 'Fonte de Dados', 'Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5'])
    else:
        log_and_print(f"Gerando relatório para {len(participants)} jogadores com base em: '{data_source}'.")
        clan_members = {p['tag']: p['name'] for p in participants}
        df = pd.DataFrame(list(clan_members.items()), columns=['Tag', 'Nome'])
        df['Fonte de Dados'] = data_source

        war_history = get_war_history_data()
        all_war_dates = sorted({date for history in war_history.values() for date in history}, reverse=True)
        log_and_print(f"-> Encontradas {len(all_war_dates)} datas de guerras únicas no histórico.")

        unique_war_dates = all_war_dates[:5]
        log_and_print(f"-> Usando as 5 datas mais recentes para o relatório: {unique_war_dates}")

        for i in range(5):
            col_name = f'Guerra -{i+1}' if i > 0 else 'Última Guerra'
            war_date = unique_war_dates[i] if i < len(unique_war_dates) else None
            if war_date:
                df[col_name] = df['Tag'].apply(lambda tag: war_history.get(tag, {}).get(war_date, '-'))
            else:
                df[col_name] = '-'

        def get_player_status(row):
            last_war_decks = pd.to_numeric(row['Última Guerra'], errors='coerce')
            war_minus_2_decks = pd.to_numeric(row.get('Guerra -2'), errors='coerce')
            last_war_decks = 0 if pd.isna(last_war_decks) else last_war_decks
            war_minus_2_decks = 0 if pd.isna(war_minus_2_decks) else war_minus_2_decks
            if last_war_decks >= 16 and war_minus_2_decks >= 16:
                return 'Campeão'
            elif last_war_decks >= 12 and war_minus_2_decks >= 12:
                return 'Ok'
            else:
                return 'Verificar'

        df['Player Status'] = df.apply(get_player_status, axis=1)
        df = df[['Nome', 'Player Status', 'Fonte de Dados', 'Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5']]

    output_path = os.path.join(data_dir, 'relatorio_participacao_guerra.xlsx')
    df.to_excel(output_path, index=False)
    log_and_print(f"Relatório salvo com sucesso em '{os.path.basename(output_path)}'.")

    log_output_path = os.path.join(data_dir, 'process_log.json')
    with open(log_output_path, 'w', encoding='utf-8') as f:
        json.dump(log_messages, f, ensure_ascii=False, indent=4)
    print(f"Logs de diagnóstico salvos em '{os.path.basename(log_output_path)}'.")

if __name__ == "__main__":
    generate_report()

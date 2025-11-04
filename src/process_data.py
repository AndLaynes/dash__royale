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
        # Salva os logs antes de sair para que o erro seja visível no dashboard
        with open(os.path.join(data_dir, 'process_log.json'), 'w', encoding='utf-8') as f:
            json.dump(log_messages, f, ensure_ascii=False, indent=4)
        sys.exit(1)

def get_war_history_data():
    """Processa o histórico de guerras para extrair a participação de cada jogador."""
    warlog_data = load_json_file(os.path.join(data_dir, 'warlog.json'))
    if not warlog_data or not warlog_data.get('items'):
        return {}

    war_history = {}
    for war in warlog_data['items']:
        war_date = datetime.strptime(war['createdDate'], '%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%d')
        for participant in war.get('participants', []):
            tag = participant['tag']
            if tag not in war_history:
                war_history[tag] = {}
            war_history[tag][war_date] = participant.get('cardsUsed', 0)
    return war_history

def generate_report():
    """
    Gera o relatório de participação em guerras com diagnósticos detalhados
    e salva os logs em um arquivo JSON.
    """
    global log_messages
    log_messages = [] # Limpa os logs para a execução atual

    log_and_print("Iniciando processamento de dados...")

    participants = []
    data_source = ""

    # Etapa 1: Tenta obter dados da guerra atual
    log_and_print("Verificando dados da guerra atual...")
    current_war_data = load_json_file(os.path.join(data_dir, 'current_war.json'))
    if current_war_data:
        participants = current_war_data.get('clan', {}).get('participants', [])
        if participants:
            log_and_print(f"-> Sucesso: {len(participants)} participantes encontrados na guerra atual.")
            data_source = "Guerra Atual"
        else:
            log_and_print("-> Info: Nenhum participante na guerra atual. Buscando no histórico.")
    else:
        log_and_print("-> Info: Dados da guerra atual não disponíveis. Buscando no histórico.")

    # Etapa 2: Se não houver guerra atual, busca a última guerra VÁLIDA no histórico
    if not participants:
        log_and_print("Verificando histórico de guerras...")
        warlog_data = load_json_file(os.path.join(data_dir, 'warlog.json'))
        if warlog_data and warlog_data.get('items'):
            for i, war in enumerate(warlog_data['items']):
                participants = war.get('participants', [])
                if participants:
                    war_date = datetime.strptime(war['createdDate'], '%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%d')
                    log_and_print(f"-> Sucesso: Encontrada guerra válida na posição {i} do histórico (Data: {war_date}) com {len(participants)} participantes.")
                    data_source = f"Histórico ({war_date})"
                    break
            if not participants:
                log_and_print("-> Alerta: Nenhuma guerra com participantes foi encontrada no histórico.")
        else:
            log_and_print("-> Alerta: Histórico de guerras não encontrado ou vazio.")

    # Etapa 3: Gera o relatório
    if not participants:
        log_and_print("\nConclusão: Nenhuma fonte de dados com participantes encontrada. O relatório de jogadores estará vazio.")
        df = pd.DataFrame(columns=['Nome', 'Player Status', 'Fonte de Dados', 'Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5'])
    else:
        log_and_print(f"Gerando relatório com base em: '{data_source}'.")
        clan_members = {p['tag']: p['name'] for p in participants}
        df = pd.DataFrame(list(clan_members.items()), columns=['Tag', 'Nome'])
        df['Fonte de Dados'] = data_source

        war_history = get_war_history_data()
        all_war_dates = sorted([date for history in war_history.values() for date in history], reverse=True)
        unique_war_dates = sorted(list(set(all_war_dates)), reverse=True)

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

    # Salva os logs em um arquivo JSON
    log_output_path = os.path.join(data_dir, 'process_log.json')
    try:
        with open(log_output_path, 'w', encoding='utf-8') as f:
            json.dump(log_messages, f, ensure_ascii=False, indent=4)
        print(f"Logs de diagnóstico salvos em '{os.path.basename(log_output_path)}'.")
    except IOError as e:
        print(f"Erro Crítico: Não foi possível salvar o arquivo de log em '{log_output_path}'.")
        print(f"Detalhes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_report()

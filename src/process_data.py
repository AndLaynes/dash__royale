import json
import pandas as pd
from datetime import datetime
import os

# O diretório do projeto é o pai do diretório 'src'
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')

def get_clan_members():
    """Obtém a lista de membros do clã a partir dos dados da guerra atual."""
    file_path = os.path.join(data_dir, 'current_war.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    members = {}
    for participant in data.get('participants', []):
        members[participant['tag']] = participant['name']
    return members

def get_war_history():
    """Processa o histórico de guerras para extrair a participação de cada jogador."""
    file_path = os.path.join(data_dir, 'warlog.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    war_history = {}
    for war in data.get('items', []):
        war_date = datetime.strptime(war['createdDate'], '%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%d')
        for participant in war.get('participants', []):
            tag = participant['tag']
            if tag not in war_history:
                war_history[tag] = {}
            war_history[tag][war_date] = participant.get('cardsUsed', 0)
    return war_history

def generate_report():
    """Gera o relatório de participação em guerras."""
    clan_members = get_clan_members()
    war_history = get_war_history()

    # Obter todas as datas de guerra e ordená-las
    all_war_dates = sorted(list(set(date for history in war_history.values() for date in history)), reverse=True)

    # Criar um DataFrame com os membros do clã
    df = pd.DataFrame(list(clan_members.items()), columns=['Tag', 'Nome'])

    # Coletar dados das últimas 5 guerras
    for i in range(5):
        col_name = f'Guerra -{i+1}' if i > 0 else 'Última Guerra'
        war_date = all_war_dates[i] if i < len(all_war_dates) else None

        if war_date:
            df[col_name] = df['Tag'].apply(lambda tag: war_history.get(tag, {}).get(war_date, '-'))
        else:
            df[col_name] = '-'

    # Calcular o "Player Status"
    def get_player_status(row):
        last_war_decks = row['Última Guerra'] if row['Última Guerra'] != '-' else 0
        war_minus_2_decks = row.get('Guerra -2', '-')
        war_minus_2_decks = war_minus_2_decks if war_minus_2_decks != '-' else 0

        if last_war_decks >= 16 and war_minus_2_decks >= 16:
            return 'Campeão'
        elif last_war_decks >= 12 and war_minus_2_decks >= 12:
            return 'Ok'
        else:
            return 'Verificar'

    df['Player Status'] = df.apply(get_player_status, axis=1)

    # Reordenar as colunas
    df = df[['Nome', 'Player Status', 'Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5']]

    # Salvar o relatório em Excel
    output_path = os.path.join(data_dir, 'relatorio_participacao_guerra.xlsx')
    df.to_excel(output_path, index=False)
    print(f"Relatório gerado com sucesso em '{output_path}'.")

if __name__ == "__main__":
    api_key = os.getenv('CLASH_ROYALE_API_KEY')
    if not api_key:
        print("Erro: A variável de ambiente 'CLASH_ROYALE_API_KEY' não foi definida.")
    else:
        generate_report()

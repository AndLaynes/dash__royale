import json
import pandas as pd
from datetime import datetime
import os

# Define o diretório de dados de forma robusta
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')

def get_war_history():
    """Processa o histórico de guerras para extrair a participação de cada jogador."""
    file_path = os.path.join(data_dir, 'warlog.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

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
    """
    Gera o relatório de participação em guerras.
    Se uma guerra estiver ativa, usa os dados dela.
    Caso contrário, usa os dados da última guerra registrada no histórico.
    """

    participants = []
    data_source = ""

    try:
        current_war_path = os.path.join(data_dir, 'current_war.json')
        with open(current_war_path, 'r', encoding='utf-8') as f:
            current_war_data = json.load(f)
        participants = current_war_data.get('participants', [])
        if participants:
            print(f"Diagnóstico: Encontrados {len(participants)} participantes na guerra atual.")
            data_source = "Guerra Atual"
        else:
            print("Diagnóstico: Nenhum participante na guerra atual. Verificando histórico.")
            participants = []
    except (FileNotFoundError, json.JSONDecodeError):
        print("Diagnóstico: Arquivo 'current_war.json' não encontrado ou inválido. Verificando histórico.")
        participants = []

    if not participants:
        try:
            warlog_path = os.path.join(data_dir, 'warlog.json')
            with open(warlog_path, 'r', encoding='utf-8') as f:
                warlog_data = json.load(f)
            warlog_items = warlog_data.get('items', [])
            if warlog_items:
                last_war = warlog_items[0]
                participants = last_war.get('participants', [])
                if participants:
                    print(f"Diagnóstico: Usando dados da última guerra do histórico com {len(participants)} participantes.")
                    data_source = "Última Guerra"
                else:
                    print("Diagnóstico: A última guerra no histórico não tem participantes.")
            else:
                print("Diagnóstico: Histórico de guerras está vazio.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Diagnóstico: Arquivo de histórico de guerras não encontrado ou inválido.")

    if not participants:
        print("Diagnóstico: Nenhuma informação de participantes encontrada. Gerando relatório vazio.")
        df = pd.DataFrame(columns=['Nome', 'Player Status', 'Fonte de Dados', 'Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5'])
        output_path = os.path.join(data_dir, 'relatorio_participacao_guerra.xlsx')
        df.to_excel(output_path, index=False)
        print(f"Relatório vazio gerado em '{output_path}'.")
        return

    clan_members = {p['tag']: p['name'] for p in participants}
    df = pd.DataFrame(list(clan_members.items()), columns=['Tag', 'Nome'])
    df['Fonte de Dados'] = data_source

    war_history = get_war_history()
    all_war_dates = sorted(list(set(date for history in war_history.values() for date in history)), reverse=True)

    for i in range(5):
        col_name = f'Guerra -{i+1}' if i > 0 else 'Última Guerra'
        war_date = all_war_dates[i] if i < len(all_war_dates) else None
        if war_date:
            df[col_name] = df['Tag'].apply(lambda tag: war_history.get(tag, {}).get(war_date, '-'))
        else:
            df[col_name] = '-'

    def get_player_status(row):
        """Função corrigida para lidar com inteiros e valores ausentes."""
        # Converte para numérico, transformando erros (como '-') em NaN (Not a Number)
        last_war_decks = pd.to_numeric(row['Última Guerra'], errors='coerce')
        war_minus_2_decks = pd.to_numeric(row.get('Guerra -2'), errors='coerce')

        # Substitui NaN por 0 para os cálculos
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
    print(f"Relatório gerado com sucesso em '{output_path}'.")

if __name__ == "__main__":
    generate_report()

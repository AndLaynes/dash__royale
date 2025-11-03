import os
import json
import pandas as pd
from datetime import datetime

# --- Configuração ---
DATA_DIR = "data"
OUTPUT_CSV_FILE = "guerra_detalhada.csv"
OUTPUT_RANKING_FILE = "relatorio_de_guerra.xlsx"
CLAN_TAG = "#9PJRJRPC"
NUMERO_DE_GUERRAS_NO_RELATORIO = 5

# --- Funções Auxiliares ---

def find_latest_war_log():
    try:
        files = [f for f in os.listdir(DATA_DIR) if f.startswith("war_log_full_") and f.endswith(".json")]
        if not files: return None
        return os.path.join(DATA_DIR, max(files))
    except FileNotFoundError:
        return None

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y%m%dT%H%M%S.%fZ")

# --- Lógica de Processamento ---

def extract_detailed_war_data(war_log_file):
    with open(war_log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    detailed_rows = []
    wars = data.get("items", [])
    if not wars:
        print("--- AVISO: O arquivo JSON não contém nenhuma 'item' (guerra). ---")
        return None

    for war in wars:
        season_id = war.get("seasonId")
        section_index = war.get("sectionIndex")
        created_date = parse_date(war["createdDate"])

        for clan in war.get("clans", []):
            if clan.get("tag") == CLAN_TAG:
                for player in clan.get("participants", []):
                    detailed_rows.append({
                        "war_id": f"S{season_id}-W{section_index}",
                        "created_date": created_date,
                        "player_tag": player.get("tag"),
                        "player_name": player.get("name"),
                        "decks_used": player.get("decksUsed", 0)
                    })

    if not detailed_rows:
        return None

    return pd.DataFrame(detailed_rows)

def create_ranking_df(df):
    if df is None or df.empty:
        return None

    # Garante que os dados estão ordenados por data
    df['created_date'] = pd.to_datetime(df['created_date'])
    df = df.sort_values(by="created_date")

    # Mapeia o nome mais recente para cada jogador
    player_names = df.drop_duplicates(subset='player_tag', keep='last').set_index('player_tag')['player_name']

    participation_pivot = df.pivot_table(
        index='player_tag',
        columns='war_id',
        values='decks_used'
    ).fillna(0).astype(int)

    war_order = df.drop_duplicates('war_id').sort_values('created_date')['war_id']
    participation_pivot = participation_pivot.reindex(columns=war_order)

    last_n_wars = participation_pivot.columns[-NUMERO_DE_GUERRAS_NO_RELATORIO:]
    ranking_df = participation_pivot[last_n_wars]

    ranking_df.insert(0, "Jogador", ranking_df.index.map(player_names))

    last_war_col = ranking_df.columns[-1]
    second_last_war_col = ranking_df.columns[-2] if len(ranking_df.columns) > 1 else None

    def check_novato(row):
        if second_last_war_col and row[last_war_col] > 0 and row.get(second_last_war_col, 0) == 0:
            return "NOVATO"
        return ""

    ranking_df["Status"] = ranking_df.apply(check_novato, axis=1)
    ranking_df = ranking_df.sort_values(by=last_war_col, ascending=True)

    return ranking_df

def main():
    print("Iniciando o processamento dos dados de guerra...")

    latest_log = find_latest_war_log()
    if not latest_log:
        print(f"ERRO: Nenhum arquivo de log ('war_log_full_*.json') encontrado em '{DATA_DIR}'.")
        return

    print(f"Processando o arquivo: {latest_log}")

    detailed_df = extract_detailed_war_data(latest_log)

    if detailed_df is not None and not detailed_df.empty:
        print(f"Salvando dados detalhados em '{OUTPUT_CSV_FILE}'...")
        detailed_df.to_csv(OUTPUT_CSV_FILE, index=False)
        print("Arquivo CSV salvo com sucesso!")

        print("Estruturando o ranking das últimas guerras...")
        final_ranking = create_ranking_df(detailed_df.copy()) # Usa uma cópia para evitar warnings

        if final_ranking is not None and not final_ranking.empty:
            print(f"Exportando o relatório para '{OUTPUT_RANKING_FILE}'...")
            final_ranking.to_excel(OUTPUT_RANKING_FILE, index=False)
            print("Relatório exportado com sucesso!")
        else:
            print("Não foi possível gerar o ranking final.")
    else:
        print("Nenhum dado de guerra válido com participantes foi encontrado para gerar o relatório.")

if __name__ == "__main__":
    main()

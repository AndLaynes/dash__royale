import os
import json
import pandas as pd
from datetime import datetime

# --- Configuração ---
DATA_DIR = "data"
OUTPUT_FILE = "relatorio_de_guerra.xlsx"
NUMERO_DE_GUERRAS_NO_RELATORIO = 5

# --- Funções Auxiliares ---

def find_latest_war_log():
    """Encontra o arquivo de log de guerra mais recente."""
    try:
        files = [f for f in os.listdir(DATA_DIR) if f.startswith("war_log_full_") and f.endswith(".json")]
        if not files: return None
        return os.path.join(DATA_DIR, max(files))
    except FileNotFoundError:
        return None

def parse_date(date_str):
    """Converte a data da API para um objeto datetime."""
    return datetime.strptime(date_str, "%Y%m%dT%H%M%S.%fZ")

# --- Lógica de Processamento ---

def process_war_data(war_log_file):
    """Lê e processa os dados de guerra do arquivo JSON."""
    with open(war_log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_wars_data = []
    player_names = {}

    for war in data.get("items", []):
        created_date = parse_date(war["createdDate"])
        season_id = war.get("seasonId")
        section_index = war.get("sectionIndex") # Usado para identificar a guerra

        for player in war.get("participants", []):
            player_tag = player["tag"]
            player_names[player_tag] = player["name"]

            all_wars_data.append({
                "war_id": f"S{season_id}-W{section_index}",
                "created_date": created_date,
                "player_tag": player_tag,
                "decks_used": player.get("decksUsed", 0)
            })

    if not all_wars_data:
        return None, None

    df = pd.DataFrame(all_wars_data)
    df = df.sort_values(by="created_date").reset_index(drop=True)
    return df, player_names

def create_ranking_df(df, player_names):
    """Estrutura os dados processados em um ranking final."""
    # Pivotar a tabela: jogadores nas linhas, guerras nas colunas
    participation_pivot = df.pivot_table(
        index='player_tag',
        columns='war_id',
        values='decks_used'
    ).fillna(0).astype(int)

    # Ordenar as colunas (guerras) pela data de criação para pegar as últimas 5
    war_order = df.drop_duplicates('war_id').sort_values('created_date')['war_id']
    participation_pivot = participation_pivot.reindex(columns=war_order)

    # Selecionar apenas as últimas N guerras
    if len(participation_pivot.columns) > NUMERO_DE_GUERRAS_NO_RELATORIO:
        last_n_wars = participation_pivot.columns[-NUMERO_DE_GUERRAS_NO_RELATORIO:]
        ranking_df = participation_pivot[last_n_wars]
    else:
        ranking_df = participation_pivot

    # Adicionar o nome do jogador
    ranking_df.insert(0, "Jogador", ranking_df.index.map(player_names))

    # Identificar Novatos
    last_war_col = ranking_df.columns[-1]
    second_last_war_col = ranking_df.columns[-2] if len(ranking_df.columns) > 1 else None

    def check_novato(row):
        # É novato se participou da última guerra mas não da penúltima
        if second_last_war_col and row[last_war_col] > 0 and row[second_last_war_col] == 0:
            return "NOVATO"
        return ""

    ranking_df["Status"] = ranking_df.apply(check_novato, axis=1)

    # Ordenar pelo menor número de decks na última guerra
    ranking_df = ranking_df.sort_values(by=last_war_col, ascending=True)

    return ranking_df

def main():
    """Função principal para orquestrar o processamento."""
    print("Iniciando o processamento dos dados de guerra...")

    latest_log = find_latest_war_log()
    if not latest_log:
        print("ERRO: Nenhum arquivo de log de guerra encontrado. Execute 'get_data.py' primeiro.")
        return

    print(f"Processando o arquivo: {latest_log}")

    processed_df, player_names_map = process_war_data(latest_log)

    if processed_df is not None:
        print("Estruturando o ranking das últimas guerras...")
        final_ranking = create_ranking_df(processed_df, player_names_map)

        print(f"Exportando o relatório para '{OUTPUT_FILE}'...")
        # index=False para não incluir a tag do jogador como uma coluna no Excel
        final_ranking.to_excel(OUTPUT_FILE, index=False)
        print("Relatório exportado com sucesso!")

    else:
        print("Nenhum dado de guerra válido encontrado para gerar o relatório.")

# --- Execução do Script ---
if __name__ == "__main__":
    main()

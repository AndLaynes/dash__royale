import os
import json
import requests
from datetime import datetime

# --- Configuração ---
CLAN_TAG = "#9PJRJRPC"
API_KEY_ENV_VAR = "CLASH_ROYALE_API_KEY"
BASE_API_URL = "https://api.clashroyale.com/v1"
DATA_DIR = "data"

# --- Funções ---

def get_api_key():
    """Recupera a chave da API das variáveis de ambiente."""
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"A variável de ambiente '{API_KEY_ENV_VAR}' não foi definida.")
    return api_key

def save_json(data, filename):
    """Salva os dados em um arquivo JSON."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em: {filepath}")

def fetch_data(endpoint, params=None):
    """Busca dados de um endpoint da API."""
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{BASE_API_URL}{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def fetch_paginated_data(endpoint):
    """Busca dados paginados, agregando todos os resultados."""
    all_items = []
    params = {'limit': 100}

    while True:
        print(f"Buscando página (cursor: {params.get('after', 'inicial')})...")
        json_response = fetch_data(endpoint, params=params)

        if not json_response:
            print("Falha ao buscar dados paginados.")
            break

        items = json_response.get('items', [])
        all_items.extend(items) # Salva todos os dados, sem filtro

        if 'paging' in json_response and 'cursors' in json_response['paging'] and 'after' in json_response['paging']['cursors']:
            params['after'] = json_response['paging']['cursors']['after']
        else:
            break

    return {"items": all_items}

def main():
    """Função principal para buscar e salvar os dados do clã."""
    try:
        clan_tag_formatted = CLAN_TAG.replace("#", "%23")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Busca da Guerra Atual
        print("Buscando dados de: current_war...")
        current_war_endpoint = f"/clans/{clan_tag_formatted}/currentriverrace"
        current_war_data = fetch_data(current_war_endpoint)
        if current_war_data:
            save_json(current_war_data, f"current_war_{timestamp}.json")

        # Busca do Histórico de Guerras
        print("\nBuscando dados de: war_log (todo o histórico)...")
        war_log_endpoint = f"/clans/{clan_tag_formatted}/riverracelog"
        war_log_data = fetch_paginated_data(war_log_endpoint)
        if war_log_data and war_log_data['items']:
            save_json(war_log_data, f"war_log_full_{timestamp}.json")

        print("\nDownload dos dados concluído!")
    except ValueError as e:
        print(f"\nErro de configuração: {e}")
        print(f"Certifique-se de que a variável de ambiente {API_KEY_ENV_VAR} está definida.")

if __name__ == "__main__":
    main()

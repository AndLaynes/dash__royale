import os
import json
import requests
from datetime import datetime

# --- Configuração ---
# A tag do seu clã (substitua pelo valor real)
# Exemplo: CLAN_TAG = "#2222GGPP"
CLAN_TAG = "#9PJRJRPC"

# Nome da variável de ambiente que armazena a chave da API
API_KEY_ENV_VAR = "CLASH_ROYALE_API_KEY"

# URL base da API do Clash Royale
BASE_API_URL = "https://api.clashroyale.com/v1"

# Diretório para salvar os dados
DATA_DIR = "data"

# --- Funções ---

def get_api_key():
    """
    Recupera a chave da API das variáveis de ambiente.
    """
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        raise ValueError(f"A variável de ambiente '{API_KEY_ENV_VAR}' não foi definida.")
    return api_key

def save_json(data, filename):
    """
    Salva os dados em um arquivo JSON no diretório de dados.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em: {filepath}")

def fetch_data(endpoint):
    """
    Busca dados de um endpoint específico da API.
    """
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    url = f"{BASE_API_URL}{endpoint}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def main():
    """
    Função principal para buscar e salvar os dados do clã.
    """
    try:
        # Verifica se a tag do clã foi definida
        if CLAN_TAG == "SUA_TAG_AQUI":
            print("!!! ATENÇÃO !!!")
            print("Por favor, substitua 'SUA_TAG_AQUI' pela tag do seu clã no script.")
            return

        # Formata a tag do clã para uso na URL (remove o '#')
        clan_tag_formatted = CLAN_TAG.replace("#", "%23")

        # --- Endpoints da API ---
        endpoints = {
            "current_war": f"/clans/{clan_tag_formatted}/currentriverrace",
            "war_log": f"/clans/{clan_tag_formatted}/riverracelog"
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Busca e salva os dados de cada endpoint
        for name, endpoint_url in endpoints.items():
            print(f"Buscando dados de: {name}...")
            data = fetch_data(endpoint_url)

            if data:
                filename = f"{name}_{timestamp}.json"
                save_json(data, filename)

        print("\nDownload dos dados concluído!")
    except ValueError as e:
        print(f"\nErro de configuração: {e}")
        print("Certifique-se de que a variável de ambiente CLASH_ROYALE_API_KEY está definida.")

# --- Execução do Script ---
if __name__ == "__main__":
    main()

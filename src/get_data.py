import os
import requests
import json
import sys
import time

# Define os caminhos de forma robusta
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')

def handle_api_error(response, endpoint_name):
    """Função centralizada para tratar erros da API e fornecer feedback claro."""
    status_code = response.status_code
    try:
        error_data = response.json()
    except json.JSONDecodeError:
        error_data = response.text

    error_messages = {
        400: "Erro de requisição (Bad Request). Verifique os parâmetros enviados.",
        403: "Erro de autenticação (Forbidden). A sua chave da API (CLASH_ROYALE_API_KEY) é inválida ou não foi definida corretamente.",
        404: f"Recurso não encontrado (Not Found). O Clan Tag pode estar incorreto. Verifique o clan_tag no início deste script.",
        500: "Erro interno no servidor da Supercell (Internal Server Error). Tente novamente mais tarde.",
        503: "Serviço indisponível (Service Unavailable). A API da Supercell pode estar em manutenção. Tente novamente mais tarde."
    }

    print(f"Erro Crítico ao buscar dados de '{endpoint_name}' (Código: {status_code}).")
    print(error_messages.get(status_code, "Um erro inesperado ocorreu."))
    print("Detalhes do erro:", error_data)
    sys.exit(1) # Interrompe a execução

def download_data():
    """
    Baixa os dados da guerra atual e o histórico de guerras da API do Clash Royale.
    """
    api_key = os.getenv('CLASH_ROYALE_API_KEY')
    if not api_key:
        print("Erro Crítico: A variável de ambiente 'CLASH_ROYALE_API_KEY' não está definida.")
        print("Por favor, configure a variável de ambiente com sua chave da API e tente novamente.")
        sys.exit(1)

    headers = {'Authorization': f'Bearer {api_key}'}
    clan_tag = '#9PJRJRPC'

    # Validação básica do formato do Clan Tag
    if not clan_tag.startswith('#') or len(clan_tag) < 4:
        print(f"Erro Crítico: O formato do Clan Tag '{clan_tag}' parece ser inválido.")
        sys.exit(1)

    # Codifica o Clan Tag para ser usado na URL
    encoded_clan_tag = '%23' + clan_tag[1:]

    endpoints = {
        'current_war': f'https://api.clashroyale.com/v1/clans/{encoded_clan_tag}/currentriverrace',
        'warlog': f'https://api.clashroyale.com/v1/clans/{encoded_clan_tag}/riverracelog'
    }

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for name, url in endpoints.items():
        print(f"Buscando dados de '{name}'...")
        try:
            response = requests.get(url, headers=headers, timeout=10) # Timeout de 10 segundos
            # Verifica se a resposta foi bem-sucedida
            if response.status_code != 200:
                handle_api_error(response, name)

            data = response.json()

            file_path = os.path.join(data_dir, f'{name}.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Dados de '{name}' salvos com sucesso em '{file_path}'.")

        except requests.exceptions.RequestException as e:
            print(f"Erro Crítico de conexão ao buscar '{name}'.")
            print("Verifique sua conexão com a internet.")
            print("Detalhes do erro:", e)
            sys.exit(1)

        # Pausa para não sobrecarregar a API
        time.sleep(1)

if __name__ == "__main__":
    download_data()

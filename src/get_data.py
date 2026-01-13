import os
import requests
import json
import sys
import time
import socket
import requests.packages.urllib3.util.connection as urllib3_cn

# --- FORCE IPV4 PATCH (GT-Z Networking) ---
# O IP Publico IPv6 (2804...) não está na whitelist. O IPv4 (191...) está.
# Forçamos o requests a usar apenas a família AF_INET (IPv4).
def allowed_gai_family():
    return socket.AF_INET

urllib3_cn.allowed_gai_family = allowed_gai_family
# ------------------------------------------

# Define os caminhos de forma robusta
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')

def handle_api_error(response, endpoint_name):
    """Função centralizada para tratar erros da API e fornecer feedback claro."""
    status_code = response.status_code
    try:
        error_data = response.json()
    except json.JSONDecodeError:
        error_data = {"raw_response": response.text}

    error_messages = {
        400: "Erro de requisição (Bad Request). Verifique os parâmetros enviados.",
        403: "Erro de autenticação (Forbidden). A sua chave da API (CLASH_ROYALE_API_KEY) é inválida ou não foi definida corretamente.",
        404: f"Recurso não encontrado (Not Found). O Clan Tag pode estar incorreto. Verifique a variável de ambiente CLAN_TAG.",
        500: "Erro interno no servidor da Supercell (Internal Server Error). Tente novamente mais tarde.",
        503: "Serviço indisponível (Service Unavailable). A API da Supercell pode estar em manutenção."
    }

    print(f"Erro Crítico ao buscar dados de '{endpoint_name}' (Código: {status_code}).", file=sys.stderr)
    print(error_messages.get(status_code, "Um erro inesperado ocorreu."), file=sys.stderr)
    print("Detalhes do erro:", json.dumps(error_data, indent=2), file=sys.stderr)
    sys.exit(1)

def get_full_river_race_log(clan_tag, headers):
    """
    Busca o histórico completo de guerras (`riverracelog`), tratando a paginação.
    """
    all_items = []

    # Define o limite de itens por página (o máximo permitido pela API é 50)
    params = {'limit': 50}

    url = f'https://api.clashroyale.com/v1/clans/{clan_tag}/riverracelog'

    page_count = 0
    while True:
        page_count += 1
        print(f"Buscando página {page_count} do histórico de guerras...")

        response = requests.get(url, headers=headers, params=params, timeout=20)

        if response.status_code != 200:
            handle_api_error(response, f"riverracelog (página {page_count})")

        data = response.json()
        items = data.get('items', [])
        all_items.extend(items)

        # Verifica se há uma próxima página
        if 'paging' in data and 'cursors' in data['paging'] and 'after' in data['paging']['cursors']:
            params['after'] = data['paging']['cursors']['after']
            time.sleep(1) # Pausa respeitosa entre as chamadas
        else:
            # Não há mais páginas
            break

    print(f"Total de {len(all_items)} registros de guerra baixados de {page_count} página(s).")
    return {'items': all_items}

def download_data():
    """
    Baixa os dados da guerra atual e o histórico completo da API do Clash Royale.
    """
    api_key = os.getenv('CLASH_ROYALE_API_KEY')
    clan_tag = os.getenv('CLAN_TAG')

    if not api_key:
        print("Erro Crítico: A variável de ambiente 'CLASH_ROYALE_API_KEY' não está definida.", file=sys.stderr)
        sys.exit(1)
    if not clan_tag:
        print("Erro Crítico: A variável de ambiente 'CLAN_TAG' não está definida.", file=sys.stderr)
        sys.exit(1)

    if not clan_tag.startswith('#'):
        print(f"Erro Crítico: O formato do CLAN_TAG '{clan_tag}' é inválido. Deve começar com '#'.", file=sys.stderr)
        sys.exit(1)

    headers = {'Authorization': f'Bearer {api_key}'}
    encoded_clan_tag = '%23' + clan_tag[1:]

    os.makedirs(data_dir, exist_ok=True)

    # 1. Baixar dados da guerra atual
    try:
        current_war_url = f'https://api.clashroyale.com/v1/clans/{encoded_clan_tag}/currentriverrace'
        print("Buscando dados de 'currentriverrace'...")
        response = requests.get(current_war_url, headers=headers, timeout=10)

        if response.status_code != 200:
            handle_api_error(response, 'currentriverrace')

        current_war_data = response.json()
        file_path = os.path.join(data_dir, 'current_war.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(current_war_data, f, indent=4, ensure_ascii=False)
        print(f"Dados de 'currentriverrace' salvos com sucesso em '{os.path.basename(file_path)}'.")

    except requests.exceptions.RequestException as e:
        print(f"Erro Crítico de conexão ao buscar 'currentriverrace'. Detalhes: {e}", file=sys.stderr)
        sys.exit(1)

    time.sleep(1)

    # 2. Baixar o histórico completo de guerras (riverracelog)
    try:
        full_log_data = get_full_river_race_log(encoded_clan_tag, headers)
        file_path = os.path.join(data_dir, 'riverracelog.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(full_log_data, f, indent=4, ensure_ascii=False)
        print(f"Histórico completo de guerras salvo com sucesso em '{os.path.basename(file_path)}'.")

    except requests.exceptions.RequestException as e:
        print(f"Erro Crítico de conexão ao buscar o histórico de guerras. Detalhes: {e}", file=sys.stderr)
        sys.exit(1)

    time.sleep(1)

    # 3. Baixar lista de membros (Ranking e Doações)
    try:
        members_url = f'https://api.clashroyale.com/v1/clans/{encoded_clan_tag}/members'
        print("Buscando lista de membros 'clan/members'...")
        response = requests.get(members_url, headers=headers, timeout=10)

        if response.status_code != 200:
            handle_api_error(response, 'clan_members')

        members_data = response.json()
        file_path = os.path.join(data_dir, 'clan_members.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(members_data, f, indent=4, ensure_ascii=False)
        print(f"Lista de membros salva com sucesso em '{os.path.basename(file_path)}'.")

    except requests.exceptions.RequestException as e:
        print(f"Erro Crítico de conexão ao buscar lista de membros. Detalhes: {e}", file=sys.stderr)
        sys.exit(1)

    time.sleep(1)

    # 4. Baixar informações do Clã (Ranking, Liga, Localização - GT-Z)
    try:
        clan_url = f'https://api.clashroyale.com/v1/clans/{encoded_clan_tag}'
        print("Buscando informações do clã 'clans/tag' (GT-Z)...")
        response = requests.get(clan_url, headers=headers, timeout=10)

        if response.status_code != 200:
            handle_api_error(response, 'clan_info')

        clan_info = response.json()
        file_path = os.path.join(data_dir, 'clan_info.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(clan_info, f, indent=4, ensure_ascii=False)
        print(f"Informações básicas do clã salvas em '{os.path.basename(file_path)}'.")

    except requests.exceptions.RequestException as e:
        print(f"Erro Crítico de conexão ao buscar info do clã. Detalhes: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    download_data()

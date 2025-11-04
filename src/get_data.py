import os
import requests
import json
import time
import sys

# O diretório do projeto é o pai do diretório 'src'
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')

# Função para obter os dados da API com paginação
def get_paginated_data(url, headers):
    all_items = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_items.extend(data.get('items', []))
            # Obter o cursor para a próxima página, se houver
            url = data.get('paging', {}).get('cursors', {}).get('after')
        else:
            print(f"Erro ao buscar dados: {response.status_code}")
            print(response.json())
            break
        time.sleep(1)  # Pausa para evitar sobrecarregar a API
    return all_items

# Função principal para baixar os dados
def download_data():
    api_key = os.getenv('CLASH_ROYALE_API_KEY')
    if not api_key:
        print("Erro: A variável de ambiente 'CLASH_ROYALE_API_KEY' não foi definida.")
        print("Certifique-se de que a variável de ambiente CLASH_ROYALE_API_KEY está definida.")
        sys.exit(1)

    headers = {'Authorization': f'Bearer {api_key}'}
    clan_tag = '#L2Y82L'  # IMPORTANTE: Verifique se este é o tag correto do seu clã.

    endpoints = {
        'current_war': f'https://api.clashroyale.com/v1/clans/%23{clan_tag[1:]}/currentriverrace',
        'warlog': f'https://api.clashroyale.com/v1/clans/%23{clan_tag[1:]}/riverracelog'
    }

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for name, url in endpoints.items():
        print(f"Buscando dados de: {name}...")
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            print(f"Erro Crítico (404 Not Found) ao buscar '{name}'.")
            print(f"Isso geralmente significa que o Clan Tag ('{clan_tag}') está incorreto ou não foi encontrado.")
            print("Por favor, verifique o clan_tag no arquivo 'src/get_data.py' e tente novamente.")
            sys.exit(1) # Interrompe a execução

        if response.status_code != 200:
            print(f"Erro ao buscar {name}: {response.status_code}")
            print(response.json())
            sys.exit(1) # Interrompe a execução para outros erros também

        data = response.json()

        # Salvar os dados em um arquivo JSON
        file_path = os.path.join(data_dir, f'{name}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Dados de '{name}' salvos em '{file_path}'.")

if __name__ == "__main__":
    download_data()

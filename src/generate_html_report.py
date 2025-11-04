import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
import json

# Define os caminhos de forma robusta
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_dir, 'data')
template_dir = os.path.join(project_dir, 'src', 'templates')

data_file = os.path.join(data_dir, 'relatorio_participacao_guerra.xlsx')
log_file = os.path.join(data_dir, 'process_log.json')
output_file = os.path.join(project_dir, 'relatorio_guerra.html')

def generate_html_report():
    """Lê os dados processados e os logs para gerar um relatório HTML completo."""
    print("Iniciando a geração do relatório HTML...")

    # Carregar os dados do arquivo Excel
    if not os.path.exists(data_file):
        print(f"Alerta: O arquivo de dados '{os.path.basename(data_file)}' não foi encontrado. O relatório será gerado sem dados de jogadores.")
        df = pd.DataFrame()
    else:
        try:
            df = pd.read_excel(data_file)
            df.fillna('-', inplace=True)
        except Exception as e:
            print(f"Erro ao ler o arquivo Excel: {e}")
            df = pd.DataFrame()

    # Carregar os logs de diagnóstico
    log_messages = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_messages = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao ler o arquivo de log: {e}")
            log_messages = [f"Falha ao carregar o log de diagnóstico: {e}"]
    else:
        print(f"Info: Arquivo de log '{os.path.basename(log_file)}' não encontrado.")

    # Determinar o título do relatório (se houver dados)
    title = "Histórico de Participação em Guerras" # Título padrão
    if not df.empty and 'Fonte de Dados' in df.columns:
        source = df['Fonte de Dados'].iloc[0]
        if source == "Guerra Atual":
            title = "Análise da Guerra Atual"
        elif "Histórico" in source:
            title = f"Análise baseada na guerra de {source.split('(')[-1].replace(')', '')}"

    # Configurar o ambiente do Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')

    # Obter a data de atualização dos dados, se disponível
    update_timestamp = datetime.now()
    if os.path.exists(data_file):
        update_timestamp = datetime.fromtimestamp(os.path.getmtime(data_file))

    # Carregar os IDs das temporadas de guerra
    season_ids_path = os.path.join(data_dir, 'war_season_ids.json')
    war_season_ids = {}
    if os.path.exists(season_ids_path):
        try:
            with open(season_ids_path, 'r', encoding='utf-8') as f:
                war_season_ids = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Alerta: Não foi possível carregar os IDs da temporada de guerra. {e}")

    # Mapeia as datas das colunas para seus IDs de temporada
    date_to_id = {date: war_season_ids.get(date) for date in war_season_ids}

    # Cria os cabeçalhos das colunas com os IDs das temporadas, se disponíveis
    column_headers = {"Nome": "Nome", "Player Status": "Player Status"}
    war_columns = ['Última Guerra', 'Guerra -2', 'Guerra -3', 'Guerra -4', 'Guerra -5']
    all_war_dates = sorted(war_season_ids.keys(), reverse=True)[:len(war_columns)]

    for i, col_name in enumerate(war_columns):
        if i < len(all_war_dates):
            war_date = all_war_dates[i]
            season_id = war_season_ids.get(war_date)
            column_headers[col_name] = f"{col_name} ({season_id})" if season_id else col_name
        else:
            # Fallback para caso não haja seasonId para aquela coluna
            column_headers[col_name] = col_name

    # Renderizar o template com os dados, logs e título
    html_content = template.render(
        report_title=title,
        players=df.to_dict(orient='records'),
        column_headers=column_headers, # Passa os novos cabeçalhos para o template
        report_date=update_timestamp.strftime('%d/%m/%Y %H:%M:%S'),
        log_messages=log_messages,
        data_found=not df.empty
    )

    # Salvar o relatório em um arquivo HTML
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Relatório HTML gerado com sucesso em '{os.path.basename(output_file)}'.")
    except IOError as e:
        print(f"Erro Crítico: Não foi possível salvar o relatório HTML em '{os.path.basename(output_file)}'. Detalhes: {e}")

if __name__ == "__main__":
    generate_html_report()

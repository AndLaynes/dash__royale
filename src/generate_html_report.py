import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# O diretório do projeto é o pai do diretório 'src'
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho para o arquivo de dados e para o diretório de templates
data_file = os.path.join(project_dir, 'data', 'relatorio_participacao_guerra.xlsx')
template_dir = os.path.join(project_dir, 'src', 'templates')
output_file = os.path.join(project_dir, 'relatorio_guerra.html')

def generate_html_report():
    """Lê os dados processados e gera um relatório HTML."""
    print("Iniciando a geração do relatório HTML...")

    # Verificar se o arquivo de dados existe
    if not os.path.exists(data_file):
        print(f"Erro: O arquivo de dados '{data_file}' não foi encontrado.")
        print("Por favor, execute o script 'process_data.py' primeiro para gerar os dados.")
        return

    # Carregar os dados do arquivo Excel
    try:
        df = pd.read_excel(data_file)
        # Substituir valores NaN por um traço para melhor visualização
        df.fillna('-', inplace=True)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    # Configurar o ambiente do Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')

    # Renderizar o template com os dados
    html_content = template.render(
        players=df.to_dict(orient='records'),
        report_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    )

    # Salvar o relatório em um arquivo HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Relatório HTML gerado com sucesso em '{output_file}'.")

if __name__ == "__main__":
    generate_html_report()

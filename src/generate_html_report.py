import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

# Define os caminhos de forma robusta
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(project_dir, 'data', 'relatorio_participacao_guerra.xlsx')
template_dir = os.path.join(project_dir, 'src', 'templates')
output_file = os.path.join(project_dir, 'relatorio_guerra.html')

def generate_html_report():
    """Lê os dados processados e gera um relatório HTML com título dinâmico."""
    print("Iniciando a geração do relatório HTML...")

    # Verificar se o arquivo de dados existe
    if not os.path.exists(data_file):
        print(f"Erro: O arquivo de dados '{data_file}' não foi encontrado.")
        return

    # Carregar os dados do arquivo Excel
    try:
        df = pd.read_excel(data_file)
        df.fillna('-', inplace=True)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        # Cria um dataframe vazio para gerar um relatório de "sem dados"
        df = pd.DataFrame()

    # Determinar o título do relatório
    title = "Histórico de Participação em Guerras" # Título padrão
    if not df.empty and 'Fonte de Dados' in df.columns:
        source = df['Fonte de Dados'].iloc[0]
        if source == "Guerra Atual":
            title = "Histórico de Participação na Guerra Atual"
        elif source == "Última Guerra":
            title = "Resultado da Última Guerra"

    # Configurar o ambiente do Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')

    # Renderizar o template com os dados e o título
    html_content = template.render(
        report_title=title,
        players=df.to_dict(orient='records'),
        report_date=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    )

    # Salvar o relatório em um arquivo HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Relatório HTML gerado com sucesso em '{output_file}'.")

if __name__ == "__main__":
    generate_html_report()

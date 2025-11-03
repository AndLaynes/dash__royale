import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

def generate_html_report():
    """
    Lê os dados do relatório Excel e gera um relatório HTML a partir de um template Jinja2.
    """
    print("Iniciando a geração do relatório HTML...")

    try:
        # Constrói os caminhos de forma robusta a partir da localização do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        excel_path = os.path.join(project_root, 'relatorio_participacao_guerra.xlsx')
        template_dir = os.path.join(script_dir, 'templates')
        output_path = os.path.join(project_root, 'relatorio_guerra.html')

        # Verifica se o arquivo Excel existe
        if not os.path.exists(excel_path):
            print(f"Erro: O arquivo de dados '{excel_path}' não foi encontrado.")
            print("Por favor, execute o script 'process_data.py' primeiro para gerar os dados.")
            return

        # Carrega os dados da planilha 'Historico_Guerra'
        df = pd.read_excel(excel_path, sheet_name='Historico_Guerra')

        # Converte o DataFrame para uma lista de dicionários para o template
        data = df.to_dict(orient='records')

        # Configura o ambiente do Jinja2
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template('report_template.html')

        # Obtém a data e hora atual para o rodapé
        generation_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        # Renderiza o template com os dados
        html_content = template.render(
            players=data,
            report_date=generation_time
        )

        # Salva o conteúdo HTML em um arquivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Relatório HTML 'relatorio_guerra.html' gerado com sucesso em: {project_root}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o relatório HTML: {e}")

if __name__ == '__main__':
    generate_html_report()

from flask import Flask, send_from_directory, redirect, url_for
import subprocess
import os

app = Flask(__name__)

# Rota para servir o relatório HTML como um arquivo estático
@app.route('/')
def index():
    return send_from_directory('.', 'relatorio_guerra.html')

# Rota para acionar a atualização dos dados
@app.route('/update')
def update():
    try:
        # Executa os scripts em sequência
        print("Atualizando dados: executando get_data.py...")
        subprocess.run(['python', 'src/get_data.py'], check=True)
        print("Atualizando dados: executando process_data.py...")
        subprocess.run(['python', 'src/process_data.py'], check=True)
        print("Atualizando dados: executando generate_html_report.py...")
        subprocess.run(['python', 'src/generate_html_report.py'], check=True)
        print("Atualização concluída com sucesso.")
    except subprocess.CalledProcessError as e:
        # Se algum script falhar, pode-se adicionar um log ou tratamento de erro
        print(f"Erro ao executar o script: {e}")
        # Opcional: retornar uma página de erro
        return "Ocorreu um erro ao atualizar os dados.", 500

    # Redireciona de volta para a página principal
    return redirect(url_for('index'))

def generate_initial_report():
    """Gera o relatório inicial se ele não existir."""
    if not os.path.exists('relatorio_guerra.html'):
        print("Arquivo 'relatorio_guerra.html' não encontrado. Gerando um novo...")
        try:
            print("Geração inicial: executando get_data.py...")
            subprocess.run(['python', 'src/get_data.py'], check=True)
            print("Geração inicial: executando process_data.py...")
            subprocess.run(['python', 'src/process_data.py'], check=True)
            print("Geração inicial: executando generate_html_report.py...")
            subprocess.run(['python', 'src/generate_html_report.py'], check=True)
            print("Geração inicial concluída com sucesso.")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao gerar o relatório inicial: {e}")
            # Se a geração falhar, o servidor não deve iniciar
            exit(1)

if __name__ == '__main__':
    generate_initial_report()
    print("Iniciando o servidor Flask...")
    app.run(debug=True)

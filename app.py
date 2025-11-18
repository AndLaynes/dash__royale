from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# Define o diretório raiz do projeto
project_root = os.path.dirname(os.path.abspath(__file__))

def serve_report(filename):
    """
    Função genérica para servir um arquivo de relatório da raiz do projeto.
    Retorna uma mensagem de erro 404 se o arquivo não for encontrado.
    """
    file_path = os.path.join(project_root, filename)
    if not os.path.exists(file_path):
        return f"""
        <h1>Erro: Relatório não encontrado</h1>
        <p>O arquivo <code>{filename}</code> não foi encontrado.</p>
        <p>Por favor, execute o script <code>python run_update.py</code> para gerar os relatórios antes de iniciar o servidor.</p>
        """, 404

    return send_from_directory(project_root, filename)

@app.route('/')
def index():
    """Serve o relatório principal (index.html)."""
    return serve_report('index.html')

@app.route('/acompanhamento_diario')
def daily_report():
    """Serve o relatório de acompanhamento diário."""
    return serve_report('acompanhamento_diario.html')

if __name__ == '__main__':
    print("Iniciando o servidor Flask...")
    print(f"Acesse o dashboard principal em http://127.0.0.1:5000")
    print(f"Acesse o acompanhamento diário em http://127.0.0.1:5000/acompanhamento_diario")
    app.run(debug=True, port=5000)

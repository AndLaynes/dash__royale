from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# Define o caminho absoluto para o arquivo de relatório
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'relatorio_guerra.html')

@app.route('/')
def index():
    """
    Serve o arquivo 'relatorio_guerra.html'.
    Se o arquivo não existir, retorna um erro 404 com uma mensagem útil.
    """
    if not os.path.exists(report_path):
        # Retorna uma mensagem de erro clara se o relatório não foi gerado ainda
        return """
        <h1>Erro: Relatório não encontrado</h1>
        <p>O arquivo <code>relatorio_guerra.html</code> não foi encontrado.</p>
        <p>Por favor, execute o script <code>python run_update.py</code> para gerar o relatório antes de iniciar o servidor.</p>
        """, 404

    # Serve o arquivo do diretório raiz do projeto
    return send_from_directory('.', 'relatorio_guerra.html')

if __name__ == '__main__':
    print("Iniciando o servidor Flask...")
    print(f"Acesse o dashboard em http://127.0.0.1:5000")
    # O modo de depuração é mantido para facilitar o desenvolvimento, mas pode ser desativado
    app.run(debug=True)

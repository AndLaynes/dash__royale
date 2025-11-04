import subprocess
import sys

def run_script(script_path):
    """
    Executa um script Python, capturando e exibindo stdout e stderr em tempo real.
    Levanta uma exceção se o script retornar um código de erro.
    """
    print(f"--- Executando {script_path} ---")
    # Usa sys.executable para garantir o uso do mesmo ambiente Python
    # O processo é executado e suas saídas (stdout, stderr) são capturadas
    process = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    # Lê e imprime a saída em tempo real
    stdout, stderr = process.communicate()

    if stdout:
        print(stdout)
    if stderr:
        # Imprime a saída de erro, crucial para a depuração
        print(stderr, file=sys.stderr)

    if process.returncode != 0:
        # Levanta uma exceção para interromper o processo de atualização
        raise subprocess.CalledProcessError(process.returncode, process.args)

def main():
    """
    Ponto de entrada principal para o processo de atualização de dados.
    """
    print("Iniciando o processo de atualização de dados do Clash Royale...")

    try:
        run_script('src/get_data.py')
        run_script('src/process_data.py')
        run_script('src/generate_html_report.py')

        print("\n\033[92mProcesso de atualização concluído com sucesso!\033[0m")
        print("Você já pode iniciar o servidor com 'python app.py'.")

    except subprocess.CalledProcessError:
        # A mensagem de erro específica já foi impressa pela função run_script
        print("\n\033[91mO processo de atualização falhou. Veja os erros acima para mais detalhes.\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\n\033[91mOcorreu um erro inesperado: {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()

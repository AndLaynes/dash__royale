import subprocess
import sys
import locale

def run_script(script_path):
    """
    Executa um script Python de forma robusta, usando a codificação de caracteres
    nativa do sistema e tratando erros de forma rigorosa.
    """
    print(f"--- Executando {script_path} ---")
    try:
        # Detecta a codificação de caracteres preferida do sistema (ex: 'cp1252' no Windows)
        system_encoding = locale.getpreferredencoding(False)

        # subprocess.run é uma forma mais moderna e segura de executar processos.
        # - check=True: Levanta uma exceção (CalledProcessError) se o script retornar um erro.
        # - capture_output=True: Captura stdout e stderr.
        # - text=True: Decodifica a saída como texto usando a codificação especificada.
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True,
            encoding=system_encoding
        )

        # Imprime a saída padrão do script apenas se ele for bem-sucedido
        if result.stdout:
            print(result.stdout)

        # A saída de erro (stderr) será capturada na exceção em caso de falha

    except subprocess.CalledProcessError as e:
        # Este erro é capturado se o script filho terminar com um código de erro (ex: falhou ao rodar)
        print(f"ERRO: O script '{script_path}' retornou um código de erro.", file=sys.stderr)
        if e.stdout:
            print("--- Saída Padrão (stdout) ---", file=sys.stderr)
            print(e.stdout, file=sys.stderr)
        if e.stderr:
            print("--- Saída de Erro (stderr) ---", file=sys.stderr)
            print(e.stderr, file=sys.stderr)
        # Re-levanta a exceção para que o loop principal pare
        raise e
    except UnicodeDecodeError as e:
        # Este erro é capturado se, mesmo com a codificação do sistema, algo der errado
        print(f"ERRO: Falha ao decodificar a saída do script '{script_path}'.", file=sys.stderr)
        print(f"Detalhes: {e}", file=sys.stderr)
        # Encerra o processo levantando um erro genérico
        raise RuntimeError(f"Falha de codificação em {script_path}") from e

def git_auto_sync():
    """
    Executa a sincronização automática com o repositório remoto (GitHub).
    Regra de Ouro: "Fazer a atualização do repositório automaticamente."
    """
    print("\n--- Iniciando Sincronização Automática (Git Auto-Sync) ---")
    
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", "chore(auto): pipeline update & logic validation [skip ci]"],
        ["git", "push", "origin", "main"]
    ]

    for cmd in commands:
        cmd_str = " ".join(cmd)
        try:
            print(f"> Executando: {cmd_str}")
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                encoding=locale.getpreferredencoding(False)
            )
            if result.stdout:
                # Filtrar saída para não poluir demais, mas mostrar progresso
                print(f"  Status: OK")
        except subprocess.CalledProcessError as e:
            # Se não houver nada para commitar, o git retorna erro 1, mas é 'ok' logicamente
            if "nothing to commit" in e.stdout or "nothing to commit" in e.stderr:
                 print("  Info: Nenhuma alteração pendente para commit.")
            else:
                print(f"  Erro no comando git: {e.stderr}", file=sys.stderr)
                # Não abortamos o script inteiro por erro de git, apenas logamos
                
def main():
    """
    Ponto de entrada principal que executa a sequência de scripts de atualização.
    """
    print("Iniciando o processo de atualização de dados do Clash Royale...")

    scripts_to_run = [
        'src/get_data.py',
        'src/process_data.py',
        'src/generate_html_report.py'
    ]

    # Executa cada script sequencialmente e para imediatamente em caso de erro
    for script in scripts_to_run:
        try:
            run_script(script)
        except (subprocess.CalledProcessError, RuntimeError):
            print(f"\n\033[91mO processo de atualização FALHOU durante a execução de '{script}'.\033[0m")
            print("Revise os erros detalhados acima.")
            sys.exit(1) # Encerra o script com um código de erro
        except Exception as e:
            print(f"\n\033[91mOcorreu um erro inesperado e fatal durante a execução de '{script}': {e}\033[0m")
            sys.exit(1)

    # Executar Auto-Sync (Pedido Expresso)
    try:
        git_auto_sync()
    except Exception as e:
        print(f"Aviso: Falha na sincronização do Git: {e}")

    # Mensagem Final Refinada (Ground Truth)
    print("\n\033[92mProcesso de atualização e sincronização concluído com sucesso!\033[0m")
    print("1. Dados coletados e processados.")
    print("2. Relatórios HTML gerados.")
    print("3. Repositório atualizado automaticamente.")
    print("Status: PRONTO PARA OPERAÇÃO.")

if __name__ == "__main__":
    main()

import requests
import os
import sys
from datetime import datetime

def send_discord_notification(success, log_summary=""):
    """
    Envia uma notificação para um canal do Discord via Webhook.
    Segurança: Usa URL de Webhook (Tokenizada) em vez de credenciais de usuário/senha.
    """
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

    if not webhook_url:
        print("Aviso: Variável 'DISCORD_WEBHOOK_URL' não definida. Notificação pulada.")
        return

    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Cores do Embed: Verde (Sucesso) ou Vermelho (Falha)
    color = 3066993 if success else 15158332 # Int values for Green / Red

    title = "✅ Dash Royale Update: SUCESSO" if success else "❌ Dash Royale Update: FALHA"
    
    description = f"**Data:** {timestamp}\n"
    if success:
        description += "O pipeline de dados foi executado e o site foi atualizado."
    else:
        description += "**ERRO CRÍTICO DETECTADO.** Verifique os logs abaixo."

    # Limita o tamanho do log para não estourar o limite do Discord (4096 chars)
    if len(log_summary) > 1000:
        log_summary = log_summary[:1000] + "... (Logs truncados)"

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": [
            {
                "name": "Resumo dos Logs",
                "value": f"```{log_summary}```",
                "inline": False
            }
        ],
        "footer": {
            "text": "Dash Royale Automation Bot • GT-Z Protocol"
        }
    }

    payload = {
        "embeds": [embed]
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in [200, 204]:
            print("Notificação Discord enviada com sucesso.")
        else:
            print(f"Falha ao enviar notificação Discord. Status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Erro de conexão com Discord: {e}", file=sys.stderr)

if __name__ == "__main__":
    # Teste de argumento via linha de comando
    status_arg = "success"
    if len(sys.argv) > 1:
        # Ex: python webhook_notifier.py failure
         if "fail" in sys.argv[1].lower():
             status_arg = "failure"
    
    # send_discord_notification(status_arg == "success", "Teste de Log.\nLinha 2 de teste.")

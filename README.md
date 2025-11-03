# Dashboard de Guerra de Clãs do Clash Royale

Este projeto é um dashboard web para visualizar o histórico de participação em guerras de um clã do Clash Royale.

## Configuração

Para que o dashboard funcione, você precisa de uma chave de API da Supercell. Você pode obter uma em [https://developer.clashroyale.com/](https://developer.clashroyale.com/).

Depois de obter sua chave, você precisa definir a variável de ambiente `CLASH_ROYALE_API_KEY`.

**No Windows:**

```
setx CLASH_ROYALE_API_KEY "sua_chave_de_api"
```

**No Linux ou macOS:**

```
export CLASH_ROYALE_API_KEY="sua_chave_de_api"
```

## Como executar

1.  Instale as dependências: `pip install -r requirements.txt`
2.  Execute o servidor: `python app.py`
3.  Acesse o dashboard em `http://127.0.0.1:5000`

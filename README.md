# Dashboard de Guerra de Clãs do Clash Royale

Este projeto é um dashboard web para visualizar o histórico de participação em guerras de um clã específico do Clash Royale. A atualização dos dados é feita manualmente para evitar o uso excessivo da API.

## 1. Configuração Inicial

Antes de usar o dashboard, você precisa configurar sua chave da API da Supercell.

### 1.1. Obtenha sua Chave da API

- Acesse [https://developer.clashroyale.com/](https://developer.clashroyale.com/) e crie uma conta.
- Crie uma nova chave de API e copie o valor.

### 1.2. Defina a Variável de Ambiente

Você **precisa** definir a chave da API como uma variável de ambiente chamada `CLASH_ROYALE_API_KEY`.

- **No Windows (Prompt de Comando):**
  ```sh
  setx CLASH_ROYALE_API_KEY "SUA_CHAVE_DE_API_AQUI"
  ```
  *Lembre-se de fechar e reabrir o terminal após executar este comando.*

- **No Linux ou macOS:**
  ```sh
  export CLASH_ROYALE_API_KEY="SUA_CHAVE_DE_API_AQUI"
  ```
  *Para tornar a variável permanente, adicione esta linha ao seu arquivo `~/.bashrc` ou `~/.zshrc`.*

### 1.3. Instale as Dependências

Com o Python instalado, instale as bibliotecas necessárias:

```sh
pip install -r requirements.txt
```

## 2. Como Usar o Dashboard

O processo é dividido em duas etapas: **atualizar os dados** e **visualizar o dashboard**.

### Etapa 1: Atualizar os Dados

Para buscar os dados mais recentes da API da Supercell e gerar o relatório, execute o script de atualização:

```sh
python run_update.py
```

- Este comando executa todo o processo: baixa os dados, os processa e cria o arquivo `relatorio_guerra.html`.
- Execute este script **uma vez por dia** ou sempre que quiser atualizar as informações.

### Etapa 2: Visualizar o Dashboard

Após atualizar os dados, inicie o servidor web local para ver o relatório:

```sh
python app.py
```

- O servidor ficará ativo.
- Abra seu navegador e acesse [http://127.0.0.1:5000](http://127.0.0.1:5000) para ver o dashboard.

---

**Importante:** Não é necessário executar `run_update.py` toda vez que você quiser ver o dashboard, apenas quando desejar obter os dados mais recentes do jogo.

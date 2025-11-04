# Dashboard de Guerra de Clãs do Clash Royale

Este projeto é um dashboard web para visualizar o histórico de participação em guerras de um clã específico do Clash Royale. A atualização dos dados é feita manualmente para evitar o uso excessivo da API.

## 1. Configuração Inicial

Antes de usar o dashboard, você precisa configurar sua chave da API da Supercell e a tag do seu clã.

### 1.1. Obtenha sua Chave da API

- Acesse [https://developer.clashroyale.com/](https://developer.clashroyale.com/) e crie uma conta.
- Crie uma nova chave de API e copie o valor.

### 1.2. Defina as Variáveis de Ambiente

Você **precisa** definir duas variáveis de ambiente: uma para a chave da API e outra para a tag do seu clã.

- **`CLASH_ROYALE_API_KEY`**: Sua chave secreta da API.
- **`CLAN_TAG`**: A tag do seu clã (ex: `#ABC123`).

**No Windows (Prompt de Comando):**
```sh
setx CLASH_ROYALE_API_KEY "SUA_CHAVE_DE_API_AQUI"
setx CLAN_TAG "SUA_CLAN_TAG_AQUI"
```
*Lembre-se de fechar e reabrir o terminal após executar este comando para que as alterações tenham efeito.*

**No Linux ou macOS:**
```sh
export CLASH_ROYALE_API_KEY="SUA_CHAVE_DE_API_AQUI"
export CLAN_TAG="SUA_CLAN_TAG_AQUI"
```
*Para tornar as variáveis permanentes, adicione estas linhas ao seu arquivo `~/.bashrc` ou `~/.zshrc`.*

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

## 3. Resolvendo Problemas

### "Nenhum dado de jogador encontrado"

Se o dashboard exibir uma tela de diagnóstico em vez da tabela de jogadores, isso significa que a atualização foi concluída, mas não encontrou dados de guerra para analisar.

**Como funciona o diagnóstico:**
A própria página do dashboard mostrará um **log detalhado** da última tentativa de atualização. Leia este log para entender a causa do problema.

**Causas mais comuns:**
1.  **Clan Tag Incorreta:** A `CLAN_TAG` definida nas suas variáveis de ambiente está errada. Verifique se você digitou a tag corretamente, incluindo o `#`.
2.  **Sem Guerra Ativa ou Histórico Vazio:** O clã pode não estar participando de uma guerra no momento, e o histórico de guerras recentes também não contém dados de participantes.
3.  **Erro na API:** A API da Supercell pode estar temporariamente offline ou sua chave (`CLASH_ROYALE_API_KEY`) pode ser inválida.

**O que fazer:**
- Verifique o log na página de diagnóstico.
- Confirme se suas variáveis de ambiente `CLAN_TAG` e `CLASH_ROYALE_API_KEY` estão corretas.
- Tente executar `python run_update.py` novamente mais tarde.

# Documentação da Lógica de Processamento de Dados

Este documento detalha a lógica utilizada pelo script `src/process_data.py` para analisar os dados da guerra atual e do histórico de guerras do clã, baixados da API da Supercell.

## A Causa do Problema no Histórico (Lógica Antiga)

Inicialmente, o script não conseguia processar os dados dos jogadores do histórico de guerras, mesmo quando o clã era encontrado nos registros. O log mostrava "Processando 0 participante(s)".

A causa do erro era uma interpretação incorreta da estrutura do arquivo `riverracelog.json` (o histórico).

**A Lógica Antiga (Incorreta):**

1.  O script iterava por cada "guerra" (`item`) no histórico.
2.  Dentro de cada guerra, ele iterava pela lista de clãs (`standings`).
3.  Quando encontrava o clã correto (comparando a tag), ele tentava encontrar a lista de `participants` no **mesmo nível** do objeto `clan`.
4.  **O erro:** A lista de participantes não existe nesse nível. Ela está *dentro* do objeto `clan`. O script procurava em `standings[i]['participants']`, quando o caminho correto era `standings[i]['clan']['participants']`.
5.  Como resultado, ele sempre encontrava uma lista vazia, e nenhum jogador era processado.

## A Solução (Lógica Nova e Corrigida)

A correção foi ajustar o caminho de busca para refletir a estrutura hierárquica correta do JSON.

**A Lógica Nova (Correta):**

1.  O script itera por cada "guerra" (`item`) e depois pelos `standings`, exatamente como antes.
2.  Quando encontra o `standing` que contém o clã correto, ele primeiro acessa o objeto `clan` dentro desse `standing`.
3.  Em seguida, ele busca a lista de `participants` **dentro** desse objeto `clan`.
4.  Com o caminho correto (`standings[i]['clan']['participants']`), o script agora encontra a lista correta de jogadores e consegue processar o histórico de participação de cada um.

---

## Estrutura dos Arquivos de Dados

O script consulta dois arquivos principais no diretório `data/`.

### 1. Guerra Atual (`current_war.json`)

Este arquivo contém os dados da guerra em andamento. É a fonte primária para determinar a lista de membros atuais do clã.

-   **Caminho para a lista de jogadores:** `['clan']['participants']`
-   **Campos Relevantes por Jogador:**
    -   `tag`: O identificador único do jogador.
    -   `name`: O nome do jogador.

### 2. Histórico de Guerras (`riverracelog.json`)

Este arquivo contém uma lista das últimas guerras do rio. É usado para construir o histórico de desempenho dos jogadores.

-   **Caminho para a lista de jogadores:** `['items'][*]['standings'][*]['clan']['participants']`
    -   `items`: Uma lista, onde cada item é uma guerra. `[*]` significa que o script itera sobre cada guerra.
    -   `standings`: Uma lista, dentro de cada guerra, com os clãs participantes. `[*]` significa que o script itera para encontrar o clã correto.
    -   `clan`: O objeto que contém os dados do clã, incluindo os participantes.
    -   `participants`: A lista final de jogadores daquele clã naquela guerra.
-   **Campos Relevantes por Jogador no Histórico:**
    -   `tag`: O identificador único do jogador (usado para cruzar com a lista de membros atuais).
    -   `name`: O nome do jogador.
    -   `decksUsed`: O número de decks que o jogador usou naquela guerra. Este é o principal indicador de desempenho.
-   **Campos Relevantes da Guerra:**
    -   `createdDate`: A data em que a semana da guerra começou. Usamos essa data para rotular as colunas do relatório (ex: "Guerra -2").

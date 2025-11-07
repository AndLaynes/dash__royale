# Metodologia e Arquitetura do Projeto Dashboard do Clã

Este documento detalha o funcionamento interno, a arquitetura e a lógica por trás do projeto do dashboard do Clash Royale. O objetivo é fornecer uma visão clara de como os dados são coletados, processados e apresentados, servindo como uma referência técnica completa.

---

### 1. Filosofia e Arquitetura Geral

O projeto foi construído com uma filosofia **"local-first"**, projetada para ser robusta, segura e fácil de manter.

-   **Local-First**: Todo o processamento pesado e a comunicação com a API da Supercell ocorrem no seu computador local. O resultado final é um único arquivo HTML estático (`index.html`), que é o único artefato enviado para a internet. Isso evita a exposição de chaves de API em servidores web e reduz a complexidade.
-   **Orquestração Centralizada**: O processo completo é gerenciado por um único script, o `run_update.py`. Isso garante que as etapas sejam sempre executadas na ordem correta e facilita a depuração, pois há um único ponto de entrada.

O fluxo de trabalho é dividido em três etapas principais, executadas sequencialmente pelo `run_update.py`:

1.  **Coleta de Dados**: `src/get_data.py`
2.  **Processamento e Análise**: `src/process_data.py`
3.  **Geração do Relatório**: `src/generate_html_report.py`

---

### 2. Etapa 1: Coleta de Dados (`src/get_data.py`)

Este script é o responsável exclusivo por se comunicar com a API da Supercell.

-   **Autenticação**: Ele utiliza a variável de ambiente `CLASH_ROYALE_API_KEY` para se autenticar. No seu caso, o script foi configurado para ler esta chave diretamente do registro do Windows, uma particularidade do seu ambiente local.
-   **Endpoints da API Utilizados**:
    -   `v1/clans/{CLAN_TAG}/currentriverrace`: Usado para obter os dados da **guerra atual**. A informação mais importante extraída daqui é a **lista de participantes do clã no momento da consulta**. Esses dados são salvos no arquivo `data/current_war.json`.
    -   `v1/clans/{CLAN_TAG}/riverracelog`: Usado para obter o **histórico completo** de todas as guerras passadas. O script foi projetado para **baixar todos os registros disponíveis**, lidando com a paginação da API para garantir que nenhum dado histórico seja perdido. O resultado é salvo em `data/riverracelog.json`.

---

### 3. Etapa 2: Processamento e Análise (`src/process_data.py`)

Este é o componente mais complexo do projeto, onde os dados brutos são transformados em informação útil.

#### a. Definição da Lista de Membros do Clã

A primeira tarefa é determinar a lista de jogadores que devem aparecer no relatório.

1.  **Fonte Primária**: O script tenta ler a lista de participantes do arquivo `data/current_war.json`. Se o clã estiver em guerra, esta é a fonte de verdade sobre quem são os membros atuais.
2.  **Fonte Secundária (Fallback)**: Se o clã não estiver em guerra (`state` é `notInWar`) ou o arquivo não existir, o script utiliza um plano B. Ele abre o `data/riverracelog.json`, pega a guerra mais recente do histórico e usa a lista de participantes daquela guerra como base para a lista de membros.

#### b. Processamento do Histórico de Guerras

Esta é a lógica central que alimenta a tabela do dashboard.

1.  **Leitura do Histórico**: O script carrega o arquivo `data/riverracelog.json`.
2.  **Iteração e Mapeamento**: Ele itera sobre cada guerra registrada no histórico.
3.  **Busca do Clã**: Dentro de cada guerra, ele percorre a lista de `standings` até encontrar o seu clã, comparando o `CLAN_TAG` do seu ambiente com o tag registrado na guerra.
4.  **Extração de Participantes (Lógica Corrigida)**: Uma vez encontrado o clã, ele navega para o caminho `['clan']['participants']` dentro do objeto do clã. Este passo é crucial e foi o local do bug anterior.
5.  **Construção do Dicionário de Desempenho**: Para cada participante encontrado, ele armazena em um grande dicionário Python: o `tag` do jogador, a `data` da guerra e o número de `decksUsed`. Ao final, este dicionário contém o histórico de desempenho de cada jogador que já participou de uma guerra pelo clã.

#### c. Montagem da Tabela Final (Pandas DataFrame)

1.  **Criação da Tabela**: Uma tabela (DataFrame) é criada usando a biblioteca Pandas, com os nomes e tags dos membros atuais do clã.
2.  **Adição das Colunas de Guerra**: O script adiciona 5 colunas: `Última Guerra`, `Guerra -2`, `Guerra -3`, `Guerra -4`, e `Guerra -5`.
3.  **Preenchimento dos Dados**: Para cada jogador na tabela e para cada coluna de guerra, ele consulta o dicionário de desempenho criado anteriormente. Se houver um registro para aquele jogador naquela data, ele preenche a célula com o número de decks usados. Caso contrário (jogador não participou ou não estava no clã), ele preenche com `0`.

#### d. Cálculo do "Player Status"

Com a tabela preenchida, uma nova coluna `Player Status` é adicionada. O script aplica a regra de negócio definida:
-   **Campeão**: Usou 16 decks nas últimas 2 guerras.
-   **Ok**: Usou entre 12 e 15 decks nas últimas 2 guerras.
-   **Verificar**: Todos os outros casos.

O resultado final deste script é um arquivo Excel (`relatorio_participacao_guerra.xlsx`) e um arquivo JSON (`war_season_ids.json`) que é usado no template HTML.

---

### 4. Etapa 3: Geração do Relatório HTML (`src/generate_html_report.py`)

Esta etapa final transforma os dados processados em uma página web visual e interativa.

-   **Motor de Template (Jinja2)**: O script usa a biblioteca Jinja2 para renderizar os templates HTML. Ele funciona como uma "mala direta": pega um template com marcadores (ex: `{{ nome_do_jogador }}`) e substitui esses marcadores pelos dados reais da tabela processada.
-   **Estrutura dos Templates**:
    -   `src/templates/base.html`: Este é o "molde" da página. Contém o `<html>`, `<head>`, `<body>`, os estilos CSS que definem o tema escuro, as cores, as fontes e os links para os arquivos JavaScript.
    -   `src/templates/report_template.html`: Este é o conteúdo específico da página do relatório. Ele contém a estrutura da tabela, a caixa de definição do status e o código que itera sobre a lista de jogadores e cria uma linha (`<tr>`) para cada um, preenchendo as células (`<td>`) com os dados correspondentes.
-   **Interatividade (DataTables.js)**: A tabela no `index.html` gerado não é uma tabela HTML simples. Após a página ser carregada, um script JavaScript da biblioteca **DataTables.js** é executado. Ele "melhora" a tabela, adicionando funcionalidades avançadas como:
    -   **Ordenação**: Clicar nos cabeçalhos para ordenar.
    -   **Pesquisa**: Um campo de busca para filtrar jogadores.
    -   **Paginação**: Dividir a tabela em várias páginas.
    -   **Exportação**: Botões para exportar os dados para PDF ou Excel.

O produto final de todo o processo é o arquivo `index.html`, uma página web autônoma, pronta para ser publicada.

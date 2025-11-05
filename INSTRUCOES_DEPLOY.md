# Guia Completo: Como Atualizar o Dashboard Online

Este arquivo contém o processo completo e simplificado para atualizar seu site do dashboard. O fluxo de trabalho é sempre o mesmo: **Sincronizar, Gerar e Publicar.**

**Seu branch de trabalho principal é:** `feature-data-collection-script`
**Seu site está publicado em:** `https://andlaynes.github.io/dash__royale/`

---

### Processo de Atualização (Passo a Passo)

Execute os comandos abaixo no seu terminal (PowerShell, Git Bash, etc.) sempre que quiser atualizar o site com as novas funcionalidades do projeto e os dados mais recentes do Clash Royale.

Você pode copiar e colar o bloco de código inteiro de uma só vez.

```bash
# PASSO 1: SINCRONIZAR O CÓDIGO
# Garante que você está no seu branch de trabalho e baixa as últimas atualizações que foram feitas no projeto.
git checkout feature-data-collection-script
git pull origin feature-data-collection-script

# PASSO 2: GERAR O NOVO RELATÓRIO
# Executa o script principal para baixar os dados mais recentes da Supercell e criar o arquivo `index.html`.
python run_update.py

# PASSO 3: PUBLICAR O NOVO SITE
# Pega o `index.html` recém-criado, o envia de forma segura para o branch `gh-pages` e limpa o ambiente.
git checkout --orphan gh-pages-temp
git add --force index.html
git commit -m "Deploy: Atualiza o site com a versão mais recente"
git push -f origin gh-pages-temp:gh-pages
git checkout feature-data-collection-script
git branch -D gh-pages-temp
```

---

### Como Isso Funciona?

*   **Passo 1 (Sincronizar):** `git pull` baixa qualquer alteração que eu tenha feito (como melhorias de layout, correção de bugs, etc.) para o seu computador.
*   **Passo 2 (Gerar):** `python run_update.py` cria o arquivo `index.html`, que é a "fotografia" mais recente do seu dashboard, já com as novas funcionalidades e os dados atuais do clã.
*   **Passo 3 (Publicar):** Os comandos `git` seguintes pegam **apenas e somente** esse arquivo `index.html` e o colocam no branch `gh-pages`, que é o branch que o seu site lê.

Após executar o último comando, espere um ou dois minutos. Ao recarregar a página do seu site, as novas alterações já estarão visíveis.

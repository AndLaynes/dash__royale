# Guia Completo: Como Atualizar o Dashboard Online (Versão Corrigida)

Este arquivo contém o processo **corrigido e final** para atualizar seu site. Um bug anterior no script de publicação fazia com que todos os arquivos do projeto fossem enviados, em vez de apenas o relatório. Este guia resolve isso.

O fluxo de trabalho continua o mesmo: **Sincronizar, Gerar e Publicar.**

**Seu branch de trabalho principal é:** `feature-data-collection-script`
**Seu site está publicado em:** `https://andlaynes.github.io/dash__royale/`

---

### Processo de Atualização (Passo a Passo Corrigido)

Copie e cole o bloco de código abaixo **inteiro** no seu terminal. Ele foi atualizado para garantir que apenas e somente o `index.html` seja publicado.

```bash
# PASSO 1: SINCRONIZAR O CÓDIGO
# Garante que você está no seu branch de trabalho e baixa as últimas atualizações.
git checkout feature-data-collection-script
git pull origin feature-data-collection-script

# PASSO 2: GERAR O NOVO RELATÓRIO
# Executa o script para criar o `index.html` mais recente.
python run_update.py

# PASSO 3: PUBLICAR O NOVO SITE (COM CORREÇÃO)
# Cria um ambiente limpo, publica APENAS o `index.html` e retorna ao seu branch de trabalho.
git checkout --orphan gh-pages-temp
git add --force index.html
git commit -m "Deploy: Atualiza o site com a versão mais recente"
git push -f origin gh-pages-temp:gh-pages
git checkout feature-data-collection-script
git branch -D gh-pages-temp
```

---

### Se o Problema Persistir (Cache do Git)

O Git pode, às vezes, manter um "cache" de arquivos. Se, mesmo após usar o script acima, você notar que outros arquivos além do `index.html` foram publicados, use esta versão **ainda mais robusta** do PASSO 3.

```bash
# PASSO 3 ALTERNATIVO: PUBLICAR LIMPANDO O CACHE
git checkout --orphan gh-pages-temp
# O comando abaixo limpa forçadamente qualquer arquivo que o Git tenha em memória.
git rm -rf --cached .
git add --force index.html
git commit -m "Deploy: Atualiza o site com a versão mais recente (limpando cache)"
git push -f origin gh-pages-temp:gh-pages
git checkout feature-data-collection-script
git branch -D gh-pages-temp
```

Após executar a publicação, espere um ou dois minutos e recarregue a página do seu site para ver as alterações. Peço desculpas novamente pelos problemas anteriores!

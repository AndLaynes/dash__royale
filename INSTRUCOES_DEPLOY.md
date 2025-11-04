# Instruções Corrigidas para Publicar o Dashboard no GitHub Pages

Este guia (agora corrigido) explica como publicar e atualizar seu dashboard de forma segura, enviando **apenas e somente o arquivo `index.html`** para a internet. O erro anterior, que publicava outros arquivos como o `README.md`, foi resolvido.

O processo utiliza um método seguro que cria um branch "órfão" — um branch totalmente limpo e independente — para garantir que apenas o relatório seja publicado.

---

### Configuração Inicial (Você só faz isso uma vez)

1.  **Siga os Passos de Atualização:**
    *   Execute pela primeira vez os passos descritos na seção **"Como Atualizar o Dashboard Online"** abaixo. Isso irá criar e enviar o branch `gh-pages` para o seu repositório no GitHub.

2.  **Ative o GitHub Pages no Seu Repositório:**
    *   Vá para a página do seu repositório no GitHub.
    *   Clique em **"Settings"** (Configurações).
    *   No menu lateral esquerdo, clique em **"Pages"**.
    *   Em "Source", selecione o branch `gh-pages` e a pasta `/ (root)`.
    *   Clique em **"Save"**.

O GitHub levará alguns minutos para publicar seu site. O link ficará visível nessa mesma página e terá o formato: `https://<seu-usuario>.github.io/<nome-do-repositorio>/`.

---

### Como Atualizar o Dashboard Online (Processo Corrigido)

Siga estes passos no seu terminal (como o PowerShell ou Git Bash) sempre que quiser atualizar o relatório que está online.

**Passo 1: Gere o Relatório Mais Recente**
Este passo continua o mesmo. Ele gera o arquivo `index.html` na raiz do seu projeto.

```bash
python run_update.py
```

**Passo 2: Publique Apenas o Relatório**
Os comandos abaixo foram redesenhados para isolar completamente o `index.html` e enviá-lo para o branch `gh-pages` sem nenhum outro arquivo do projeto.

```bash
# Cria um branch temporário e totalmente limpo, sem nenhum arquivo do projeto.
git checkout --orphan gh-pages-temp

# Adiciona FORÇADAMENTE apenas o arquivo index.html.
# O '--force' é necessário porque o index.html está no seu .gitignore.
git add --force index.html

# Cria um registro da atualização.
git commit -m "Deploy: Atualiza relatório do dashboard"

# Envia este branch limpo para o branch 'gh-pages' do GitHub.
# Isto irá substituir completamente o que estava lá antes. É seguro e desejado.
git push -f origin gh-pages-temp:gh-pages

# Volta para o seu branch de trabalho principal (ex: 'main' ou 'master').
# Se seu branch principal tiver outro nome, ajuste o comando abaixo.
git checkout main

# Deleta o branch temporário do seu computador para manter tudo limpo.
git branch -D gh-pages-temp
```

**Pronto!** Agora, com certeza, apenas o `index.html` foi publicado. Após alguns minutos, suas atualizações estarão visíveis no link do seu GitHub Pages. Peço desculpas novamente pelo erro anterior!

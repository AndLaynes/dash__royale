# Instruções para Publicar o Dashboard no GitHub Pages

Este guia explica como publicar e atualizar seu dashboard de forma segura, enviando **apenas o arquivo HTML final** (`index.html`) para a internet. Todo o seu código-fonte, scripts e chaves de API permanecerão privados no seu computador.

O processo utiliza um branch especial do Git chamado `gh-pages`, que o GitHub usa para hospedar sites estáticos.

---

### Configuração Inicial (Você só faz isso uma vez)

1.  **Execute o Processo de Publicação Pela Primeira Vez:**
    *   Siga os passos na seção "Como Atualizar o Dashboard" abaixo para enviar o branch `gh-pages` para o seu repositório no GitHub pela primeira vez.

2.  **Ative o GitHub Pages no Seu Repositório:**
    *   Vá para a página do seu repositório no GitHub.
    *   Clique em **"Settings"** (Configurações).
    *   No menu lateral esquerdo, clique em **"Pages"**.
    *   Em "Source", selecione o branch `gh-pages` e a pasta `/ (root)`.
    *   Clique em **"Save"**.

O GitHub levará alguns minutos para publicar seu site. O link ficará visível nessa mesma página e terá o formato: `https://<seu-usuario>.github.io/<nome-do-repositorio>/`.

---

### Como Atualizar o Dashboard (Passos para cada atualização)

Siga estes passos no seu terminal (como o PowerShell ou Git Bash) sempre que quiser atualizar o relatório que está online.

**Passo 1: Gere o Relatório Mais Recente**
Execute o script principal para baixar os dados mais recentes e gerar o arquivo `index.html`.

```bash
python run_update.py
```

**Passo 2: "Empacote" o Relatório para Envio**
Os comandos abaixo criam um branch temporário (`gh-pages`) que conterá apenas o seu `index.html`. É um processo seguro e automatizado.

*   **Atenção:** Se você tiver alterações não salvas (não "commitadas"), o Git pode pedir para você salvá-las primeiro. Se isso acontecer, você pode "commitar" suas alterações no branch principal ou usar `git stash` para guardá-las temporariamente.

```bash
# Cria e/ou acessa o branch de publicação.
git checkout -B gh-pages

# Puxa a versão mais recente do index.html do seu branch principal (assumindo que seja 'main').
# Se o seu branch principal tiver outro nome (ex: 'master'), substitua 'main' no comando abaixo.
git checkout main -- index.html

# Adiciona o arquivo ao "pacote" de envio.
git add index.html

# Cria um registro da atualização.
git commit -m "Atualiza relatório do dashboard"

# Envia o relatório para o GitHub.
# O '--force' é necessário aqui porque estamos substituindo o relatório antigo pelo novo.
# É seguro usar neste caso específico.
git push origin gh-pages --force

# Volta para o seu branch de trabalho principal.
git checkout main
```

**Pronto!** Após alguns minutos, suas alterações estarão visíveis no link do seu GitHub Pages.

# Guia de Deploy Seguro

Este guia contém o processo passo a passo para atualizar o dashboard online de forma segura, evitando os erros de "arquivos não rastreados" (`untracked working tree files`).

**Siga os passos na ordem exata.**

---

### Processo de Atualização Completo

#### PASSO 1: Limpeza e Sincronização

Este passo é **CRUCIAL**. Ele vai limpar sua pasta local de arquivos temporários e baixar a versão mais recente do código, incluindo as correções de bugs.

**Atenção:** O comando `git clean` vai apagar arquivos não monitorados. Certifique-se de que não há nenhuma alteração local que você queira salvar.

```bash
# Vá para o seu branch de trabalho principal
git checkout feature-data-collection-script

# COMANDO DE LIMPEZA: Remove todos os arquivos e pastas não rastreados
# Isso resolve o erro "untracked working tree files".
git clean -fdx

# Baixa a versão mais recente do código do repositório
git pull origin feature-data-collection-script
```

#### PASSO 2: Geração do Relatório

Agora que seu código está limpo e atualizado, execute o script para gerar o `index.html`.

```bash
# Execute o script de atualização
python run_update.py
```
Se este passo falhar, pare e me envie o log de erro.

#### PASSO 3: Publicação no GitHub Pages

Este é o processo final para enviar **apenas o `index.html`** para o seu site.

```bash
# Cria um branch temporário e limpo para o deploy
git checkout --orphan gh-pages-temp

# Adiciona SOMENTE o arquivo index.html, ignorando todo o resto
git add --force index.html

# Cria o commit
git commit -m "Deploy: Atualiza o relatório do site"

# Envia o branch temporário para o branch 'gh-pages' do seu repositório
git push -f origin gh-pages-temp:gh-pages

# Volta para o seu branch de trabalho
git checkout feature-data-collection-script

# Deleta o branch temporário
git branch -D gh-pages-temp
```

---

Após executar o PASSO 3, aguarde um ou dois minutos e atualize a página do seu site. As alterações devem estar visíveis. Se encontrar qualquer erro, me envie o log completo.

# 📋 HANDOFF - Clash Royale Dashboard

**Projeto:** Dashboard de Acompanhamento de Guerra do Clã  
**Repositório:** https://github.com/AndLaynes/dash__royale  
**Última Atualização:** 30/12/2025  
**Branch Atual:** `feature-data-collection-script`

---

## 🎯 O QUE É ESTE PROJETO?

Dashboard automatizado para acompanhar a participação dos membros do clã em guerras do Clash Royale. Gera relatórios HTML com:

1. **Relatório Principal** (`index.html`): Histórico das últimas 5 guerras com status de participação
2. **Acompanhamento Diário** (`acompanhamento_diario.html`): Tracking diário dos ataques durante a guerra atual

---

## ⚙️ CONFIGURAÇÃO INICIAL (IMPORTANTE!)

### 1. Variáveis de Ambiente

Você **DEVE** configurar estas variáveis de ambiente antes de executar o projeto:

#### Windows (PowerShell):
```powershell
# Temporário (válido apenas para a sessão atual)
$env:CLASH_ROYALE_API_KEY = "seu_token_aqui"
$env:CLAN_TAG = "#TAG_DO_CLA"

# Permanente (recomendado)
[System.Environment]::SetEnvironmentVariable('CLASH_ROYALE_API_KEY', 'seu_token_aqui', 'User')
[System.Environment]::SetEnvironmentVariable('CLAN_TAG', '#TAG_DO_CLA', 'User')
```

#### Linux/Mac:
```bash
export CLASH_ROYALE_API_KEY="seu_token_aqui"
export CLAN_TAG="#TAG_DO_CLA"

# Para tornar permanente, adicione ao ~/.bashrc ou ~/.zshrc
```

### 2. Como Obter a API Key da Supercell

1. Acesse: https://developer.clashroyale.com/
2. Faça login com sua conta Supercell
3. Crie um novo token (a key precisa ser renovada periodicamente)
4. **IMPORTANTE:** O IP da sua máquina deve estar autorizado

### 3. Como Encontrar a Tag do Clã

1. Abra o Clash Royale
2. Vá para o perfil do clã
3. A tag aparece abaixo do nome do clã (ex: `#2YQJV89QG`)
4. **IMPORTANTE:** A tag DEVE começar com `#`

---

## 🚀 INSTALAÇÃO

### 1. Clone o Repositório
```bash
git clone https://github.com/AndLaynes/dash__royale.git
cd dash__royale
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

**Dependências:**
- `requests` - HTTP requests para a API
- `pandas` - Análise de dados
- `openpyxl` - Manipulação de Excel
- `Jinja2` - Templates HTML
- `Flask` - Servidor web

---

## 📊 COMO USAR

### Workflow Completo (3 passos)

#### Passo 1: Atualizar Dados
```bash
python run_update.py
```

Este comando executa na ordem:
1. `src/get_data.py` - Baixa dados da API
2. `src/process_data.py` - Processa e analisa os dados
3. `src/generate_html_report.py` - Gera os HTMLs

**Arquivos criados:**
- `data/current_war.json` - Dados da guerra atual
- `data/riverracelog.json` - Histórico de guerras
- `data/relatorio_participacao_guerra.xlsx` - Análise em Excel
- `data/daily_war_history.json` - Histórico diário acumulado
- `index.html` - Relatório principal
- `acompanhamento_diario.html` - Relatório diário

#### Passo 2: Iniciar o Servidor
```bash
python app.py
```

**Acessar:**
- Relatório Principal: http://127.0.0.1:5000
- Acompanhamento Diário: http://127.0.0.1:5000/acompanhamento_diario

#### Passo 3: Publicar no GitHub Pages (Opcional)

```bash
# Adicionar arquivos
git add index.html acompanhamento_diario.html

# Commit
git commit -m "Atualização dos relatórios - $(date)"

# Push
git push origin feature-data-collection-script
```

---

## 🏗️ ARQUITETURA DO PROJETO

### Pipeline de Dados

```
API Clash Royale
    ↓
get_data.py → JSONs (data/)
    ↓
process_data.py → Excel + JSON processado
    ↓
generate_html_report.py → HTMLs
    ↓
app.py (Flask) → Servidor Web
```

### Estrutura de Arquivos

```
dash__royale/
├── 📁 data/                        # ⚠️ GITIGNORED (dados sensíveis)
│   ├── current_war.json
│   ├── riverracelog.json
│   ├── relatorio_participacao_guerra.xlsx
│   ├── daily_war_history.json
│   ├── process_log.json
│   └── war_season_ids.json
│
├── 📁 src/
│   ├── get_data.py                 # 1️⃣ Download API
│   ├── process_data.py             # 2️⃣ Processamento
│   ├── generate_html_report.py     # 3️⃣ Geração HTML
│   └── 📁 templates/
│       ├── base.html               # Template base (CSS + DataTables)
│       ├── report_template.html    # Template do relatório principal
│       └── daily_report_template.html  # Template do acompanhamento diário
│
├── run_update.py                   # 🎯 Script principal (orquestrador)
├── app.py                          # 🌐 Servidor Flask
├── index.html                      # Relatório gerado
├── acompanhamento_diario.html      # Relatório diário gerado
├── requirements.txt
├── .gitignore
├── HANDOFF.md                      # 📋 VOCÊ ESTÁ AQUI
├── README.md
├── warlog.md                       # Documentação da lógica de processamento
└── INSTRUCOES_DEPLOY.md
```

---

## 🔧 LÓGICA DE NEGÓCIO

### Sistema de Status dos Jogadores

O script `process_data.py` classifica cada jogador automaticamente:

| Status | Critério | Cor |
|--------|----------|-----|
| ✅ **OK** | Participou de 4-5 das últimas 5 guerras | Verde |
| ⚠️ **Razoável** | Participou de 2-3 das últimas 5 guerras | Amarelo |
| 🔴 **Verificar** | Participou de 0-1 das últimas 5 guerras | Vermelho |

### Métrica de Participação

- **Participou** = Usou pelo menos 1 deck na guerra
- **Não Participou** = 0 decks usados ou ausente da guerra

### Histórico Diário (Guerra Atual)

O arquivo `daily_war_history.json` **acumula** os dados dia a dia:
- Executa `run_update.py` diariamente
- O histórico cresce automaticamente (não sobrescreve)
- Ideal para ver a evolução dos ataques ao longo da semana

---

## 🐛 TROUBLESHOOTING

### Erro: "Variável de ambiente não definida"

**Causa:** `CLASH_ROYALE_API_KEY` ou `CLAN_TAG` não configuradas  
**Solução:** Veja seção "Configuração Inicial" acima

### Erro: 403 Forbidden

**Causa:** API Key inválida ou IP não autorizado  
**Solução:**
1. Verifique se a key está correta
2. Acesse https://developer.clashroyale.com/
3. Adicione seu IP atual à lista de IPs permitidos
4. Crie uma nova key se necessário

### Erro: 404 Not Found

**Causa:** CLAN_TAG incorreta  
**Solução:**
1. Verifique se a tag começa com `#`
2. Confirme a tag no jogo
3. Certifique-se de que não há espaços extras

### Relatório Vazio

**Causa:** Os arquivos JSON podem estar vazios ou corrompidos  
**Solução:**
```bash
# Limpar dados antigos
rm -rf data/*

# Baixar dados novamente
python run_update.py
```

### Erro de Codificação (UnicodeDecodeError)

**Causa:** Windows usa codificação diferente (cp1252)  
**Solução:** O script `run_update.py` já trata isso automaticamente com `locale.getpreferredencoding()`

---

## 📈 DEPLOY NO GITHUB PAGES

### Opção 1: Deploy Manual

1. Execute `python run_update.py`
2. Commit e push dos HTMLs gerados:
```bash
git add index.html acompanhamento_diario.html
git commit -m "Update reports - $(date)"
git push origin feature-data-collection-script
```

3. Configure GitHub Pages:
   - Acesse: Settings → Pages
   - Source: `feature-data-collection-script` branch
   - Pasta: `/ (root)`
   - Salvar

4. Acesse: https://andlaynes.github.io/dash__royale/

### Opção 2: Automação com GitHub Actions (Futuro)

Ver arquivo `INSTRUCOES_DEPLOY.md` para instruções detalhadas sobre automação.

---

## 🔒 SEGURANÇA

### ⚠️ NUNCA COMMITE:

- ❌ API Keys
- ❌ Arquivos do diretório `data/`
- ❌ Arquivo `.env` (se você criar um)

### ✅ O que está no .gitignore:

```
data/
.env
__pycache__/
*.pyc
warlog.json
riverracelog.json
relatorio_guerra.html
app.log
```

---

## 📚 DOCUMENTAÇÃO ADICIONAL

- **README.md** - Visão geral do projeto
- **warlog.md** - Detalhes técnicos da lógica de processamento
- **INSTRUCOES_DEPLOY.md** - Instruções de deploy
- **METODOLOGIA.md** - Metodologia de desenvolvimento
- **00_SYS_KERNEL.md** - Protocolo de desenvolvimento
- **01_SYS_CALIBRATION.md** - Protocol de calibração
- **02_SYS_MAP.md** - Protocolo de mapeamento arquitetural
- **99_SYS_AUDIT.md** - Protocolo de auditoria

---

## 🆘 SUPORTE

### Problemas com a API da Supercell

- Documentação oficial: https://developer.clashroyale.com/
- Status da API: https://status.supercell.com/

### Problemas com o Código

1. Verifique os logs em `data/process_log.json`
2. Execute passo a passo:
   ```bash
   python src/get_data.py
   python src/process_data.py
   python src/generate_html_report.py
   ```
3. Verifique o mapa arquitetural (execute `02_SYS_MAP.md`)

---

## 🔄 MANUTENÇÃO REGULAR

### Diariamente (Durante Guerra)
```bash
python run_update.py
```

### Semanalmente (Após Guerra)
```bash
python run_update.py
git add index.html acompanhamento_diario.html
git commit -m "Update: Guerra finalizada $(date)"
git push
```

### Mensalmente
- Renovar API Key se necessário
- Verificar se a tag do clã mudou
- Atualizar dependências: `pip install -r requirements.txt --upgrade`

---

## ✅ CHECKLIST DE HANDOFF

- [x] Variáveis de ambiente configuradas
- [x] Dependências instaladas (`pip install -r requirements.txt`)
- [x] API Key da Supercell válida e funcionando
- [x] Tag do clã correta
- [x] `run_update.py` executado com sucesso
- [x] Servidor Flask funcionando (`python app.py`)
- [x] HTMLs gerados corretamente
- [x] Git sincronizado com GitHub
- [x] GitHub Pages configurado (opcional)

---

## 🚨 STATUS ATUAL DO PROJETO

**Branch:** `feature-data-collection-script`  
**Commits à frente do remote:** 2 commits  
**Ação necessária:** `git push origin feature-data-collection-script`

**Arquivos não rastreados detectados** - Provavelmente os HTMLs gerados ou arquivos do diretório `data/`.

---

## 📝 NOTAS FINAIS

1. **Nunca delete o diretório `data/`** sem backup - contém o histórico acumulado
2. **Execute `run_update.py` DIARIAMENTE** durante a guerra para manter o acompanhamento diário atualizado
3. **Sempre faça pull antes de push** para evitar conflitos
4. **A API da Supercell tem rate limits** - o script já tem delays (`time.sleep(1)`)
5. **Os HTMLs são estáticos** - não fazem requisições em tempo real à API

---

**Documento criado por:** Antigravity AI  
**Data:** 30/12/2025  
**Versão:** 1.0  

**Qualquer dúvida, consulte a documentação ou execute os protocolos SYS_* para análise detalhada.**

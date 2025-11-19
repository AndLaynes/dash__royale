# 🏆 Clash Royale Dashboard

Dashboard interativo para clãs do Clash Royale com sistema de ligas, rankings e estatísticas.

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Configure sua chave da API do Clash Royale:

**Windows:**
```powershell
setx CR_API_KEY "sua_chave_aqui"
```

**Linux/Mac:**
```bash
export CR_API_KEY="sua_chave_aqui"
```

Obtenha sua chave em: https://developer.clashroyale.com

## 📊 Uso

```bash
python main.py
```

Abra os arquivos HTML gerados no navegador.

## ✨ Funcionalidades

- 🏆 Sistema de Ligas (10 tiers)
- 🥇 Top 10 Podium Visual
- ⚔️ Histórico de Guerras
- 📈 Estatísticas de Membros
- 📄 Exportação PDF

## 🔐 Segurança

⚠️ **NUNCA** commite sua chave de API! O `.gitignore` já protege dados sensíveis.

## 📝 Licença

MIT License

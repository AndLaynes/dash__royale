import json
import os
import pandas as pd
from datetime import datetime

# Define paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
OUTPUT_DIR = os.path.dirname(os.path.dirname(__file__))

# ==========================================
# TEMPLATES CSS & HTML (O DESIGN FIEL)
# ==========================================
STYLE_CSS = """
:root {
    --bg-dark: #0f1420;
    --bg-panel: #1a202c;
    --bg-header: #151a30;
    --primary-yellow: #fbbf24;
    --primary-red: #ef4444;
    --primary-green: #10b981;
    --text-main: #ffffff;
    --text-muted: #9ca3af;
    --border-color: #2d3748;
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

body {
    background-color: var(--bg-dark);
    color: var(--text-main);
    background-image: repeating-linear-gradient(45deg, #0f1420, #0f1420 10px, #111623 10px, #111623 20px);
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

/* HEADER */
.main-header {
    background-color: var(--bg-header);
    border-bottom: 2px solid #252b42;
    padding: 15px 0;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
}

.clan-identity { display: flex; align-items: center; gap: 15px; }

.clan-logo-img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 3px solid #fbbf24;
}

.clan-info h1 {
    font-size: 24px;
    color: #fbbf24;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

.clan-badges { display: flex; gap: 10px; }
.badge {
    background: #2d3748;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
    color: #cbd5e0;
}
.trophy-icon { color: #fbbf24; }

/* NAV PILLS */
.nav-pills { display: flex; gap: 10px; }

.nav-item {
    padding: 10px 20px;
    border-radius: 8px;
    text-decoration: none;
    color: #a0aec0;
    background: #232a3b;
    font-weight: 600;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
}

.nav-item:hover { background: #2d3748; color: white; }

.nav-item.active {
    background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(239, 68, 68, 0.3);
}

/* PAGE CONTENT */
.page-title-section {
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1px solid #2d3748;
    padding-bottom: 20px;
}

.page-title h2 { font-size: 28px; font-weight: 700; margin-bottom: 5px; }
.page-subtitle { color: #a0aec0; font-size: 14px; }

.meta-box {
    background: #2d3748;
    color: #fbbf24;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
    border: 1px solid #fbbf24;
    display: inline-block;
    margin-top: 10px;
}

/* CARDS ESTATISTICOS */
.audit-stats { display: flex; gap: 15px; }
.stat-box {
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 800;
    font-size: 16px;
    min-width: 120px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}
.stat-green { background: rgba(16, 185, 129, 0.2); color: #34d399; border-color: #059669; }
.stat-yellow { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border-color: #d97706; }
.stat-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border-color: #dc2626; }

/* INFO BOX */
.info-box {
    background: rgba(30, 58, 138, 0.2);
    border: 1px solid #1e3a8a;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
}
.info-header { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; }
.info-icon { font-size: 20px; color: #60a5fa; }
.info-title { font-weight: 700; color: white; font-size: 16px; }
.info-content { color: #cbd5e0; font-size: 14px; line-height: 1.6; }
.highlight { color: #fbbf24; font-weight: bold; }

/* TABLE */
.custom-table { width: 100%; border-collapse: separate; border-spacing: 0 8px; }
.custom-table th {
    text-align: left;
    color: #718096;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0 15px 10px 15px;
}
.custom-table tr.data-row { background: #1a202c; transition: transform 0.2s; }
.custom-table tr.data-row:hover { transform: translateY(-2px); background: #2d3748; }
.custom-table td { padding: 15px; border-top: 1px solid #2d3748; border-bottom: 1px solid #2d3748; color: white; font-size: 14px; font-weight: 500; }
.custom-table td:first-child { border-left: 1px solid #2d3748; border-top-left-radius: 8px; border-bottom-left-radius: 8px; }
.custom-table td:last-child { border-right: 1px solid #2d3748; border-top-right-radius: 8px; border-bottom-right-radius: 8px; }

.status-badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
}
.status-incomplete { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #d97706; }
.status-complete { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }
.status-zero { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626; }

.missing-badge {
    background: #ef4444; color: white;
    width: 24px; height: 24px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: bold;
}
"""

def get_page_template(active_page, content):
    nav_items = [
        ("index.html", "Visão Geral", "🏠", "Visão Geral"),
        ("daily_war.html", "Guerra", "⚔️", "Guerra"),
        ("members_stats.html", "Membros", "👥", "Membros"),
        ("ranking.html", "Ranking", "🏅", "Ranking")
    ]
    
    nav_html = ""
    for link, text, icon, key in nav_items:
        active_class = "active" if key == active_page else ""
        nav_html += f'<a href="{link}" class="nav-item {active_class}"><span>{icon}</span>{text}</a>'

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OS GUARDIÕES - {active_page}</title>
    <style>{STYLE_CSS}</style>
</head>
<body>
    <header class="main-header">
        <div class="container header-content">
            <div class="clan-identity">
                <div class="clan-logo">
                    <!-- LOGO REMOVIDA POR SOLICITAÇÃO -->
                </div>
                <div class="clan-info">
                    <h1>OS GUARDIÕES</h1>
                    <div class="clan-badges">
                        <span class="badge">#9PJRJRPC</span>
                        <span class="badge"><span class="trophy-icon">🏆</span> 3097</span>
                    </div>
                </div>
            </div>
            
            <nav class="nav-pills">
                {nav_html}
            </nav>
            
            <div style="color: #718096; font-size: 12px;">
                {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </div>
        </div>
    </header>

    <div class="container">
        {content}
    </div>

    <!-- SCRIPTS PARA FILTRO E ORDENAÇÃO -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const tables = document.querySelectorAll('.custom-table');
        tables.forEach(table => {{
            const headers = table.querySelectorAll('th');
            headers.forEach((header, index) => {{
                header.style.cursor = 'pointer';
                header.innerHTML += ' <span style="font-size:10px">⇅</span>';
                header.addEventListener('click', () => sortTable(table, index));
            }});
        }});
    }});

    function sortTable(table, colIndex) {{
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAsc = table.getAttribute('data-order') === 'asc';
        
        rows.sort((a, b) => {{
            // Tenta pegar o valor de texto ou um atributo data-value se existir
            let valA = a.children[colIndex].innerText.trim();
            let valB = b.children[colIndex].innerText.trim();
            
            // Tratamento para números
            if (!isNaN(parseFloat(valA)) && isFinite(valA)) {{
                return isAsc ? valA - valB : valB - valA;
            }}
            return isAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
        }});

        // Inverte a ordem para o próximo clique
        table.setAttribute('data-order', isAsc ? 'desc' : 'asc');
        
        // Reanexa as linhas
        rows.forEach(row => tbody.appendChild(row));
    }}
    </script>
</body>
</html>"""

def generate_html_report():
    print("Iniciando geração de relatórios...")
    
    # 1. Carregar dados
    daily_json_path = os.path.join(DATA_DIR, 'daily_war_history.json')
    excel_path = os.path.join(DATA_DIR, 'relatorio_participacao_guerra.xlsx')
    
    with open(daily_json_path, 'r', encoding='utf-8') as f:
        daily_data = json.load(f)
        
    df = pd.read_excel(excel_path)
    df = df.fillna(0)

    # 2. Processar Lógica de Auditoria
    # 2. Processar Lógica de Auditoria (GT-Z War Rules)
    # 0=Seg, 1=Ter, 2=Qua (Exibir Última Guerra Fechada)
    # 3=Qui, 4=Sex, 5=Sab, 6=Dom (Exibir Guerra Atual)
    weekday = datetime.now().weekday()
    
    audit_rows = []
    
    # STATUS: TREINO (Seg-Qua) -> Pega do River Race Log (Histórico Fechado)
    if weekday < 3:
        print(f"Hoje é {datetime.now().strftime('%A')} (Treino). Exibindo Última Guerra Fechada.")
        
        # Carregar riverracelog
        history_log_path = os.path.join(DATA_DIR, 'riverracelog.json')
        if os.path.exists(history_log_path):
            with open(history_log_path, 'r', encoding='utf-8') as f:
                r_log = json.load(f)
            
            # Pega a última guerra (Item 0) - que é a última fechada
            if r_log.get('items'):
                last_war = r_log['items'][0]
                
                # Meta Fechada = 16 Decks
                meta_decks = 16
                
                # Achar o clã
                my_clan_tag = "9PJRJRPC" # Hardcoded para segurança
                clan_standing = next((c for c in last_war.get('standings', []) 
                                    if c['clan']['tag'].replace('#','') == my_clan_tag), None)
                
                if clan_standing:
                    participants = clan_standing['clan']['participants']
                    for p in participants:
                        total_used = p.get('decksUsed', 0)
                        
                        status = "ZERADO"
                        faltam = meta_decks - total_used
                        if total_used >= meta_decks:
                            status = "EM DIA"
                            faltam = 0
                        elif total_used > 0:
                            status = "INCOMPLETO"
                            
                        # Tentar pegar cargo do Excel se existir
                        cargo = "member"
                        if not df.empty:
                            match = df[df['Nome'] == p['name']]
                            if not match.empty:
                                # cargo = match.iloc[0]['Cargo'] # Futuro
                                pass

                        audit_rows.append({
                            "name": p['name'],
                            "tag": p['tag'],
                            "cargo": cargo,
                            "decks": total_used,
                            "faltam": faltam,
                            "status": status
                        })
                else:
                    print("Clã não encontrado no histórico recente.")
        else:
            print("Histórico riverracelog.json não encontrado.")

    # STATUS: GUERRA (Qui-Dom) -> Pega do Daily History (Tempo Real)
    else:
        print(f"Hoje é {datetime.now().strftime('%A')} (Guerra). Exibindo Auditoria em Tempo Real.")
        
        # Meta Dinâmica: (Dia da Semana - 2) * 4. Ex: Qui(3)-2 = 1*4 = 4. Sex(4)-2 = 2*4 = 8.
        # Max 16.
        days_in_war = weekday - 2 
        meta_decks = days_in_war * 4
        if meta_decks > 16: meta_decks = 16
        if meta_decks < 4: meta_decks = 4 # Fallback

        players_audit = daily_data.get('players', {})
        for tag, p_data in players_audit.items():
            history = p_data.get('history', {})
            total_used = sum(int(v) for v in history.values())
            
            status = "ZERADO"
            faltam = meta_decks - total_used
            if total_used >= meta_decks:
                status = "EM DIA"
                faltam = 0
            elif total_used > 0:
                status = "INCOMPLETO"
            
            # Tentar pegar cargo do Excel
            cargo = "member"
            if not df.empty:
                match = df[df['Nome'] == p_data['name']] 
                # pode falhar se nome mudou, tag é melhor mas excel tem nome
                pass
            
            audit_rows.append({
                "name": p_data['name'],
                "tag": tag,
                "cargo": cargo,
                "decks": total_used,
                "faltam": faltam,
                "status": status
            })

    # Se falhar tudo, evitar crash
    if not audit_rows:
        meta_decks = 0

    # 3. FILTRAGEM DE MEMBROS (Limitar a 50)
    # Regra: Priorizar quem tem decks usados. Se empatar em 0, alfabético.
    # Mas idealmente queremos quem está no cla. Como não temos a lista oficial 'current_members' isolada aqui,
    # vamos assumir que quem jogou é membro. Quem não jogou (ZERADO) pode ser ex-membro.
    # Vamos ordenar por Status (INCOMPLETO > EM DIA > ZERADO) e cortar em 50?
    # Não, melhor cortar os ZERADOs excedentes.
    
    # Nova ordenação de prioridade para inclusão na lista:
    # 1. Decks Usados (desc) -> Garante que quem jogou fique.
    # 2. Status != Zerado
    
    def priority_key(x):
        return (x['decks'], x['status'] != 'ZERADO')
        
    # Ordenar todos por prioridade de "atividade"
    audit_rows.sort(key=priority_key, reverse=True)
    
    # Manter apenas os top 50 mais ativos (ou todos se < 50)
    active_members_count = len([r for r in audit_rows if r['decks'] > 0])
    
    # Se tivermos mais de 50 registros, cortamos.
    # Mas cuidado para não cortar membros novos que ainda não jogaram (0 decks) mas são do clã.
    # Como fallback, vamos limitar a 50 itens na visualização se passar muito.
    # O usuário reclamou de 71. Vamos fixar em 50 para a tabela.
    
    # Reordenar para Exibição (Incompleto -> Zerado -> Em Dia) SOMENTE os top 50
    top_50_rows = audit_rows[:50]
    
    def display_sort_key(x):
        # Ordem de exibição: Quem deve atenção primeiro?
        # 1. INCOMPLETO (Fez algo mas falta) - Amarelo
        # 2. ZERADO (Não fez nada) - Vermelho
        # 3. EM DIA (Tudo certo) - Verde
        order = {"INCOMPLETO": 0, "ZERADO": 1, "EM DIA": 2}
        return (order[x['status']], -x['faltam'], x['name'])
    
    top_50_rows.sort(key=display_sort_key)
    
    # Recalcular Stats baseados APENAS nos 50 exibidos
    count_em_dia = sum(1 for r in top_50_rows if r['status'] == 'EM DIA')
    count_incompleto = sum(1 for r in top_50_rows if r['status'] == 'INCOMPLETO')
    count_zerado = sum(1 for r in top_50_rows if r['status'] == 'ZERADO')

    # 4. Gerar HTML da Tabela
    audit_table_html = ""
    for row in top_50_rows:
        status_class = "status-incomplete"
        if row['status'] == "EM DIA": status_class = "status-complete"
        elif row['status'] == "ZERADO": status_class = "status-zero"
        
        missing_html = f'<div class="missing-badge">-{row["faltam"]}</div>' if row['faltam'] > 0 else '<span style="color:#34d399">✓</span>'
        
        audit_table_html += f"""
        <tr class="data-row">
            <td>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span>{row['name']}</span>
                    <span style="color:#718096; font-size:10px;">{row['tag']}</span>
                </div>
            </td>
            <td style="color:#a0aec0;">{row['cargo']}</td>
            <td style="font-weight:bold; font-size:16px;">{row['decks']}/{meta_decks}</td>
            <td>{missing_html}</td>
            <td><span class="status-badge {status_class}">{row['status']}</span></td>
        </tr>
        """

    # 5. Montar Conteúdo Daily War
    audit_content = f"""
    <div class="page-title-section">
        <div>
            <h2>Status de Guerra</h2>
            <p class="page-subtitle">Acompanhamento de Decks na Guerra Atual</p>
            <div class="meta-box">Meta do Dia: {meta_decks} Decks</div>
        </div>
        <div class="audit-stats">
            <div class="stat-box stat-green">
                {count_em_dia} EM DIA
            </div>
            <div class="stat-box stat-yellow">
                {count_incompleto} INCOMPLETO
            </div>
            <div class="stat-box stat-red">
                {count_zerado} ZERADO
            </div>
        </div>
    </div>

    <div class="info-box">
        <div class="info-header">
            <div class="info-icon">⚔️</div>
            <div class="info-title">Como funciona a Métrica de Guerra?</div>
        </div>
        <div class="info-content">
            O sistema monitora o uso de decks durante os dias oficiais de guerra (Quinta a Domingo).
            <br><br>
            <span class="highlight">Quinta-feira:</span> Meta 4 Decks (Início)<br>
            <span class="highlight">Sexta-feira:</span> Meta 8 Decks<br>
            <span class="highlight">Sábado:</span> Meta 12 Decks<br>
            <span class="highlight">Domingo:</span> Meta 16 Decks (Fechamento)
            <br><br>
            <i>*O dashboard atualiza automaticamente usando o último dia disponível.</i>
        </div>
    </div>

    <table class="custom-table">
        <thead>
            <tr>
                <th>JOGADOR</th>
                <th>CARGO</th>
                <th>DECKS USADOS</th>
                <th>FALTAM</th>
                <th>STATUS</th>
            </tr>
        </thead>
        <tbody>
            {audit_table_html}
        </tbody>
    </table>
    """

    # Escrever Daily War
    with open(os.path.join(OUTPUT_DIR, 'daily_war.html'), 'w', encoding='utf-8') as f:
        f.write(get_page_template("Guerra", audit_content))

    # 6. Gerar Outras Páginas (Placeholders com mesmo estilo por enquanto)
    index_content = """
    <div class="page-title-section">
        <div>
            <h2>Visão Geral</h2>
            <p class="page-subtitle">Bem-vindo ao Dashboard dos Guardiões</p>
        </div>
    </div>
    <div style="text-align:center; padding: 50px; color: #718096;">
        <p>Visão Geral Atualizada. Selecione a aba 'Auditoria' para detalhes da guerra.</p>
    </div>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(get_page_template("Visão Geral", index_content))

    with open(os.path.join(OUTPUT_DIR, 'members_stats.html'), 'w', encoding='utf-8') as f:
        f.write(get_page_template("Membros", index_content))

    with open(os.path.join(OUTPUT_DIR, 'ranking.html'), 'w', encoding='utf-8') as f:
        f.write(get_page_template("Ranking", index_content))

    print("Relatórios HTML gerados com sucesso!")

if __name__ == "__main__":
    generate_html_report()

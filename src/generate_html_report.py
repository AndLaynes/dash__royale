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
/* RESPONSIVE SUB-768px */
@media (max-width: 768px) {
    .header-content { flex-direction: column; align-items: flex-start; }
    .nav-pills { width: 100%; overflow-x: auto; padding-bottom: 5px; }
    .nav-item { white-space: nowrap; }
    
    .page-title-section { 
        flex-direction: column; 
        align-items: flex-start; 
        gap: 15px; 
    }
    
    .audit-stats { 
        width: 100%; 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 10px; 
    }
    .stat-box { min-width: auto; }
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

def format_clash_date(date_str):
    """Converte '20231124T123000.000Z' para '24/11/2023 12:30'"""
    if not date_str or date_str == 'N/A': return 'N/A'
    try:
        # Tenta formatar string da API
        if 'T' in date_str:
            dt = datetime.strptime(date_str, '%Y%m%dT%H%M%S.%fZ')
            return dt.strftime('%d/%m/%Y %H:%M')
        return date_str
    except Exception:
        return date_str

def generate_html_report():
    print("Iniciando geração de relatórios...")
    
    # 1. Carregar dados (Membros primeiro para mapeamento de Cargo)
    daily_json_path = os.path.join(DATA_DIR, 'daily_war_history.json')
    members_json_path = os.path.join(DATA_DIR, 'clan_members.json')
    
    # Initialize members_api globally for the function
    members_api = []
    
    # Criar Mapa de Membros (Tag -> Dados)
    member_map = {}
    role_label = {"leader": "Líder", "coLeader": "Co-Líder", "elder": "Ancião", "member": "Membro"}
    
    if os.path.exists(members_json_path):
        with open(members_json_path, 'r', encoding='utf-8') as f:
            # LOAD MEMBERS API HERE
            members_api = json.load(f).get('items', [])
            for m in members_api:
                member_map[m['tag']] = {
                    'role': role_label.get(m['role'], 'Membro'),
                    'name': m['name'],
                    'trophies': m['trophies'],
                    'donations': m['donations'],
                    'lastSeen': m.get('lastSeen')
                }
    
    with open(daily_json_path, 'r', encoding='utf-8') as f:
        daily_data = json.load(f)
        
    excel_path = os.path.join(DATA_DIR, 'relatorio_participacao_guerra.xlsx')
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        df = df.fillna(0)
    else:
        df = pd.DataFrame()

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
                            
                        # Tentar pegar cargo do Mapa de Membros
                        cargo = "Membro"
                        if p['tag'] in member_map:
                            cargo = member_map[p['tag']]['role']

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
            
            # Tentar pegar cargo do Mapa de Membros
            cargo = "Membro"
            if tag in member_map:
                cargo = member_map[tag]['role']
            
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
        </div>
        <div class="audit-stats">
             <!-- META AGORA É UM STAT-BOX PARA ALINHAMENTO -->
            <div class="stat-box" style="border: 1px solid #fbbf24; color: #fbbf24; background: rgba(251, 191, 36, 0.1);">
                <div style="font-size:10px; opacity:0.8;">META DA GUERRA</div>
                {meta_decks} DECKS
            </div>
            <div class="stat-box stat-green">
                <div style="font-size:10px; opacity:0.8;">EM DIA</div>
                {count_em_dia}
            </div>
            <div class="stat-box stat-yellow">
                <div style="font-size:10px; opacity:0.8;">INCOMPLETO</div>
                {count_incompleto}
            </div>
            <div class="stat-box stat-red">
                <div style="font-size:10px; opacity:0.8;">ZERADO</div>
                {count_zerado}
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

    # 6. Gerar Página INDEX (Dashboard Geral)
    print("Gerando Dashboard (Index)...")
    
    # 1. Carregar Clan Info (GT-Z para Liga e Location)
    clan_info_path = os.path.join(DATA_DIR, 'clan_info.json')
    league_name = "Desconhecida"
    clan_war_trophies = 0
    clan_location = "Desconhecido"
    
    if os.path.exists(clan_info_path):
        with open(clan_info_path, 'r', encoding='utf-8') as f:
            c_info = json.load(f)
            clan_war_trophies = c_info.get('clanWarTrophies', 0)
            clan_location = c_info.get('location', {}).get('name', 'N/A')
            
            # Inferir Liga (Ground Truth)
            if clan_war_trophies >= 3000: league_name = "Liga Lendária"
            elif clan_war_trophies >= 1500: league_name = "Liga Ouro"
            elif clan_war_trophies >= 600: league_name = "Liga Prata"
            else: league_name = "Liga Bronze"
    else:
        # Fallback para current_war
        if 'clan' in daily_data:
             clan_war_trophies = daily_data['clan'].get('clanScore', 0) # Fallback incerto
        
    # 2. Performance de Guerra e Participação
    war_rank = "N/A"
    war_state = "Em Treino"
    if weekday >= 3: war_state = "Em Guerra ⚔️"
    
    part_full = 0
    part_idling = 0 # Incompleto
    part_none = 0
    
    # Analisar Último Log para Participação Real
    if os.path.exists(os.path.join(DATA_DIR, 'riverracelog.json')):
        try:
            with open(os.path.join(DATA_DIR, 'riverracelog.json'), 'r') as f:
                last_log = json.load(f)['items'][0]
                
                # Rank
                my_standing = next((c for c in last_log['standings'] if c['clan']['tag'].replace("#","") == "9PJRJRPC"), None)
                if my_standing:
                    war_rank = f"#{my_standing['rank']}"
                    
                    # Participação (Baseado no Log Anterior para ter Ground Truth fechado)
                    for p in my_standing['clan']['participants']:
                        decks = p['decksUsed']
                        if decks >= 4: part_full += 1 # Assumindo 4 decks/dia como 'ativo no dia', mas log é semanal.
                        elif decks > 0: part_idling += 1
                        else: part_none += 1
                    
                    # Ajuste para 'None' (Total Members - Participants in Log)
                    # O log só mostra quem participou ou teve fama? Não, mostra participants.
                    # Mas se member count > participants list, o resto é None.
                    # Vamos usar os contadores diretos da lista de participantes da guerra.
        except:
            pass

    # 3. Doações e Top Jogadores (Expandido para Top 10)
    total_donations = 0
    top_donors = []
    
    # Se ja temos members_api carregado e ordenado
    # Recalcular estatísticas frescas
    
    # Ordenar por Doações
    sorted_donations = sorted(members_api, key=lambda x: x['donations'], reverse=True)
    total_donations = sum(m['donations'] for m in members_api)
    top_donors = sorted_donations[:10] # Top 10
    
    # Ordenar por Troféus (MVPs)
    sorted_trophies = sorted(members_api, key=lambda x: x['trophies'], reverse=True)
    top_trophies = sorted_trophies[:10] # Top 10


    # HTML Construction
    
    def render_list(items, value_key, icon, color_style=""):
        html = ""
        for i, p in enumerate(items):
            rank_display = f"{i+1}."
            html += f"""
            <div class="list-item">
                <span class="rank-num">{rank_display}</span>
                <span class="badgex" style="{color_style}">{icon} {p[value_key]}</span>
                <span class="p-name">{p['name']}</span>
            </div>
            """
        return html
        
    donors_html = render_list(top_donors, 'donations', '🃏')
    mvp_html = render_list(top_trophies, 'trophies', '🏆', "background:#fbbf24; color:#000;")

    index_content = f"""
    <div class="dashboard-grid">
        <!-- 1. IDENTIDADE DO CLÃ -->
        <div class="dash-card main-card">
            <div class="card-header">
                <h3>CLÃ OS GUARDIÕES</h3>
                <span class="status-badge status-complete">{league_name}</span>
            </div>
            <div class="card-body big-stat">
                <div>
                   <div class="stat-value">🏆 {clan_war_trophies}</div>
                   <div class="stat-label">Troféus de Guerra</div>
                </div>
                <div style="text-align:right;">
                    <div class="stat-value">{clan_location}</div>
                    <div class="stat-label">Localização</div>
                </div>
            </div>
        </div>

        <!-- 2. STATUS DE GUERRA -->
        <div class="dash-card war-card">
            <div class="card-header">
                <h3>⚔️ ÚLTIMA GUERRA</h3>
            </div>
            <div class="card-body">
                <div class="stat-row">
                    <span class="label">Posição Final:</span>
                    <span class="value accent">{war_rank}</span>
                </div>
                 <div class="stat-row">
                    <span class="label">Part. Total (Full):</span>
                    <span class="value" style="color:var(--primary-green)">{part_full} Jogadores</span>
                </div>
                <div class="stat-row">
                    <span class="label">Part. Parcial:</span>
                    <span class="value" style="color:var(--primary-yellow)">{part_idling} Jogadores</span>
                </div>
            </div>
        </div>

        <!-- 3. DOAÇÕES (TOP 10) -->
        <div class="dash-card donation-card">
            <div class="card-header">
                <h3>🤝 DOAÇÕES ({total_donations})</h3>
            </div>
            <div class="card-body scrollable-list">
                 {donors_html}
            </div>
        </div>
        
        <!-- 4. TOP JOGADORES (TOP 10) -->
        <div class="dash-card mvp-card">
            <div class="card-header">
                <h3>🔥 TOP 10 TROFÉUS</h3>
            </div>
            <div class="card-body scrollable-list">
                {mvp_html}
            </div>
        </div>
    </div>
    
    <style>
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .dash-card {{
            background: var(--bg-panel);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border-color);
            display: flex; flex-direction: column;
        }}
        .dash-card h3 {{
             margin: 0; font-size: 14px; color: var(--text-muted); text-transform: uppercase;
             letter-spacing: 1px;
        }}
        .card-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 15px; padding-bottom: 10px;
            border-bottom: 1px solid #ffffff10;
        }}
        .big-stat {{
            display: flex; justify-content: space-between; align-items: center;
        }}
        .stat-value {{ font-size: 22px; font-weight: bold; color: var(--text-main); }}
        .stat-label {{ font-size: 11px; color: var(--text-muted); }}
        
        .stat-row {{
            display: flex; justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid #ffffff05;
            font-size: 14px;
        }}
        .value.accent {{ color: var(--primary-yellow); font-weight: bold; }}
        
        .scrollable-list {{
            max-height: 300px;
            overflow-y: auto;
            padding-right: 5px;
        }}
        
        /* Custom Scrollbar for lists */
        .scrollable-list::-webkit-scrollbar {{ width: 4px; }}
        .scrollable-list::-webkit-scrollbar-track {{ background: #1a202c; }}
        .scrollable-list::-webkit-scrollbar-thumb {{ background: #2d3748; border-radius: 2px; }}

        .list-item {{
            display: flex; align-items: center; gap: 10px;
            margin-bottom: 8px; font-size: 13px;
        }}
        .rank-num {{
            width: 20px; color: var(--text-muted); font-weight: bold;
        }}
        .badgex {{
            background: #2d3748; padding: 2px 6px; border-radius: 4px; 
            font-size: 11px; font-weight: bold; min-width: 60px; text-align: center;
        }}
        .p-name {{
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px;
        }}
        
        .war-card {{ border-top: 3px solid var(--primary-red); }}
        .donation-card {{ border-top: 3px solid var(--primary-green); }}
        .mvp-card {{ border-top: 3px solid var(--primary-yellow); }}
        .main-card {{ border-top: 3px solid #3b82f6; }}
    </style>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(get_page_template("Visão Geral", index_content))

    # 6. Gerar Página de MEMBROS (GT-Z)
    members_json_path = os.path.join(DATA_DIR, 'clan_members.json')
    if os.path.exists(members_json_path):
        with open(members_json_path, 'r', encoding='utf-8') as f:
            members_api = json.load(f).get('items', [])
            
        print(f"Processando {len(members_api)} membros para a lista oficial.")
        
        # Ordenar por Cargo (Líder > Co-Líder > Ancião > Membro)
        role_map = {"leader": 3, "coLeader": 2, "elder": 1, "member": 0}
        role_label = {"leader": "Líder", "coLeader": "Co-Líder", "elder": "Ancião", "member": "Membro"}
        
        members_api.sort(key=lambda x: (role_map.get(x['role'], 0), x['trophies']), reverse=True)
        
        members_table_html = ""
        for m in members_api:
            # Formatação de datas
            role_pt = role_label.get(m["role"], m["role"])
            role_badge = f'<span class="badge" style="background:#4a5568">{role_pt}</span>'
            if m["role"] == "leader": role_badge = f'<span class="badge" style="background:#e53e3e">Líder</span>'
            if m["role"] == "coLeader": role_badge = f'<span class="badge" style="background:#d69e2e">Co-Líder</span>'
            
            last_seen_fmt = format_clash_date(m.get('lastSeen', 'N/A'))

            members_table_html += f"""
            <tr class="data-row">
                <td>
                    <div style="font-weight:bold;">{m['name']}</div>
                    <div style="font-size:10px; color:#718096;">{m['tag']}</div>
                </td>
                <td>{role_badge}</td>
                <td><span style="color:#fbbf24">🏆 {m['trophies']}</span></td>
                <td><span style="color:#34d399"> cards {m['donations']}</span></td>
                <td style="color:#a0aec0">{last_seen_fmt}</td>
            </tr>
            """
            
        members_content = f"""
        <div class="page-title-section">
            <div>
                <h2>Membros Oficiais</h2>
                <p class="page-subtitle">Lista atualizada via Supercell API</p>
                <div class="meta-box">{len(members_api)} Membros no Clã</div>
            </div>
        </div>
        
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Cargo</th>
                    <th>Troféus</th>
                    <th>Doações</th>
                    <th>Último Acesso</th>
                </tr>
            </thead>
            <tbody>
                {members_table_html}
            </tbody>
        </table>
        """
        
        with open(os.path.join(OUTPUT_DIR, 'members_stats.html'), 'w', encoding='utf-8') as f:
            f.write(get_page_template("Membros", members_content))
            
    else:
        print("AVISO: clan_members.json não encontrado. Pulando página de membros.")

    # 7. Gerar Página de RANKING (GT-Z Logic)
    # Lógica: Cruzar Members API com RiverRaceLog para calcular Score
    if os.path.exists(members_json_path):
        # 1. Carregar Histórico de Guerra para calcular Médias
        river_log_path = os.path.join(DATA_DIR, 'riverracelog.json')
        war_stats = {} # tag -> {fame: 0, decks: 0}
        
        if os.path.exists(river_log_path):
            with open(river_log_path, 'r', encoding='utf-8') as f:
                r_log = json.load(f)
            
            # Analisar últimas 10 guerras apenas
            for war in r_log.get('items', [])[:10]:
                 # Achar o clã
                my_clan = next((c for c in war.get('standings', []) 
                                if c['clan']['tag'].replace('#','') == "9PJRJRPC"), None)
                if my_clan:
                    for p in my_clan['clan']['participants']:
                        tag = p['tag']
                        if tag not in war_stats: war_stats[tag] = {'fame': 0, 'decks': 0}
                        war_stats[tag]['fame'] += p.get('fame', 0)
                        war_stats[tag]['decks'] += p.get('decksUsed', 0)

        # 2. Calcular Métricas para Membros Atuais
        rank_data = [] # {name, score, metrics: {}}
        
        # Encontrar Maximos para Normalização
        max_fame = 0
        max_efficiency = 0
        max_trophies = 0
        max_donations = 0
        
        # Pré-processamento
        temp_list = []
        for m in members_api:
            tag = m['tag']
            w_stat = war_stats.get(tag, {'fame': 0, 'decks': 0})
            
            fame = w_stat['fame']
            decks = w_stat['decks']
            efficiency = (fame / decks) if decks > 0 else 0
            trophies = m['trophies']
            donations = m['donations']
            
            if fame > max_fame: max_fame = fame
            if efficiency > max_efficiency: max_efficiency = efficiency
            if trophies > max_trophies: max_trophies = trophies
            if donations > max_donations: max_donations = donations
            
            temp_list.append({
                "name": m['name'],
                "tag": tag,
                "fame": fame,
                "efficiency": efficiency,
                "trophies": trophies,
                "donations": donations
            })
            
        # 3. Calcular Score Final
        # Pesos: Fame 50%, Efficiency 25%, Trophies 15%, Donations 10%
        for p in temp_list:
            norm_fame = (p['fame'] / max_fame * 100) if max_fame > 0 else 0
            norm_eff = (p['efficiency'] / max_efficiency * 100) if max_efficiency > 0 else 0
            norm_troph = (p['trophies'] / max_trophies * 100) if max_trophies > 0 else 0
            norm_don = (p['donations'] / max_donations * 100) if max_donations > 0 else 0
            
            score = (norm_fame * 0.50) + (norm_eff * 0.25) + (norm_troph * 0.15) + (norm_don * 0.10)
            
            rank_data.append({
                **p,
                "score": round(score, 1),
                "norm_breakdown": [norm_fame, norm_eff, norm_troph, norm_don]
            })
            
        # Ordenar pelo Score
        rank_data.sort(key=lambda x: x['score'], reverse=True)
        
        # 4. Gerar HTML
        rank_table_html = ""
        # Verificar se rank_data tem itens
        if not rank_data:
             rank_table_html = "<tr><td colspan='5' style='text-align:center'>Não há dados suficientes para o ranking ainda.</td></tr>"
        else:
            for i, r in enumerate(rank_data):
                rank_pos = i + 1
                medal = ""
                if rank_pos == 1: medal = "🥇"
                elif rank_pos == 2: medal = "🥈"
                elif rank_pos == 3: medal = "🥉"
                
                rank_table_html += f"""
                <tr class="data-row">
                    <td style="font-weight:bold; font-size:16px;">{medal} #{rank_pos}</td>
                    <td style="font-weight:600;">{r['name']}</td>
                    <td style="color:#fbbf24; font-weight:800; font-size:18px;">{r['score']}</td>
                    <td style="font-size:13px; color:#a0aec0;">
                        Fame: <b style="color:white">{r['fame']}</b><br>
                        Eff: <b style="color:white">{int(r['efficiency'])}</b>
                    </td>
                    <td style="font-size:13px; color:#a0aec0;">
                        Troféus: <b style="color:white">{r['trophies']}</b><br>
                        Donates: <b style="color:white">{r['donations']}</b>
                    </td>
                </tr>
                """
        
        ranking_content = f"""
        <div class="page-title-section">
            <div>
                <h2>Ranking de Performance</h2>
                <p class="page-subtitle">Algoritmo unificado de desempenho (Guerra + Atividade)</p>
            </div>
        </div>
        
        <div class="info-box">
             <div class="info-header">
                <div class="info-icon">📊</div>
                <div class="info-title">Como funciona o Score do Ranking?</div>
            </div>
            <div class="info-content">
                O Score é calculado normalizando as métricas relativas ao melhor do clã.<br><br>
                <ul>
                    <li><span class="highlight">50% - Ouro do Rio (Fame):</span> Acumulado nas últimas 10 guerras.</li>
                    <li><span class="highlight">25% - Eficiência (Win Rate Estimado):</span> Média de Fame por Deck usado.</li>
                    <li><span class="highlight">15% - Troféus:</span> Nível de habilidade atual (Ladder).</li>
                    <li><span class="highlight">10% - Doações:</span> Contribuição diária de cartas.</li>
                </ul>
            </div>
        </div>
        
        <table class="custom-table" data-order="desc">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Jogador</th>
                    <th>SCORE FINAL</th>
                    <th>Guerra (Fame/Eff)</th>
                    <th>Perfil (Troph/Don)</th>
                </tr>
            </thead>
            <tbody>
                {rank_table_html}
            </tbody>
        </table>
        """
        
        with open(os.path.join(OUTPUT_DIR, 'ranking.html'), 'w', encoding='utf-8') as f:
            f.write(get_page_template("Ranking", ranking_content))

    print("Relatórios HTML gerados com sucesso!")

if __name__ == "__main__":
    generate_html_report()

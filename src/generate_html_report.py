import json
import os
import pandas as pd
from datetime import datetime, timedelta, timezone

# Define paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
OUTPUT_DIR = os.path.dirname(os.path.dirname(__file__))

# ==========================================
# CONSTANTES GLOBAIS
# ==========================================
# Fuso Horário Brasil (GMT-3)
BRAZIL_TZ = timezone(timedelta(hours=-3))

# [GT-Z] PDF FUNCTIONALITY DELETED PER USER REQUEST (2026-01-26)

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
.audit-timestamp {
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    color: #718096;
    border: 1px solid #2d3748;
    padding: 4px 8px;
    border-radius: 4px;
    background: #1a202c;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}



/* RESPONSIVE SUB-768px */
@media (max-width: 768px) {
    .header-content { flex-direction: column; align-items: flex-start; gap: 15px; }
    .nav-pills { 
        width: 100%; 
        flex-wrap: wrap; 
        justify-content: center; 
        padding-bottom: 5px; 
    }
    .nav-item { white-space: nowrap; font-size: 13px; padding: 8px 15px; }
    .audit-timestamp { width: 100%; justify-content: center; margin-top: 10px; }
    
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
    
    .dashboard-grid {
        grid-template-columns: 1fr !important;
    }
}



/* PDF CLEAN MODE (GT-Z Print Style) */
.pdf-clean-mode {
    background-color: #ffffff !important;
    background-image: none !important;
    color: #000000 !important;
}

.pdf-clean-mode table {
    page-break-inside: auto !important;
    width: 98% !important;
    margin: 0 auto !important;
    table-layout: fixed !important;
    border-collapse: collapse !important; /* Grid Sólido: Garante fechamento */
    border: 1px solid #000000 !important; /* Borda externa da tabela */
    border-right: 1px solid #000000 !important; /* Reforço de fechamento */
}
.pdf-clean-mode thead { 
    display: table-header-group !important;
}
.pdf-clean-mode tr { 
    page-break-inside: avoid !important; 
    page-break-after: auto !important;
}
.pdf-clean-mode * {
    color: #000000 !important;
    border-color: #000000 !important;
    background: transparent !important;
    box-shadow: none !important;
    text-shadow: none !important;
}
.pdf-clean-mode .main-header,
.pdf-clean-mode .nav-pills,
.pdf-clean-mode .info-box,
.pdf-clean-mode .audit-timestamp,
.pdf-clean-mode #pdf-export-btn { 
    display: none !important; 
}
.pdf-clean-mode .container {
    max-width: 100% !important;
    padding: 0 20px !important;
    margin: 0 !important;
}
.pdf-clean-mode .stat-box {
    border: 1px solid #000000 !important;
    color: #000000 !important;
}
.pdf-clean-mode th, .pdf-clean-mode td {
    border: 1px solid #000000 !important; /* Garante linhas verticais e horizontais em TUDO */
    padding: 4px !important;
    font-size: 11px !important;
    word-wrap: break-word !important;
    background: #ffffff !important;
}
/* Forçar fechamento visual explícito no último filho se necessário, mas collapse já resolve */
.pdf-clean-mode td:last-child, .pdf-clean-mode th:last-child {
    border-right: 1px solid #000000 !important;
}
/* Otimização de Colunas para PDF */
.pdf-clean-mode th:nth-child(3), 
.pdf-clean-mode td:nth-child(3) { /* Decks Used */
    width: 60px !important; 
    text-align: center !important;
}
.pdf-clean-mode th:nth-child(4),
.pdf-clean-mode td:nth-child(4) { /* Faltam */
    width: 40px !important;
    text-align: center !important;
}

.pdf-clean-mode .status-badge {
    border: none !important; /* Remove bordas arredondadas */
    border-radius: 0 !important;
    font-weight: normal !important;
    color: #000000 !important;
    padding: 0 !important;
    text-transform: uppercase;
}
.pdf-clean-mode .missing-badge {
    background: transparent !important;
    color: #000000 !important;
    border: none !important; /* Remove círculo */
    border-radius: 0 !important;
    width: auto !important;
    height: auto !important;
    font-weight: normal !important;
    display: inline !important;
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

    generated_at = datetime.now(BRAZIL_TZ).strftime("%d/%m/%Y %H:%M")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OS GUARDIÕES - {active_page}</title>
    <style>{STYLE_CSS}</style>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
</head>
<body>
    <header class="main-header">
        <div class="container header-content">
            <div class="clan-identity">
                <div class="clan-info">
                    <h1 style="display:flex; align-items:center; gap:10px;">
                        OS GUARDIÕES 
                        <span style="font-size:12px; color:#fbbf24; border:1px solid #fbbf24; padding:2px 6px; border-radius:4px; opacity:0.8;">#9PJRJRPC</span>
                    </h1>
                </div>
            </div>
            
            <div style="display:flex; flex-direction:column; align-items:flex-end; gap:10px;">
                <nav class="nav-pills">
                    {nav_html}
                </nav>
                <div class="audit-timestamp">
                    <span>🕒 Atualizado:</span>
                    <strong style="color:#cbd5e0">{generated_at}</strong>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        {content}
    </div>

    <script>
    function downloadPDF() {{
        const element = document.body;
        const btn = document.getElementById('pdf-export-btn');
        
        // Add Clean Mode Class
        element.classList.add('pdf-clean-mode');
        
        // Options
        var opt = {{
          margin:       5,
          filename:     'Relatorio_Guerra_DashRoyale.pdf',
          image:        {{ type: 'jpeg', quality: 0.98 }},
          html2canvas:  {{ scale: 2, useCORS: true }},
          jsPDF:        {{ unit: 'mm', format: 'a4', orientation: 'portrait' }}
        }};

        // Generate
        html2pdf().set(opt).from(element).save().then(function(){{
            // Remove Clean Mode Class after save
            element.classList.remove('pdf-clean-mode');
        }});
    }}
    </script>

    <script>
    // [GT-Z] Scripts Cleaned (Sorting Restoration)

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
            let valA = a.children[colIndex].getAttribute('data-value') || a.children[colIndex].innerText.trim();
            let valB = b.children[colIndex].getAttribute('data-value') || b.children[colIndex].innerText.trim();
            
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
    """Converte '20231124T123000.000Z' para '24/11/2023 12:30' (GMT-3)"""
    if not date_str or date_str == 'N/A': return 'N/A'
    try:
        # Tenta formatar string da API (UTC)
        if 'T' in date_str:
            # Remover 'Z' e frações para facilitar parse, ou usar strptime com %f
            # API Clash geralmente manda %Y%m%dT%H%M%S.%fZ
            
            # Limpeza basica para suportar formatos variados
            clean_date = date_str.replace('Z', '')
            
            if '.' in clean_date:
                dt = datetime.strptime(clean_date, '%Y%m%dT%H%M%S.%f')
            else:
                dt = datetime.strptime(clean_date, '%Y%m%dT%H%M%S')
            
            # Definir como UTC
            dt = dt.replace(tzinfo=timezone.utc)
            
            # Converter para BRT
            dt_br = dt.astimezone(BRAZIL_TZ)
            
            return dt_br.strftime('%d/%m/%Y %H:%M')
        return date_str
    except Exception as e:
        return date_str

def generate_static_pdf(rows, meta_decks, counts, war_label, output_dir):
    """
    [GT-Z] PDF GENERATION DELETED.
    Function stub kept for interface stability but empty.
    """
    return

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
    # 3=Qui, 4=Sex, 5=Sab, 6=Dom (Exibir Guerra Atual)
    weekday = datetime.now(BRAZIL_TZ).weekday()
    
    audit_rows = []

    # STATUS: TREINO (Seg-Qua) -> Pega do River Race Log (Histórico Fechado)
    if weekday < 3:
        print(f"Hoje é {datetime.now(BRAZIL_TZ).strftime('%A')} (Treino). Exibindo Última Guerra Fechada.")
        
        # Carregar riverracelog
        history_log_path = os.path.join(DATA_DIR, 'riverracelog.json')
        if os.path.exists(history_log_path):
            with open(history_log_path, 'r', encoding='utf-8') as f:
                r_log = json.load(f)
            
            # Pega a última guerra (Item 0) - que é a última fechada
            if r_log.get('items'):
                last_war = r_log['items'][0]
                
                # [GT-Z] DEFINE WAR LABEL FOR AUDIT CONTENT
                s_id = last_war.get('seasonId', '?')
                s_idx = last_war.get('sectionIndex', '?')
                war_label = f"Temporada {s_id} | Semana {s_idx} (Finalizada)"
                
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
                        total_fame = p.get('fame', 0)
                        
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
                            "fame": total_fame,
                            "faltam": faltam,
                            "status": status
                        })
                else:
                    print("Clã não encontrado no histórico recente.")
        else:
            print("Histórico riverracelog.json não encontrado.")

    # STATUS: GUERRA (Qui-Dom) -> Pega do Daily History (Tempo Real)
    else:
        print(f"Hoje é {datetime.now(BRAZIL_TZ).strftime('%A')} (Guerra). Exibindo Auditoria Retrospectiva (Protocolo D-1).")
        
        # ---------------------------------------------------------
        # LÓGICA DE AUDITORIA D-1 (STRICT RETROSPECTIVE) - GT-Z
        # ---------------------------------------------------------
        # O sistema não deve cobrar o dia corrente (Real-Time), mas sim fechar
        # o dia anterior.
        #
        # HOJE      | AUDITA    | META (ACUMULADA)
        # ----------------------------------------
        # Quinta    | N/A       | (Mostra parcial ou zero)
        # Sexta     | Quinta    | 4 Decks
        # Sábado    | Sexta     | 8 Decks (4 Qui + 4 Sex)
        # Domingo   | Sábado    | 12 Decks
        # Segunda   | Domingo   | 16 Decks (Feita no bloco 'else' acima)
        
        # Ajuste do Index para D-1 (Auditoria Acumulada)
        # weekday: 3=Qui, 4=Sex, 5=Sab, 6=Dom
        
        # [CORREÇÃO GT-Z 23/01]
        # A meta deve ser o ACUMULADO DO DIA CORRENTE.
        # Ex: Sexta (4) -> Meta deve ser 8 (4 de Qui + 4 de Sex).
        # Antigamente, fazia D-1 estrito (olhava meta de quinta), o que era errado para o incentivo diário.
        
        audit_target_day_index = weekday # Se hoje é Sex(4), meta é baseada em 4.
        
        # Meta: (DiaAuditado_Index - 2) * 4
        # Ex Sexta (4): (4 - 2) * 4 = 8 Decks.
        
        days_in_war_audit = audit_target_day_index - 2
        meta_decks = days_in_war_audit * 4
        
        if meta_decks < 4: 
            # Caso especial: Quinta-feira (3). (3-2)*4 = 4 Decks.
            # Segurança para não gerar meta 0 ou negativa.
            meta_decks = 4 

        if meta_decks > 16: meta_decks = 16
        
        # [NOVO] Extrair Identificação da Guerra
        season_id = daily_data.get('seasonId', '?')
        section_idx = daily_data.get('sectionIndex', '?')
        war_label = f"Temporada {season_id} | Semana {section_idx}"

        players_audit = daily_data.get('players', {})
        for tag, p_data in players_audit.items():
            history = p_data.get('history', {})
            fame_history = p_data.get('fame_history', {})
            total_used = sum(int(v) for v in history.values())
            total_fame = sum(int(v) for v in fame_history.values())
            
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
                "cargo": cargo,
                "decks": total_used,
                "fame": total_fame,
                "faltam": faltam,
                "status": status
            })

    # Se falhar tudo, evitar crash
    if not audit_rows:
        meta_decks = 0

    # 3. MEMBER FILTERING (View Limit: 50)
    # Logic: Prioritize Active Users. If tied at 0, sort alphabetically.
    # Assumption: Active players are confirmed members. Zero-activity entries may indicate non-members or departures.
    # Display Order: Status Priority (INCOMPLETO > EM DIA > ZERADO).
    #
    # Truncation Policy: Excess ZERADO entries are removed to maintain dashboard performance.
    
    # Nova ordenação de prioridade para inclusão na lista:
    # 1. Decks Usados (desc) -> Garante que quem jogou fique.
    # 2. Status != Zerado
    
    def priority_key(x):
        return (x['decks'], x['status'] != 'ZERADO')
        
    # Ordenar todos por prioridade de "atividade"
    audit_rows.sort(key=priority_key, reverse=True)
    
    # Manter apenas os top 50 mais ativos (ou todos se < 50)
    active_members_count = len([r for r in audit_rows if r['decks'] > 0])
    
    # [VIEW CONSTRAINT] 
    # Hard Limit: 50 items.
    # Justification: UX Optimization and Layout Stability.
    
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

    # 6. Calcular Total de Jogadores Listados
    total_listed = len(top_50_rows)

    # 7. Gerar HTML da Tabela
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
            <td style="color:#fbbf24; font-weight:bold;">{row['fame']}</td>
            <td><span class="status-badge {status_class}">{row['status']}</span></td>
        </tr>
        """

    pdf_shadow_content = ""

    # 5. Montar Conteúdo Daily War
    # [GT-Z] PDF BUTTON REMOVED

    audit_content = f"""
    <div id="printable-area">

        <!-- HEADER DO PAGINA (Carimbo) -->
        <div class="page-title-section">
        <div>
            <h2>Status de Guerra</h2>
            <div style="display:flex; flex-direction:column;">
                <p class="page-subtitle">Acompanhamento de Decks na Guerra Atual</p>
                <div style="margin-top:5px;">
                    <span class="badge" style="background:#2d3748; color:#a0aec0; border:1px solid #4a5568;">
                        Dados de: {datetime.now(BRAZIL_TZ).strftime('%d/%m')}
                    </span>
                    <span class="badge" style="background:#2d3748; color:#fbbf24; border:1px solid #d97706; margin-left:5px;">
                        Fonte: {war_label}
                    </span>
                </div>
            </div>
        </div>
        <div style="display:flex; justify-content:flex-end; margin-top: -30px; margin-bottom: 20px;">
            <button id="pdf-export-btn" onclick="downloadPDF()" style="background:#fbbf24; color:#0f1420; border:none; padding:8px 16px; border-radius:6px; font-weight:bold; cursor:pointer; display:flex; align-items:center; gap:8px;">
                <span>📄</span> Exportar PDF
            </button>
        </div>
        </div>
        
        <div class="audit-stats">
             <!-- META AGORA É UM STAT-BOX PARA ALINHAMENTO -->
            <div class="stat-box" style="border: 1px solid #fbbf24; color: #fbbf24; background: rgba(251, 191, 36, 0.1);">
                <div style="font-size:10px; opacity:0.8;">META DA GUERRA</div>
                {meta_decks} DECKS
            </div>
            <div class="stat-box" style="border: 1px solid #a0aec0; color: #cbd5e0; background: rgba(45, 55, 72, 0.5);">
                <div style="font-size:10px; opacity:0.8;">MEMBROS ATIVOS</div>
                {total_listed}
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
            <strong>1. Métrica Primária (Obrigatória): PARTICIPAÇÃO</strong><br>
            O objetivo é usar <strong>4 Decks todos os dias</strong> de guerra (Quinta a Domingo).<br>
            <span class="highlight">Quinta:</span> Meta 4 <span style="color:#718096">|</span> 
            <span class="highlight">Sexta:</span> Meta 8 <span style="color:#718096">|</span> 
            <span class="highlight">Sábado:</span> Meta 12 <span style="color:#718096">|</span> 
            <span class="highlight">Domingo:</span> Meta 16
            <div style="margin-top:8px; border-top:1px solid #ffffff10; padding-top:8px;">
                <strong>2. Métrica Secundária (Qualidade): FAMA</strong><br>
                Define a qualidade das batalhas. Usada para desempate.<br>
                <span style="color:#fbbf24">★ Vitória (Duel):</span> 250pts &nbsp;|&nbsp; 
                <span style="color:#fbbf24">★ Vitória (1v1):</span> 200pts &nbsp;|&nbsp; 
                <span style="color:#ef4444">💀 Derrota:</span> 100pts
            </div>
        </div>
    </div>

    <table class="custom-table">
        <thead>
            <tr>
                <th>JOGADOR</th>
                <th>CARGO</th>
                <th>DECKS USADOS</th>
                <th>FALTAM</th>
                <th>FAMA</th>
                <th>STATUS</th>
            </tr>
        </thead>
        <tbody>
            {audit_table_html}
        </tbody>
    </table>
    </div>
    
    </div>
    """

    # Escrever Daily War
    with open(os.path.join(OUTPUT_DIR, 'daily_war.html'), 'w', encoding='utf-8') as f:
        f.write(get_page_template("Guerra", audit_content))

    # [GT-Z] STATIC PDF GENERATION CALL REMOVED
    # generate_static_pdf(top_50_rows, meta_decks, counts, war_label, OUTPUT_DIR)

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
    season_id = "?" 
    war_state = "Em Treino"
    if weekday >= 3: war_state = "Em Guerra ⚔️"
    
    part_full = 0
    part_idling = 0 # Incompleto
    part_none = 0
    
    # Tag Alvo (Normalizada)
    TARGET_TAG_CLEAN = "9PJRJRPC"

    # Analisar Último Log para Participação Real
    if os.path.exists(os.path.join(DATA_DIR, 'riverracelog.json')):
        try:
            with open(os.path.join(DATA_DIR, 'riverracelog.json'), 'r', encoding='utf-8') as f:
                r_log = json.load(f)
                items = r_log.get('items', [])
                if items:
                    last_log = items[0]
                    season_id = last_log.get('seasonId', '?')
                    
                    # Rank
                    my_standing = None
                    for c in last_log['standings']:
                         raw_tag = c['clan']['tag']
                         if raw_tag.replace('#','').strip().upper() == TARGET_TAG_CLEAN:
                             my_standing = c
                             break
                    
                    if my_standing:
                        war_rank = f"#{my_standing['rank']}"
                        
                        # Participação (Baseado no Log Anterior para ter Ground Truth fechado)
                        for p in my_standing['clan']['participants']:
                            decks = p['decksUsed']
                            if decks >= 4: part_full += 1 
                            elif decks > 0: part_idling += 1
                            else: part_none += 1
        except Exception as e:
            print(f"Erro ao processar status de guerra: {e}")

    # 3. Doações e Top Jogadores (Expandido para Top 10)
    total_donations = 0
    top_donors = []
    
    # Se ja temos members_api carregado e ordenado
    # Recalcular estatísticas frescas
    
    # Ordenar por Doações
    sorted_donations = sorted(members_api, key=lambda x: x['donations'], reverse=True)
    total_donations = sum(m['donations'] for m in members_api)
    top_donors = sorted_donations[:5] # Top 5 (Compact View)
    
    # Ordenar por Troféus (MVPs)
    sorted_trophies = sorted(members_api, key=lambda x: x['trophies'], reverse=True)
    top_trophies = sorted_trophies[:5] # Top 5 (Compact View)


    
    # HTML Construction - PREMIUM UI OVERHAUL (GT-Z 2.2)
    
    def render_player_cards(items, value_key, icon, theme="blue"):
        html = ""
        colors = {
            "blue": "linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%)",
            "gold": "linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%)"
        }
        border_colors = {
            "blue": "rgba(59, 130, 246, 0.3)",
            "gold": "rgba(251, 191, 36, 0.3)"
        }
        
        bg_style = colors.get(theme, colors["blue"])
        border_style = border_colors.get(theme, border_colors["blue"])
        
        for i, p in enumerate(items):
            rank = i + 1
            rank_badge = ""
            if rank <= 3:
                rank_icon = ["🥇", "🥈", "🥉"][rank-1]
                rank_badge = f'<div class="rank-medal">{rank_icon}</div>'
            else:
                rank_badge = f'<div class="rank-number">#{rank}</div>'
                
            html += f"""
            <div class="player-card compact" style="background: {bg_style}; border: 1px solid {border_style};">
                <div class="card-content-wrapper">
                    <div class="card-left">
                        {rank_badge}
                        <div class="player-info">
                            <div class="p-name">{p['name']}</div>
                        </div>
                    </div>
                    <div class="card-right">
                        <div class="p-value">
                            <span class="p-icon">{icon}</span>
                            {p[value_key]}
                        </div>
                    </div>
                </div>
            </div>
            """
        return html
        
    donors_html = render_player_cards(top_donors, 'donations', '🃏', "blue")
    mvp_html = render_player_cards(top_trophies, 'trophies', '🏆', "gold")

    # EXTRAÇÃO DE DADOS HISTÓRICOS PARA O GRÁFICO (MANTIDO)
    chart_dates = []
    chart_scores = []
    
    TARGET_TAG_CLEAN = "9PJRJRPC"

    if os.path.exists(os.path.join(DATA_DIR, 'riverracelog.json')):
        try:
            with open(os.path.join(DATA_DIR, 'riverracelog.json'), 'r', encoding='utf-8') as f:
                r_log = json.load(f)
                items_list = r_log.get('items', [])
                for item in reversed(items_list):
                    my_clan = None
                    for standing in item.get('standings', []):
                        clan_info = standing.get('clan', {})
                        raw_tag = clan_info.get('tag', '')
                        processed_tag = raw_tag.replace('#', '').strip().upper()
                        if processed_tag == TARGET_TAG_CLEAN:
                            my_clan = clan_info
                            break
                    
                    if my_clan:
                        c_date = item.get('createdDate', '')
                        if c_date:
                            try:
                                dt = datetime.strptime(c_date, '%Y%m%dT%H%M%S.%fZ')
                                d_str = dt.strftime('%d/%m')
                                chart_dates.append(d_str)
                                chart_scores.append(my_clan.get('clanScore', 0))
                            except ValueError:
                                try:
                                    dt = datetime.strptime(c_date, '%Y%m%dT%H%M%SZ')
                                    d_str = dt.strftime('%d/%m')
                                    chart_dates.append(d_str)
                                    chart_scores.append(my_clan.get('clanScore', 0))
                                except: pass
        except Exception as e:
            print(f"Erro ao gerar dados do gráfico: {e}")

    js_dates = json.dumps(chart_dates)
    js_scores = json.dumps(chart_scores)

    index_content = f"""
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
    
    <style>
        /* Compact Layout Fixes */
        .player-card.compact {{
            padding: 8px 12px;
            margin-bottom: 6px;
        }}
        .card-content-wrapper {{
            display: flex;
            align-items: center;
            width: 100%;
            gap: 15px; /* Keeps name and value close but separated */
        }}
        
        .card-left {{ display: flex; align-items: center; gap: 10px; flex-shrink: 0; }}
        .rank-medal {{ font-size: 18px; }}
        .rank-number {{ 
            font-size: 12px; font-weight: bold; color: #a0aec0; 
            width: 20px; text-align: center;
        }}
        /* Name truncating if needed, but flex should handle it */
        .p-name {{ font-weight: 700; font-size: 13px; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px; }}
        
        .card-right {{ flex-shrink: 0; }}
        /* Value styling */
        .p-value {{ font-weight: 800; font-size: 13px; color: white; display: flex; align-items: center; gap: 4px; }}
        .p-icon {{ font-size: 14px; }}

        /* Split Columns Grid */
        .split-columns {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }}
        @media (max-width: 768px) {{
            .split-columns {{ grid-template-columns: 1fr; }}
        }}

        /* War Status Visuals */
        .war-status-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }}
        .war-metric-box {{
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border-left: 3px solid #4a5568;
        }}
        .war-metric-box.accent {{ border-left-color: #fbbf24; }}
        .war-metric-label {{ font-size: 11px; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
        .war-metric-value {{ font-size: 20px; font-weight: 800; color: white; }}
    </style>

    <!-- 1. GRÁFICO PREMIUM -->
    <div class="dash-card" style="margin-bottom:20px; border-top: 3px solid #fbbf24; background: linear-gradient(180deg, #1a202c 0%, #171923 100%);">
        <div class="card-header">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:24px">📈</span>
                <div>
                    <h3 style="margin:0; font-size:18px;">Evolução de Troféus</h3>
                    <div style="font-size:12px; color:#718096;">Histórico de Performance do Clã</div>
                </div>
            </div>
            <span class="status-badge status-complete">{league_name}</span>
        </div>
        <div style="position: relative; height:350px; width:100%; padding: 10px;">
            <canvas id="trophyChart"></canvas>
        </div>
    </div>

    <!-- 2. WAR STATUS CARD (Full Width) -->
    <div class="dash-card" style="margin-bottom: 20px; background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%); border: 1px solid #4a5568;">
        <div class="card-header">
            <div>
                <h3 style="color:#fbbf24;">⚔️ Status de Guerra</h3>
                <div style="font-size:11px; color:#a0aec0;">SEASON {season_id}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:10px; color:#a0aec0;">TROFÉUS ATUAIS</div>
                <div style="font-size:24px; font-weight:800; color:#fbbf24;">{clan_war_trophies} 🏆</div>
            </div>
        </div>
        
        <div class="card-body">
            <div class="war-status-container">
                <div class="war-metric-box accent">
                    <div class="war-metric-label">Rank Anterior</div>
                    <div class="war-metric-value">{war_rank}</div>
                </div>
                <div class="war-metric-box" style="border-left-color: #10b981;">
                    <div class="war-metric-label">Participação Total</div>
                    <div class="war-metric-value">{part_full} <span style="font-size:12px; opacity:0.7;">/ 50</span></div>
                </div>
            </div>
            
            <div style="margin-top:20px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <span style="font-size:12px; color:#a0aec0;">Parciais (Incompletos)</span>
                    <span style="font-size:12px; font-weight:bold; color:#fbbf24;">{part_idling}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:12px; color:#a0aec0;">Ausentes (0 Decks)</span>
                    <span style="font-size:12px; font-weight:bold; color:#ef4444;">{part_none}</span>
                    </div>
            </div>
        </div>
    </div>

    <!-- 3 & 4. SIDE BY SIDE LISTS -->
    <div class="split-columns">
        <!-- TOP DOAÇÕES -->
        <div class="dash-card">
            <div class="card-header">
                <h3>🃏 Doadores (Top 5)</h3>
                <span class="badge" style="background:#3182ce;">{total_donations} Cards</span>
            </div>
            <div class="scrollable-list">
                {donors_html}
            </div>
        </div>

        <!-- MVP TROFÉUS -->
        <div class="dash-card">
            <div class="card-header">
                <h3>🏆 Top Ladder (Top 5)</h3>
                <span class="badge" style="background:#d69e2e;">Habilidade</span>
            </div>
            <div class="scrollable-list">
                {mvp_html}
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        Chart.register(ChartDataLabels); // Register Plugin
        
        const ctx = document.getElementById('trophyChart');
        if (ctx) {{
            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: {js_dates},
                    datasets: [{{
                        label: 'Troféus',
                        data: {js_scores},
                        borderColor: '#fbbf24',
                        backgroundColor: (context) => {{
                            const ctx = context.chart.ctx;
                            const gradient = ctx.createLinearGradient(0, 0, 0, 300);
                            gradient.addColorStop(0, 'rgba(251, 191, 36, 0.4)');
                            gradient.addColorStop(1, 'rgba(251, 191, 36, 0.0)');
                            return gradient;
                        }},
                        borderWidth: 3,
                        pointBackgroundColor: '#1a202c',
                        pointBorderColor: '#fbbf24',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8,
                        fill: true,
                        tension: 0.3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {{ padding: {{ top: 30, right: 20, left: 10, bottom: 10 }} }},
                    plugins: {{
                        legend: {{ display: false }},
                        datalabels: {{
                            color: '#fbbf24',
                            align: 'top',
                            offset: 6,
                            font: {{ weight: 'bold', size: 12 }},
                            formatter: function(value) {{ return value; }}
                        }},
                        tooltip: {{
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#fbbf24',
                            padding: 12,
                            displayColors: false,
                            callbacks: {{
                                label: function(context) {{ return '🏆 ' + context.parsed.y; }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            grid: {{ color: 'rgba(45, 55, 72, 0.5)' }},
                            ticks: {{ color: '#a0aec0', font: {{ size: 10 }} }}
                        }},
                        x: {{
                            grid: {{ display: false }},
                            ticks: {{ color: '#a0aec0', font: {{ size: 11 }} }}
                        }}
                    }}
                }}
            }});
        }}
    }});
    </script>
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
                <td data-value="{m['name']}">
                    <div style="font-weight:bold;">{m['name']}</div>
                    <div style="font-size:10px; color:#718096;">{m['tag']}</div>
                </td>
                <td>{role_badge}</td>
                <td data-value="{m['trophies']}"><span style="color:#fbbf24">🏆 {m['trophies']}</span></td>
                <td data-value="{m['donations']}"><span style="color:#34d399"> cards {m['donations']}</span></td>
                <td style="color:#a0aec0" data-value="{m.get('lastSeen', '')}">{last_seen_fmt}</td>
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
                    <td style="font-weight:bold; font-size:16px;" data-value="{rank_pos}">{medal} #{rank_pos}</td>
                    <td style="font-weight:600;" data-value="{r['name']}">{r['name']}</td>
                    <td style="color:#fbbf24; font-weight:800; font-size:18px;" data-value="{r['score']}">{r['score']}</td>
                    <td style="font-size:13px; color:#a0aec0;" data-value="{r['fame']}">
                        Fame: <b style="color:white">{r['fame']}</b><br>
                        Eff: <b style="color:white">{int(r['efficiency'])}</b>
                    </td>
                    <td style="font-size:13px; color:#a0aec0;" data-value="{r['trophies']}">
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

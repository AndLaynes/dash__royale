import os
import json
import requests
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Configurações
CLAN_TAG = "%239PJRJRPC"  # Tag fixa do clã (#9PJRJRPC)
API_BASE_URL = "https://api.clashroyale.com/v1"
API_KEY = os.environ.get("CR_API_KEY")
DATA_DIR = "data"

def get_headers():
    if not API_KEY:
        return None
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

def save_json(data, filename):
    """Salva dados em arquivo JSON no diretório data."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em: {filepath}")

def load_json(filename):
    """Carrega dados de arquivo JSON do diretório data."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            print(f"Carregando cache local: {filepath}")
            return json.load(f)
    return None

def fetch_data(endpoint):
    """Busca dados da API."""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar API ({url}): {e}")
        return None

def get_data_with_cache(endpoint, filename):
    """
    Tenta buscar da API e salvar.
    Se falhar (sem chave, sem net, erro), tenta carregar do cache.
    """
    data = fetch_data(endpoint)
    if data:
        save_json(data, filename)
        return data
    
    print(f"Tentando usar cache local para {filename}...")
    cached_data = load_json(filename)
    if cached_data:
        return cached_data
    
    print(f"AVISO: Não foi possível obter dados para {filename} (nem API, nem Cache).")
    return None

def calculate_league(war_trophies):
    """
    Calcula a liga atual baseado nos troféus de guerra.
    Retorna: (nome_liga, próximo_threshold, troféus_faltantes, progresso_percentual, próxima_liga)
    """
    # Ligas do Clash Royale (baseado em pesquisa)
    leagues = [
        ("Bronze I", 0, 200),
        ("Bronze II", 200, 400),
        ("Bronze III", 400, 600),
        ("Silver I", 600, 900),
        ("Silver II", 900, 1200),
        ("Silver III", 1200, 1500),
        ("Gold I", 1500, 2000),
        ("Gold II", 2000, 2500),
        ("Gold III", 2500, 3000),
        ("Legendary", 3000, 5000)
    ]
    
    current_league = "Bronze I"
    next_league = "Bronze II"
    next_threshold = 200
    current_min = 0
    
    for i, (league_name, min_trophies, max_trophies) in enumerate(leagues):
        if war_trophies >= min_trophies and war_trophies < max_trophies:
            current_league = league_name
            next_threshold = max_trophies
            current_min = min_trophies
            # Próxima liga
            if i + 1 < len(leagues):
                next_league = leagues[i + 1][0]
            else:
                next_league = "Legendary"
            break
        elif war_trophies >= max_trophies:
            current_league = league_name
            next_threshold = max_trophies
            current_min = min_trophies
            if i + 1 < len(leagues):
                next_league = leagues[i + 1][0]
            else:
                next_league = "Legendary"
    
    trophies_to_next = max(0, next_threshold - war_trophies)
    
    # Calcular progresso percentual dentro da liga atual
    league_range = next_threshold - current_min
    if league_range > 0:
        progress_in_league = war_trophies - current_min
        progress_pct = min(100, (progress_in_league / league_range) * 100)
    else:
        progress_pct = 100
    
    return current_league, next_threshold, trophies_to_next, int(progress_pct), next_league

def get_war_day_status():
    """
    Determina o status da guerra baseado no dia da semana (Retrospectivo).
    O script roda no dia X para auditar o dia X-1.
    
    0 = Segunda (Audita Domingo - Fim)
    1 = Terça (Treino)
    2 = Quarta (Treino)
    3 = Quinta (Treino/Início)
    4 = Sexta (Audita Quinta - Dia 1)
    5 = Sábado (Audita Sexta - Dia 2)
    6 = Domingo (Audita Sábado - Dia 3)
    """
    today = datetime.now().weekday()
    
    # Mapeamento de auditoria
    audit_map = {
        4: {"target": 4, "day_name": "Quinta-feira (Dia 1)", "is_audit": True},
        5: {"target": 8, "day_name": "Sexta-feira (Dia 2)", "is_audit": True},
        6: {"target": 12, "day_name": "Sábado (Dia 3)", "is_audit": True},
        0: {"target": 16, "day_name": "Domingo (Dia 4 - Final)", "is_audit": True}
    }
    
    if today in audit_map:
        return audit_map[today]
    
    return {"target": 0, "day_name": "Dia de Treino", "is_audit": False}

def main():
    print("=== JULES Squad: Clash Royale Dashboard Generator ===")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # 1. Obter dados (API -> Cache -> Memória)
    # Normaliza tag para uso na API se necessário (embora a URL use %23)
    # A URL precisa de %23. O endpoint é /clans/%23TAG
    
    clan_info = get_data_with_cache(f"/clans/{CLAN_TAG}", "clan_info.json")
    current_war = get_data_with_cache(f"/clans/{CLAN_TAG}/currentriverrace", "current_war.json")
    war_log = get_data_with_cache(f"/clans/{CLAN_TAG}/riverracelog?limit=20", "war_log.json")
    
    if not clan_info:
        print("ERRO CRÍTICO: Não há dados do clã para gerar o dashboard.")
        return

    # Dados processados para o template
    context = {
        "clan": clan_info,
        "war": current_war,
        "war_log": war_log,
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    # 2. Configurar Jinja2
    env = Environment(loader=FileSystemLoader("templates"))
    template_index = env.get_template("index.html")
    template_history = env.get_template("war_history.html")
    template_members = env.get_template("members_stats.html")
    template_ranking = env.get_template("ranking.html")

    # 3. Renderizar HTML Index
    html_content_index = template_index.render(context)
    
    # 3.5 Processar dados de Membros
    members_context = {"clan": clan_info}
    if clan_info and "memberList" in clan_info:
        members = clan_info["memberList"]
        
        # Calcular estatísticas
        total_donations = sum(m.get("donations", 0) for m in members)
        avg_trophies = int(sum(m.get("trophies", 0) for m in members) / len(members)) if members else 0
        
        # Calcular dias offline (mockado, API não fornece isso diretamente em memberList)
        # Pode ser calculado se tivermos battleLog ou outro endpoint
        for member in members:
            # Placeholder - em produção, seria calculado via lastSeenTime ou battleLog
            member["lastSeen"] = 0  # 0 = online hoje
        
        members_context.update({
            "members": members,
            "total_donations": total_donations,
            "avg_trophies": avg_trophies
        })
    
    html_content_members = template_members.render(members_context)
    
    # 5.5 Processar Ranking
    ranking_context = {"clan": clan_info, "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}
    if clan_info and "memberList" in clan_info:
        members = clan_info["memberList"]
        sorted_by_trophies = sorted(members, key=lambda x: x.get("trophies", 0), reverse=True)
        
        for member in members:
            member["war_score"] = member.get("donations", 0) * 10 + member.get("trophies", 0) // 100
        
        # Preparar dados para o gráfico (top 10)
        top_10 = sorted_by_trophies[:10]
        ranking_chart_data = {
            "labels": [p["name"][:10] + "..." if len(p["name"]) > 10 else p["name"] for p in top_10],
            "trophies": [p.get("trophies", 0) for p in top_10]
        }
        
        ranking_context.update({
            "top_players": sorted_by_trophies[:3],
            "all_players": sorted_by_trophies,
            "ranking_chart_data": ranking_chart_data
        })
    
    html_content_ranking = template_ranking.render(ranking_context)

    # 5.6 Processar Acompanhamento Diário (Auditoria)
    audit_status = get_war_day_status()
    daily_context = {
        "clan": clan_info, 
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "audit": audit_status
    }
    
    if audit_status["is_audit"]:
        # Criar mapa de decks usados pelos participantes da guerra
        participants_decks = {}
        if current_war and "clan" in current_war and "participants" in current_war["clan"]:
            for p in current_war["clan"]["participants"]:
                participants_decks[p["tag"]] = p["decksUsed"]
        
        audit_list = []
        if clan_info and "memberList" in clan_info:
            for member in clan_info["memberList"]:
                tag = member["tag"]
                decks_used = participants_decks.get(tag, 0)
                target = audit_status["target"]
                
                # Definir Status
                if decks_used >= target:
                    status = "ok"
                    status_text = "Em Dia"
                elif decks_used > 0:
                    status = "warning"
                    status_text = "Incompleto"
                else:
                    status = "critical"
                    status_text = "Zerado"
                
                audit_list.append({
                    "name": member["name"],
                    "tag": tag,
                    "role": member["role"],
                    "decks_used": decks_used,
                    "decks_missing": max(0, target - decks_used),
                    "status": status,
                    "status_text": status_text
                })
        
        # Ordenar: Críticos primeiro, depois Warning, depois OK
        # Dentro do status, ordenar por decks faltantes (desc)
        audit_list.sort(key=lambda x: (
            0 if x["status"] == "critical" else 1 if x["status"] == "warning" else 2, 
            -x["decks_missing"]
        ))
        
        daily_context["audit_list"] = audit_list
        
        # Contadores
        daily_context["count_ok"] = sum(1 for x in audit_list if x["status"] == "ok")
        daily_context["count_warning"] = sum(1 for x in audit_list if x["status"] == "warning")
        daily_context["count_critical"] = sum(1 for x in audit_list if x["status"] == "critical")

    template_daily = env.get_template("daily_war.html")
    html_content_daily = template_daily.render(daily_context)

    # 4. Processar Histórico de Guerra (Última Guerra)
    history_context = {"clan": clan_info, "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M")}
    
    # Calcular Liga baseada em troféus de guerra
    war_trophies = clan_info.get("clanWarTrophies", 0) if clan_info else 0
    league_name, next_threshold, trophies_to_next, progress_pct, next_league_name = calculate_league(war_trophies)
    
    # Processar dados históricos para o gráfico (Pontuação do Clã)
    war_chart_data = {"labels": [], "scores": []}
    if war_log and "items" in war_log:
        # Limitar às últimas 10 guerras para o gráfico
        recent_wars = war_log["items"][:10]
        recent_wars.reverse()  # Ordem cronológica
        
        target_tag = CLAN_TAG.replace("%23", "#")
        for idx, war in enumerate(recent_wars):
            my_clan_data = next((s for s in war.get("standings", []) if s.get("clan", {}).get("tag") == target_tag), None)
            if my_clan_data:
                season_id = war.get('seasonId', 0)
                section_index = war.get('sectionIndex', idx+1)
                # Formato: "Temporada X - Seção Y"
                label = f"T{season_id}-S{section_index}"
                war_chart_data["labels"].append(label)
                war_chart_data["scores"].append(my_clan_data["clan"].get("clanScore", 0))
    
    history_context.update({
        "league_name": league_name,
        "next_league_name": next_league_name,
        "next_league_threshold": next_threshold,
        "trophies_to_next": trophies_to_next,
        "league_progress": progress_pct,
        "war_chart_data": war_chart_data
    })
    
    # Processar última guerra
    last_war = None
    if war_log and "items" in war_log and len(war_log["items"]) > 0:
        last_war = war_log["items"][0]
    
    if last_war:
        participants = []
        
        # Encontrar o clã na lista de standings
        # A API retorna a tag com #, mas nossa constante pode estar com %23
        target_tag = CLAN_TAG.replace("%23", "#")
        
        my_clan_standing = next((s for s in last_war["standings"] if s["clan"]["tag"] == target_tag), None)
        
        if my_clan_standing:
            if "participants" in my_clan_standing["clan"]:
                war_participants = my_clan_standing["clan"]["participants"]
                
                # CORREÇÃO CRÍTICA: Filtrar apenas jogadores ATIVOS do clã
                # Criar set de tags de membros ativos
                active_member_tags = set()
                if clan_info and "memberList" in clan_info:
                    active_member_tags = {member["tag"] for member in clan_info["memberList"]}
                
                # Filtrar participantes da guerra que são membros ativos
                clan_participants = [p for p in war_participants if p["tag"] in active_member_tags]
                
                print(f"Total de participantes na guerra: {len(war_participants)}")
                print(f"Participantes ativos (membros atuais): {len(clan_participants)}")
            else:
                clan_participants = []
            
            for p in clan_participants:
                decks_used = p["decksUsed"]
                
                # Lógica de Classificação
                status_label = "Perigo"
                status_class = "danger"
                
                if decks_used == 16:
                    status_label = "Campeão"
                    status_class = "champion"
                elif 12 <= decks_used <= 15:
                    status_label = "Atenção"
                    status_class = "warning"
                
                participants.append({
                    "name": p["name"],
                    "tag": p["tag"],
                    "decksUsed": decks_used,
                    "fame": p["fame"],
                    "status_label": status_label,
                    "status_class": status_class
                })
            
            # Ordenar por decks usados (desc) e depois fama (desc)
            participants.sort(key=lambda x: (x["decksUsed"], x["fame"]), reverse=True)
            
            history_context.update({
                "season_id": last_war["seasonId"],
                "section_index": last_war["sectionIndex"],
                "participants": participants
            })
    else:
        print("Aviso: Nenhum histórico de guerra encontrado para gerar a tabela detalhada.")

    # 5. Renderizar HTML Histórico
    html_content_history = template_history.render(history_context)

    # 6. Salvar arquivos
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content_index)
    
    with open("war_history.html", "w", encoding="utf-8") as f:
        f.write(html_content_history)
    
    with open("members_stats.html", "w", encoding="utf-8") as f:
        f.write(html_content_members)
    
    with open("ranking.html", "w", encoding="utf-8") as f:
        f.write(html_content_ranking)

    with open("daily_war.html", "w", encoding="utf-8") as f:
        f.write(html_content_daily)
    
    print(f"\n=== SUCESSO ===")
    print(f"Arquivos gerados:")
    print(f"1. {os.path.abspath('index.html')}")
    print(f"2. {os.path.abspath('war_history.html')}")
    print(f"3. {os.path.abspath('members_stats.html')}")
    print(f"4. {os.path.abspath('ranking.html')}")
    print(f"Dados brutos salvos em: {os.path.abspath(DATA_DIR)}")

if __name__ == "__main__":
    main()

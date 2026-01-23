# GROUND TRUTH: Métrica de Guerra (Clash Royale)

## 1. Calendário Oficial
A Guerra de Clãs (River Race) segue um ciclo estrito de 7 dias.

*   **Dias de Treino (Training Days)**: Segunda, Terça, Quarta.
    *   **STATUS**: ❌ **NÃO CONTABILIZAR**.
    *   Ações nestes dias não contam para pontos de guerra.
*   **Dias de Batalha (War Days)**: Quinta, Sexta, Sábado, Domingo.
    *   **STATUS**: ✅ **CONTABILIZAR STRICTAMENTE**.
    *   Estes são os únicos dias que geram dados para o Dashboard.

## 2. Regras de Decks (Meta Híbrida: Online + D-1)
A lógica de auditoria combina o histórico consolidado (D-1) com a atividade em tempo real (Online).

*   **QUINTA-FEIRA (Início):**
    *   **Lógica:** 4 Decks (Online).
    *   **Meta:** 4.
    *   *Nota:* Não há D-1. Apenas o que é feito no dia conta.

*   **SEXTA-FEIRA:**
    *   **Lógica:** 4 Decks (D-1 / Quinta) + 4 Decks (Online / Sexta).
    *   **Meta:** 8.

*   **SÁBADO:**
    *   **Lógica:** 8 Decks (D-1 / Qui+Sex) + 4 Decks (Online / Sábado).
    *   **Meta:** 12.

*   **DOMINGO (Final):**
    *   **Lógica:** 12 Decks (D-1 / Qui+Sex+Sáb) + 4 Decks (Online / Domingo).
    *   **Meta:** 16.

*   **SEGUNDA-FEIRA (Fechamento):**
    *   **Lógica:** Auditoria Final da semana anterior.
    *   **Meta:** 16.
    *   *Nota:* Após a primeira atualização de segunda-feira, qualquer dado é inválido.

*   **TERÇA & QUARTA (Congelamento):**
    *   **Status:** INVÁLIDO.
    *   O sistema não deve gerar novas métricas de guerra nestes dias. Aguardar a próxima quinta-feira.

## 3. Lógica do Dashboard (Hard Constraints)
O código deve determinar o que exibir baseado no dia da semana atual:

1.  **Segunda, Terça, Quarta (Dias de Treino)**:
    *   **Exibir**: Dados da **Última Guerra Encerrada** (Total de Quinta-Domingo da semana anterior).
    *   **Não Atualizar**: Não inserir "0 decks" no histórico para estes dias. Ignorar dados da API de "currentriverrace" se estiver em 'training'.

2.  **Quinta (Dia 1 de Guerra)**:
    *   **Exibir**: Dados parciais de Quinta.
    *   **Meta**: 4.

3.  **Sexta (Dia 2 de Guerra)**:
    *   **Exibir**: Soma de Quinta + Sexta.
    *   **Meta**: 8.

## 4. Ranking Algorithm (Score Logic)
O Score de Performance (0-100) é calculado pela média ponderada normalizada das métricas relativas ao Máximo do Clã.

| Métrica | Peso | Justificativa |
| :--- | :--- | :--- |
| **Fama (Ouro)** | **50%** | Objetivo Primário da Guerra. |
| **Eficiência** | **25%** | Qualidade do Deck (Vitórias). |
| **Troféus** | **15%** | Habilidade Individual (Ladder). |
| **Doações** | **10%** | Contribuição Social. |

**Nota de Auditoria (23/01/2026):**
Um jogador com **menos troféus** pode estar acima de um com mais troféus se sua Fama for significativamente maior (Peso 50% vs 15%). Isso é comportamento esperado e validado.

## 5. Fonte de Verdade (Falha de API)
Se a API não retornar dados de guerra (ex: bug ou manutenção) em um dia de batalha, deve-se manter os dados do último "checkpoint" válido no `daily_war_history.json`.

---
*Documento gerado sob diretriz estrita do usuário. Referência Oficial.*

# GROUND TRUTH: Métrica de Guerra (Clash Royale)

## 1. Calendário Oficial
A Guerra de Clãs (River Race) segue um ciclo estrito de 7 dias.

*   **Dias de Treino (Training Days)**: Segunda, Terça, Quarta.
    *   **STATUS**: ❌ **NÃO CONTABILIZAR**.
    *   Ações nestes dias não contam para pontos de guerra.
*   **Dias de Batalha (War Days)**: Quinta, Sexta, Sábado, Domingo.
    *   **STATUS**: ✅ **CONTABILIZAR STRICTAMENTE**.
    *   Estes são os únicos dias que geram dados para o Dashboard.

## 2. Regras de Decks (Meta)
O limite de decks é diário e não cumulativo para execução, mas cumulativo para auditoria.

*   **Limite Diário**: 4 Decks.
*   **Meta Acumulada (Soma Esperada no Dashboard):**
    *   **Quinta**: 4 Decks.
    *   **Sexta**: 8 Decks (4 de Qui + 4 de Sex).
    *   **Sábado**: 12 Decks.
    *   **Domingo**: 16 Decks (Meta Final).

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

## 4. Fonte de Verdade (Falha de API)
Se a API não retornar dados de guerra (ex: bug ou manutenção) em um dia de batalha, deve-se manter os dados do último "checkpoint" válido no `daily_war_history.json`.

---
*Documento gerado sob diretriz estrita do usuário. Referência Oficial.*

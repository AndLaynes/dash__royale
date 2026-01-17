# PROTOCOLO DE AUDITORIA DE GUERRA: DEFINIÇÃO MATEMÁTICA E LÓGICA (AI_WAR_METRIC_PROTOCOL)
**Target:** Agentes de IA, LLMs e Auditores Humanos.
**Contexto:** Dash Royale (Supercell API Integration).
**Diretriz:** Ground Truth Zero-Trust (GT-Z).
**Versão:** 1.0.0

---

## 1. O CICLO TEMPORAL DA GUERRA (HARD CONSTRAINT)
O evento "River Race" (Guerra de Clãs) ocorre em um ciclo **imutável** de 4 dias de batalha ativa. O entendimento deste ciclo é pré-requisito para qualquer análise de dados.

| Dia da Semana | Tipo de Evento | Status do Sistema | Ação do Agente |
| :--- | :--- | :--- | :--- |
| **Segunda (Mon)** | **Encerramento** | `War End / Cooldown` | **Auditoria Final** (Consolida Dom) |
| **Terça (Tue)** | Treino | `Training` | Ignorar (Dados Irrelevantes) |
| **Quarta (Wed)** | Treino | `Training` | Ignorar (Dados Irrelevantes) |
| **Quinta (Thu)** | **Guerra: Dia 1** | `War Active` | Coleta Parcial (Audita sex) |
| **Sexta (Fri)** | **Guerra: Dia 2** | `War Active` | **Audita Quinta (D-1)** |
| **Sábado (Sat)** | **Guerra: Dia 3** | `War Active` | **Audita Sexta (D-1)** |
| **Domingo (Sun)** | **Guerra: Dia 4** | `War Active` | **Audita Sábado (D-1)** |

> **NOTA CRÍTICA:** A Segunda-feira é o dia da "Verdade Final". Ela captura o que aconteceu no Domingo.

---

## 2. A REGRA DO "D-1" (RETROSPECTIVE AUDIT)
Para garantir a integridade dos dados, **nunca** auditamos o dia "corrente" como verdade absoluta durante a execução do relatório de conformidade, pois o dia ainda não acabou. Auditamos o dia **anterior** que já foi encerrado (Snapshot Fechado).

### Fórmula de Auditoria Diária
Se `HOJE` é o dia da execução do script:

1.  **SE HOJE = SEXTA (Friday):**
    *   **Alvo da Auditoria:** Quinta-feira (Thursday).
    *   **Meta de Decks:** 4.
    *   **Lógica de Dados:** Ler chave `"YYYY-MM-DD"` correspondente à Quinta no JSON de histórico. **NÃO USAR** o total acumulado da API se ele incluir decks de sexta.

2.  **SE HOJE = SÁBADO (Saturday):**
    *   **Alvo da Auditoria:** Sexta-feira (Friday).
    *   **Meta de Decks:** 8 (Acumulado: 4 Qui + 4 Sex).
    *   **Lógica de Dados:** Somar chaves de Quinta + Sexta.

3.  **SE HOJE = DOMINGO (Sunday):**
    *   **Alvo da Auditoria:** Sábado (Saturday).
    *   **Meta de Decks:** 12 (Acumulado: 4 Qui + 4 Sex + 4 Sáb).

4.  **SE HOJE = SEGUNDA (Monday):**
    *   **Alvo da Auditoria:** Domingo (Sunday - Fim da Guerra).
    *   **Meta de Decks:** 16 (Full War).
    *   **Status:** "MISSÃO CUMPRIDA" ou "FALHA".

---

## 3. O MECANISMO DE SNAPSHOT (A EVIDÊNCIA)
O sistema **não deve alucinar** subtrações. Ele deve ler o arquivo de persistência local:
`e:/dash__royale/dash__royale/data/daily_war_history.json`

### Estrutura Obrigatória do JSON (Exemplo Real Validado)
```json
"players": {
    "#TAG_DO_JOGADOR": {
        "name": "NOME",
        "history": {
            "2026-01-15": 4,  // Quinta (Fixo/Travado)
            "2026-01-16": 4   // Sexta  (Em progresso ou Travado)
        }
    }
}
```

**Regra de Ouro para IAs:**
*   Se você quer saber se o jogador está "EM DIA" na SEXTA para a meta de QUINTA:
    *   **LEIA APENAS:** `history["2026-01-15"]`.
    *   **META:** 4.
    *   **IGNRE:** `history["2026-01-16"]` (O que ele fez hoje não salva o erro de ontem para fins de disciplina).

---

## 4. O ALGORITMO DA META (DYNAMIC TARGET)
A meta não é estática. Ela evolui com o dia da semana.

`MetaDecks = (DiaDaSemana_Index - 2) * 4`
*(Onde Segunda=0, Terça=1... Quinta=3, Sexta=4)*

*   **Exemplo Sexta (4):** `(4 - 2) * 4 = 2 * 4 = 8`.
    *   *Correção de Contexto:* Se estamos auditando "Até ontem", o script ajusta o Index.

---

## 5. ESTADO "ZERADO" (CRITICAL FLAG)
Um jogador é considerado `ZERADO` se, e somente se:
*   `Sum(history.values()) == 0`
*   ISTO É UMA BANDEIRA VERMELHA DE EXPULSÃO.

> **ASSINATURA DO PROTOCOLO:**
> Documento gerado sob o protocolo GT-Z para alinhamento de contexto de IA.
> Qualquer desvio desta lógica constitui uma "Alucinação de Métrica".

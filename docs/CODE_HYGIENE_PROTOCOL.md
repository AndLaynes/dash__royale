# PROTOCOLO DE HIGIENE DE CÓDIGO (CLEAN CODE POLICY)
**Versão:** 1.0.0
**Status:** ATIVO
**Aplicação:** Todo o código fonte do Dash Royale (Python, HTML, CSS, JS).

## 1. PRINCÍPIO "CODE IS NOT A PLACE FOR DEATH"
O código deve ser limpo, profissional e compatível com qualquer infraestrutura (Legacy ou Modern).

### 📐 REGRA 1: Proibição de Emojis em Lógica (Zero Tolerance)
*   **Proibido:** Usar emojis (⚠️, ✅, ❌, etc.) dentro de strings de log, variáveis, comentários críticos ou saídas de console.
*   **Motivo:** Emojis dependem de `chcp 65001` (UTF-8). Servidores Windows Server antigos ou containers minimalistas podem rodar em `cp1252` ou ASCII puro, causando o crash `UnicodeEncodeError`.
*   **Exceção:** Emojis são permitidos EXCLUSIVAMENTE em arquivos `.html` (Front-end) onde o charset é definido via `<meta charset="UTF-8">`.

### 🚨 REGRA 2: Caracteres ASCII-Only em Logs
Os logs de sistema devem ser puramente textuais para garantir auditabilidade em qualquer visualizador de texto.

**Tabela de Substituição Padrão:**
| Emoji Ruim | Texto Bom | Significado |
| :--- | :--- | :--- |
| ⚠️ | `[!]` ou `[WARN]` | Alerta / Perigo |
| ❌ | `[x]` ou `[ERR]` | Erro / Falha |
| ✅ | `[v]` ou `[OK]` | Sucesso |
| 🚀 | `[>]` | Início / Deploy |

## 2. AUDITORIA DE LLM (HARD CONSTRAINT)
Ao gerar código via AI, o Agente DEVE filtrar qualquer "decoração" estética que a IA tente inserir no stdout.

> **ASSINATURA:** Protocolo implementado após Incidente `charmap codec` de 17/01/2026.

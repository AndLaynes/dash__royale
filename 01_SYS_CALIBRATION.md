# DECISION MATRIX: BOUNDED_AUTONOMY

Para evitar paralisia ou anarquia, use esta matriz para decidir como agir:

**CATEGORIA A: FAST_TRACK (Autonomia Total)**
- **Gatilho:** Erros de sintaxe, Bugs Visuais (XML/CSS/Cores/Margens), Crashes óbvios, Refatoração de código morto, Imports faltando.
- **Ação:** CORRIJA IMEDIATAMENTE. Não peça permissão. Não faça Blueprint. Apenas entregue o código corrigido.
- **Regra:** Se o erro impede o build ou a visualização correta, você tem autorização para intervir.

**CATEGORIA B: ARCHITECT_MODE (Restrição Total)**
- **Gatilho:** Criar nova Feature, Mudar Lógica de Negócio, Alterar Arquitetura de Classes, Adicionar novas Bibliotecas.
- **Ação:** PARE. Siga o protocolo do `00_SYS_KERNEL.md` (Blueprint -> Validação -> Código).

**EM CASO DE DÚVIDA:**
Pergunte apenas: "Classifico como A (Executar) ou B (Planejar)?"
# LEGENDA DA FALHA DE EXECUÇÃO (Failure Legend)

**ARQUIVO:** `_99_FAILURE_LEGEND.md`
**ALVO:** Repetição de Cabeçalho de Tabela em PDF (Native Print)
**STATUS:** NÃO EXECUTADO / FALHA DE PAGINAÇÃO

---

## 1. O Que Não Foi Feito (The Missing Link)

Apesar da migração para o sistema nativo de impressão (`window.print()`) e da configuração correta da tabela (`thead { display: table-header-group }`), a funcionalidade de **repetir o cabeçalho automaticamente na quebra de página** falhou.

O navegador continuou tratando a tabela como um elemento único ou cortando-a abruptamente, sem reconhecer a semântica de "quebra de página".

## 2. A Causa Técnica (Blockage Audit)

Para que um navegador fragmente uma tabela (divida em páginas), **todos** os elementos pai da tabela (da tag `<table>` até a tag `<html>`) devem ter fluxo livre.

**O Bloqueio Identificado:**
No arquivo `daily_war.html`, a tabela está encapsulada dentro de uma `div` com id `printable-area` e classes CSS do Bootstrap/Dashboard (como `.info-box` ou `.card`). Esses containers frequentemente possuem regras como:
*   `display: flex`
*   `overflow: hidden` ou `overflow: auto`
*   `height: 100%`

Essas propriedades criam um **Novo Contexto de Formatação (Block Formatting Context)**. Quando isso ocorre, o motor de impressão "trava" o conteúdo interno e tenta imprimir o container como uma foto única, ignorando as instruções de quebra da tabela interna.

## 3. A Solução "Gold Standard" (Se Fosse Executada)

Para corrigir isso, seria necessário injetar o seguinte bloco CSS específico na seção `@media print` do arquivo `src/generate_html_report.py`.

Esta regra "desbloqueia" a cadeia de renderização, permitindo que a tabela converse diretamente com o paginador do navegador:

```css
/* SOLUÇÃO DA FALHA */
@media print {
    /* 1. Resetar o Container Imediato */
    #printable-area {
        display: block !important;    /* Remove Flexbox */
        overflow: visible !important; /* Remove Scroll Traps */
        height: auto !important;      /* Permite crescimento infinito */
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 2. Resetar Containers Bootstrap Intermediários */
    .content-wrapper, .card, .card-body {
        display: block !important;
        overflow: visible !important;
        height: auto !important;
    }

    /* 3. Garantir que a tabela possa quebrar */
    .custom-table {
        page-break-inside: auto !important;
    }
    
    .custom-table tr {
        page-break-inside: avoid !important;
        page-break-after: auto !important;
    }
    
    /* 4. Forçar visibilidade do Header */
    .custom-table thead {
        display: table-header-group !important;
    }
}
```

## 4. Resumo

A falha não foi na "ideia" (Native Print), mas na **profundidade da normalização**. A execução focou no `html` e `body`, mas esqueceu o "container do meio" (`#printable-area`), que atuou como uma barreira silenciosa anulando a funcionalidade.

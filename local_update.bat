@echo off
chcp 65001 > nul
title DASH ROYALE :: MANUAL UPDATE BOT
color 0A

echo ========================================================
echo     DASH ROYALE -- SISTEMA DE ATUALIZACAO MANUAL
echo     PROTOCOLO GT-Z :: AMBIENTE LOCAL
echo ========================================================
echo.

echo [1/3] Sincronizando com a Nuvem (Git Pull)...
echo       Isso garante que trabalho do robo online nao seja perdido.
git pull origin main
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERRO CRITICO] Falha ao sincronizar com o GitHub.
    echo Possivel conflito de arquivos ou falta de internet.
    echo Resolva o conflito antes de prosseguir.
    pause
    exit /b %errorlevel%
)
echo [OK] Repositorio sincronizado.
echo.

echo [2/3] Executando Pipeline de Dados (Python)...
echo       - get_data.py
echo       - process_data.py
echo       - generate_html_report.py
echo       - git_auto_sync (Push automatico)
python run_update.py
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERRO CRITICO] O pipeline de atualizacao falhou.
    echo Verifique os logs acima.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/3] Ciclo Completo.
echo ========================================================
echo     STATUS: OPERACAO REALIZADA COM SUCESSO
echo     O painel esta atualizado e sincronizado.
echo ========================================================
pause

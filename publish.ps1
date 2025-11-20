# 1. Atualizar dados da Supercell (Gera novos HTMLs)
# Tenta pegar a chave do ambiente de usuário, se não existir, assume que já está na sessão
if (-not $env:CR_API_KEY) {
    $env:CR_API_KEY = [System.Environment]::GetEnvironmentVariable('CR_API_KEY', 'User')
}
python main.py

# 2. Enviar para o GitHub
git add .
git commit -m "🔄 Update dashboard data: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin master

Write-Host "`n✅ Publicado com sucesso! Acesse: https://andlaynes.github.io/dash__royale/" -ForegroundColor Green

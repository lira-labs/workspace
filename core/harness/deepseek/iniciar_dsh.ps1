# ==============================================================================
# SCRIPT DE INICIALIZAÇÃO · DEEPSEEK HARNESS (DSH) WEB UI
# ==============================================================================

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "🤖 INICIANDO DEEPSEEK HARNESS (DSH) · GRAFOPARADA AUDITOR CÉTICO" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Carregando o servidor web local do DeepSeek Harness..." -ForegroundColor Yellow
Write-Host "Acesse o painel web no seu navegador quando a URL aparecer abaixo." -ForegroundColor Gray
Write-Host ""

npx --yes @deepseek-ai/dsh web

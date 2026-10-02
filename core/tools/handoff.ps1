<#
.SYNOPSIS
    Script de automacao para sincronizacao e Handoff entre Notebook e PC.
.DESCRIPTION
    Suporta:
    - -Pull   : Sincroniza alteracoes do GitHub (git pull) e exibe o estado do HANDOFF.md.
    - -Push   : Atualiza metadados do HANDOFF.md, adiciona alteracoes, commita e envia (git push).
    - -Status : Verifica divergencias locais e remotas.
.EXAMPLE
    .\core\tools\handoff.ps1 -Pull
    .\core\tools\handoff.ps1 -Push -Message "feat: conclui modulo de visualizacao"
#>
param(
    [switch]$Pull,
    [switch]$Push,
    [switch]$Status,
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"

$workspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$handoffPath = Join-Path $workspaceRoot "HANDOFF.md"

if (-not (Test-Path $handoffPath)) {
    Write-Error "Arquivo HANDOFF.md nao encontrado em $handoffPath"
    exit 1
}

$gitCmd = "git"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    $minGitPath = "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe"
    if (Test-Path $minGitPath) {
        $gitCmd = $minGitPath
    } else {
        Write-Error "Git nao encontrado no sistema."
        exit 1
    }
}

function Get-ActiveBranch {
    return (& $gitCmd -C $workspaceRoot rev-parse --abbrev-ref HEAD).Trim()
}

# 1. MODO STATUS
if ($Status) {
    $branch = Get-ActiveBranch
    Write-Host "[HANDOFF STATUS] Workspace: $workspaceRoot" -ForegroundColor Cyan
    Write-Host "Branch atual: $branch" -ForegroundColor Cyan
    & $gitCmd -C $workspaceRoot status -s
    exit 0
}

# 2. MODO PULL (Inicio de sessao)
if ($Pull -or (-not $Push)) {
    $branch = Get-ActiveBranch
    Write-Host "[HANDOFF] Sincronizando com GitHub (Branch: $branch)..." -ForegroundColor Cyan
    
    $hasChanges = [bool](& $gitCmd -C $workspaceRoot status --porcelain)
    if ($hasChanges) {
        Write-Host "Guardando alteracoes locais temporariamente..." -ForegroundColor Yellow
        & $gitCmd -C $workspaceRoot stash -u
    }
    try {
        & $gitCmd -C $workspaceRoot pull origin $branch
        Write-Host "Sincronizacao com GitHub concluida com sucesso!" -ForegroundColor Green
    } catch {
        Write-Warning "Aviso ao executar git pull: $_"
    } finally {
        if ($hasChanges) {
            Write-Host "Restaurando alteracoes locais..." -ForegroundColor Yellow
            & $gitCmd -C $workspaceRoot stash pop
        }
    }

    Write-Host "`n[HANDOFF] Resumo da Ultima Sessao:" -ForegroundColor Yellow
    $lines = Get-Content -Path $handoffPath -Encoding UTF8
    $capture = $false
    foreach ($line in $lines) {
        if ($line -match "^##\s+.*Metadata|^##\s+.*Metadados") {
            $capture = $true
        } elseif ($capture -and $line -match "^##\s+") {
            $capture = $false
        }
        if ($capture) {
            Write-Host $line -ForegroundColor Gray
        }
    }
    
    if (-not $Push) { exit 0 }
}

# 3. MODO PUSH (Final de sessao / marco)
if ($Push) {
    $branch = Get-ActiveBranch
    $nowStr = (Get-Date).ToString("dd/MM/yyyy HH:mm")
    
    Write-Host "[HANDOFF] Atualizando metadados em HANDOFF.md..." -ForegroundColor Cyan
    
    $lines = Get-Content -Path $handoffPath -Encoding UTF8
    $updatedLines = @()
    foreach ($line in $lines) {
        if ($line -match "^\s*-\s*\*\*.*Atualiza") {
            $updatedLines += "- **Ultima Atualizacao:** $nowStr"
        } elseif ($line -match "^\s*-\s*\*\*Branch Ativo") {
            $updatedLines += "- **Branch Ativo:** ``$branch``"
        } else {
            $updatedLines += $line
        }
    }
    
    [System.IO.File]::WriteAllLines($handoffPath, $updatedLines, [System.Text.Encoding]::UTF8)
    Write-Host "Metadados atualizados para: $nowStr" -ForegroundColor Green

    Write-Host "[HANDOFF] Preparando commit e push..." -ForegroundColor Cyan
    & $gitCmd -C $workspaceRoot add .

    $commitMsg = if ($Message) { $Message } else { "chore: auto-handoff sync ($nowStr)" }
    
    $statusOutput = & $gitCmd -C $workspaceRoot status --porcelain
    if ($statusOutput) {
        & $gitCmd -C $workspaceRoot commit -m $commitMsg
        Write-Host "Commit realizado: '$commitMsg'" -ForegroundColor Green
    } else {
        Write-Host "Nenhuma alteracao de arquivos pendente para commitar." -ForegroundColor Yellow
    }

    Write-Host "Enviando para GitHub ($branch)..." -ForegroundColor Cyan
    & $gitCmd -C $workspaceRoot push origin $branch
    Write-Host "Handoff concluido e enviado com sucesso ao GitHub!" -ForegroundColor Green
}

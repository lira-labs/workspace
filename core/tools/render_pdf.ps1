# Script de Exportacao Headless Edge para PDF A4 Perfeito
$ErrorActionPreference = 'Stop'

$html = (Resolve-Path 'code/projeto_ead_tutores/ebook-hq.html').Path
$pdf = [System.IO.Path]::GetFullPath('code/projeto_ead_tutores/assets/ebook-operacao-byte-socratico.pdf')
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path $edge)) {
    $edge = 'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
}

Write-Host "Edge encontrado em: $edge"
Write-Host "HTML de entrada: $html"
Write-Host "PDF de saida: $pdf"

if (Test-Path $pdf) {
    Remove-Item $pdf -Force -ErrorAction SilentlyContinue
}

$argList = @(
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    '--print-to-pdf-no-header',
    '--run-all-compositor-stages-before-draw',
    '--virtual-time-budget=12000',
    "--print-to-pdf=$pdf",
    "file:///$html"
)

Write-Host "Iniciando renderizacao do PDF via Edge..."
$proc = Start-Process -FilePath $edge -ArgumentList $argList -PassThru -Wait
Write-Host "Processo concluido com codigo: $($proc.ExitCode)"

if (Test-Path $pdf) {
    $len = (Get-Item $pdf).Length / 1MB
    Write-Host ("PDF gerado com sucesso! Tamanho: {0:N2} MB" -f $len)
} else {
    Write-Error "Falha: PDF nao foi criado!"
}

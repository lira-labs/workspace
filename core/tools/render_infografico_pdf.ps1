# Script de Renderizacao do Poster Infografico em PDF
$ErrorActionPreference = 'Stop'

$html = (Resolve-Path 'code/projeto_ead_tutores/infografico.html').Path
$pdf = [System.IO.Path]::GetFullPath('code/projeto_ead_tutores/assets/infografico-anatomia-tutor-ia.pdf')
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path $edge)) {
    $edge = 'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
}

Write-Host "Edge: $edge"
Write-Host "HTML: $html"
Write-Host "PDF: $pdf"

if (Test-Path $pdf) {
    Remove-Item $pdf -Force -ErrorAction SilentlyContinue
}

$argList = @(
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    '--print-to-pdf-no-header',
    '--run-all-compositor-stages-before-draw',
    '--virtual-time-budget=10000',
    "--print-to-pdf=$pdf",
    "file:///$html"
)

Write-Host "Iniciando renderizacao do poster..."
$proc = Start-Process -FilePath $edge -ArgumentList $argList -PassThru -Wait
Write-Host "Processo concluido com codigo: $($proc.ExitCode)"

if (Test-Path $pdf) {
    $len = (Get-Item $pdf).Length / 1MB
    Write-Host ("PDF gerado com sucesso! Tamanho: {0:N2} MB" -f $len)
} else {
    Write-Error "Falha ao gerar o PDF!"
}

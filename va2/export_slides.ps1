$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open('C:\Users\ccunh\Documents\workspace\va2\GrafoParada_Seminario2_CauaLira.pptx', [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
$exportDir = 'C:\Users\ccunh\Documents\workspace\va2\slides_preview'
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir | Out-Null
}
$pres.SaveAs($exportDir, 17) # 17 = ppSaveAsPNG
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Output "Export complete"
Get-ChildItem $exportDir

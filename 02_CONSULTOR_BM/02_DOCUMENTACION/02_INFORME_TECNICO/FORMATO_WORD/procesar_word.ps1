param([ValidateSet('preparar','finalizar')][string]$Etapa)
$ErrorActionPreference = 'Stop'
$taskPython = $env:MSP_PYTHON
if (!$taskPython) { $taskPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' }
if (!(Test-Path -LiteralPath $taskPython)) { throw 'Defina MSP_PYTHON con la ruta de Python que tenga lxml instalado.' }
if ($Etapa -eq 'preparar') {
    & $taskPython (Join-Path $PSScriptRoot 'preparar_referencia.py')
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar la referencia.' }
    exit 0
}
& $taskPython (Join-Path $PSScriptRoot 'finalizar_docx.py')
if ($LASTEXITCODE -ne 0) { throw 'No se pudo completar el formato de Word.' }
$taskPath = Join-Path $PSScriptRoot 'Informe_Tecnico_SIGEM.docx'
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
$taskDoc = $null
try {
    $taskDoc = $taskWord.Documents.Open($taskPath, $false, $false)
    # Word pagina el documento y calcula ambos índices, sin intervención manual.
    $taskDoc.Fields.Update() | Out-Null
    foreach ($taskIndex in $taskDoc.TablesOfContents) { $taskIndex.Update() }
    foreach ($taskIndex in $taskDoc.TablesOfFigures) { $taskIndex.Update() }
    $taskDoc.Repaginate()
    $taskDoc.Fields.Update() | Out-Null
    foreach ($taskStory in $taskDoc.StoryRanges) {
        $taskStory.Fields.Update() | Out-Null
        $taskNext = $taskStory.NextStoryRange
        while ($null -ne $taskNext) { $taskNext.Fields.Update() | Out-Null; $taskNext=$taskNext.NextStoryRange }
    }
    $taskDoc.Save()
    Write-Output "Word final generado con índices y paginación actualizados: $($taskDoc.ComputeStatistics(2)) páginas."
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close(0); [Runtime.InteropServices.Marshal]::ReleaseComObject($taskDoc) | Out-Null }
    $taskWord.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord) | Out-Null
}

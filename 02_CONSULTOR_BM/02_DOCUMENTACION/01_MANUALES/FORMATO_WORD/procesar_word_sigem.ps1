param([ValidateSet('preparar','finalizar')][string]$Etapa)
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = 'C:\Users\MARCELO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$output = if ($env:MSP_WORD_OUTPUT_NAME) { $env:MSP_WORD_OUTPUT_NAME } else { 'Manual_SIGEM.docx' }
if ($Etapa -eq 'preparar') {
  & $python (Join-Path $root 'preparar_referencia.py')
  $env:MSP_WORD_OUTPUT_NAME = $output
  exit $LASTEXITCODE
}
$env:MSP_WORD_OUTPUT_NAME = $output
& $python (Join-Path $root 'finalizar_docx.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open((Join-Path $root $output))
foreach ($field in $doc.Fields) { $field.Update() }
$doc.Save(); $doc.Close(); $word.Quit()

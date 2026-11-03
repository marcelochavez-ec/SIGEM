param([ValidateSet('preparar','finalizar')][string]$Etapa)
$env:MSP_WORD_OUTPUT_NAME = 'Manual_SIGEM.docx'
& (Join-Path $PSScriptRoot 'procesar_word_sigem.ps1') -Etapa $Etapa
exit $LASTEXITCODE

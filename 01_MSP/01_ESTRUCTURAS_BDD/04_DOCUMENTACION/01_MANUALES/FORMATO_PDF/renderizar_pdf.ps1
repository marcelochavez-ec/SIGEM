# Elaborado por Marcelo Chávez, consultor especialista en protección social.
# marcelo_chavez_s@outlook.com | 098 333 26 87
# https://www.linkedin.com/in/marcelochavezec
$ErrorActionPreference = 'Stop'
$quarto = Get-Command quarto -ErrorAction SilentlyContinue
$ejecutable = if ($quarto) { $quarto.Source } else { 'C:/Program Files/Quarto/bin/quarto.exe' }
if (-not (Test-Path -LiteralPath $ejecutable)) { throw 'Instale Quarto o agréguelo al PATH.' }
Push-Location -LiteralPath $PSScriptRoot
try {
    & $ejecutable render Manual_integral_API_Presidencia.qmd --to pdf
    if ($LASTEXITCODE -ne 0) { throw 'Falló el renderizado PDF; revise el diagnóstico de Quarto.' }
} finally { Pop-Location }

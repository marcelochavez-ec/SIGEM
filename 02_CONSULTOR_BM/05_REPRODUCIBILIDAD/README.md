# Reproducibilidad

El entorno autorizado es `msp_01`. `environment.yml` es una especificación declarativa y no demuestra por sí sola una recreación exitosa.

## Validación controlada

1. Activar el entorno existente: `conda activate msp_01`.
2. Verificar `python --version`, `quarto --version` y `pip check`.
3. Ejecutar las pruebas Django desde `02_SOFT`.
4. Renderizar los manuales con Quarto.
5. Registrar cualquier dependencia faltante.

No se crea ni modifica automáticamente ningún entorno.

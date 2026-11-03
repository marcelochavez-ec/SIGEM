# Documentación y manuales

Los manuales fuente se mantienen en formato Quarto dentro de `01_MANUALES`. Las salidas PDF y DOCX se generan en el mismo subdirectorio cuando Quarto y Pandoc están disponibles en `msp_01`. No se afirma una salida validada hasta ejecutar el render.

## Entregables vigentes

1. Manual de usuario: `01_MANUALES/FORMATO_WORD/Manual_SIGEM.docx` y `01_MANUALES/FORMATO_PDF/Manual_SIGEM.pdf`.
2. Informe técnico: `02_INFORME_TECNICO/FORMATO_WORD/Informe_Tecnico_SIGEM.docx` y `02_INFORME_TECNICO/FORMATO_PDF/Informe_Tecnico_SIGEM.pdf`.
3. Las fuentes editables son `Manual_SIGEM.qmd` e `Informe_Tecnico_SIGEM.qmd` en sus respectivos directorios Word y PDF.
4. Los archivos anteriores se retiraron de las carpetas de entrega y se conservaron fuera de ellas en `99_ARCHIVO_OBSOLETO_API_PRESIDENCIA` para recuperación histórica.

## Verificación realizada el 3 de noviembre de 2026

1. Se renderizaron los cuatro archivos con Quarto desde el ambiente Conda `msp_01`; no se usó un Python del `PATH`.
2. El texto extraído de ambos DOCX no contiene el título anterior ni referencias a Presidencia; cada documento tiene contenido distinto y acorde con su propósito.
3. El manual PDF tiene 7 páginas y el informe técnico PDF tiene 9 páginas; ambos son A4.
4. Se revisaron visualmente portada y última página de cada PDF mediante rasterización Poppler; no se observaron recortes ni solapamientos.
5. El manual documenta navegación, datos generales, validaciones y el bloqueo de niveles II/III. El informe documenta capas, dependencias, flujo, pruebas y limitaciones actuales.
6. Las pruebas funcionales del módulo registradas en el informe permanecen: 2 pruebas Django aprobadas, sintaxis JavaScript aprobada y `manage.py check` aprobado.
7. Se actualizó exclusivamente el footer de los PDF del manual y del informe con nombre, cargo, correo, teléfono e indicador de LinkedIn; los DOCX no fueron modificados.

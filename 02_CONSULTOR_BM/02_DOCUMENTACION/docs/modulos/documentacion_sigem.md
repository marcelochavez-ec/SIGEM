# Módulo de documentación SIGEM

## 1. Objetivo funcional

Entregar un manual de usuario y un informe técnico que describan la versión realmente implementada de SIGEM, en formatos Word y PDF.

## 2. Ubicación de archivos

1. Fuentes y salidas del manual: `01_MANUALES/FORMATO_WORD` y `01_MANUALES/FORMATO_PDF`.
2. Fuentes y salidas del informe: `02_INFORME_TECNICO/FORMATO_WORD` y `02_INFORME_TECNICO/FORMATO_PDF`.
3. Procesos Word: scripts `procesar_word_*`, `preparar_referencia.py` y `finalizar_docx.py`.
4. Estilos PDF: `latex/estilo_manual_sigem.tex` y `latex/estilo_informe_sigem.tex`.

## 3. Flujo de generación

1. Quarto lee el QMD correspondiente.
2. Para Word, el pre-render prepara la referencia institucional y el post-render ajusta campos del DOCX.
3. Para PDF, Quarto ejecuta XeLaTeX con papel A4, créditos y estilo institucional.
4. Las salidas se verifican por texto, metadatos PDF y rasterización de páginas.
5. Los estilos PDF incorporan en el footer los datos de contacto institucionales solicitados; el procesamiento Word conserva su footer propio.

## 4. Entradas y salidas

Las entradas son los QMD, la referencia DOCX, logos, créditos y estilos. Las salidas vigentes son `Manual_SIGEM.docx`, `Manual_SIGEM.pdf`, `Informe_Tecnico_SIGEM.docx` e `Informe_Tecnico_SIGEM.pdf`.

## 5. Contenido documentado

El manual cubre acceso, navegación, datos generales, validaciones y el mensaje de construcción para niveles II y III. El informe cubre presentación, JavaScript, Django, persistencia, recursos estáticos, dependencias, pruebas y limitaciones.

## 6. Dependencias y pruebas

La generación se ejecuta con Conda `msp_01`, Quarto, Pandoc, XeLaTeX y el runtime documental para ajustes DOCX. Se verificaron los cuatro renders, tamaños A4 de los PDF, ausencia del título anterior en Word y revisión visual de páginas representativas.

## 7. Riesgos y pendientes

Los niveles II y III continúan en construcción. La habilitación futura de esos niveles debe conservar la validación del servidor y actualizar ambos documentos.

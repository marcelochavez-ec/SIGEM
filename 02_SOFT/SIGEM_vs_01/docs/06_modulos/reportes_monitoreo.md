# Módulo Reporte de Monitoreo

## 1. Nombre del módulo

Reporte de monitoreo SIGEM.

## 2. Objetivo funcional

1. Presentar un dashboard ejecutivo del avance de registros SIGEM.
2. Resumir matrices registradas, Direcciones Provinciales cargadas, archivos finales y modificaciones.
3. Mostrar lectura territorial por Direcciones Provinciales.
4. Visualizar estado de carga y carga por fecha.

## 3. Ubicación de archivos modificados o creados

1. `sigem/views.py`
2. `sigem/urls.py`
3. `templates/base.html`
4. `templates/sigem/reportes_monitoreo.html`
5. `static/sigem/css/01_componentes.css`
6. `static/sigem/css/03_responsive.css`
7. `static/sigem/js/reportes_monitoreo.js`
8. `static/sigem/vendor/echarts/echarts.min.js`
9. `docs/06_modulos/reportes_monitoreo.md`

## 4. Flujo general paso a paso

1. El usuario selecciona `Reporte de monitoreo` en el menu lateral.
2. Django resuelve la ruta `/reportes-monitoreo/`.
3. La vista `reportes_monitoreo` ejecuta `obtener_series_reportes_monitoreo`.
4. La vista consulta registros de `SigemFormulario` y `RespuestaS01`.
5. El template muestra tarjetas KPI y graficos principales sin un contenedor visual general que sature la interfaz.
6. El JavaScript lee el JSON generado por Django y dibuja graficos interactivos con Apache ECharts.
7. El usuario puede pasar el mouse sobre barras, puntos o sectores para ver tooltip.
8. El usuario puede hacer clic en KPIs o graficos para abrir un popup explicativo.

## 5. Entradas del módulo

1. Peticion HTTP GET a `/reportes-monitoreo/`.
2. Tabla `sigem.sigem_formulario`.
3. Tabla `sigem.respuesta_s01`.
4. Campo territorial `s01_dg05` para Dirección Provincial.
5. Campo `version` de la cabecera para identificar formularios versionados.
6. Campos `fecha_registro` y `fecha_actualizacion` de la cabecera.

## 6. Salidas del módulo

1. Tarjeta de matrices registradas.
2. Tarjeta de Direcciones Provinciales cargadas.
3. Tarjeta de archivos finales cargados.
4. Tarjeta de modificaciones registradas.
5. Gráfico de barras por Direcciones Provinciales.
6. Gráfico dona por estado de carga: almacenados, modificados y versionados.
7. Gráfico de línea por fecha de carga.
8. Popups y tooltips de lectura interactiva.

## 7. Fuentes de datos utilizadas

1. `sigem.sigem_formulario`
2. `sigem.respuesta_s01`

## 8. Reglas de negocio aplicadas

1. El total de matrices se calcula desde `SigemFormulario.objects.count()`.
2. El total de Direcciones Provinciales cargadas se calcula con conteo distinto de `s01_dg05`.
3. Los archivos finales cargados corresponden a estados `ENVIADO` y `VALIDADO`.
4. Las modificaciones registradas se identifican comparando `fecha_actualizacion` contra `fecha_registro`.
5. Los formularios versionados se identifican cuando `version` es mayor que 1.
6. Las series territoriales excluyen valores nulos o vacios.
7. El dashboard no muestra cantones, parroquias ni estado del predio porque no son indicadores prioritarios del panel ejecutivo.

## 9. Lógica UI

1. El menu lateral incorpora la opción `Reporte de monitoreo`.
2. El panel principal evita un contenedor global; cada KPI y cada gráfico conserva su propia tarjeta visual.
3. Las métricas principales se muestran como tarjetas KPI.
4. El gráfico territorial se titula `Por Direcciones Provinciales`.
5. El gráfico territorial alinea las etiquetas a la izquierda y permite saltos de línea para Direcciones Provinciales largas.
6. El gráfico temporal se titula `Carga por fecha`.
7. Los graficos se dibujan con Apache ECharts usando una librería estática local del aplicativo.
8. Los graficos tienen tooltip nativo de ECharts al pasar el mouse y popup institucional al hacer clic.
9. El tooltip de la serie temporal se reposiciona hacia la izquierda cuando el punto consultado está cerca del borde derecho de la pantalla.
10. La capa responsive reorganiza el dashboard a una columna en pantallas pequenas.

## 10. Lógica server

1. `obtener_series_reportes_monitoreo` concentra las consultas ORM.
2. `serie_respuesta` agrupa dinamicamente un campo de `RespuestaS01`.
3. La serie `estado_carga` resume matrices almacenadas, modificadas y versionadas.
4. `reportes_monitoreo` renderiza el template y entrega los datos en formato Python/JSON.
5. La vista no modifica base de datos.

## 11. Consultas SQL o lógica ETL relevante

1. No se escribe SQL manual.
2. El ORM genera agregaciones `COUNT`, `COUNT DISTINCT` y agrupaciones por campo.
3. La evolucion de carga usa `TruncDate` sobre `fecha_registro`.

## 12. Dependencias

1. Django ORM.
2. Templates Django.
3. CSS local del aplicativo.
4. JavaScript nativo del navegador.
5. Apache ECharts `6.1.0` como dependencia estática local.

## 13. Validaciones realizadas

1. `python manage.py check`.
2. Verificacion de sintaxis JavaScript con `node --check`.
3. Verificacion de renderizado del template con datos de prueba para confirmar la carga de `echarts.min.js`.
4. Verificacion de que el template usa contenedores ECharts y ya no conserva elementos `<canvas>`.
5. `python manage.py makemigrations --check --dry-run` sin cambios pendientes de modelo.
6. Prueba real con cliente Django sobre `/reportes-monitoreo/`: HTTP 200, `echarts.min.js` cargado, `chartProvincias` presente y sin `<canvas>`.

## 14. Pruebas sugeridas o ejecutadas

1. Ejecutada: renderizar `templates/sigem/reportes_monitoreo.html` con datos simulados.
2. Ejecutada: validar `manage.py check`.
3. Ejecutada: verificar estructura de métricas, Direcciones Provinciales, estado de carga y fechas.
4. Ejecutada: validar sintaxis de `static/sigem/js/reportes_monitoreo.js`.
5. Ejecutada: solicitar `/reportes-monitoreo/` contra PostgreSQL real mediante cliente Django.
6. No ejecutada en esta validación: batería completa `python manage.py test sigem --noinput`, porque requeriría crear base de datos de prueba en PostgreSQL institucional.
7. Sugerida: confirmar que las cifras coincidan con consultas directas a PostgreSQL.
8. Sugerida: validar visualmente el dashboard en navegador con datos reales.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. Si existen registros sin S01, no apareceran en las series territoriales.
2. La métrica de modificaciones depende de qué `fecha_actualizacion` refleje cambios reales de formulario.
3. Los graficos son informativos y no reemplazan reportes estadisticos auditados.

## 16. Cambios realizados en esta tarea

1. Se creó el módulo `Reporte de monitoreo`.
2. Se agregó ruta Django dedicada.
3. Se agregó opción lateral de navegación.
4. Se implementó dashboard con KPIs ejecutivos y tres graficos principales.
5. Se agregó JavaScript propio para graficos interactivos, tooltips y popups.
6. Se agregó CSS responsive para el dashboard.
7. Se retiraron rankings de cantones, parroquias y estado del predio.
8. Se elimino el contenedor visual general del dashboard para que queden solo las tarjetas necesarias.
9. Se ajustaron las etiquetas del eje territorial para que no se corten.
10. Se cambio la dona a `Estado de Carga` con almacenados, modificados y versionados.
11. Se ajustaron los titulos visibles a `Reporte de monitoreo`, `Por Direcciones Provinciales` y `Carga por fecha`.
12. Se corrigió el posicionamiento del tooltip para evitar que salga fuera de la pantalla.
13. Se migraron los tres graficos principales a Apache ECharts.
14. Se agregó `echarts.min.js` como recurso local para evitar dependencia de internet en ejecución.

## 17. Pendientes o recomendaciones futuras

1. Agregar filtros por periodo cuando el volumen de registros lo requiera.
2. Incorporar exportacion a Excel o PDF si el dashboard se usa como reporte formal.



# Modulo Reporte de Monitoreo

## 1. Nombre del modulo

Reporte de monitoreo SIGES.

## 2. Objetivo funcional

1. Presentar un dashboard ejecutivo del avance de registros SIGES.
2. Resumir matrices registradas, Direcciones Provinciales cargadas, archivos finales y modificaciones.
3. Mostrar lectura territorial por Direcciones Provinciales.
4. Visualizar estado de carga y carga por fecha.

## 3. Ubicacion de archivos modificados o creados

1. `siges/views.py`
2. `siges/urls.py`
3. `templates/base.html`
4. `templates/siges/reportes_monitoreo.html`
5. `static/siges/css/01_componentes.css`
6. `static/siges/css/03_responsive.css`
7. `static/siges/js/reportes_monitoreo.js`
8. `docs/06_modulos/reportes_monitoreo.md`

## 4. Flujo general paso a paso

1. El usuario selecciona `Reporte de monitoreo` en el menu lateral.
2. Django resuelve la ruta `/reportes-monitoreo/`.
3. La vista `reportes_monitoreo` ejecuta `obtener_series_reportes_monitoreo`.
4. La vista consulta registros de `SigesFormulario` y `RespuestaS01`.
5. El template muestra tarjetas KPI y graficos principales sin un contenedor visual general que sature la interfaz.
6. El JavaScript lee el JSON generado por Django y dibuja graficos interactivos en canvas.
7. El usuario puede pasar el mouse sobre barras, puntos o sectores para ver tooltip.
8. El usuario puede hacer clic en KPIs o graficos para abrir un popup explicativo.

## 5. Entradas del modulo

1. Peticion HTTP GET a `/reportes-monitoreo/`.
2. Tabla `siges.siges_formulario`.
3. Tabla `siges.respuesta_s01`.
4. Campo territorial `s01_dg05` para Dirección Provincial.
5. Campo `version` de la cabecera para identificar formularios versionados.
6. Campos `fecha_registro` y `fecha_actualizacion` de la cabecera.

## 6. Salidas del modulo

1. Tarjeta de matrices registradas.
2. Tarjeta de Direcciones Provinciales cargadas.
3. Tarjeta de archivos finales cargados.
4. Tarjeta de modificaciones registradas.
5. Grafico de barras por Direcciones Provinciales.
6. Grafico dona por estado de carga: almacenados, modificados y versionados.
7. Grafico de linea por fecha de carga.
8. Popups y tooltips de lectura interactiva.

## 7. Fuentes de datos utilizadas

1. `siges.siges_formulario`
2. `siges.respuesta_s01`

## 8. Reglas de negocio aplicadas

1. El total de matrices se calcula desde `SigesFormulario.objects.count()`.
2. El total de Direcciones Provinciales cargadas se calcula con conteo distinto de `s01_dg05`.
3. Los archivos finales cargados corresponden a estados `ENVIADO` y `VALIDADO`.
4. Las modificaciones registradas se identifican comparando `fecha_actualizacion` contra `fecha_registro`.
5. Los formularios versionados se identifican cuando `version` es mayor que 1.
6. Las series territoriales excluyen valores nulos o vacios.
7. El dashboard no muestra cantones, parroquias ni estado del predio porque no son indicadores prioritarios del panel ejecutivo.

## 9. Logica UI

1. El menu lateral incorpora la opcion `Reporte de monitoreo`.
2. El panel principal evita un contenedor global; cada KPI y cada grafico conserva su propia tarjeta visual.
3. Las metricas principales se muestran como tarjetas KPI.
4. El grafico territorial se titula `Por Direcciones Provinciales`.
5. El grafico territorial alinea las etiquetas a la izquierda y permite saltos de linea para Direcciones Provinciales largas.
6. El grafico temporal se titula `Carga por fecha`.
7. Los graficos se dibujan en canvas para evitar dependencias externas.
8. Los graficos tienen tooltip al pasar el mouse y popup al hacer clic.
9. El tooltip se reposiciona hacia la izquierda cuando el punto consultado esta cerca del borde derecho de la pantalla.
10. La capa responsive reorganiza el dashboard a una columna en pantallas pequenas.

## 10. Logica server

1. `obtener_series_reportes_monitoreo` concentra las consultas ORM.
2. `serie_respuesta` agrupa dinamicamente un campo de `RespuestaS01`.
3. La serie `estado_carga` resume matrices almacenadas, modificadas y versionadas.
4. `reportes_monitoreo` renderiza el template y entrega los datos en formato Python/JSON.
5. La vista no modifica base de datos.

## 11. Consultas SQL o logica ETL relevante

1. No se escribe SQL manual.
2. El ORM genera agregaciones `COUNT`, `COUNT DISTINCT` y agrupaciones por campo.
3. La evolucion de carga usa `TruncDate` sobre `fecha_registro`.

## 12. Dependencias

1. Django ORM.
2. Templates Django.
3. CSS local del aplicativo.
4. JavaScript nativo del navegador.
5. Canvas HTML5.

## 13. Validaciones realizadas

1. `python manage.py check`.
2. Verificacion de sintaxis JavaScript con `node --check`.
3. Verificacion de datos generados por `obtener_series_reportes_monitoreo`.
4. Verificacion de carga del enlace lateral.

## 14. Pruebas sugeridas o ejecutadas

1. Ejecutada: validar ruta `/reportes-monitoreo/`.
2. Ejecutada: validar `manage.py check`.
3. Ejecutada: verificar estructura de metricas, Direcciones Provinciales, estado de carga y fechas.
4. Sugerida: confirmar que las cifras coincidan con consultas directas a PostgreSQL.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. Si existen registros sin S01, no apareceran en las series territoriales.
2. La metrica de modificaciones depende de que `fecha_actualizacion` refleje cambios reales de formulario.
3. Los graficos son informativos y no reemplazan reportes estadisticos auditados.

## 16. Cambios realizados en esta tarea

1. Se creo el modulo `Reporte de monitoreo`.
2. Se agrego ruta Django dedicada.
3. Se agrego opcion lateral de navegacion.
4. Se implemento dashboard con KPIs ejecutivos y tres graficos principales.
5. Se agrego JavaScript propio para graficos interactivos, tooltips y popups.
6. Se agrego CSS responsive para el dashboard.
7. Se retiraron rankings de cantones, parroquias y estado del predio.
8. Se elimino el contenedor visual general del dashboard para que queden solo las tarjetas necesarias.
9. Se ajustaron las etiquetas del eje territorial para que no se corten.
10. Se cambio la dona a `Estado de Carga` con almacenados, modificados y versionados.
11. Se ajustaron los titulos visibles a `Reporte de monitoreo`, `Por Direcciones Provinciales` y `Carga por fecha`.
12. Se corrigio el posicionamiento del tooltip para evitar que salga fuera de la pantalla.

## 17. Pendientes o recomendaciones futuras

1. Agregar filtros por periodo cuando el volumen de registros lo requiera.
2. Incorporar exportacion a Excel o PDF si el dashboard se usa como reporte formal.



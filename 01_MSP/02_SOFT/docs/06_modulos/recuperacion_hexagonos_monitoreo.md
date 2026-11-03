# Recuperación de hexágonos y Reporte de monitoreo

## 1. Respaldo local y alcance

1. El repositorio Git raíz es `SIGEM`; el aplicativo se encuentra en `02_SOFT/SIGEM_vs_01`.
2. Antes de retirar componentes se guardaron los ocho archivos de interfaz que tenían cambios locales en el commit `0a1d6f1`.
3. La etiqueta anotada `respaldo/hexagonos-monitoreo-20261102` identifica el estado completo anterior al retiro: HTML, estilos, adaptación móvil, enlaces, vista, helper ORM, template, JavaScript y ECharts.
4. El retiro se identifica mediante la etiqueta `cambio/retiro-hexagonos-monitoreo-20261102`. Ambas etiquetas son locales; esta tarea no ejecuta `git push` ni publica en GitHub.
5. No se copiaron datos, credenciales ni configuraciones de producción. El respaldo conserva código y documentación versionados, no una copia de PostgreSQL.

## 2. Estado implementado tras el retiro

1. Se retiró `hero-hex-group` y sus tres enlaces del template de inicio.
2. Se eliminaron los selectores `.hero-hex*`, `.hex-main`, `.hex-blue`, `.hex-green` y sus ajustes responsive.
3. El banner conserva texto e imagen, ajustando la columna visual; las tres tarjetas inferiores permanecen disponibles.
4. Se retiró el enlace `Reporte de monitoreo` de `templates/base.html`.
5. Se desregistró la ruta de reporte en `sigem/urls.py`: `/reportes-monitoreo/` devuelve 404 y el nombre de ruta no se puede resolver.
6. Se conservan `reportes_monitoreo`, `obtener_series_reportes_monitoreo`, el template, JavaScript, estilos de reporte y ECharts, sin acceso público. No se modificaron modelos, SQL ni registros.

## 3. Consultar el respaldo sin sobrescribir la versión vigente

1. Comprobar que existen ambas etiquetas y consultar el historial desde la raíz del repositorio:

```powershell
git show --no-patch respaldo/hexagonos-monitoreo-20261102
git show --stat cambio/retiro-hexagonos-monitoreo-20261102
```

2. Consultar el template original sin reemplazar archivos:

```powershell
git show respaldo/hexagonos-monitoreo-20261102:02_SOFT/SIGEM_vs_01/templates/sigem/inicio.html
```

3. Comparar únicamente un componente para ver exactamente qué se retiró:

```powershell
git diff respaldo/hexagonos-monitoreo-20261102 cambio/retiro-hexagonos-monitoreo-20261102 -- 02_SOFT/SIGEM_vs_01/templates/sigem/inicio.html
```

## 4. Reincorporar hexágonos en una versión futura

1. Guardar primero los cambios vigentes y trabajar en una rama de recuperación.
2. Recuperar del respaldo solo el bloque `hero-hex-group` del template de inicio.
3. Integrar sus selectores en `01_componentes.css` y las reglas correspondientes en `03_responsive.css`.
4. Revisar el ancho del banner y el contenedor de imagen: fueron adaptados para la versión sin hexágonos.
5. Validar los nombres de las rutas y el destino externo del tercer hexágono; el respaldo preserva los enlaces originales, que deben revisarse antes de reincorporarse.
6. Actualizar la versión del CSS y las pruebas que actualmente exigen ausencia de hexágonos.
7. Revisar escritorio y móvil y actualizar `inicio.md` e `interfaz.md` según el resultado final.

## 5. Reincorporar Reporte de monitoreo

1. Revisar el código conservado en `sigem/views.py`: `reportes_monitoreo(request)` recibe la petición y devuelve HTML; `obtener_series_reportes_monitoreo()` no recibe argumentos y devuelve métricas y series calculadas por ORM.
2. Validar sus campos y fuentes `sigem.sigem_formulario` y `sigem.respuesta_s01` contra los modelos vigentes. No restaurar modelos ni migraciones antiguos.
3. Verificar `templates/sigem/reportes_monitoreo.html`, `static/sigem/js/reportes_monitoreo.js`, los selectores de reporte y `static/sigem/vendor/echarts/echarts.min.js`; si fueron retirados en cambios posteriores, obtener únicamente estos componentes del respaldo.
4. Registrar nuevamente la ruta `reportes-monitoreo/` con vista `views.reportes_monitoreo` y nombre `reportes_monitoreo`.
5. Incorporar el enlace al menú lateral con su estado activo `reportes` y el icono `monitoring`.
6. Actualizar las pruebas que actualmente esperan 404 y `NoReverseMatch`; agregar validaciones del dashboard con datos simulados antes de consultar registros reales.
7. Ejecutar `manage.py check`, validar gráficos, métricas, permisos vigentes y rendimiento de agregaciones, y actualizar la documentación del módulo.

## 6. Validaciones realizadas y límites

1. `manage.py check`: sin incidencias.
2. `manage.py test sigem.tests.InicioSinComponentesRetiradosTest --noinput --verbosity 2`: tres pruebas correctas, sin base de datos de pruebas.
3. `git diff --check`: sin errores de espacios.
4. No se ejecutaron migraciones ni escrituras en PostgreSQL; no se cambió la configuración productiva.
5. No se realizó comprobación visual automatizada: falta `npx`, requisito de Playwright CLI en esta sesión.
6. Un historial Git permite recuperar código, pero cambios futuros en rutas, estilos o datos pueden requerir adaptación y resolución de conflictos. No restaurar archivos completos antiguos ni toda la aplicación para recuperar un componente.

## 7. Publicación futura

1. Un respaldo local no protege ante pérdida del disco. Cuando se decida publicar en GitHub, incluir explícitamente las dos etiquetas junto con los commits del aplicativo; un envío normal de la rama no garantiza subir las etiquetas locales.
2. Antes de publicar, revisar el repositorio completo según sus reglas de datos y credenciales. Esta tarea solo registró los cambios de interfaz, navegación, pruebas y documentación indicados.

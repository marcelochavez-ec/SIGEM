# Módulo Inicio

## 1. Nombre del módulo

Inicio SIGEM.

## 2. Objetivo funcional

Presentar el inicio institucional y orientar hacia establecimientos, roles y usuarios, y manual de usuario.

## 3. Ubicación de archivos

1. `templates/sigem/inicio.html`: contenido del inicio.
2. `templates/base.html`: navegación compartida y versión de CSS.
3. `static/sigem/css/01_componentes.css`: componentes y banner.
4. `static/sigem/css/03_responsive.css`: adaptación por ancho.
5. `static/sigem/css/app.css`: importaciones con versión para evitar caché anterior.
6. `sigem/views.py`: vista `inicio`, sin cambios en esta tarea.
7. `sigem/tests.py`: clase `InicioSinComponentesRetiradosTest`.

## 4. Flujo general paso a paso

1. El usuario ingresa a `/`.
2. Django ejecuta `inicio` y entrega `active_page='inicio'`.
3. El template muestra texto institucional, imagen y tres tarjetas de navegación.
4. El usuario abre establecimientos, roles y usuarios, o manual.
5. El menú ofrece Inicio, Establecimientos, Roles y usuarios y Manual de usuario; no ofrece Reporte de monitoreo.

## 5. Entradas

1. Petición HTTP GET a `/` y contexto `active_page`.
2. Imagen `establecimiento_salud.jpg`, estilos y fuentes locales existentes.

## 6. Salidas

1. HTML del inicio sin hexágonos.
2. Tres tarjetas de acceso, franja informativa y layout institucional compartido.

## 7. Fuentes de datos

1. El inicio no consulta tablas ni necesita credenciales propias.
2. Utiliza templates y archivos estáticos locales.

## 8. Reglas de negocio

1. El inicio no captura datos ni ejecuta agregaciones.
2. Las tres tarjetas inferiores permanecen disponibles.
3. Los hexágonos se retiraron del HTML y del CSS, no se ocultan mediante una regla visual.
4. Su recuperación debe integrar selectivamente los componentes respaldados en Git.

## 9. Lógica UI

1. El banner muestra `Plataforma tecnológica para registro de información desarrollada por:` y la unidad responsable.
2. En escritorio, el texto ocupa el espacio disponible y la imagen tiene una columna de hasta 286 px, eliminando la reserva de espacio de los hexágonos.
3. Hasta 1180 px, la imagen se centra debajo del texto y conserva su ancho limitado.
4. Hasta 575 px, se omiten imagen y contenedor visual para evitar una franja vacía.
5. Se conservan iconos circulares, bordes, sombras y navegación de las tarjetas.
6. La versión CSS `20261102a` solicita las hojas modificadas al refrescar. Se mantiene la separación entre HTML y estilos.

## 10. Lógica server

1. `inicio(request)` recibe la petición, prepara el estado activo del menú y devuelve el render del template.
2. No se modificó la función ni se añadieron consultas.

## 11. SQL o ETL relevante

1. No aplica: este módulo no ejecuta SQL ni procesos ETL.

## 12. Dependencias

1. Django: rutas, vistas y templates.
2. CSS Grid y media queries existentes.
3. Estilos y fuentes locales de Unfold y Material Symbols.
4. No se añadieron paquetes ni JavaScript.

## 13. Validaciones realizadas el 2 de noviembre de 2026

1. `python manage.py check`: sin incidencias.
2. Render del inicio: HTTP 200, tres tarjetas e imagen presentes, sin hexágonos ni enlace al reporte.
3. Resolución de las rutas de Inicio, Establecimientos, Roles y usuarios y Manual.
4. `git diff --check`: sin errores.

## 14. Pruebas ejecutadas y alcance

1. `python manage.py test sigem.tests.InicioSinComponentesRetiradosTest --noinput --verbosity 2`: tres pruebas correctas.
2. Se usaron `SimpleTestCase` y `RequestFactory`; Django omitió la preparación de base de datos.
3. No se ejecutaron pruebas que crean registros ni se modificó PostgreSQL.
4. No se ejecutó revisión visual en navegador: falta `npx`, requisito de Playwright CLI en esta sesión.

## 15. Riesgos y rendimiento

1. Comprobar el aspecto responsive al refrescar el navegador; la validación automática cubre render y rutas.
2. No se añaden consultas ni dependencias y se reduce el HTML y CSS del inicio.
3. Restaurar archivos enteros antiguos puede sobrescribir avances; utilizar la guía de recuperación selectiva.

## 16. Cambios de esta tarea

1. Se guardaron los ocho archivos de interfaz previamente modificados en el commit `0a1d6f1`.
2. Se creó la etiqueta anotada `respaldo/hexagonos-monitoreo-20261102`, con diseño y módulo de reporte completos.
3. Se retiraron los tres hexágonos, sus enlaces y reglas CSS, incluidas las de móvil.
4. Se redistribuyó el banner conservando texto e imagen y los ajustes previos de tarjetas, encabezado y footer.
5. Se retiró el acceso lateral al reporte y se actualizó la versión de estilos.
6. Se añadieron pruebas y la guía `recuperacion_hexagonos_monitoreo.md`.

## 17. Seguimiento

1. Para reincorporar componentes en una versión futura, seguir `docs/06_modulos/recuperacion_hexagonos_monitoreo.md`.
2. El respaldo es local en Git; esta tarea no publica en GitHub.

# Modulo SIGES 01

## 1. Nombre del modulo

SIGES 01 - Aplicativo web Django para matriz SIGES.

## 2. Objetivo funcional

1. Registrar matrices SIGES en PostgreSQL `productos_bm`, schema `SIGES`.
2. Implementar las secciones iniciales `s01` y `s02`.
3. Mostrar una seccion por pagina para facilitar la captura.
4. Impedir avanzar a S02 si S01 no esta completa y validada.
5. Mostrar el logo MSP en la esquina superior izquierda.

## 3. Ubicacion de archivos modificados o creados

1. `config_siges/settings.py`
2. `config_siges/asgi.py`
3. `config_siges/wsgi.py`
4. `manage.py`
5. `deploy_siges.py`
6. `siges/forms.py`
7. `siges/views.py`
8. `siges/services.py`
9. `siges/migrations/0001_initial.py`
10. `templates/base.html`
11. `templates/siges/inicio.html`
12. `templates/siges/establecimientos.html`
13. `templates/siges/roles_usuarios.html`
14. `templates/siges/manual_usuario.html`
15. `templates/siges/matriz_form.html`
16. `templates/siges/matriz_detalle.html`
17. `static/siges/css/app.css`
18. `static/siges/css/00_base.css`
19. `static/siges/css/01_componentes.css`
20. `static/siges/css/02_footer.css`
21. `static/siges/css/03_responsive.css`
22. `static/siges/js/reportes_monitoreo.js`
23. `templates/siges/reportes_monitoreo.html`
24. `README.md`
25. `docs/06_modulos/siges_01.md`
26. `docs/06_modulos/reportes_monitoreo.md`
27. `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`
28. `docs/03_interfaz/interfaz.md`
29. `docs/08_codigo/lectura_codigo.md`
30. `docs/08_codigo/python.md`
31. `docs/08_codigo/frontend.md`

## 4. Flujo general paso a paso

1. El usuario ingresa al sistema.
2. Para iniciar localmente, el usuario ejecuta `python deploy_siges.py`.
3. El script se relanza con `C:\ProgramData\anaconda3\envs\msp_01\python.exe` si la terminal usa otro Python.
4. El script lee las variables guardadas en `msp_01` y valida que `SIGES_DB_PASSWORD` exista.
5. El script ejecuta `check`, `migrate`, `cargar_catalogos_siges` y `runserver`.
6. La vista de inicio muestra el home SIGES con accesos a establecimientos, roles y usuarios, y manual de usuario.
7. La pantalla `Establecimientos` muestra acciones principales, resumen S01/S02 y registros SIGES.
8. La pantalla `Reportes de monitoreo` resume avance de registros por territorio, estado y mes.
9. El usuario crea una matriz desde `Nuevo Registro`.
10. La pagina S01 muestra Datos Generales y buscador real de establecimientos.
11. Si S01 tiene campos incompletos, Django muestra errores y no avanza.
12. Si S01 valida correctamente, sus datos quedan en sesion y se habilita S02.
13. La pagina S02 muestra Acceso y Movilizacion.
14. Al guardar S02, el servicio guarda cabecera, `respuesta_s01` y `respuesta_s02`.
15. El usuario llega al detalle del registro guardado.

## 5. Entradas del modulo

1. Usuario autenticado.
2. Campos `s01_dg01` a `s01_dg13`.
3. Campos `s02_am01` a `s02_am06`.
4. Catalogos de `s02_am02`, `s02_am03` y `s02_am06`.
5. Variables de entorno:
   1. `DJANGO_SECRET_KEY`
   2. `DJANGO_DEBUG`
   3. `DJANGO_ALLOWED_HOSTS`
   4. `SIGES_DB_NAME`
   5. `SIGES_DB_USER`
   6. `SIGES_DB_PASSWORD`
   7. `SIGES_DB_HOST`
   8. `SIGES_DB_PORT`
   9. `SIGES_DB_SCHEMA`
   10. `DJANGO_FORCE_SCRIPT_NAME`, opcional, define una ruta base de publicacion como `/siges` cuando el aplicativo se sirve detras de Nginx.
6. Ambiente Conda activo: `msp_01`.

## 6. Salidas del modulo

1. Registro cabecera en `siges_formulario`.
2. Registro de S01 en `respuesta_s01`.
3. Registro de S02 en `respuesta_s02`.
4. Pantallas de home, establecimientos, roles y usuarios, manual en construccion, captura paginada y detalle.
5. Administracion de catalogos, roles y usuarios con Django Unfold.
6. Dashboard de reportes de monitoreo con KPIs, graficos y rankings territoriales.

## 7. Fuentes de datos utilizadas

1. PostgreSQL `productos_bm`.
2. Schema PostgreSQL `SIGES`.
3. Catalogos cargados por `cargar_catalogos_siges`.

## 8. Reglas de negocio aplicadas

1. S01 debe estar completa antes de pasar a S02.
2. `s01_dg01` se usa como `unicodigo` de cabecera.
3. `s02_am04` debe ser decimal mayor o igual a cero.
4. Las opciones de `s02_am02`, `s02_am03` y `s02_am06` deben pertenecer a su variable.
5. No se usa SQLite.
6. No se versionan credenciales reales.
7. La clave PostgreSQL debe estar configurada en el ambiente Conda `msp_01`, no en archivos del proyecto.
8. La migracion inicial no debe borrar tablas existentes; debe crear solo lo faltante cuando la base ya tiene estructura previa.

## 9. Logica UI

1. `templates/base.html` define encabezado SIGES, menu lateral, footer institucional y carga local de estilos Unfold.
2. `templates/siges/inicio.html` muestra el home con banner institucional y tres modulos principales.
3. `templates/siges/establecimientos.html` muestra gestion de establecimientos, acciones y resumen S01/S02.
4. `templates/siges/roles_usuarios.html` enlaza acciones de administracion hacia Django Admin con Unfold.
5. `templates/siges/manual_usuario.html` muestra el estado `En construccion`.
6. `templates/siges/matriz_form.html` muestra un paginador S01/S02.
7. S02 aparece bloqueada hasta completar S01.
8. `static/siges/css/app.css` funciona como indice de CSS y carga archivos especializados.
9. El footer institucional se organiza en cuatro bloques: ministerio, tecnologia, recursos y contacto; usa separadores verticales, tipografia compacta, textura punteada e iconografia Material Symbols.
10. `templates/siges/reportes_monitoreo.html` muestra KPIs, graficos canvas y rankings para lectura ejecutiva.

## 10. Logica server

1. `S01DatosGeneralesForm` valida los campos de S01.
2. `S02AccesoMovilizacionForm` valida los campos de S02.
3. `matriz_wizard` controla el paso actual y el bloqueo entre secciones.
4. La sesion conserva temporalmente S01 hasta guardar S02.
5. `guardar_matriz_SIGES` persiste cabecera, S01 y S02 en una transaccion.
6. `deploy_siges.py` valida Django y levanta el servidor local en `0.0.0.0:8036`.
7. `deploy_siges.py` configura Waitress con hilos y limite de conexiones para reducir avisos de cola en desarrollo local.
8. `settings.py` permite publicar el aplicativo bajo una ruta base institucional mediante `DJANGO_FORCE_SCRIPT_NAME`, conservando enlaces, favicon y archivos estaticos cuando Nginx expone SIGES como subruta.
9. `reportes_monitoreo` consulta agregaciones ORM para alimentar el dashboard sin modificar datos.

## 11. Consultas SQL o logica ETL relevante

1. No se ejecuta SQL manual desde la vista.
2. Django ORM consulta catalogos y registros.
3. PostgreSQL se configura con `search_path=SIGES,public`.
4. `0001_initial.py` usa SQL idempotente para crear tablas faltantes cuando algunas relaciones ya existen.

## 12. Dependencias

1. Python desde Conda `msp_01`.
2. Django 6.1.1.
3. Django Unfold 0.108.0.
4. Psycopg.
5. Whitenoise.
6. Script local `deploy_siges.py` basado en libreria estandar de Python.

## 13. Validaciones realizadas

1. Se configuro PostgreSQL obligatorio.
2. Se retiro referencia operativa a SQLite.
3. Se separo el paquete de configuracion como `config_siges`.
4. Se agrego paginacion S01/S02 con bloqueo de avance.
5. Se agrego el logo MSP al encabezado.
6. Se agrego `deploy_siges.py` para iniciar el aplicativo con un solo comando.
7. Se ajusto `settings.py` para leer variables persistidas de `msp_01`.

## 14. Pruebas sugeridas o ejecutadas

1. Sugerida desde Positron: `conda activate msp_01`.
2. Sugerida desde Positron: `pip install -r requirements.txt`.
3. Sugerida desde Positron: configurar `SIGES_DB_PASSWORD` en el ambiente Conda `msp_01`.
4. Ejecutada: `python manage.py check`.
5. Ejecutada: `python manage.py migrate`.
6. Ejecutada: `python manage.py cargar_catalogos_siges`.
7. Ejecutada: `python deploy_siges.py`.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. La aplicacion requiere conectividad a `10.64.100.191:5432`.
2. Si el schema `SIGES` tiene migraciones anteriores incompatibles, debe revisarse antes de migrar.
3. `s02_am01` y `s02_am05` siguen como texto hasta contar con catalogo formal.

## 16. Cambios realizados en esta tarea

1. Se agrego logo institucional al encabezado.
2. Se implemento formulario paginado por secciones.
3. Se bloqueo avance de S01 a S02 si S01 no valida.
4. Se configuro PostgreSQL obligatorio.
5. Se renombro el paquete interno a `config_siges`.
6. Se actualizo README y documentacion tecnica.
7. Se retiro la referencia operativa a `.env` y se dejo la conexion atada a variables del ambiente Conda `msp_01`.
8. Se agrego un script de levantamiento local con un solo comando.
9. Se retiro el lanzador anterior `levantar_SIGES.py` para mantener un unico comando oficial.
10. Se ajusto la migracion inicial para soportar tablas ya existentes en `productos_bm.SIGES`.
11. Se aplicaron migraciones y se cargaron catalogos SIGES correctamente.
12. Se integro Unfold en configuracion, admin, formularios, templates y tokens CSS del aplicativo.
13. Se reorganizo `docs` en subcarpetas numeradas y se agrego un indice general de documentacion.
14. Se agrego un diagrama Draw.io estilizado para documentar arquitectura, consulta de unicodigo, validacion por seccion y guardado transaccional.
15. Se adapto el aplicativo a cuatro interfaces institucionales: home, establecimientos, roles y usuarios, y manual de usuario en construccion.
16. Se separo la pantalla de inicio de la gestion de establecimientos para conservar un home inicial del aplicativo.
17. Se cargo CSS local de Unfold y fuentes de iconos Material Symbols provistas por Unfold.
18. Se fijo `Century Gothic` como tipografia global, se redujo la escala de texto y se incorporo `img/establecimiento_salud.jpg` al hero del home.
19. Se ajusto el footer institucional manteniendo el contenido original `Python/Django/Bootstrap`, recursos de sincronizacion, interoperabilidad e informes, y aumentando ligeramente el tamano de letra para mejorar lectura.
20. Se limpio el hero del home retirando la textura de puntos, eliminando el texto flotante sobre la imagen y separando los hexagonos para evitar superposiciones.
21. Se diferencio el bloque principal del home con fondo celeste institucional, borde cromaticamente consistente y sombra suave para mejorar contraste visual.
22. Se ajusto la posicion del hexagono `KPIs y estadisticas` frente al bloque de `Red de Establecimientos de Salud` y `Acceso controlado y auditado` para mantener una separacion minima uniforme tipo panal.
23. Se redujo el alto del bloque interno `En construccion` en la pantalla `Manual de usuario`, manteniendo el ancho y la estructura del panel principal.
24. Se igualo el alto del panel principal entre `Roles y usuarios` y `Manual de usuario` mediante `balanced-page-panel`, evitando desplazamientos del footer al cambiar de seccion.
25. Se agrego en el hero del home el texto superior `Sistema tecnologico para el registro de informacion desarrollado por:` y se ajusto el centrado vertical del bloque textual.
26. Se agrego una capa responsive integral con breakpoints equivalentes a Bootstrap para header, navegacion, home, tarjetas, formularios, filtros, tablas, detalle, manual, roles y footer.
27. Se mantuvo el estilo Unfold mediante tokens visuales compartidos y clases `unfold-*`, reforzando adaptacion para desktop, tablet, celular y pantallas angostas.
28. Se reorganizo el CSS por responsabilidad: base/layout, componentes, footer y responsive.
29. Se agrego documentacion especifica en `docs/08_codigo` para explicar separacion de capas, codigo Python, templates, CSS y JavaScript.
30. Se agregaron documentos individuales de modulos: inicio, establecimientos, roles y usuarios, y manual de usuario.
31. Se documento internamente el codigo Python principal mediante docstrings y comentarios explicativos en `models.py`, `forms.py`, `views.py`, `services.py`, `admin.py`, `urls.py`, `settings.py`, `deploy_siges.py` y `cargar_catalogos_siges.py`.
32. Se actualizo `docs/08_codigo/python.md` para reflejar el criterio de documentacion dentro del codigo fuente y la documentacion narrativa complementaria.
33. Se reemplazaron los diagramas anteriores por un unico archivo Draw.io editable del primer modelo logico S01/S02 en `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`.
34. Se reestructuro el diagrama como modelo logico de negocio, separando fuente institucional, parametrizacion, cabecera, respuestas por seccion y administracion/trazabilidad.
35. Se retiro la referencia al modelo fisico y se dejo el Draw.io como propuesta de modelo logico de tablas relacionadas previa al modelo entidad relacion detallado.
36. Se retiraron las lineas de relacion detalladas del Draw.io y se reemplazo por lineas funcionales solo entre contenedores grandes.
37. Se agrego membrete institucional con proyecto, instituciones, version, fecha, consultor, rol, correo y movil pendiente de completar.
38. Se ajusto el membrete del Draw.io a formato cuadriculado compacto, con logos institucionales, correo y movil definitivo del consultor.
39. Se ajusto Waitress con `threads`, `connection_limit` y `channel_timeout` parametrizables por variables de entorno.
40. Se retiro la seccion obsoleta `S03` de la parametrizacion y se eliminaron los objetos heredados `respuesta_s03` y `vw_catalogo_s03`.
41. Se retiraron codigos tecnicos `S01/S02` de las etiquetas principales visibles para usuario final.
42. Se configuraron las etiquetas principales del wizard y detalle para leer `formulario_seccion.nombre`.
43. Se agrego `img/msp_favicon.png` como favicon global del aplicativo y del admin Unfold.
44. Se fijo el titulo de la pestana del navegador como `SIGES` para todos los modulos y el admin.
45. Se agrego soporte para publicacion por proxy Nginx bajo ruta base configurable con `DJANGO_FORCE_SCRIPT_NAME`.
46. Se fijaron versiones explicitas en `requirements.txt`: `Django==6.1.1` y `django-unfold==0.108.0`.
47. Se valido que Unfold y las vistas principales rendericen correctamente con Django 6.1.1.
48. Se ajusto el hexagono principal del home para presentar `Todos los niveles`, `Establecimientos` y `de Salud` en tres filas.
49. Se configuro el hexagono de reportes del home como enlace externo al Sistema de Analitica en Salud del MSP.
50. Se ajusto el hexagono de roles del home para presentar `Administracion de roles` y `usuarios` en dos filas.
51. Se ajustaron los textos de los hexagonos del home para precisar `Establecimientos de Salud` y `MSP` en filas separadas, y dividir el enlace de reportes en cuatro filas.
52. Se renombro el hexagono de analitica del home como `KPIs e indicadores`, `Sistema`, `Analitica en` y `Salud`.
53. Se habilito navegacion directa desde los hexagonos del home: establecimientos abre el modulo de monitoreo y roles abre administracion de roles y usuarios.
54. Se creo el modulo `Reportes de monitoreo` con opcion lateral, ruta propia, dashboard, KPIs, graficos canvas y rankings territoriales.
55. Se sustituyo la identidad logica anterior por SIGES en capas Django, rutas, modelos, servicios, vistas, templates, archivos estaticos, comandos de administracion, migraciones y documentacion del proyecto.
56. Se renombro el modelo cabecera a `SigesFormulario`, manteniendo la tabla fisica `siges_formulario` para conservar la integridad de la base PostgreSQL.
57. Se renombraron las carpetas de presentacion a `templates/siges` y `static/siges`, y se actualizaron las referencias en templates, settings y documentacion.
58. Se renombro el comando de catalogos a `cargar_catalogos_siges`.
59. Se agrego la migracion `0003_establecimientoingresado.py` para registrar en el estado de Django la vista institucional `vm_establecimientos_ingresados` como modelo no administrado.
60. Se aplicaron las migraciones bajo el app label `siges` y se verifico que las rutas principales rendericen correctamente.

## 17. Pendientes o recomendaciones futuras

1. Validar conexion real desde Positron con `msp_01`.
2. Confirmar que `SIGES_DB_PASSWORD` esta configurada en `msp_01`.
3. Definir catalogos formales adicionales si S02 requiere mas listas desplegables.



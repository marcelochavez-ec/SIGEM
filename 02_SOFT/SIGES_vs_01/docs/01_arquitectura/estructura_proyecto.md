# Estructura Del Proyecto

## Archivos principales

1. `deploy_siges.py`: valida Django y levanta el servidor local en `0.0.0.0:8036`.
2. `manage.py`: ejecuta comandos Django.
3. `requirements.txt`: lista dependencias Python.
4. `README.md`: resume el contexto general de uso y mantenimiento del aplicativo.

## Configuración

1. `config_siges/settings.py`: configura Django, PostgreSQL, templates y estáticos.
2. `config_siges/urls.py`: define rutas raiz.
3. `config_siges/wsgi.py`: punto WSGI.
4. `config_siges/asgi.py`: punto ASGI.

## Aplicación `SIGES`

1. `siges/models.py`: modelos de catálogos, formulario, respuestas y vista institucional `managed=False`.
2. `siges/forms.py`: formularios y validaciones.
3. `siges/views.py`: vistas de inicio, formulario, detalle y endpoints JSON.
4. `siges/services.py`: consultas de establecimientos y persistencia de matriz.
5. `siges/urls.py`: rutas del aplicativo.
6. `siges/admin.py`: registro de modelos en Django Admin usando Unfold.

## Interfaz

1. `templates/base.html`: layout institucional.
2. `templates/siges/inicio.html`: home inicial del aplicativo.
3. `templates/siges/establecimientos.html`: pantalla de gestión de establecimientos y acceso a S01/S02.
4. `templates/siges/roles_usuarios.html`: pantalla de administración visual de roles y usuarios.
5. `templates/siges/manual_usuario.html`: pantalla de manual de usuario en construccion.
6. `templates/siges/matriz_form.html`: formulario secuencial S01/S02.
7. `templates/siges/matriz_detalle.html`: detalle de matriz guardada.
8. `static/siges/css/app.css`: índice de estilos; importa los CSS especializados.
9. `static/siges/css/00_base.css`: variables, tipografia, header, layout y navegación base.
10. `static/siges/css/01_componentes.css`: tarjetas, hero, formularios, tablas y componentes.
11. `static/siges/css/02_footer.css`: footer institucional.
12. `static/siges/css/03_responsive.css`: breakpoints responsive tipo Bootstrap.
13. `static/siges/js/establecimientos.js`: buscador y autocompletado.
14. `docs/03_interfaz/interfaz.md`: documenta identidad visual y componentes de interfaz.
15. `docs/08_codigo/`: documenta lectura técnica del código por capas.

## Arquitecturas

1. `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`: diagrama editable del primer modelo lógico del aplicativo SIGES para S01 y S02.



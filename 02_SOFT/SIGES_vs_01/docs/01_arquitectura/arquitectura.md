# Arquitectura

## Organizacion general

El proyecto usa una estructura Django convencional.

1. `config_siges/` contiene configuración, rutas raiz, ASGI y WSGI.
2. `siges/` contiene modelos, formularios, vistas, rutas y comandos del aplicativo.
3. `templates/` contiene las interfaces HTML.
4. `static/siges/css/` contiene estilos.
5. `static/siges/js/` contiene interacciones del navegador.
6. `img/` contiene imagenes institucionales servidas como estáticos.
7. `docs/` contiene documentación del módulo.

## Flujo de componentes

1. El navegador solicita una pantalla o endpoint.
2. `siges/urls.py` enruta la peticion hacia `siges/views.py`.
3. `views.py` coordina formularios, consultas y renderizado.
4. `forms.py` valida las secciones.
5. `models.py` representa las tablas administradas y la fuente institucional de consulta.
6. `services.py` concentra consultas de establecimiento y persistencia de matriz.
7. PostgreSQL almacena la información en el esquema `SIGES`.

## Diagrama lógico

1. Archivo editable Draw.io: `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`.
2. El diagrama muestra el primer alcance funcional del modelo lógico SIGES para S01 y S02.
3. El archivo representa fuente institucional, parametrizacion de la matriz, registro de formulario, respuestas por sección y administración/trazabilidad.
4. El diagrama funciona como modelo lógico por capas, con variables, formatos y restricciones principales.
5. Las líneas representan relación funcional entre contenedores grandes, no conexión campo a campo.

## Decisiones de simplicidad

1. Se usan vistas basadas en funciones.
2. No se implementan APIs adicionales fuera de las necesarias para el buscador.
3. No se incorpora React, Vue ni Angular.
4. No se implementa autenticacion funcional en esta etapa.

## Uso de Unfold

1. `config_siges/settings.py` configura `UNFOLD` con cabecera, colores institucionales y navegación del panel administrativo.
2. `siges/admin.py` utiliza clases Unfold para modelos, fieldsets e inlines.
3. `siges/forms.py` agrega clases visuales compatibles con la semantica Unfold en los widgets del formulario.
4. Los templates propios mantienen la experiencia del aplicativo, pero usan clases `unfold-*` para conservar consistencia visual.



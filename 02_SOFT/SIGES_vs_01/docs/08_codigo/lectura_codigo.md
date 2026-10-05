# Lectura Técnica Del Código

## 1. Proposito

Este documento explica como leer el código del aplicativo SIGES sin mezclar responsabilidades. Sirve como base para auditoria técnica, mantenimiento y posterior construccion de informes en Quarto.

## 2. Criterio de documentación

1. El código fuente mantiene comentarios útiles y docstrings técnicos.
2. La explicación detallada queda en Markdown para evitar ensuciar archivos Python, HTML, CSS o JavaScript.
3. Cuando se requiera documentación línea por línea, se debe ampliar esta carpeta `docs/08_codigo/`.
4. Los templates quedan reservados para estructura HTML y textos editables.

## 3. Separación por capas

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| Configuración | `config_siges/` | Inicializar Django, base de datos, templates, estáticos y apps. |
| Modelo | `siges/models.py` | Representar tablas, relaciones, restricciones y fuente institucional. |
| Formulario | `siges/forms.py` | Definir campos, widgets y validaciones. |
| Vista/controlador | `siges/views.py` | Coordinar peticion, formulario, servicio, template y respuesta. |
| Servicio | `siges/services.py` | Centralizar consultas y persistencia reutilizable. |
| Rutas | `siges/urls.py` | Exponer endpoints HTML y JSON. |
| HTML | `templates/` | Estructura visual y textos editables. |
| CSS | `static/siges/css/` | Apariencia, layout y responsive. |
| JavaScript | `static/siges/js/` | Interacción del navegador y autocompletado. |
| Documentación | `docs/` | Explicación técnica y funcional versionable. |

## 4. Archivos CSS

1. `app.css`: archivo índice; importa el resto de hojas de estilo.
2. `00_base.css`: variables, tipografia, body, header, sidebar y layout general.
3. `01_componentes.css`: paneles, hero, tarjetas, formularios, tablas, stepper, detalle y componentes visuales.
4. `02_footer.css`: footer institucional, columnas, contacto, copyright y sello.
5. `03_responsive.css`: breakpoints para escritorio, tablet, móvil y pantallas angostas.

## 5. Archivos JavaScript

1. `establecimientos.js`: controla el buscador de establecimientos.
2. Escucha cambios en el campo de búsqueda.
3. Consulta `/api/establecimientos/buscar/`.
4. Renderiza resultados como botones.
5. Consulta `/api/establecimientos/<unicodigo>/`.
6. Autocompleta campos S01.

## 6. Flujo MVT Django

1. El navegador solicita una URL.
2. `config_siges/urls.py` dirige la solicitud hacia `siges/urls.py`.
3. `siges/urls.py` selecciona una vista.
4. `siges/views.py` coordina datos, formularios y servicios.
5. `siges/forms.py` valida entradas.
6. `siges/services.py` consulta o guarda datos.
7. `siges/models.py` representa las tablas PostgreSQL.
8. El template HTML se renderiza con contexto.
9. CSS y JavaScript se cargan desde `static`.

## 7. Regla para futuras modificaciones

1. Si se cambia texto visible, modificar templates.
2. Si se cambia apariencia, modificar CSS.
3. Si se cambia interacción de navegador, modificar JavaScript.
4. Si se cambia validación, modificar forms.
5. Si se cambia consulta o guardado reutilizable, modificar services.
6. Si se cambia flujo de página, modificar views.
7. Si se cambia estructura de datos, modificar models y documentar base de datos.



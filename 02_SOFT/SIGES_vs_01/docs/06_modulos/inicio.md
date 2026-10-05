# Módulo Inicio

## 1. Nombre del módulo

Inicio SIGES.

## 2. Objetivo funcional

Presentar la pantalla inicial del aplicativo y orientar al usuario hacia los tres flujos principales: establecimientos, roles y usuarios, y manual de usuario.

## 3. Ubicación de archivos

1. `templates/siges/inicio.html`
2. `siges/views.py`
3. `static/siges/css/01_componentes.css`
4. `static/siges/css/03_responsive.css`

## 4. Flujo de usuario

1. El usuario ingresa a `/`.
2. Django ejecuta la vista `inicio`.
3. La vista renderiza `templates/siges/inicio.html`.
4. El template muestra el hero institucional, los hexágonos informativos y las tarjetas de acceso.
5. El usuario selecciona una opción y navega a la pantalla correspondiente.

## 5. Entradas

1. Peticion HTTP GET a `/`.
2. Contexto `active_page='inicio'`.

## 6. Salidas

1. HTML del home institucional.
2. Accesos a `Establecimientos`, `Roles y usuarios` y `Manual de usuario`.

## 7. Lógica UI

1. El hero contiene el texto `Plataforma tecnológica desarrollada por:` y la unidad responsable.
2. Los hexágonos muestran acceso a establecimientos Red MSP, administración de roles y KPIs de Analytics en Salud.
3. Las tarjetas inferiores funcionan como navegación principal.
4. Cada tarjeta inferior usa un contenedor visual propio con borde, fondo blanco, sombra suave y estado hover.
5. La capa responsive reorganiza los componentes por ancho de pantalla.

## 8. Lógica server

1. La vista `inicio` no consulta base de datos.
2. La vista solo prepara el estado activo del menu.
3. La respuesta se entrega mediante `render`.

## 9. Reglas de negocio

1. El home no debe capturar datos.
2. El home no debe contener CSS ni JavaScript embebido.
3. La navegación debe mantenerse explicita y simple.

## 10. Validaciones realizadas

1. Ruta `/` responde HTTP 200.
2. El CSS se sirve desde archivos estáticos.
3. El template no contiene bloques `<style>` ni scripts embebidos.

## 11. Cambios realizados

1. Se adapto el hero institucional.
2. Se agregó texto superior de desarrollo tecnologico.
3. Se ajustaron hexágonos y comportamiento responsive.
4. Se reforzó el contenedor visual de cada opción de navegación del home principal.
5. Se actualizaron las etiquetas visibles de los hexágonos institucionales del home.
6. Se fijo la primera línea del hexágono principal para que `Todos los niveles de` no se divida visualmente.



# Modulo Manual de Usuario

## 1. Nombre del modulo

Manual de usuario.

## 2. Objetivo funcional

Reservar la pantalla donde posteriormente se publicara la guia funcional del sistema.

## 3. Ubicacion de archivos

1. `templates/siges/manual_usuario.html`
2. `siges/views.py`
3. `static/siges/css/01_componentes.css`
4. `static/siges/css/03_responsive.css`

## 4. Flujo de usuario

1. El usuario ingresa a `/manual/`.
2. La vista muestra el estado `En construccion`.
3. El usuario comprende que la documentacion funcional sera publicada despues.

## 5. Entradas

1. Peticion GET a `/manual/`.
2. Contexto `active_page='manual'`.

## 6. Salidas

1. Pantalla institucional de manual en construccion.

## 7. Logica UI

1. El panel principal usa `balanced-page-panel`.
2. El bloque interno `construction-box` reduce el alto para evitar espacio vertical excesivo.
3. El componente responde a pantallas desktop, tablet y movil.

## 8. Logica server

1. La vista `manual_usuario` no consulta base de datos.
2. La vista solo renderiza el template.

## 9. Reglas de negocio

1. No se debe documentar contenido funcional que aun no existe.
2. La pantalla debe indicar estado en construccion.

## 10. Validaciones realizadas

1. `/manual/` responde HTTP 200.
2. El footer mantiene estabilidad visual respecto a Roles y usuarios.

## 11. Cambios realizados

1. Se redujo el alto del bloque interno.
2. Se igualo el alto del panel principal con Roles y usuarios.



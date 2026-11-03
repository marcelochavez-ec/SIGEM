# Código Frontend

## 1. Proposito

Este documento explica la organizacion del frontend sin mezclar HTML, CSS y JavaScript.

## 2. Templates HTML

1. `templates/base.html` define el layout general.
2. `templates/sigem/inicio.html` contiene estructura y textos del home.
3. `templates/sigem/establecimientos.html` contiene estructura de gestión de establecimientos.
4. `templates/sigem/roles_usuarios.html` contiene estructura de acciones administrativas.
5. `templates/sigem/manual_usuario.html` contiene estructura del manual en construccion.
6. `templates/sigem/matriz_form.html` contiene estructura del formulario S01/S02.
7. `templates/sigem/matriz_detalle.html` contiene estructura del detalle guardado.
8. Los templates no contienen bloques CSS.
9. Los templates no contienen lógica JavaScript embebida, salvo carga de archivo estatico.

## 3. CSS

1. `app.css` importa las hojas especializadas.
2. `00_base.css` controla bases visuales y layout institucional.
3. `01_componentes.css` controla componentes reutilizables.
4. `02_footer.css` controla exclusivamente el footer.
5. `03_responsive.css` controla adaptacion a escritorio, tablet y móvil.

## 4. JavaScript

1. `establecimientos.js` permanece separado en `static/sigem/js`.
2. El script usa atributos `data-*` para encontrar elementos.
3. El script no depende de textos visibles para funcionar.
4. El script consume endpoints JSON.
5. El script actualiza campos S01 sin modificar templates.

## 5. Responsive

1. Desktop amplio conserva sidebar lateral.
2. Tablet convierte el menu en navegación superior.
3. Móvil apila tarjetas, formularios, filtros y footer.
4. Tablas mantienen scroll horizontal.
5. Botones ocupan ancho completo en móvil para mejorar uso tactil.

## 6. Reglas para editar textos

1. Cambiar textos de pantalla en templates.
2. No tocar CSS si solo cambia redacción.
3. No tocar JavaScript si solo cambia redacción.
4. Mantener clases y atributos `data-*` porque sostienen estilos e interacciones.



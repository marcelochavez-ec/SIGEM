# Interfaz

## Identidad visual

La interfaz adopta una referencia visual compatible con Analítica en Salud del MSP y con las nuevas pantallas institucionales SIGEM.

1. El encabezado usa un fondo azul institucional con transición hacia cyan.
2. El logotipo MSP se presenta en blanco mediante estilo CSS para conservar contraste sobre fondo azul.
3. El encabezado muestra el texto `Bienvenido(a) al`, el título `SIGEM` y el subtítulo `Sistema de Gestión y Monitoreo de los Establecimientos de Salud de la Red MSP`.
4. La navegación principal se presenta en una barra lateral izquierda con las opciones `Inicio`, `Establecimientos`, `Roles y usuarios` y `Manual de usuario`.
5. El footer institucional usa una franja compacta azul con textura punteada, columnas separadas, íconos Material Symbols, tecnología, recursos, contacto, aviso de sitio seguro, copyright y versión.
6. La tipografía global del aplicativo se define como `Century Gothic`, con escala reducida para evitar textos sobredimensionados.
7. El alto general se controla desde `00_base.css`, `01_componentes.css`, `02_footer.css` y `03_responsive.css` para que el footer sea visible con menor desplazamiento vertical en pantallas de escritorio, sin perder adaptación en tablet y móvil.
8. El encabezado mantiene una altura institucional intermedia para conservar presencia visual sin recuperar el exceso de scroll anterior.

## Componentes visuales

1. `templates/sigem/inicio.html` funciona como home inicial con banner institucional contrastado y tres tarjetas de acceso.
2. El home utiliza hexágonos informativos sin superposicion, Material Symbols y la imagen `img/establecimiento_salud.jpg` como referencia visual del establecimiento de salud.
3. `templates/sigem/establecimientos.html` contiene la pantalla de gestión de establecimientos, acciones principales y resumen visible de S01/S02.
4. `templates/sigem/roles_usuarios.html` contiene las acciones visuales de crear, modificar y desactivar roles o usuarios, enlazadas al panel administrativo Unfold/Django.
5. `templates/sigem/manual_usuario.html` contiene el estado `En construccion`, siguiendo la referencia visual entregada.
6. `templates/sigem/matriz_form.html` conserva el flujo real de captura S01/S02 dentro del nuevo layout institucional.
7. El buscador de establecimientos mantiene resultados visibles debajo del campo y consulta datos reales desde PostgreSQL.
8. No se utiliza animacion de numeros ni textura de puntos en el fondo del hero.
9. El diseño responde a pantallas angostas reordenando menu, tarjetas, formularios y footer sin superposiciones.
10. El footer mantiene el contenido tecnologico original: `Python`, `Django` y `Bootstrap`; `Recursos` muestra `Sincronizacion con PRAS y RDACAA`, `Interoperabilidad` e `Informes de monitoreo y control`; `Contacto` muestra correo, telefono y dirección institucional.
11. El hero no muestra texto flotante sobre la imagen institucional; los hexágonos quedan encajados con distancia mínima y uniforme para mantener lectura clara.
12. El bloque principal del home usa fondo celeste institucional y borde en la misma familia cromatica para diferenciarlo del fondo general sin romper la imagen institucional.
13. La pantalla `Manual de usuario` conserva el panel principal y reduce el alto del bloque interno `En construccion` para evitar exceso de espacio vertical.
14. Las pantallas `Roles y usuarios` y `Manual de usuario` comparten la clase `balanced-page-panel` para conservar el mismo alto del panel principal y evitar saltos del footer al navegar.
15. El hero del home muestra una línea superior `Sistema tecnologico para el registro de informacion desarrollado por:` y debajo la unidad responsable, ambas centradas verticalmente dentro del bloque.
16. La interfaz aplica una capa responsive por breakpoints equivalentes a Bootstrap para escritorio amplio, escritorio medio, tablet, móvil y móvil angosto.
17. En tablet y móvil, el menu lateral se reorganiza como navegación superior, las tarjetas pasan de grilla multiple a una columna, formularios y filtros se apilan, tablas quedan con desplazamiento horizontal y el footer se compacta en columnas verticales.
18. Los componentes Unfold propios del aplicativo mantienen tokens visuales, bordes, radios, sombras y estados consistentes en todos los breakpoints.
19. La hoja `app.css` funciona como índice de estilos y carga `00_base.css`, `01_componentes.css`, `02_footer.css` y `03_responsive.css` para mantener separada la presentacion por responsabilidad.
20. Los templates no contienen CSS embebido ni JavaScript funcional embebido; solo cargan archivos estáticos cuando corresponde.
21. Los paneles principales, el hero, las tarjetas de navegación, el menú lateral y el footer usan alturas y espaciados más compactos para reducir el scroll vertical general.
22. La clase `balanced-page-panel` dejó de depender de una altura fija alta y ahora usa una altura mínima adaptable al viewport mediante `clamp()` y `100dvh`.
23. Los elementos interactivos del aplicativo usan una regla global de cursor para mostrar la mano sobre enlaces, botones, selectores, controles accionables y componentes con atributos `data-*` utilizados por la interfaz.
24. La barra inferior del navegador que muestra la URL al pasar sobre enlaces reales pertenece al navegador y no al aplicativo; se conserva el uso de enlaces estándar para mantener accesibilidad, navegación normal y compatibilidad con abrir en nueva pestaña.

## Integracion visual con Unfold

1. `templates/base.html` carga estilos locales de Unfold: `unfold/fonts/inter/styles.css`, `unfold/fonts/material-symbols/styles.css` y `unfold/css/styles.css`.
2. La interfaz propia utiliza clases semanticas `unfold-*` para headers, tarjetas, pasos y campos.
3. Los tokens CSS `--unfold-primary`, `--unfold-surface`, `--unfold-border`, `--unfold-radius` y `--unfold-shadow` unifican la paleta del aplicativo con el estilo del panel administrativo.
4. Los formularios Django agregan clases `unfold-input` y `unfold-select` desde `forms.py`.
5. La administración Django utiliza `unfold.admin.ModelAdmin` y `unfold.admin.TabularInline`.



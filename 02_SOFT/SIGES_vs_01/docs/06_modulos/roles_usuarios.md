# Modulo Roles y Usuarios

## 1. Nombre del modulo

Administracion institucional de roles y usuarios.

## 2. Objetivo funcional

Presentar accesos institucionales para gestionar cuentas, grupos y permisos desde el panel administrativo Django/Unfold, conservando la identidad visual del aplicativo SIGES.

## 3. Ubicacion de archivos

1. `templates/siges/roles_usuarios.html`
2. `siges/views.py`
3. `siges/admin.py`
4. `static/siges/css/01_componentes.css`
5. `static/siges/css/03_responsive.css`
6. `static/siges/css/unfold_admin.css`
7. `config_siges/settings.py`
8. `templates/base.html`
9. `templates/unfold/layouts/base_simple.html`
10. `static/siges/js/unfold_admin.js`

## 4. Flujo de usuario

1. El usuario ingresa a `/roles-usuarios/`.
2. La vista consulta usuarios y grupos nativos de Django.
3. La pantalla muestra un resumen de usuarios registrados, usuarios activos y roles configurados.
4. La pantalla muestra accesos operativos para crear usuarios, modificar usuarios y administrar roles.
5. La opcion Crear usuario dirige al formulario de creacion de usuarios del admin Unfold.
6. La opcion Modificar usuarios dirige al listado de usuarios del admin Unfold.
7. La opcion Roles y permisos dirige al listado de grupos/perfiles del admin Unfold.
8. El panel Unfold mantiene navegacion hacia Inicio, Establecimientos, Roles y usuarios y catalogos SIGES.

## 5. Entradas

1. Peticion GET a `/roles-usuarios/`.
2. Contexto `active_page='roles'`.
3. Sesion autenticada de Django cuando el usuario ingresa al admin.
4. Permisos nativos de Django para usuarios, grupos y modelos SIGES.

## 6. Salidas

1. Pantalla de tablero operativo con resumen, acciones principales y consulta rapida.
2. Navegacion hacia rutas del admin Django/Unfold.
3. Pantallas administrativas con logo MSP, tipografia Century Gothic y paleta SIGES.

## 7. Fuentes de datos utilizadas

1. `auth_user`: tabla nativa de usuarios Django.
2. `auth_group`: tabla nativa de grupos/roles Django.
3. `auth_permission`: tabla nativa de permisos Django.
4. `SIGES.*`: modelos administrativos del formulario SIGES visibles en Unfold.

## 8. Reglas de negocio

1. El modulo publico no crea autenticacion paralela.
2. La gestion de cuentas usa las reglas nativas de Django.
3. El control de acceso se mantiene por usuario, grupo y permiso.
4. La interfaz administrativa debe verse integrada al aplicativo raiz.
5. Los estilos administrativos se cargan desde `static/siges/css/unfold_admin.css`.
6. Las imagenes institucionales se leen desde `img` mediante el sistema de archivos estaticos de Django.

## 9. Logica UI

1. `templates/siges/roles_usuarios.html` extiende `base.html`, por lo que conserva header, menu lateral y footer del aplicativo.
2. El bloque `role-summary-grid` muestra tres indicadores de control: usuarios registrados, usuarios activos y roles configurados.
3. El bloque `role-action-grid` organiza las tres acciones principales con icono, titulo y descripcion; la tarjeta completa funciona como enlace.
4. El bloque `role-lists-grid` muestra usuarios recientes y roles disponibles como consulta rapida.
5. `static/siges/css/01_componentes.css` contiene los estilos del tablero, tarjetas, iconos, listas y estados visuales.
6. `static/siges/css/03_responsive.css` adapta el tablero a desktop, tablet y movil.
7. Unfold usa el logo `logo_msp.png` servido desde los estaticos del proyecto.
8. El CSS del admin aplica Century Gothic, radio de 8px y colores institucionales.
9. `templates/unfold/layouts/base_simple.html` reemplaza localmente el layout base de Unfold para agregar cabecera y pie institucional al admin.
10. `static/siges/js/unfold_admin.js` fuerza la preferencia visual clara del admin en el navegador.

## 10. Logica server

1. `roles_usuarios` no modifica datos.
2. `get_user_model()` obtiene el modelo activo de usuarios de Django.
3. `User.objects.count()` calcula el total de usuarios registrados.
4. `User.objects.filter(is_active=True).count()` calcula usuarios habilitados.
5. `Group.objects.count()` calcula el total de roles/grupos configurados.
6. `User.objects.order_by("-date_joined")[:5]` recupera los cinco usuarios creados mas recientemente.
7. `Group.objects.order_by("name")[:5]` recupera los cinco primeros grupos ordenados alfabeticamente.
8. El contexto entrega indicadores, usuarios recientes, roles disponibles y `active_page='roles'` al template.
9. La gestion real de altas, modificaciones y roles queda delegada al admin Django/Unfold.
10. `settings.py` configura `UNFOLD` para tema claro, identidad, navegacion y estilos SIGES.
11. `base.html` versiona `app.css` para que el navegador recargue cambios visuales recientes.
12. `UNFOLD["SCRIPTS"]` carga `unfold_admin.js` antes de inicializar la interfaz administrativa.

## 11. Consultas SQL o logica ETL relevante

1. No existen consultas SQL manuales en este modulo.
2. Django ORM consulta `auth_user` para totales y usuarios recientes.
3. Django ORM consulta `auth_group` para totales y roles disponibles.
4. Django Admin administra `auth_permission` cuando se asignan permisos a grupos o usuarios.

## 12. Dependencias

1. Django Admin.
2. Django Auth.
3. Unfold.
4. Material Symbols.
5. CSS institucional del aplicativo.

## 13. Validaciones realizadas

1. Se debe ejecutar `python manage.py check` despues del cambio.
2. Se debe validar acceso a `/roles-usuarios/`.
3. Se debe validar acceso a `/admin/auth/user/`.
4. Se debe validar acceso a `/admin/auth/group/`.

## 14. Pruebas sugeridas

1. Ingresar con superusuario.
2. Crear un usuario de prueba.
3. Asignarlo a un grupo.
4. Confirmar que el grupo limita los permisos visibles.
5. Verificar que el logo y los estilos carguen correctamente en el admin.

## 15. Riesgos y supuestos

1. La seguridad depende de permisos Django correctamente asignados.
2. El modulo asume que Unfold esta instalado en el ambiente `msp_01`.
3. El modulo asume que `logo_msp.png` existe en la carpeta `img`.

## 16. Cambios realizados en esta tarea

1. Se rediseño la pantalla publica de Roles y usuarios como tablero SIGES.
2. Se agregaron indicadores de usuarios registrados, usuarios activos y roles configurados.
3. Se agrego consulta rapida de usuarios recientes y roles disponibles.
4. Se mantuvieron accesos al admin Unfold para crear usuarios, modificar usuarios y administrar grupos.
5. Se forzo Unfold a tema claro con `THEME='light'`.
6. Se adapto la capa responsive del tablero.
7. Se alineo Unfold con la identidad SIGES.
8. Se agrego navegacion administrativa para usuarios, grupos y catalogos SIGES.
9. Se agrego un CSS puente para el admin sin duplicar los estilos principales del aplicativo.
10. Se actualizo el parametro de version de `app.css` para evitar caché visual del navegador.
11. Se agrego un layout local de Unfold con cabecera y footer institucionales.
12. Se agrego un script de admin para limpiar la preferencia oscura persistida en el navegador.
13. Se reforzo el CSS del admin para mantener fondo claro y paleta institucional.
14. Se fijo el titulo del navegador del admin como `SIGES` en templates locales y script institucional.
15. Se retiraron las flechas laterales de las tarjetas principales para simplificar la lectura visual.

## 17. Pendientes o recomendaciones futuras

1. Definir perfiles institucionales finales antes de crear grupos productivos.
2. Revisar permisos con usuarios reales antes de habilitar acceso operativo.



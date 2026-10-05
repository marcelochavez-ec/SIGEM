# Codigo Python

## 1. Proposito

Este documento describe la funcion tecnica de los archivos Python principales del aplicativo.

## 1.1. Criterio de comentarios dentro del codigo

1. Los archivos Python principales incorporan docstrings para explicar el proposito de modulos, clases y funciones.
2. Los bloques criticos incorporan comentarios con `#` para explicar por que existe cada linea o grupo de lineas.
3. La documentacion evita convertir el codigo en una estructura compleja; solo agrega contexto para que el mantenedor pueda modificarlo.
4. El detalle narrativo complementario permanece en Markdown para preparar futuros informes Quarto.

## 2. `config_siges/settings.py`

1. Define la configuracion principal de Django.
2. Registra aplicaciones instaladas, incluyendo `SIGES` y Unfold.
3. Configura middleware.
4. Define ubicacion de templates.
5. Configura PostgreSQL `productos_bm`.
6. Define `search_path=SIGES,public` para trabajar en el schema funcional.
7. Configura archivos estaticos.
8. No debe contener contraseñas escritas directamente.

## 3. `siges/models.py`

1. `EstablecimientoIngresado` representa la fuente institucional `vm_establecimientos_ingresados`.
2. `managed=False` evita que Django intente crear o modificar esa fuente.
3. `FormularioSeccion` almacena secciones del formulario.
4. `FormularioVariable` almacena variables/campos parametrizables.
5. `FormularioOpcion` almacena catalogos de opciones.
6. `FormularioValidacion` almacena reglas documentables de validacion.
7. `SigesFormulario` funciona como cabecera de cada matriz.
8. `RespuestaS01` almacena datos generales.
9. `RespuestaS02` almacena acceso y movilizacion.
10. Las restricciones se declaran con `UniqueConstraint` y `CheckConstraint` cuando pertenecen al modelo administrado.
11. El archivo contiene comentarios por modelo, campo relevante, relacion y restriccion para facilitar cambios posteriores.

## 4. `siges/forms.py`

1. `texto` normaliza valores vacios.
2. `datos_s01_desde_establecimiento` transforma un registro institucional en datos del formulario S01.
3. `BaseSIGESForm` aplica clases visuales Unfold/Bootstrap-like a widgets.
4. `S01DatosGeneralesForm` define campos S01 y valida que el unicodigo exista.
5. `S01DatosGeneralesForm.clean` autocompleta datos institucionales faltantes.
6. `S02AccesoMovilizacionForm` define campos S02.
7. Los catalogos de S02 se cargan desde `FormularioOpcion`.
8. El archivo documenta con comentarios el origen de cada campo, la razon de los campos `readonly`, el autocompletado y la carga de catalogos.

## 5. `siges/views.py`

1. `health` expone una respuesta JSON simple para comprobar estado.
2. `api_buscar_establecimientos` entrega coincidencias al buscador.
3. `api_detalle_establecimiento` entrega datos para autocompletar S01.
4. `inicio` renderiza home.
5. `establecimientos` lista matrices y aplica filtros.
6. `roles_usuarios` renderiza accesos administrativos.
7. `manual_usuario` renderiza la pantalla en construccion.
8. `matriz_wizard` controla S01/S02, sesion temporal, validacion y guardado.
9. `detalle_matriz` muestra registros guardados.
10. El archivo documenta cada vista como controlador: lectura de parametros, seleccion de formulario, manejo de sesion, validacion y redireccion.

## 6. `siges/services.py`

1. `buscar_establecimientos` consulta la fuente institucional por unicodigo o nombre.
2. `obtener_datos_establecimiento` obtiene un establecimiento unico para autocompletar.
3. `guardar_matriz_SIGES` guarda cabecera, S01 y S02 dentro de una transaccion.
4. `full_clean` valida reglas del modelo antes de cerrar la persistencia.
5. El archivo documenta por comentarios cada paso de consulta y guardado transaccional.

## 7. `deploy_siges.py`

1. Valida dependencias basicas.
2. Inicializa Django.
3. Registra carpetas para autoreload.
4. Muestra informacion de inicio.
5. Levanta el servidor local en el puerto `8036`.
6. No debe imprimir credenciales.
7. No debe crear ni borrar estructuras de base de datos.
8. El archivo contiene comentarios sobre host, puerto, autoreload, Waitress y validacion inicial.

## 8. `siges/admin.py`

1. Configura el panel administrativo Django/Unfold.
2. Define listados, filtros, busquedas, fieldsets e inlines.
3. Documenta cada clase administrativa para diferenciar administracion tecnica de logica del aplicativo publico.

## 9. `config_siges/urls.py` y `siges/urls.py`

1. Documentan las rutas raiz y las rutas del aplicativo.
2. Cada `path` incluye un comentario funcional.
3. El namespace `siges` permite usar rutas con `{% url 'siges:nombre' %}` desde templates.



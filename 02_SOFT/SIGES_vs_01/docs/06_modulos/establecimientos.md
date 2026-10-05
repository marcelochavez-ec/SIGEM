# Modulo Establecimientos

## 1. Nombre del modulo

Gestion de establecimientos de salud.

## 2. Objetivo funcional

Permitir el acceso a la creacion, busqueda, modificacion y eliminacion de matrices SIGES asociadas a establecimientos de salud.

## 3. Ubicacion de archivos

1. `templates/siges/establecimientos.html`
2. `templates/siges/matriz_form.html`
3. `templates/siges/matriz_detalle.html`
4. `siges/views.py`
5. `siges/forms.py`
6. `siges/services.py`
7. `static/siges/js/establecimientos.js`
8. `static/siges/css/01_componentes.css`
9. `static/siges/css/03_responsive.css`
10. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/niveles_atencion.py`

## 4. Flujo de usuario

1. El usuario ingresa a `/establecimientos/`.
2. La pantalla muestra acciones de nuevo registro, modificacion y eliminacion.
3. El usuario inicia una nueva matriz desde S01.
4. S01 solicita el nivel de atencion antes de buscar unicodigos.
5. S01 permite buscar establecimientos reales por unicodigo o nombre dentro del nivel seleccionado.
6. El JavaScript consulta el endpoint JSON y autocompleta datos institucionales.
7. Al completar S01, el sistema permite avanzar a S02.
8. S02 registra frontera, movilizacion, frecuencia, tiempo de traslado, unidad del tiempo, categoria de accesibilidad y tipo de via.
9. Al guardar S02, la matriz queda persistida en PostgreSQL.
10. Desde el listado, el usuario puede seleccionar una matriz para modificarla.
11. Desde el listado, el usuario puede seleccionar una o varias matrices para eliminarlas.

## 5. Entradas

1. Filtros `q` y `unicodigo` en la pantalla de registros.
2. Campos `s01_dg01` a `s01_dg13`.
3. Campos `s02_am01` a `s02_am06`, incluyendo `s02_am04_unidad` para diferenciar horas y minutos.
4. Catalogos de `FormularioOpcion`.
5. Fuente `siges.vm_establecimientos_ingresados`.
6. Seleccion de registros mediante checkbox en el listado.
7. Selector `nivel_atencion` limitado a `I NIVEL DE ATENCION`, `II NIVEL DE ATENCION` y `III NIVEL DE ATENCION`.

## 6. Salidas

1. Listado de matrices SIGES.
2. Registro en `siges.siges_formulario`.
3. Registro en `siges.respuesta_s01`.
4. Registro en `siges.respuesta_s02`.
5. Detalle de matriz guardada.
6. Mensajes de confirmacion o advertencia cuando se modifica o elimina.

## 7. Logica UI

1. `establecimientos.html` muestra acciones principales y registros existentes.
2. `matriz_form.html` muestra el paginador S01/S02.
3. `matriz_detalle.html` muestra los datos guardados.
4. Las grillas se apilan en tablet y movil.
5. Las tablas conservan desplazamiento horizontal para evitar desbordes.
6. La pantalla de establecimientos ya no muestra resumen fijo de secciones, porque el aplicativo incorporara mas modulos.
7. El listado permite seleccionar todos los registros visibles o seleccionar registros individuales.
8. La accion `Modificar seleccionado` exige un solo registro seleccionado.
9. La accion `Eliminar seleccionados` permite eliminar uno o varios registros previa confirmacion del navegador.
10. La seccion de registros se organiza en tres niveles: encabezado operativo, busqueda por unicodigo y tabla de resultados.
11. El encabezado operativo contiene el boton primario `Nuevo registro`.
12. La busqueda separa consulta parcial y unicodigo exacto para reducir errores de captura.
13. La tabla muestra la matriz, unicodigo, estado, fecha de registro y acciones directas de ver/modificar.
14. Las acciones por fila se muestran como botones compactos con iconos para facilitar lectura de usuario final.
15. Las etiquetas principales del wizard no muestran codigos tecnicos `S01` o `S02`.
16. Los nombres visibles del wizard se leen desde `siges.formulario_seccion.nombre`.
17. El usuario final solo ve nombres funcionales de seccion y el unicodigo del establecimiento.
18. Los botones de accion inferiores se separan de los campos del formulario para mejorar lectura y evitar que queden pegados a los inputs.
19. En una nueva matriz, el usuario debe seleccionar primero el nivel de atencion para filtrar el buscador de unicodigos.
20. En S02, `Frontera`, `Unidad del tiempo de traslado` y `Categoria de accesibilidad` se muestran como opciones de seleccion unica.
21. El detalle de la matriz muestra el tiempo junto con su unidad seleccionada.
22. S02 organiza sus campos en bloques logicos: ubicacion fronteriza, movilizacion y transporte, tiempo de traslado, accesibilidad y via.
23. Cada variable principal de S02 muestra una descripcion breve debajo de la etiqueta para orientar al usuario final.
24. El campo numerico de tiempo se habilita visualmente solo despues de seleccionar `Horas` o `Minutos`.
25. La seccion activa del wizard se resalta con color institucional para indicar en que paso se encuentra el usuario.
26. El formulario de matriz ya no usa un contenedor visual grande alrededor de todo el flujo; conserva solo los bloques internos necesarios.
27. En S01, `Nivel de atencion del establecimiento de salud` aparece antes del buscador porque es el filtro principal del unicodigo.
28. El bloque de nivel de atencion se destaca visualmente con fondo turquesa suave.
29. Cuando S01 esta activo, el paso `Datos Generales` se resalta con color amarillo pastel.
30. S01 muestra textos de ayuda debajo de las etiquetas para explicar nivel, unicodigo, institucion, canton, parroquia, direccion, responsable y demas campos principales.

## 8. Logica server

1. `establecimientos` filtra registros por unicodigo.
2. `matriz_wizard` controla el paso actual.
3. `S01DatosGeneralesForm` valida unicodigo real.
4. `S02AccesoMovilizacionForm` carga catalogos activos.
5. `guardar_matriz_SIGES` persiste la informacion en una transaccion.
6. `establecimientos` procesa POST para modificar un registro seleccionado o eliminar varios registros seleccionados.
7. `matriz_wizard` obtiene nombres visibles desde `FormularioSeccion` antes de renderizar los templates.
8. `detalle_matriz` entrega nombres funcionales de seccion al template de detalle.
9. `SigesFormulario` apunta a `siges_formulario` y usa `id_formulario` entero secuencial.
10. `S02AccesoMovilizacionForm` obtiene sus listas desplegables desde `FormularioOpcion.descripcion`.
11. `FormularioOpcion.__str__` devuelve la descripcion para que los select muestren etiquetas funcionales y no codigos tecnicos.
12. `S01DatosGeneralesForm` valida que el unicodigo exista dentro del nivel de atencion seleccionado.
13. `buscar_establecimientos` recibe `nivel_atencion` y filtra `siges.vm_establecimientos_ingresados`.
14. `S02AccesoMovilizacionForm` carga `s02_am01`, `s02_am04_unidad` y `s02_am05` desde `FormularioOpcion`, pero guarda la etiqueta porque esas columnas son texto controlado.
15. `S02AccesoMovilizacionForm.clean()` valida que si la unidad es `Minutos`, el tiempo sea menor a 60.
16. `guardar_matriz_siges` persiste `s02_am04_unidad` junto con el resto de respuestas S02.
17. `datos_iniciales` precarga `s02_am04_unidad` al modificar una matriz existente.
18. `matriz_form.html` renderiza S02 con estructura especifica para agrupar preguntas relacionadas.
19. `static/siges/js/matriz_form.js` controla la habilitacion del tiempo segun la unidad seleccionada, sin incluir JavaScript dentro del template.
20. `matriz_form.html` renderiza S01 con el selector `nivel_atencion` separado del resto de campos para reforzar el flujo de captura.
21. `S01DatosGeneralesForm` define `help_text` por campo para entregar descripciones al template sin escribir textos sueltos en la vista.

## 9. Reglas de negocio

1. No se puede avanzar a S02 sin completar S01.
2. El unicodigo debe existir en la fuente institucional.
3. El tiempo hasta el Establecimiento de Salud no puede ser negativo.
4. Las opciones S02 deben pertenecer a su variable correspondiente.
5. Para modificar desde el listado se debe seleccionar exactamente una matriz.
6. Para eliminar se debe seleccionar al menos una matriz.
7. Las respuestas cerradas guardan la llave tecnica `id_opcion`, pero el usuario ve la etiqueta `descripcion`.
8. La cabecera del formulario no guarda `observaciones` ni `establecimiento_id`; el identificador funcional visible es el `unicodigo`.
9. El buscador de establecimientos solo consulta unicodigos del nivel de atencion seleccionado.
10. La cabecera `siges.siges_formulario` almacena `nivel_atencion` para trazabilidad y futura diferenciacion de formularios por nivel.
11. `Frontera` solo admite `Si` o `No`.
12. `Categoria de accesibilidad` solo admite `Urbano` o `Rural`.
13. La unidad del tiempo solo admite `Horas` o `Minutos`.
14. Si la unidad seleccionada es `Minutos`, el valor debe ser menor a 60; si son horas, se admiten valores decimales mayores o iguales a cero.

## 10. Validaciones realizadas

1. `/establecimientos/` responde HTTP 200.
2. `/matriz/nueva/?paso=s01` responde HTTP 200.
3. `python manage.py check` no reporta errores.
4. `SigesFormulario.objects` lee registros desde `siges.siges_formulario` con `id_formulario` entero.
5. `S02AccesoMovilizacionForm` despliega etiquetas de opciones: medio de movilizacion, frecuencia y tipo de via.
6. `/` responde HTTP 200 con Waitress levantado en el puerto 8036.
7. `/matriz/1/` responde HTTP 200 usando ruta entera.
8. `python -m py_compile` valido `forms.py`, `models.py`, `services.py`, `views.py` y `admin.py`.
9. `python manage.py check` no reporto errores.
10. `S02AccesoMovilizacionForm` cargo opciones reales: `Frontera` con `Si/No`, unidad con `Horas/Minutos`, categoria con `Urbano/Rural`, medio con 3 opciones, frecuencia con 4 opciones y tipo de via con 3 opciones.
11. La validacion funcional bloqueo `60` minutos y acepto `59` minutos.
12. El renderizado de `/matriz/nueva/?paso=s02` respondio HTTP 200, mostro la unidad de tiempo y ya no mostro el texto `Distrito`.
13. `/`, `/establecimientos/`, `/matriz/nueva/?paso=s01` y `/static/siges/js/matriz_form.js` respondieron HTTP 200 con servidor temporal en `127.0.0.1:8041`.
14. El renderizado de S02 contiene los bloques `Ubicacion fronteriza`, `Movilizacion y transporte`, `Tiempo de traslado` y `Accesibilidad y via`.
15. La validacion acepto `1.25` horas como valor decimal no negativo.
16. El renderizado de `/matriz/nueva/?paso=s01` respondio HTTP 200 sin el contenedor `content-panel unfold-card`.
17. El HTML de S01 muestra `Nivel de atencion del establecimiento de salud` antes de `Buscar establecimiento por unicodigo o nombre`.
18. El HTML de S01 contiene el bloque `level-selector-card` y el paso activo `step-s01 active`.

## 11. Cambios realizados

1. Se adapto la pantalla al layout responsive.
2. Se mantuvo JavaScript separado en `static/siges/js/establecimientos.js`.
3. Se mantuvo CSS separado en archivos estaticos por responsabilidad.
4. Se retiro el bloque informativo fijo de S01/S02 y la franja informativa de la pantalla de establecimientos.
5. Se agrego seleccion de registros, modificacion desde el listado y eliminacion masiva controlada.
6. Se rediseño el bloque de registros para separar busqueda, seleccion y resultados con mayor jerarquia visual.
7. Se actualizaron estilos responsivos para que la busqueda y la gestion de seleccion se apilen correctamente en tablet y movil.
8. Se actualizo el versionamiento de `app.css` para evitar cache visual del navegador.
9. Se retiraron codigos tecnicos `S01/S02` de las etiquetas principales de formulario y detalle.
10. Se conectaron los nombres visibles de seccion con la tabla `formulario_seccion`.
11. Se alineo Django con el schema `siges` y la tabla `siges_formulario`.
12. Se cambio la ruta de detalle y edicion de UUID a entero.
13. Se retiro `observaciones` del formulario y del servicio de guardado.
14. Se corrigio el arranque para usar `config_siges.settings` y la app real `siges`.
15. Se verifico que las preguntas cerradas muestren etiquetas desde catalogo y mantengan integridad por FK.
16. Se aumento el espaciado superior del bloque `.actions` para separar botones inferiores de los campos de captura.
17. Se simplifico el estilo global de botones primarios para usar color institucional plano, sin degradado lateral ni efecto visual recargado.
18. Se agrego selector de nivel de atencion en S01 y filtro de busqueda por nivel.
19. Se agrego almacenamiento de `nivel_atencion` en `siges.siges_formulario`.
20. Se creo el catalogo controlado `niveles_atencion.py` para documentar I, II y III nivel.
21. Se actualizo S02 para que `Frontera` y `Categoria de accesibilidad` sean opciones controladas desde catalogo.
22. Se agrego `s02_am04_unidad` en modelo, formulario, servicio, precarga de edicion, admin y detalle.
23. Se cambio la etiqueta de tiempo a `Tiempo hasta el Establecimiento de Salud`.
24. Se agrego validacion cruzada para impedir `60` minutos o valores superiores cuando la unidad sea minutos.
25. Se agrego estilo CSS para grupos de radio, manteniendo la identidad visual institucional.
26. Se reorganizo visualmente S02 en bloques logicos con descripciones de ayuda por campo.
27. Se agrego `matriz_form.js` para activar el campo de tiempo luego de seleccionar unidad.
28. Se reforzo el estado visual del paso activo del wizard.
29. Se agregaron reglas responsive para los nuevos bloques de S02.
30. Se retiro el contenedor visual grande del formulario de matriz.
31. Se reorganizo S01 para que el nivel de atencion sea el primer control operativo.
32. Se agregaron descripciones `help_text` a los campos S01.
33. Se agrego color amarillo pastel al paso activo de Datos Generales y fondo turquesa al selector de nivel.



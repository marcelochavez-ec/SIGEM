# Bloqueo de niveles II y III

## 1. Objetivo funcional

El formulario de datos generales permite seleccionar el nivel de atención. Los niveles II y III permanecen identificados como funcionalidades en construcción y no permiten iniciar la captura.

## 2. Archivos modificados

1. `sigem/forms.py`: valida en servidor los niveles II y III.
2. `templates/sigem/matriz_form.html`: incorpora el mensaje visual `En construcción`.
3. `static/sigem/js/establecimientos.js`: muestra el mensaje y desactiva los controles restantes.
4. `static/sigem/css/01_componentes.css`: presenta el estado deshabilitado.
5. `sigem/tests.py`: prueba los dos niveles bloqueados.

## 3. Flujo

1. El usuario selecciona el nivel de atención.
2. Si selecciona Nivel I, el buscador y los botones continúan disponibles.
3. Si selecciona Nivel II o Nivel III, aparece el mismo mensaje `En construcción` utilizado por el manual de usuario.
4. Se desactivan los controles y botones restantes; el selector de nivel permanece habilitado para cambiar a Nivel I.
5. Si se intenta enviar Nivel II o III directamente mediante HTTP, el formulario devuelve el mismo mensaje y no consulta ni guarda la matriz.

## 4. Reglas y validaciones

La regla se aplica en JavaScript para la respuesta inmediata y en `S01DatosGeneralesForm.clean()` para impedir que pueda omitirse desde el navegador. No se modifican modelos, tablas PostgreSQL ni catálogos.

## 5. Pruebas realizadas

Se agregaron pruebas unitarias para Nivel II y Nivel III. La ejecución debe realizarse con el entorno Conda `msp_01` mediante `python manage.py test sigem.tests.S01NivelConstruccionFormTest` desde `01_MSP/02_SOFT`.

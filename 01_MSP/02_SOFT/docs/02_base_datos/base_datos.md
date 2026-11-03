# Base De Datos

## Conexión

1. Base: `productos_bm`.
2. Schema funcional: `SIGEM`.
3. `search_path`: `SIGEM,public`.
4. Ambiente local: `msp_01`.

## Fuente institucional de consulta

### `sigem.vm_establecimientos_ingresados`

1. Estado: activa.
2. Uso: catálogo maestro para Sección 01.
3. Acción del aplicativo: solo lectura.
4. Modelo Django: `EstablecimientoIngresado`.
5. Configuración: `managed = False`.
6. Campo de búsqueda: `uni_codigo`.

Se verifico que `uni_codigo` y `uni_serial` no presentan duplicados en los registros consultados.

## Tablas administradas por Django para SIGEM

1. `sigem.sigem_formulario`.
2. `sigem.respuesta_s01`.
3. `sigem.respuesta_s02`.
4. `sigem.formulario_seccion`.
5. `sigem.formulario_variable`.
6. `sigem.formulario_opcion`.
7. `sigem.formulario_validacion`.

## Diagrama lógico

1. Archivo editable Draw.io: `docs/07_arquitecturas/modelo_entidad_relacion_sigem_s01_s02.drawio`.
2. Alcance: modelo lógico actual del aplicativo SIGEM con fuente institucional, parametrizacion, cabecera, respuestas S01/S02, administración y trazabilidad.
3. La relación entre `sigem.vm_establecimientos_ingresados` y `sigem.sigem_formulario` se documenta como referencia lógica por `uni_codigo`/`unicodigo`, no como llave foránea física.
4. El Draw.io evita líneas de relación detalladas y prioriza contenedores funcionales con tablas de variables, formatos, restricciones y uso funcional.

## Estructuras existentes observadas

1. Tablas `auth_*`, `django_*`: creadas por Django en el schema `sigem`. Se conservan para compatibilidad con admin, roles y usuarios.
2. La sección `S03` fue retirada porque no corresponde al alcance actual del aplicativo.
3. Los objetos heredados `sigem.respuesta_s03` y `sigem.vw_catalogo_s03` fueron eliminados del schema funcional.

## Protección aplicada

1. No se modifico `vm_establecimientos_ingresados`.
2. No se duplicaron registros del catálogo maestro.
3. La eliminación se limitó a objetos asociados a `S03`, previa instrucción explicita.



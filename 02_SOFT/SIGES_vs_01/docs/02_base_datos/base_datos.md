# Base De Datos

## Conexion

1. Base: `productos_bm`.
2. Schema funcional: `SIGES`.
3. `search_path`: `SIGES,public`.
4. Ambiente local: `msp_01`.

## Fuente institucional de consulta

### `siges.vm_establecimientos_ingresados`

1. Estado: activa.
2. Uso: catalogo maestro para Seccion 01.
3. Accion del aplicativo: solo lectura.
4. Modelo Django: `EstablecimientoIngresado`.
5. Configuracion: `managed = False`.
6. Campo de busqueda: `uni_codigo`.

Se verifico que `uni_codigo` y `uni_serial` no presentan duplicados en los registros consultados.

## Tablas administradas por Django para SIGES

1. `siges.siges_formulario`.
2. `siges.respuesta_s01`.
3. `siges.respuesta_s02`.
4. `siges.formulario_seccion`.
5. `siges.formulario_variable`.
6. `siges.formulario_opcion`.
7. `siges.formulario_validacion`.

## Diagrama logico

1. Archivo editable Draw.io: `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`.
2. Alcance: modelo logico actual del aplicativo SIGES con fuente institucional, parametrizacion, cabecera, respuestas S01/S02, administracion y trazabilidad.
3. La relacion entre `siges.vm_establecimientos_ingresados` y `siges.siges_formulario` se documenta como referencia logica por `uni_codigo`/`unicodigo`, no como llave foranea fisica.
4. El Draw.io evita lineas de relacion detalladas y prioriza contenedores funcionales con tablas de variables, formatos, restricciones y uso funcional.

## Estructuras existentes observadas

1. Tablas `auth_*`, `django_*`: creadas por Django en el schema `SIGES`. Se conservan para compatibilidad con admin, roles y usuarios.
2. La seccion `S03` fue retirada porque no corresponde al alcance actual del aplicativo.
3. Los objetos heredados `siges.respuesta_s03` y `siges.vw_catalogo_s03` fueron eliminados del schema funcional.

## Proteccion aplicada

1. No se modifico `vm_establecimientos_ingresados`.
2. No se duplicaron registros del catalogo maestro.
3. La eliminacion se limito a objetos asociados a `S03`, previa instruccion explicita.



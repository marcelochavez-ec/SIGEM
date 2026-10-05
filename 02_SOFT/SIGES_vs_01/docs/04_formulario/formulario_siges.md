# Formulario SIGES

## Flujo implementado

1. El usuario ingresa a la pagina principal.
2. El usuario crea una nueva matriz.
3. La Seccion 01 permite buscar un establecimiento real.
4. El buscador consulta `siges.vm_establecimientos_ingresados`.
5. Al seleccionar un `uni_codigo`, se autocompletan los campos institucionales.
6. La Seccion 01 valida el unicodigo contra PostgreSQL.
7. La Seccion 01 se conserva en sesion hasta completar S02.
8. La Seccion 02 valida los campos de acceso y movilizacion.
9. Al guardar S02, el aplicativo persiste cabecera, S01 y S02.
10. El usuario puede regresar a S01 desde S02 y editar una matriz guardada.

## Seccion 01

Los datos institucionales provienen de `vm_establecimientos_ingresados`.

1. `s01_dg01`: `uni_codigo`.
2. `s01_dg02`: `uni_nombre` o `establecimiento`.
3. `s01_dg03`: `tipologia`.
4. `s01_dg04`: `igu_descripcion`.
5. `s01_dg05`: `dp_descripcion` o `prv_descripcion`.
6. `s01_dg06`: `can_descripcion`.
7. `s01_dg07`: `par_descripcion`.
8. `s01_dg08`: `uni_direccion`.
9. `s01_dg09`: `estado`.
10. `s01_dg10`: `dificilacceso`.
11. `s01_dg11`: `represen_legal`.
12. `s01_dg12`: `tlf_movil`.
13. `s01_dg13`: `ced_ident_rep_legal`.

## Seccion 02

La Seccion 02 registra acceso y movilizacion.

1. Frontera.
2. Medio de movilizacion.
3. Frecuencia del transporte publico.
4. Tiempo hasta el Establecimiento de Salud.
5. Categoria de accesibilidad.
6. Tipo de via.

## Validaciones

1. S01 no avanza si el unicodigo no existe en PostgreSQL.
2. S01 no permite continuar sin responsable, movil y cedula.
3. S02 exige catalogos validos para los campos desplegables.
4. S02 exige que el tiempo sea mayor o igual a cero.



# Formulario SIGES

## Flujo implementado

1. El usuario ingresa a la página principal.
2. El usuario crea una nueva matriz.
3. La Sección 01 permite buscar un establecimiento real.
4. El buscador consulta `siges.vm_establecimientos_ingresados`.
5. Al seleccionar un `uni_codigo`, se autocompletan los campos institucionales.
6. La Sección 01 valida el unicódigo contra PostgreSQL.
7. La Sección 01 se conserva en sesión hasta completar S02.
8. La Sección 02 valida los campos de acceso y movilización.
9. Al guardar S02, el aplicativo persiste cabecera, S01 y S02.
10. El usuario puede regresar a S01 desde S02 y editar una matriz guardada.

## Sección 01

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

## Sección 02

La Sección 02 registra acceso y movilización.

1. Frontera.
2. Medio de movilización.
3. Frecuencia del transporte público.
4. Tiempo hasta el Establecimiento de Salud.
5. Categoría de accesibilidad.
6. Tipo de vía.

## Validaciones

1. S01 no avanza si el unicódigo no existe en PostgreSQL.
2. S01 no permite continuar sin responsable, móvil y cedula.
3. S02 exige catálogos validos para los campos desplegables.
4. S02 exige que el tiempo en horas sea mayor o igual a uno y que minutos sea entero entre uno y cincuenta y nueve.
5. Cuando el usuario registra horas decimales, el sistema almacena la parte entera en horas y convierte la fracción a minutos enteros.



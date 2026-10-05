# Base de datos SIGES - nivel 1

## 1. Nombre del modulo

Modulo de estructuras de base de datos del nivel 1 para el Sistema de Informacion para la Gestion de Establecimientos de Salud.

## 2. Objetivo funcional

Crear y verificar el esquema `siges` en la base de datos `productos_bm`, dejando listas las tablas maestras, tablas de respuesta, validaciones y vista de catalogo para las secciones iniciales del formulario:

1. `Datos Generales`.
2. `Acceso y Movilizacion`.

## 3. Ubicacion de archivos modificados o creados

1. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/configuracion.py`.
2. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/catalogos_nivel_1.py`.
3. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/ddl_nivel_1.py`.
4. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/ejecutar_nivel_1.py`.
5. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/niveles_atencion.py`.
6. `01_ESTRUCTURAS_BDD/01_BASE_DATOS/01_NIVEL/main_siges_nivel_1.py`.
7. `01_ESTRUCTURAS_BDD/01_ESTRUCTURAS_BDD/01_NIVEL/crear_estructuras_siges_nivel_1.py`.
8. `01_ESTRUCTURAS_BDD/04_DOCUMENTACION/01_NIVEL/base_datos_nivel_1.md`.
9. `.gitignore`.

## 4. Flujo general paso a paso

1. El script principal lee la configuracion PostgreSQL desde variables de ambiente o desde `01_ESTRUCTURAS_BDD/03_CONFIGURACIONES/config.yml`.
2. La conexion se arma con SQLAlchemy y el driver `psycopg`.
3. El DDL crea el esquema `siges` si no existe.
4. El DDL crea tablas, indices, funciones, triggers y vista del nivel 1.
5. El proceso carga o actualiza las secciones `s01` y `s02`.
6. El proceso carga o actualiza 20 variables funcionales.
7. El proceso carga o actualiza 16 opciones de catalogo para variables desplegables o dicotomicas.
8. El proceso carga o actualiza reglas documentales de validacion para unicodigo, frontera, tiempo, unidad de tiempo y categoria de accesibilidad.
9. El proceso verifica tablas, columnas y conteos esperados.

## 5. Entradas del modulo

1. Archivo de configuracion local: `01_ESTRUCTURAS_BDD/03_CONFIGURACIONES/config.yml`.
2. Variables de ambiente opcionales: `SIGES_DB_USER`, `SIGES_DB_PASSWORD`, `SIGES_DB_HOST`, `SIGES_DB_PORT`, `SIGES_DB_NAME` y `SIGES_DB_SCHEMA`.
3. Definicion funcional de secciones y variables en `catalogos_nivel_1.py`.
4. Definicion SQL estructural en `ddl_nivel_1.py`.

## 6. Salidas del modulo

1. Esquema PostgreSQL `siges`.
2. Tablas base del formulario.
3. Tablas de respuesta para S01 y S02.
4. Indices de busqueda e integridad.
5. Funciones y triggers de auditoria.
6. Vista `siges.vw_catalogo_formulario_nivel_1`.
7. Mensaje de verificacion con tablas faltantes, columnas faltantes, columnas adicionales y conteos.

## 7. Fuentes de datos utilizadas

1. `productos_bm.siges.formulario_seccion`: catalogo de secciones.
2. `productos_bm.siges.formulario_variable`: catalogo de variables.
3. `productos_bm.siges.formulario_opcion`: catalogo de opciones desplegables.
4. `productos_bm.siges.formulario_validacion`: reglas documentales de validacion.
5. `productos_bm.siges.siges_formulario`: cabecera de formulario.
6. `productos_bm.siges.respuesta_s01`: respuesta de datos generales.
7. `productos_bm.siges.respuesta_s02`: respuesta de acceso y movilizacion.
8. `productos_bm.siges.vm_establecimientos_ingresados`: fuente institucional de unicodigos y nivel de atencion.

## 8. Reglas de negocio aplicadas

1. El esquema oficial del modulo es `siges`.
2. La seccion `s01` contiene 13 variables institucionales de datos generales.
3. La seccion `s02` contiene 7 variables de acceso y movilizacion.
4. `s02_am01` corresponde a `Frontera` y se parametriza como catalogo dicotomico: `Si` y `No`.
5. `s02_am02`, `s02_am03` y `s02_am06` se mantienen como variables de catalogo para movilidad, frecuencia y tipo de via.
6. `s02_am04` se guarda como decimal y no permite valores negativos.
7. `s02_am04_unidad` registra la unidad del tiempo de traslado: `Horas` o `Minutos`.
8. Si `s02_am04_unidad` es `Minutos`, el valor de `s02_am04` debe ser menor o igual a 59.
9. Si `s02_am04_unidad` es `Horas`, el valor de `s02_am04` puede ser decimal mayor o igual a cero.
10. `s02_am05` corresponde a `Categoria de accesibilidad` y se parametriza como catalogo dicotomico territorial: `Urbano` y `Rural`.
11. Cada formulario tiene una respuesta S01 y una respuesta S02 mediante relacion uno a uno.
12. La integridad referencial protege que las opciones con llave foranea pertenezcan a la variable esperada.
13. Las restricciones `CHECK` de S02 protegen nuevas respuestas de frontera, unidad de tiempo, rango de minutos y categoria urbano/rural.
14. `siges_formulario.id_formulario` es un secuencial positivo de tipo `SERIAL`/`integer`, generado automaticamente desde 1 hasta N.
15. Cada respuesta S01 y S02 se relaciona con ese secuencial mediante `id_formulario`, conservando el vinculo con el `unicodigo` registrado en la cabecera.
16. `siges_formulario.nivel_atencion` almacena el nivel seleccionado para filtrar unicodigos y preparar formularios diferenciados por I, II y III nivel.
17. El catalogo controlado de niveles permite solo `I NIVEL DE ATENCION`, `II NIVEL DE ATENCION` y `III NIVEL DE ATENCION`.

## 9. Logica UI relacionada

Este modulo no implementa interfaz grafica. Sin embargo, deja la vista `vw_catalogo_formulario_nivel_1` preparada para que la capa web consulte:

1. Nombre visible de seccion.
2. Etiqueta visible de variable.
3. Tipo de control esperado.
4. Tipo de dato.
5. Opciones activas cuando la variable sea de catalogo.

## 10. Logica server relacionada

Este modulo no ejecuta logica Django. Su salida alimenta la capa server porque define:

1. Tablas de catalogo para formularios.
2. Tablas de persistencia para respuestas.
3. Restricciones de base que complementan validaciones del aplicativo.

## 11. Consultas SQL o logica ETL relevante

1. `CREATE SCHEMA IF NOT EXISTS siges`: crea el espacio logico de base de datos.
2. `CREATE TABLE IF NOT EXISTS`: permite ejecutar el proceso mas de una vez sin recrear tablas existentes.
3. `INSERT ... ON CONFLICT`: actualiza catalogos sin duplicar codigos.
4. `CREATE OR REPLACE VIEW`: actualiza la vista de lectura de catalogos.
5. `CREATE OR REPLACE FUNCTION`: actualiza funciones de auditoria e integridad.

## 12. Dependencias

1. Python en ambiente Conda `msp_01`.
2. `sqlalchemy`.
3. `psycopg`.
4. `PyYAML`.
5. PostgreSQL con acceso a la base `productos_bm`.

## 13. Validaciones realizadas

1. Conexion a PostgreSQL desde el ambiente `msp_01`.
2. Creacion del esquema `siges`.
3. Existencia de 7 tablas base esperadas.
4. Existencia de la vista `vw_catalogo_formulario_nivel_1`.
5. Conteo de 2 secciones.
6. Conteo de 20 variables.
7. Conteo de 16 opciones.
8. Conteo de 25 validaciones acumuladas en base, incluyendo reglas obligatorias y reglas especificas de S01/S02.
9. Verificacion sin tablas faltantes.
10. Verificacion sin columnas faltantes.
11. Verificacion sin columnas adicionales en las tablas esperadas.
12. Verificacion de tipo `integer` para `id_formulario` en `siges_formulario`, `respuesta_s01` y `respuesta_s02`.
13. Verificacion de la columna `s02_am04_unidad` en `respuesta_s02`.
14. Verificacion de catalogos S02: `Frontera`, `Unidad del tiempo de traslado`, `Categoria de accesibilidad` y `Tipo de via`.
15. Prueba transaccional con rollback: insercion valida con `59` minutos.
16. Prueba transaccional con rollback: bloqueo correcto de `60` minutos cuando la unidad es `Minutos`.

## 14. Pruebas ejecutadas

1. Ejecucion directa:

```powershell
python 01_ESTRUCTURAS_BDD\01_BASE_DATOS\01_NIVEL\main_siges_nivel_1.py
```

2. Ejecucion por ruta antigua compatible:

```powershell
python 01_ESTRUCTURAS_BDD\01_ESTRUCTURAS_BDD\01_NIVEL\crear_estructuras_siges_nivel_1.py
```

3. Consulta de control sobre `information_schema.tables` e `information_schema.views`.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. El proceso es de ejecucion unica para construir estructuras iniciales; no se calendariza en Airflow.
2. El proceso no elimina tablas ni columnas existentes.
3. Si en el futuro se requiere eliminar columnas productivas, debe hacerse con migracion controlada y respaldo previo.
4. Las claves y parametros sensibles permanecen fuera del codigo fuente.
5. Los indices se concentran en busquedas por `unicodigo`, `estado` y relaciones padre-hijo.
6. Se agrega indice sobre `nivel_atencion` para filtrar cabeceras por nivel cuando el volumen aumente.

## 16. Cambios realizados en esta tarea

1. Se separo el script monolitico en modulos de configuracion, catalogos, DDL, ejecucion y main.
2. Se corrigio el esquema operativo para trabajar sobre `siges`.
3. Se incorporo S01 y S02 en la estructura inicial.
4. Se corrigio el modelo de S02 para que solo las variables realmente catalogadas tengan claves foraneas a opciones.
5. Se agrego una vista consolidada de catalogos para el nivel 1.
6. Se protegio `config.yml` en `.gitignore`.
7. Se ajusto `id_formulario` para que sea secuencial `integer` positivo y no UUID ni `bigint`.
8. Se retiro `observaciones` de `siges_formulario` y se agrego una limpieza preventiva para `establecimiento_id` si quedara como columna heredada.
9. Se agrego `nivel_atencion` a `siges_formulario`.
10. Se creo `niveles_atencion.py` como DataFrame maestro de niveles permitidos.
11. Se parametrizo `s02_am01` como catalogo dicotomico `Si/No`.
12. Se cambio la etiqueta de `s02_am04` a `Tiempo hasta el Establecimiento de Salud`.
13. Se agrego la variable `s02_am04_unidad` con opciones `Horas` y `Minutos`.
14. Se agrego la regla de base para impedir minutos mayores a 59.
15. Se parametrizo `s02_am05` como catalogo `Urbano/Rural`.
16. Se reordeno `s02_am06` para quedar despues de la categoria de accesibilidad.
17. Se alineo el comando Django `cargar_catalogos_siges` con los catalogos del nivel 1 para evitar reversiones de metadata.

## 17. Pendientes o recomendaciones futuras

1. Cuando se defina el nivel 2, crear `01_ESTRUCTURAS_BDD/01_BASE_DATOS/02_NIVEL`.
2. Cuando se defina el nivel 3, crear `01_ESTRUCTURAS_BDD/01_BASE_DATOS/03_NIVEL`.
3. Alinear posteriormente la capa Django para mantener la capa Django alineada con el esquema `siges` y la tabla `siges_formulario`.

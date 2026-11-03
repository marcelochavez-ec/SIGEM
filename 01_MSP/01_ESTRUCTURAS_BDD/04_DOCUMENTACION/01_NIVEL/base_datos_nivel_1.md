# Base de datos SIGEM - Nivel 1

## 1. Nombre del módulo

Estructuras de base de datos del nivel 1 para el Sistema de Información para la Gestión de Establecimientos de Salud.

## 2. Objetivo funcional

Crear, actualizar y verificar la estructura inicial del esquema `sigem` en PostgreSQL para las dos primeras secciones del formulario:

1. **Datos Generales**.
2. **Acceso y Movilización**.

El proceso deja creadas las tablas maestras, tablas de respuesta, catálogos, validaciones, funciones, triggers, índices y vista de catálogo requeridos por el aplicativo SIGEM.

## 3. Archivo raíz de ejecución

El archivo que debe ejecutarse para construir o reconstruir la estructura del nivel 1 es:

```powershell
python 01_ESTRUCTURAS_BDD\01_BASE_DATOS\01_NIVEL\paso_00_main_sigem_nivel_1.py
```

Este archivo llama al orquestador del nivel 1 y no contiene lógica de negocio propia. Su función es ser el punto único y claro de arranque.

## 4. Orden de scripts del nivel 1

| Orden | Archivo | Función principal |
|---|---|---|
| 00 | `paso_00_main_sigem_nivel_1.py` | Punto de entrada. Ejecuta el proceso completo del nivel 1. |
| 01 | `paso_01_configuracion.py` | Lee variables de ambiente o `config.yml`, arma la configuración PostgreSQL y crea el motor SQLAlchemy. |
| 02 | `paso_02_catalogos_nivel_1.py` | Define secciones, variables, opciones y validaciones funcionales de S01 y S02. |
| 03 | `paso_03_niveles_atencion.py` | Define el DataFrame maestro de niveles de atención permitidos: I, II y III nivel. |
| 04 | `paso_04_ddl_nivel_1.py` | Construye el DDL PostgreSQL del esquema, tablas, restricciones, índices, funciones, triggers y vista. |
| 05 | `paso_05_ejecutar_nivel_1.py` | Orquesta la ejecución: prepara estructura heredada vacía, ejecuta DDL, carga catálogos, carga validaciones y verifica resultados. |

## 5. Flujo general paso a paso

1. `paso_00_main_sigem_nivel_1.py` llama a `crear_estructura_nivel_1()`.
2. `paso_05_ejecutar_nivel_1.py` obtiene la configuración mediante `paso_01_configuracion.py`.
3. Se abre una transacción con SQLAlchemy.
4. Se revisa si `sigem_formulario` conserva una estructura heredada vacía con `id_formulario` no entero o columnas ya retiradas.
5. Si la estructura heredada está vacía, se eliminan las tablas de respuesta y cabecera para permitir su recreación limpia.
6. Se ejecuta el DDL generado por `paso_04_ddl_nivel_1.py`.
7. Se crean, si no existen, el esquema `sigem`, tablas, relaciones, restricciones, índices, funciones, triggers y vista.
8. Se cargan o actualizan las secciones funcionales `s01` y `s02`.
9. Se cargan o actualizan las variables funcionales definidas para ambas secciones.
10. Se cargan o actualizan las opciones de catálogo para preguntas cerradas.
11. Se cargan o actualizan las reglas documentales de validación.
12. Se verifica la existencia de tablas, columnas, tipos clave y conteos esperados.
13. Se imprime un resumen operativo del proceso.

## 6. Qué se recrea si se borra la estructura

Si se elimina completamente el esquema `sigem` o se eliminan las tablas del nivel 1, el archivo raíz vuelve a crear:

1. Esquema `sigem`.
2. Tabla `formulario_seccion`.
3. Tabla `formulario_variable`.
4. Tabla `formulario_opcion`.
5. Tabla `formulario_validacion`.
6. Tabla `sigem_formulario`.
7. Tabla `respuesta_s01`.
8. Tabla `respuesta_s02`.
9. Índices funcionales y de búsqueda.
10. Función `fn_actualizar_fecha_actualizacion`.
11. Función `fn_actualizar_actualizado_en`.
12. Función `fn_validar_respuesta_s02_opciones`.
13. Triggers de actualización y validación.
14. Vista `vw_catalogo_formulario_nivel_1`.
15. Catálogos, variables, opciones y validaciones de S01/S02.

El proceso es idempotente: puede ejecutarse más de una vez sin duplicar catálogos. No borra datos productivos existentes de forma automática.

## 7. Alcance de recreación y protección de datos

1. Si las tablas no existen, se crean.
2. Si el esquema no existe, se crea.
3. Si los catálogos ya existen, se actualizan mediante `ON CONFLICT`.
4. Si existe una estructura heredada vacía, el proceso puede limpiarla y recrearla.
5. Si existe una estructura heredada con registros, el proceso se detiene y solicita migración controlada.
6. El proceso no ejecuta `DROP SCHEMA` ni elimina datos productivos sin instrucción explícita.

Esta regla protege registros reales. Para una reconstrucción total desde cero, primero debe eliminarse manualmente el esquema o las tablas objetivo con respaldo previo. Luego se ejecuta `paso_00_main_sigem_nivel_1.py`.

## 8. Entradas del módulo

1. Variables de ambiente opcionales:
   1. `SIGEM_DB_USER`.
   2. `SIGEM_DB_PASSWORD`.
   3. `SIGEM_DB_HOST`.
   4. `SIGEM_DB_PORT`.
   5. `SIGEM_DB_NAME`.
   6. `SIGEM_DB_SCHEMA`.
2. Archivo local opcional: `01_ESTRUCTURAS_BDD/03_CONFIGURACIONES/config.yml`.
3. Definición funcional en `paso_02_catalogos_nivel_1.py`.
4. Definición SQL en `paso_04_ddl_nivel_1.py`.

## 9. Salidas del módulo

1. Esquema PostgreSQL `sigem`.
2. Tablas maestras de formulario.
3. Tablas de respuesta de S01 y S02.
4. Relaciones y restricciones de integridad.
5. Índices.
6. Funciones y triggers de auditoría.
7. Vista consolidada de catálogo.
8. Resumen de verificación en consola.

## 10. Reglas de negocio aplicadas

1. `s01` contiene datos generales del establecimiento.
2. `s02` contiene acceso y movilización.
3. `id_formulario` es secuencial positivo de tipo `integer`.
4. `sigem_formulario` no usa `observaciones` ni `establecimiento_id`.
5. `nivel_atencion` queda almacenado en la cabecera del formulario.
6. S01 y S02 se relacionan con la cabecera mediante `id_formulario`.
7. Cada formulario tiene una respuesta S01 y una respuesta S02.
8. Las opciones de S02 se validan contra la variable que les corresponde.
9. El tiempo de traslado en `Horas` admite valores reales positivos mayores o iguales a `1`, con máximo dos decimales.
10. El tiempo de traslado en `Minutos` admite solo valores enteros positivos entre `1` y `59`.
11. `respuesta_s02` almacena el tiempo normalizado en `s02_am04_horas` y `s02_am04_minutos`.
12. Cuando el usuario registra horas decimales, la parte entera se almacena como horas y la fracción se convierte a minutos enteros.
13. La categoría de accesibilidad admite `Urbano` o `Rural`.
14. Frontera admite `Si`, `Sí` o `No`.

## 11. Dependencias

1. Python en ambiente Conda `msp_01`.
2. `sqlalchemy`.
3. `psycopg`.
4. `PyYAML`.
5. `pandas`.
6. PostgreSQL con acceso a la base `productos_bm`.

## 12. Validaciones esperadas

Al finalizar, el resumen debe mostrar:

1. `tablas_faltantes`: lista vacía.
2. `columnas_faltantes`: diccionario vacío.
3. `columnas_sobrantes`: diccionario vacío.
4. `tipos_incorrectos`: diccionario vacío.
5. `vistas_faltantes`: lista vacía.
6. `funciones_faltantes`: lista vacía.
7. `triggers_faltantes`: lista vacía.
8. `indices_faltantes`: lista vacía.
9. Conteos de secciones, variables, opciones y validaciones cargadas.

## 12.1 Validación ejecutada

1. Se ejecutó `python 01_ESTRUCTURAS_BDD\01_BASE_DATOS\01_NIVEL\paso_00_main_sigem_nivel_1.py`.
2. El proceso terminó correctamente sobre `productos_bm.sigem`.
3. Resultado operativo: 2 secciones, 20 variables, 16 opciones y 6 validaciones cargadas por el proceso.
4. La verificación devolvió tablas, columnas, vistas, funciones, triggers e índices faltantes como listas o diccionarios vacíos.
5. Se corrigió el DDL para eliminar el trigger heredado `trg_validar_respuesta_s02_opciones` antes de normalizar `respuesta_s02`, evitando referencias antiguas dentro de la función de validación.
6. Se consolidó la cabecera heredada `siges_formulario` hacia `sigem_formulario` cuando la tabla nueva está vacía y la heredada conserva registros, manteniendo las respuestas S01/S02 asociadas al mismo `id_formulario`.
7. Se verificó que `sigem_formulario`, `respuesta_s01` y `respuesta_s02` conserven 8 registros después de la consolidación.

## 13. Pruebas sugeridas

1. Ejecutar el archivo raíz:

```powershell
python 01_ESTRUCTURAS_BDD\01_BASE_DATOS\01_NIVEL\paso_00_main_sigem_nivel_1.py
```

2. Verificar que exista el esquema `sigem`.
3. Verificar que existan las siete tablas esperadas.
4. Verificar que exista `sigem.vw_catalogo_formulario_nivel_1`.
5. Revisar que `id_formulario` sea `integer`.
6. Revisar que `observaciones` y `establecimiento_id` no existan en `sigem_formulario`.

## 14. Consideraciones de seguridad

1. Las credenciales no deben quedar en el código fuente.
2. `config.yml` debe permanecer excluido por `.gitignore`.
3. No se debe subir a GitHub ninguna clave, token, contraseña ni host sensible.
4. La reconstrucción destructiva debe hacerse manualmente y con respaldo, no como comportamiento por defecto del script.

## 15. Cambios documentados en esta versión

1. Se deja una sola documentación oficial para `01_NIVEL`.
2. Se retira la documentación antigua de S03 que no correspondía al nivel 1 actual.
3. Se numeran los scripts con prefijo `paso_XX`.
4. Se declara `paso_00_main_sigem_nivel_1.py` como archivo raíz de ejecución.
5. Se documenta qué recrea el proceso cuando el esquema o las tablas fueron borradas.

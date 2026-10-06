# Modelo Lógico SIGES 01

## Archivo editable

1. Diagrama Draw.io: `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`.
2. El archivo puede abrirse en diagrams.net para revisar, mover bloques lógicos o exportar el modelo a PNG/PDF.
3. El diagrama está construido con formas, conectores y textos nativos de Draw.io; no es una imagen incrustada.
4. El alcance del archivo es lógico y de negocio; documenta la propuesta de tablas relacionadas previa al modelo entidad relación detallado.

## Tablas principales

1. `formulario_seccion`: define secciones activas de la matriz.
2. `formulario_variable`: define variables por sección.
3. `formulario_opcion`: define opciones de variables tipo catálogo.
4. `formulario_validacion`: registra reglas simples por variable.
5. `siges_formulario`: cabecera de cada matriz registrada.
6. `respuesta_s01`: respuesta de Datos Generales.
7. `respuesta_s02`: respuesta de Acceso y Movilización.

## Relaciones

```text
formulario_seccion (1) ─────── (N) formulario_variable
formulario_variable (1) ────── (N) formulario_opcion
formulario_variable (1) ────── (N) formulario_validacion
auth_user (1) ──────────────── (N) siges_formulario
siges_formulario (1) ───────── (1) respuesta_s01
siges_formulario (1) ───────── (1) respuesta_s02
formulario_opcion (1) <─────── (N) respuesta_s02.s02_am02
formulario_opcion (1) <─────── (N) respuesta_s02.s02_am03
formulario_opcion (1) <─────── (N) respuesta_s02.s02_am06
```

## Criterio de implementacion

1. S01 se guarda como texto porque la definición entregada contiene campos descriptivos sin catálogos cerrados.
2. S02 usa catálogos solo donde existen opciones previamente definidas: medio de movilización, frecuencia y tipo de vía.
3. `s02_am04` conserva el valor capturado y se normaliza en `s02_am04_horas` y `s02_am04_minutos`.
4. Si la unidad es `Horas`, la parte entera se almacena como horas y la fraccion se convierte a minutos enteros.
5. Si la unidad es `Minutos`, solo se admiten enteros entre `1` y `59`.
4. El modelo opera sobre PostgreSQL `productos_bm`, schema `SIGES`, usando el ambiente Conda `msp_01`.

## Diagrama lógico Draw.io S01/S02

1. El archivo `modelo_entidad_relacion_siges_s01_s02.drawio` resume visualmente el modelo lógico implementado para las dos primeras secciones.
2. El lienzo usa dimensiones amplias para permitir exportacion en alta resolucion desde Draw.io cuando se requiera usarlo en informes o presentaciones.
3. El diagrama muestra seis grupos: fuente institucional, parametrizacion lógica, registro SIGES, administración/trazabilidad, S01 y S02.
4. Cada grupo contiene tablas resumidas con variable, formato y restricción o uso funcional.
5. Las relaciones se dibujan solo entre contenedores funcionales grandes para conservar una lectura clara.

## Criterio de lectura

1. Azul: parametrizacion de la matriz.
2. Verde: registro y respuestas guardadas.
3. Amarillo: fuente institucional consultada.
4. Morado: administración y trazabilidad.
5. `vm_establecimientos_ingresados` se documenta como fuente de consulta y autocompletado por unicódigo, no como tabla con llave foránea física hacia el formulario.
6. Las variables se documentan con formato, restricción y uso funcional para facilitar revisión técnica sin depender de líneas de conexión entre cada tabla.



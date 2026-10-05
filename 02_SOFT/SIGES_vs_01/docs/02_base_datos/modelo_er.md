# Modelo Logico SIGES 01

## Archivo editable

1. Diagrama Draw.io: `docs/07_arquitecturas/modelo_entidad_relacion_siges_s01_s02.drawio`.
2. El archivo puede abrirse en diagrams.net para revisar, mover bloques logicos o exportar el modelo a PNG/PDF.
3. El diagrama esta construido con formas, conectores y textos nativos de Draw.io; no es una imagen incrustada.
4. El alcance del archivo es logico y de negocio; documenta la propuesta de tablas relacionadas previa al modelo entidad relacion detallado.

## Tablas principales

1. `formulario_seccion`: define secciones activas de la matriz.
2. `formulario_variable`: define variables por seccion.
3. `formulario_opcion`: define opciones de variables tipo catalogo.
4. `formulario_validacion`: registra reglas simples por variable.
5. `siges_formulario`: cabecera de cada matriz registrada.
6. `respuesta_s01`: respuesta de Datos Generales.
7. `respuesta_s02`: respuesta de Acceso y Movilizacion.

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

1. S01 se guarda como texto porque la definicion entregada contiene campos descriptivos sin catalogos cerrados.
2. S02 usa catalogos solo donde existen opciones previamente definidas: medio de movilizacion, frecuencia y tipo de via.
3. `s02_am04` es numerico decimal y no permite valores negativos.
4. El modelo opera sobre PostgreSQL `productos_bm`, schema `SIGES`, usando el ambiente Conda `msp_01`.

## Diagrama logico Draw.io S01/S02

1. El archivo `modelo_entidad_relacion_siges_s01_s02.drawio` resume visualmente el modelo logico implementado para las dos primeras secciones.
2. El lienzo usa dimensiones amplias para permitir exportacion en alta resolucion desde Draw.io cuando se requiera usarlo en informes o presentaciones.
3. El diagrama muestra seis grupos: fuente institucional, parametrizacion logica, registro SIGES, administracion/trazabilidad, S01 y S02.
4. Cada grupo contiene tablas resumidas con variable, formato y restriccion o uso funcional.
5. Las relaciones se dibujan solo entre contenedores funcionales grandes para conservar una lectura clara.

## Criterio de lectura

1. Azul: parametrizacion de la matriz.
2. Verde: registro y respuestas guardadas.
3. Amarillo: fuente institucional consultada.
4. Morado: administracion y trazabilidad.
5. `vm_establecimientos_ingresados` se documenta como fuente de consulta y autocompletado por unicodigo, no como tabla con llave foranea fisica hacia el formulario.
6. Las variables se documentan con formato, restriccion y uso funcional para facilitar revision tecnica sin depender de lineas de conexion entre cada tabla.



# SIGES 01

Aplicativo web Django para registrar la matriz SIGES contra PostgreSQL institucional.

## Alcance actual

1. Login con autenticacion nativa de Django.
2. Dashboard de registros con búsqueda y selección de `unicodigo`.
3. Formulario paginado por sección:
   1. `S01` - Datos Generales.
   2. `S02` - Acceso y Movilización.
4. Bloqueo de avance: no se puede pasar a S02 si S01 no esta completo y validado.
5. Logo MSP visible en la esquina superior izquierda.
6. Administración de catálogos mediante Django Unfold.

## Ejecución local con Conda

Desde una terminal de Positron:

```bash
conda activate msp_01
cd C:\Users\MARCELO\OneDrive\Documentos\MSP\14_SEP2026\03_SOFT_ATENCION_INTEGRAL\02_SOFT_SIGES\siges_01
pip install -r requirements.txt
```

Configurar la conexión PostgreSQL dentro del ambiente Conda `msp_01`:

```bash
conda env config vars set SIGES_DB_NAME=productos_bm
conda env config vars set SIGES_DB_USER=marcelo_chavez
conda env config vars set SIGES_DB_PASSWORD="TU_CLAVE_POSTGRESQL"
conda env config vars set SIGES_DB_HOST=10.64.100.191
conda env config vars set SIGES_DB_PORT=5432
conda env config vars set SIGES_DB_SCHEMA=siges
conda deactivate
conda activate msp_01
```

Levantar el aplicativo con un solo comando:

```bash
python deploy_siges.py
```

Este comando ejecuta `check` y levanta el servidor WSGI Waitress en el puerto `8036`. No ejecuta migraciones, no crea usuarios y no modifica PostgreSQL.

Si necesita levantar manualmente el servidor local:

```bash
python manage.py runserver 0.0.0.0:8036
```

Abrir:

```text
http://127.0.0.1:8036/
```

## Base de datos

El aplicativo apunta siempre a PostgreSQL:

```text
base   : productos_bm
schema : SIGES
host   : 10.64.100.191
puerto : 5432
```

No se usa SQLite. No se deben versionar credenciales reales.

La clave PostgreSQL no se guarda en archivos del proyecto. Debe estar definida en el ambiente Conda `msp_01` como `SIGES_DB_PASSWORD`.
La configuración Django tambien lee las variables persistidas en `C:\ProgramData\anaconda3\envs\msp_01\conda-meta\state`, para que los comandos locales usen la misma conexión institucional.

## Estructura principal

1. `config_siges/`: configuración Django, URLs raiz, WSGI y ASGI.
2. `deploy_siges.py`: arranque local con un solo comando.
3. `siges/`: aplicación funcional de la matriz SIGES.
4. `siges/models.py`: modelos de catálogo, cabecera y respuestas S01/S02.
5. `siges/forms.py`: formularios por sección.
6. `siges/views.py`: dashboard, paginación S01/S02, creación, edición y detalle.
7. `siges/management/commands/cargar_catalogos_siges.py`: carga idempotente de secciones, variables y opciones.
8. `siges/migrations/0001_initial.py`: migracion inicial compatible con tablas preexistentes.
9. `templates/siges/`: pantallas del aplicativo.
10. `static/siges/css/app.css`: estilos del aplicativo.
11. `img/logo_msp.png`: logo institucional mostrado en el encabezado.

## Variables implementadas

### S01 - Datos Generales

1. `s01_dg01`: Unicódigo.
2. `s01_dg02`: Establecimiento de Salud.
3. `s01_dg03`: Tipologia.
4. `s01_dg04`: Institución.
5. `s01_dg05`: Dirección Provincial.
6. `s01_dg06`: Cantón.
7. `s01_dg07`: Parroquia.
8. `s01_dg08`: Dirección del Establecimiento.
9. `s01_dg09`: Permiso de funcionamiento.
10. `s01_dg10`: Estado del predio.
11. `s01_dg11`: Nombres completos del Responsable.
12. `s01_dg12`: Móvil del Responsable.
13. `s01_dg13`: Cedula de identidad del Responsable.

### S02 - Acceso y Movilización

1. `s02_am01`: Frontera.
2. `s02_am02`: Medio de movilización.
3. `s02_am03`: Frecuencia del transporte público.
4. `s02_am04`: Tiempo hasta el Establecimiento de Salud.
5. `s02_am04_unidad`: Unidad del tiempo de traslado.
6. `s02_am05`: Categoría de accesibilidad.
7. `s02_am06`: Tipo de vía.



# Ejecución

## Comando principal

Desde Positron o PowerShell:

```powershell
conda activate msp_01
cd C:\Users\MARCELO\OneDrive\Documentos\MSP\14_SEP2026\03_SOFT_ATENCION_INTEGRAL\02_SOFT_SIGEM\SIGEM_01
python deploy_sigem.py
```

## Acceso

Local:

```text
http://127.0.0.1:8036
```

Red autorizada:

```text
http://IP_SERVIDOR:8036
```

## Alcance del lanzador

`deploy_sigem.py` realiza solamente:

1. Verificacion de existencia de `manage.py`.
2. Validación Django mediante `manage.py check`.
3. Levantamiento del servidor WSGI Waitress en `0.0.0.0:8036`.
4. Reinicio automatico cuando cambian archivos en `templates/`, `static/`, `img/`, `sigem/` o `config_sigem/`.

No realiza migraciones, no crea usuarios, no instala dependencias y no modifica PostgreSQL.

## Dependencia del servidor local

El aplicativo utiliza `waitress` para evitar el warning propio de `manage.py runserver`.

La configuración local de Waitress queda parametrizada para evitar saturacion de cola durante la carga simultanea de HTML, CSS, JavaScript e imagenes:

1. `SIGEM_WAITRESS_THREADS`: hilos WSGI. Valor por defecto: `16`.
2. `SIGEM_WAITRESS_CONNECTION_LIMIT`: conexiones concurrentes. Valor por defecto: `200`.
3. `SIGEM_WAITRESS_CHANNEL_TIMEOUT`: tiempo maximo de canal inactivo. Valor por defecto: `120`.

Si se requiere probar otros valores desde Positron:

```powershell
$env:SIGEM_WAITRESS_THREADS="24"
$env:SIGEM_WAITRESS_CONNECTION_LIMIT="300"
python deploy_sigem.py
```

Si el ambiente `msp_01` no tiene instalada la dependencia, se ejecuta una sola vez:

```powershell
pip install -r requirements.txt
```

## Autoreload

El autoreload esta activo por defecto. Al guardar cambios en templates HTML, CSS, JS, imagenes o código Python del aplicativo, el servidor se reinicia automaticamente.

Si se necesita desactivarlo temporalmente:

```powershell
$env:SIGEM_AUTORELOAD="false"
python deploy_sigem.py
```

## Detener el servidor

Para detener el servidor desde la terminal se utiliza:

```text
Ctrl + C
```

El lanzador captura esa interrupcion y muestra un cierre limpio sin traceback.



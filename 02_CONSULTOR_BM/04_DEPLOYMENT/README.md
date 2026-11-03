# Operación local y QA de SIGEM

Esta carpeta contiene scripts Python independientes de Codex para inspección Git, publicación controlada, validación previa y preparación de un plan para QA 194.

## Uso seguro

1. Activar `conda activate msp_01`.
2. Ejecutar `python 02_CONSULTOR_BM/04_DEPLOYMENT/01_git_local.py` para inspección.
3. Ejecutar `python 02_CONSULTOR_BM/04_DEPLOYMENT/02_github.py` para diagnóstico del remoto.
4. Ejecutar `python 02_CONSULTOR_BM/04_DEPLOYMENT/03_validar_qa.py --report 02_CONSULTOR_BM/04_DEPLOYMENT/logs/qa_local.md` para ejecutar `manage.py check` y las pruebas de `sigem.tests`.
5. Ejecutar `python 02_CONSULTOR_BM/04_DEPLOYMENT/04_servidor_194_qa.py` para generar el plan seguro con `HEAD`, o agregar `--ref <commit>`.
6. Para una comprobación remota de solo lectura en QA 194, usar `--check-remote --host 10.64.100.194 --user marcelo.chavez --remote-dir /home/marcelo.chavez/PROYECTO_BM/APPs/health_analytics_msp_31agosto2026 --ssh-key "$env:USERPROFILE/.ssh/id_ed25519_msp_monitoring"`.

Los scripts no publican, no conectan al servidor, no ejecutan migraciones ni modifican producción por defecto. Las credenciales y la configuración privada deben permanecer fuera de los archivos versionados.

## Resultado de validación local

Ejecutados el 3 de noviembre de 2026 con el ambiente Conda `msp_01`:

1. `01_git_local.py`: OK; inspección local sin modificar Git.
2. `02_github.py`: OK; remoto GitHub accesible mediante `git ls-remote`, sin publicar cambios.
3. `03_validar_qa.py`: APTO; `manage.py check` aprobado y 13 pruebas de `sigem.tests` aprobadas.
4. `04_servidor_194_qa.py`: permite generar el plan seguro o ejecutar una comprobación SSH explícita de solo lectura.

El archivo `config/qa.example.toml` es solo una plantilla y mantiene host, usuario, directorio y clave vacíos. La configuración real se pasa por argumentos y no se guarda en Git. El `HEAD` local y `origin/main` son distintos; no se ejecutó `push` automático.

## Verificación exclusiva de QA 194

La comprobación realizada en `10.64.100.194` utilizó:

- Ruta real encontrada: `/home/marcelo.chavez/PROYECTO_BM/APPs/health_analytics_msp_31agosto2026`.
- SSH, usuario y clave: conexión exitosa.
- Git remoto: rama `main`, commit `64a5b8056cafeece7c234e7a9a722c0f6b442cd8`.
- Estructura de deployment: `README_DEPLOY.md` y carpeta `deploy` presentes.
- URL local del servidor: `http://127.0.0.1:8595/app_direct/analytics-msp/` respondió `302 Moved Temporarily`.

La ruta histórica `APP_ANALYTICS_MSP` no existe en 194 y no se utiliza para la prueba. No se ejecutaron reinicios, migraciones, copias ni despliegues remotos.

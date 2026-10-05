# Estructuras de base de datos SIGES

Esta carpeta contiene la capa de estructuras de base de datos del proyecto SIGES.

## Organización

1. `01_BASE_DATOS`: scripts Python modulares para crear estructuras por nivel de establecimientos.
2. `01_ESTRUCTURAS_BDD`: rutas históricas o de compatibilidad para ejecuciones existentes.
3. `02_DATA_FUENTE`: archivos fuente usados como insumo técnico o documental.
4. `03_CONFIGURACIONES`: configuraciones locales de conexión. Los archivos sensibles no deben versionarse.
5. `04_DOCUMENTACION`: documentación técnica por nivel.
6. `05_ARQUITECTURAS`: modelos visuales y archivos de arquitectura.

## Nivel 1

El nivel 1 se ejecuta desde:

```powershell
python 01_ESTRUCTURAS_BDD\01_BASE_DATOS\01_NIVEL\paso_00_main_siges_nivel_1.py
```

La documentación técnica está en:

```text
04_DOCUMENTACION/01_NIVEL/base_datos_nivel_1.md
```


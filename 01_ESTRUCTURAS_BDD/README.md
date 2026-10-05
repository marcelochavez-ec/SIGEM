# Estructuras de base de datos SIGES

Esta carpeta contiene la capa de estructuras de base de datos del proyecto SIGES.

## Organizacion

1. `01_BASE_DATOS`: scripts Python modulares para crear estructuras por nivel de establecimientos.
2. `01_ESTRUCTURAS_BDD`: rutas historicas o de compatibilidad para ejecuciones existentes.
3. `02_DATA_FUENTE`: archivos fuente usados como insumo tecnico o documental.
4. `03_CONFIGURACIONES`: configuraciones locales de conexion. Los archivos sensibles no deben versionarse.
5. `04_DOCUMENTACION`: documentacion tecnica por nivel.
6. `05_ARQUITECTURAS`: modelos visuales y archivos de arquitectura.

## Nivel 1

El nivel 1 se ejecuta desde:

```powershell
python 01_ESTRUCTURAS_BDD\01_BASE_DATOS\01_NIVEL\main_cgs_nivel_1.py
```

Tambien se conserva la ruta anterior:

```powershell
python 01_ESTRUCTURAS_BDD\01_ESTRUCTURAS_BDD\01_NIVEL\crear_estructuras_siges_nivel_1.py
```

La documentacion tecnica esta en:

```text
04_DOCUMENTACION/01_NIVEL/base_datos_nivel_1.md
```


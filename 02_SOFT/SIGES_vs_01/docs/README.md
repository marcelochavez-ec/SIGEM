# Documentacion Del Aplicativo SIGES

## Proposito

Esta carpeta organiza la documentacion tecnica y funcional del aplicativo SIGES desarrollado en Django sobre PostgreSQL `productos_bm`, schema `SIGES`.

La documentacion esta separada por carpetas numeradas para que el recorrido sea natural: primero arquitectura, luego base de datos, interfaz, formulario, ejecucion, modulos y diagramas editables.

## Orden de lectura sugerido

1. Revisar `01_arquitectura` para entender la estructura general del aplicativo.
2. Revisar `02_base_datos` para entender tablas, relaciones y fuentes institucionales.
3. Revisar `03_interfaz` para entender la identidad visual y componentes de pantalla.
4. Revisar `04_formulario` para entender el flujo funcional de la matriz SIGES.
5. Revisar `05_ejecucion` para levantar el aplicativo localmente.
6. Revisar `06_modulos` para ver la documentacion tecnica del modulo implementado.
7. Revisar `07_arquitecturas` para abrir diagramas editables en Draw.io.
8. Revisar `08_codigo` para entender la separacion tecnica entre Python, HTML, CSS y JavaScript.

## Estructura documental

```text
docs/
├── README.md
├── 01_arquitectura/
│   ├── arquitectura.md
│   └── estructura_proyecto.md
├── 02_base_datos/
│   ├── base_datos.md
│   ├── modelo_er.md
│   └── MODEL_1_reference.png
├── 03_interfaz/
│   └── interfaz.md
├── 04_formulario/
│   └── formulario_siges.md
├── 05_ejecucion/
│   └── ejecucion.md
├── 06_modulos/
│   ├── siges_01.md
│   ├── establecimientos.md
│   ├── inicio.md
│   ├── manual_usuario.md
│   ├── reportes_monitoreo.md
│   └── roles_usuarios.md
└── 07_arquitecturas/
    └── modelo_entidad_relacion_siges_s01_s02.drawio
└── 08_codigo/
    ├── lectura_codigo.md
    ├── python.md
    └── frontend.md
```

## Contenido por carpeta

### `01_arquitectura`

1. Describe la arquitectura general del aplicativo.
2. Explica la separacion entre configuracion Django, aplicacion `SIGES`, templates, static, documentacion y script de inicio.
3. Documenta como esta ordenado el proyecto a nivel de carpetas y archivos principales.

### `02_base_datos`

1. Describe la conexion a PostgreSQL `productos_bm`.
2. Documenta el uso del schema `SIGES`.
3. Explica las tablas administradas por Django.
4. Registra la fuente institucional `siges.vm_establecimientos_ingresados`.
5. Incluye el modelo entidad relacion en Markdown y una imagen de referencia previa.

### `03_interfaz`

1. Documenta la identidad visual aplicada al aplicativo.
2. Explica el encabezado institucional, logo, colores, botones, tarjetas, formularios y paginacion.
3. Registra la integracion visual con Unfold en la capa de interfaz.

### `04_formulario`

1. Describe el flujo funcional del formulario SIGES.
2. Explica la captura por secciones S01 y S02.
3. Documenta reglas de avance, validaciones y comportamiento esperado para el usuario.

### `05_ejecucion`

1. Indica como iniciar el aplicativo localmente.
2. Documenta el uso del ambiente Conda `msp_01`.
3. Explica el script `deploy_siges.py`.
4. Registra consideraciones de puerto, PostgreSQL y servidor local.

### `06_modulos`

1. Contiene la documentacion tecnica de `siges_01` y sus modulos funcionales.
2. Resume objetivo, ubicacion de archivos, entradas, salidas, reglas de negocio, logica UI, logica server, dependencias, pruebas y riesgos.
3. Incluye modulos de inicio, establecimientos, roles y usuarios, reportes de monitoreo y manual de usuario.
4. Debe actualizarse cada vez que se modifique un modulo.

### `07_arquitecturas`

1. Contiene el diagrama editable oficial del primer modelo entidad relacion.
2. El archivo `modelo_entidad_relacion_siges_s01_s02.drawio` grafica el modelo logico del Sistema de Informacion para la Gestion de Establecimientos de Salud, organizado por fuente institucional, parametrizacion, cabecera, secciones, administracion y trazabilidad.
3. El archivo esta construido con objetos nativos de Draw.io; por tanto, sus bloques, textos y relaciones pueden moverse o editarse individualmente en Draw.io o diagrams.net.
4. El diagrama documenta la propuesta de tablas relacionadas previa al modelo entidad relacion detallado.

### `08_codigo`

1. Explica como leer el codigo por capas.
2. Documenta la separacion entre modelo, vista/controlador, templates, CSS, JavaScript y configuracion.
3. Sirve como base para documentacion linea por linea o bloque por bloque sin ensuciar el codigo fuente.

## Como esta ordenado el aplicativo

1. `config_siges/` contiene la configuracion principal de Django.
2. `siges/` contiene modelos, formularios, vistas, servicios, rutas, admin y comandos del aplicativo.
3. `templates/` contiene la estructura HTML institucional y pantallas de SIGES.
4. `static/` contiene CSS y JavaScript del aplicativo.
5. `img/` contiene activos institucionales como `logo_msp.png`.
6. `deploy_siges.py` levanta el aplicativo local en el puerto `8036`.
7. `requirements.txt` lista dependencias Python del proyecto.
8. `docs/` conserva la documentacion organizada y versionable.

## Criterios de mantenimiento

1. Mantener esta estructura numerada cuando se agreguen nuevos documentos.
2. No dejar documentos tecnicos sueltos en la raiz de `docs`, excepto este `README.md`.
3. Crear nuevos documentos en la carpeta que corresponda por tema.
4. Actualizar `06_modulos/siges_01.md` cuando cambie la logica del modulo.
5. Actualizar `08_codigo` cuando se reorganicen archivos o responsabilidades tecnicas.
6. Actualizar diagramas en `07_arquitecturas` cuando cambien relaciones, tablas o componentes relevantes.




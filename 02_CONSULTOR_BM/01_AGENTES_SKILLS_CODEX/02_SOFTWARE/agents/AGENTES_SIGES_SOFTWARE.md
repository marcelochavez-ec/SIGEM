
# AGENTES_SIGES_SOFTWARE.md

## Identificación del componente

1. **Tipo**: agente local de desarrollo de software.
2. **Propósito**: concentrar reglas operativas para mantener, validar y desplegar el aplicativo SIGES.
3. **Ámbito de aplicación**: capa de software Django, templates, estilos, JavaScript, documentación técnica, validaciones y despliegue.
4. **Forma de uso**: revisar este archivo antes de realizar cambios funcionales o visuales en el aplicativo. Sus reglas orientan el trabajo local y no forman parte del código productivo que se publica en GitHub.
5. **Ubicación centralizada**: `03_IA/02_SOFTWARE/agents/AGENTES_SIGES_SOFTWARE.md`.

# SIGES — Sistema Web para Gestión de Información Hospitalaria

> Regla visual vigente: todo el aplicativo debe usar `font-family: 'Century Gothic', sans-serif;` en el `body`, con escala tipográfica contenida y elegante para evitar textos sobredimensionados.

> Regla de organización vigente: los templates HTML deben contener estructura y textos editables; el CSS debe permanecer en `static/siges/css/`; el JavaScript debe permanecer en `static/siges/js/`; la lógica Python debe permanecer en `siges/views.py`, `siges/forms.py`, `siges/services.py` y `siges/models.py`. No se debe mezclar CSS o JavaScript dentro de templates salvo una carga de archivo estático mediante `{% static %}`.

> Regla de documentación vigente: la explicación técnica detallada, incluso línea por línea cuando sea necesario, debe quedar en Markdown dentro de `docs/`. El código fuente debe conservar comentarios útiles y docstrings técnicos, evitando comentarios obvios que ensucien la lectura. Para documentación analítica de código utilizar preferentemente `docs/08_codigo/`.

```text
============================================================
Autor: Ing. Marcelo Chávez
Consultor Especialista en Protección Social Banco Mundial
Email: marcelo_chavez_ec@outlook.com
============================================================
```

---

# 1. PROPÓSITO DEL AGENTE

Este archivo define las reglas obligatorias que deberá seguir Codex durante el desarrollo del aplicativo web **SIGES**.

SIGES será un sistema web desarrollado con **Python + Django**, destinado al registro progresivo y validado de información relacionada con la gestión hospitalaria.

El objetivo de este proyecto NO es construir una arquitectura sofisticada ni aplicar patrones innecesariamente complejos.

El objetivo es desarrollar una aplicación:

* ordenada;
* estable;
* mantenible;
* modular;
* comprensible;
* documentada;
* visualmente profesional;
* fácil de modificar;
* compatible con los conocimientos de Python de un ingeniero estadístico;
* preparada para crecer progresivamente.

Debe priorizarse permanentemente:

> **Simplicidad + claridad + separación de responsabilidades + documentación.**

Nunca deberá priorizarse sofisticación técnica sobre mantenibilidad.

---

# 2. PRINCIPIO GENERAL DE DESARROLLO

Codex deberá comportarse como un desarrollador cuidadoso que trabaja sobre un sistema institucional.

NO deberá comportarse como un generador autónomo que modifica indiscriminadamente el proyecto.

Antes de crear, borrar, reemplazar, migrar o reorganizar cualquier componente deberá analizar:

1. qué existe;
2. qué se utiliza;
3. qué puede reutilizarse;
4. qué falta;
5. qué podría estar obsoleto;
6. qué modificación es realmente necesaria.

Se utilizará siempre la solución técnicamente correcta **más sencilla posible**.

---

# 3. REGLA FUNDAMENTAL: EVITAR SOBREINGENIERÍA

Está expresamente prohibido introducir arquitectura innecesariamente compleja.

NO deberán incorporarse, salvo requerimiento explícito posterior:

* microservicios;
* arquitectura hexagonal;
* Clean Architecture compleja;
* CQRS;
* event sourcing;
* RabbitMQ;
* Kafka;
* Celery;
* Redis;
* Kubernetes;
* GraphQL;
* APIs separadas sin necesidad;
* repositorios abstractos;
* servicios genéricos excesivos;
* factories innecesarias;
* múltiples capas de abstracción;
* patrones avanzados que dificulten entender el flujo;
* autenticación externa;
* Keycloak;
* OAuth;
* JWT;
* Docker Swarm;
* orquestadores complejos.

Si una funcionalidad puede resolverse de forma clara con Django estándar, deberá utilizarse Django estándar.

---

# 4. NIVEL DE COMPLEJIDAD DEL CÓDIGO

La programación deberá escribirse pensando en que posteriormente será mantenida directamente por un profesional con conocimientos de:

* estadística;
* Python;
* SQL;
* PostgreSQL;
* análisis de datos;
* desarrollo web básico/intermedio.

El código podrá ser extenso si eso mejora su claridad.

Se deberá preferir:

```python
if condicion:
    accion()
```

sobre estructuras innecesariamente abstractas.

La prioridad será:

> que el código pueda abrirse, leerse y entenderse rápidamente.

---

# 5. UBICACIÓN DEL PROYECTO

El aplicativo deberá desarrollarse dentro del proyecto SIGES existente.

La raíz de trabajo corresponde conceptualmente a:

```text
02_SOFT_SIGES/
└── siges_01/
```

Codex deberá trabajar únicamente dentro del proyecto asignado.

No deberá crear proyectos Django paralelos sin autorización.

No deberá crear carpetas arbitrarias fuera de la estructura acordada.

---

# 6. ENTORNO PYTHON

Existe un entorno Python prevíamente definido.

Se utilizará:

```text
msp_01
```

Codex NO deberá:

* crear un nuevo ;
* crear otro entorno Conda;
* ejecutar ;
* crear ;
* sustituir el entorno existente;
* modificar el entorno global sin necesidad.

El aplicativo deberá asumir que prevíamente se activa:

```bash
conda activate msp_01
```

Posteriormente deberá poder iniciarse utilizando un único comando Python.

---

# 7. ARCHIVO ÚNICO DE ARRANQUE

Deberá existir en la raíz del proyecto un archivo:

```text
deploy_siges.py
```

Su propósito será exclusivamente simplificar el inicio de la aplicación.

El usuario deberá poder ejecutar:

```bash
python deploy_siges.py
```

y obtener el aplicativo disponible en:

```text
http://127.0.0.1:8036
```

Para acceso desde otras máquinas de una red autorizada podrá utilizarse:

```text
http://IP_DEL_SERVIDOR:8036
```

El servidor de desarrollo deberá levantarse conceptualmente como:

```bash
python manage.py runserver 0.0.0.0:8036
```

El archivo  podrá realizar comprobaciones sencillas como:

* verificar que  exista;
* verificar que Django pueda inicializarse;
* mostrar el puerto de ejecución;
* ejecutar el servidor.

NO deberá:

* crear bases;
* crear usuarios;
* ejecutar borrados;
* eliminar tablas;
* modificar datos;
* reconstruir automáticamente el esquema;
* crear entornos Python;
* instalar paquetes automáticamente;
* ejecutar migraciones destructivas.

---

# 8. PUERTO DEL APLICATIVO

Durante esta etapa el puerto oficial de pruebas será:

```text
8036
```

Por tanto:

```text
HOST = 0.0.0.0
PORT = 8036
```

No deberá modificarse este puerto arbitrariamente.

---

# 9. FRAMEWORK

Se utilizará:

```text
Python
Django
PostgreSQL
Django Unfold
HTML
CSS
JavaScript
```

Unfold podrá utilizarse para apoyar componentes administrativos y coherencia visual cuando corresponda.

Sin embargo, SIGES NO deberá convertirse simplemente en una personalización del Django Admin.

Las pantallas principales deberán ser interfaces propias del aplicativo.

---

# 10. ALCANCE DE LA PRIMERA ETAPA

La primera implementación funcional deberá concentrarse exclusivamente en:

```text
SECCIÓN 01 — Datos generales
SECCIÓN 02 — Segunda sección del formulario SIGES
```

No deberán construirse anticipadamente todas las secciones futuras.

La arquitectura deberá permitir agregarlas posteriormente sin rehacer el sistema.

---

# 11. FLUJO GENERAL DEL FORMULARIO

SIGES funcionará como un formulario secuencial.

Ejemplo:

```text
Inicio
   ↓
Sección 01
   ↓
Validación
   ↓
Guardar
   ↓
Sección 02
   ↓
Validación
   ↓
Guardar
   ↓
Siguiente sección futura
```

Una sección NO podrá considerarse terminada mientras existan campos obligatorios inválidos o incompletos.

---

# 12. REGLA DE NAVEGACIÓN ENTRE SECCIONES

El sistema deberá permitir:

```text
Anterior
Guardar
Guardar y continuar
```

El usuario podrá regresar a una sección anterior.

Ejemplo:

```text
Sección 01
   ↓
Sección 02
   ↓
Volver a Sección 01
   ↓
Modificar
   ↓
Guardar
   ↓
Continuar nuevamente
```

Los datos prevíamente registrados deberán recuperarse.

No deberán desaparecer al navegar entre secciones.

---

# 13. VALIDACIÓN OBLIGATORIA

Cada sección deberá tener validaciónes independientes.

Las validaciónes deberán implementarse principalmente utilizando:

```text
forms.py
```

No deberán concentrarse todas las validaciónes dentro de:

```text
views.py
```

Cuando una sección contenga errores:

* deberá permanecer en esa sección;
* deberá mostrar claramente qué campos tienen problemas;
* deberá conservar los datos válidos ya ingresados;
* no deberá avanzar a la siguiente sección.

---

# 14. NO PERMITIR SECCIONES VACÍAS

Las secciones obligatorias no podrán omitirse.

El sistema no deberá permitir avanzar simplemente pulsando:

```text
Siguiente
```

si existen campos obligatorios sin completar.

---

# 15. SECCIÓN 01 — DATOS GENERALES

La primera sección utilizará información institucional existente en PostgreSQL.

La variable principal de identificación será:

```text
unicodigo
```

El usuario deberá poder:

1. escribir parcialmente un unicódigo;
2. visualizar coincidencias;
3. selecciónar un establecimiento;
4. recuperar automáticamente sus datos.

---

# 16. BUSCADOR DE UNICÓDIGO

NO deberá utilizarse un  HTML cargando miles de registros de golpe.

Deberá existir un buscador/autocompletado.

Ejemplo visual:

```text
┌─────────────────────────────────────────┐
│ Buscar establecimiento                  │
│ 000123...                               │
└─────────────────────────────────────────┘

Resultados:

000123 — Hospital ...
000124 — Centro de Salud ...
000125 — Hospital ...
```

El usuario podrá buscar utilizando:

* unicódigo;
* nombre del establecimiento;

si ambos campos existen en la fuente.

---

# 17. AUTOCOMPLETADO DE DATOS

Después de selecciónar el unicódigo correcto, los campos institucionales deberán completarse automáticamente.

Conceptualmente:

```text
UNICÓDIGO
    ↓
PostgreSQL
    ↓
siges.vm_establecimientos_ingresados
    ↓
establecimiento seleccionado
    ↓
Datos generales
```

Los datos institucionales recuperados desde el catálogo maestro no deberán obligar al usuario a volver a escribir información que ya existe.

---

# 18. TABLA MAESTRA DE ESTABLECIMIENTOS

La fuente principal para esta etapa será:

```text
siges.vm_establecimientos_ingresados
```

Esta estructura se considera:

> FUENTE DE CONSULTA / CATÁLOGO MAESTRO PARA LA SECCIÓN 01.

Codex deberá comprobar primero que realmente puede obtener registros desde esta tabla o vista.

Antes de diseñar el buscador deberá ejecutar una prueba equivalente a:

```sql
SELECT *
FROM siges.vm_establecimientos_ingresados
LIMIT 10;
```

También deberá confirmar la existencia y contenido del campo correspondiente al:

```text
unicodigo
```

No deberá asumir nombres de columnas sin inspeccionarlos.

---

# 19. PROHIBIDO SIMULAR UNICÓDIGOS

Está prohibido:

* colocar unicódigos en listas Python;
* inventar establecimientos;
* crear datos de prueba como sustituto de PostgreSQL;
* insertar catálogos manualmente;
* hardcodear establecimientos en JavaScript;
* duplicar el catálogo dentro del aplicativo.

La consulta deberá provenir realmente de PostgreSQL.

---

# 20. BASE DE DATOS

La aplicación trabajará con la base institucional:

```text
productos_bm
```

El esquema funcional correspondiente al aplicativo será:

```text
SIGES
```

Todas las estructuras nuevas propias de SIGES deberán permanecer dentro de:

```text
productos_bm.SIGES
```

No deberán crearse tablas de negocio en:

```text
public
```

ni en esquemas diferentes sin autorización.

---

# 21. CREDENCIALES DE BASE DE DATOS

Está prohibido escribir directamente en el código:

```python
password = "..."
```

Las credenciales deberán manejarse mediante configuración externa.

Puede utilizarse:

```text
.env
```

o el mecanismo ya utilizado institucionalmente por el proyecto.

Las variables podrán representar:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_SCHEMA
```

Por ejemplo:

```text
DB_NAME=productos_bm
DB_SCHEMA=SIGES
```

Los valores reales de credenciales no deberán almacenarse en Git.

---

# 22. SEARCH_PATH DE POSTGRESQL

Django deberá quedar correctamente configurado para trabajar prioritariamente con:

```text
SIGES
```

Cuando corresponda podrá configurarse PostgreSQL mediante:

```text
search_path=SIGES,public
```

El objetivo es evitar que Django cree accidentalmente estructuras funcionales de SIGES dentro de .

---

# 23. MODELOS SOBRE TABLAS EXISTENTES

Cuando una tabla o vista ya exista y Django únicamente necesite consultarla, deberá analizarse el uso de:

```python
class Meta:
    managed = False
```

Ejemplo conceptual:

```python
class Establecimiento(models.Model):
    ...

    class Meta:
        managed = False
        db_table = 'vm_establecimientos_ingresados'
```

Esto evitará que Django intente recrear estructuras maestras que ya existen.

---

# 24. MODELO ENTIDAD–RELACIÓN

Todo el modelo entidad–relación correspondiente a SIGES deberá pertenecer al esquema:

```text
SIGES
```

El diseño deberá ser coherente.

No deberán existir tablas SIGES dispersas en diferentes esquemas.

---

# 25. TABLAS EXISTENTES

Antes de generar modelos nuevos, Codex deberá inspeccionar las tablas existentes.

Deberá clasificarlas conceptualmente como:

```text
A. Activa
B. Reutilizable
C. Posiblemente obsoleta
D. Desconocida
```

Este análisis deberá documentarse.

---

# 26. PROHIBICIÓN DE ELIMINAR TABLAS AUTOMÁTICAMENTE

Codex NO tiene autorización para ejecutar:

```sql
DROP TABLE
DROP SCHEMA
TRUNCATE
CASCADE
```

sobre estructuras existentes salvo instrucción explícita del usuario.

Aunque una tabla parezca obsoleta, deberá solamente documentarse.

Ejemplo:

```text
Tabla:
SIGES.tabla_antigua

Estado:
Posiblemente obsoleta.

Motivo:
No existe referencia desde los modelos actuales.

Acción:
NINGUNA.

Recomendación:
Revisar manualmente antes de eliminar.
```

---

# 27. LIMPIEZA DE ESTRUCTURAS ANTIGUAS

Si posteriormente se requiere limpiar tablas antiguas, deberá crearse un script SQL independiente.

Por ejemplo:

```text
sql/
└── revision_tablas_obsoletas.sql
```

Pero dicho script NO deberá ejecutarse automáticamente.

---

# 28. MIGRACIONES

Las migraciones Django deberán utilizarse únicamente para estructuras administradas realmente por Django.

No deberán generarse migraciones que intenten modificar tablas institucionales existentes sin necesidad.

Antes de:

```bash
python manage.py makemigrations
python manage.py migrate
```

Codex deberá conocer qué modelos son administrados por Django y cuáles no.

---

# 29. AUTENTICACIÓN

Durante esta etapa inicial:

> NO SE IMPLEMENTARÁ AUTENTICACIÓN FUNCIONAL DEL APLICATIVO.

No deberán crearse:

* páginas de login personalizadas;
* usuarios SIGES;
* roles MASTER;
* roles zonales;
* perfiles;
* permisos propios;
* recuperación de contraseñas;
* OAuth;
* Keycloak;
* JWT.

La autenticación será incorporada posteriormente cuando el formulario básico esté estabilizado.

---

# 30. ESTRUCTURA GENERAL RECOMENDADA

Se deberá mantener una estructura sencilla.

Ejemplo:

```text
siges_01/
│
├── manage.py
├── deploy_siges.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── siges/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── services/
│   │   └── establecimientos.py
│   │
│   ├── migrations/
│   │
│   ├── templates/
│   │   └── siges/
│   │       ├── base.html
│   │       ├── inicio.html
│   │       ├── formulario_base.html
│   │       ├── seccion_01.html
│   │       └── seccion_02.html
│   │
│   └── static/
│       └── siges/
│           ├── css/
│           │   ├── base.css
│           │   ├── formulario.css
│           │   └── efectos.css
│           │
│           ├── js/
│           │   ├── formulario.js
│           │   ├── establecimientos.js
│           │   └── matrix.js
│           │
│           └── img/
│               └── ...
│
├── docs/
│   ├── README.md
│   ├── 01_arquitectura/
│   ├── 02_base_datos/
│   ├── 03_interfaz/
│   ├── 04_formulario/
│   ├── 05_ejecucion/
│   ├── 06_modulos/
│   └── 07_arquitecturas/
│
└── sql/
    └── ...
```

La estructura podrá ajustarse ligeramente si existe una razón técnica clara.

No deberá convertirse en decenas de carpetas sin necesidad.

---

# 31. REGLA SOBRE

La carpeta:

```text
services/
```

se utilizará únicamente cuando ayude realmente a separar consultas o lógica reutilizable.

Ejemplo:

```text
services/establecimientos.py
```

podrá contener la lógica específica para recuperar establecimientos.

No deberán crearse veinte servicios para operaciones trivíales.

---

# 32. RESPONSABILIDAD DE

 deberá contener:

* definición de modelos;
* relaciones;
* metadatos;
* restricciones estructurales.

No deberá contener:

* HTML;
* JavaScript;
* CSS;
* lógica de visualización.

---

# 33. RESPONSABILIDAD DE

 deberá contener:

* formularios Django;
* campos;
* widgets;
* validaciónes;
* métodos ;
* validaciónes entre campos.

Éste será uno de los principales archivos para controlar las reglas del formulario.

---

# 34. RESPONSABILIDAD DE

 deberá coordinar:

```text
petición
↓
formulario
↓
validación
↓
modelo
↓
respuesta
```

Las vistas deberán mantenerse sencillas.

Preferentemente se utilizarán:

> vistas basadas en funciones

cuando resulten más fáciles de comprender.

No deberán utilizarse Class Based Views complejas únicamente por sofisticación.

---

# 35. RESPONSABILIDAD DE

Las rutas deberán ser explícitas y descriptivas.

Ejemplo:

```text
/
formulario/seccion-01/
formulario/seccion-02/
api/establecimientos/buscar/
```

Las URLs no deberán esconderse en estructuras complejas.

---

# 36. TEMPLATES

Los archivos HTML deberán permanecer exclusivamente dentro de:

```text
templates/
```

El HTML deberá concentrarse en:

* estructura;
* campos;
* componentes visuales;
* bloques reutilizables.

No deberá contener grandes cantidades de CSS o JavaScript embebido.

---

# 37. CSS

Los estilos deberán almacenarse en:

```text
static/siges/css/
```

Regla visual obligatoria:

```css
body {
  font-family: 'Century Gothic', sans-serif;
}
```

La escala tipografica del aplicativo deberá mantenerse contenida y legible, evitando titulares, botones, menus o textos de tarjetas excesivamente grandes.

Está prohibido crear páginas con cientos de líneas de:

```html
<style>
...
</style>
```

dentro de los templates.

Puede existir estilo inline puntual únicamente cuando esté técnicamente justificado.

---

# 38. JAVASCRIPT

Todo comportamiento visual significativo deberá mantenerse en:

```text
static/siges/js/
```

Ejemplos:

```text
establecimientos.js
formulario.js
matrix.js
```

Está prohibido concentrar grandes scripts JavaScript dentro del HTML.

---

# 39. SEPARACIÓN OBLIGATORIA

Debe cumplirse:

```text
PYTHON      → lógica del sistema
HTML        → estructura de interfaz
CSS         → apariencia
JAVASCRIPT  → interacción del navegador
POSTGRESQL  → persistencia
MARKDOWN    → documentación
```

No deberán mezclarse indiscriminadamente.

---

# 40. IDENTIDAD VISUAL

El aplicativo SIGES deberá heredar visualmente la identidad del aplicativo:

```text
Analítica en Salud
```

Esta aplicación será una **referencia visual**, NO una referencia arquitectónica.

Esto significa:

```text
Se reutiliza:
✓ lenguaje visual
✓ encabezados
✓ estética
✓ distribución
✓ logos institucionales
✓ colores
✓ sensación tecnológica
✓ fondos
✓ efectos

NO se reutiliza:
✗ desorden estructural
✗ mezcla de HTML/CSS/JS/Python
✗ archivos gigantes
✗ código duplicado
✗ lógica acoplada
```

---

# 41. CARPETA DE IMÁGENES

Las imágenes institucionales deberán mantenerse en:

```text
static/siges/img/
```

Si el proyecto ya posee una carpeta institucional , deberá reutilizarse o copiarse ordenadamente dentro de la estructura estática definitiva.

Codex deberá revisar primero qué imágenes existen.

---

# 42. LOGOS

Los logos institucionales existentes deberán ser reutilizados.

Codex NO deberá:

* buscar nuevos logos en internet;
* reemplazar logos oficiales;
* inventar logotipos;
* utilizar imágenes externas arbitrarias.

---

# 43. TRANSPARENCIA DE LOGOS

Visualmente los logos deberán mostrarse sin cuadros blancos artificiales.

Cuando el archivo PNG original tenga transparencia deberá preservarse.

El diseño deberá utilizar CSS apropiado:

```css
background: transparent;
object-fit: contain;
```

No deberá intentar falsificar transparencia destruyendo la imagen.

---

# 44. HEADER

Los logos deberán adaptarse al encabezado manteniendo:

* proporción;
* nitidez;
* margen;
* alineación;
* tamaño institucional.

No deberán deformarse.

Ejemplo conceptual:

```text
┌───────────────────────────────────────────────────────────┐
│ MSP      SIGES                    Información hospitalaria │
└───────────────────────────────────────────────────────────┘
```

---

# 45. EFECTO VISUAL TIPO MATRIX

SIGES deberá conservar el efecto visual inspirado en los fondos tecnológicos del aplicativo Analítica en Salud.

Se utilizará una animación discreta formada por caracteres o números.

El efecto deberá:

* mantenerse detrás del contenido;
* utilizar baja opacidad;
* no dificultar la lectura;
* no bloquear clics;
* consumir pocos recursos;
* adaptarse al tamaño de pantalla.

El JavaScript deberá estar en:

```text
static/siges/js/matrix.js
```

Los estilos asociados deberán estar en:

```text
static/siges/css/efectos.css
```

Nunca dentro de la lógica Python.

---

# 46. EFECTOS VISUALES

Los efectos deberán ser elegantes y discretos.

NO se deberán incorporar:

* animaciones excesivas;
* transiciones innecesarias;
* efectos 3D pesados;
* librerías enormes para animaciones sencillas;
* fondos que reduzcan legibilidad;
* elementos distractores.

---

# 47. INTERFAZ DEL FORMULARIO

La interfaz deberá mostrar claramente:

```text
SIGES
Gestión de información hospitalaria
```

y el progreso actual.

Ejemplo:

```text
Datos generales      ●
Acceso                ○
...
```

Las secciones futuras podrán mostrarse deshabilitadas o incorporarse progresivamente.

---

# 48. BOTONES

Los botones deberán ser consistentes.

Ejemplo:

```text
[ ← Anterior ]        [ Guardar ]        [ Guardar y continuar → ]
```

No deberán existir acciones ambiguas.

---

# 49. ESTADO DEL REGISTRO

Cada registro deberá permitir conocer qué secciones fueron completadas.

No es necesario diseñar inicialmente un motor complejo de workflow.

Puede utilizarse una estructura sencilla que permita determinar el progreso.

Por ejemplo:

```text
ultima_seccion_completada
```

o una estrategia igualmente simple y justificada.

---

# 50. IDENTIFICACIÓN DEL REGISTRO

Los registros propios de SIGES deberán poseer una clave primaria técnica independiente.

Por ejemplo:

```text
id
```

El  identifica al establecimiento, pero no deberá asumirse automáticamente que constituye la clave primaria de todas las tablas transacciónales.

Esto es importante porque un establecimiento podrá potencialmente registrar información en diferentes periodos.

---

# 51. NORMALIZACIÓN

El diseño de PostgreSQL deberá procurar un modelo relacional consistente.

Las tablas deberán evitar duplicación innecesaria de catálogos.

Sin embargo, tampoco deberá aplicarse normalización excesiva que dificulte el uso del sistema.

Como referencia:

> procurar un diseño relacional razonablemente normalizado hasta 3FN cuando corresponda.

---

# 52. INTEGRIDAD REFERENCIAL

Cuando existan relaciones entre estructuras propias de SIGES deberán utilizarse:

* claves primarias;
* claves foráneas;
* restricciones;
* tipos de datos apropiados.

No deberá dependerse solamente de validaciónes JavaScript.

---

# 53. VALIDACIÓN EN DIFERENTES NIVELES

Las reglas deberán aplicarse donde corresponda:

```text
Navegador       → experiencia del usuario
Django Forms    → validación principal
Modelo          → consistencia
PostgreSQL      → integridad final
```

JavaScript no deberá convertirse en la única protección del dato.

---

# 54. BÚSQUEDA DE ESTABLECIMIENTOS

El buscador deberá consultar únicamente los registros necesarios.

Ejemplo conceptual:

```text
Usuario escribe:
"0001"

↓ AJAX / fetch

Django consulta PostgreSQL

↓ devuelve pocos resultados

JavaScript muestra coincidencias
```

No deberá cargar el catálogo entero en el navegador.

---

# 55. ENDPOINT DE BÚSQUEDA

Podrá existir una ruta sencilla como:

```text
/api/establecimientos/buscar/
```

Su única responsabilidad será recibir un término y devolver coincidencias.

No deberá convertirse el proyecto completo en una API REST.

No se necesita Django REST Framework para esta funcionalidad inicial.

Puede utilizarse:

```python
JsonResponse
```

de Django.

---

# 56. EJEMPLO CONCEPTUAL

Flujo:

```text
GET /api/establecimientos/buscar/?q=123
```

Django:

```text
recibe q
↓
consulta siges.vm_establecimientos_ingresados
↓
limita resultados
↓
retorna JSON
```

JavaScript:

```text
recibe JSON
↓
muestra opciones
↓
usuario selecciona
↓
autocompleta formulario
```

---

# 57. PROTECCIÓN CONTRA CONSULTAS INSEGURAS

No deberá construirse SQL concatenando directamente texto del usuario.

Evitar:

```python
sql = "SELECT ... WHERE nombre = '" + valor + "'"
```

Deberá utilizarse:

* Django ORM; o
* consultas parametrizadas.

---

# 58. CONSULTAS SQL DIRECTAS

Se permitirá SQL directo cuando una consulta específica sea más clara que el ORM.

En ese caso deberá:

* estar parametrizado;
* documentarse;
* mantenerse en un lugar identificable;
* evitar concatenaciones inseguras.

---

# 59. CONFIGURACIÓN CENTRALIZADA

La configuración general deberá permanecer en archivos previsibles.

Ejemplo:

```text
config/settings.py
```

No deberán existir diferentes credenciales o parámetros repetidos en numerosos archivos.

---

# 60. DEPENDENCIAS

 deberá contener únicamente dependencias necesarias.

No deberán añadirse paquetes por conveniencia si Python o Django ya resuelven la necesidad.

Ejemplo de dependencias razonables:

```text
Django
psycopg
django-unfold
python-dotenv
```

según lo que efectivamente utilice el proyecto.

---

# 61. NO ACTUALIZAR DEPENDENCIAS INDISCRIMINADAMENTE

Codex no deberá ejecutar:

```bash
pip install --upgrade ...
```

masivamente.

Tampoco deberá modificar versiónes de múltiples paquetes para resolver un problema puntual sin analizar consecuencias.

---

# 62. DJANGO UNFOLD

Unfold podrá utilizarse como capa visual complementaria.

Principalmente podrá apoyar:

* administración;
* componentes;
* estilos coherentes;
* futuras pantallas internas.

No deberá introducir dependencia innecesaria de Unfold en toda la lógica de negocio.

---

# 63. DJANGO ADMIN

Django Admin puede mantenerse disponible para tareas técnicas internas.

Pero el formulario principal SIGES será una interfaz web propia.

No deberá obligarse al usuario final a capturar toda la información desde .

---

# 64. DOCUMENTACIÓN OBLIGATORIA DENTRO DEL CÓDIGO

Todo archivo Python propio deberá incluir inicialmente:

```python
# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================
```

Posteriormente deberá incluir una descripción del propósito del archivo.

---

# 65. COMENTARIOS EN TERCERA PERSONA

Los comentarios deberán redactarse en tercera persona.

Correcto:

```python
# Se importa Path para gestionar las rutas del proyecto.
from pathlib import Path
```

Correcto:

```python
# Se valida que el formulario contenga información válida.
if form.is_valid():
```

Evitar:

```python
# Importamos Path.
```

Evitar:

```python
# Aquí validamos.
```

---

# 66. DOCUMENTACIÓN LÍNEA POR LÍNEA

El código deberá estar ampliamente documentado.

Cuando una instrucción represente una acción funcional deberá explicarse.

Ejemplo:

```python
# Se importa JsonResponse para devolver resultados estructurados al navegador.
from django.http import JsonResponse

# Se obtiene el término enviado desde el buscador de establecimientos.
termino = request.GET.get("q", "").strip()

# Se limita la consulta para evitar recuperar registros innecesarios.
resultados = resultados[:20]
```

No deberán escribirse comentarios inútiles como:

```python
# Se suma uno.
contador += 1
```

si el contexto ya es totalmente evidente.

La documentación deberá aportar entendimiento.

---

# 67. DOCSTRINGS

Funciones relevantes deberán incluir docstrings simples.

Ejemplo:

```python
def buscar_establecimientos(request):
    """
    Recupera establecimientos desde PostgreSQL a partir del
    unicódigo o del nombre ingresado por el usuario.
    """
```

No deberán crearse docstrings de varias páginas.

---

# 68. CARPETA

Deberá existir:

```text
docs/
```

La documentación se escribirá en Markdown.

---

# 69.

Deberá explicar:

* qué es SIGES;
* objetivo;
* tecnología;
* estructura;
* ejecución;
* puerto;
* base;
* esquema;
* estado actual del desarrollo.

---

# 70.

Deberá describir:

```text
Navegador
   ↓
Django
   ↓
Forms / Views
   ↓
Models / Services
   ↓
PostgreSQL
   ↓
productos_bm.SIGES
```

También deberá explicar por qué se utiliza esta estructura sencilla.

---

# 71.

Deberá documentar:

* base de datos;
* esquema;
* tablas utilizadas;
* tablas administradas por Django;
* estructuras externas;
* relaciones;
* fuente de establecimientos;
* tablas posiblemente obsoletas;
* restricciones.

---

# 72.

Deberá documentar:

* secciones;
* campos;
* validaciónes;
* navegación;
* reglas para avanzar;
* reglas para regresar;
* persistencia;
* comportamiento de Guardar;
* comportamiento de Guardar y continuar.

---

# 73.

Deberá documentar:

* identidad visual;
* logos;
* header;
* colores;
* CSS;
* animación Matrix;
* comportamiento responsive;
* componentes.

---

# 74.

Deberá explicar exactamente:

```bash
conda activate msp_01
cd 02_SOFT_SIGES/siges_01
python deploy_siges.py
```

Resultado esperado:

```text
http://127.0.0.1:8036
```

---

# 75.

Deberá explicar archivo por archivo.

Ejemplo:

```text
manage.py
Administra comandos de Django.

deploy_siges.py
Inicializa el servidor de desarrollo en el puerto 8036.

siges/models.py
Define las estructuras de datos utilizadas por el aplicativo.

siges/forms.py
Define formularios y validaciones.

siges/views.py
Coordina las peticiones del usuario.

SIGES/services/establecimientos.py
Centraliza la consulta al catálogo de establecimientos.

siges/static/siges/js/matrix.js
Gestiona la animación tecnológica de fondo.
```

---

# 76. DOCUMENTACIÓN SINCRONIZADA

Cada modificación estructural deberá actualizar también la documentación relacionada.

Por ejemplo:

Si cambia:

```text
models.py
```

deberá revisarse:

```text
docs/02_base_datos/base_datos.md
docs/01_arquitectura/estructura_proyecto.md
```

Si cambia:

```text
matrix.js
```

deberá revisarse:

```text
docs/03_interfaz/interfaz.md
docs/01_arquitectura/estructura_proyecto.md
```

---

# 77. NO DOCUMENTAR FUNCIONALIDADES INEXISTENTES

La documentación deberá reflejar únicamente lo implementado.

No deberá decir:

```text
El sistema dispone de autenticación...
```

si todavía no existe.

---

# 78. MANEJO DE ERRORES

Los errores deberán mostrarse de forma comprensible.

Ejemplo:

```text
No fue posible consultar los establecimientos.
Revise la conexión con la base de datos.
```

No deberá mostrarse al usuario final un traceback de Python como interfaz normal.

Durante desarrollo sí deberá mantenerse información suficiente en consola para diagnóstico.

---

# 79. LOGGING

Durante esta primera etapa se utilizará logging sencillo.

No deberá implementarse una infraestructura compleja.

Se deberá registrar al menos:

* errores de base;
* errores internos;
* errores durante consultas críticas.

Nunca deberán registrarse contraseñas.

---

# 80. RESPONSIVE

La aplicación deberá visualizarse correctamente en:

* escritorio;
* portátil;
* tablet.

El diseño principal se orientará a escritorio por tratarse de un aplicativo institucional de captura.

---

# 81. ACCESIBILIDAD BÁSICA

Los formularios deberán utilizar:

* labels visibles;
* mensajes de error;
* contraste suficiente;
* botones identificables;
* tamaños legibles.

---

# 82. PROCESO DE IMPLEMENTACIÓN OBLIGATORIO

Codex deberá trabajar en este orden.

## FASE 1 — Inspección

1. inspeccionar estructura del proyecto;
2. identificar archivos existentes;
3. identificar código reutilizable;
4. identificar dependencias;
5. revisar configuración Django;
6. revisar esquema PostgreSQL;
7. revisar tablas existentes;
8. comprobar .

## FASE 2 — Limpieza lógica

1. detectar archivos innecesarios;
2. NO borrarlos automáticamente si existe duda;
3. simplificar estructura;
4. eliminar únicamente código generado claramente descartable y exclusivamente cuando forme parte del proyecto local que se está reconstruyendo;
5. nunca borrar datos PostgreSQL sin autorización.

## FASE 3 — Configuración

1. configurar Django;
2. configurar PostgreSQL;
3. configurar esquema ;
4. configurar estáticos;
5. configurar templates;
6. configurar Unfold;
7. configurar puerto 8036.

## FASE 4 — Validación PostgreSQL

Antes de trabajar en la UI del establecimiento:

1. comprobar conexión;
2. recuperar registros;
3. identificar columnas reales;
4. documentar estructura;
5. comprobar búsqueda por unicódigo.

## FASE 5 — Sección 01

Implementar:

* formulario;
* buscador;
* autocompletado;
* validaciónes;
* persistencia;
* navegación.

## FASE 6 — Sección 02

Implementar:

* formulario;
* modelo;
* validaciónes;
* guardado;
* retorno a sección anterior;
* continuidad.

## FASE 7 — Diseño visual

Aplicar:

* identidad Analítica en Salud;
* logos;
* header;
* estilos;
* fondo tecnológico;
* efecto Matrix.

## FASE 8 — Documentación

Verificar:

* comentarios;
* docstrings;
* docs;
* arquitectura;
* ejecución;
* BD;
* archivos.

## FASE 9 — Prueba integral

Probar:

```text
python deploy_siges.py
```

y comprobar:

```text
http://127.0.0.1:8036
```

---

# 83. PRUEBA MÍNIMA OBLIGATORIA DE BASE

Antes de considerar terminada la Sección 01 deberá comprobarse:

```text
1. Django conecta a productos_bm.
2. PostgreSQL utiliza SIGES.
3. vm_establecimientos_ingresados es accesible.
4. Existen registros.
5. El buscador devuelve unicódigos reales.
6. Seleccionar un resultado completa información.
```

Si falla el punto 1, NO deberá continuar modificando JavaScript para intentar resolverlo.

Debe solucionarse la capa donde realmente existe el problema.

---

# 84. PRUEBA DEL FLUJO

Deberá ejecutarse:

```text
Abrir SIGES
↓
Sección 01
↓
Buscar unicódigo
↓
Seleccionarlo
↓
Completar datos restantes
↓
Guardar
↓
Continuar
↓
Sección 02
↓
Completar
↓
Guardar
↓
Volver
↓
Modificar Sección 01
↓
Guardar
↓
Volver a Sección 02
↓
Confirmar persistencia
```

---

# 85. NO SOLUCIONAR ERRORES MEDIANTE REESCRITURAS MASIVAS

Cuando ocurra un error, Codex deberá identificar:

```text
archivo
↓
línea
↓
causa
↓
corrección mínima
```

No deberá responder a un error sencillo reconstruyendo media aplicación.

---

# 86. REGLA DE CAMBIOS MÍNIMOS

Antes de modificar un archivo se deberá responder internamente:

> ¿Puede corregirse el problema modificando únicamente este componente?

Si la respuesta es sí, no deberán modificarse otros archivos sin necesidad.

---

# 87. ARCHIVOS EXISTENTES

No deberá sobrescribirse un archivo completo simplemente porque Codex prefiera otra implementación.

Primero deberá comprender su función.

---

# 88. PROHIBIDO DUPLICAR FUNCIONALIDAD

No deberán coexistir archivos como:

```text
views.py
views_new.py
views_final.py
views_final2.py
views_ok.py
```

Lo mismo aplica para:

```text
models
forms
CSS
JavaScript
templates
```

La implementación definitiva deberá ocupar una ubicación clara.

---

# 89. NOMBRES DE ARCHIVOS

Los nombres deberán ser descriptivos.

Correctos:

```text
establecimientos.py
formulario.js
matrix.js
seccion_01.html
base_datos.md
```

Evitar:

```text
utils2.py
nuevo.py
final.py
prueba_ok.py
codigo1.py
```

---

# 90. NOMBRES DE VARIABLES

Se utilizarán nombres claros.

Ejemplo:

```python
unicodigo
establecimiento
registro_SIGES
seccion_actual
resultados
```

Evitar:

```python
x
xx
tmp2
dato_a
obj1
```

salvo usos matemáticos muy locales.

---

# 91. IDIOMA DEL CÓDIGO

El proyecto podrá utilizar identificadores en español cuando represente claramente el dominio.

Se deberá mantener consistencia.

No mezclar arbitrariamente:

```text
guardar_registro
save_form
datosUsuario
registro_data
```

---

# 92. JAVASCRIPT SIMPLE

Se utilizará JavaScript nativo cuando sea suficiente.

Ejemplo:

```javascript
fetch(...)
```

No deberá incorporarse React, Vue o Angular para resolver el autocompletado del establecimiento.

---

# 93. CSS SIMPLE Y MANTENIBLE

Se utilizarán clases reutilizables.

Ejemplo:

```text
.SIGES-header
.SIGES-card
.SIGES-form
.SIGES-button
.SIGES-progress
```

Evitar selectores excesivamente específicos.

---

# 94. SIN CSS MEZCLADO CON PYTHON

Python nunca deberá generar bloques CSS completos.

---

# 95. SIN HTML MEZCLADO EN PYTHON

Las views no deberán devolver grandes cadenas HTML.

Incorrecto:

```python
return HttpResponse("<html> ... </html>")
```

para las interfaces principales.

Se utilizará:

```python
render(...)
```

---

# 96. SIN JAVASCRIPT GENERADO DESDE PYTHON

La lógica JavaScript deberá estar en archivos estáticos siempre que sea razonable.

---

# 97. CONFIGURACIÓN DE PRODUCCIÓN

Por ahora el objetivo es una etapa de desarrollo/control.

No deberá complicarse la aplicación con infraestructura de producción antes de qué el formulario funcione.

Posteriormente podrán incorporarse:

* Docker;
* Gunicorn;
* Nginx;
* autenticación;
* HTTPS;
* alta concurrencia;
* balanceo;
* monitoreo.

Pero NO forman parte de esta primera reconstrucción salvo archivos existentes que sea necesario conservar.

---

# 98. DOCKER

Si existe Dockerfile prevíamente requerido, podrá mantenerse preparado.

Pero:

> el desarrollo local deberá poder funcionar sin obligar al usuario a levantar Docker.

El comando principal para esta etapa será:

```bash
python deploy_siges.py
```

---

# 99. COMPORTAMIENTO DE CODEX ANTE INCERTIDUMBRE

Si Codex encuentra una estructura cuyo propósito no puede determinar con certeza:

NO deberá eliminarla.

Deberá:

1. conservarla;
2. documentarla;
3. continuar trabajando sobre los componentes necesarios.

---

# 100. COMPORTAMIENTO ANTE CONFLICTOS DE BASE

Si encuentra:

* duplicados;
* primary keys inválidas;
* columnas inconsistentes;
* tablas incompletas;
* restricciones incompatibles;

no deberá intentar corregirlas destructivamente.

Deberá identificar exactamente:

```text
tabla
columna
restricción
problema
impacto
```

y aplicar únicamente una corrección segura si pertenece al nuevo modelo SIGES.

---

# 101.

Debe tratarse inicialmente como una fuente existente.

No deberá ejecutar sobre ella:

```sql
ALTER TABLE
DROP TABLE
TRUNCATE
DELETE
```

para hacer funcionar el formulario.

Si presenta problemas estructurales deberán documentarse primero.

---

# 102. NO CREAR PRIMARY KEYS ARBITRARIAS

No deberá asumir que ,  u otra columna es única sin verificarlo.

Antes de definir:

```text
PRIMARY KEY
UNIQUE
```

deberá comprobar duplicados.

---

# 103. DIAGNÓSTICO DE DUPLICADOS

Cuando sea necesario deberá utilizar consultas equivalentes a:

```sql
SELECT columna, COUNT(*)
FROM SIGES.tabla
GROUP BY columna
HAVING COUNT(*) > 1;
```

antes de establecer unicidad.

---

# 104. RESULTADO ESPERADO DE LA PRIMERA ENTREGA

Al terminar esta etapa deberá existir:

```text
✓ Proyecto Django organizado
✓ Entorno msp_01 respetado
✓ Puerto 8036
✓ deploy_siges.py
✓ PostgreSQL conectado
✓ productos_bm utilizado
✓ esquema SIGES utilizado
✓ vm_establecimientos_ingresados funcionando
✓ buscador de unicódigo funcionando
✓ autocompletado funcionando
✓ Sección 01 funcionando
✓ Sección 02 funcionando
✓ navegación secuencial
✓ validaciones
✓ persistencia
✓ volver/editar/guardar
✓ identidad institucional
✓ logos institucionales
✓ efecto tipo Matrix
✓ CSS separado
✓ JavaScript separado
✓ templates separados
✓ código Python organizado
✓ documentación Markdown
✓ comentarios en tercera persona
```

---

# 105. COSAS QUE NO DEBEN APARECER EN LA PRIMERA ENTREGA

```text
✗ sistema complejo de usuarios
✗ login institucional
✗ Keycloak
✗ OAuth
✗ microservicios
✗ Redis
✗ Celery
✗ Kubernetes
✗ React
✗ Vue
✗ Angular
✗ GraphQL
✗ arquitectura distribuida
✗ múltiples bases innecesarias
✗ nuevos entornos virtuales
✗ borrado automático de tablas
✗ reconstrucción completa de PostgreSQL
✗ código HTML dentro de Python
✗ CSS grande dentro de HTML
✗ JavaScript grande dentro de HTML
✗ listas de establecimientos hardcodeadas
```

---

# 106. CRITERIO PARA ACEPTAR UNA SOLUCIÓN

Ante dos alternativas técnicamente válidas:

```text
Alternativa A:
30 líneas claras.

Alternativa B:
6 clases + 4 interfaces + 3 factories + 8 archivos.
```

Se elegirá:

```text
Alternativa A.
```

Siempre que sea mantenible y correcta.

---

# 107. CRITERIO DE LEGIBILIDAD

Una persona deberá poder abrir:

```text
forms.py
```

y comprender las validaciónes.

Abrir:

```text
views.py
```

y comprender el flujo.

Abrir:

```text
establecimientos.py
```

y comprender cómo consulta PostgreSQL.

Abrir:

```text
formulario.js
```

y comprender la interacción.

Abrir:

```text
formulario.css
```

y comprender la presentación.

---

# 108. REGLA DE DEPURACIÓN

Cuando una característica no funcione deberá diagnosticarse por capas.

Ejemplo para el buscador:

```text
1. ¿PostgreSQL contiene datos?
2. ¿Django puede consultarlos?
3. ¿El endpoint devuelve JSON?
4. ¿JavaScript recibe JSON?
5. ¿La interfaz muestra resultados?
```

No deberá modificarse todo simultáneamente.

---

# 109. MENSAJES EN CONSOLA

Durante inicio,  deberá mostrar información sencilla.

Ejemplo:

```text
============================================================
SIGES
Sistema de Gestión de Información Hospitalaria
============================================================

Entorno Django: OK
Aplicación: SIGES
Puerto: 8036

Acceso local:
http://127.0.0.1:8036

Servidor:
http://0.0.0.0:8036

============================================================
```

No deberá mostrar contraseñas.

---

# 110. COMANDO PRINCIPAL

El objetivo de experiencia de desarrollo será siempre:

```bash
conda activate msp_01
python deploy_siges.py
```

Nada más para levantar la aplicación durante esta etapa.

---

# 111. IMPLEMENTACIÓN INCREMENTAL

Codex deberá completar una funcionalidad antes de iniciar otra.

Orden:

```text
Conexión PostgreSQL
↓
Consulta establecimiento
↓
Buscador
↓
Autocompletado
↓
Sección 01
↓
Persistencia
↓
Sección 02
↓
Navegación
↓
Diseño visual
↓
Documentación final
```

---

# 112. NO PRIORIZAR DISEÑO SOBRE FUNCIONALIDAD

Primero deberá comprobarse:

```text
los datos existen
↓
se consultan
↓
se validan
↓
se guardan
```

Después se perfeccionará la presentación.

No deberán utilizarse varias horas de trabajo corrigiendo animaciones mientras PostgreSQL todavía no responde.

---

# 113. PRESERVACIÓN DEL CONTROL DEL PROYECTO

El principio central será:

> Ing. Marcelo Chávez deberá poder comprender y modificar directamente la aplicación.

Por tanto, cualquier implementación que vuelva innecesariamente difícil modificar un campo, validación, consulta, template o estilo deberá simplificarse.

---

# 114. PROHIBICIÓN DE DECISIONES DE NEGOCIO INVENTADAS

Codex no deberá inventar:

* categorías;
* opciones;
* validaciónes clínicas;
* reglas hospitalarias;
* códigos;
* catálogos;
* obligatoriedad de campos.

Las reglas del dominio deberán provenir de las definiciones suministradas para SIGES.

---

# 115. NO MODIFICAR DATOS FUENTE

Los catálogos institucionales utilizados como referencia deberán considerarse de lectura salvo indicación expresa.

El aplicativo registrará su propia información sin alterar innecesariamente las fuentes maestras.

---

# 116. NOMENCLATURA DE SECCIONES

Cuando las secciones posean códigos institucionales deberán conservarse.

Ejemplo conceptual:

```text
s01
s02
s03
```

Las tablas, modelos y variables podrán reflejar dicha nomenclatura cuando ayude a conservar trazabilidad.

---

# 117. FUTURAS SECCIONES

La incorporación de una nueva sección deberá requerir principalmente:

```text
modelo, si corresponde
formulario
vista
template
URL
documentación
```

No deberá obligar a reconstruir las secciones anteriores.

---

# 118. CONTROL DE CAMBIOS DEL PROYECTO

Git podrá utilizarse normalmente.

Sin embargo, no deberá convertirse el versionamiento en el foco del desarrollo.

Se recomiendan commits funcionales claros como:

```text
Configura conexión PostgreSQL para SIGES
Implementa búsqueda de establecimientos
Implementa sección 01 del formulario
Implementa sección 02 del formulario
Aplica identidad visual institucional
Documenta arquitectura SIGES
```

---

# 119.

Deberá excluir al menos:

```text
.env
__pycache__/
*.pyc
.vscode/
.idea/
.DS_Store
logs/
```

y otros artefactos locales que correspondan.

Nunca deberán versionarse credenciales.

---

# 120. REGLA FINAL DE IMPLEMENTACIÓN

Antes de dar por terminada cualquier tarea Codex deberá comprobar:

```text
¿Funciona?
¿Es simple?
¿Está ordenado?
¿Está separado por responsabilidad?
¿Está documentado?
¿Puede Marcelo entenderlo?
¿Se respetó PostgreSQL existente?
¿Se evitó sobreingeniería?
```

Si una respuesta es NO, la tarea todavía no deberá considerarse terminada.

---

# 121. PRIORIDAD MÁXIMA

Las prioridades del proyecto, en orden, son:

```text
1. Integridad de los datos
2. Funcionamiento
3. Claridad
4. Mantenibilidad
5. Separación de responsabilidades
6. Documentación
7. Experiencia de usuario
8. Apariencia visual
9. Sofisticación técnica
```

La sofisticación técnica será siempre la última prioridad.

---

# 122. INSTRUCCIÓN INICIAL PARA CODEX

Al recibir este , Codex deberá comenzar realizando únicamente un diagnóstico del proyecto actual.

Deberá identificar:

```text
estructura actual
settings actuales
apps Django
modelos
formularios
vistas
templates
CSS
JavaScript
imágenes
dependencias
conexión PostgreSQL
tablas del esquema SIGES
estado de vm_establecimientos_ingresados
```

Después deberá reconstruir progresivamente la aplicación respetando estas reglas.

NO deberá comenzar inmediatamente creando usuarios, migraciones, tablas nuevas o entornos virtuales.

---

# 123. CONDICIÓN DE ÉXITO DE ESTA ETAPA

Esta fase se considerará satisfactoria cuando se pueda ejecutar:

```bash
conda activate msp_01
python deploy_siges.py
```

abrir:

```text
http://127.0.0.1:8036
```

y realizar correctamente el siguiente recorrido:

```text
Abrir SIGES
↓
Visualizar identidad institucional
↓
Ingresar a Sección 01
↓
Buscar un unicódigo REAL
↓
Obtener establecimientos desde productos_bm.SIGES
↓
Seleccionar establecimiento
↓
Autocompletar datos institucionales
↓
Completar información requerida
↓
Guardar
↓
Continuar a Sección 02
↓
Completar información
↓
Guardar
↓
Regresar a Sección 01
↓
Modificar
↓
Guardar nuevamente
↓
Continuar
↓
Comprobar que ningún dato se perdió
```

Todo esto deberá funcionar con una estructura comprensible, limpia y documentada.

---

# 124. PRINCIPIO MAESTRO DEL PROYECTO

> **SIGES debe verse como un aplicativo institucional profesional, pero su código debe seguir siendo sencillo, explícito, ordenado y controlable.**

> **La apariencia puede ser sofisticada. La arquitectura no debe ser innecesariamente sofisticada.**

> **Todo componente debe existir porque cumple una función concreta y comprensible.**

> **No se elimina, recrea o modifica información institucional sin una razón comprobada.**

> **Codex implementa exactamente lo solicitado y evita ampliar el alcance por iniciativa propia.**

---

# FIN DEL AGENTS.

# AGENTS.md

# SIGES — Sistema Web para Gestión de Información Hospitalaria

```text
============================================================
Autor: Ing. Marcelo Chávez
Consultor Especialista en Protección Social Banco Mundial
Email: marcelo_chavez_ec@outlook.com
============================================================
```

---

# 1. PROPÓSITO DEL AGENTE

Este archivo define las reglas obligatorias que deberá seguir Codex durante el desarrollo del aplicativo web **SIGES**.

SIGES será un sistema web desarrollado con **Python + Django**, destinado al registro progresivo y validado de información relacionada con la gestión hospitalaria.

El objetivo de este proyecto NO es construir una arquitectura sofisticada ni aplicar patrones innecesariamente complejos.

El objetivo es desarrollar una aplicación:

* ordenada;
* estable;
* mantenible;
* modular;
* comprensible;
* documentada;
* visualmente profesional;
* fácil de modificar;
* compatible con los conocimientos de Python de un ingeniero estadístico;
* preparada para crecer progresivamente.

Debe priorizarse permanentemente:

> **Simplicidad + claridad + separación de responsabilidades + documentación.**

Nunca deberá priorizarse sofisticación técnica sobre mantenibilidad.

---

# 2. PRINCIPIO GENERAL DE DESARROLLO

Codex deberá comportarse como un desarrollador cuidadoso que trabaja sobre un sistema institucional.

NO deberá comportarse como un generador autónomo que modifica indiscriminadamente el proyecto.

Antes de crear, borrar, reemplazar, migrar o reorganizar cualquier componente deberá analizar:

1. qué existe;
2. qué se utiliza;
3. qué puede reutilizarse;
4. qué falta;
5. qué podría estar obsoleto;
6. qué modificación es realmente necesaria.

Se utilizará siempre la solución técnicamente correcta **más sencilla posible**.

---

# 3. REGLA FUNDAMENTAL: EVITAR SOBREINGENIERÍA

Está expresamente prohibido introducir arquitectura innecesariamente compleja.

NO deberán incorporarse, salvo requerimiento explícito posterior:

* microservicios;
* arquitectura hexagonal;
* Clean Architecture compleja;
* CQRS;
* event sourcing;
* RabbitMQ;
* Kafka;
* Celery;
* Redis;
* Kubernetes;
* GraphQL;
* APIs separadas sin necesidad;
* repositorios abstractos;
* servicios genéricos excesivos;
* factories innecesarias;
* múltiples capas de abstracción;
* patrones avanzados que dificulten entender el flujo;
* autenticación externa;
* Keycloak;
* OAuth;
* JWT;
* Docker Swarm;
* orquestadores complejos.

Si una funcionalidad puede resolverse de forma clara con Django estándar, deberá utilizarse Django estándar.

---

# 4. NIVEL DE COMPLEJIDAD DEL CÓDIGO

La programación deberá escribirse pensando en que posteriormente será mantenida directamente por un profesional con conocimientos de:

* estadística;
* Python;
* SQL;
* PostgreSQL;
* análisis de datos;
* desarrollo web básico/intermedio.

El código podrá ser extenso si eso mejora su claridad.

Se deberá preferir:

```python
if condicion:
    accion()
```

sobre estructuras innecesariamente abstractas.

La prioridad será:

> que el código pueda abrirse, leerse y entenderse rápidamente.

---

# 5. UBICACIÓN DEL PROYECTO

El aplicativo deberá desarrollarse dentro del proyecto SIGES existente.

La raíz de trabajo corresponde conceptualmente a:

```text
02_SOFT_SIGES/
└── siges_01/
```

Codex deberá trabajar únicamente dentro del proyecto asignado.

No deberá crear proyectos Django paralelos sin autorización.

No deberá crear carpetas arbitrarias fuera de la estructura acordada.

---

# 6. ENTORNO PYTHON

Existe un entorno Python prevíamente definido.

Se utilizará:

```text
msp_01
```

Codex NO deberá:

* crear un nuevo ;
* crear otro entorno Conda;
* ejecutar ;
* crear ;
* sustituir el entorno existente;
* modificar el entorno global sin necesidad.

El aplicativo deberá asumir que prevíamente se activa:

```bash
conda activate msp_01
```

Posteriormente deberá poder iniciarse utilizando un único comando Python.

---

# 7. ARCHIVO ÚNICO DE ARRANQUE

Deberá existir en la raíz del proyecto un archivo:

```text
deploy_siges.py
```

Su propósito será exclusivamente simplificar el inicio de la aplicación.

El usuario deberá poder ejecutar:

```bash
python deploy_siges.py
```

y obtener el aplicativo disponible en:

```text
http://127.0.0.1:8036
```

Para acceso desde otras máquinas de una red autorizada podrá utilizarse:

```text
http://IP_DEL_SERVIDOR:8036
```

El servidor de desarrollo deberá levantarse conceptualmente como:

```bash
python manage.py runserver 0.0.0.0:8036
```

El archivo  podrá realizar comprobaciones sencillas como:

* verificar que  exista;
* verificar que Django pueda inicializarse;
* mostrar el puerto de ejecución;
* ejecutar el servidor.

NO deberá:

* crear bases;
* crear usuarios;
* ejecutar borrados;
* eliminar tablas;
* modificar datos;
* reconstruir automáticamente el esquema;
* crear entornos Python;
* instalar paquetes automáticamente;
* ejecutar migraciones destructivas.

---

# 8. PUERTO DEL APLICATIVO

Durante esta etapa el puerto oficial de pruebas será:

```text
8036
```

Por tanto:

```text
HOST = 0.0.0.0
PORT = 8036
```

No deberá modificarse este puerto arbitrariamente.

---

# 9. FRAMEWORK

Se utilizará:

```text
Python
Django
PostgreSQL
Django Unfold
HTML
CSS
JavaScript
```

Unfold podrá utilizarse para apoyar componentes administrativos y coherencia visual cuando corresponda.

Sin embargo, SIGES NO deberá convertirse simplemente en una personalización del Django Admin.

Las pantallas principales deberán ser interfaces propias del aplicativo.

---

# 10. ALCANCE DE LA PRIMERA ETAPA

La primera implementación funcional deberá concentrarse exclusivamente en:

```text
SECCIÓN 01 — Datos generales
SECCIÓN 02 — Segunda sección del formulario SIGES
```

No deberán construirse anticipadamente todas las secciones futuras.

La arquitectura deberá permitir agregarlas posteriormente sin rehacer el sistema.

---

# 11. FLUJO GENERAL DEL FORMULARIO

SIGES funcionará como un formulario secuencial.

Ejemplo:

```text
Inicio
   ↓
Sección 01
   ↓
Validación
   ↓
Guardar
   ↓
Sección 02
   ↓
Validación
   ↓
Guardar
   ↓
Siguiente sección futura
```

Una sección NO podrá considerarse terminada mientras existan campos obligatorios inválidos o incompletos.

---

# 12. REGLA DE NAVEGACIÓN ENTRE SECCIONES

El sistema deberá permitir:

```text
Anterior
Guardar
Guardar y continuar
```

El usuario podrá regresar a una sección anterior.

Ejemplo:

```text
Sección 01
   ↓
Sección 02
   ↓
Volver a Sección 01
   ↓
Modificar
   ↓
Guardar
   ↓
Continuar nuevamente
```

Los datos prevíamente registrados deberán recuperarse.

No deberán desaparecer al navegar entre secciones.

---

# 13. VALIDACIÓN OBLIGATORIA

Cada sección deberá tener validaciónes independientes.

Las validaciónes deberán implementarse principalmente utilizando:

```text
forms.py
```

No deberán concentrarse todas las validaciónes dentro de:

```text
views.py
```

Cuando una sección contenga errores:

* deberá permanecer en esa sección;
* deberá mostrar claramente qué campos tienen problemas;
* deberá conservar los datos válidos ya ingresados;
* no deberá avanzar a la siguiente sección.

---

# 14. NO PERMITIR SECCIONES VACÍAS

Las secciones obligatorias no podrán omitirse.

El sistema no deberá permitir avanzar simplemente pulsando:

```text
Siguiente
```

si existen campos obligatorios sin completar.

---

# 15. SECCIÓN 01 — DATOS GENERALES

La primera sección utilizará información institucional existente en PostgreSQL.

La variable principal de identificación será:

```text
unicodigo
```

El usuario deberá poder:

1. escribir parcialmente un unicódigo;
2. visualizar coincidencias;
3. selecciónar un establecimiento;
4. recuperar automáticamente sus datos.

---

# 16. BUSCADOR DE UNICÓDIGO

NO deberá utilizarse un  HTML cargando miles de registros de golpe.

Deberá existir un buscador/autocompletado.

Ejemplo visual:

```text
┌─────────────────────────────────────────┐
│ Buscar establecimiento                  │
│ 000123...                               │
└─────────────────────────────────────────┘

Resultados:

000123 — Hospital ...
000124 — Centro de Salud ...
000125 — Hospital ...
```

El usuario podrá buscar utilizando:

* unicódigo;
* nombre del establecimiento;

si ambos campos existen en la fuente.

---

# 17. AUTOCOMPLETADO DE DATOS

Después de selecciónar el unicódigo correcto, los campos institucionales deberán completarse automáticamente.

Conceptualmente:

```text
UNICÓDIGO
    ↓
PostgreSQL
    ↓
siges.vm_establecimientos_ingresados
    ↓
establecimiento seleccionado
    ↓
Datos generales
```

Los datos institucionales recuperados desde el catálogo maestro no deberán obligar al usuario a volver a escribir información que ya existe.

---

# 18. TABLA MAESTRA DE ESTABLECIMIENTOS

La fuente principal para esta etapa será:

```text
siges.vm_establecimientos_ingresados
```

Esta estructura se considera:

> FUENTE DE CONSULTA / CATÁLOGO MAESTRO PARA LA SECCIÓN 01.

Codex deberá comprobar primero que realmente puede obtener registros desde esta tabla o vista.

Antes de diseñar el buscador deberá ejecutar una prueba equivalente a:

```sql
SELECT *
FROM siges.vm_establecimientos_ingresados
LIMIT 10;
```

También deberá confirmar la existencia y contenido del campo correspondiente al:

```text
unicodigo
```

No deberá asumir nombres de columnas sin inspeccionarlos.

---

# 19. PROHIBIDO SIMULAR UNICÓDIGOS

Está prohibido:

* colocar unicódigos en listas Python;
* inventar establecimientos;
* crear datos de prueba como sustituto de PostgreSQL;
* insertar catálogos manualmente;
* hardcodear establecimientos en JavaScript;
* duplicar el catálogo dentro del aplicativo.

La consulta deberá provenir realmente de PostgreSQL.

---

# 20. BASE DE DATOS

La aplicación trabajará con la base institucional:

```text
productos_bm
```

El esquema funcional correspondiente al aplicativo será:

```text
SIGES
```

Todas las estructuras nuevas propias de SIGES deberán permanecer dentro de:

```text
productos_bm.SIGES
```

No deberán crearse tablas de negocio en:

```text
public
```

ni en esquemas diferentes sin autorización.

---

# 21. CREDENCIALES DE BASE DE DATOS

Está prohibido escribir directamente en el código:

```python
password = "..."
```

Las credenciales deberán manejarse mediante configuración externa.

Puede utilizarse:

```text
.env
```

o el mecanismo ya utilizado institucionalmente por el proyecto.

Las variables podrán representar:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_SCHEMA
```

Por ejemplo:

```text
DB_NAME=productos_bm
DB_SCHEMA=SIGES
```

Los valores reales de credenciales no deberán almacenarse en Git.

---

# 22. SEARCH_PATH DE POSTGRESQL

Django deberá quedar correctamente configurado para trabajar prioritariamente con:

```text
SIGES
```

Cuando corresponda podrá configurarse PostgreSQL mediante:

```text
search_path=SIGES,public
```

El objetivo es evitar que Django cree accidentalmente estructuras funcionales de SIGES dentro de .

---

# 23. MODELOS SOBRE TABLAS EXISTENTES

Cuando una tabla o vista ya exista y Django únicamente necesite consultarla, deberá analizarse el uso de:

```python
class Meta:
    managed = False
```

Ejemplo conceptual:

```python
class Establecimiento(models.Model):
    ...

    class Meta:
        managed = False
        db_table = 'vm_establecimientos_ingresados'
```

Esto evitará que Django intente recrear estructuras maestras que ya existen.

---

# 24. MODELO ENTIDAD–RELACIÓN

Todo el modelo entidad–relación correspondiente a SIGES deberá pertenecer al esquema:

```text
SIGES
```

El diseño deberá ser coherente.

No deberán existir tablas SIGES dispersas en diferentes esquemas.

---

# 25. TABLAS EXISTENTES

Antes de generar modelos nuevos, Codex deberá inspeccionar las tablas existentes.

Deberá clasificarlas conceptualmente como:

```text
A. Activa
B. Reutilizable
C. Posiblemente obsoleta
D. Desconocida
```

Este análisis deberá documentarse.

---

# 26. PROHIBICIÓN DE ELIMINAR TABLAS AUTOMÁTICAMENTE

Codex NO tiene autorización para ejecutar:

```sql
DROP TABLE
DROP SCHEMA
TRUNCATE
CASCADE
```

sobre estructuras existentes salvo instrucción explícita del usuario.

Aunque una tabla parezca obsoleta, deberá solamente documentarse.

Ejemplo:

```text
Tabla:
SIGES.tabla_antigua

Estado:
Posiblemente obsoleta.

Motivo:
No existe referencia desde los modelos actuales.

Acción:
NINGUNA.

Recomendación:
Revisar manualmente antes de eliminar.
```

---

# 27. LIMPIEZA DE ESTRUCTURAS ANTIGUAS

Si posteriormente se requiere limpiar tablas antiguas, deberá crearse un script SQL independiente.

Por ejemplo:

```text
sql/
└── revision_tablas_obsoletas.sql
```

Pero dicho script NO deberá ejecutarse automáticamente.

---

# 28. MIGRACIONES

Las migraciones Django deberán utilizarse únicamente para estructuras administradas realmente por Django.

No deberán generarse migraciones que intenten modificar tablas institucionales existentes sin necesidad.

Antes de:

```bash
python manage.py makemigrations
python manage.py migrate
```

Codex deberá conocer qué modelos son administrados por Django y cuáles no.

---

# 29. AUTENTICACIÓN

Durante esta etapa inicial:

> NO SE IMPLEMENTARÁ AUTENTICACIÓN FUNCIONAL DEL APLICATIVO.

No deberán crearse:

* páginas de login personalizadas;
* usuarios SIGES;
* roles MASTER;
* roles zonales;
* perfiles;
* permisos propios;
* recuperación de contraseñas;
* OAuth;
* Keycloak;
* JWT.

La autenticación será incorporada posteriormente cuando el formulario básico esté estabilizado.

---

# 30. ESTRUCTURA GENERAL RECOMENDADA

Se deberá mantener una estructura sencilla.

Ejemplo:

```text
siges_01/
│
├── manage.py
├── deploy_siges.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── siges/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── services/
│   │   └── establecimientos.py
│   │
│   ├── migrations/
│   │
│   ├── templates/
│   │   └── siges/
│   │       ├── base.html
│   │       ├── inicio.html
│   │       ├── formulario_base.html
│   │       ├── seccion_01.html
│   │       └── seccion_02.html
│   │
│   └── static/
│       └── siges/
│           ├── css/
│           │   ├── base.css
│           │   ├── formulario.css
│           │   └── efectos.css
│           │
│           ├── js/
│           │   ├── formulario.js
│           │   ├── establecimientos.js
│           │   └── matrix.js
│           │
│           └── img/
│               └── ...
│
├── docs/
│   ├── README.md
│   ├── 01_arquitectura/
│   ├── 02_base_datos/
│   ├── 03_interfaz/
│   ├── 04_formulario/
│   ├── 05_ejecucion/
│   ├── 06_modulos/
│   └── 07_arquitecturas/
│
└── sql/
    └── ...
```

La estructura podrá ajustarse ligeramente si existe una razón técnica clara.

No deberá convertirse en decenas de carpetas sin necesidad.

---

# 31. REGLA SOBRE

La carpeta:

```text
services/
```

se utilizará únicamente cuando ayude realmente a separar consultas o lógica reutilizable.

Ejemplo:

```text
services/establecimientos.py
```

podrá contener la lógica específica para recuperar establecimientos.

No deberán crearse veinte servicios para operaciones trivíales.

---

# 32. RESPONSABILIDAD DE

 deberá contener:

* definición de modelos;
* relaciones;
* metadatos;
* restricciones estructurales.

No deberá contener:

* HTML;
* JavaScript;
* CSS;
* lógica de visualización.

---

# 33. RESPONSABILIDAD DE

 deberá contener:

* formularios Django;
* campos;
* widgets;
* validaciónes;
* métodos ;
* validaciónes entre campos.

Éste será uno de los principales archivos para controlar las reglas del formulario.

---

# 34. RESPONSABILIDAD DE

 deberá coordinar:

```text
petición
↓
formulario
↓
validación
↓
modelo
↓
respuesta
```

Las vistas deberán mantenerse sencillas.

Preferentemente se utilizarán:

> vistas basadas en funciones

cuando resulten más fáciles de comprender.

No deberán utilizarse Class Based Views complejas únicamente por sofisticación.

---

# 35. RESPONSABILIDAD DE

Las rutas deberán ser explícitas y descriptivas.

Ejemplo:

```text
/
formulario/seccion-01/
formulario/seccion-02/
api/establecimientos/buscar/
```

Las URLs no deberán esconderse en estructuras complejas.

---

# 36. TEMPLATES

Los archivos HTML deberán permanecer exclusivamente dentro de:

```text
templates/
```

El HTML deberá concentrarse en:

* estructura;
* campos;
* componentes visuales;
* bloques reutilizables.

No deberá contener grandes cantidades de CSS o JavaScript embebido.

---

# 37. CSS

Los estilos deberán almacenarse en:

```text
static/siges/css/
```

Está prohibido crear páginas con cientos de líneas de:

```html
<style>
...
</style>
```

dentro de los templates.

Puede existir estilo inline puntual únicamente cuando esté técnicamente justificado.

---

# 38. JAVASCRIPT

Todo comportamiento visual significativo deberá mantenerse en:

```text
static/siges/js/
```

Ejemplos:

```text
establecimientos.js
formulario.js
matrix.js
```

Está prohibido concentrar grandes scripts JavaScript dentro del HTML.

---

# 39. SEPARACIÓN OBLIGATORIA

Debe cumplirse:

```text
PYTHON      → lógica del sistema
HTML        → estructura de interfaz
CSS         → apariencia
JAVASCRIPT  → interacción del navegador
POSTGRESQL  → persistencia
MARKDOWN    → documentación
```

No deberán mezclarse indiscriminadamente.

---

# 40. IDENTIDAD VISUAL

El aplicativo SIGES deberá heredar visualmente la identidad del aplicativo:

```text
Analítica en Salud
```

Esta aplicación será una **referencia visual**, NO una referencia arquitectónica.

Esto significa:

```text
Se reutiliza:
✓ lenguaje visual
✓ encabezados
✓ estética
✓ distribución
✓ logos institucionales
✓ colores
✓ sensación tecnológica
✓ fondos
✓ efectos

NO se reutiliza:
✗ desorden estructural
✗ mezcla de HTML/CSS/JS/Python
✗ archivos gigantes
✗ código duplicado
✗ lógica acoplada
```

---

# 41. CARPETA DE IMÁGENES

Las imágenes institucionales deberán mantenerse en:

```text
static/siges/img/
```

Si el proyecto ya posee una carpeta institucional , deberá reutilizarse o copiarse ordenadamente dentro de la estructura estática definitiva.

Codex deberá revisar primero qué imágenes existen.

---

# 42. LOGOS

Los logos institucionales existentes deberán ser reutilizados.

Codex NO deberá:

* buscar nuevos logos en internet;
* reemplazar logos oficiales;
* inventar logotipos;
* utilizar imágenes externas arbitrarias.

---

# 43. TRANSPARENCIA DE LOGOS

Visualmente los logos deberán mostrarse sin cuadros blancos artificiales.

Cuando el archivo PNG original tenga transparencia deberá preservarse.

El diseño deberá utilizar CSS apropiado:

```css
background: transparent;
object-fit: contain;
```

No deberá intentar falsificar transparencia destruyendo la imagen.

---

# 44. HEADER

Los logos deberán adaptarse al encabezado manteniendo:

* proporción;
* nitidez;
* margen;
* alineación;
* tamaño institucional.

No deberán deformarse.

Ejemplo conceptual:

```text
┌───────────────────────────────────────────────────────────┐
│ MSP      SIGES                    Información hospitalaria │
└───────────────────────────────────────────────────────────┘
```

---

# 45. EFECTO VISUAL TIPO MATRIX

SIGES deberá conservar el efecto visual inspirado en los fondos tecnológicos del aplicativo Analítica en Salud.

Se utilizará una animación discreta formada por caracteres o números.

El efecto deberá:

* mantenerse detrás del contenido;
* utilizar baja opacidad;
* no dificultar la lectura;
* no bloquear clics;
* consumir pocos recursos;
* adaptarse al tamaño de pantalla.

El JavaScript deberá estar en:

```text
static/siges/js/matrix.js
```

Los estilos asociados deberán estar en:

```text
static/siges/css/efectos.css
```

Nunca dentro de la lógica Python.

---

# 46. EFECTOS VISUALES

Los efectos deberán ser elegantes y discretos.

NO se deberán incorporar:

* animaciones excesivas;
* transiciones innecesarias;
* efectos 3D pesados;
* librerías enormes para animaciones sencillas;
* fondos que reduzcan legibilidad;
* elementos distractores.

---

# 47. INTERFAZ DEL FORMULARIO

La interfaz deberá mostrar claramente:

```text
SIGES
Gestión de información hospitalaria
```

y el progreso actual.

Ejemplo:

```text
Datos generales      ●
Acceso                ○
...
```

Las secciones futuras podrán mostrarse deshabilitadas o incorporarse progresivamente.

---

# 48. BOTONES

Los botones deberán ser consistentes.

Ejemplo:

```text
[ ← Anterior ]        [ Guardar ]        [ Guardar y continuar → ]
```

No deberán existir acciones ambiguas.

---

# 49. ESTADO DEL REGISTRO

Cada registro deberá permitir conocer qué secciones fueron completadas.

No es necesario diseñar inicialmente un motor complejo de workflow.

Puede utilizarse una estructura sencilla que permita determinar el progreso.

Por ejemplo:

```text
ultima_seccion_completada
```

o una estrategia igualmente simple y justificada.

---

# 50. IDENTIFICACIÓN DEL REGISTRO

Los registros propios de SIGES deberán poseer una clave primaria técnica independiente.

Por ejemplo:

```text
id
```

El  identifica al establecimiento, pero no deberá asumirse automáticamente que constituye la clave primaria de todas las tablas transacciónales.

Esto es importante porque un establecimiento podrá potencialmente registrar información en diferentes periodos.

---

# 51. NORMALIZACIÓN

El diseño de PostgreSQL deberá procurar un modelo relacional consistente.

Las tablas deberán evitar duplicación innecesaria de catálogos.

Sin embargo, tampoco deberá aplicarse normalización excesiva que dificulte el uso del sistema.

Como referencia:

> procurar un diseño relacional razonablemente normalizado hasta 3FN cuando corresponda.

---

# 52. INTEGRIDAD REFERENCIAL

Cuando existan relaciones entre estructuras propias de SIGES deberán utilizarse:

* claves primarias;
* claves foráneas;
* restricciones;
* tipos de datos apropiados.

No deberá dependerse solamente de validaciónes JavaScript.

---

# 53. VALIDACIÓN EN DIFERENTES NIVELES

Las reglas deberán aplicarse donde corresponda:

```text
Navegador       → experiencia del usuario
Django Forms    → validación principal
Modelo          → consistencia
PostgreSQL      → integridad final
```

JavaScript no deberá convertirse en la única protección del dato.

---

# 54. BÚSQUEDA DE ESTABLECIMIENTOS

El buscador deberá consultar únicamente los registros necesarios.

Ejemplo conceptual:

```text
Usuario escribe:
"0001"

↓ AJAX / fetch

Django consulta PostgreSQL

↓ devuelve pocos resultados

JavaScript muestra coincidencias
```

No deberá cargar el catálogo entero en el navegador.

---

# 55. ENDPOINT DE BÚSQUEDA

Podrá existir una ruta sencilla como:

```text
/api/establecimientos/buscar/
```

Su única responsabilidad será recibir un término y devolver coincidencias.

No deberá convertirse el proyecto completo en una API REST.

No se necesita Django REST Framework para esta funcionalidad inicial.

Puede utilizarse:

```python
JsonResponse
```

de Django.

---

# 56. EJEMPLO CONCEPTUAL

Flujo:

```text
GET /api/establecimientos/buscar/?q=123
```

Django:

```text
recibe q
↓
consulta siges.vm_establecimientos_ingresados
↓
limita resultados
↓
retorna JSON
```

JavaScript:

```text
recibe JSON
↓
muestra opciones
↓
usuario selecciona
↓
autocompleta formulario
```

---

# 57. PROTECCIÓN CONTRA CONSULTAS INSEGURAS

No deberá construirse SQL concatenando directamente texto del usuario.

Evitar:

```python
sql = "SELECT ... WHERE nombre = '" + valor + "'"
```

Deberá utilizarse:

* Django ORM; o
* consultas parametrizadas.

---

# 58. CONSULTAS SQL DIRECTAS

Se permitirá SQL directo cuando una consulta específica sea más clara que el ORM.

En ese caso deberá:

* estar parametrizado;
* documentarse;
* mantenerse en un lugar identificable;
* evitar concatenaciones inseguras.

---

# 59. CONFIGURACIÓN CENTRALIZADA

La configuración general deberá permanecer en archivos previsibles.

Ejemplo:

```text
config/settings.py
```

No deberán existir diferentes credenciales o parámetros repetidos en numerosos archivos.

---

# 60. DEPENDENCIAS

 deberá contener únicamente dependencias necesarias.

No deberán añadirse paquetes por conveniencia si Python o Django ya resuelven la necesidad.

Ejemplo de dependencias razonables:

```text
Django
psycopg
django-unfold
python-dotenv
```

según lo que efectivamente utilice el proyecto.

---

# 61. NO ACTUALIZAR DEPENDENCIAS INDISCRIMINADAMENTE

Codex no deberá ejecutar:

```bash
pip install --upgrade ...
```

masivamente.

Tampoco deberá modificar versiónes de múltiples paquetes para resolver un problema puntual sin analizar consecuencias.

---

# 62. DJANGO UNFOLD

Unfold podrá utilizarse como capa visual complementaria.

Principalmente podrá apoyar:

* administración;
* componentes;
* estilos coherentes;
* futuras pantallas internas.

No deberá introducir dependencia innecesaria de Unfold en toda la lógica de negocio.

---

# 63. DJANGO ADMIN

Django Admin puede mantenerse disponible para tareas técnicas internas.

Pero el formulario principal SIGES será una interfaz web propia.

No deberá obligarse al usuario final a capturar toda la información desde .

---

# 64. DOCUMENTACIÓN OBLIGATORIA DENTRO DEL CÓDIGO

Todo archivo Python propio deberá incluir inicialmente:

```python
# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================
```

Posteriormente deberá incluir una descripción del propósito del archivo.

---

# 65. COMENTARIOS EN TERCERA PERSONA

Los comentarios deberán redactarse en tercera persona.

Correcto:

```python
# Se importa Path para gestionar las rutas del proyecto.
from pathlib import Path
```

Correcto:

```python
# Se valida que el formulario contenga información válida.
if form.is_valid():
```

Evitar:

```python
# Importamos Path.
```

Evitar:

```python
# Aquí validamos.
```

---

# 66. DOCUMENTACIÓN LÍNEA POR LÍNEA

El código deberá estar ampliamente documentado.

Cuando una instrucción represente una acción funcional deberá explicarse.

Ejemplo:

```python
# Se importa JsonResponse para devolver resultados estructurados al navegador.
from django.http import JsonResponse

# Se obtiene el término enviado desde el buscador de establecimientos.
termino = request.GET.get("q", "").strip()

# Se limita la consulta para evitar recuperar registros innecesarios.
resultados = resultados[:20]
```

No deberán escribirse comentarios inútiles como:

```python
# Se suma uno.
contador += 1
```

si el contexto ya es totalmente evidente.

La documentación deberá aportar entendimiento.

---

# 67. DOCSTRINGS

Funciones relevantes deberán incluir docstrings simples.

Ejemplo:

```python
def buscar_establecimientos(request):
    """
    Recupera establecimientos desde PostgreSQL a partir del
    unicódigo o del nombre ingresado por el usuario.
    """
```

No deberán crearse docstrings de varias páginas.

---

# 68. CARPETA

Deberá existir:

```text
docs/
```

La documentación se escribirá en Markdown.

---

# 69.

Deberá explicar:

* qué es SIGES;
* objetivo;
* tecnología;
* estructura;
* ejecución;
* puerto;
* base;
* esquema;
* estado actual del desarrollo.

---

# 70.

Deberá describir:

```text
Navegador
   ↓
Django
   ↓
Forms / Views
   ↓
Models / Services
   ↓
PostgreSQL
   ↓
productos_bm.SIGES
```

También deberá explicar por qué se utiliza esta estructura sencilla.

---

# 71.

Deberá documentar:

* base de datos;
* esquema;
* tablas utilizadas;
* tablas administradas por Django;
* estructuras externas;
* relaciones;
* fuente de establecimientos;
* tablas posiblemente obsoletas;
* restricciones.

---

# 72.

Deberá documentar:

* secciones;
* campos;
* validaciónes;
* navegación;
* reglas para avanzar;
* reglas para regresar;
* persistencia;
* comportamiento de Guardar;
* comportamiento de Guardar y continuar.

---

# 73.

Deberá documentar:

* identidad visual;
* logos;
* header;
* colores;
* CSS;
* animación Matrix;
* comportamiento responsive;
* componentes.

---

# 74.

Deberá explicar exactamente:

```bash
conda activate msp_01
cd 02_SOFT_SIGES/siges_01
python deploy_siges.py
```

Resultado esperado:

```text
http://127.0.0.1:8036
```

---

# 75.

Deberá explicar archivo por archivo.

Ejemplo:

```text
manage.py
Administra comandos de Django.

deploy_siges.py
Inicializa el servidor de desarrollo en el puerto 8036.

siges/models.py
Define las estructuras de datos utilizadas por el aplicativo.

siges/forms.py
Define formularios y validaciones.

siges/views.py
Coordina las peticiones del usuario.

SIGES/services/establecimientos.py
Centraliza la consulta al catálogo de establecimientos.

siges/static/siges/js/matrix.js
Gestiona la animación tecnológica de fondo.
```

---

# 76. DOCUMENTACIÓN SINCRONIZADA

Cada modificación estructural deberá actualizar también la documentación relacionada.

Por ejemplo:

Si cambia:

```text
models.py
```

deberá revisarse:

```text
docs/02_base_datos/base_datos.md
docs/01_arquitectura/estructura_proyecto.md
```

Si cambia:

```text
matrix.js
```

deberá revisarse:

```text
docs/03_interfaz/interfaz.md
docs/01_arquitectura/estructura_proyecto.md
```

---

# 77. NO DOCUMENTAR FUNCIONALIDADES INEXISTENTES

La documentación deberá reflejar únicamente lo implementado.

No deberá decir:

```text
El sistema dispone de autenticación...
```

si todavía no existe.

---

# 78. MANEJO DE ERRORES

Los errores deberán mostrarse de forma comprensible.

Ejemplo:

```text
No fue posible consultar los establecimientos.
Revise la conexión con la base de datos.
```

No deberá mostrarse al usuario final un traceback de Python como interfaz normal.

Durante desarrollo sí deberá mantenerse información suficiente en consola para diagnóstico.

---

# 79. LOGGING

Durante esta primera etapa se utilizará logging sencillo.

No deberá implementarse una infraestructura compleja.

Se deberá registrar al menos:

* errores de base;
* errores internos;
* errores durante consultas críticas.

Nunca deberán registrarse contraseñas.

---

# 80. RESPONSIVE

La aplicación deberá visualizarse correctamente en:

* escritorio;
* portátil;
* tablet.

El diseño principal se orientará a escritorio por tratarse de un aplicativo institucional de captura.

---

# 81. ACCESIBILIDAD BÁSICA

Los formularios deberán utilizar:

* labels visibles;
* mensajes de error;
* contraste suficiente;
* botones identificables;
* tamaños legibles.

---

# 82. PROCESO DE IMPLEMENTACIÓN OBLIGATORIO

Codex deberá trabajar en este orden.

## FASE 1 — Inspección

1. inspeccionar estructura del proyecto;
2. identificar archivos existentes;
3. identificar código reutilizable;
4. identificar dependencias;
5. revisar configuración Django;
6. revisar esquema PostgreSQL;
7. revisar tablas existentes;
8. comprobar .

## FASE 2 — Limpieza lógica

1. detectar archivos innecesarios;
2. NO borrarlos automáticamente si existe duda;
3. simplificar estructura;
4. eliminar únicamente código generado claramente descartable y exclusivamente cuando forme parte del proyecto local que se está reconstruyendo;
5. nunca borrar datos PostgreSQL sin autorización.

## FASE 3 — Configuración

1. configurar Django;
2. configurar PostgreSQL;
3. configurar esquema ;
4. configurar estáticos;
5. configurar templates;
6. configurar Unfold;
7. configurar puerto 8036.

## FASE 4 — Validación PostgreSQL

Antes de trabajar en la UI del establecimiento:

1. comprobar conexión;
2. recuperar registros;
3. identificar columnas reales;
4. documentar estructura;
5. comprobar búsqueda por unicódigo.

## FASE 5 — Sección 01

Implementar:

* formulario;
* buscador;
* autocompletado;
* validaciónes;
* persistencia;
* navegación.

## FASE 6 — Sección 02

Implementar:

* formulario;
* modelo;
* validaciónes;
* guardado;
* retorno a sección anterior;
* continuidad.

## FASE 7 — Diseño visual

Aplicar:

* identidad Analítica en Salud;
* logos;
* header;
* estilos;
* fondo tecnológico;
* efecto Matrix.

## FASE 8 — Documentación

Verificar:

* comentarios;
* docstrings;
* docs;
* arquitectura;
* ejecución;
* BD;
* archivos.

## FASE 9 — Prueba integral

Probar:

```text
python deploy_siges.py
```

y comprobar:

```text
http://127.0.0.1:8036
```

---

# 83. PRUEBA MÍNIMA OBLIGATORIA DE BASE

Antes de considerar terminada la Sección 01 deberá comprobarse:

```text
1. Django conecta a productos_bm.
2. PostgreSQL utiliza SIGES.
3. vm_establecimientos_ingresados es accesible.
4. Existen registros.
5. El buscador devuelve unicódigos reales.
6. Seleccionar un resultado completa información.
```

Si falla el punto 1, NO deberá continuar modificando JavaScript para intentar resolverlo.

Debe solucionarse la capa donde realmente existe el problema.

---

# 84. PRUEBA DEL FLUJO

Deberá ejecutarse:

```text
Abrir SIGES
↓
Sección 01
↓
Buscar unicódigo
↓
Seleccionarlo
↓
Completar datos restantes
↓
Guardar
↓
Continuar
↓
Sección 02
↓
Completar
↓
Guardar
↓
Volver
↓
Modificar Sección 01
↓
Guardar
↓
Volver a Sección 02
↓
Confirmar persistencia
```

---

# 85. NO SOLUCIONAR ERRORES MEDIANTE REESCRITURAS MASIVAS

Cuando ocurra un error, Codex deberá identificar:

```text
archivo
↓
línea
↓
causa
↓
corrección mínima
```

No deberá responder a un error sencillo reconstruyendo media aplicación.

---

# 86. REGLA DE CAMBIOS MÍNIMOS

Antes de modificar un archivo se deberá responder internamente:

> ¿Puede corregirse el problema modificando únicamente este componente?

Si la respuesta es sí, no deberán modificarse otros archivos sin necesidad.

---

# 87. ARCHIVOS EXISTENTES

No deberá sobrescribirse un archivo completo simplemente porque Codex prefiera otra implementación.

Primero deberá comprender su función.

---

# 88. PROHIBIDO DUPLICAR FUNCIONALIDAD

No deberán coexistir archivos como:

```text
views.py
views_new.py
views_final.py
views_final2.py
views_ok.py
```

Lo mismo aplica para:

```text
models
forms
CSS
JavaScript
templates
```

La implementación definitiva deberá ocupar una ubicación clara.

---

# 89. NOMBRES DE ARCHIVOS

Los nombres deberán ser descriptivos.

Correctos:

```text
establecimientos.py
formulario.js
matrix.js
seccion_01.html
base_datos.md
```

Evitar:

```text
utils2.py
nuevo.py
final.py
prueba_ok.py
codigo1.py
```

---

# 90. NOMBRES DE VARIABLES

Se utilizarán nombres claros.

Ejemplo:

```python
unicodigo
establecimiento
registro_SIGES
seccion_actual
resultados
```

Evitar:

```python
x
xx
tmp2
dato_a
obj1
```

salvo usos matemáticos muy locales.

---

# 91. IDIOMA DEL CÓDIGO

El proyecto podrá utilizar identificadores en español cuando represente claramente el dominio.

Se deberá mantener consistencia.

No mezclar arbitrariamente:

```text
guardar_registro
save_form
datosUsuario
registro_data
```

---

# 92. JAVASCRIPT SIMPLE

Se utilizará JavaScript nativo cuando sea suficiente.

Ejemplo:

```javascript
fetch(...)
```

No deberá incorporarse React, Vue o Angular para resolver el autocompletado del establecimiento.

---

# 93. CSS SIMPLE Y MANTENIBLE

Se utilizarán clases reutilizables.

Ejemplo:

```text
.SIGES-header
.SIGES-card
.SIGES-form
.SIGES-button
.SIGES-progress
```

Evitar selectores excesivamente específicos.

---

# 94. SIN CSS MEZCLADO CON PYTHON

Python nunca deberá generar bloques CSS completos.

---

# 95. SIN HTML MEZCLADO EN PYTHON

Las views no deberán devolver grandes cadenas HTML.

Incorrecto:

```python
return HttpResponse("<html> ... </html>")
```

para las interfaces principales.

Se utilizará:

```python
render(...)
```

---

# 96. SIN JAVASCRIPT GENERADO DESDE PYTHON

La lógica JavaScript deberá estar en archivos estáticos siempre que sea razonable.

---

# 97. CONFIGURACIÓN DE PRODUCCIÓN

Por ahora el objetivo es una etapa de desarrollo/control.

No deberá complicarse la aplicación con infraestructura de producción antes de qué el formulario funcione.

Posteriormente podrán incorporarse:

* Docker;
* Gunicorn;
* Nginx;
* autenticación;
* HTTPS;
* alta concurrencia;
* balanceo;
* monitoreo.

Pero NO forman parte de esta primera reconstrucción salvo archivos existentes que sea necesario conservar.

---

# 98. DOCKER

Si existe Dockerfile prevíamente requerido, podrá mantenerse preparado.

Pero:

> el desarrollo local deberá poder funcionar sin obligar al usuario a levantar Docker.

El comando principal para esta etapa será:

```bash
python deploy_siges.py
```

---

# 99. COMPORTAMIENTO DE CODEX ANTE INCERTIDUMBRE

Si Codex encuentra una estructura cuyo propósito no puede determinar con certeza:

NO deberá eliminarla.

Deberá:

1. conservarla;
2. documentarla;
3. continuar trabajando sobre los componentes necesarios.

---

# 100. COMPORTAMIENTO ANTE CONFLICTOS DE BASE

Si encuentra:

* duplicados;
* primary keys inválidas;
* columnas inconsistentes;
* tablas incompletas;
* restricciones incompatibles;

no deberá intentar corregirlas destructivamente.

Deberá identificar exactamente:

```text
tabla
columna
restricción
problema
impacto
```

y aplicar únicamente una corrección segura si pertenece al nuevo modelo SIGES.

---

# 101.

Debe tratarse inicialmente como una fuente existente.

No deberá ejecutar sobre ella:

```sql
ALTER TABLE
DROP TABLE
TRUNCATE
DELETE
```

para hacer funcionar el formulario.

Si presenta problemas estructurales deberán documentarse primero.

---

# 102. NO CREAR PRIMARY KEYS ARBITRARIAS

No deberá asumir que ,  u otra columna es única sin verificarlo.

Antes de definir:

```text
PRIMARY KEY
UNIQUE
```

deberá comprobar duplicados.

---

# 103. DIAGNÓSTICO DE DUPLICADOS

Cuando sea necesario deberá utilizar consultas equivalentes a:

```sql
SELECT columna, COUNT(*)
FROM SIGES.tabla
GROUP BY columna
HAVING COUNT(*) > 1;
```

antes de establecer unicidad.

---

# 104. RESULTADO ESPERADO DE LA PRIMERA ENTREGA

Al terminar esta etapa deberá existir:

```text
✓ Proyecto Django organizado
✓ Entorno msp_01 respetado
✓ Puerto 8036
✓ deploy_siges.py
✓ PostgreSQL conectado
✓ productos_bm utilizado
✓ esquema SIGES utilizado
✓ vm_establecimientos_ingresados funcionando
✓ buscador de unicódigo funcionando
✓ autocompletado funcionando
✓ Sección 01 funcionando
✓ Sección 02 funcionando
✓ navegación secuencial
✓ validaciones
✓ persistencia
✓ volver/editar/guardar
✓ identidad institucional
✓ logos institucionales
✓ efecto tipo Matrix
✓ CSS separado
✓ JavaScript separado
✓ templates separados
✓ código Python organizado
✓ documentación Markdown
✓ comentarios en tercera persona
```

---

# 105. COSAS QUE NO DEBEN APARECER EN LA PRIMERA ENTREGA

```text
✗ sistema complejo de usuarios
✗ login institucional
✗ Keycloak
✗ OAuth
✗ microservicios
✗ Redis
✗ Celery
✗ Kubernetes
✗ React
✗ Vue
✗ Angular
✗ GraphQL
✗ arquitectura distribuida
✗ múltiples bases innecesarias
✗ nuevos entornos virtuales
✗ borrado automático de tablas
✗ reconstrucción completa de PostgreSQL
✗ código HTML dentro de Python
✗ CSS grande dentro de HTML
✗ JavaScript grande dentro de HTML
✗ listas de establecimientos hardcodeadas
```

---

# 106. CRITERIO PARA ACEPTAR UNA SOLUCIÓN

Ante dos alternativas técnicamente válidas:

```text
Alternativa A:
30 líneas claras.

Alternativa B:
6 clases + 4 interfaces + 3 factories + 8 archivos.
```

Se elegirá:

```text
Alternativa A.
```

Siempre que sea mantenible y correcta.

---

# 107. CRITERIO DE LEGIBILIDAD

Una persona deberá poder abrir:

```text
forms.py
```

y comprender las validaciónes.

Abrir:

```text
views.py
```

y comprender el flujo.

Abrir:

```text
establecimientos.py
```

y comprender cómo consulta PostgreSQL.

Abrir:

```text
formulario.js
```

y comprender la interacción.

Abrir:

```text
formulario.css
```

y comprender la presentación.

---

# 108. REGLA DE DEPURACIÓN

Cuando una característica no funcione deberá diagnosticarse por capas.

Ejemplo para el buscador:

```text
1. ¿PostgreSQL contiene datos?
2. ¿Django puede consultarlos?
3. ¿El endpoint devuelve JSON?
4. ¿JavaScript recibe JSON?
5. ¿La interfaz muestra resultados?
```

No deberá modificarse todo simultáneamente.

---

# 109. MENSAJES EN CONSOLA

Durante inicio,  deberá mostrar información sencilla.

Ejemplo:

```text
============================================================
SIGES
Sistema de Gestión de Información Hospitalaria
============================================================

Entorno Django: OK
Aplicación: SIGES
Puerto: 8036

Acceso local:
http://127.0.0.1:8036

Servidor:
http://0.0.0.0:8036

============================================================
```

No deberá mostrar contraseñas.

---

# 110. COMANDO PRINCIPAL

El objetivo de experiencia de desarrollo será siempre:

```bash
conda activate msp_01
python deploy_siges.py
```

Nada más para levantar la aplicación durante esta etapa.

---

# 111. IMPLEMENTACIÓN INCREMENTAL

Codex deberá completar una funcionalidad antes de iniciar otra.

Orden:

```text
Conexión PostgreSQL
↓
Consulta establecimiento
↓
Buscador
↓
Autocompletado
↓
Sección 01
↓
Persistencia
↓
Sección 02
↓
Navegación
↓
Diseño visual
↓
Documentación final
```

---

# 112. NO PRIORIZAR DISEÑO SOBRE FUNCIONALIDAD

Primero deberá comprobarse:

```text
los datos existen
↓
se consultan
↓
se validan
↓
se guardan
```

Después se perfeccionará la presentación.

No deberán utilizarse varias horas de trabajo corrigiendo animaciones mientras PostgreSQL todavía no responde.

---

# 113. PRESERVACIÓN DEL CONTROL DEL PROYECTO

El principio central será:

> Ing. Marcelo Chávez deberá poder comprender y modificar directamente la aplicación.

Por tanto, cualquier implementación que vuelva innecesariamente difícil modificar un campo, validación, consulta, template o estilo deberá simplificarse.

---

# 114. PROHIBICIÓN DE DECISIONES DE NEGOCIO INVENTADAS

Codex no deberá inventar:

* categorías;
* opciones;
* validaciónes clínicas;
* reglas hospitalarias;
* códigos;
* catálogos;
* obligatoriedad de campos.

Las reglas del dominio deberán provenir de las definiciones suministradas para SIGES.

---

# 115. NO MODIFICAR DATOS FUENTE

Los catálogos institucionales utilizados como referencia deberán considerarse de lectura salvo indicación expresa.

El aplicativo registrará su propia información sin alterar innecesariamente las fuentes maestras.

---

# 116. NOMENCLATURA DE SECCIONES

Cuando las secciones posean códigos institucionales deberán conservarse.

Ejemplo conceptual:

```text
s01
s02
s03
```

Las tablas, modelos y variables podrán reflejar dicha nomenclatura cuando ayude a conservar trazabilidad.

---

# 117. FUTURAS SECCIONES

La incorporación de una nueva sección deberá requerir principalmente:

```text
modelo, si corresponde
formulario
vista
template
URL
documentación
```

No deberá obligar a reconstruir las secciones anteriores.

---

# 118. CONTROL DE CAMBIOS DEL PROYECTO

Git podrá utilizarse normalmente.

Sin embargo, no deberá convertirse el versionamiento en el foco del desarrollo.

Se recomiendan commits funcionales claros como:

```text
Configura conexión PostgreSQL para SIGES
Implementa búsqueda de establecimientos
Implementa sección 01 del formulario
Implementa sección 02 del formulario
Aplica identidad visual institucional
Documenta arquitectura SIGES
```

---

# 119.

Deberá excluir al menos:

```text
.env
__pycache__/
*.pyc
.vscode/
.idea/
.DS_Store
logs/
```

y otros artefactos locales que correspondan.

Nunca deberán versionarse credenciales.

---

# 120. REGLA FINAL DE IMPLEMENTACIÓN

Antes de dar por terminada cualquier tarea Codex deberá comprobar:

```text
¿Funciona?
¿Es simple?
¿Está ordenado?
¿Está separado por responsabilidad?
¿Está documentado?
¿Puede Marcelo entenderlo?
¿Se respetó PostgreSQL existente?
¿Se evitó sobreingeniería?
```

Si una respuesta es NO, la tarea todavía no deberá considerarse terminada.

---

# 121. PRIORIDAD MÁXIMA

Las prioridades del proyecto, en orden, son:

```text
1. Integridad de los datos
2. Funcionamiento
3. Claridad
4. Mantenibilidad
5. Separación de responsabilidades
6. Documentación
7. Experiencia de usuario
8. Apariencia visual
9. Sofisticación técnica
```

La sofisticación técnica será siempre la última prioridad.

---

# 122. INSTRUCCIÓN INICIAL PARA CODEX

Al recibir este , Codex deberá comenzar realizando únicamente un diagnóstico del proyecto actual.

Deberá identificar:

```text
estructura actual
settings actuales
apps Django
modelos
formularios
vistas
templates
CSS
JavaScript
imágenes
dependencias
conexión PostgreSQL
tablas del esquema SIGES
estado de vm_establecimientos_ingresados
```

Después deberá reconstruir progresivamente la aplicación respetando estas reglas.

NO deberá comenzar inmediatamente creando usuarios, migraciones, tablas nuevas o entornos virtuales.

---

# 123. CONDICIÓN DE ÉXITO DE ESTA ETAPA

Esta fase se considerará satisfactoria cuando se pueda ejecutar:

```bash
conda activate msp_01
python deploy_siges.py
```

abrir:

```text
http://127.0.0.1:8036
```

y realizar correctamente el siguiente recorrido:

```text
Abrir SIGES
↓
Visualizar identidad institucional
↓
Ingresar a Sección 01
↓
Buscar un unicódigo REAL
↓
Obtener establecimientos desde productos_bm.SIGES
↓
Seleccionar establecimiento
↓
Autocompletar datos institucionales
↓
Completar información requerida
↓
Guardar
↓
Continuar a Sección 02
↓
Completar información
↓
Guardar
↓
Regresar a Sección 01
↓
Modificar
↓
Guardar nuevamente
↓
Continuar
↓
Comprobar que ningún dato se perdió
```

Todo esto deberá funcionar con una estructura comprensible, limpia y documentada.

---

# 124. PRINCIPIO MAESTRO DEL PROYECTO

> **SIGES debe verse como un aplicativo institucional profesional, pero su código debe seguir siendo sencillo, explícito, ordenado y controlable.**

> **La apariencia puede ser sofisticada. La arquitectura no debe ser innecesariamente sofisticada.**

> **Todo componente debe existir porque cumple una función concreta y comprensible.**

> **No se elimina, recrea o modifica información institucional sin una razón comprobada.**

> **Codex implementa exactamente lo solicitado y evita ampliar el alcance por iniciativa propia.**

---

# FIN DEL AGENTS.md

## Regla ortográfica institucional

Toda documentación técnica, funcional, de base de datos, backend y frontend debe escribirse en español técnico claro respetando las tildes que correspondan según la palabra usada. Esto aplica a README, documentos Markdown, comentarios, docstrings, etiquetas visibles, textos de ayuda, títulos, mensajes de interfaz y documentación de módulos. No se deben retirar tildes por comodidad técnica. Los identificadores de código, nombres de variables, nombres de columnas, rutas, comandos y claves de configuración se mantienen sin cambios cuando la tilde pueda romper una referencia técnica.



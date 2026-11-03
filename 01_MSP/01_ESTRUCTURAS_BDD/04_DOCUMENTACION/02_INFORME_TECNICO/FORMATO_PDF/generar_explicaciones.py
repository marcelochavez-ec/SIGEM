"""Anotaciones del manual, ligadas a las líneas públicas de Python.
Elaborado por Marcelo Chávez. marcelo_chavez_s@outlook.com | 098 333 26 87
https://www.linkedin.com/in/marcelochavezec
No abre credenciales ni ejecuta la API. Solo analiza tres fuentes públicas con AST.
"""
from pathlib import Path
import ast,json,re
MANUAL=Path(__file__).resolve().parent
RAIZ=MANUAL.parents[2]
FUENTES=['deploy/presidencia/api.py','deploy/presidencia/auth.py','deploy/presidencia/linux/servidor.py']
FUNCIONES={
 'create_app':'construye la aplicación FastAPI, su configuración, el gateway y sus rutas',
 'authorize':'valida Bearer, usuario/clave del cliente API y autorización institucional antes del endpoint',
 'view':'resuelve un SID y convierte rechazos o fallos de identidad en respuestas HTTP',
 'invalid_input':'responde 422 sin devolver los secretos que causaron un error de validación',
 'read_snapshot':'lee el corte REST autorizado y valida tamaño, indicadores, fecha y vigencia',
 'headers':'añade políticas de no caché, tipos de contenido, referencia y ancestros iframe',
 'live':'informa que el proceso FastAPI atiende peticiones',
 'ready':'comprueba la disponibilidad y vigencia del corte de indicadores',
 'shiny_health':'consulta por HTTP el visualizador interno para comprobar su disponibilidad',
 'open_session':'valida la cuenta institucional y devuelve la URL temporal del módulo y sus cinco indicadores',
 'shiny_http':'valida la sesión y reenvía HTTP al visualizador con encabezados internos firmados',
 'shiny_websocket':'mantiene el canal interactivo autorizado entre navegador y visualizador',
 'to_upstream':'reenvía al visualizador los mensajes WebSocket recibidos del navegador',
 'to_browser':'envía al navegador los mensajes de texto o binarios del visualizador',
 'check_session':'revalida la sesión cada diez segundos mientras se mantiene el WebSocket',
 'catalog':'entrega el catálogo REST protegido de los cinco indicadores',
 'series':'entrega los puntos agregados de un indicador filtrados por año y rango mensual',
 'module':'abre el indicador inicial de una sesión autorizada',
 'embed':'construye el iframe interno de un indicador después de validar el SID',
 'close_view':'revoca una sesión después de validar su origen HTTP',
 'authorized_demo':'carga la demostración con una URL de iframe de la sesión autorizada',
 'no_anonymous':'rechaza el acceso HTTP al visualizador sin SID',
 'no_anonymous_ws':'rechaza conexiones WebSocket directas sin autorización',
 'demo':'entrega una página inicial que indica cómo crear la sesión',
 'root':'redirige la raíz de este servicio a su entrada de visualización',
 'schema':'adapta OpenAPI a las rutas públicas y declara las tres credenciales API juntas',
 'page':'envuelve el contenido en una página HTML que ocupa todo el espacio disponible',
 '__init__':'prepara la instancia y sus valores de configuración',
 '__call__':'consulta la cuenta institucional, comprueba vigencia y módulo y verifica su contraseña cuando se recibe',
 'verify_institutional_password':'selecciona scrypt o Argon2 según el formato del hash institucional',
 'verify_client':'comprueba el usuario del cliente API y verifica su contraseña contra el hash Argon2',
 'principal':'revalida la identidad institucional configurada sin pedir su contraseña nuevamente',
 'issue':'crea una sesión temporal después de comprobar la contraseña institucional',
 'resolve':'consulta una sesión, comprueba caducidad y revalida revocación o cambio de contraseña',
 'revoke':'retira una sesión del registro en memoria',
 'throttle':'limita fallos de acceso por origen dentro de una ventana de sesenta segundos',
 'filter':'oculta el SID de las rutas antes de escribir un mensaje de registro',
}
CAMPOS={
 'fecha':'fecha del punto mensual, validada como fecha de calendario', 'mes':'nombre del mes mostrado en la serie',
 'valor':'resultado numérico del indicador para ese período', 'meta_mensual':'meta del mes; puede ser nula',
 'numerador':'numerador acumulado del indicador; admite nulo', 'numerador_puntual':'numerador del período puntual; admite nulo',
 'denominador':'denominador usado en la medición; admite nulo', 'fecha_corte':'fecha hasta la que corresponde el dato; admite nulo',
 'fecha_actualizacion':'fecha y hora de actualización; admite nulo', 'id':'uno de los cinco identificadores de indicador permitidos',
 'titulo':'título institucional del indicador', 'objetivo':'descripción del objetivo del indicador',
 'unidad':'unidad de medida, restringida al texto Porcentaje', 'linea_base':'valor de línea base del indicador',
 'meta_2026':'meta anual del año 2026', 'datos':'lista validada de puntos mensuales del modelo Punto',
 'modulo':'módulo, restringido al identificador PRESIDENCIA', 'origen':'identificación de la fuente de datos',
 'generado_en':'fecha y hora en que se produjo el corte autorizado', 'indicadores':'lista de indicadores o enlaces del catálogo',
 'dashboard':'plantilla de URL de visualización del indicador', 'usuario_sivas':'nombre institucional obligatorio, de uno a ochenta caracteres',
 'clave_sivas':'contraseña institucional tratada como SecretStr, de uno a 256 caracteres',
 'indicador':'indicador inicial autorizado; por defecto primer-nivel', 'username':'nombre canónico de la identidad institucional',
 'user_id':'ID interno de la persona; no es su contraseña', 'fingerprint':'huella SHA-256 del hash para detectar cambios posteriores de credencial',
}
ASIGNACIONES={
 'IDS':'declara los cinco identificadores que admite la integración',
 'LABELS':'relaciona esos identificadores con sus títulos institucionales',
 'IndicatorId':'restringe mediante Literal los valores de indicador admitidos',
 'BASE':'resuelve la carpeta real del archivo para encontrar recursos relativos',
 'model_config':'rechaza campos ajenos al contrato; cuando corresponde también impide NaN e infinito',
 'api_key':'obtiene el Bearer del argumento de pruebas o de PRESIDENCIA_API_KEY',
 'gate':'crea o reutiliza el gateway que verifica cliente API, identidad y sesiones',
 'source':'resuelve la ubicación del corte JSON de indicadores desde la configuración',
 'shiny':'normaliza la dirección del visualizador quitando la barra final',
 'parsed':'separa esquema, host y otras partes de la URL para validarlas',
 'ttl':'obtiene la antigüedad máxima permitida al corte, expresada en horas',
 'ancestors':'lee la lista explícita de orígenes que pueden embeber el visualizador',
 'environment':'lee el nombre del ambiente para identificarlo en FastAPI y OpenAPI',
 'app':'crea la instancia FastAPI o adapta su generador OpenAPI',
 'bearer':'prepara el lector del encabezado Authorization sin emitir un rechazo automático',
 'client_user':'prepara el lector del encabezado X-API-Usuario',
 'client_password':'prepara el lector del encabezado X-API-Clave',
 'cut':'lee y valida el corte mediante el contrato Pydantic o reutiliza la lectura validada',
 'age':'calcula en segundos la diferencia entre el instante actual UTC y la generación del corte',
 'dates':'extrae las fechas del indicador para detectar duplicados o años no admitidos',
 'target':'construye la dirección interna a la que se enviará la petición HTTP del visualizador',
 'response':'guarda la respuesta del visualizador o de la siguiente capa HTTP',
 'prefix':'define /api/v1/presidencia, base de los endpoints REST',
 'sid':'genera o recibe el identificador aleatorio temporal de la sesión; no es el Bearer permanente',
 'base':'construye el prefijo público de las URLs de esa sesión a partir de host y esquema de la petición',
 'internal':'lee la URL interna del visualizador para reenviar HTTP y WebSocket',
 'signed':'obtiene los encabezados internos firmados que acreditan la sesión ante el dashboard',
 'origin':'lee el origen declarado por el navegador para comprobar de dónde procede el WebSocket',
 'expected':'normaliza el esquema del WebSocket a HTTP/HTTPS para compararlo con Origin',
 'expected_parts':'extrae esquema y host que deben coincidir con el origen del navegador',
 'backend':'construye la URL ws/wss del visualizador interno, conservando ruta y consulta',
 'message':'recibe un mensaje WebSocket para enviarlo al otro extremo sin convertir su contenido',
 'tasks':'crea las tres tareas: navegador a visualizador, retorno y comprobación periódica de sesión',
 'done, pending':'espera a que termine una tarea para cerrar de forma coordinada las demás',
 'indicator':'localiza el indicador cuyo ID coincide con el solicitado',
 'data':'convierte el indicador validado a tipos JSON y conserva únicamente los puntos del rango pedido',
 'session':'consulta la sesión actual del SID o recibe una copia de sus datos ya validados',
 'result':'genera o completa el documento OpenAPI que consulta Swagger',
 'health_prefix':'lee el prefijo público de las comprobaciones de salud',
 'operation':'representa cada operación HTTP a la que se aplican las credenciales de OpenAPI',
 'SQL_IDENTITY':'declara la consulta institucional parametrizada de lectura; no crea ni modifica personas',
 'row':'obtiene una sola cuenta que cumple actividad, vigencia y permiso de módulo',
 'now':'obtiene el instante actual del reloj configurado para vigencia, revalidación o intentos',
 'timestamp':'produce la marca temporal que forma parte de la firma interna',
 'username':'recupera el usuario canónico de la sesión validada para firmar el acceso',
 'payload':'une usuario, módulo, marca temporal y SID en el mensaje a firmar',
 'signature':'calcula HMAC-SHA256 con la clave interna del puente sobre ese mensaje',
 'start, count':'recupera inicio y número de fallos de la ventana de ese origen',
 'identity':'consulta la identidad institucional actual y su huella de credencial',
 'config':'toma la configuración de registro de Uvicorn para instalar el filtro de SID',
}
RETORNOS={
 'authorize':'Termina la comprobación de acceso; la ruta solo continúa si no se lanzó un error.',
 'view':'Devuelve una copia de la sesión autorizada para ese SID.',
 'invalid_input':'Devuelve JSON genérico con estado 422; no refleja clave_sivas en el error.',
 'read_snapshot':'Devuelve el objeto Corte validado para los endpoints de lectura.',
 'headers':'Devuelve la respuesta HTTP con las políticas de seguridad incorporadas.',
 'live':'Devuelve estado activo, módulo y ambiente como JSON.',
 'ready':'Devuelve estado listo, número de indicadores y fecha del corte.',
 'shiny_health':'Devuelve disponibilidad del visualizador después de comprobar su respuesta HTTP.',
 'open_session':'Devuelve JSON con url, demo, vigencia_segundos y una URL para cada uno de los cinco indicadores.',
 'shiny_http':'Devuelve el cuerpo y estado del visualizador, reenviando solo los encabezados autorizados.',
 'catalog':'Devuelve módulo, fecha del corte y enlaces del catálogo REST.',
 'series':'Devuelve los puntos del indicador dentro del año y meses solicitados, con origen y fecha del corte.',
 'module':'Invoca la vista del indicador inicial guardado en la sesión.',
 'embed':'Devuelve HTML con el iframe interno y el título escapado del indicador.',
 'close_view':'Confirma en JSON que la sesión fue cerrada.',
 'authorized_demo':'Entrega el HTML de demostración sustituyendo su marcador por la URL autorizada.',
 'demo':'Entrega instrucciones HTML para solicitar una sesión de visualización.',
 'root':'Responde con redirección a /embed/presidencia.',
 'schema':'Devuelve el documento OpenAPI ya adaptado y almacenado en caché.',
 'page':'Devuelve el documento HTML completo con metadatos, estilos y contenido del iframe.',
 '__call__':'Devuelve Identity con usuario, ID y huella de credencial; no devuelve el hash original al consumidor.',
 'verify_institutional_password':'Devuelve el resultado de verificar la contraseña frente al formato del hash detectado.',
 'principal':'Solicita al proveedor comprobar la identidad configurada sin una contraseña nueva.',
 'issue':'Devuelve el SID que acaba de crearse; la contraseña no forma parte de ese identificador.',
 'resolve':'Devuelve una copia de la sesión después de las comprobaciones de vigencia y revocación.',
 'headers.auth':'Devuelve los cinco encabezados internos que R validará antes de renderizar el dashboard.',
 'filter':'Permite procesar el registro después de ocultar el SID; no cambia la sesión real del navegador.',
}
SQL={
 34:'Selecciona ID, nombre de usuario y hash almacenado únicamente para verificar identidad.',
 35:'Lee credenciales.usuarios, sin modificar esa tabla.',36:'Compara el nombre mediante un parámetro %s, sin concatenarlo a SQL.',
 37:'Exige usuario activo y excluye el uso de una cuenta superusuario para esta integración.',
 38:'Exige que la fecha inicial de vigencia ya haya comenzado.',39:'Admite vigencia indefinida o una fecha final nula;',40:'en caso de fecha final definida, exige que aún no haya vencido.',
 41:'Exige además la existencia de una asignación de módulo válida.',42:'Lee las asignaciones de credenciales.usuario_modulo.',
 43:'Exige que el módulo relacionado permanezca activo.',44:'Exige que el rol relacionado permanezca activo.',
 45:'Relaciona la asignación con esta persona y exige que esté activa.',46:'Restringe el permiso al módulo PRESIDENCIA y a los roles USUARIO o ADMINISTRADOR.',
 47:'Cierra la comprobación EXISTS de autorización institucional.',48:'Finaliza la cadena SQL; todavía no ejecuta ninguna consulta.'}
IMPORTS={'html':'escape de títulos que se insertan en HTML','asyncio':'tareas y esperas asíncronas del proxy WebSocket','os':'variables de entorno privadas del proceso','secrets':'comparación de credenciales y generación aleatoria de SID','datetime':'fechas, horas y cálculos de vigencia UTC','pathlib':'rutas de archivos independientes del directorio desde el que se invoca el código','typing':'anotaciones de tipo y valores de indicador permitidos','urllib.parse':'separación y validación de direcciones URL','httpx':'peticiones HTTP asíncronas al visualizador interno','fastapi':'aplicación, rutas, dependencias, excepciones y contrato HTTP','fastapi.responses':'respuestas HTML, redirección y cuerpos HTTP','fastapi.security':'lectores de los tres encabezados de autenticación API','fastapi.middleware.trustedhost':'comprobación de nombres de host permitidos','fastapi.exceptions':'manejo de errores de validación de entradas','fastapi.openapi.utils':'generación de OpenAPI para Swagger','pydantic':'modelos de entrada/salida y tratamiento de contraseñas como secretos','websockets.asyncio.client':'conexión WebSocket hacia el visualizador','auth':'gateway y proveedor de identidad institucional reutilizados por api.py','hashlib':'SHA-256 para huellas y firmas','hmac':'firma interna HMAC que acredita el acceso al dashboard','time':'reloj del gateway y de sus sesiones','dataclasses':'identidad inmutable con campos definidos','threading':'exclusión mutua al consultar o modificar sesiones en memoria','argon2':'verificación de hashes Argon2','argon2.exceptions':'rechazos de hash o verificación sin propagar detalles sensibles','psycopg':'lectura de identidad en PostgreSQL','nacl':'verificación del formato scrypt creado por sodium en R','nacl.exceptions':'detección de contraseña scrypt inválida','psycopg.rows':'lectura de resultados SQL por nombre de columna','logging':'filtrado de mensajes antes de escribir registros','re':'reconocimiento de rutas que contienen un SID','uvicorn':'servidor ASGI que ejecuta la aplicación FastAPI'}
def name(n):
 try:return ast.unparse(n)
 except Exception:return ''
def description(n,ctx,filename):
 purpose=FUNCIONES.get(ctx,'realiza esta parte de la integración')
 if isinstance(n,(ast.Import,ast.ImportFrom)):
  mod=n.module if isinstance(n,ast.ImportFrom) else n.names[0].name
  return 'Importa '+mod+' para '+IMPORTS.get(mod,'utilizar los componentes indicados de esa biblioteca')+'.'
 if isinstance(n,ast.AnnAssign):
  k=name(n.target)
  if k=='datos' and name(n.annotation)=='str':return 'Define `datos`: URL del endpoint REST que entrega la serie de este indicador.'
  return 'Define `'+k+'`: '+CAMPOS.get(k,'campo tipado del contrato indicado en esta clase')+'.'
 if isinstance(n,(ast.Assign,ast.AugAssign)):
  k=', '.join(name(t) for t in n.targets) if isinstance(n,ast.Assign) else name(n.target)
  if k.startswith('self.'):
   v=k.split('.')[-1]
   meanings={'sessions':'el registro de SID y sesiones en memoria','lock':'un bloqueo para proteger sesiones e intentos concurrentes','failures':'el contador por origen usado al limitar intentos','username':'el usuario institucional en mayúsculas','client_user':'el nombre del cliente API','checked':'el momento de la última revalidación'}
   return 'Actualiza `'+k+'`: '+meanings.get(v,'la configuración de la instancia utilizada por '+ctx)+'.'
  if k=="operation['security']":return 'Declara en OpenAPI que Bearer, UsuarioAPI y ClaveAPI se exigen juntos para esta operación.'
  if k.startswith('response.headers'):return 'Establece `'+k+'` en la respuesta; esta política limita caché, interpretación de tipos, referencias u orígenes iframe según la línea de código.'
  if k.startswith('self.sessions['):return 'Almacena el SID junto con identidad, indicador, vencimiento y momento de última comprobación.'
  if k.startswith('session['):return 'Actualiza la marca de revalidación de esta sesión sin prolongar su vencimiento.'
  if k.startswith('record.'):return 'Actualiza el registro de log para ocultar el SID y evitar un segundo formateo con argumentos originales.'
  if k.startswith('config[') or k.startswith('handler['):return 'Registra o aplica el filtro OcultarSesion en los manejadores de salida de Uvicorn.'
  return 'En `'+ctx+'`, '+ASIGNACIONES.get(k,'asigna `'+k+'` al resultado de la expresión mostrada')+'.'
 if isinstance(n,ast.Return):return RETORNOS.get(ctx+'.auth' if filename.endswith('auth.py') and ctx=='headers' else ctx,'Devuelve el resultado de esta operación de '+ctx+'.')
 if isinstance(n,(ast.With,ast.AsyncWith)):
  t=name(n.items[0].context_expr)
  if 'lock' in t:return 'Adquiere el bloqueo de memoria durante la comprobación o modificación; se libera al salir del bloque.'
  if 'psycopg' in t:return 'Abre una conexión PostgreSQL de solo lectura con límites de conexión/consulta y resultados por nombre.'
  if 'httpx' in t:return 'Abre un cliente HTTP asíncrono con el timeout indicado y sin seguir redirecciones automáticamente.'
  if 'connect' in t:return 'Abre el WebSocket interno con firma, límite de tamaño y tiempo máximo de apertura.'
  return 'Gestiona automáticamente la apertura y cierre del recurso utilizado por '+ctx+'.'
 if isinstance(n,ast.If):
  c=name(n.test)
  if '__name__' in c:return 'Ejecuta el arranque de Uvicorn únicamente cuando servidor.py se invoca como programa principal.'
  if ctx=='create_app':return 'Comprueba `'+c+'`; rechaza configuración insegura o inválida antes de publicar las rutas.'
  if ctx=='authorize':return 'Comprueba ausencia/esquema del Bearer y compara el token en tiempo constante; un fallo activa AccessDenied.'
  if ctx=='read_snapshot':return 'Comprueba `'+c+'` para asegurar integridad y vigencia del corte antes de devolver datos.'
  if ctx=='shiny_websocket':return 'Compara Origin con el esquema y host públicos esperados; una diferencia impide abrir el WebSocket.'
  if ctx=='resolve':return 'Comprueba `'+c+'` para rechazar vencimiento, revisar revocación o detectar cambio de credencial.'
  if ctx=='__call__':return 'Comprueba `'+c+'` antes de aceptar la identidad institucional o verificar su contraseña.'
  return 'Comprueba `'+c+'` dentro de `'+ctx+'`, que '+purpose+'.'
 if isinstance(n,ast.Raise):
  t=name(n.exc)
  meanings={'401':'rechaza la autenticación o sesión inválida','403':'rechaza el origen no autorizado','422':'rechaza parámetros fuera de contrato','503':'informa indisponibilidad de identidad, corte o visualizador'}
  for code,v in meanings.items():
   if code in t:return 'Interrumpe esta ruta con HTTP '+code+': '+v+'. No devuelve el secreto recibido.'
  if 'AccessDenied' in t:return 'Interrumpe la operación por acceso denegado; la ruta superior lo convierte en un rechazo de autenticación.'
  if 'IdentityUnavailable' in t:return 'Señala que no es posible comprobar identidad o emitir otra sesión; no concede acceso por omisión.'
  if 'RuntimeError' in t:return 'Detiene el arranque con un mensaje de configuración; evita servir una API mal configurada.'
  return 'Interrumpe la validación del recurso y deja que el manejador del bloque traduzca el error.'
 if isinstance(n,ast.Try):return 'Agrupa operaciones de `'+ctx+'` cuyos errores se traducen a una respuesta controlada.'
 if isinstance(n,ast.ExceptHandler):return 'Captura `'+name(n.type)+'` en `'+ctx+'` para responder sin mostrar detalles internos ni credenciales.'
 if isinstance(n,(ast.For,ast.AsyncFor)):
  return 'Recorre `'+name(n.iter)+'` asignando cada elemento a `'+name(n.target)+'` dentro de `'+ctx+'`.'
 if isinstance(n,ast.While):return 'Mantiene el bucle de `'+ctx+'` hasta desconexión, revocación o cancelación coordinada.'
 if isinstance(n,ast.Pass):return 'No añade otra acción: conserva la excepción declarada o el rechazo principal del bloque anterior.'
 if isinstance(n,ast.Break):return 'Finaliza el bucle al detectar desconexión del navegador.'
 if isinstance(n,ast.Expr):
  t=name(n.value)
  if isinstance(n.value,ast.Constant):return 'Texto descriptivo del componente; no ejecuta una operación de red ni abre un servicio.'
  if 'gate.throttle' in t:return 'Consulta o incrementa el contador de fallos del origen, antes de aceptar más intentos.'
  if 'gate.verify_client' in t:return 'Verifica X-API-Usuario y X-API-Clave contra el cliente y su hash configurados.'
  if 'gate.principal' in t:return 'Comprueba que la cuenta institucional configurada siga activa, vigente y autorizada para PRESIDENCIA.'
  if 'to_thread' in t:return 'Ejecuta la validación síncrona de sesión/firma en un hilo y espera el resultado sin bloquear esa espera de red.'
  if 'uvicorn.run' in t:return 'Inicia Uvicorn con la fábrica create_app y las opciones de puerto, trabajador, proxy y registro del bloque.'
  if 'PasswordHasher' in t:return 'Verifica la contraseña contra el hash Argon2; no recupera una contraseña desde el hash.'
  if 'verify_institutional_password' in t:return 'Comprueba la contraseña institucional con el algoritmo que corresponde al hash almacenado.'
  if '.pop' in t:return 'Retira la sesión vencida/revocada del diccionario; si no existe, no añade un error secundario.'
  if 'socket.close' in t:return 'Cierra el WebSocket con código 1008 (política) o 1011 (fallo interno), según el bloque.'
  if 'socket.accept' in t:return 'Acepta el WebSocket del navegador después de comprobar SID, origen y conexión interna.'
  if 'asyncio.sleep' in t:return 'Espera diez segundos antes de revalidar la sesión del WebSocket.'
  if 'task.cancel' in t:return 'Cancela una tarea pendiente cuando otro extremo ya terminó.'
  if 'asyncio.gather' in t:return 'Espera el cierre de las tareas y recoge sus excepciones para terminar coordinadamente.'
  if 'app.add_middleware' in t:return 'Instala TrustedHostMiddleware con la lista de hosts aceptados desde configuración.'
  if 'send' in t:return 'Reenvía el mensaje de texto o binario al extremo indicado, conservando su tipo.'
  return 'Ejecuta `'+t[:145]+'` dentro de `'+ctx+'` para '+purpose+'.'
 return 'En `'+ctx+'`, '+purpose+'.'
REVISION_API = {91: 'Exige un Bearer de al menos 32 caracteres antes de crear la aplicación.',
 93: 'Usa el gateway recibido en pruebas o crea uno con el usuario del cliente API configurado.',
 94: 'Entrega al gateway el hash Argon2 de la clave API y la clave HMAC del puente; no son la '
     'contraseña institucional.',
 95: 'Construye PostgresIdentity para consultar únicamente la cuenta institucional autorizada.',
 96: 'Fija en el gateway el nombre institucional que podrá generar sesiones de Presidencia.',
 97: 'Lee PRESIDENCIA_VIEW_SECONDS como entero; el valor por defecto es 28.800 segundos.',
 101: 'Rechaza una dirección del visualizador sin host o protocolo HTTP/HTTPS, o que incluya '
      'credenciales, consulta o fragmento.',
 104: 'Comprueba que la antigüedad máxima del corte sea mayor que cero.',
 107: 'Impide comodines, saltos de línea y punto y coma en la configuración de orígenes iframe.',
 110: 'Crea FastAPI con título identificable del ambiente y versión 1.0.0.',
 111: 'Describe en OpenAPI el alcance del módulo y la diferencia entre credenciales API y sesión '
      'temporal.',
 112: 'Lee la ruta de Swagger desde PRESIDENCIA_DOCS_URL; su valor inicial es /docs.',
 113: 'Configura la URL de OpenAPI y desactiva la interfaz ReDoc.',
 114: 'Instala el control de host de FastAPI para rechazar dominios no autorizados.',
 115: 'Convierte la cadena de hosts permitidos en una lista separando por comas.',
 120: 'Declara authorize como dependencia de acceso: recibe la petición y el Bearer que FastAPI extrajo '
      'de Authorization.',
 121: 'Recibe X-API-Usuario y X-API-Clave mediante Depends; ninguno se obtiene del JavaScript del '
      'iframe.',
 124: 'Rechaza un Bearer ausente, un esquema distinto de Bearer o un token diferente al configurado; '
      'compara el token en tiempo constante.',
 130: 'Registra el intento fallido asociado al origen para limitar repeticiones dentro de la ventana '
      'configurada.',
 133: 'Devuelve 401 y el encabezado WWW-Authenticate: Bearer, sin especificar qué secreto falló.',
 135: 'Devuelve 503 cuando la identidad institucional no puede comprobarse; no concede acceso por '
      'omisión.',
 203: 'Registra POST /api/v1/presidencia/sesiones y exige que authorize termine correctamente antes de '
      'ejecutar open_session.',
 204: 'Recibe el cuerpo SolicitudSesion ya validado y Request para conocer la dirección pública de la '
      'solicitud.',
 206: 'Extrae la contraseña de SecretStr solo dentro del backend y llama a Gateway.issue con usuario, '
      'contraseña e indicador inicial.',
 215: 'Construye la base pública /vista/<sid> usando esquema y host de Request; Nginx debe aportar los '
      'encabezados correctos.',
 216: 'Devuelve url para el módulo y demo para la página de prueba; ambas incorporan el SID temporal.',
 217: 'Incluye vigencia_segundos y empieza la lista de enlaces individuales de los cinco indicadores.',
 218: 'Asocia cada ID autorizado con su URL /embed/presidencia/<id>; no devuelve contraseñas ni hashes.',
 224: 'Declara el proxy HTTP que recibe SID, recurso interno solicitado y petición HTTP del navegador.',
 225: 'Comprueba la sesión antes de reenviar el recurso; ejecuta esa validación síncrona mediante un '
      'hilo.',
 226: 'Obtiene los encabezados firmados para que el dashboard reconozca al usuario ya autenticado.',
 229: 'Abre un cliente HTTP con espera máxima de cuarenta segundos y sin seguir redirecciones.',
 230: 'Reenvía el método y la consulta recibidos al recurso interno autorizado.',
 231: 'Reenvía el cuerpo y prepara una lista limitada de encabezados del navegador.',
 232: 'Solo admite content-type, cookie, accept y range del navegador; añade después los encabezados '
      'firmados del gateway.',
 235: 'Construye la respuesta con el cuerpo y el estado HTTP del visualizador.',
 236: 'Filtra los encabezados de retorno para no propagar encabezados internos arbitrarios.',
 237: 'Conserva tipo de contenido, disposición de descarga y encabezados de rango necesarios para '
      'recursos y archivos.',
 247: 'Lee Origin del WebSocket para identificar la página que intenta establecer la conexión.',
 248: 'Convierte ws/wss a http/https para comparar el origen contra la URL pública del socket.',
 250: 'Exige igualdad exacta de esquema y host del origen; si no coinciden se cierra la conexión.',
 257: 'Conecta al WebSocket interno con firma, máximo de 4 MiB por mensaje y diez segundos para abrir '
      'la conexión.',
 278: 'Revalida el SID mientras el WebSocket sigue abierto, permitiendo aplicar vencimiento o '
      'revocación.',
 290: 'Registra GET /api/v1/presidencia, aplica authorize y valida su salida con el modelo Catalogo.',
 294: 'Construye un enlace REST y una plantilla de URL de dashboard para cada indicador; la plantilla '
      'exige reemplazar la sesión por un SID real.',
 296: 'Registra GET /api/v1/presidencia/{indicator_id}/serie; exige authorize y valida la respuesta '
      'como Serie.',
 297: 'Limita indicator_id a los cinco IDs y anio a 2026 mediante Query; no habilita otros años por '
      'cambiar la URL.',
 298: 'Declara mes_desde entre uno y doce; su valor inicial es uno.',
 299: 'Declara mes_hasta entre uno y doce; su valor inicial es doce.',
 300: 'Comprueba que el primer mes del rango no sea posterior al último.',
 305: 'Conserva únicamente puntos cuyo año y mes pertenecen al rango autorizado de la petición.',
 316: 'Construye el iframe interno con indicador y SID; escapa el título para que su texto no se '
      'interprete como HTML.'}
def annotate(path):
 s=(RAIZ/path).read_text(encoding='utf-8-sig');lines=s.splitlines();tree=ast.parse(s)
 funcs=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
 classes=[n for n in ast.walk(tree) if isinstance(n,ast.ClassDef)]
 nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.stmt,ast.ExceptHandler)) and not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
 rows={}
 for i,line in enumerate(lines,1):
  st=line.strip()
  if not st:continue
  contexts=[n for n in funcs if n.lineno<=i<=n.end_lineno]
  ctx=min(contexts,key=lambda n:n.end_lineno-n.lineno).name if contexts else 'módulo'
  headers=[n for n in funcs if n.lineno<=i<(n.body[0].lineno if n.body else n.lineno+1)]
  cl=[n for n in classes if n.lineno==i]
  if path.endswith('auth.py') and i in SQL:d=SQL[i]
  elif st.startswith('#'):d='Comentario del código: '+st.lstrip('# ').strip()
  elif st.startswith('@'):
   d='Aplica el decorador `'+st[1:]+'`. '+('Vincula el método y la ruta HTTP con la función que aparece a continuación.' if '@app.' in st else 'Define el comportamiento de la clase o función siguiente.')
  elif headers:
   f=min(headers,key=lambda n:n.end_lineno-n.lineno);d=('Define `'+f.name+'`, que '+('firma el acceso interno al visualizador con HMAC-SHA256' if path.endswith('auth.py') and f.name=='headers' else FUNCIONES.get(f.name,'implementa esta operación'))+'.' if i==f.lineno else 'Completa los parámetros de `'+f.name+'`: '+st+'.')
  elif cl:
   nm=cl[0].name;d='Declara `'+nm+'`: '+({'Gateway':'control del cliente API, identidad, SID, firma y fallos','PostgresIdentity':'proveedor de identidad institucional de lectura','Identity':'identidad inmutable con usuario, ID y huella','AccessDenied':'excepción para denegar acceso','IdentityUnavailable':'excepción por indisponibilidad de identidad','OcultarSesion':'filtro de logging que oculta SID'}.get(nm,'modelo de datos validado de FastAPI/Pydantic'))+'.'
  else:
   candidates=[n for n in nodes if n.lineno<=i<=getattr(n,'end_lineno',n.lineno)]
   n=min(candidates,key=lambda n:(n.end_lineno-n.lineno, -n.lineno)) if candidates else None
   d=description(n,ctx,path) if n else 'Cierra la estructura de parámetros o datos del bloque anterior.'
   if n and i>n.lineno:
    d='Continuación de la instrucción de la línea '+str(n.lineno)+': '+d
  if path.endswith('/api.py') and i in REVISION_API:d=REVISION_API[i]
  rows[str(i)]={'codigo':line,'explicacion':d}
 return rows
salida={p:annotate(p) for p in FUENTES}
(MANUAL/'recursos/explicaciones_python.json').write_text(json.dumps(salida,ensure_ascii=False,indent=2),encoding='utf-8')
print('Anotaciones verificables:',{p:len(v) for p,v in salida.items()})

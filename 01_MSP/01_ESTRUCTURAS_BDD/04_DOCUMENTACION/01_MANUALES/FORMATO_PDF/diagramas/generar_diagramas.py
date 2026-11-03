"""Figuras del manual. Elaborado por Marcelo Chávez, Protección Social - Banco Mundial.
marcelo_chavez_s@outlook.com | 098 333 26 87 | https://www.linkedin.com/in/marcelochavezec
Paleta institucional existente: azul MSP, turquesa, grises y fondo transparente.
"""
from pathlib import Path
from html import escape
import re,math
D=Path(__file__).resolve().parent
INK='#003872';ACC='#008A99';MUT='#52677A';RULE='#B8CEDC'
def text(x,y,t,size=22,color=INK,anchor='start',bold=False):
 return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}"'+(' font-weight="700"' if bold else '')+'>'+escape(t)+'</text>'
def box(x,y,w,h,title,lines=(),focal=False):
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="white" stroke="{ACC if focal else RULE}" stroke-width="{3 if focal else 2}"/>'
 for i,t in enumerate(title.split('|')):s+=text(x+20,y+36+i*29,t,24,bold=True)
 for i,t in enumerate(lines):s+=text(x+20,y+h-24-(len(lines)-1-i)*25,t,19,MUT)
 return s
def arrow(path,dashed=False):
 tokens=re.findall(r'[MHV]|-?\d+(?:\.\d+)?',path)
 pts=[];i=0;x=y=0
 while i<len(tokens):
  cmd=tokens[i];i+=1
  if cmd=='M':x=float(tokens[i]);y=float(tokens[i+1]);i+=2
  elif cmd=='H':x=float(tokens[i]);i+=1
  elif cmd=='V':y=float(tokens[i]);i+=1
  pts.append((x,y))
 if len(pts)>2:
  parts=[f'M{pts[0][0]} {pts[0][1]}']
  for j in range(1,len(pts)-1):
   a,b,c=pts[j-1],pts[j],pts[j+1]
   l1=math.dist(a,b);l2=math.dist(b,c);r=min(8,l1/2,l2/2)
   q=(b[0]-(b[0]-a[0])*r/l1,b[1]-(b[1]-a[1])*r/l1)
   t=(b[0]+(c[0]-b[0])*r/l2,b[1]+(c[1]-b[1])*r/l2)
   parts.append(f'L{q[0]} {q[1]} Q{b[0]} {b[1]} {t[0]} {t[1]}')
  parts.append(f'L{pts[-1][0]} {pts[-1][1]}');path=' '.join(parts)
 return f'<path d="{path}" fill="none" stroke="{ACC}" stroke-width="2"'+(' stroke-dasharray="7 5"' if dashed else '')+' marker-end="url(#arrow)"/>'
def label(x,y,t,size=19):
 w=len(t)*size*.56+24
 return f'<rect x="{x-w/2}" y="{y-size}" width="{w}" height="{size+8}" fill="white"/>'+text(x,y,t,size,MUT,'middle')
def write(name,title,height,body,source_y):
 foot=text(32,source_y,'Fuente: Sistema de Visualización Analítica en Salud (SIVAS).',19,MUT)+text(32,source_y+25,'Elaboración: Marcelo Chávez.',19,MUT)
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Integración de Indicadores de Presidencia. Elaboración: Marcelo Chávez.</desc><defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0L10 4L0 8Z" fill="{ACC}"/></marker></defs>'''+text(32,42,title,28,bold=True)+body+foot+'</svg>'
 (D/(name+'.svg')).write_text(svg,encoding='utf-8')
 (D/(name+'.html')).write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>'+escape(title)+'</title><style>html,body{margin:0;background:transparent}svg{display:block}</style>'+svg+'</html>',encoding='utf-8')
# Arquitectura: componentes físicos y entrada pública; el visualizador conserva el módulo original.
b=arrow('M360 154 H436')+arrow('M764 154 H840')+arrow('M1004 216 V316')
b+=arrow('M840 386 H764')+arrow('M436 386 H360')
b+=arrow('M930 456 V516 H196 V456')+label(564,500,'Validación institucional: solo lectura')
b+=arrow('M1168 180 H1188 V644 H1168',True)
b+=box(32,92,328,124,'Sistema externo',('Backend HTTP + iframe',))
b+=box(436,92,328,124,'Publicación HTTPS',('Dominio institucional',))
b+=box(840,92,328,124,'Nginx del servidor 197',('Puerto 8595',))
b+=box(840,316,328,140,'FastAPI en Python',('api.py · auth.py · servidor.py','127.0.0.1:8000'),True)
b+=box(436,316,328,140,'Dashboard institucional',('Módulo original en R Shiny','127.0.0.1:8001'))
b+=box(32,316,328,140,'PostgreSQL',('Identidad y fuentes autorizadas',))
b+=box(840,580,328,128,'Aplicativo principal',('Docker y ShinyProxy existentes',))
b+=text(32,620,'Las rutas de integración conservan su publicación HTTPS.',21,MUT)
b+=text(32,652,'El sistema consumidor utiliza la URL temporal autorizada.',21,MUT)
write('arquitectura','Arquitectura de la integración publicada',790,b,740)
# Secuencia: cuatro participantes y mensajes numerados.
xs=[142,446,750,1054];names=['Sistema|externo','HTTPS /|Nginx','FastAPI ·|Python','Dashboard|institucional']
b=''
for x,n in zip(xs,names):
 b+=f'<path d="M{x} 196 V980" stroke="{RULE}" stroke-width="2" stroke-dasharray="6 6"/>'
 b+=box(x-110,96,220,100,n,())
steps=[(0,1,244,'1. POST de sesión',False),(1,2,320,'2. Remite credenciales',False),(2,1,400,'3. JSON: URL temporal',True),(1,0,480,'4. Entrega URL al backend',True),(0,1,560,'5. Navegador abre iframe',False),(1,2,640,'6. Solicita /vista/{sid}',False),(2,3,720,'7. Acceso interno firmado',False),(3,2,800,'8. HTML y WebSocket',True),(2,1,880,'9. Respuesta del dashboard',True),(1,0,960,'10. Vista interactiva',True)]
for a,c,y,t,dash in steps:b+=arrow(f'M{xs[a]} {y} H{xs[c]}',dash)+label((xs[a]+xs[c])/2,y-14,t,18)
write('secuencia','Solicitud de sesión y visualización desde un sistema externo',1044,b,996)
# Seguridad: controles en el orden de ingreso.
b='';ys=[92,260,428,596]
for y in ys[:-1]:b+=arrow(f'M600 {y+120} V{y+168}')
for y,title,lines in zip(ys,['Publicación HTTPS y Nginx','Autenticación del cliente en FastAPI','Autenticación institucional de SIVAS','Sesión temporal y dashboard autorizado'],[
 ('Entrada al servicio publicado y transmisión HTTP / WebSocket.',),
 ('Authorization: Bearer · X-API-Usuario · X-API-Clave',),
 ('Usuario, contraseña vigente y permiso de PRESIDENCIA en PostgreSQL.',),
 ('SID vigente → identidad interna firmada → visualizador institucional.',)]):
 b+=box(80,y,1040,120,title,lines,y==260)
write('seguridad','Capas de autenticación y acceso',796,b,746)
# Concurrencia: múltiples consumidores y el servicio publicado.
b=arrow('M302 174 H360 V340 H420')+arrow('M302 362 H420')+arrow('M302 550 H384 V386 H420')
b+=arrow('M720 362 H840')+arrow('M1004 424 V552')
for y,n in [(112,'Sistema externo A'),(300,'Sistema externo B'),(488,'Sistema externo C')]:b+=box(32,y,270,124,n,('Solicitudes autorizadas',))
b+=box(420,300,300,124,'HTTPS / Nginx',('Enrutamiento y WebSocket',))
b+=box(840,300,328,124,'FastAPI en Python',('Autenticación y sesiones',),True)
b+=box(840,552,328,132,'Dashboard institucional',('Interacción del módulo original',))
b+=text(420,590,'Sesiones identificadas por SID.',21,MUT)
b+=text(420,622,'Vigencia y revocación verificadas.',21,MUT)
b+=text(420,654,'Continuidad mediante WebSocket.',21,MUT)
write('concurrencia','Publicación y multiconcurrencia',762,b,712)
print('Cuatro diagramas SVG/HTML actualizados con fuente y elaboración en dos líneas.')

# Dos recorridos del mismo proceso FastAPI; corte REST frente a visualización.
b=text(32,102,'DATOS REST · corte agregado',22,bold=True)
for x,w,title,lines,focal in [(32,248,'PostgreSQL',('Consultas institucionales',),False),(324,248,'Exportador R',('exportar.R / bootstrap.R',),False),(616,248,'Corte JSON',('Refresco horario',),False),(908,260,'FastAPI',('GET de series',),True)]:
 b+=box(x,132,w,124,title,lines,focal)
for a,c in [(280,324),(572,616),(864,908)]:b+=arrow(f'M{a} 194 H{c}')
b+=text(32,346,'VISUALIZACIÓN · HTML y WebSocket',22,bold=True)
for x,w,title,lines,focal in [(32,248,'Sistema externo',('Backend + navegador',),False),(324,248,'HTTPS / Nginx',('Público 443 / interno 8595',),False),(616,248,'FastAPI',('127.0.0.1:8000',),True),(908,260,'Adaptador Shiny',('127.0.0.1:8001',),False)]:
 b+=box(x,376,w,124,title,lines,focal)
for a,c in [(280,324),(572,616),(864,908)]:b+=arrow(f'M{a} 438 H{c}')
b+=text(32,558,'Ambos recorridos utilizan el mismo servicio FastAPI del 197.',21,MUT)
b+=text(32,590,'El adaptador reutiliza la UI, el server y las consultas originales de Presidencia.',21,MUT)
write('recorridos','Datos REST y visualización: dos recorridos',700,b,644)

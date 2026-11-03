"""Valida descargas y concordancia de cortes sin conectarse a servidores."""
from pathlib import Path
import zipfile,json,hashlib,xml.etree.ElementTree as ET,datetime
BASE=Path('tmp/auditoria_api_20261026');NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ids=['primer-nivel','salud-mental','paquete-ninos','paquete-gestantes','medicamentos']
months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
def mes(s):
 t=s.lower().split('-')[0];return next((i for i,n in enumerate(months,1)if n==t or n[:3]==t),None)
def rows_xlsx(p):
 with zipfile.ZipFile(p)as z:
  assert z.testzip() is None
  strings=[''.join(x.itertext())for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  rows=[]
  for r in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:sheetData/s:row',NS):
   row=[]
   for c in r.findall('s:c',NS):
    v=c.find('s:v',NS);v=None if v is None else v.text;row.append(strings[int(v)]if c.get('t')=='s'and v is not None else v)
   rows.append(row)
  return rows
out={'inicio_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tipo':'local_validacion_de_descargas_reales','indicadores':[]}
for id in ids:
 file=BASE/'individual'/(id+'.xlsx');rows=rows_xlsx(file);rest=json.loads((BASE/(id+'_rest.json')).read_text(encoding='utf-8'));metrics=json.loads((BASE/'individual'/(id+'_metricas.json')).read_text(encoding='utf-8'))
 real=sorted(rest['datos'],key=lambda x:x['fecha']);chart=[p['y'] for s in metrics['series']if s['nombre'].lower().startswith('indicador')for p in s['datos']if p['y']is not None]
 excel=[float(r[3])for r in rows[1:]];val=[float(r['valor'])for r in real]
 dates=[datetime.date.fromisoformat(r['fecha']).month for r in real];exdates=[mes(r[1])for r in rows[1:]]
 comparable=len(chart)==len(val)==len(excel);max_c=max((abs(a-b)for a,b in zip(chart,val)),default=0);max_x=max((abs(a-b)for a,b in zip(excel,val)),default=0)
 ok=comparable and max_c<=0.011 and max_x<=0.011 and dates==exdates
 out['indicadores'].append({'id':id,'estado':'aprobado'if ok else'fallido','filas_excel':len(rows)-1,'columnas_excel':len(rows[0]),'filas_REST':len(real),'puntos_grafico_no_nulos':len(chart),'filas_tabla':metrics['filas'],'meses_coinciden':dates==exdates,'desviacion_max_grafico_REST':max_c,'desviacion_max_excel_REST':max_x,'tolerancia':0.011,'generado_en_REST':rest['generado_en'],'CRC_ZIP':'correcto','sha256_xlsx':hashlib.sha256(file.read_bytes()).hexdigest()})
files=['atenciones_establecimientos_primer_nivel.pdf','atenciones_salud_mental.pdf','ninios_ninias_paquete_priorizado_edad.pdf','gestantes_paquete_priorizado_edad.pdf']
try:
 from pypdf import PdfReader
 out['pdf_publicos']=[{'archivo':f,'paginas':len(PdfReader(BASE/f).pages),'sha256':hashlib.sha256((BASE/f).read_bytes()).hexdigest()}for f in files]
 if(BASE/'pdf/fichas.json').exists():
  out['pdf_descargados_handler']=[]
  for id in ids[:4]:
   p=BASE/'pdf'/(id+'.pdf')
   if p.exists():out['pdf_descargados_handler'].append({'id':id,'paginas':len(PdfReader(p).pages),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
except ImportError:out['pdf_validacion']='pendiente: requiere pypdf en el intérprete de validación.'
out['fin_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(BASE/'archivos_y_cortes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('Concordancia REST/gráfico/Excel:',[(x['id'],x['estado'])for x in out['indicadores']])

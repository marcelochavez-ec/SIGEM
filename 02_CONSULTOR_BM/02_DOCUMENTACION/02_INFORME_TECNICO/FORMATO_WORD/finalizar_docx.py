"""Ajustes deterministas de tablas y figuras que reference-doc no resuelve."""
from pathlib import Path
import os
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
from preparar_referencia import NS, W, el, xml, ROOT

def ensure(parent, name):
    x=parent.find('w:'+name,NS)
    if x is None:x=el(name);parent.append(x)
    return x

def main():
    path=ROOT/os.getenv('MSP_WORD_OUTPUT_NAME','Informe_Tecnico_SIGEM.docx')
    with ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
    with ZipFile(ROOT/'Referencia_MSP_preparada.docx') as z:
        source=E.fromstring(z.read('word/document.xml'))
        purple=source.find('.//w:tbl/w:tr/w:tc/w:tcPr/w:shd',NS).get(f'{{{W}}}fill')
    doc=E.fromstring(parts['word/document.xml'])
    captions=[]
    bookmark_id=max([int(v) for v in doc.xpath('//w:bookmarkStart/@w:id',namespaces=NS)] or [0])+1
    for p in doc.findall('.//w:p',NS):
        if p.xpath('string(w:pPr/w:pStyle/@w:val)',namespaces=NS) != 'ImageCaption':continue
        pp=ensure(p,'pPr')
        for name in ('jc','keepNext'):
            x=pp.find('w:'+name,NS)
            if x is not None:pp.remove(x)
        caption=''.join(p.xpath('.//w:t/text()',namespaces=NS)).replace('"','')
        name=f'msp_fig_{len(captions)+1:02d}'
        p.insert(1,el('bookmarkStart',id=bookmark_id,name=name));p.append(el('bookmarkEnd',id=bookmark_id))
        bookmark_id+=1;captions.append((name,caption))
    # La lista se genera desde las leyendas y PAGEREF calcula páginas reales.
    # Evita diferencias de idioma/separador y la exclusión de leyendas en tablas.
    for p in doc.findall('w:body/w:p',NS):
        if ''.join(p.xpath('.//w:t/text()',namespaces=NS))!='MSP_INDICE_FIGURAS':continue
        parent=p.getparent();pos=parent.index(p);parent.remove(p)
        for name,caption in captions:
            entry=el('p');pp=el('pPr');pp.append(el('pStyle',val='TOC1'))
            tabs=el('tabs');tabs.append(el('tab',val='right',leader='dot',pos=9746));pp.append(tabs);entry.append(pp)
            run=el('r');text=el('t');text.text=caption;run.append(text);entry.append(run)
            run=el('r');run.append(el('tab'));entry.append(run)
            field=el('fldSimple',instr=f' PAGEREF {name} \\h ')
            run=el('r');text=el('t');text.text='0';run.append(text);field.append(run);entry.append(field)
            parent.insert(pos,entry);pos+=1
    for table in doc.findall('.//w:tbl',NS):
        figure=bool(table.findall('.//w:drawing',NS))
        tp=ensure(table,'tblPr'); borders=ensure(tp,'tblBorders')
        for edge in ('top','left','bottom','right','insideH','insideV'):
            b=ensure(borders,edge)
            b.attrib.clear();b.set(f'{{{W}}}val','nil' if figure else 'single')
            if not figure:
                b.set(f'{{{W}}}sz','4');b.set(f'{{{W}}}color','000000')
        if figure:
            for p in table.findall('.//w:p',NS):
                pp=ensure(p,'pPr');ensure(pp,'keepLines')
                if p.findall('.//w:drawing',NS):ensure(pp,'keepNext')
            continue
        rows=table.findall('w:tr',NS)
        cols=len(rows[0].findall('w:tc',NS))
        widths=[3400,6346] if cols==2 else [9746//cols]*cols
        tw=ensure(tp,'tblW');tw.set(f'{{{W}}}type','dxa');tw.set(f'{{{W}}}w',str(sum(widths)))
        layout=ensure(tp,'tblLayout');layout.set(f'{{{W}}}type','fixed')
        grid=ensure(table,'tblGrid')
        for child in list(grid):grid.remove(child)
        for width in widths:grid.append(el('gridCol',w=width))
        margins=ensure(tp,'tblCellMar')
        for edge in ('left','right'):
            margin=ensure(margins,edge);margin.set(f'{{{W}}}w','108');margin.set(f'{{{W}}}type','dxa')
        # Reutiliza el color y borde de la plantilla, sin bandas añadidas.
        for i,row in enumerate(table.findall('w:tr',NS)):
            trp=ensure(row,'trPr')
            if i==0:ensure(trp,'tblHeader')
            for j,cell in enumerate(row.findall('w:tc',NS)):
                cp=ensure(cell,'tcPr');shd=ensure(cp,'shd')
                cw=ensure(cp,'tcW');cw.set(f'{{{W}}}type','dxa');cw.set(f'{{{W}}}w',str(widths[min(j,len(widths)-1)]))
                shd.set(f'{{{W}}}val','clear');shd.set(f'{{{W}}}fill',purple if i==0 else 'FFFFFF')
                for p in cell.findall('w:p',NS):
                    pp=ensure(p,'pPr');ps=ensure(pp,'pStyle');ps.set(f'{{{W}}}val','MSPTableHeader' if i==0 else 'MSPTableText')
                    # Pandoc puede fijar negrita explícita en el encabezado.
                    for run in p.findall('w:r',NS):
                        rp=run.find('w:rPr',NS)
                        if rp is not None:
                            color=rp.find('w:color',NS)
                            if color is not None:rp.remove(color)
        # No fija alturas: el texto conserva la expansión natural de la fila.
    # El encabezado y el pie permanecen en las partes copiadas por Pandoc.
    settings=E.fromstring(parts['word/settings.xml']);ensure(settings,'updateFields').set(f'{{{W}}}val','true')
    parts['word/document.xml'],parts['word/settings.xml']=xml(doc),xml(settings)
    with ZipFile(path,'w',ZIP_DEFLATED) as z:
        for n,data in parts.items():z.writestr(n,data)
    print('Formato de tablas y figuras aplicado.')

if __name__=='__main__':main()

"""Prepara la copia institucional sin reconstruir las partes gráficas del original."""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'TEMPLATE_WORD_QUARTO_MSP_LATEX.docx'
DEST = ROOT / 'Referencia_MSP_preparada.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}

def el(tag, **attrs):
    x = E.Element(f'{{{W}}}{tag}')
    for k, v in attrs.items(): x.set(f'{{{W}}}{k}', str(v))
    return x

def xml(x):
    return E.tostring(x, xml_declaration=True, encoding='UTF-8', standalone=True)

def main():
    with ZipFile(SOURCE) as z: parts = {n: z.read(n) for n in z.namelist()}
    doc, styles = (E.fromstring(parts[n]) for n in ('word/document.xml', 'word/styles.xml'))
    pars = doc.findall('w:body/w:p', NS)
    def semantic(sid, name, sample=None, size=22, bold=False, align='both', after=0, before=0, level=None):
        old = styles.find(f"w:style[@w:styleId='{sid}']", NS)
        if old is not None: styles.remove(old)
        st = el('style', type='paragraph', styleId=sid)
        st.extend([el('name', val=name), el('basedOn', val='Normal'), el('next', val='BodyText'), el('qFormat')])
        pp = deepcopy(sample.find('w:pPr', NS)) if sample is not None else el('pPr')
        for x in list(pp):
            if E.QName(x).localname in ('pStyle','rPr','numPr','spacing','jc','outlineLvl'): pp.remove(x)
        pp.extend([el('spacing', before=before, after=after, line=240, lineRule='auto'), el('jc', val=align)])
        if level is not None: pp.extend([el('outlineLvl',val=level),el('keepNext'),el('keepLines')])
        rp = el('rPr')
        rp.extend([el('rFonts', ascii='Arial Narrow', hAnsi='Arial Narrow', eastAsia='Arial Narrow', cs='Arial Narrow'),el('color',val='000000'),el('sz',val=size),el('szCs',val=size),el('lang',val='es-EC')])
        if bold: rp.extend([el('b'),el('bCs')])
        st.extend([pp,rp]); styles.append(st)
        return st
    # Roles Pandoc. Las medidas provienen de los párrafos realmente usados,
    # no de los estilos de título de Office que quedaron sin aplicar.
    semantic('Title','Title',pars[1],26,True,'center')
    semantic('Subtitle','Subtitle',size=24,align='center',after=120)
    semantic('BodyText','Body Text',pars[12],22,after=120)
    semantic('FirstParagraph','First Paragraph',pars[12],22,after=120)
    semantic('Heading1','heading 1',pars[10],22,True,after=120,before=240,level=0)
    semantic('Heading2','heading 2',pars[19],24,True,after=120,before=180,level=1)
    semantic('Heading3','heading 3',size=22,bold=True,after=100,before=120,level=2)
    semantic('Caption','Caption',size=22,align='center',after=160)
    semantic('ImageCaption','Image Caption',size=22,align='center',after=160)
    semantic('TableCaption','Table Caption',size=22,after=100)
    semantic('Compact','Compact',size=22,align='left',after=0)
    semantic('TOCHeading','TOC Heading',size=22,bold=True,align='left',after=200,before=120)
    for i in range(1,4): semantic(f'TOC{i}',f'toc {i}',size=22,align='left',after=60)
    semantic('MSPFigure','MSP Figure',size=22,align='center',after=80)
    semantic('MSPTableText','MSP Table Text',size=22,align='left')
    semantic('MSPTableHeader','MSP Table Header',size=22,bold=True,align='center')
    styles.find("w:style[@w:styleId='MSPTableHeader']/w:rPr/w:color",NS).set(f'{{{W}}}val','FFFFFF')
    # Normalización conservadora: cada variante directa se convierte en estilo
    # con sus mismas propiedades. No se reescriben texto, listas ni tablas.
    p_cache, r_cache = {}, {}
    for p in doc.findall('.//w:p',NS):
        pp = p.find('w:pPr',NS)
        if pp is not None:
            fmt = deepcopy(pp)
            prior = fmt.find('w:pStyle',NS)
            base = prior.get(f'{{{W}}}val') if prior is not None else 'Normal'
            if prior is not None: fmt.remove(prior)
            # La numeración sigue en el párrafo para mantener cada secuencia.
            num = fmt.find('w:numPr',NS)
            if num is not None: fmt.remove(num)
            key = (base,E.tostring(fmt))
            if key not in p_cache:
                sid=f'MSPPar{len(p_cache)+1:03d}'
                st=el('style',type='paragraph',customStyle=1,styleId=sid)
                st.extend([el('name',val=f'MSP párrafo {len(p_cache)+1:03d}'),el('basedOn',val=base)])
                rp=fmt.find('w:rPr',NS)
                if rp is not None: fmt.remove(rp)
                st.append(fmt)
                styles.append(st); p_cache[key]=sid
            newpp=el('pPr');newpp.append(el('pStyle',val=p_cache[key]))
            if pp.find('w:numPr',NS) is not None: newpp.append(deepcopy(pp.find('w:numPr',NS)))
            # rPr de pPr describe la marca de fin de párrafo; no debe pasar a
            # rPr del estilo, pues cambiaría el tamaño heredado por sus palabras.
            if pp.find('w:rPr',NS) is not None: newpp.append(deepcopy(pp.find('w:rPr',NS)))
            p.replace(pp,newpp)
        for run in p.findall('w:r',NS):
            rp=run.find('w:rPr',NS)
            if rp is None or rp.find('w:rStyle',NS) is not None: continue
            key=E.tostring(rp)
            if key not in r_cache:
                sid=f'MSPRun{len(r_cache)+1:03d}'
                st=el('style',type='character',customStyle=1,styleId=sid)
                char_fmt=deepcopy(rp)
                for prop in ('b','bCs','i','iCs'):
                    toggle=char_fmt.find('w:'+prop,NS)
                    if toggle is not None:char_fmt.remove(toggle)
                st.extend([el('name',val=f'MSP carácter {len(r_cache)+1:03d}'),el('basedOn',val='DefaultParagraphFont'),char_fmt])
                styles.append(st);r_cache[key]=sid
            newrp=el('rPr');newrp.append(el('rStyle',val=r_cache[key]))
            # Word no reproduce el resaltado desde un estilo de carácter;
            # se conserva además en el run para no perder el aspecto de la copia.
            for prop in ('highlight','b','bCs','i','iCs'):
                if rp.find('w:'+prop,NS) is not None:newrp.append(deepcopy(rp.find('w:'+prop,NS)))
            run.replace(rp,newrp)
    # Estilo de tabla tomado de la primera matriz institucional (violeta/blanco).
    table=doc.find('.//w:tbl',NS)
    st=el('style',type='table',customStyle=1,styleId='Table')
    st.append(el('name',val='Table'))
    tp=deepcopy(table.find('w:tblPr',NS))
    for x in list(tp):
        if E.QName(x).localname in ('tblW','tblInd','tblLook','tblStyle'):tp.remove(x)
    st.append(tp)
    # La negrita pertenece a MSP Table Header: duplicarla en el estilo de
    # tabla haría que Word la invierta al combinar ambos estilos.
    header=el('tblStylePr',type='firstRow');rp=el('rPr');rp.append(el('color',val='FFFFFF'));header.append(rp)
    cell=el('tcPr');sample=table.find('w:tr/w:tc/w:tcPr/w:shd',NS)
    if sample is not None:cell.append(deepcopy(sample))
    header.append(cell);st.append(header)
    old=styles.find("w:style[@w:styleId='Table']",NS)
    if old is not None:styles.remove(old)
    styles.append(st)
    parts['word/document.xml'],parts['word/styles.xml']=xml(doc),xml(styles)
    with ZipFile(DEST,'w',ZIP_DEFLATED) as z:
        for n,data in parts.items():z.writestr(n,data)
    print('Referencia preparada:',DEST.name)

if __name__=='__main__':main()

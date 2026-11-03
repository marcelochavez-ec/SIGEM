"""Verificaciones estructurales de la entrega; no sustituye la revisión visual."""
from hashlib import sha256
from zipfile import ZipFile
from pathlib import Path
from lxml import etree as E
import re,json
from preparar_referencia import ROOT,NS,W

def read_doc(path):
    with ZipFile(path) as z:return {n:z.read(n) for n in z.namelist()}

def main():
    source=ROOT/'TEMPLATE_WORD_QUARTO_MSP_LATEX.docx'
    assert sha256(source.read_bytes()).hexdigest()=='ed001b1e3c9564e28a3ea9806c4e5f61d8a140c24f8ae694677fa0db79b530a9','El original cambió.'
    original,reference,final=map(read_doc,[source,ROOT/'Referencia_MSP_preparada.docx',ROOT/'Manual_Indicadores_Presidencia_MSP.docx'])
    for name,data in original.items():
        if name not in ('word/document.xml','word/styles.xml'):assert reference[name]==data,name
    orig=E.fromstring(original['word/document.xml']);doc=E.fromstring(final['word/document.xml'])
    a,b=(x.find('w:body/w:sectPr',NS) for x in (orig,doc))
    for name in ('pgSz','pgMar','cols','docGrid'):
        assert dict(a.find('w:'+name,NS).attrib)==dict(b.find('w:'+name,NS).attrib),name
    graphics={sha256(v).hexdigest() for k,v in original.items() if k.startswith('word/media/')}
    retained={sha256(v).hexdigest() for k,v in final.items() if k.startswith('word/media/')}
    assert graphics<=retained,'Falta un recurso gráfico de la plantilla.'
    captions=doc.xpath('//w:p[w:pPr/w:pStyle[@w:val="ImageCaption"]]',namespaces=NS)
    # Word puede dividir una instrucción entre varios runs al guardar.
    field_codes=''.join(doc.xpath('//w:instrText/text()',namespaces=NS))
    field_codes+=' '+' '.join(doc.xpath('//w:fldSimple/@w:instr',namespaces=NS))
    refs=re.findall(r'PAGEREF\s+(msp_fig_\d+)',field_codes)
    assert len(captions)==len(refs)==17,(len(captions),len(refs))
    assert set(refs)=={f'msp_fig_{i:02d}' for i in range(1,18)}
    for i,p in enumerate(captions,1):assert p.xpath('boolean(w:bookmarkStart[@w:name=$name])',namespaces=NS,name=f'msp_fig_{i:02d}')
    text=' '.join(doc.xpath('//w:t/text()',namespaces=NS))
    for forbidden in ('MSP_INDICE_FIGURAS','No se encontraron entradas','VISITA TÉCNICA AL CENTRO','XXXX','DLIs','BM_INDICADORES_01'):
        assert forbidden not in text,forbidden
    assert 'Meta 2026 (%)' in text
    qmd=(ROOT/'Manual_de_usuario_Indicadores_de_Presidencia.qmd').read_text(encoding='utf-8')
    resources=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',qmd)
    assert len(resources)==17
    for filename in resources:assert (ROOT/filename).is_file(),filename
    for filename in ('preparar_referencia.py','finalizar_docx.py','verificar_manual.py','procesar_word.ps1','Manual_de_usuario_Indicadores_de_Presidencia.qmd'):
        s=(ROOT/filename).read_text(encoding='utf-8')
        assert not re.search(r'\\u00(?:e1|e9|ed|f3|fa|f1|c1|c9|cd|d3|da|d1)',s),filename
    result={'original_intacto':True,'partes_no_editables_referencia_intactas':True,'geometria_institucional':True,'graficos_originales_conservados':len(graphics),'figuras_y_referencias':17,'recursos_disponibles':len(resources),'contenido_ajeno_o_marcadores':False}
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()

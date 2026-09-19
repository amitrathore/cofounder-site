#!/usr/bin/env python3
"""Build the three review DOCX files from canonical Markdown; no website writes.
Preset: standard_business_brief; memo_masthead without decorative rule.
Overrides: black 24pt title; dark-red headings; 9pt running labels; yellow fields.
Literal legal clause/subclause identifiers are retained for stable cross-reference.
"""
from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
HERE=Path(__file__).resolve().parent
STEMS=['awake-cofounder-agreement-v2-review','guide','change-summary']

def plain(text):
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',text)
    return text.replace('**','').replace('`','').replace('<br>','\n')

def runs(p,text):
    # Link labels, bold, code, and completion fields are parsed without loss.
    pat=r'(\[[^\]]+\]\([^)]+\)|\*\*.*?\*\*|`[^`]+`|\[(?:REQUIRED|SELECT ONE|OPTIONAL|COUNSEL|DRAFTING NOTE):[^\]]*\])'
    for part in re.split(pat,text):
        if not part: continue
        link=re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)',part)
        if link:
            h=OxmlElement('w:hyperlink'); target=link[2]
            if target.startswith('./'): target=target[2:]
            h.set(qn('r:id'),p.part.relate_to(target,RT.HYPERLINK,is_external=True))
            r=OxmlElement('w:r'); pr=OxmlElement('w:rPr')
            color=OxmlElement('w:color'); color.set(qn('w:val'),'245B87');pr.append(color)
            r.append(pr);t=OxmlElement('w:t');t.text=plain(link[1]);r.append(t);h.append(r);p._p.append(h)
        elif part.startswith('**'):
            r=p.add_run(part[2:-2]);r.bold=True
            if '[' in part:r.font.highlight_color=WD_COLOR_INDEX.YELLOW
        else:
            r=p.add_run(part.strip('`'))
            if re.match(r'\[(REQUIRED|SELECT ONE|OPTIONAL|COUNSEL|DRAFTING NOTE):',part):
                r.font.highlight_color=WD_COLOR_INDEX.YELLOW

def number_id(doc,fmt):
    root=doc.part.numbering_part.element
    aid=max([int(x.get(qn('w:abstractNumId'))) for x in root.findall(qn('w:abstractNum'))]+[-1])+1
    nid=max([int(x.get(qn('w:numId'))) for x in root.findall(qn('w:num'))]+[0])+1
    an=OxmlElement('w:abstractNum');an.set(qn('w:abstractNumId'),str(aid))
    lvl=OxmlElement('w:lvl');lvl.set(qn('w:ilvl'),'0')
    for name,val in [('start','1'),('numFmt',fmt),('lvlText','%1.' if fmt=='decimal' else '•'),('lvlJc','left')]:
        x=OxmlElement('w:'+name);x.set(qn('w:val'),val);lvl.append(x)
    pp=OxmlElement('w:pPr');tabs=OxmlElement('w:tabs');tab=OxmlElement('w:tab');tab.set(qn('w:val'),'num');tab.set(qn('w:pos'),'720');tabs.append(tab);pp.append(tabs)
    ind=OxmlElement('w:ind');ind.set(qn('w:left'),'720');ind.set(qn('w:hanging'),'360');pp.append(ind);lvl.append(pp);an.append(lvl);root.append(an)
    num=OxmlElement('w:num');num.set(qn('w:numId'),str(nid));x=OxmlElement('w:abstractNumId');x.set(qn('w:val'),str(aid));num.append(x);root.append(num)
    return nid

def build(stem):
    d=Document();sec=d.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Inches(1)
    sec.header_distance=sec.footer_distance=Inches(.492)
    specs=[('Normal',11,0,6,'161411'),('Title',24,0,8,'161411'),('Subtitle',11,0,6,'555555'),('Heading 1',16,16,8,'9B3029'),('Heading 2',13,12,6,'9B3029'),('Heading 3',12,8,4,'161411'),('Header',9,0,0,'555555'),('Footer',9,0,0,'555555'),('List Paragraph',11,0,8,'161411')]
    for name,size,bef,aft,col in specs:
        st=d.styles[name];st.font.name='Calibri';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string(col);st.font.bold=name.startswith('Heading')
        pf=st.paragraph_format;pf.space_before=Pt(bef);pf.space_after=Pt(aft);pf.line_spacing=1.167 if name=='List Paragraph' else 1.10
        for border in st.element.findall('./'+qn('w:pPr')+'/'+qn('w:pBdr')):
            border.getparent().remove(border)
        pf.keep_with_next=name.startswith('Heading') or name=='Title';pf.widow_control=True;pf.alignment=WD_ALIGN_PARAGRAPH.LEFT
    label={'guide':'COMPLETION GUIDE','change-summary':'CHANGE SUMMARY'}.get(stem,'AWAKE COFOUNDER AGREEMENT')
    sec.header.paragraphs[0].text=label+' | V2.0 PUBLIC REVIEW DRAFT'
    ft=sec.footer.paragraphs[0];ft.alignment=WD_ALIGN_PARAGRAPH.RIGHT;ft.add_run('Not approved for signature | ')
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');ft._p.append(fld)
    d.core_properties.title=label.title()+' — Version 2.0 Public Review Draft';d.core_properties.author='Amit Rathore';d.core_properties.subject='California holding LLC + Delaware corporation; unapproved review draft'
    content=(HERE/(stem+'.md')).read_text()
    expected=[]
    for block in content.strip().split('\n\n'):
        if block=='---': continue
        if block.startswith('#'):
            m=re.match(r'^(#{1,4}) (.*)$',block);assert m,block
            depth=len(m[1]);text=m[2]
            p=d.add_paragraph(style='Title' if depth==1 else f'Heading {depth-1}');runs(p,text)
            if stem==STEMS[0] and (text=='Execution' or text.startswith('Schedule ')):
                p.paragraph_format.page_break_before=True
            expected.append(plain(text));continue
        block=re.sub(r'^> ?', '',block,flags=re.M).replace('<br>\n','\n').replace('<br>','\n')
        lines=block.splitlines()
        islist=all(re.match(r'^(?:- |\d+\. )',x) for x in lines)
        if islist:
            fmt='decimal' if re.match(r'^\d',lines[0]) else 'bullet';nid=number_id(d,fmt)
            for line in lines:
                text=re.sub(r'^(?:- |\d+\. )','',line)
                p=d.add_paragraph(style='List Paragraph');pp=p._p.get_or_add_pPr();np=OxmlElement('w:numPr')
                il=OxmlElement('w:ilvl');il.set(qn('w:val'),'0');ni=OxmlElement('w:numId');ni.set(qn('w:val'),str(nid));np.append(il);np.append(ni);pp.append(np)
                runs(p,text);expected.append(plain(text))
        else:
            assert not block.startswith('|'), 'Tables need explicit geometry'
            p=d.add_paragraph();runs(p,block);expected.append(plain(block))
            if block.startswith('**Limited Liability Company Operating Agreement'):
                p.paragraph_format.page_break_before=True
                p.paragraph_format.keep_with_next=True
            if block.startswith(('Signature:','Name:')):p.paragraph_format.keep_with_next=True
    path=HERE/(stem+'.docx');d.save(path)
    # Hyperlink text is included through XML iteration for exact source reconciliation.
    actual=[''.join(el.itertext()) for el in []]
    actual=[''.join(t.text or '' for t in p._p.iter(qn('w:t'))) for p in d.paragraphs]
    norm=lambda x:re.sub(r'\s+','',x)
    assert norm(''.join(actual))==norm(''.join(expected)),stem+' source text mismatch'
    print(stem,len(d.paragraphs),'paragraphs; source reconciliation passed')

if __name__=='__main__':
    for stem in STEMS:build(stem)

#!/usr/bin/env python3
"""
Generate standalone notes for Chapter 5 — Thorax & Rib Cage
Source: Dr. Parag Nigam, WII + peer-reviewed elaboration
Outputs: Elephant_Chapter_5.docx  and  Elephant_Chapter_5.pdf
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, Image as RLImage,
                                 HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

DIR    = '/home/user/Workshop-on-Conference'
SLIDES = '/home/user/Workshop-on-Conference/slide_images/crops'
OUT_D  = os.path.join(DIR, 'Elephant_Chapter_5.docx')
OUT_P  = os.path.join(DIR, 'Elephant_Chapter_5.pdf')

DARK   = RGBColor(0x1B, 0x43, 0x32)
MED    = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT  = RGBColor(0x52, 0xB7, 0x88)
TINT   = RGBColor(0xD8, 0xF3, 0xDC)
TINT2  = RGBColor(0xEA, 0xF7, 0xEE)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
MUTED  = RGBColor(0x55, 0x55, 0x55)
REDL   = RGBColor(0xFA, 0xE0, 0xD8)
RED    = RGBColor(0x8B, 0x00, 0x00)

def rgb_hex(rgb): return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'
def slide(n): return os.path.join(SLIDES, f'slide_{n:02d}.png')

# ── DOCX HELPERS ──────────────────────────────────────────────────────────────
def shade_cell(cell, hex_color):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color); tcPr.append(shd)

def page_break(doc):
    p = doc.add_paragraph(); run = p.add_run()
    br = OxmlElement('w:br'); br.set(qn('w:type'), 'page'); run._r.append(br)
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)

def sec1(doc, text):
    h = doc.add_paragraph(text); h.style = doc.styles['Heading 1']
    h.paragraph_format.space_before = Pt(8); h.paragraph_format.space_after = Pt(2)
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(7); p.paragraph_format.space_after = Pt(7)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(14); run.font.bold = True
    run.font.color.rgb = WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def sec2(doc, text):
    h = doc.add_paragraph(text); h.style = doc.styles['Heading 2']
    h.paragraph_format.space_before = Pt(4); h.paragraph_format.space_after = Pt(2)
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(MED))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(11); run.font.bold = True
    run.font.color.rgb = WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def para(doc, text, size=9.5, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4):
    p = doc.add_paragraph(); p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(size); run.font.bold = bold
    run.font.italic = italic; run.font.color.rgb = color or BLACK
    return p

def bullet(doc, text, level=0, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.5)
    p.paragraph_format.first_line_indent = Cm(-0.3)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(('◦  ' if level > 0 else '•  ') + text)
    run.font.name = 'Calibri'; run.font.size = Pt(size); run.font.color.rgb = BLACK

def img(doc, n, caption='', width_cm=15):
    path = slide(n)
    if os.path.exists(path):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(path, width=Cm(width_cm))
    if caption:
        cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(6)
        cr = cp.add_run(caption)
        cr.font.name = 'Calibri'; cr.font.size = Pt(8)
        cr.font.italic = True; cr.font.color.rgb = MUTED

def keybox(doc, text, danger=False):
    bg = rgb_hex(REDL) if danger else rgb_hex(TINT)
    fg = RED if danger else DARK
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, bg)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(5)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(9)
    run.font.bold = True; run.font.color.rgb = fg
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def dtable(doc, headers, rows, widths=None):
    n = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n); tbl.style = 'Table Grid'
    for i, h in enumerate(headers):
        shade_cell(tbl.rows[0].cells[i], rgb_hex(MED))
        p = tbl.rows[0].cells[i].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(str(h))
        run.font.name='Calibri'; run.font.size=Pt(8.5); run.font.bold=True; run.font.color.rgb=WHITE
    for ri, row in enumerate(rows):
        bg = rgb_hex(TINT2) if ri % 2 else 'FFFFFF'
        for ci, val in enumerate(row):
            shade_cell(tbl.rows[ri+1].cells[ci], bg)
            p = tbl.rows[ri+1].cells[ci].paragraphs[0]
            txt, bld = (val[0], val[1]) if isinstance(val, tuple) else (val, False)
            run = p.add_run(str(txt)); run.font.bold = bld
            run.font.name='Calibri'; run.font.size=Pt(8.5); run.font.color.rgb=BLACK
    if widths:
        for row in tbl.rows:
            for ci, cell in enumerate(row.cells):
                if ci < len(widths): cell.width = Cm(widths[ci])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD WORD DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
def build_docx():
    doc = Document()
    s = doc.sections[0]
    s.page_width=Cm(21); s.page_height=Cm(29.7)
    s.left_margin=s.right_margin=Cm(2.0); s.top_margin=s.bottom_margin=Cm(1.8)
    doc.core_properties.title  = 'Elephant Anatomy Notes — Chapter 5: Thorax & Rib Cage'
    doc.core_properties.author = 'Dr. Parag Nigam, WII (web-elaborated)'

    # TITLE BANNER
    tbl = doc.add_table(rows=1, cols=1); tbl.style='Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(18); p.paragraph_format.space_after=Pt(18)
    r0 = p.add_run('STUDY NOTES — CHAPTER 5\n')
    r0.font.name='Calibri'; r0.font.size=Pt(9); r0.font.bold=True; r0.font.color.rgb=LIGHT
    r1 = p.add_run('Thorax & Rib Cage\n')
    r1.font.name='Calibri'; r1.font.size=Pt(22); r1.font.bold=True; r1.font.color.rgb=WHITE
    r2 = p.add_run('Biological and Anatomical Aspects of Elephants\n')
    r2.font.name='Calibri'; r2.font.size=Pt(11); r2.font.bold=False; r2.font.color.rgb=TINT
    r3 = p.add_run('Dr. Parag Nigam, PhD  ·  Wildlife Institute of India, Dehradun')
    r3.font.name='Calibri'; r3.font.size=Pt(10); r3.font.italic=True; r3.font.color.rgb=TINT
    doc.add_paragraph()
    keybox(doc,
        'Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  |  Technical Support: WII Dehradun\n'
        'Notes elaborated with peer-reviewed literature and web sources.')

    keybox(doc,
        'CONTENTS OF THIS DOCUMENT:\n'
        '  5.1  Rib Count & Structure — rib pairs, sternal vs asternal vs floating ribs, keel sternum\n'
        '  5.2  Comparison with Domestic Species — rib counts, pleural space, breathing mechanisms\n'
        '  5.3  No Pleural Space — Unique Respiratory Anatomy — fused pleura, diaphragm-only breathing\n'
        '  5.4  Diaphragm — Structure & Function — respiratory rate, tidal volume, evolutionary reason\n'
        '  5.5  Necropsy Findings — Thorax — normal vs pathological findings, heart, trachea parasites\n'
        '  CRITICAL DANGER KEYBOX — sternal recumbency, thoracocentesis, IPPV, necropsy note')

    # ─────────────────────────────────────────────────────────────────────────
    # CHAPTER 5: THORAX & RIB CAGE
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '5.  Thorax & Rib Cage')
    img(doc, 10, 'Slide 10 — Thoracic skeleton: extensive rib cage reaching to os coxae level', 14)

    sec2(doc, '5.1  Rib Count & Structure')
    para(doc,
        'The elephant rib cage is one of the most expansive of any terrestrial mammal. It extends '
        'posteriorly almost to the level of the os coxae (pelvis), enclosing the enormous thoracic '
        'cavity needed to house a 12–21 kg heart and very large lungs.',
        size=9.5, space_after=4)
    dtable(doc,
        ['Parameter', 'Asian Elephant', 'African Elephant'],
        [('Total rib pairs','19–20','21'),
         ('Sternal ribs (attached directly to sternum)','6','6'),
         ('Asternal ribs (attached via costal cartilage)','9','9'),
         ('Floating ribs (free — no sternal attachment)','~4–5','~6'),
         ('Extent of rib cage','Reaches nearly to os coxae level','Similar extent'),
         ('Thoracic cavity volume','Very large — accommodates 12–21 kg heart','Very large')],
        widths=[6, 5, 5.5])
    bullet(doc, 'Sternum: has a definite keel (carina) — unlike most domestic animals where the sternum is flat')
    bullet(doc, 'Xiphoid cartilage: articulates obliquely and bends ventrally — relevant to positioning during anaesthesia')
    bullet(doc, 'Costal cartilages: wide, calcify with age; useful at necropsy for gross age estimation')
    bullet(doc, 'Thoracic vertebrae: 19–20 in Asian elephant; each bears a pair of ribs; spinous processes elongated dorsally')

    sec2(doc, '5.2  Comparison with Domestic Species')
    dtable(doc,
        ['Species', 'Rib Pairs', 'Pleural Space', 'Breathing Mechanism'],
        [('Asian Elephant','19–20','ABSENT — pleura fused','Diaphragm ONLY'),
         ('African Elephant','21','ABSENT — pleura fused','Diaphragm ONLY'),
         ('Horse','18','Present — fluid-filled','Diaphragm + rib cage expansion'),
         ('Cattle','13','Present — fluid-filled','Diaphragm + rib cage expansion'),
         ('Dog','13','Present — fluid-filled','Diaphragm + rib cage expansion'),
         ('Human','12','Present — fluid-filled','Diaphragm + rib cage expansion')],
        widths=[3.5, 2.5, 4.5, 6])

    sec2(doc, '5.3  No Pleural Space — Unique Respiratory Anatomy')
    para(doc,
        'The elephant is the ONLY mammal known to have no true pleural space. In all other '
        'mammals, a fluid-filled pleural cavity separates the visceral pleura (covering the lung) '
        'from the parietal pleura (lining the chest wall), creating a sealed pressure-differential '
        'space that passively drives lung inflation and deflation. In elephants, this space does '
        'not exist:',
        size=9.5, space_after=5)
    bullet(doc, 'Both visceral and parietal pleura are composed of DENSE CONNECTIVE TISSUE (not the typical serous membrane found in other mammals)')
    bullet(doc, 'The two pleural layers are FUSED together via loose connective tissue — no fluid-filled pleural cavity exists between them')
    bullet(doc, 'Lungs are therefore physically ADHERED to the chest wall — they cannot collapse passively as in other mammals')
    bullet(doc, 'Breathing is driven almost ENTIRELY by DIAPHRAGM MOVEMENT — no contribution from rib cage expansion/contraction')
    bullet(doc, 'The diaphragm is unusually THICK AND MUSCULAR to generate the required inspiratory pressure differentials alone')
    bullet(doc, 'This adaptation may be related to semi-aquatic evolutionary ancestry — swimming elephants submerge with trunk as snorkel; pleural fusion may prevent lung compression at depth')
    bullet(doc, "West JB (2001): confirmed the biophysical significance of this arrangement for deep-water breathing during swimming")

    sec2(doc, '5.4  Diaphragm — Structure & Function')
    bullet(doc, 'Diaphragm is the PRIMARY and near-exclusive respiratory muscle in elephants')
    bullet(doc, 'Much thicker and more muscular than in other large mammals')
    bullet(doc, 'On contraction: pulls lungs downward and posteriorly (caudoventrally), increasing thoracic volume → inspiration')
    bullet(doc, 'On relaxation: thoracic volume decreases → passive expiration')
    bullet(doc, 'Accessory respiratory muscles (intercostals) play a MINIMAL role compared to other species')
    bullet(doc, 'Resting respiratory rate: ~4–8 breaths per minute (slower than most mammals of similar metabolic rate)')
    bullet(doc, 'Tidal volume: very large, compensating for slow rate')
    bullet(doc, 'The central tendon of the diaphragm is anchored to the caudal border of the sternum and the thoracic vertebral column')
    bullet(doc, 'Diaphragm weight estimated at 2–4% of total body weight — reflects the enormous musculature required')

    keybox(doc,
        'CRITICAL CLINICAL DANGERS — UNIQUE TO ELEPHANTS:\n\n'
        '1. STERNAL RECUMBENCY IS FATAL\n'
        '   In sternal (prone) position, abdominal viscera shift cranially and compress the diaphragm '
        'from the ventral aspect, preventing its caudal movement → complete respiratory arrest develops '
        'within minutes. The xiphoid cartilage arrangement also physically prevents full sternal '
        'recumbency. ALWAYS maintain LATERAL recumbency (left lateral preferred) for any sedated or '
        'anaesthetised elephant.\n\n'
        '2. NO THORACOCENTESIS / CHEST DRAINAGE POSSIBLE\n'
        '   Because the visceral and parietal pleura are fused, there is NO pleural cavity to drain. '
        'Fluid (haemothorax, exudate) accumulates WITHIN the connective tissue, making thoracocentesis '
        'impossible and diagnostically misleading. Fluid accumulation in this region is a serious clinical '
        'emergency with no simple drainage solution.\n\n'
        '3. ANAESTHESIA — IPPV PARAMETERS DIFFER\n'
        '   Intermittent Positive Pressure Ventilation (IPPV) parameters differ significantly from other '
        'large mammals. Inspiratory pressures must overcome the resistance of the fused pleural connective '
        'tissue. Standard equine or bovine IPPV protocols are NOT directly applicable.\n\n'
        '4. NECROPSY NOTE\n'
        '   Never mistake the normal firm lung-wall adhesion for pathological pleuritis or fibrinous pleurisy. '
        'The adhesion is present in ALL elephants — it is the normal anatomical state, not a disease finding.',
        danger=True)

    sec2(doc, '5.5  Necropsy Findings — Thorax')
    bullet(doc, 'On opening the chest wall: lungs appear firmly attached to the inner chest wall surface — this is NORMAL anatomy, not adhesion from pleuropneumonia')
    bullet(doc, 'No fluid should be present in the "pleural space" — any fluid collection between chest wall and lung surface is pathological (haemorrhage, exudate, oedema)')
    bullet(doc, 'Heart: positioned centrally in the thorax; apex is BIFID (double-pointed) — distinctive and normal; weight 12–21 kg')
    bullet(doc, 'Lungs: large, soft, pink-grey; spongy texture; may show mild congestion post-mortem (gravitational)')
    bullet(doc, 'Trachea: large-diameter; check for foreign bodies, mucus plugs, parasites (Mammomonogamus)')
    bullet(doc, 'Pericardium: check for haemopericardium, fibrinous deposits (endotheliotropic herpesvirus — EEHV — in calves)')
    bullet(doc, 'Intercostal spaces: examine for intercostal muscle haemorrhage — may indicate electrocution (lightning or poaching)')
    bullet(doc, 'Diaphragm: inspect for tears, herniation, parasitic cysts (Taenia spp.) on peritoneal surface')

    keybox(doc,
        'MORTALITY INVESTIGATION — THORAX DOCUMENTATION CHECKLIST:\n'
        '• Measure heart weight; document bifid apex; check for EEHV haemorrhages (calves)\n'
        '• Describe lung colour, texture, consolidation, parasites, foreign bodies\n'
        '• Document any fluid between lung and chest wall (volume, colour, odour, consistency)\n'
        '• Collect tracheal swabs for respiratory pathogen PCR (EEHV, Elephant Poxvirus, Mycobacterium)\n'
        '• Inspect diaphragm integrity — tears are common in HEC (human-elephant conflict) fatalities\n'
        '• Intercostal muscle haemorrhage: photograph and sample (histology for lightning/electrocution)')
    doc.add_paragraph()

    # FOOTER
    para(doc,
        'Notes compiled from lecture by Dr. Parag Nigam, PhD — Wildlife Institute of India  |  Web-elaborated June 2026',
        size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc,
        'Training Program: Essentials for Mortality Investigation of Asian Elephant  ·  5–6 June 2026, Raigarh, Chhattisgarh',
        size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(OUT_D)
    print(f'  ✓  {OUT_D}  ({os.path.getsize(OUT_D)//1024} KB)')


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD PDF DOCUMENT
# ══════════════════════════════════════════════════════════════════════════════
def build_pdf():
    W, H = A4
    doc = SimpleDocTemplate(OUT_P, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.8*cm, bottomMargin=1.8*cm)
    styles = getSampleStyleSheet()
    story  = []

    DK = colors.HexColor('#1B4332'); MD = colors.HexColor('#2D6A4F')
    LT = colors.HexColor('#52B788'); TN = colors.HexColor('#D8F3DC')
    T2 = colors.HexColor('#EAF7EE'); RD = colors.HexColor('#FAE0D8')
    WH = colors.white
    MT = colors.HexColor('#555555'); DRD = colors.HexColor('#8B0000')

    def ST(name, **kw):
        s = ParagraphStyle(name, parent=styles['Normal'])
        for k, v in kw.items(): setattr(s, k, v)
        return s

    sH1  = ST('H1', fontSize=13, textColor=WH, leading=17, fontName='Helvetica-Bold')
    sH2  = ST('H2', fontSize=10.5, textColor=WH, leading=14, fontName='Helvetica-Bold')
    sBD  = ST('BD', fontSize=9, leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
    sBL  = ST('BL', fontSize=9, leading=13, leftIndent=12, firstLineIndent=-9, spaceAfter=2)
    sBL2 = ST('B2', fontSize=8.5, leading=12, leftIndent=24, firstLineIndent=-9, spaceAfter=1)
    sCAP = ST('CP', fontSize=7.5, textColor=MT, leading=10, alignment=TA_CENTER,
              fontName='Helvetica-Oblique', spaceAfter=4)
    sKY  = ST('KY', fontSize=8.5, textColor=DK, leading=12, fontName='Helvetica-Bold')
    sKYR = ST('KR', fontSize=8.5, textColor=DRD, leading=12, fontName='Helvetica-Bold')
    sFT  = ST('FT', fontSize=7.5, textColor=MT, alignment=TA_CENTER, fontName='Helvetica-Oblique')
    sTD  = ST('TD', fontSize=8, leading=11, spaceAfter=1)
    sTH  = ST('TH', fontSize=8, leading=11, textColor=WH, fontName='Helvetica-Bold')
    sTIT = ST('TT', fontSize=22, textColor=WH, leading=28, fontName='Helvetica-Bold',
              alignment=TA_CENTER)
    sSUB = ST('SB', fontSize=9.5, textColor=LT, leading=13, fontName='Helvetica-Oblique',
              alignment=TA_CENTER)

    CW = W - 4*cm

    def h1(txt):
        story.append(Spacer(1, 0.2*cm))
        t = Table([[Paragraph(txt, sH1)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                               ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                               ('LEFTPADDING',(0,0),(-1,-1),8)]))
        story.append(t); story.append(Spacer(1, 0.12*cm))

    def h2(txt):
        story.append(Spacer(1, 0.1*cm))
        t = Table([[Paragraph(txt, sH2)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),MD),
                               ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
                               ('LEFTPADDING',(0,0),(-1,-1),6)]))
        story.append(t); story.append(Spacer(1, 0.08*cm))

    def pb(txt, sub=False):
        prefix = '    ◦  ' if sub else '•  '
        story.append(Paragraph(prefix + txt, sBL2 if sub else sBL))

    def bdy(txt): story.append(Paragraph(txt, sBD))

    def kyb(txt, danger=False):
        ks = sKYR if danger else sKY; bg = RD if danger else TN
        t = Table([[Paragraph(txt, ks)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),
                               ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                               ('LEFTPADDING',(0,0),(-1,-1),8),('BOX',(0,0),(-1,-1),0.5,MD)]))
        story.append(t); story.append(Spacer(1, 0.12*cm))

    def pi(n, cap='', w=13):
        path = slide(n)
        if os.path.exists(path):
            story.append(Spacer(1, 0.15*cm))
            ri = RLImage(path, width=w*cm, height=w*cm*0.65)
            ri.hAlign = 'CENTER'
            story.append(ri)
            if cap: story.append(Paragraph(cap, sCAP))
            story.append(Spacer(1, 0.1*cm))

    def dtbl(hdrs, rows, wds=None):
        n = len(hdrs)
        if not wds: wds = [17/n]*n
        data = [[Paragraph(str(h), sTH) for h in hdrs]]
        for row in rows:
            data.append([Paragraph(str(v[0] if isinstance(v, tuple) else v), sTD) for v in row])
        t = Table(data, colWidths=[w*cm for w in wds])
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),MD),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[WH,T2]),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#BBBBBB')),
            ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
            ('LEFTPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(t); story.append(Spacer(1, 0.2*cm))

    def hr(): story.append(HRFlowable(width='100%', thickness=0.5, color=LT, spaceAfter=4))

    # TITLE
    tb = Table([[Paragraph('STUDY NOTES — CHAPTER 5', sTIT)],
                [Paragraph('Thorax &amp; Rib Cage', ST('T2', fontSize=16, textColor=WH,
                  leading=22, fontName='Helvetica-Bold', alignment=TA_CENTER))],
                [Paragraph('Biological and Anatomical Aspects of Elephants', sSUB)],
                [Paragraph('Dr. Parag Nigam, PhD  ·  Wildlife Institute of India, Dehradun', sSUB)]],
               colWidths=[CW])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                             ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
                             ('LEFTPADDING',(0,0),(-1,-1),12)]))
    story.append(Spacer(1, 0.4*cm)); story.append(tb); story.append(Spacer(1, 0.3*cm))
    kyb('Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  |  Technical Support: WII Dehradun')
    kyb('CONTENTS: 5.1 Rib Count  |  5.2 Species Comparison  |  5.3 No Pleural Space  |  5.4 Diaphragm  |  5.5 Necropsy Findings')

    # ── CHAPTER 5 ─────────────────────────────────────────────────────────────
    h1('5.  Thorax & Rib Cage')
    pi(10, 'Slide 10 — Thoracic skeleton: extensive rib cage reaching to os coxae level', 13)

    h2('5.1  Rib Count & Structure')
    bdy('The elephant rib cage is one of the most expansive of any terrestrial mammal, extending posteriorly almost to the level of the os coxae (pelvis). It encloses the enormous thoracic cavity housing a 12–21 kg heart and very large lungs.')
    dtbl(['Parameter','Asian Elephant','African Elephant'],
         [('Total rib pairs','19–20','21'),
          ('Sternal ribs (direct sternum attachment)','6','6'),
          ('Asternal ribs (costal cartilage)','9','9'),
          ('Floating ribs (free)','~4–5','~6'),
          ('Rib cage extent','Reaches nearly to os coxae level','Similar'),
          ('Thoracic cavity','Very large — accommodates 12–21 kg heart','Very large')],
         wds=[5.5, 5.5, 6])
    pb('Sternum: definite keel (carina) present — unlike flat sternum of most domestic animals')
    pb('Xiphoid cartilage: articulates obliquely, bends ventrally — relevant to anaesthesia positioning')
    pb('Costal cartilages: wide; calcify with age — useful at necropsy for gross age estimation')
    pb('Thoracic vertebrae: 19–20 in Asian elephant; spinous processes elongated dorsally')

    h2('5.2  Comparison with Domestic Species')
    dtbl(['Species','Rib Pairs','Pleural Space','Breathing Mechanism'],
         [('Asian Elephant','19–20','ABSENT — pleura fused','Diaphragm ONLY'),
          ('African Elephant','21','ABSENT — pleura fused','Diaphragm ONLY'),
          ('Horse','18','Present — fluid-filled','Diaphragm + rib cage expansion'),
          ('Cattle','13','Present — fluid-filled','Diaphragm + rib cage expansion'),
          ('Dog','13','Present — fluid-filled','Diaphragm + rib cage expansion'),
          ('Human','12','Present — fluid-filled','Diaphragm + rib cage expansion')],
         wds=[3.5, 2.5, 4.5, 6.5])

    h2('5.3  No Pleural Space — Unique Respiratory Anatomy')
    bdy('Elephants are the ONLY mammals with no true pleural space. Both visceral and parietal pleura are composed of dense connective tissue and are FUSED together via loose connective tissue. Lungs are physically adhered to the chest wall and cannot collapse passively. Breathing is driven ENTIRELY by diaphragm movement.')
    pb('Both pleural layers fused — no fluid-filled cavity between them')
    pb('Lungs physically adhered to chest wall — cannot collapse passively as in other mammals')
    pb('Diaphragm unusually thick and muscular — generates ALL inspiratory pressure alone')
    pb('Resting respiratory rate: ~4–8 breaths/min; large tidal volume compensates for slow rate')
    pb('Evolutionary reason: semi-aquatic ancestry — swimming elephants breathe via trunk-snorkel; pleural fusion prevents lung compression at depth')
    pb('West JB (2001): confirmed biophysical significance for deep-water diving/swimming')

    h2('5.4  Diaphragm — Structure & Function')
    pb('PRIMARY and near-exclusive respiratory muscle in elephants')
    pb('On contraction: pulls lungs caudoventrally → increases thoracic volume → inspiration')
    pb('On relaxation: thoracic volume decreases → passive expiration')
    pb('Intercostal muscles play MINIMAL role compared to other species')
    pb('Central tendon anchored to caudal sternum border and thoracic vertebral column')
    pb('Diaphragm weight ~2–4% of total body weight — reflects enormous musculature required')

    kyb('CRITICAL DANGERS:\n'
        '1. STERNAL RECUMBENCY = FATAL — abdominal organs crush diaphragm → respiratory arrest within minutes. ALWAYS lateral recumbency (left lateral preferred).\n'
        '2. NO THORACOCENTESIS — no pleural cavity to drain; fluid in connective tissue is a clinical emergency.\n'
        '3. ANAESTHESIA: IPPV parameters differ from other large mammals — standard equine/bovine protocols NOT applicable.\n'
        '4. NECROPSY: Firm lung-chest adhesion is NORMAL — do NOT diagnose as fibrinous pleuritis.', danger=True)

    h2('5.5  Necropsy Findings — Thorax')
    pb('Lungs appear FIRMLY ATTACHED to inner chest wall — NORMAL anatomy, not adhesion from pleuropneumonia')
    pb('Any fluid between chest wall and lung surface is PATHOLOGICAL (haemorrhage, exudate, oedema)')
    pb('Heart: centrally located; BIFID (double-pointed) apex — distinctive and normal; weight 12–21 kg')
    pb('Lungs: large, soft, pink-grey; spongy texture; mild congestion common post-mortem (gravitational)')
    pb('Trachea: large-diameter; check for foreign bodies, mucus plugs, parasites (Mammomonogamus)')
    pb('Pericardium: check for haemopericardium, fibrinous deposits (EEHV in calves)')
    pb('Intercostal muscles: haemorrhage may indicate electrocution (lightning or poaching)')
    pb('Diaphragm: inspect for tears, herniation, parasitic cysts (Taenia spp.) on peritoneal surface')

    kyb('MORTALITY INVESTIGATION — THORAX CHECKLIST:\n'
        '• Measure heart weight; document bifid apex; check for EEHV haemorrhages (calves)\n'
        '• Describe lung colour, texture, consolidation, parasites, foreign bodies\n'
        '• Document any fluid between lung and chest wall (volume, colour, odour, consistency)\n'
        '• Collect tracheal swabs for respiratory pathogen PCR (EEHV, Mycobacterium)\n'
        '• Inspect diaphragm integrity — tears common in HEC fatalities\n'
        '• Intercostal muscle haemorrhage: photograph and sample for histology (lightning/electrocution)')

    hr()
    story.append(Paragraph(
        'Dr. Parag Nigam, WII Dehradun  |  Web-elaborated notes  |  June 2026  |  '
        'Training Program: Mortality Investigation of Asian Elephant, Raigarh, Chhattisgarh', sFT))

    doc.build(story)
    print(f'  ✓  {OUT_P}  ({os.path.getsize(OUT_P)//1024} KB)')


if __name__ == '__main__':
    print('Building Chapter 5 standalone notes...\n')
    print('  → Word document...')
    build_docx()
    print('  → PDF document...')
    build_pdf()
    print('\nDone.')

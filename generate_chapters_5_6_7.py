#!/usr/bin/env python3
"""
Generate standalone notes for Chapters 5, 6 & 7 of elephant anatomy notes:
  5 — Thorax & Rib Cage
  6 — Skull Morphology & Sexual Dimorphism
  7 — Age Estimation — Molar Progression
Source: Dr. Parag Nigam, WII + peer-reviewed elaboration
Outputs: Elephant_Chapters_5_6_7.docx  and  Elephant_Chapters_5_6_7.pdf
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
OUT_D  = os.path.join(DIR, 'Elephant_Chapters_5_6_7.docx')
OUT_P  = os.path.join(DIR, 'Elephant_Chapters_5_6_7.pdf')

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
    doc.core_properties.title  = 'Elephant Anatomy Notes — Chapters 5, 6 & 7'
    doc.core_properties.author = 'Dr. Parag Nigam, WII (web-elaborated)'

    # TITLE BANNER
    tbl = doc.add_table(rows=1, cols=1); tbl.style='Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(18); p.paragraph_format.space_after=Pt(18)
    r0 = p.add_run('STUDY NOTES — CHAPTERS 5, 6 & 7\n')
    r0.font.name='Calibri'; r0.font.size=Pt(9); r0.font.bold=True; r0.font.color.rgb=LIGHT
    r1 = p.add_run('Thorax & Rib Cage  ·  Skull Morphology  ·  Age Estimation\n')
    r1.font.name='Calibri'; r1.font.size=Pt(18); r1.font.bold=True; r1.font.color.rgb=WHITE
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
        '  Chapter 5 — Thorax & Rib Cage  (rib count, sternal anatomy, NO pleural space — critical danger)\n'
        '  Chapter 6 — Skull Morphology & Sexual Dimorphism  (honeycomb sinuses, frontal/lateral/mandible comparisons)\n'
        '  Chapter 7 — Age Estimation — Molar Progression  (M1–M6 table, lamellae counting, forensic ageing rules)')
    page_break(doc)

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
    bullet(doc, 'Costal cartilages: wide, calcify with age; relevant to ageing at necropsy')
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
    bullet(doc, 'West JB (2001): confirmed the biophysical significance of this arrangement for deep-water breathing during swimming')

    sec2(doc, '5.4  Diaphragm — Structure & Function')
    bullet(doc, 'Diaphragm is the PRIMARY and near-exclusive respiratory muscle in elephants')
    bullet(doc, 'Much thicker and more muscular than in other large mammals')
    bullet(doc, 'On contraction: pulls lungs downward and posteriorly (caudoventrally), increasing thoracic volume → inspiration')
    bullet(doc, 'On relaxation: thoracic volume decreases → passive expiration')
    bullet(doc, 'Accessory respiratory muscles (intercostals) play a MINIMAL role compared to other species')
    bullet(doc, 'Resting respiratory rate: ~4–8 breaths per minute (slower than most mammals of similar metabolic rate)')
    bullet(doc, 'Tidal volume: very large, compensating for slow rate')

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
        'tissue. Standard equine or bovine IPPV protocols are NOT directly applicable.',
        danger=True)

    sec2(doc, '5.5  Necropsy Findings — Thorax')
    bullet(doc, 'On opening the chest wall: lungs appear firmly attached to the inner chest wall surface — this is NORMAL anatomy, not adhesion from pleuropneumonia')
    bullet(doc, 'No fluid should be present in the "pleural space" — any fluid collection between chest wall and lung surface is pathological (haemorrhage, exudate, oedema)')
    bullet(doc, 'Heart: positioned centrally in the thorax; apex is BIFID (double-pointed) — distinctive and normal; weight 12–21 kg')
    bullet(doc, 'Lungs: large, soft, pink-grey; spongy texture; may show mild congestion post-mortem (gravitational)')
    bullet(doc, 'Trachea: large-diameter; check for foreign bodies, mucus plugs, parasites (Mammomonogamus)')
    keybox(doc, 'NECROPSY NOTE: Never mistake the normal firm lung-wall adhesion for pathological pleuritis or fibrinous pleurisy. The adhesion is present in ALL elephants — it is the normal anatomical state, not a disease finding.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # CHAPTER 6: SKULL
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '6.  Skull Morphology & Sexual Dimorphism')
    img(doc, 11, 'Slide 11 — Skull: Male vs Female (Frontal view) with labelled anatomy', 14)
    img(doc, 12, 'Slide 12 — Skull: Lateral view, mandible comparison and photograph', 14)
    img(doc, 13, 'Slide 13 — Skull photographs: male (left) vs female (right)', 14)

    sec2(doc, '6.1  Skull Architecture — General Features')
    para(doc,
        'The elephant skull is one of the most architecturally distinctive in the animal kingdom. '
        'Its imposing external size is largely an illusion created by a massive internal network '
        'of air sinuses (diploë) — a honeycomb-like trabecular structure of bone that reduces skull '
        'weight while maintaining structural strength. This engineering solution is essential for '
        'supporting the weight of the long trunk, heavy tusks, and large mandible without overloading '
        'the cervical vertebrae and neck musculature.',
        size=9.5, space_after=5)
    bullet(doc, 'Diploic (honeycomb) sinuses: massive air-filled trabecular network in the frontal and parietal bones — give the skull its characteristic domed appearance')
    bullet(doc, 'The actual BRAIN CASE is relatively small and positioned posteriorly within the skull mass — the brain accounts for only a small fraction of apparent head size')
    bullet(doc, 'Skull bones present: interparietal, parietal, frontal, nasal, lacrimal, maxilla, premaxilla, temporal, occipital bones, mandible')
    bullet(doc, 'Incisive fossa: deep socket in the premaxilla bone — houses the base (alveolus / root) of the tusks; 1/3 of tusk length is buried here')
    bullet(doc, 'Infraorbital foramen: located on the dorsal skull surface below the orbit — larger than in most mammals')
    bullet(doc, 'Temporal fossa: large and deep — accommodates the powerful temporal muscles used for mastication')

    sec2(doc, '6.2  Comparison of Skull Regions — Functional Anatomy')
    dtable(doc,
        ['Skull Region', 'Structure', 'Function / Clinical Relevance'],
        [('Frontal bone','Filled with extensive diploic sinuses','Lightweight structural dome; NOT an indicator of brain size'),
         ('Premaxilla','Bears the incisive fossa (tusk alveolus)','Deep socket for tusk root — 1/3 of tusk length here; enlarged in males'),
         ('Temporal bone','Temporal fossa for temporal muscle origin; temporal gland overlies it','Temporal gland between eye and ear; musth secretion exits via duct here'),
         ('Occipital bone','Posterior skull; occipital condyles articulate with atlas (C1)','Occipital bosses (enlarged in older males) — sex determination feature'),
         ('Nasal bones','Short, posterior-set; external nares high on skull','Trunks attach at nares; high placement allows trunk flexibility'),
         ('Mandible','Lower jaw; symphysis (chin region) sexually dimorphic','Key sex determination feature — elongated in males, short/pointed in females')],
        widths=[3.5, 5, 8])

    sec2(doc, '6.3  Sexual Dimorphism — Frontal View')
    para(doc,
        'The following features are identifiable on a frontal (anterior) view of the skull and allow '
        'sex determination even from a heavily decomposed or skeletonised carcass:',
        size=9.5, space_after=4)
    dtable(doc,
        ['Feature', 'Label', 'Male Skull', 'Female Skull'],
        [('Parieto-occipital crest','A','CONCAVE / distinctly depressed along median plane of dorsal border — "saddle-shaped"','Rounded and somewhat CONVEX on dorso-median region — "dome-shaped"'),
         ('Frontal bone','B','NARROW forehead; "pinched" appearance above nares; steep lateral walls','WIDER forehead; more gradual lateral slope'),
         ('External nares','C','Well ABOVE orbit level; placed higher on skull; lateral edge slopes sharply downward','DUMB-BELL shape; less elevated; more symmetric'),
         ('Incisive fossa','D','DEEP and narrow; "scooped out" below inferior border of nares; abrupt transition','Inferior border SLOPES GENTLY into fossa; less abrupt'),
         ('Tusk alveoli (sockets)','E','LARGER and stouter sockets; tusks well-developed (may be reduced in makhna bulls)','Tusk often absent or greatly reduced alveoli; small tushes common')],
        widths=[4, 1.5, 5.5, 5.5])

    sec2(doc, '6.4  Sexual Dimorphism — Lateral View')
    dtable(doc,
        ['Feature', 'Label', 'Male Skull', 'Female Skull'],
        [('Frontal bone (profile)','F','Slightly CONCAVE forehead when viewed from the side','Gently ROUNDED forehead — smoother curve'),
         ('Temporal line / postero-medial wall','G','PROMINENT — robust temporal muscle attachment ridges clearly visible','Smooth; ridges not pronounced'),
         ('Premaxillaries','H','LARGE and well-developed; reflect large tusk root sockets','Smaller'),
         ('Parieto-occipital region','I','LARGE, swollen BOSSES on either side of occipital crest — more pronounced with age','Rounded; bosses absent or minimal'),
         ('Mandible chin (symphysis)','—','ELONGATED; drops downward; THICK and broad — projects anteriorly','THIN; SHORT and POINTED — does not project forward')],
        widths=[4.5, 1.5, 5.5, 5])

    sec2(doc, '6.5  Cranial Proportions — Quantitative Ratios')
    dtable(doc,
        ['Measurement Ratio', 'Male', 'Female', 'Clinical Use'],
        [('Occipital length : Forehead length','Greater; ~1.5–1.65','Almost equal (ratio ~1.0)','Single ratio gives reliable sex indication'),
         ('Forehead length : Total head length','Less than 0.5 (forehead <50% of head)','Greater than 0.5 (forehead >50% of head)','Measurable from skulls in any condition')],
        widths=[5.5, 3, 3, 5])

    sec2(doc, '6.6  Mandible — Detailed Comparison')
    dtable(doc,
        ['Feature', 'Male Mandible', 'Female Mandible'],
        [('Symphysis (chin) shape','Elongated, dropped downwards; thick and broad — distinct "chin" projection','Thin, short and pointed — barely projects'),
         ('Ramus (vertical part)','Tall and robust','Shorter and more gracile'),
         ('Molar tooth row length','Longer (larger M5–M6 molars)','Shorter'),
         ('Overall mass','Heavier and more robust','Lighter'),
         ('Use at necropsy','Mandible alone sufficient to sex a carcass','Reliable in animals >5 years old')],
        widths=[4.5, 6, 6])

    sec2(doc, '6.7  Age-Dependency of Sexual Dimorphism')
    bullet(doc, 'Skull sexual dimorphism is AGE-DEPENDENT — during the first two years of life, male and female skulls are nearly identical in shape')
    bullet(doc, 'Differences become progressively more pronounced as males grow: tusk alveoli enlarge, temporal muscle attachment ridges develop, occipital bosses form')
    bullet(doc, 'By age 10–15 years: male skull features reliably identifiable')
    bullet(doc, 'By age 25–30 years: full sexual dimorphism expressed; skull sex determination is straightforward')
    bullet(doc, 'Recent research (Loo AHB et al. 2024, PMC12383435): the PELVIC BONE shows the GREATEST degree of sexual dimorphism — especially overall pelvic girdle length and pubic symphysis morphology; skull is second most dimorphic')
    bullet(doc, 'Makhna bulls (tuskless males): common in Sri Lankan population, rare in India; skull shows male features in all other respects except reduced/absent tusk alveoli')

    sec2(doc, '6.8  Practical Guide to Skull-Based Sex Determination at Mortality Site')
    dtable(doc,
        ['Step', 'Action', 'Look For'],
        [('1','Identify parieto-occipital crest (top rear of skull)','Male: saddle-shaped depression on median line; Female: smooth dome'),
         ('2','Assess frontal bone width','Male: narrow "pinched" forehead above nares; Female: wider'),
         ('3','Examine incisive fossa (below trunk attachment)','Male: deep, narrow, scooped; Female: gently sloping'),
         ('4','Check tusk alveoli size','Male: large deep sockets; Female: small or absent'),
         ('5','Examine mandible chin (symphysis)','Male: elongated, drops forward, thick; Female: short, pointed'),
         ('6','Measure forehead:head length ratio','Male: <0.5; Female: >0.5'),
         ('7','Check for occipital bosses (rear of skull)','Male >10 yrs: enlarged bosses; Female: absent/minimal'),
         ('8','Record findings','Document ALL features in mortality investigation form')],
        widths=[1, 4.5, 11])

    keybox(doc,
        'MORTALITY INVESTIGATION — SKULL KEY POINTS:\n'
        '• Skull morphology alone permits DEFINITIVE SEX DETERMINATION even from a fully skeletonised '
        'or badly decomposed carcass — use this when soft tissues are absent\n'
        '• The apparent large size of the skull is mostly AIR SINUSES — do not mistake for a large brain\n'
        '• Diploic sinuses may trap putrefactive gases — be aware during incision of skull at necropsy\n'
        '• Tusk alveoli depth indicates past tusk size — document even if tusks have been removed by poachers\n'
        '• Makhna identification: male skull without tusk alveoli — confirm via other features (occipital bosses, mandible, pelvis)')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # CHAPTER 7: AGE ESTIMATION
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '7.  Age Estimation — Molar Progression')
    img(doc, 14, 'Slide 14 — Molar table for assessing age with skull cross-section', 14)

    sec2(doc, '7.1  Unique Horizontal Molar Replacement')
    para(doc,
        'Elephants possess the most unusual dental replacement mechanism of any living mammal — '
        'HORIZONTAL MOLAR PROGRESSION (anteroposterior tooth displacement). Unlike vertical tooth '
        'replacement (where new teeth erupt below the old ones and push them upward) seen in all '
        'other mammals, elephant molars develop at the BACK of the jaw and progressively move '
        'FORWARD (anteriorly) as each preceding molar wears down. The worn tooth fragments drop '
        'off from the front of the jaw as the new tooth pushes it out from behind — like a slow '
        'conveyor belt of teeth moving through the jaw across the animal\'s lifetime.',
        size=9.5, space_after=5)
    bullet(doc, 'Six molar sets (M1–M6) develop sequentially on each side of the UPPER AND LOWER jaw = 24 total molar positions')
    bullet(doc, 'At any given time: maximum 2 molars in wear simultaneously on any one side (one active, one partially replacing the front)')
    bullet(doc, 'Each succeeding molar set is LARGER, has MORE enamel plates (lamellae), and persists in use for LONGER than the preceding one')
    bullet(doc, 'This mechanism evolved in late Oligocene epoch — characterises all elephantimorphs (fossil + modern elephants)')
    bullet(doc, 'The number of enamel plates (lamellae) visible on the occlusal (chewing) surface is the PRIMARY KEY for molar identification')

    sec2(doc, '7.2  How to Examine the Molars at Necropsy')
    bullet(doc, 'Open the mouth or cut the jaw to expose the molar teeth on each side (upper and lower)')
    bullet(doc, 'Identify the ACTIVE molar (the one with the worn, flat occlusal surface currently being used for chewing)')
    bullet(doc, 'COUNT the enamel plates (lamellae) — vertical ridges of enamel running transversely across the tooth surface')
    bullet(doc, 'ASSESS DEGREE OF WEAR: the occlusal surface tilts front-to-back as anterior plates wear first and posterior plates are still developing')
    bullet(doc, 'Note whether an ERUPTING molar is visible behind the active molar — indicates transition between molar sets')
    bullet(doc, 'Document BOTH upper and lower jaw molars; record which side was examined (left/right)')

    sec2(doc, '7.3  Molar Identification & Age Table — Asian Elephant (Elephas maximus)')
    dtable(doc,
        ['Molar', 'No. of Enamel Plates (Lamellae)', 'Appearance Age', 'Replacement Age (worn out by)', 'Estimated Animal Age When in Active Use', 'Notes'],
        [('M1 (deciduous)','4','4 months','2–2.5 years','0 – 2.5 years','Deciduous; very small; worn rapidly; first to drop off'),
         ('M2 (deciduous)','8','6 months','~6 years','6 months – 6 years','Still a milk tooth; may overlap with M1 in early life'),
         ('M3','12','3 years','~12 years','3 – 12 years','First "permanent-like" molar; noticeably larger than M2'),
         ('M4','12 (WIDER plates)','8 years','~25 years','8 – 25 years','Same plate count as M3 but WIDER lamellae — key distinguishing feature'),
         ('M5','16','20 years','50–60 years','20 – 50/60 years','Longest period of use; present during prime adulthood'),
         ('M6 (last)','24','~40 years','Death (never replaced)','40 years – end of life','Final molar; when exhausted → starvation → death')],
        widths=[1.5, 3.5, 2.5, 3.5, 4, 2.5])

    sec2(doc, '7.4  Comparison: Asian vs African Elephant Molar Timeline')
    dtable(doc,
        ['Molar', 'Asian Elephant — Replacement Age', 'African Elephant — Replacement Age', 'Key Difference'],
        [('M1','2–2.5 years','2–3 years','Similar'),
         ('M2','~6 years','~5 years','Similar'),
         ('M3','~12 years','~10 years','Slightly longer in Asian'),
         ('M4','~25 years','~22 years','Slightly longer in Asian'),
         ('M5','50–60 years','~40 years','MAJOR difference — Asian M5 lasts longer'),
         ('M6','Life long (60–70+ yrs)','~47 years','African elephants die of M6 exhaustion ~47 yrs; Asian ~65–70 yrs')],
        widths=[2, 4, 4, 6.5])

    sec2(doc, '7.5  Forensic Age Assessment Protocol — Step by Step')
    dtable(doc,
        ['Step', 'Action', 'Interpretation'],
        [('1','Identify which molar is in active wear (flat occlusal surface, forward in jaw)','Gives molar number; cross-check with lamellae count'),
         ('2','Count enamel plates (lamellae) on the active molar','M1=4, M2=8, M3=12, M4=12w, M5=16, M6=24'),
         ('3','Distinguish M3 (12 plates) from M4 (12 wider plates)','Measure lamellae width — M4 lamellae are noticeably broader'),
         ('4','Assess wear gradient','Anterior plates flatter/more worn = tooth is in later wear stage → animal closer to upper age range for that molar'),
         ('5','Check if erupting tooth is visible behind the active molar','If yes: animal is transitioning — age is near upper end of current molar range'),
         ('6','Cross-reference with body size and other indicators','Shoulder height, temporal muscle development, skin wrinkling, tusk size'),
         ('7','Record age estimate with confidence range','Always give a range, e.g. "M5 in wear, ~50–60% worn → estimated age 35–50 years"')],
        widths=[1, 5.5, 10])

    sec2(doc, '7.6  Age Estimation from Other Anatomical Features')
    para(doc, 'While molar wear is the most reliable single indicator, several other anatomical features contribute to age estimation:', size=9.5, space_after=4)
    dtable(doc,
        ['Feature', 'Young / Juvenile', 'Middle-aged Adult', 'Old (>45 years)'],
        [('Temporal hollowing','None — full temples','Slight hollowing begins','Deep temporal depression — "sunken temples"'),
         ('Skin texture','Relatively smooth','Progressively more wrinkled','Deeply wrinkled, very dry'),
         ('Tusk size (males)','Short (<50 cm)','Medium (50–100 cm)','Long (>100 cm); sometimes broken'),
         ('Skull sexual dimorphism','Minimal','Developing','Fully expressed; occipital bosses prominent in males'),
         ('Nail / foot pad condition','Intact, even','Some wear','Cracked, uneven wear'),
         ('Body condition','Good muscling','Good','Often thin; prominent skull and hip bones')],
        widths=[4, 4, 4, 4.5])

    keybox(doc,
        'MORTALITY INVESTIGATION — AGE ESTIMATION RULES:\n\n'
        '1. ALWAYS open and examine the molars — molar wear is the MOST RELIABLE age indicator\n'
        '2. NEVER age an elephant by tusk size alone — tusk growth varies hugely between individuals\n'
        '3. Count lamellae (enamel plates) with a probe/brush after cleaning — DO NOT estimate\n'
        '4. Distinguish M3 (12 narrow plates) from M4 (12 WIDE plates) — they look similar but span very different age ranges\n'
        '5. M6 status is critical: if M6 is fully worn / absent → animal was >60 years; cause of death may be nutritional/starvation secondary to dental exhaustion\n'
        '6. Document BOTH sides of the jaw: right and left mandibular and maxillary molars\n'
        '7. Photograph the molar(s) in situ before removal — scale bar mandatory\n'
        '8. Record: molar number identified, lamellae count, estimated % of wear, presence of erupting molar behind it')
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
    sTIT = ST('TT', fontSize=18, textColor=WH, leading=24, fontName='Helvetica-Bold',
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
    tb = Table([[Paragraph('STUDY NOTES — CHAPTERS 5, 6 & 7', sTIT)],
                [Paragraph('Thorax & Rib Cage  ·  Skull Morphology & Sexual Dimorphism  ·  Age Estimation', sSUB)],
                [Paragraph('Biological and Anatomical Aspects of Elephants', sSUB)],
                [Paragraph('Dr. Parag Nigam, PhD  ·  Wildlife Institute of India, Dehradun', sSUB)]],
               colWidths=[CW])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                             ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
                             ('LEFTPADDING',(0,0),(-1,-1),12)]))
    story.append(Spacer(1, 0.4*cm)); story.append(tb); story.append(Spacer(1, 0.3*cm))
    kyb('Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  |  Technical Support: WII Dehradun')
    kyb('CONTENTS: Ch.5 — Thorax & Rib Cage  |  Ch.6 — Skull Morphology & Sexual Dimorphism  |  Ch.7 — Age Estimation')
    story.append(PageBreak())

    # ── CHAPTER 5 ─────────────────────────────────────────────────────────────
    h1('5.  Thorax & Rib Cage')
    pi(10,'Slide 10 — Thoracic skeleton: extensive rib cage reaching to os coxae level',13)

    h2('5.1  Rib Count & Structure')
    dtbl(['Parameter','Asian Elephant','African Elephant'],
         [('Total rib pairs','19–20','21'),
          ('Sternal ribs (direct sternum attachment)','6','6'),
          ('Asternal ribs (costal cartilage)','9','9'),
          ('Floating ribs (free)','~4–5','~6'),
          ('Rib cage extent','Reaches nearly to os coxae level','Similar'),
          ('Thoracic cavity','Very large — accommodates 12–21 kg heart','Very large')],
         wds=[5.5,5.5,6])
    pb('Sternum: definite keel (carina) present — unlike flat sternum of most domestic animals')
    pb('Xiphoid cartilage: articulates obliquely, bends ventrally — relevant to anaesthesia positioning')
    pb('Costal cartilages: wide; calcify with age — useful at necropsy for gross age estimation')

    h2('5.2  No Pleural Space — Unique Respiratory Anatomy')
    bdy('Elephants are the ONLY mammals with no true pleural space. Both visceral and parietal pleura are composed of dense connective tissue and are FUSED together. Lungs are physically adhered to the chest wall. Breathing is driven ENTIRELY by diaphragm movement.')
    dtbl(['Species','Rib Pairs','Pleural Space','Breathing Mechanism'],
         [('Asian Elephant','19–20','ABSENT — pleura fused','Diaphragm ONLY'),
          ('African Elephant','21','ABSENT — pleura fused','Diaphragm ONLY'),
          ('Horse','18','Present — fluid-filled','Diaphragm + rib cage expansion'),
          ('Cattle','13','Present — fluid-filled','Diaphragm + rib cage expansion'),
          ('Dog','13','Present — fluid-filled','Diaphragm + rib cage expansion')],
         wds=[4,2.5,4.5,6])
    pb('Diaphragm: unusually thick and muscular; generates all inspiratory pressure alone')
    pb('Resting respiratory rate: ~4–8 breaths/min; large tidal volume compensates')
    pb('Evolutionary reason: semi-aquatic ancestry — swimming elephants breathe via trunk-snorkel')
    pb('West JB (2001): confirmed biophysical significance for deep-water diving/swimming')

    h2('5.3  Necropsy Findings — Thorax')
    pb('Lungs appear FIRMLY ATTACHED to inner chest wall — NORMAL anatomy, not adhesion from pleuropneumonia')
    pb('Any fluid between chest wall and lung surface is PATHOLOGICAL (haemorrhage, exudate, oedema)')
    pb('Heart: centrally located; BIFID (double-pointed) apex — distinctive and normal; weight 12–21 kg')
    pb('Trachea: large-diameter; check for foreign bodies, mucus plugs, parasites (Mammomonogamus)')

    kyb('CRITICAL DANGERS:\n'
        '1. STERNAL RECUMBENCY = FATAL — abdominal organs crush diaphragm → respiratory arrest within minutes. ALWAYS lateral recumbency.\n'
        '2. NO THORACOCENTESIS — no pleural cavity to drain; fluid in connective tissue is a clinical emergency.\n'
        '3. ANAESTHESIA: IPPV parameters differ from other large mammals — standard equine/bovine protocols NOT applicable.\n'
        '4. NECROPSY: Firm lung-chest adhesion is NORMAL — do NOT diagnose as fibrinous pleuritis.', danger=True)
    story.append(PageBreak())

    # ── CHAPTER 6 ─────────────────────────────────────────────────────────────
    h1('6.  Skull Morphology & Sexual Dimorphism')
    pi(11,'Slide 11 — Skull: Male vs Female (Frontal view) with labelled anatomy',13)
    pi(12,'Slide 12 — Skull: Lateral view, mandible comparison and photograph',13)
    pi(13,'Slide 13 — Skull photographs: male (left) vs female (right)',13)

    h2('6.1  Skull Architecture')
    bdy('The elephant skull\'s imposing size is largely due to massive DIPLOIC SINUSES (honeycomb air spaces) in the frontal and parietal bones. This lightweight structure supports trunk and tusk weight without overloading the neck. The actual brain case is SMALL and positioned posteriorly.')
    pb('Incisive fossa (premaxilla): deep socket housing 1/3 of tusk length underground')
    pb('Temporal fossa: large — accommodates powerful temporal mastication muscles')
    pb('Bones present: interparietal, parietal, frontal, nasal, lacrimal, maxilla, premaxilla, temporal, occipital, mandible')

    h2('6.2  Sexual Dimorphism — Frontal View')
    dtbl(['Feature','Label','Male Skull','Female Skull'],
         [('Parieto-occipital crest','A','CONCAVE / depressed on median dorsal border — "saddle"','Rounded, CONVEX on dorso-median region — "dome"'),
          ('Frontal bone','B','NARROW; "pinched" above nares; steep lateral walls','WIDER; more gradual lateral slope'),
          ('External nares','C','HIGH above orbit; lateral edge slopes sharply down','Dumb-bell shape; less elevated'),
          ('Incisive fossa','D','DEEP, narrow, "scooped out" below inferior nares border','Slopes gently; less abrupt'),
          ('Tusk alveoli','E','LARGE, stout sockets; well-developed tusks','Small or absent alveoli; tushes or none')],
         wds=[4,1.5,5.5,6])

    h2('6.3  Sexual Dimorphism — Lateral View & Mandible')
    dtbl(['Feature','Label','Male','Female'],
         [('Frontal (profile)','F','Slightly CONCAVE','Gently ROUNDED'),
          ('Temporal line','G','PROMINENT muscle ridges','Smooth; minimal ridges'),
          ('Premaxillaries','H','LARGE','Smaller'),
          ('Parieto-occipital bosses','I','Large, SWOLLEN — prominent in older males','Absent or minimal'),
          ('Mandible symphysis (chin)','--','ELONGATED, drops forward, THICK & BROAD','SHORT, THIN and POINTED')],
         wds=[4.5,1.5,5.5,6])

    h2('6.4  Quantitative Ratios')
    dtbl(['Ratio','Male','Female'],
         [('Occipital length : Forehead length','~1.5–1.65 (greater)','~1.0 (almost equal)'),
          ('Forehead length : Total head length','<0.5 (forehead <50% of head)','> 0.5 (forehead >50% of head)')],
         wds=[7,5,5])
    pb('Dimorphism is AGE-DEPENDENT: <2 years skulls look similar in both sexes')
    pb('Full male features by age 25–30 years; tusk alveoli enlarge, bosses develop from age 10+')
    pb('Pelvic bone shows GREATER sexual dimorphism than skull (Loo et al. 2024, PMC12383435)')
    pb('Makhna (tuskless bulls): all other male skull features present EXCEPT tusk alveoli')

    h2('6.5  Mortality Investigation — Skull-Based Sex Determination')
    dtbl(['Step','Action','Result'],
         [('1','Check parieto-occipital crest (top rear)','Male: saddle; Female: dome'),
          ('2','Assess frontal width above nares','Male: narrow/pinched; Female: wider'),
          ('3','Examine incisive fossa depth','Male: deep/scooped; Female: gentle slope'),
          ('4','Check tusk alveoli size','Male: large; Female: small/absent'),
          ('5','Examine mandible chin','Male: elongated/thick; Female: short/pointed'),
          ('6','Measure forehead:head ratio','Male: <0.5; Female: >0.5'),
          ('7','Record ALL findings in mortality form','Document with photographs + scale bar')],
         wds=[1,5.5,10.5])
    kyb('SKULL KEY POINTS: Definitive sex determination from skull alone even from fully skeletonised carcass. Large skull = mostly AIR SINUSES, not brain. Document tusk alveoli depth even if tusks removed by poachers.')
    story.append(PageBreak())

    # ── CHAPTER 7 ─────────────────────────────────────────────────────────────
    h1('7.  Age Estimation — Molar Progression')
    pi(14,'Slide 14 — Molar table for assessing age with skull cross-section',13)

    h2('7.1  Horizontal Molar Replacement — Unique Proboscidean Feature')
    bdy('Elephant molars develop at the BACK of the jaw and move FORWARD as each preceding molar wears down. Worn fragments drop off from the front. Six molar sets (M1–M6), each larger and longer-lasting than the last. Maximum 2 molars in use simultaneously on any one side. Final molar (M6) is never replaced.')

    h2('7.2  Molar Identification & Age Table (Asian Elephant)')
    dtbl(['Molar','Enamel Plates (Lamellae)','Appearance Age','Worn Out By','Active Use Age Range','Notes'],
         [('M1','4','4 months','2–2.5 yrs','0–2.5 yrs','Deciduous; very small; first to drop off'),
          ('M2','8','6 months','~6 yrs','6 mths–6 yrs','Milk tooth; overlaps M1'),
          ('M3','12','3 yrs','~12 yrs','3–12 yrs','First permanent-like molar'),
          ('M4','12 (WIDER plates)','8 yrs','~25 yrs','8–25 yrs','SAME count as M3 but WIDER lamellae — key distinction'),
          ('M5','16','20 yrs','50–60 yrs','20–60 yrs','Longest in use; present during prime adulthood'),
          ('M6','24','~40 yrs','Death — never replaced','40 yrs–end of life','Final molar; exhaustion → starvation → death')],
         wds=[1.5,3.5,2.5,3.5,4,3])

    h2('7.3  Asian vs African Elephant Molar Timeline')
    dtbl(['Molar','Asian Elephant — Worn by','African Elephant — Worn by'],
         [('M5','50–60 years','~40 years'),
          ('M6 (last molar)','~65–70 years (life long)','~47 years'),
          ('Max natural lifespan','65–70 years','~47–50 years'),
          ('Death mechanism','M6 exhaustion → cannot chew → starvation','Same mechanism; earlier in African')],
         wds=[4,6.5,6.5])

    h2('7.4  Necropsy Protocol — Molar Examination')
    dtbl(['Step','Action','Interpretation'],
         [('1','Open jaw; expose molars on both sides','Identify active molar — flat occlusal surface = currently in use'),
          ('2','Count enamel plates (lamellae) with brush/probe','M1=4, M2=8, M3=12, M4=12wide, M5=16, M6=24'),
          ('3','Distinguish M3 vs M4 (both have 12 plates)','M4 lamellae are WIDER — measure width; a key distinction'),
          ('4','Assess wear gradient (front-to-back tilt)','Anterior plates more worn = tooth in later stage → age at upper end of that molar range'),
          ('5','Check for erupting molar behind active molar','Present = transitioning to next set → near upper age of current molar'),
          ('6','Photograph with scale bar before removal','Mandatory for mortality investigation records'),
          ('7','Record age estimate with range','E.g., "M5 in wear, ~60% worn → estimated age 35–50 years"')],
         wds=[1,5.5,10.5])

    h2('7.5  Additional Age Indicators')
    dtbl(['Feature','Young (<15 yrs)','Middle-aged (15–40 yrs)','Old (>45 yrs)'],
         [('Temporal hollowing','None — full temples','Slight','Deep depression — "sunken temples"'),
          ('Tusk size (male)','Short <50 cm','Medium 50–100 cm','Long >100 cm; often broken or worn'),
          ('Skin texture','Relatively smooth','Progressively wrinkled','Deeply wrinkled; very dry'),
          ('Skull sexual dimorphism','Minimal','Developing','Fully expressed; bosses prominent'),
          ('Body condition','Well-muscled','Good','Often thin; skull/hip bones prominent')],
         wds=[4.5,4,4.5,4])

    kyb('AGE ESTIMATION RULES:\n'
        '1. ALWAYS examine molars — most reliable single indicator\n'
        '2. NEVER age by tusk size alone — growth varies between individuals\n'
        '3. Count lamellae with probe AFTER cleaning — do not estimate\n'
        '4. Distinguish M3 vs M4 by lamellae WIDTH (not count)\n'
        '5. M6 fully worn/absent → animal >60 years; death may be starvation from dental exhaustion\n'
        '6. Document both sides (left/right, upper/lower) of the jaw\n'
        '7. Give age as a RANGE, not a single number: "M5 in wear, ~50–60% worn → est. age 30–45 years"')

    hr()
    story.append(Paragraph(
        'Dr. Parag Nigam, WII Dehradun  |  Web-elaborated notes  |  June 2026  |  '
        'Training Program: Mortality Investigation of Asian Elephant, Raigarh, Chhattisgarh', sFT))

    doc.build(story)
    print(f'  ✓  {OUT_P}  ({os.path.getsize(OUT_P)//1024} KB)')


if __name__ == '__main__':
    print('Building Chapters 5, 6 & 7 standalone notes...\n')
    print('  → Word document...')
    build_docx()
    print('  → PDF document...')
    build_pdf()
    print('\nDone.')

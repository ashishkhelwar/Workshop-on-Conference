#!/usr/bin/env python3
"""
Generate Notes on Biological and Anatomical Aspects of Elephants
Source: Basic_elephant_PPT.pdf by Dr. Parag Nigam, WII
Outputs: Elephant_Anatomy_Notes_2026.docx and Elephant_Anatomy_Notes_2026.pdf
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, Image as RLImage,
                                 KeepTogether, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

DIR    = '/home/user/Workshop-on-Conference'
SLIDES = '/home/user/Workshop-on-Conference/slide_images/crops'
OUT_D  = os.path.join(DIR, 'Elephant_Anatomy_Notes_2026.docx')
OUT_P  = os.path.join(DIR, 'Elephant_Anatomy_Notes_2026.pdf')

# ── Palette ───────────────────────────────────────────────────────────────────
DARK   = RGBColor(0x1B, 0x43, 0x32)
MED    = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT  = RGBColor(0x52, 0xB7, 0x88)
TINT   = RGBColor(0xD8, 0xF3, 0xDC)
TINT2  = RGBColor(0xEA, 0xF7, 0xEE)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
MUTED  = RGBColor(0x55, 0x55, 0x55)
ORANGE = RGBColor(0xD4, 0x6B, 0x08)

def rgb_hex(rgb): return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'

def slide(n): return os.path.join(SLIDES, f'slide_{n:02d}.png')

# ═══════════════════════════════════════════════════════════════════════════════
# WORD DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════════

def shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(0)

def section_header(doc, text, level=1):
    if level == 1:
        h = doc.add_paragraph(text)
        h.style = doc.styles['Heading 1']
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after  = Pt(4)
        tbl = doc.add_table(rows=1, cols=1)
        tbl.style = 'Table Grid'
        cell = tbl.rows[0].cells[0]
        shade_cell(cell, rgb_hex(DARK))
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after  = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Calibri'; run.font.size = Pt(14); run.font.bold = True
        run.font.color.rgb = WHITE
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
    else:
        h = doc.add_paragraph(text)
        h.style = doc.styles['Heading 2']
        h.paragraph_format.space_before = Pt(6)
        h.paragraph_format.space_after  = Pt(2)
        tbl = doc.add_table(rows=1, cols=1)
        tbl.style = 'Table Grid'
        cell = tbl.rows[0].cells[0]
        shade_cell(cell, rgb_hex(MED))
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after  = Pt(3)
        run = p.add_run(text)
        run.font.name = 'Calibri'; run.font.size = Pt(11); run.font.bold = True
        run.font.color.rgb = WHITE
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

def para(doc, text, size=9.5, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(size); run.font.bold = bold
    run.font.italic = italic; run.font.color.rgb = color or BLACK
    return p

def bullet(doc, text, level=0, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent   = Cm(0.5 + level * 0.5)
    p.paragraph_format.first_line_indent = Cm(-0.3)
    p.paragraph_format.space_after   = Pt(2)
    run = p.add_run(f'•  {text}')
    run.font.name = 'Calibri'; run.font.size = Pt(size); run.font.color.rgb = BLACK

def add_slide_image(doc, slide_num, caption='', width_cm=15):
    path = slide(slide_num)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after  = Pt(2)
        run = p.add_run()
        run.add_picture(path, width=Cm(width_cm))
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(6)
        cr = cp.add_run(caption)
        cr.font.name = 'Calibri'; cr.font.size = Pt(8); cr.font.italic = True
        cr.font.color.rgb = MUTED

def keybox(doc, text, color=None):
    bg = color or rgb_hex(TINT)
    fg = DARK
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, bg)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(9); run.font.bold = True
    run.font.color.rgb = fg
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def dtable(doc, headers, rows, widths=None):
    n = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n)
    tbl.style = 'Table Grid'
    for i, h in enumerate(headers):
        shade_cell(tbl.rows[0].cells[i], rgb_hex(MED))
        p = tbl.rows[0].cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(str(h))
        run.font.name = 'Calibri'; run.font.size = Pt(8.5); run.font.bold = True
        run.font.color.rgb = WHITE
    for ri, row in enumerate(rows):
        bg = rgb_hex(TINT2) if ri % 2 else 'FFFFFF'
        for ci, val in enumerate(row):
            shade_cell(tbl.rows[ri+1].cells[ci], bg)
            p = tbl.rows[ri+1].cells[ci].paragraphs[0]
            if isinstance(val, tuple):
                txt, bld = val
                run = p.add_run(str(txt)); run.font.bold = bld
            else:
                run = p.add_run(str(val))
            run.font.name = 'Calibri'; run.font.size = Pt(8.5); run.font.color.rgb = BLACK
    if widths:
        for row in tbl.rows:
            for ci, cell in enumerate(row.cells):
                if ci < len(widths):
                    cell.width = Cm(widths[ci])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def build_docx():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width   = Cm(21); sec.page_height  = Cm(29.7)
    sec.left_margin  = sec.right_margin  = Cm(2.0)
    sec.top_margin   = sec.bottom_margin = Cm(1.8)
    doc.core_properties.title  = 'Biological and Anatomical Aspects of Elephants — Notes'
    doc.core_properties.author = 'Dr. Parag Nigam, WII Dehradun'

    # ── TITLE PAGE ─────────────────────────────────────────────────────────────
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(16)
    r0 = p.add_run('STUDY NOTES\n')
    r0.font.name='Calibri'; r0.font.size=Pt(9); r0.font.bold=True; r0.font.color.rgb=LIGHT
    r1 = p.add_run('Biological and Anatomical Aspects of Elephants\n')
    r1.font.name='Calibri'; r1.font.size=Pt(20); r1.font.bold=True; r1.font.color.rgb=WHITE
    r2 = p.add_run('Dr. Parag Nigam, PhD  ·  Wildlife Institute of India, Dehradun')
    r2.font.name='Calibri'; r2.font.size=Pt(10); r2.font.italic=True; r2.font.color.rgb=TINT
    doc.add_paragraph()

    add_slide_image(doc, 1, 'Slide 1 — Title slide', width_cm=14)
    add_slide_image(doc, 2, 'Slide 2 — The Asian elephant: largest terrestrial mammal', width_cm=14)

    keybox(doc,
        'Dr. Parag Nigam, PhD | Head, Dept. of Wildlife Health Management, Wildlife Institute of India\n'
        'Training Program: "Essentials for Mortality Investigation of Asian Elephant"\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh, Chhattisgarh')

    page_break(doc)

    # ── SECTION 1: TAXONOMY & OVERVIEW ─────────────────────────────────────────
    section_header(doc, '1. Taxonomy & Overview')

    add_slide_image(doc, 3, 'Slide 3 — Three species of elephants: Savanna, Forest and Asian', width_cm=14)
    add_slide_image(doc, 4, 'Slide 4 — Knowing Elephants: key facts', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '1.1  Classification & Species', level=2)
    bullet(doc, 'Family: Proboscidae')
    bullet(doc, 'Three living species:')
    bullet(doc, 'Savanna / Bush Elephant (Loxodonta africana) — largest, found in sub-Saharan Africa', level=1)
    bullet(doc, 'African Forest Elephant (Loxodonta cyclotis) — smaller, central African rainforests', level=1)
    bullet(doc, 'Asian Elephant (Elephas maximus) — India, Sri Lanka & SE Asia', level=1)
    bullet(doc, 'Asian elephant has FIVE sub-strains: Indian, Burmese, Ceylonese, Sumatran, Malaysian')
    doc.add_paragraph()

    section_header(doc, '1.2  Body Size & Weight', level=2)
    dtable(doc,
        ['Parameter', 'Bull (Male)', 'Cow (Female)'],
        [
            ('Height', '9 ft / 2.7 m', '7.5 ft / 2.3 m'),
            ('Weight', '3–5 tons', '2.3–4.5 tons'),
            ('Calf at birth — Height', '90–100 cm', '90–100 cm'),
            ('Calf at birth — Weight', '80–100 kg', '80–100 kg'),
        ],
        widths=[5, 5, 5]
    )

    section_header(doc, '1.3  Senses & Behaviour', level=2)
    bullet(doc, 'Poor eyesight; highly dependent on senses of smell and hearing')
    bullet(doc, 'Can perceive sound frequencies inaudible to the human ear (infrasound communication)')
    bullet(doc, 'Distribution limited to South Asia and South-East Asia (see map — Slide 4)')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 2: THE TRUNK ───────────────────────────────────────────────────
    section_header(doc, '2. The Trunk (Proboscis)')
    add_slide_image(doc, 5, 'Slide 5 — The trunk: longest nose in the animal kingdom', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '2.1  Structure', level=2)
    bullet(doc, 'The trunk is the elongated upper lip of the elephant')
    bullet(doc, 'Composed of approximately 6,000 circular and longitudinal muscles')
    bullet(doc, 'Belongs to Order Proboscidae (defines the order)')
    bullet(doc, 'Has NO bones — entirely muscular structure')
    doc.add_paragraph()

    section_header(doc, '2.2  Function', level=2)
    bullet(doc, 'Used in multiple ways equivalent to a human hand')
    bullet(doc, 'Finger-like process at tip of trunk combined with suction action')
    bullet(doc, 'Can pick up objects as small as a pin')
    bullet(doc, 'Used for breathing, smelling, drinking, bathing, grasping food and social interaction')
    keybox(doc, 'KEY FACT: The trunk is the most versatile appendage in the animal kingdom — 6,000+ muscles, no bones.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 3: SKELETON ────────────────────────────────────────────────────
    section_header(doc, '3. Skeletal System')
    add_slide_image(doc, 6, 'Slide 6 — Appendicular skeleton, 18 nails and foot anatomy', width_cm=14)
    add_slide_image(doc, 7, 'Slide 7 — Full articulated skeleton on display', width_cm=14)
    add_slide_image(doc, 8, 'Slide 8 — Bone structure: Elephant vs Horse cross section', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '3.1  General Features', level=2)
    bullet(doc, 'Appendicular skeleton — limbs adapted for supporting enormous body weight')
    bullet(doc, 'Total of 18 nails (digitigrade stance)')
    bullet(doc, 'Limbs function as pillars — bones aligned vertically under the body')

    section_header(doc, '3.2  Bone Microstructure', level=2)
    bullet(doc, 'Most long bones do NOT have hollow marrow cavities')
    bullet(doc, 'Filled with spongy bone or red marrow instead of hollow space')
    bullet(doc, 'Thickness of compact bone is LESS than that of other domestic animals')
    bullet(doc, 'Compensated by spongy bone inside — simultaneously provides more haemopoietic tissue')
    bullet(doc, 'Evolutionary advantage: reduces total skeletal weight while reinforcing haemopoietic tissue production')
    keybox(doc, 'NOTE: Compact bone thinner than horse/cattle — do not mistake for pathology during necropsy.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 4: FOOT ANATOMY ───────────────────────────────────────────────
    section_header(doc, '4. Foot Anatomy')
    add_slide_image(doc, 9, 'Slide 9 — Foot skeletal anatomy: forefoot (Prepollex) and hindfoot (Prehallux)', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '4.1  Structure', level=2)
    bullet(doc, 'Forefoot: Radio-Ulna → Carpal → Metacarpal → Phalanges (Digits I, II, III)')
    bullet(doc, 'Hindfoot: Tibia-Fibula → Tarsal → Metatarsal → Phalanges (Digits I, II, III)')
    bullet(doc, 'Elephant feet have variable skeletal foot anatomy with 5 digits (phalangeal bones)')
    bullet(doc, 'Sesamoid bone acts as a SIXTH digit for weight distribution')
    bullet(doc, 'Prepollex (forefoot) and Prehallux (hindfoot) — extra weight-bearing bony processes')

    keybox(doc, 'The foot\'s unique sesamoid "sixth digit" distributes weight across a wide surface — critical for supporting 3–5 tons.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 5: RIB CAGE ───────────────────────────────────────────────────
    section_header(doc, '5. Thorax & Rib Cage')
    add_slide_image(doc, 10, 'Slide 10 — Thoracic skeleton showing rib cage structure', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '5.1  Rib Count & Structure', level=2)
    bullet(doc, '19 or 20 pairs of ribs:')
    bullet(doc, '6 sternal ribs (attached to sternum)', level=1)
    bullet(doc, '9 asternal ribs (attached to cartilage)', level=1)
    bullet(doc, '9 floating ribs (free)', level=1)
    bullet(doc, 'Extensive rib cage almost reaching the level of os coxae — indicates VERY LARGE thoracic cavity')
    bullet(doc, 'Sternum has a definite keel present')
    bullet(doc, 'Articulates obliquely — xiphoid cartilage bends ventrally')

    keybox(doc, 'CRITICAL: The xiphoid arrangement prevents sternal recumbency. An accidental fall in sternal position is FATAL for an elephant — lungs are crushed by body weight. Always keep anesthetized/down elephants in lateral recumbency.', color='FAE0D8')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 6: SKULL ──────────────────────────────────────────────────────
    section_header(doc, '6. Skull Morphology & Sexual Dimorphism')
    add_slide_image(doc, 11, 'Slide 11 — Skull: Male vs Female comparison (Frontal view)', width_cm=14)
    add_slide_image(doc, 12, 'Slide 12 — Skull: Lateral view and Mandible comparison', width_cm=14)
    add_slide_image(doc, 13, 'Slide 13 — Skull photographs: male (left) vs female (right)', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '6.1  Frontal View Differences', level=2)
    dtable(doc,
        ['Feature', 'Male Skull', 'Female Skull'],
        [
            ('Parieto-occipital crest', 'Concave / distinctly depressed on median plane of dorsal border', 'Rounded and somewhat convex on dorso-median region'),
            ('Frontal bone', 'Narrow forehead, "pinched" above nares', 'Wider forehead'),
            ('External nares', 'Well above orbit, placed higher, lateral edge sloping down', 'Dumb-bell shape'),
            ('Incisive fossa', 'Deep and narrow, "Scooped out" below inferior nares border', 'Inferior border slopes gently into fossa'),
            ('Tusk alveoli', 'Larger and stouter; incisors larger, though may be reduced in makhna', 'Tusk often absent or with reduced alveoli'),
        ],
        widths=[4.5, 5.5, 5.5]
    )

    section_header(doc, '6.2  Lateral View Differences', level=2)
    dtable(doc,
        ['Feature', 'Male Skull', 'Female Skull'],
        [
            ('Frontal', 'Slightly concave forehead', 'Rounded forehead'),
            ('Temporal line (post. medial wall)', 'Present with robust muscle attachment', 'Smooth and not so pronounced'),
            ('Premaxillaries', 'Large', 'Smaller'),
            ('Parieto-occipital region', 'Large, swollen bosses', 'Rounded'),
        ],
        widths=[4.5, 5.5, 5.5]
    )

    section_header(doc, '6.3  Mandible', level=2)
    dtable(doc,
        ['Feature', 'Male Skull', 'Female Skull'],
        [
            ('Chin (median projection from anterior end of mandibular symphysis)', 'Elongated, dropped downwards and somewhat thick and broad', 'Thin, short and pointed'),
        ],
        widths=[5, 5, 5.5]
    )

    section_header(doc, '6.4  Other Measurements', level=2)
    dtable(doc,
        ['Measurement', 'Male', 'Female'],
        [
            ('Ratio of occipital length and forehead length', 'Greater than female; around 1.5–1.65', 'Almost equal'),
            ('Ratio of forehead length to head length', 'Less than half head length', 'Greater than half head length'),
        ],
        widths=[6, 5, 4.5]
    )
    keybox(doc, 'PRACTICAL USE: Skull morphology allows sex determination of a carcass even when soft tissue is absent — important for mortality investigations.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 7: AGE ESTIMATION ─────────────────────────────────────────────
    section_header(doc, '7. Age Estimation')
    add_slide_image(doc, 14, 'Slide 14 — Molar progression table for assessing age', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '7.1  Molar Progression Method', level=2)
    para(doc,
        'Elephants have a unique horizontal molar replacement system — molars progress forward in the jaw '
        'and are replaced sequentially (M1 to M6). Age can be estimated by examining which molar set is '
        'currently in use.',
        size=9.5, space_after=6)

    dtable(doc,
        ['Molar Set', 'Number of Plates', 'Appearance Age', 'Replacement Age'],
        [
            ('I',   '4',              '4 months',  '2–2.5 years'),
            ('II',  '8',              '6 months',  '6 years'),
            ('III', '12',             '3 years',   '12 years'),
            ('IV',  '12 (more wide)', '8 years',   '25 years'),
            ('V',   '16',             '20 years',  '50–60 years'),
            ('VI',  '24',             '40 years',  'Life long'),
        ],
        widths=[2.5, 3.5, 4.5, 5]
    )

    keybox(doc, 'RULE: When M6 is worn out (~60–70 yrs), the elephant can no longer chew food efficiently and starves to death — the biological clock of elephant longevity.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 8: DENTITION ──────────────────────────────────────────────────
    section_header(doc, '8. Dentition — Tusks & Molars')
    add_slide_image(doc, 15, 'Slide 15 — Dentition: tusks (incisors), molar progression and cross sections', width_cm=14)
    add_slide_image(doc, 16, 'Slide 16 — Tusk anatomy: cross section showing cementum, dentine, pulp and enamel', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '8.1  Dental Formula', level=2)
    bullet(doc, 'Pair of Incisors (Tusks) — upper incisors only')
    bullet(doc, '6 sets of molars (M1–M6), one active at a time per jaw quadrant')
    bullet(doc, 'No canines or premolars')

    section_header(doc, '8.2  Tusks', level=2)
    bullet(doc, 'Upper incisors that have undergone exaggerated evolutionary development')
    bullet(doc, 'Only 2/3rd of total tusk length is visible externally — 1/3rd embedded in skull')
    bullet(doc, 'Tusk structure (outside to inside):')
    bullet(doc, 'Enamel — tip only', level=1)
    bullet(doc, 'Cementum — outer layer', level=1)
    bullet(doc, 'Dentine — bulk of the tusk (makes up ~90% of volume)', level=1)
    bullet(doc, 'Tusk pulp cavity — inner core where ivory is formed as tusk grows', level=1)
    bullet(doc, 'Ivory properties:')
    bullet(doc, 'Bulk of tusks made of DENTINE — not enamel', level=1)
    bullet(doc, 'Not brittle (unlike enamel)', level=1)
    bullet(doc, 'Creamy in colour', level=1)
    bullet(doc, 'Has characteristic Schreger lines (cross-hatched pattern) — diagnostic of true ivory')

    section_header(doc, '8.3  Schreger Lines', level=2)
    add_slide_image(doc, 20, 'Slide 20 — Schreger lines visible in ivory cross-section', width_cm=14)
    bullet(doc, 'Distinctive cross-hatching visible on cut surface of ivory')
    bullet(doc, 'Unique to proboscideans — used forensically to identify real elephant ivory')
    bullet(doc, 'Pattern results from the architecture of dentinal tubules in the dentine matrix')
    keybox(doc, 'FORENSIC: Schreger lines confirm identity of ivory even in worked/carved pieces — legally important under CITES and Wildlife Protection Act.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 9: SKIN & GLANDS ──────────────────────────────────────────────
    section_header(doc, '9. Skin, Eyes & Integumentary Glands')
    add_slide_image(doc, 17, 'Slide 17 — Skin texture, mammary glands and temporal gland', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '9.1  Eyes', level=2)
    bullet(doc, 'Eyes have NO lacrimal apparatus (no conventional tear glands)')
    bullet(doc, 'Moisturization provided by Harderian glands')
    bullet(doc, 'Robust nictitating membrane (third eyelid) present')
    bullet(doc, 'Poor visual acuity — compensated by excellent olfaction and hearing')

    section_header(doc, '9.2  Mammary Glands', level=2)
    bullet(doc, 'Elephants have TWO pectoral mammary glands (located on the chest between forelegs)')
    bullet(doc, 'Unique among mammals — most other mammals have inguinal/abdominal mammary glands')
    bullet(doc, 'Lactation can last up to 4–5 years')

    section_header(doc, '9.3  Temporal Gland', level=2)
    bullet(doc, 'Located between the eye and ear on both sides of the head')
    bullet(doc, 'Secretes musth fluid in bulls during musth (heightened testosterone phase)')
    bullet(doc, 'Both sexes have temporal glands; secretion more pronounced during musth in males')

    section_header(doc, '9.4  Skin & Sweat Glands', level=2)
    bullet(doc, 'Lack typical skin sweat glands')
    bullet(doc, 'Thermoregulation achieved via:')
    bullet(doc, 'Ear flapping — large surface area with blood vessels for heat dissipation', level=1)
    bullet(doc, 'Water/mud bathing', level=1)
    bullet(doc, 'Skin: thick, deeply wrinkled — wrinkles increase surface area for cooling', level=1)
    keybox(doc, 'NOTE: Absence of sweat glands means elephants are highly vulnerable to heat stress — critical consideration during capture and transport operations.')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 10: INTERNAL ORGANS ───────────────────────────────────────────
    section_header(doc, '10. Internal Organs')
    add_slide_image(doc, 18, 'Slide 18 — Full internal organ diagram (labelled)', width_cm=14)
    add_slide_image(doc, 19, 'Slide 19 — Internal organ details: heart, reproductive system, lungs', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '10.1  Digestive System', level=2)
    bullet(doc, 'Monogastric hindgut fermentation system')
    bullet(doc, 'Total bowel length up to 35 metres')
    bullet(doc, 'Most of the ingesta pass UNDIGESTED (poor digestive efficiency ~40%)')
    bullet(doc, 'Liver has NO gall bladder')
    bullet(doc, 'Stomach is simple and single-chambered')

    section_header(doc, '10.2  Urinary System', level=2)
    bullet(doc, 'Multipyramidal smooth kidneys (lobulated — similar to cetaceans)')
    bullet(doc, 'Small urinary bladder relative to body size')

    section_header(doc, '10.3  Reproductive System', level=2)
    bullet(doc, 'Testes are INTRAABDOMINAL (do not descend into scrotum)')
    bullet(doc, 'No external scrotum — testes located near kidneys')
    bullet(doc, 'Female: bicornuate uterus; vaginal opening ventral, far forward')

    section_header(doc, '10.4  Cardiovascular System', level=2)
    bullet(doc, 'Heart weight: 12–21 kg')
    bullet(doc, 'Heart displays a DOUBLE-POINTED apex (bifid apex) — unique among mammals')
    bullet(doc, 'Located centrally in thoracic cavity')

    section_header(doc, '10.5  Nervous System', level=2)
    bullet(doc, 'Brain weight: 3.5–5.5 kg (largest land animal brain)')
    bullet(doc, 'Gyrated (folded) brain with prominent temporal lobes')
    bullet(doc, 'High cognitive ability — tool use, self-recognition, mourning behaviour documented')

    section_header(doc, '10.6  Respiratory System', level=2)
    bullet(doc, 'Connective tissue (no pleural cavity) — the thick visceral pleura is adhered to the parietal pleura')
    bullet(doc, 'Lungs are attached to the diaphragm')
    bullet(doc, 'Breathing relies mainly on MOVEMENT OF THE DIAPHRAGM (not rib expansion)')
    keybox(doc, 'CRITICAL for anaesthesia: Lungs are glued to chest wall — no true pleural space. Thoracic wounds cause rapid respiratory compromise. In sternal recumbency, the weight of abdominal organs crushes lungs → FATAL.', color='FAE0D8')
    keybox(doc, 'KEY FACTS SUMMARY:\n'
        '• No gall bladder  •  Intraabdominal testes  •  Bifid heart apex\n'
        '• No pleural cavity  •  Hindgut fermentation  •  35 m bowel\n'
        '• Multipyramidal kidneys  •  Breathing via diaphragm only')
    doc.add_paragraph()

    page_break(doc)

    # ── SECTION 11: HEIGHT & WEIGHT ESTIMATION ────────────────────────────────
    section_header(doc, '11. Field Estimation of Height & Weight')
    add_slide_image(doc, 21, 'Slide 21 — Assessing height using front foot circumference', width_cm=14)
    add_slide_image(doc, 22, 'Slide 22 — Assessing weight using body girth measurements', width_cm=14)
    doc.add_paragraph()

    section_header(doc, '11.1  Height Estimation', level=2)
    bullet(doc, 'Simple field formula:')
    bullet(doc, 'Height = 2 × Circumference of the front foot', level=1)
    bullet(doc, 'Measure the circumference of the front footprint at ground level')
    bullet(doc, 'Quick method usable at a mortality site even without the animal present (footprints in soil)')

    section_header(doc, '11.2  Weight Estimation Formulae', level=2)
    dtable(doc,
        ['Formula', 'Parameters', 'Notes'],
        [
            ('Weight (kg) = 12.8 (G + Ng) − 4281',
             'G = Chest girth (cm)\nNg = Neck girth (cm)',
             'General formula'),
            ('Weight (kg) = 18 (HG) − 3336',
             'HG = Heart girth (cm)',
             'Male specific'),
            ('Weight (kg) = 15 (HG) − 2562',
             'HG = Heart girth (cm)',
             'Female specific'),
            ('Weight (kg) = 1010 + 0.036 (L × G)',
             'L = Body length, base of forehead to base of tail (cm)\nG = Chest girth just caudal to elbow (cm)',
             'Alternative formula'),
        ],
        widths=[5, 6, 4.5]
    )

    bullet(doc, 'Heart girth (HG) — measured just caudal to the elbow')
    bullet(doc, 'Chest girth (G) — same as heart girth in some formulae')
    bullet(doc, 'Neck girth (Ng) — measured at mid-neck')
    keybox(doc, 'FIELD USE: Height and weight data are MANDATORY fields in elephant mortality forms — use front-foot circumference for height and heart-girth for weight estimate even from a carcass.')
    doc.add_paragraph()

    # ── REFERENCES ─────────────────────────────────────────────────────────────
    section_header(doc, '12. Key References & Notes')
    bullet(doc, 'Nigam P. (2026). Biological and Anatomical Aspects of Elephants. Training Program: Essentials for Mortality Investigation of Asian Elephant. WII, Dehradun.')
    bullet(doc, 'Laws RM (1966). Age criteria for the African elephant. East African Wildlife Journal 4:1–37.')
    bullet(doc, 'Shoshani J & Tassy P (1996). The Proboscidea: Evolution and Palaeoecology of Elephants and their Relatives. Oxford University Press.')
    bullet(doc, 'Sukumar R (2003). The Living Elephants: Evolutionary Ecology, Behaviour, and Conservation. Oxford University Press.')
    doc.add_paragraph()

    para(doc, 'Notes compiled from PPT slides by Dr. Parag Nigam, PhD — Wildlife Institute of India',
         size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, 'Training Program: Essentials for Mortality Investigation of Asian Elephant  |  5–6 June 2026, Raigarh',
         size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(OUT_D)
    size_kb = os.path.getsize(OUT_D) // 1024
    print(f'  ✓  {OUT_D}  ({size_kb} KB)')


# ═══════════════════════════════════════════════════════════════════════════════
# PDF DOCUMENT (ReportLab)
# ═══════════════════════════════════════════════════════════════════════════════

def build_pdf():
    W, H = A4
    doc = SimpleDocTemplate(OUT_P, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.8*cm, bottomMargin=1.8*cm)
    styles = getSampleStyleSheet()
    story  = []

    DARK_RL   = colors.HexColor('#1B4332')
    MED_RL    = colors.HexColor('#2D6A4F')
    LIGHT_RL  = colors.HexColor('#52B788')
    TINT_RL   = colors.HexColor('#D8F3DC')
    TINT2_RL  = colors.HexColor('#EAF7EE')
    RED_RL    = colors.HexColor('#FAE0D8')
    WHITE_RL  = colors.white
    BLACK_RL  = colors.HexColor('#1A1A1A')
    MUTED_RL  = colors.HexColor('#555555')

    def ST(name, parent='Normal', **kw):
        s = ParagraphStyle(name, parent=styles[parent])
        for k, v in kw.items(): setattr(s, k, v)
        return s

    s_title   = ST('T', fontSize=22, textColor=WHITE_RL, leading=28,
                   alignment=TA_CENTER, fontName='Helvetica-Bold')
    s_sub     = ST('S', fontSize=10, textColor=LIGHT_RL, leading=14,
                   alignment=TA_CENTER, fontName='Helvetica-Oblique')
    s_h1      = ST('H1', fontSize=13, textColor=WHITE_RL, leading=17,
                   fontName='Helvetica-Bold', spaceAfter=2)
    s_h2      = ST('H2', fontSize=10.5, textColor=WHITE_RL, leading=14,
                   fontName='Helvetica-Bold', spaceAfter=2)
    s_body    = ST('B', fontSize=9, leading=13, spaceAfter=3,
                   alignment=TA_JUSTIFY)
    s_bullet  = ST('BL', fontSize=9, leading=13, leftIndent=12,
                   firstLineIndent=-8, spaceAfter=2)
    s_bullet2 = ST('BL2', fontSize=8.5, leading=12, leftIndent=24,
                   firstLineIndent=-8, spaceAfter=1)
    s_cap     = ST('CAP', fontSize=7.5, textColor=MUTED_RL, leading=10,
                   alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=4)
    s_key     = ST('KY', fontSize=8.5, textColor=DARK_RL, leading=12,
                   fontName='Helvetica-Bold', spaceAfter=2)
    s_key_r   = ST('KYR', fontSize=8.5, textColor=colors.HexColor('#8B0000'),
                   leading=12, fontName='Helvetica-Bold', spaceAfter=2)
    s_ref     = ST('REF', fontSize=8, textColor=MUTED_RL, leading=11,
                   leftIndent=10, firstLineIndent=-10, spaceAfter=3)
    s_footer  = ST('FT', fontSize=7.5, textColor=MUTED_RL, alignment=TA_CENTER,
                   fontName='Helvetica-Oblique')

    def sec1(text):
        story.append(Spacer(1, 0.2*cm))
        t = Table([[Paragraph(text, s_h1)]], colWidths=[W - 4*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), DARK_RL),
            ('TOPPADDING',  (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',  (0,0), (-1,-1), 8),
            ('BOX', (0,0), (-1,-1), 0, DARK_RL),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.15*cm))

    def sec2(text):
        story.append(Spacer(1, 0.1*cm))
        t = Table([[Paragraph(text, s_h2)]], colWidths=[W - 4*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), MED_RL),
            ('TOPPADDING',  (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING',  (0,0), (-1,-1), 6),
            ('BOX', (0,0), (-1,-1), 0, MED_RL),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.1*cm))

    def pb(text, sub=False):
        s = s_bullet2 if sub else s_bullet
        prefix = '    ◦  ' if sub else '•  '
        story.append(Paragraph(f'{prefix}{text}', s))

    def bdy(text):
        story.append(Paragraph(text, s_body))

    def keyb(text, danger=False):
        bg = RED_RL if danger else TINT_RL
        ks = s_key_r if danger else s_key
        t = Table([[Paragraph(text, ks)]], colWidths=[W - 4*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('TOPPADDING',  (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING',  (0,0), (-1,-1), 8),
            ('BOX', (0,0), (-1,-1), 0.5, MED_RL),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.15*cm))

    def img(n, caption='', w=14):
        path = slide(n)
        if os.path.exists(path):
            story.append(Spacer(1, 0.2*cm))
            story.append(RLImage(path, width=w*cm, height=w*cm*0.65))
            if caption:
                story.append(Paragraph(caption, s_cap))
            story.append(Spacer(1, 0.1*cm))

    def dtbl(headers, rows, widths=None):
        W_avail = 17  # cm
        n = len(headers)
        if not widths:
            widths = [W_avail / n] * n
        data = [[Paragraph(str(h), ST('th', fontSize=8, textColor=WHITE_RL,
                                      fontName='Helvetica-Bold', leading=10))
                 for h in headers]]
        for row in rows:
            data.append([Paragraph(str(v[0] if isinstance(v, tuple) else v),
                                   ST('td', fontSize=8, leading=10, spaceAfter=1))
                         for v in row])
        t = Table(data, colWidths=[w*cm for w in widths])
        style = [
            ('BACKGROUND', (0,0), (-1,0), MED_RL),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE_RL, TINT2_RL]),
            ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#AAAAAA')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]
        t.setStyle(TableStyle(style))
        story.append(t)
        story.append(Spacer(1, 0.2*cm))

    def hr():
        story.append(HRFlowable(width='100%', thickness=0.5,
                                color=LIGHT_RL, spaceAfter=4))

    # ── TITLE PAGE ─────────────────────────────────────────────────────────────
    title_data = [[Paragraph('STUDY NOTES', ST('tl', fontSize=9, textColor=LIGHT_RL,
                                               fontName='Helvetica-Bold', alignment=TA_CENTER)),
                   ''],
                  [Paragraph('Biological and Anatomical Aspects of Elephants', s_title), ''],
                  [Paragraph('Dr. Parag Nigam, PhD  ·  Head, Dept. of Wildlife Health Management', s_sub), ''],
                  [Paragraph('Wildlife Institute of India, Dehradun  ·  nigamp@wii.gov.in', s_sub), ''],
                  ]
    tt = Table([[Paragraph('STUDY NOTES\nBiological and Anatomical Aspects of Elephants\n'
                           'Dr. Parag Nigam, PhD  |  Wildlife Institute of India, Dehradun',
                           ST('tp', fontSize=16, textColor=WHITE_RL, leading=22,
                              fontName='Helvetica-Bold', alignment=TA_CENTER))]],
               colWidths=[W - 4*cm])
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_RL),
        ('TOPPADDING', (0,0), (-1,-1), 20),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(Spacer(1, 0.5*cm))
    story.append(tt)
    story.append(Spacer(1, 0.3*cm))
    img(1, 'Slide 1 — Title slide', w=13)
    img(2, 'Slide 2 — The largest terrestrial mammal', w=13)
    keyb('Training Program: "Essentials for Mortality Investigation of Asian Elephant"\n'
         'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh, Chhattisgarh')
    story.append(PageBreak())

    # ── SECTION 1 ──────────────────────────────────────────────────────────────
    sec1('1.  Taxonomy & Overview')
    img(3, 'Slide 3 — Three species of elephants', w=13)
    img(4, 'Slide 4 — Key facts about the Asian elephant', w=13)
    sec2('1.1  Classification & Species')
    pb('Family: Proboscidae')
    pb('Three living species: Savanna Elephant (Loxodonta africana), African Forest Elephant (Loxodonta cyclotis), Asian Elephant (Elephas maximus)')
    pb('Asian elephant has five sub-strains: Indian, Burmese, Ceylonese, Sumatran, Malaysian')
    sec2('1.2  Body Size')
    dtbl(['Parameter', 'Bull', 'Cow'],
         [('Height', '9 ft / 2.7 m', '7.5 ft / 2.3 m'),
          ('Weight', '3–5 tons', '2.3–4.5 tons'),
          ('Calf height at birth', '90–100 cm', '90–100 cm'),
          ('Calf weight at birth', '80–100 kg', '80–100 kg')],
         widths=[5.5, 5.5, 6])
    sec2('1.3  Senses')
    pb('Poor eyesight; relies on smell and hearing')
    pb('Can perceive infrasound frequencies inaudible to humans')
    story.append(PageBreak())

    # ── SECTION 2 ──────────────────────────────────────────────────────────────
    sec1('2.  The Trunk (Proboscis)')
    img(5, 'Slide 5 — The trunk: structure and fine-motor capability', w=13)
    sec2('2.1  Structure')
    pb('Elongated upper lip; composed of ~6,000 circular and longitudinal muscles')
    pb('No bones — entirely muscular; belongs to Order Proboscidae')
    sec2('2.2  Function')
    pb('Equivalent to a human hand — grasping, breathing, smelling, drinking, bathing')
    pb('Finger-like process at tip + suction action enables picking objects as small as a pin')
    keyb('KEY: 6,000+ muscles, no bones — most versatile appendage in the animal kingdom.')
    story.append(PageBreak())

    # ── SECTION 3 ──────────────────────────────────────────────────────────────
    sec1('3.  Skeletal System')
    img(6, 'Slide 6 — Appendicular skeleton & 18 nails', w=13)
    img(7, 'Slide 7 — Full articulated skeleton', w=13)
    img(8, 'Slide 8 — Bone cross section: Elephant vs Horse', w=13)
    sec2('3.1  General')
    pb('Total 18 nails; digitigrade stance; limbs act as pillars')
    sec2('3.2  Bone Microstructure')
    pb('Long bones lack hollow marrow cavity — filled with spongy bone / red marrow')
    pb('Compact bone layer thinner than domestic animals; compensated by spongy bone')
    pb('Provides more haemopoietic tissue; reduces overall skeletal weight')
    keyb('NOTE: Thin compact bone is NORMAL — do not misdiagnose as pathology during PM examination.')
    story.append(PageBreak())

    # ── SECTION 4 ──────────────────────────────────────────────────────────────
    sec1('4.  Foot Anatomy')
    img(9, 'Slide 9 — Foot skeletal anatomy: forefoot (Prepollex) and hindfoot (Prehallux)', w=13)
    pb('5 digits (phalangeal bones) per foot')
    pb('Sesamoid bone acts as a SIXTH digit for weight distribution')
    pb('Forefoot: Radio-Ulna → Carpal → Metacarpal → Phalanges (Digits I–III) + Prepollex')
    pb('Hindfoot: Tibia-Fibula → Tarsal → Metatarsal → Phalanges (Digits I–III) + Prehallux')
    keyb('Sesamoid "sixth digit" distributes 3–5 tons across a wide padded surface.')
    story.append(PageBreak())

    # ── SECTION 5 ──────────────────────────────────────────────────────────────
    sec1('5.  Thorax & Rib Cage')
    img(10, 'Slide 10 — Thoracic skeleton showing rib cage', w=13)
    pb('19 or 20 pairs of ribs: 6 sternal + 9 asternal + 9 floating')
    pb('Extensive rib cage reaches level of os coxae — very large thoracic cavity')
    pb('Sternum: definite keel present; articulates obliquely; xiphoid cartilage bends ventrally')
    keyb('CRITICAL: Sternal recumbency is FATAL — xiphoid arrangement prevents it. '
         'Always maintain lateral recumbency in anesthetized elephants.', danger=True)
    story.append(PageBreak())

    # ── SECTION 6 ──────────────────────────────────────────────────────────────
    sec1('6.  Skull Morphology & Sexual Dimorphism')
    img(11, 'Slide 11 — Skull: Frontal view, male vs female', w=13)
    img(12, 'Slide 12 — Skull: Lateral view & mandible', w=13)
    img(13, 'Slide 13 — Skull photographs', w=13)
    sec2('6.1  Frontal View')
    dtbl(['Feature', 'Male Skull', 'Female Skull'],
         [('Parieto-occipital crest', 'Concave / distinctly depressed', 'Rounded and convex'),
          ('Frontal bone', 'Narrow, "pinched" above nares', 'Wider forehead'),
          ('External nares', 'Well above orbit, lateral edge slopes', 'Dumb-bell shape'),
          ('Incisive fossa', 'Deep and narrow, scooped out', 'Slopes gently'),
          ('Tusk alveoli', 'Larger and stouter', 'Absent or reduced')],
         widths=[5, 6, 6])
    sec2('6.2  Lateral View & Mandible')
    dtbl(['Feature', 'Male', 'Female'],
         [('Frontal', 'Slightly concave', 'Rounded'),
          ('Temporal line', 'Robust muscle attachment', 'Smooth'),
          ('Premaxillaries', 'Large', 'Smaller'),
          ('Parieto-occipital', 'Large, swollen bosses', 'Rounded'),
          ('Mandible chin', 'Elongated, dropped, thick', 'Thin, short, pointed')],
         widths=[5, 6, 6])
    keyb('PRACTICAL: Skull morphology allows sex determination of carcass even without soft tissue.')
    story.append(PageBreak())

    # ── SECTION 7 ──────────────────────────────────────────────────────────────
    sec1('7.  Age Estimation — Molar Progression')
    img(14, 'Slide 14 — Molar table for age assessment', w=13)
    bdy('Molars progress forward (M1→M6) and are replaced horizontally. The active molar set determines age.')
    dtbl(['Molar', 'No. of Plates', 'Appearance Age', 'Replacement Age'],
         [('I', '4', '4 months', '2–2.5 yrs'),
          ('II', '8', '6 months', '6 yrs'),
          ('III', '12', '3 yrs', '12 yrs'),
          ('IV', '12 (wider)', '8 yrs', '25 yrs'),
          ('V', '16', '20 yrs', '50–60 yrs'),
          ('VI', '24', '40 yrs', 'Life long')],
         widths=[2, 3.5, 4.5, 7])
    keyb('RULE: When M6 wears out (~60–70 yrs), elephant can no longer chew and dies of starvation.')
    story.append(PageBreak())

    # ── SECTION 8 ──────────────────────────────────────────────────────────────
    sec1('8.  Dentition — Tusks & Molars')
    img(15, 'Slide 15 — Dentition: tusks and molar cross sections', w=13)
    img(16, 'Slide 16 — Tusk anatomy: cementum, dentine, pulp, enamel', w=13)
    sec2('8.1  Dental Formula')
    pb('1 pair of upper incisors (tusks) + 6 molar sets  |  No canines, no premolars')
    sec2('8.2  Tusk Structure (outer→inner)')
    pb('Enamel (tip only) → Cementum (outer layer) → Dentine (~90% bulk) → Pulp cavity (centre)')
    pb('Only 2/3 of length visible externally; 1/3 embedded in skull')
    pb('Ivory = dentine: not brittle, creamy in colour, no enamel structure')
    sec2('8.3  Schreger Lines')
    img(20, 'Slide 20 — Schreger lines in ivory cross section', w=13)
    pb('Cross-hatched pattern unique to proboscidean dentine — forensically diagnostic of real ivory')
    keyb('FORENSIC: Schreger lines confirm elephant ivory identity — admissible under CITES / WPA 1972.')
    story.append(PageBreak())

    # ── SECTION 9 ──────────────────────────────────────────────────────────────
    sec1('9.  Skin, Eyes & Integumentary Glands')
    img(17, 'Slide 17 — Skin, mammary glands and temporal gland', w=13)
    sec2('9.1  Eyes')
    pb('No lacrimal apparatus; moisturized by Harderian glands')
    pb('Robust nictitating membrane (third eyelid) present')
    sec2('9.2  Mammary Glands')
    pb('TWO pectoral mammary glands — located on chest between forelegs (unusual placement)')
    sec2('9.3  Temporal Gland')
    pb('Between eye and ear; secretes musth fluid in bulls during musth period')
    sec2('9.4  Skin & Thermoregulation')
    pb('NO skin sweat glands — thermoregulation via ear flapping, mud/water bathing, wrinkled skin')
    keyb('NOTE: Absence of sweat glands → vulnerable to heat stress during capture/transport.')
    story.append(PageBreak())

    # ── SECTION 10 ─────────────────────────────────────────────────────────────
    sec1('10.  Internal Organs')
    img(18, 'Slide 18 — Full internal organ diagram (labelled)', w=13)
    img(19, 'Slide 19 — Heart, reproductive system, respiratory anatomy', w=13)
    sec2('10.1  Digestive')
    pb('Monogastric hindgut fermentation; bowel up to 35 m; ~40% digestive efficiency')
    pb('No gall bladder; simple stomach')
    sec2('10.2  Urinary')
    pb('Multipyramidal smooth kidneys; small urinary bladder')
    sec2('10.3  Reproductive')
    pb('Testes INTRAABDOMINAL (near kidneys) — no external scrotum')
    sec2('10.4  Cardiovascular')
    pb('Heart: 12–21 kg; BIFID APEX (double-pointed) — unique among mammals')
    sec2('10.5  Nervous')
    pb('Brain: 3.5–5.5 kg; gyrated with prominent temporal lobes; high cognitive ability')
    sec2('10.6  Respiratory')
    pb('No pleural cavity — visceral pleura adhered to parietal pleura')
    pb('Lungs attached to diaphragm; breathing driven by diaphragm movement')
    keyb('CRITICAL: No pleural cavity + diaphragm breathing → sternal recumbency crushes lungs = FATAL. '
         'No thoracocentesis possible. Maintain lateral position.', danger=True)
    story.append(PageBreak())

    # ── SECTION 11 ─────────────────────────────────────────────────────────────
    sec1('11.  Field Estimation of Height & Weight')
    img(21, 'Slide 21 — Assessing height from front foot circumference', w=13)
    img(22, 'Slide 22 — Assessing weight using girth measurements', w=13)
    sec2('11.1  Height')
    pb('Height (ft) = 2 × Circumference of front foot (ft)')
    pb('Usable from footprint impressions at mortality site')
    sec2('11.2  Weight Formulae')
    dtbl(['Formula', 'Parameters', 'Notes'],
         [('12.8 (G + Ng) − 4281', 'G = Chest girth (cm), Ng = Neck girth (cm)', 'General'),
          ('18 (HG) − 3336', 'HG = Heart girth (cm)', 'Male'),
          ('15 (HG) − 2562', 'HG = Heart girth (cm)', 'Female'),
          ('1010 + 0.036 (L × G)', 'L = Forehead-to-tail (cm), G = Chest girth (cm)', 'Alternative')],
         widths=[5, 7, 5])
    keyb('FIELD: Record height and weight in all mortality forms — use front-foot circumference and heart girth even from carcass.')

    hr()
    story.append(Paragraph(
        'Notes compiled from lecture slides by Dr. Parag Nigam, PhD — Wildlife Institute of India  |  '
        'Training: Essentials for Mortality Investigation of Asian Elephant  |  Raigarh, 5–6 June 2026',
        s_footer))

    doc.build(story)
    size_kb = os.path.getsize(OUT_P) // 1024
    print(f'  ✓  {OUT_P}  ({size_kb} KB)')


if __name__ == '__main__':
    print('Building Elephant Anatomy Notes...\n')
    print('  → Word document...')
    build_docx()
    print('  → PDF document...')
    build_pdf()
    print('\nDone.')

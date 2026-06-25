#!/usr/bin/env python3
"""
Generate Notes on Biological and Anatomical Aspects of Elephants
Source: Basic_elephant_PPT.pdf by Dr. Parag Nigam, WII
        + Web-elaborated content from peer-reviewed literature
Outputs: Elephant_Anatomy_Notes_2026.docx and Elephant_Anatomy_Notes_2026.pdf
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, Image as RLImage,
                                 HRFlowable, KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

DIR    = '/home/user/Workshop-on-Conference'
SLIDES = '/home/user/Workshop-on-Conference/slide_images/crops'
OUT_D  = os.path.join(DIR, 'Elephant_Anatomy_Notes_2026.docx')
OUT_P  = os.path.join(DIR, 'Elephant_Anatomy_Notes_2026.pdf')

DARK   = RGBColor(0x1B, 0x43, 0x32)
MED    = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT  = RGBColor(0x52, 0xB7, 0x88)
TINT   = RGBColor(0xD8, 0xF3, 0xDC)
TINT2  = RGBColor(0xEA, 0xF7, 0xEE)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
MUTED  = RGBColor(0x55, 0x55, 0x55)
ORANGE = RGBColor(0xD4, 0x6B, 0x08)
REDL   = RGBColor(0xFA, 0xE0, 0xD8)
RED    = RGBColor(0x8B, 0x00, 0x00)

def rgb_hex(rgb): return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'
def slide(n): return os.path.join(SLIDES, f'slide_{n:02d}.png')

# ═══════════════════════════════════════════════════════════════════════════════
#  WORD HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════════════════════
#  BUILD WORD DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════════
def build_docx():
    doc = Document()
    s = doc.sections[0]
    s.page_width=Cm(21); s.page_height=Cm(29.7)
    s.left_margin=s.right_margin=Cm(2.0); s.top_margin=s.bottom_margin=Cm(1.8)
    doc.core_properties.title  = 'Biological and Anatomical Aspects of Elephants — Elaborated Notes'
    doc.core_properties.author = 'Dr. Parag Nigam, WII (web-elaborated)'

    # TITLE BANNER
    tbl = doc.add_table(rows=1, cols=1); tbl.style='Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(18); p.paragraph_format.space_after=Pt(18)
    r0 = p.add_run('STUDY NOTES — ELABORATED\n')
    r0.font.name='Calibri'; r0.font.size=Pt(9); r0.font.bold=True; r0.font.color.rgb=LIGHT
    r1 = p.add_run('Biological and Anatomical Aspects of Elephants\n')
    r1.font.name='Calibri'; r1.font.size=Pt(20); r1.font.bold=True; r1.font.color.rgb=WHITE
    r2 = p.add_run('Dr. Parag Nigam, PhD  ·  Head, Dept. of Wildlife Health Management\nWildlife Institute of India, Dehradun')
    r2.font.name='Calibri'; r2.font.size=Pt(10); r2.font.italic=True; r2.font.color.rgb=TINT
    doc.add_paragraph()
    img(doc, 1, 'Slide 1 — Title slide', 13)
    img(doc, 2, 'Slide 2 — The Asian elephant: largest terrestrial mammal', 13)
    keybox(doc,
        'Source: Training Program "Essentials for Mortality Investigation of Asian Elephant"\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  |  Technical Support: WII Dehradun\n'
        'Notes elaborated with peer-reviewed literature and web sources.')
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 1: TAXONOMY
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '1.  Taxonomy, Classification & Overview')
    img(doc, 3, 'Slide 3 — Three living species of elephants', 14)
    img(doc, 4, 'Slide 4 — Key facts: Asian elephant', 14)

    sec2(doc, '1.1  Evolutionary Position & Order')
    para(doc,
        'Elephants belong to Order Proboscidea — one of the oldest surviving mammalian orders, with a '
        'fossil record extending back ~55 million years to the Paleocene epoch. At its peak, Proboscidea '
        'comprised over 160 species across all continents except Australia and Antarctica. Today only three '
        'species remain, all in the Family Elephantidae.',
        size=9.5, space_after=4)
    dtable(doc,
        ['Taxonomic Rank', 'Classification'],
        [('Kingdom','Animalia'),('Phylum','Chordata'),('Class','Mammalia'),
         ('Order','Proboscidea'),('Family','Elephantidae'),
         ('Genus (African)','Loxodonta'),('Genus (Asian)','Elephas'),
         ('Species (Asian)','Elephas maximus Linnaeus, 1758')],
        widths=[5, 10.5])

    sec2(doc, '1.2  Three Living Species')
    dtable(doc,
        ['Species', 'Scientific Name', 'Range', 'Key Feature'],
        [('Savanna / Bush Elephant','Loxodonta africana','Sub-Saharan Africa (savanna)','Largest; two finger-like trunk tips; 4 hooves on hindfoot'),
         ('African Forest Elephant','Loxodonta cyclotis','Central African rainforests','Smaller; rounder ears; darker skin; straighter tusks'),
         ('Asian Elephant','Elephas maximus','South & South-East Asia','One finger-like trunk tip; 5 hooves on hindfoot; domed head')],
        widths=[4, 4.5, 4, 5])
    para(doc,
        'Key distinguishing features of Asian vs African elephants: Asian elephants have a single '
        'finger-like projection at the trunk tip (African have two), a more domed head with a central '
        'indentation, smaller rounded ears, and five hooves on the hindfoot (vs three in African). '
        'The skin of Asian elephants may show pink depigmentation on the trunk, ears, or neck.',
        size=9.5, space_after=4)

    sec2(doc, '1.3  Asian Elephant Subspecies')
    para(doc,
        'The IUCN (2020) recognizes four subspecies of Elephas maximus, though taxonomy remains debated:',
        size=9.5, space_after=4)
    dtable(doc,
        ['Subspecies', 'Scientific Name', 'Range', 'Status'],
        [('Indian (Mainland)','E. m. indicus','India, Nepal, Bhutan, Bangladesh, Myanmar, Thailand, Laos, Vietnam, Cambodia, Malaysia','Endangered'),
         ('Sri Lankan','E. m. maximus','Sri Lanka','Endangered — largest body size'),
         ('Sumatran','E. m. sumatranus','Sumatra (Indonesia)','Critically Endangered — smallest body size'),
         ('Bornean (Pygmy)','E. m. borneensis','Borneo (Malaysia/Indonesia)','Endangered — genetically distinct')],
        widths=[3.5, 4, 5.5, 3])
    bullet(doc, 'The PPT lists five strains (Indian, Burmese, Ceylonese, Sumatran, Malaysian) — these correspond to geographic populations; modern genetics recognizes four IUCN subspecies.')
    bullet(doc, 'Phylogeographic studies indicate that Sri Lankan and mainland Indian populations are not always distinct enough for separate subspecific status (IUCN Red List Assessment 2020).')

    sec2(doc, '1.4  Body Size — Asian Elephant')
    dtable(doc,
        ['Parameter', 'Bull (Male)', 'Cow (Female)', 'Calf at Birth'],
        [('Shoulder height','~9 ft / 2.7–3.2 m','~7.5 ft / 2.3–2.5 m','90–100 cm'),
         ('Body weight','3–5.4 tonnes','2.3–4.2 tonnes','80–100 kg'),
         ('Trunk length','~2 m','~2 m','Short — grows rapidly'),
         ('Lifespan','60–70 years in wild','60–70 years in wild','—')],
        widths=[4.5, 4, 4, 4])

    sec2(doc, '1.5  Senses')
    bullet(doc, 'Vision: Poor — eyes positioned laterally, wide visual field but poor depth perception; relies far more on smell and hearing')
    bullet(doc, 'Olfaction: Exceptional — can detect water sources up to 12 km away; ~2,000 olfactory receptor genes (more than any other mammal)')
    bullet(doc, 'Hearing: Can detect infrasound (frequencies <20 Hz, inaudible to humans); used for long-distance communication up to 10 km')
    bullet(doc, 'Touch: Highly sensitive skin, especially at trunk tip and around lips; vibrissae (sensory hairs) on trunk and face')
    bullet(doc, 'Seismic sense: May detect seismic waves from other elephants through ground vibration sensed via feet and transmitted through skeleton')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 2: TRUNK
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '2.  The Trunk (Proboscis)')
    img(doc, 5, 'Slide 5 — The trunk: close-up of structure and fine-motor capability', 14)

    sec2(doc, '2.1  Evolutionary Origin & Structure')
    para(doc,
        'The elephant\'s trunk (proboscis) is a remarkable evolutionary development — a fusion of the '
        'elongated nose and upper lip. It is the defining feature of Order Proboscidea and has no anatomical '
        'equivalent in any other living mammal. The trunk is classified as a muscular hydrostat — a '
        'biological structure that generates movement and force through the coordinated action of muscles '
        'alone, without any bony skeleton for support.',
        size=9.5, space_after=5)
    bullet(doc, 'Total length: approximately 1.5–2 metres in adult Asian elephants')
    bullet(doc, 'Contains up to 150,000 separate muscle fascicles (bundles of muscle fibres)')
    bullet(doc, 'Organized into FOUR main muscle groups:')
    bullet(doc, 'Longitudinal muscles — for elongation and shortening', level=1)
    bullet(doc, 'Radial muscles — for narrowing/stiffening the trunk', level=1)
    bullet(doc, 'Transverse muscles — for lateral bending', level=1)
    bullet(doc, 'Oblique muscles — for rotational movements and torsion', level=1)
    bullet(doc, 'No bones or cartilage — shape changes rely entirely on near-incompressibility of muscle tissue')
    bullet(doc, 'Abundant blood vessels support high metabolic demands and enable stiffening through engorgement')

    sec2(doc, '2.2  Finger-like Tip — Asian vs African')
    dtable(doc,
        ['Feature', 'Asian Elephant', 'African Elephant'],
        [('Trunk tip projections','ONE finger-like process (upper lip)','TWO finger-like processes (upper + lower lip)'),
         ('Gripping method','Wraps around object (grasping)','Pinch between two processes'),
         ('Fine motor ability','High — can pick up single blade of grass','Similar fine motor ability'),
         ('Hooves on hindfoot','5 hooves','3 hooves')],
        widths=[5, 5.5, 5.5])

    sec2(doc, '2.3  Functions of the Trunk')
    dtable(doc,
        ['Function', 'Detail'],
        [('Respiration','Primary airway — breathing through trunk nostrils'),
         ('Olfaction','Chemosensory — can detect scents up to 12 km; 2,000+ olfactory receptor genes'),
         ('Water intake','Can hold 8–12 litres of water per fill; used for drinking and bathing'),
         ('Grasping','Can carry loads up to 270 kg; also manipulates objects as small as a pin'),
         ('Feeding','Strips bark, plucks grass, breaks branches; processes ~150 kg of food daily'),
         ('Communication','Trumpeting, rumbling, touch gestures between individuals'),
         ('Dust/mud bathing','Sprays dust/mud over body for thermoregulation and parasite control'),
         ('Tool use','Uses trunk to hold tools, throw projectiles, and make gestures'),
         ('Combat','Striking, pushing, and wrestling during male-male conflict')],
        widths=[4, 12.5])

    sec2(doc, '2.4  Nerve Supply')
    bullet(doc, 'A unique proboscis nerve runs along both sides of the trunk, connecting to the brain')
    bullet(doc, 'Enables precise proprioceptive feedback for fine motor control')
    bullet(doc, 'The tip of the trunk has highly concentrated mechanoreceptors (similar to human fingertip sensitivity)')

    keybox(doc, 'KEY FACT: 150,000 muscle fascicles, no bones — the trunk is the most versatile appendage in the animal kingdom. A single muscular hydrostat that breathes, smells, drinks, carries 270 kg, and picks up a pin.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 3: SKELETAL SYSTEM
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '3.  Skeletal System')
    img(doc, 6, 'Slide 6 — Appendicular skeleton and 18 nails (digitigrade)', 14)
    img(doc, 7, 'Slide 7 — Full articulated elephant skeleton on display at museum', 14)
    img(doc, 8, 'Slide 8 — Cross-section comparison: Elephant bone vs Horse bone', 14)

    sec2(doc, '3.1  Overall Skeletal Architecture')
    bullet(doc, 'Total number of bones: 326–351 (varies between individuals)')
    bullet(doc, 'Skeleton divided into: skull, spinal column, ribs & sternum (axial), and limbs (appendicular)')
    bullet(doc, 'African elephants: 21 pairs of ribs; Asian elephants: 19–20 pairs')
    bullet(doc, 'Vertebrae are connected by tight joints which limit backbone flexibility (unlike most mammals)')
    bullet(doc, 'No collarbone (clavicle): shoulder blade is suspended by a muscular sling that absorbs impact with each step')

    sec2(doc, '3.2  Limb Architecture — Columnar Design')
    para(doc,
        'Elephant limbs are structured in a columnar (pillar-like) fashion — bones are stacked nearly '
        'vertically, transferring the animal\'s weight straight down through the skeleton to the ground. '
        'This minimizes sideways (shear) forces that would otherwise fatigue bones and connective tissues '
        'over time in an animal weighing 3–5 tonnes.',
        size=9.5, space_after=5)
    bullet(doc, 'Limbs function as pillars — nearly perpendicular to the ground at all times')
    bullet(doc, 'Unlike other mammals, the limb is nearly straight (no extreme joint flexion at rest)')
    bullet(doc, 'Allows sleeping standing up without muscle fatigue')
    bullet(doc, 'Total of 18 nails across all four feet (digitigrade stance)')

    sec2(doc, '3.3  Bone Microstructure — Unique Adaptations')
    para(doc,
        'A cross-section of elephant long bone compared to horse long bone (Slide 8) reveals a fundamental '
        'structural difference that is critical to understand during postmortem examination:',
        size=9.5, space_after=4)
    dtable(doc,
        ['Feature', 'Elephant Long Bone', 'Horse/Cattle Long Bone'],
        [('Medullary (marrow) cavity','ABSENT — no hollow cavity','Present — large hollow cavity'),
         ('Internal structure','Filled with spongy bone + red marrow throughout','Compact cortex with hollow centre'),
         ('Compact bone thickness','THINNER than domestic animals','Thick cortical bone'),
         ('Haemopoietic tissue','More abundant — spongy bone throughout','Less — confined to epiphyses'),
         ('Evolutionary advantage','Reduces skeletal weight; increases blood cell production','Standard mammalian architecture')],
        widths=[5, 5.5, 5.5])
    keybox(doc, 'NECROPSY NOTE: Thin compact bone + absence of marrow cavity is NORMAL in elephants — do NOT misdiagnose as pathological osteoporosis, nutritional bone disease, or rickets during postmortem examination.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 4: FOOT
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '4.  Foot Anatomy')
    img(doc, 9, 'Slide 9 — Foot skeletal anatomy: forefoot (Prepollex) and hindfoot (Prehallux)', 14)

    sec2(doc, '4.1  Overview — Semi-Digitigrade Posture')
    para(doc,
        'Elephants walk in a semi-digitigrade posture — balancing on their toes — but the foot appears '
        'functionally flat because of the large fibro-fatty cushion pad that fills the space beneath the '
        'phalanges and sesamoid bones. This pad acts as a shock absorber, compressing under load and '
        'expanding when weight is removed, reducing ground impact pressure significantly.',
        size=9.5, space_after=5)

    sec2(doc, '4.2  Bone Anatomy of the Foot')
    dtable(doc,
        ['Region', 'Forefoot (Manus)', 'Hindfoot (Pes)'],
        [('Upper limb bones','Radio-Ulna','Tibia-Fibula'),
         ('Proximal row','Carpal bones','Tarsal bones'),
         ('Mid-foot','Metacarpal bones','Metatarsal bones'),
         ('Digits','Phalanges — Digits I, II, III','Phalanges — Digits I, II, III'),
         ('"Sixth digit"','Prepollex (sesamoid)','Prehallux (sesamoid)')],
        widths=[4.5, 6, 6])

    sec2(doc, '4.3  The Sesamoid "Sixth Digit" — Pre-hallux / Pre-pollex')
    para(doc,
        'The most unique feature of elephant foot anatomy is the pre-hallux (hindfoot) and pre-pollex '
        '(forefoot) — a specialized sesamoid bone embedded within a tendon or ligament that extends '
        'into the foot pad and acts as an internal support strut:',
        size=9.5, space_after=4)
    bullet(doc, 'Does NOT articulate like a true toe — it is embedded in the fat pad, not in a synovial joint')
    bullet(doc, 'Acts as a lever that distributes load across the foot pad')
    bullet(doc, 'Works together with the cushioned fat pad to spread 3–5 tonnes across a large ground surface')
    bullet(doc, 'Front foot circumference can be used to accurately estimate shoulder height — FFC accounts for 86% of variance in body weight (research validated in Sumatran elephants)')
    bullet(doc, 'Elephants can walk silently despite their size — foot pad absorbs ground vibration')
    keybox(doc, 'FIELD TIP: Measure the circumference of the front foot impression at a mortality site → Height (ft) = 2 × Front Foot Circumference (ft). This is the fastest field estimate of elephant size.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 5: THORAX
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '5.  Thorax & Rib Cage')
    img(doc, 10, 'Slide 10 — Thoracic skeleton: extensive rib cage reaching to os coxae', 14)

    sec2(doc, '5.1  Rib Count & Structure')
    dtable(doc,
        ['Parameter', 'Asian Elephant', 'African Elephant'],
        [('Total rib pairs','19–20','21'),
         ('Sternal ribs (attached to sternum)','6','6'),
         ('Asternal ribs (attached to cartilage)','9','9'),
         ('Floating ribs (free)','~4–5','~6'),
         ('Extent of rib cage','Reaches nearly to os coxae level','Similar extent'),
         ('Thoracic cavity size','Very large','Very large')],
        widths=[5.5, 5.5, 5.5])
    bullet(doc, 'Sternum: has a definite keel present; xiphoid cartilage articulates obliquely and bends ventrally')
    bullet(doc, 'The enormous thoracic cavity accommodates a 12–21 kg heart and large lungs')

    sec2(doc, '5.2  No Pleural Space — Unique Respiratory Anatomy')
    para(doc,
        'The elephant is the ONLY mammal known to have no true pleural space. In all other mammals, '
        'a fluid-filled pleural cavity separates the visceral pleura (covering the lung) from the parietal '
        'pleura (lining the chest wall), creating a sealed pressure-differential space that drives breathing. '
        'In elephants:',
        size=9.5, space_after=5)
    bullet(doc, 'Both visceral and parietal pleura are composed of DENSE CONNECTIVE TISSUE')
    bullet(doc, 'The two pleural layers are FUSED together via loose connective tissue — no fluid-filled space between them')
    bullet(doc, 'Lungs are therefore physically ADHERED to the chest wall — they cannot collapse like mammalian lungs normally do')
    bullet(doc, 'Breathing is driven almost entirely by DIAPHRAGM MOVEMENT (not by rib cage expansion and contraction)')
    bullet(doc, 'This adaptation is thought to be related to their semi-aquatic evolutionary ancestry (swimming elephants submerge trunks)')
    bullet(doc, 'An unusually thick diaphragm generates the respiratory pressure differences')

    keybox(doc,
        'CRITICAL CLINICAL DANGER:\n'
        '1. STERNAL RECUMBENCY IS FATAL — In sternal position, the abdominal organs compress the diaphragm '
        'from below, preventing its movement → complete respiratory arrest. The xiphoid arrangement also '
        'prevents normal sternal recumbency. Always maintain LATERAL recumbency.\n'
        '2. NO THORACOCENTESIS — Because the pleural layers are fused (no pleural cavity), it is impossible '
        'to drain a pleural effusion. Any fluid accumulation in this connective tissue layer is a serious '
        'clinical emergency.\n'
        '3. ANAESTHESIA: Ventilation support must account for diaphragm-driven breathing — IPPV parameters '
        'differ significantly from other large mammals.',
        danger=True)
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 6: SKULL
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '6.  Skull Morphology & Sexual Dimorphism')
    img(doc, 11, 'Slide 11 — Skull: Male vs Female (Frontal view) with labelled anatomy', 14)
    img(doc, 12, 'Slide 12 — Skull: Lateral view, mandible comparison and photograph', 14)
    img(doc, 13, 'Slide 13 — Skull photographs: male (left) vs female (right)', 14)

    sec2(doc, '6.1  Skull Architecture — General Features')
    para(doc,
        'The elephant skull is one of the most distinctive in the animal kingdom. Its apparent size is '
        'largely an illusion — the skull is filled with an extensive honeycomb-like network of air sinuses '
        '(diploë), which dramatically reduce the skull\'s actual bone weight while maintaining structural '
        'rigidity. This is essential for supporting the heavy trunk and tusks without overloading the neck.',
        size=9.5, space_after=5)
    bullet(doc, 'Massive diploic (honeycomb) sinuses fill the forehead region — give the skull its domed appearance')
    bullet(doc, 'The true brain case is relatively small, positioned posteriorly within the skull mass')
    bullet(doc, 'Skull contains: interparietal, parietal, frontal, nasal, lacrimal, maxilla, premaxilla, mandible, temporal and occipital bones')
    bullet(doc, 'Incisive fossa = deep depression in the premaxilla where tusk roots (alveoli) are embedded')
    bullet(doc, 'Infraorbital foramen present on the dorsal skull surface below the orbit')

    sec2(doc, '6.2  Sexual Dimorphism — Frontal View')
    dtable(doc,
        ['Feature (Frontal view)', 'Male Skull', 'Female Skull'],
        [('Parieto-occipital crest (A)','Concave / distinctly depressed on median plane of dorsal border','Rounded and somewhat convex on dorso-median region'),
         ('Frontal bone (B)','Narrow forehead; "pinched" above nares','Wider forehead'),
         ('External nares (C)','Well above orbit; placed higher; lateral edge slopes down','Dumb-bell shape'),
         ('Incisive fossa (D)','Deep and narrow; "Scooped out" below inferior nares border','Inferior border slopes gently into fossa'),
         ('Tusk alveoli (E)','Larger and stouter; incisors larger (may be reduced in makhna)','Tusk often absent or with reduced alveoli')],
        widths=[5, 5.5, 5.5])

    sec2(doc, '6.3  Sexual Dimorphism — Lateral View')
    dtable(doc,
        ['Feature (Lateral view)', 'Male Skull', 'Female Skull'],
        [('Frontal (F)','Slightly concave forehead','Rounded forehead'),
         ('Temporal line / postero-medial wall (G)','Present with robust muscle attachment','Smooth and not so pronounced'),
         ('Premaxillaries (H)','Large','Smaller'),
         ('Parieto-occipital region (I)','Large, swollen bosses','Rounded'),
         ('Mandible chin (symphysis)','Elongated, dropped downwards; thick and broad','Thin, short and pointed')],
        widths=[5, 5.5, 5.5])

    sec2(doc, '6.4  Other Measurements')
    dtable(doc,
        ['Measurement', 'Male', 'Female'],
        [('Ratio of occipital length to forehead length','Greater than female; around 1.5–1.65','Almost equal'),
         ('Ratio of forehead length to head length','Less than half head length','Greater than half head length')],
        widths=[7, 5, 4.5])

    sec2(doc, '6.5  Age-Dependency of Sexual Dimorphism')
    bullet(doc, 'Skull sexual dimorphism is age-dependent — during first two years of life, male and female skulls are nearly identical')
    bullet(doc, 'Differences become progressively more pronounced with age as males develop robust tusk alveoli, temporal muscle attachments, and occipital bosses')
    bullet(doc, 'Recent research (2024, PMC) found that pelvic bone shows the GREATEST sexual dimorphism, not skull — especially in overall pelvic girdle length and pubic symphysis')

    keybox(doc, 'PRACTICAL: Skull morphology allows definitive sex determination from a carcass even when ALL soft tissues are absent — critical for mortality investigation reports where body is decomposed.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 7: AGE ESTIMATION
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '7.  Age Estimation — Molar Progression')
    img(doc, 14, 'Slide 14 — Molar table for assessing age with skull cross-section', 14)

    sec2(doc, '7.1  Unique Horizontal Molar Replacement')
    para(doc,
        'Elephants possess the most unusual dental replacement mechanism among all mammals — horizontal '
        'molar progression. Unlike vertical tooth replacement seen in all other mammals, elephant molars '
        'develop at the BACK of the jaw and progressively move FORWARD (anteriorly) as each preceding '
        'molar wears down. The worn tooth fragments drop off from the front of the jaw as the new tooth '
        'pushes it out from behind.',
        size=9.5, space_after=5)
    bullet(doc, 'Six molar sets (M1–M6) develop on each side of the upper AND lower jaw (24 molars total)')
    bullet(doc, 'Maximum of 2 molars in wear simultaneously in any one half of the jaw at any given time')
    bullet(doc, 'Each succeeding molar set is LARGER and has MORE plates (lamellae) than the preceding one')
    bullet(doc, 'The number of enamel plates (lamellae) on each molar is the key identification feature')

    sec2(doc, '7.2  Molar Identification & Age Table (Asian Elephant)')
    dtable(doc,
        ['Molar', 'No. of Enamel Plates', 'Appearance Age', 'Replacement Age', 'Notes'],
        [('M1','4','4 months','2–2.5 years','Deciduous; worn quickly'),
         ('M2','8','6 months','6 years','Still a milk tooth'),
         ('M3','12','3 years','12 years','First permanent-like molar'),
         ('M4','12 (wider plates)','8 years','25 years','Distinguishable by wider lamellae'),
         ('M5','16','20 years','50–60 years','Long wear period; most time in use'),
         ('M6','24','40 years','Life long (until death)','Last molar — never replaced')],
        widths=[1.5, 3, 3, 3.5, 5.5])

    sec2(doc, '7.3  Forensic Age Assessment from Molars')
    bullet(doc, 'Examine which molar set is currently in wear in the jaw')
    bullet(doc, 'Count the number of enamel plates (lamellae) on the active molar')
    bullet(doc, 'Assess the degree of wear (front-to-back wear gradient = tilt of the occlusal surface)')
    bullet(doc, 'A complete (full) molar has at least 8 or more lamellae visible without frontal or rear wear')
    bullet(doc, 'African elephant molar timeline differs: M6 worn by ~47 years; Asian elephant M6 lasts to ~60–70 years')

    keybox(doc, 'RULE: When M6 is completely worn down (~60–70 yrs in Asian elephants), the animal can no longer chew food efficiently → loses body condition → dies of starvation. M6 wear status is therefore the biological clock of elephant longevity. Document molar status on ALL elephant mortality forms.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 8: DENTITION & TUSKS
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '8.  Dentition — Tusks & Ivory')
    img(doc, 15, 'Slide 15 — Dentition: tusks, molar cross-sections and skull position', 14)
    img(doc, 16, 'Slide 16 — Tusk anatomy: layered structure, pulp cavity and trimming', 14)

    sec2(doc, '8.1  Dental Formula')
    dtable(doc,
        ['Tooth Type', 'Present?', 'Detail'],
        [('Incisors (upper)','YES — pair of tusks','Exaggerated upper incisors; only upper pair'),
         ('Canines','NO','Absent in all proboscideans'),
         ('Premolars','NO','Absent in all proboscideans'),
         ('Molars','YES — 6 sets (M1–M6)','One set active at a time; progress forward horizontally')],
        widths=[4, 3, 9.5])

    sec2(doc, '8.2  Tusks — Anatomy and Composition')
    para(doc,
        'Tusks are permanently growing incisors (upper only) that have undergone exaggerated evolutionary '
        'development for digging, bark stripping, combat, and as a display of sexual fitness. Only 2/3 of '
        'the tusk\'s total length is externally visible; the remaining 1/3 is embedded deep within the '
        'incisive fossa (alveolus) of the premaxilla bone.',
        size=9.5, space_after=5)
    dtable(doc,
        ['Layer (outer → inner)', 'Composition', 'Notes'],
        [('Cementum','Acellular bone-like tissue','Thin outer covering; protects dentine'),
         ('Dentine','Mineralized collagen + calcium phosphate crystals (hydroxyapatite)','~90% of tusk volume; this IS ivory'),
         ('Enamel','Calcium phosphate crystal matrix','ONLY at tip; wears off quickly'),
         ('Pulp cavity (centre)','Connective tissue, blood vessels, nerves','Where ivory is continuously formed')],
        widths=[4, 5.5, 7])
    bullet(doc, 'Ivory properties: NOT brittle (unlike enamel), creamy/white in colour, continuous growth throughout life')
    bullet(doc, 'Tusks grow approximately 10–15 cm per year in adult males')
    bullet(doc, '"Makhna" = tuskless male Asian elephant (common in Sri Lankan population; rare in Indian)')
    bullet(doc, 'Female Asian elephants usually have very small tushes or none visible; African females have prominent tusks')

    sec2(doc, '8.3  Schreger Lines — The Ivory Fingerprint')
    img(doc, 20, 'Slide 20 — Schreger lines in cross-section of ivory (forensic identification)', 14)
    para(doc,
        'Schreger lines are the most important forensic feature for identifying elephant ivory. They appear '
        'as characteristic cross-hatching (engine turning, stacked chevrons, or checkerboard pattern) on '
        'a polished cross-section of ivory dentine, resulting from the three-dimensional arrangement of '
        'mineralized collagen fibrils in the dentine matrix.',
        size=9.5, space_after=5)
    bullet(doc, 'Visible on cross-sections perpendicular to the tusk axis as a checkerboard / chevron pattern')
    bullet(doc, 'On longitudinal sections: alternating light and dark stripes')
    bullet(doc, 'TWO types:')
    bullet(doc, 'Outer Schreger lines — clearly visible near the cementum surface', level=1)
    bullet(doc, 'Inner Schreger lines — faintly visible near the pulp cavity', level=1)
    bullet(doc, 'Angle of intersection of Schreger lines distinguishes species:')
    bullet(doc, 'ELEPHANT ivory: average angle 115° — characteristic "V" or chevron shape', level=1)
    bullet(doc, 'MAMMOTH ivory: smaller angle — distinguishable from elephant ivory', level=1)
    bullet(doc, 'Hippo, walrus, boar: NO Schreger lines — conclusively not elephant/mammoth ivory', level=1)
    keybox(doc, 'FORENSIC / LEGAL: Schreger lines are the gold standard for confirming elephant ivory identity — admissible in court. Visible under UV black light. Required identification test under CITES Appendix I and Wildlife Protection Act 1972 (India). Document in all seizure reports involving suspected ivory.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 9: SKIN, EYES & GLANDS
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '9.  Skin, Eyes & Integumentary Glands')
    img(doc, 17, 'Slide 17 — Skin texture (left), mammary glands (centre), temporal gland (right)', 14)

    sec2(doc, '9.1  Skin')
    bullet(doc, 'Skin is deeply wrinkled and thick (up to 2.5 cm over the back and head)')
    bullet(doc, 'Wrinkles significantly increase surface area for heat dissipation — critical for thermoregulation')
    bullet(doc, 'Skin colour: dark grey; depigmented (pink) patches may appear on trunk, ears, and neck — more common in Asian elephants')
    bullet(doc, 'Sparse hair covering (not completely hairless): more visible in calves, reduces with age')
    bullet(doc, 'Vibrissae (sensory whiskers) present on trunk, face, and tail tip')
    bullet(doc, 'NO typical skin sweat glands across the body surface')
    bullet(doc, 'Very few sweat glands — only clustered around the TOENAILS (sole source of sweat secretion)')

    sec2(doc, '9.2  Thermoregulation Methods (in absence of sweat glands)')
    bullet(doc, 'Ear flapping: large surface area with subcutaneous blood vessels → convective heat loss (ears can reduce blood temperature by up to 5°C)')
    bullet(doc, 'Water bathing and mud wallowing: evaporative cooling')
    bullet(doc, 'Seeking shade during peak heat hours')
    bullet(doc, 'Seeking wet areas / water bodies to immerse and cool body core')
    keybox(doc, 'FIELD WARNING: Elephants are highly susceptible to heat stress and hyperthermia during capture, immobilization, or transport. No functional body sweat glands = very limited intrinsic cooling. Monitor body temperature, spray water on ears, and minimize exposure to direct sunlight.', danger=True)

    sec2(doc, '9.3  Eyes & Lacrimal System')
    bullet(doc, 'Eyes have NO lacrimal apparatus (no conventional tear ducts or lacrimal glands)')
    bullet(doc, 'Eye moisturization is entirely provided by the Harderian gland — a large modified gland in the orbit')
    bullet(doc, 'Harderian gland secretion provides lubrication and may have immunological function')
    bullet(doc, 'Robust nictitating membrane (third eyelid) present — moves mediolaterally to clean and protect the cornea')
    bullet(doc, 'Poor visual acuity — eyesight is secondary to olfaction and hearing')

    sec2(doc, '9.4  Mammary Glands')
    bullet(doc, 'Female elephants have TWO pectoral mammary glands — located between the front legs on the chest wall')
    bullet(doc, 'This is unusual among mammals — most species have inguinal or abdominal mammary glands')
    bullet(doc, 'Calves suckle with their MOUTH (not trunk) by reaching up between the mother\'s front legs')
    bullet(doc, 'Lactation period: up to 4–5 years; calves are milk-dependent for at least 2 years')
    bullet(doc, 'Milk production: ~11–12 litres per day during peak lactation')

    sec2(doc, '9.5  Temporal Gland — Musth')
    para(doc,
        'The temporal gland is a specialized secretory structure unique to elephants, located on each '
        'side of the head between the eye and the ear. It is present in BOTH sexes:',
        size=9.5, space_after=4)
    bullet(doc, 'Histologically: a MODIFIED APOCRINE SWEAT GLAND (not a true salivary or sebaceous gland)')
    bullet(doc, 'Secretes an oily fluid containing cholesterol, phenol, cresol, and farnesol (pheromone-like compounds)')
    bullet(doc, 'In MALES during musth: secretes thick, dark "temporin" — a tar-like fluid indicating peak testosterone')
    bullet(doc, 'In FEMALES: may activate during exciting or stressful periods (births, encounters)')
    bullet(doc, 'MUSTH characteristics in bulls:')
    bullet(doc, 'Drooling from mouth, dribbling urine continuously (green tinge)', level=1)
    bullet(doc, 'Swollen temporal gland with heavy temporin secretion', level=1)
    bullet(doc, 'Aggressive, unpredictable behaviour; testosterone levels 60× normal baseline', level=1)
    bullet(doc, 'Duration: days to months; annual event in mature bulls', level=1)
    keybox(doc, 'SAFETY: A bull elephant in musth is EXTREMELY DANGEROUS and unpredictable. Dark temporal gland secretion + dribbling urine = musth indicator. Approach only with extreme caution. Musth can override dominance hierarchies — even trained captive elephants in musth are dangerous.')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 10: INTERNAL ORGANS
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '10.  Internal Organs')
    img(doc, 18, 'Slide 18 — Full labelled internal organ diagram', 14)
    img(doc, 19, 'Slide 19 — Heart, reproductive system, and respiratory anatomy details', 14)

    sec2(doc, '10.1  Digestive System')
    bullet(doc, 'Monogastric (single-stomach) HINDGUT FERMENTATION system — fermentation occurs in the cecum and large intestine (like horses), not in the stomach (unlike cattle)')
    bullet(doc, 'Total bowel (intestinal) length: up to 35 metres')
    bullet(doc, 'Digestive efficiency: only ~40% — most plant ingesta pass undigested; compensated by consuming 150–200 kg of plant material daily')
    bullet(doc, 'Stomach: simple, single-chambered; muscular; relatively small')
    bullet(doc, 'LIVER: has NO GALL BLADDER — bile drains directly from liver into the duodenum via the bile duct; a duodenal pouch connects biliary and pancreatic ducts (unique arrangement)')
    bullet(doc, 'Water intake: 80–200 litres per day depending on climate and season')
    bullet(doc, 'Dung: 16–18 separate dung boluses per day; ~120 kg dung daily; important seed dispersal')

    sec2(doc, '10.2  Urinary System')
    bullet(doc, 'KIDNEYS: multipyramidal smooth kidneys (lobulated appearance, unlike smooth kidneys of most mammals; similar to cetaceans and bears)')
    bullet(doc, 'Small urinary bladder relative to body size')
    bullet(doc, 'Urine output: 10–15 urinations per day producing 6–18 litres total')
    bullet(doc, 'Urine during musth: continuously dribbled, often green-tinged (hormonal metabolites)')

    sec2(doc, '10.3  Cardiovascular System')
    dtable(doc,
        ['Parameter', 'Value / Feature'],
        [('Heart weight','12–21 kg (up to 30 lbs in large bulls)'),
         ('Heart rate','~30 beats per minute (resting); slower in larger individuals'),
         ('Apex shape','BIFID (double-pointed) apex — unique among living mammals'),
         ('Position','Centrally located in thoracic cavity'),
         ('Blood volume','~160 litres in a 5-tonne elephant')],
        widths=[5.5, 11])
    bullet(doc, 'The BIFID apex (two-pointed heart) is a diagnostic finding at necropsy — do not mistake for pathological deformity')
    bullet(doc, 'Large blood vessels adapted for high-pressure, high-volume circulation')

    sec2(doc, '10.4  Reproductive System')
    dtable(doc,
        ['Feature', 'Male', 'Female'],
        [('Testes','INTRAABDOMINAL — never descend; located near kidneys','Two ovaries; cyclical ovarian activity'),
         ('External genitalia','No scrotum; penis sheathed ventrally, becomes S-shaped when erect','Vulva located ventrally, far forward toward hindlegs'),
         ('Uterus','—','Bicornuate (two-horned) uterus'),
         ('Gestation','—','~22 months (longest of any land mammal)'),
         ('Interbirth interval','—','4–5 years (lactational anoestrus)'),
         ('Sexual maturity','10–15 years','8–12 years')],
        widths=[4, 6.5, 6])
    bullet(doc, 'Intraabdominal testes: important necropsy note — do not confuse with other intra-abdominal structures; testes are located retroperitoneally near the kidneys')

    sec2(doc, '10.5  Brain & Nervous System')
    para(doc,
        'The elephant has the largest brain of any living land animal, with remarkable cognitive capabilities:',
        size=9.5, space_after=4)
    dtable(doc,
        ['Feature', 'Elephant', 'Human (comparison)'],
        [('Brain weight','3.5–5.5 kg','~1.4 kg'),
         ('Total neurons','~257 billion (African elephant)','~86 billion'),
         ('Cortical neurons','~5.6 billion (cerebral cortex)','~16 billion'),
         ('Cerebellar neurons','97.5% of all neurons in cerebellum','Less than 80%'),
         ('Temporal lobes','Disproportionately large — largest of any mammal','Prominent but relatively smaller'),
         ('Olfactory bulbs','Very large — highest density of olfactory receptors of any mammal','Relatively small'),
         ('Self-recognition','Passes mirror test (MSR)','Yes')],
        widths=[5, 6, 5.5])
    bullet(doc, 'Brain is gyrated (deeply folded) — increases surface area for neuronal density')
    bullet(doc, 'Prominent temporal lobes: associated with auditory processing, long-term memory, and spatial navigation')
    bullet(doc, 'Documented cognitive abilities: tool use, problem-solving, empathy, cooperation, mourning rituals, social memory spanning decades')

    sec2(doc, '10.6  Respiratory System')
    bullet(doc, 'THE ONLY MAMMAL with no true pleural space (see Section 5.2 for details)')
    bullet(doc, 'Visceral pleura adhered to parietal pleura via dense connective tissue — lungs are glued to the chest wall')
    bullet(doc, 'Breathing driven entirely by diaphragm movement (very thick diaphragm)')
    bullet(doc, 'Trachea: large-diameter; connects to two large-volume lungs in the thoracic cavity')
    keybox(doc,
        'KEY INTERNAL ORGAN SUMMARY FOR NECROPSY:\n'
        '• No gall bladder (direct bile duct drainage)  •  Intraabdominal testes (no scrotum)\n'
        '• Bifid (double-pointed) heart apex  •  No true pleural cavity\n'
        '• Multipyramidal lobulated kidneys  •  35 m intestinal length\n'
        '• Hindgut fermentation (not ruminant)  •  22-month gestation in females\n'
        '• Brain weight 3.5–5.5 kg with prominent temporal lobes')
    doc.add_paragraph()
    page_break(doc)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 11: HEIGHT & WEIGHT
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '11.  Field Estimation of Height & Weight')
    img(doc, 21, 'Slide 21 — Assessing height using front foot circumference', 14)
    img(doc, 22, 'Slide 22 — Assessing weight: body girth measurement positions', 14)

    sec2(doc, '11.1  Height Estimation')
    para(doc,
        'The shoulder height of an elephant can be accurately estimated from the circumference of its front '
        'footprint — a field method validated across multiple elephant populations:',
        size=9.5, space_after=4)
    bullet(doc, 'Formula: Shoulder Height = 2 × Circumference of front foot (same units)')
    bullet(doc, 'Forefoot circumference accounts for 86% of variance in body weight (Sumatran elephant study)')
    bullet(doc, 'Correlation of FFC with shoulder height: R = 0.809 (strong correlation, validated)')
    bullet(doc, 'Correlation of FFC with body length: R = 0.769')
    bullet(doc, 'Practical advantage: measurement can be taken from a fresh footprint even without the animal present — valuable at mortality sites, field surveys, and wildlife corridors')
    bullet(doc, 'Additional formula (refined): SH (cm) = 1.17 × FFC (cm) + 75.73')

    sec2(doc, '11.2  Weight Estimation Formulae')
    dtable(doc,
        ['Formula (kg)', 'Parameters', 'Notes'],
        [('12.8 (G + Ng) − 4281',
          'G = Chest girth (cm)\nNg = Neck girth (cm)',
          'General formula; applicable to both sexes'),
         ('18 × (HG) − 3336',
          'HG = Heart girth (cm)',
          'Male-specific formula'),
         ('15 × (HG) − 2562',
          'HG = Heart girth (cm)',
          'Female-specific formula'),
         ('1010 + 0.036 (L × G)',
          'L = Body length, forehead base to tail base (cm)\nG = Chest girth just caudal to elbow (cm)',
          'Two-parameter formula; good general accuracy')],
        widths=[5, 6.5, 5])

    sec2(doc, '11.3  Measurement Landmarks')
    dtable(doc,
        ['Measurement', 'Definition', 'Practical Note'],
        [('Front Foot Circumference (FFC)', 'Circumference around the front foot at ground level', 'Can be measured from footprint in soft soil'),
         ('Chest / Heart Girth (HG)', 'Circumference just caudal (behind) the elbow', 'Most reliable single weight predictor'),
         ('Neck Girth (Ng)', 'Circumference at mid-neck', 'Easier to measure in captive elephants'),
         ('Body Length (L)', 'From base of forehead (top of trunk root) to base of tail', 'Measured along dorsal midline')],
        widths=[4, 5.5, 7])

    keybox(doc, 'MANDATORY FIELD DATA: Height and weight MUST be recorded in all elephant mortality investigation forms.\n'
        '• Use front foot circumference (from footprint) for height if carcass is inaccessible\n'
        '• Use heart girth measurement for weight estimation\n'
        '• Document all measurement landmarks and formula used')
    doc.add_paragraph()

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 12: REFERENCES
    # ─────────────────────────────────────────────────────────────────────────
    sec1(doc, '12.  References & Sources')
    bullet(doc, 'Nigam P. (2026). Biological and Anatomical Aspects of Elephants [PPT]. Training Program: Essentials for Mortality Investigation of Asian Elephant. WII, Dehradun.')
    bullet(doc, 'Shoshani J & Tassy P (1996). The Proboscidea: Evolution and Palaeoecology of Elephants and Their Relatives. Oxford University Press.')
    bullet(doc, 'Sukumar R (2003). The Living Elephants: Evolutionary Ecology, Behaviour, and Conservation. Oxford University Press.')
    bullet(doc, 'IUCN SSC Asian Elephant Specialist Group (2020). Elephas maximus. IUCN Red List of Threatened Species.')
    bullet(doc, 'Herring SM et al. (2021). Elephants evolved strategies reducing the biomechanical complexity of their trunk. Current Biology.')
    bullet(doc, 'Loo AHB et al. (2024). Sexual Dimorphism in Skeletal Morphology of Asian Elephants. PMC12383435.')
    bullet(doc, 'Herculano-Houzel S et al. (2014). The elephant brain in numbers. Frontiers in Neuroanatomy. PMC4053853.')
    bullet(doc, 'Wittemyer G & Klingel H (2016). Temporal gland secretion in African elephants. Mammalian Biology.')
    bullet(doc, 'CITES Ivory Identification Guide: cites.org/eng/resources/pub/E-Ivory-guide.pdf')
    bullet(doc, 'Sreetharan M et al. (2016). Body weight formulation in Asian elephant. ResearchGate 299053386.')
    bullet(doc, "West JB (2001). The elephant's respiratory system: Adaptations to gravitational stress. ResearchGate 13921092.")
    doc.add_paragraph()
    para(doc, 'Notes compiled from lecture by Dr. Parag Nigam, PhD — Wildlife Institute of India  |  Web-elaborated June 2026',
         size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, 'Training Program: Essentials for Mortality Investigation of Asian Elephant  ·  5–6 June 2026, Raigarh, Chhattisgarh',
         size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(OUT_D)
    print(f'  ✓  {OUT_D}  ({os.path.getsize(OUT_D)//1024} KB)')


# ═══════════════════════════════════════════════════════════════════════════════
#  BUILD PDF DOCUMENT
# ═══════════════════════════════════════════════════════════════════════════════
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
    WH = colors.white; BK = colors.HexColor('#1A1A1A')
    MT = colors.HexColor('#555555'); DRD = colors.HexColor('#8B0000')

    def ST(name, **kw):
        s = ParagraphStyle(name, parent=styles['Normal'])
        for k, v in kw.items(): setattr(s, k, v)
        return s

    sH1   = ST('H1', fontSize=13, textColor=WH, leading=17, fontName='Helvetica-Bold')
    sH2   = ST('H2', fontSize=10.5, textColor=WH, leading=14, fontName='Helvetica-Bold')
    sBD   = ST('BD', fontSize=9, leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
    sBL   = ST('BL', fontSize=9, leading=13, leftIndent=12, firstLineIndent=-9, spaceAfter=2)
    sBL2  = ST('B2', fontSize=8.5, leading=12, leftIndent=24, firstLineIndent=-9, spaceAfter=1)
    sCAP  = ST('CP', fontSize=7.5, textColor=MT, leading=10, alignment=TA_CENTER,
               fontName='Helvetica-Oblique', spaceAfter=4)
    sKY   = ST('KY', fontSize=8.5, textColor=DK, leading=12, fontName='Helvetica-Bold')
    sKYR  = ST('KR', fontSize=8.5, textColor=DRD, leading=12, fontName='Helvetica-Bold')
    sFT   = ST('FT', fontSize=7.5, textColor=MT, alignment=TA_CENTER, fontName='Helvetica-Oblique')
    sTD   = ST('TD', fontSize=8, leading=11, spaceAfter=1)
    sTH   = ST('TH', fontSize=8, leading=11, textColor=WH, fontName='Helvetica-Bold')
    sTIT  = ST('TT', fontSize=20, textColor=WH, leading=26, fontName='Helvetica-Bold',
               alignment=TA_CENTER)
    sSUB  = ST('SB', fontSize=9.5, textColor=LT, leading=13, fontName='Helvetica-Oblique',
               alignment=TA_CENTER)

    CW = W - 4*cm  # content width

    def h1(txt):
        story.append(Spacer(1, 0.2*cm))
        t = Table([[Paragraph(txt, sH1)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                               ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                               ('LEFTPADDING',(0,0),(-1,-1),8),('BOX',(0,0),(-1,-1),0,DK)]))
        story.append(t); story.append(Spacer(1, 0.12*cm))

    def h2(txt):
        story.append(Spacer(1, 0.1*cm))
        t = Table([[Paragraph(txt, sH2)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),MD),
                               ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
                               ('LEFTPADDING',(0,0),(-1,-1),6),('BOX',(0,0),(-1,-1),0,MD)]))
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

    # TITLE PAGE
    tb = Table([[Paragraph('STUDY NOTES — ELABORATED\nBiological and Anatomical Aspects of Elephants', sTIT)],
                [Paragraph('Dr. Parag Nigam, PhD  ·  Wildlife Institute of India, Dehradun', sSUB)],
                [Paragraph('Training Program: Essentials for Mortality Investigation of Asian Elephant\nChhattisgarh Forest Department  ·  5–6 June 2026, Raigarh', sSUB)]],
               colWidths=[CW])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                             ('TOPPADDING',(0,0),(-1,-1),16),('BOTTOMPADDING',(0,0),(-1,-1),16),
                             ('LEFTPADDING',(0,0),(-1,-1),12)]))
    story.append(Spacer(1, 0.4*cm)); story.append(tb); story.append(Spacer(1, 0.3*cm))
    pi(1,'Slide 1 — Title slide',13); pi(2,'Slide 2 — Largest terrestrial mammal',13)
    kyb('Notes elaborated with peer-reviewed literature and web sources | June 2026')
    story.append(PageBreak())

    # S1 TAXONOMY
    h1('1.  Taxonomy, Classification & Overview')
    pi(3,'Slide 3 — Three living species of elephants',13)
    pi(4,'Slide 4 — Key facts about the Asian elephant',13)
    h2('1.1  Classification')
    dtbl(['Rank','Value'],[('Kingdom','Animalia'),('Phylum','Chordata'),('Class','Mammalia'),
         ('Order','Proboscidea (fossil record ~55 million years)'),('Family','Elephantidae'),
         ('Genus/Species (Asian)','Elephas maximus Linnaeus, 1758')],wds=[4,13])
    h2('1.2  Three Living Species')
    dtbl(['Species','Scientific Name','Key Distinction'],
         [('Savanna Elephant','Loxodonta africana','Largest; 2 trunk-tip fingers; 4 hindfoot hooves'),
          ('Forest Elephant','Loxodonta cyclotis','Smaller; rounder ears; rainforest adapted'),
          ('Asian Elephant','Elephas maximus','1 trunk-tip finger; domed head; 5 hindfoot hooves')],
         wds=[4,5,8])
    h2('1.3  Asian Elephant Subspecies (IUCN 2020)')
    dtbl(['Subspecies','Range','IUCN Status'],
         [('E. m. indicus (Indian/Mainland)','South & Southeast Asian mainland','Endangered'),
          ('E. m. maximus (Sri Lankan)','Sri Lanka','Endangered — largest body size'),
          ('E. m. sumatranus (Sumatran)','Sumatra, Indonesia','Critically Endangered — smallest'),
          ('E. m. borneensis (Bornean Pygmy)','Borneo','Endangered — genetically distinct')],
         wds=[5,7,5])
    h2('1.4  Body Size & Senses')
    dtbl(['Parameter','Bull','Cow'],
         [('Shoulder height','2.7–3.2 m (9 ft)','2.3–2.5 m (7.5 ft)'),
          ('Weight','3–5.4 tonnes','2.3–4.2 tonnes'),
          ('Calf at birth — height/weight','90–100 cm / 80–100 kg','90–100 cm / 80–100 kg')],
         wds=[5.5,5.5,6])
    pb('Olfaction: ~2,000 olfactory receptor genes — most of any mammal; detects water up to 12 km')
    pb('Hearing: detects infrasound <20 Hz; communication range up to 10 km')
    pb('Touch: seismic sense through feet may detect distant elephant movements')
    story.append(PageBreak())

    # S2 TRUNK
    h1('2.  The Trunk (Proboscis)')
    pi(5,'Slide 5 — The trunk: structure and fine-motor capability',13)
    h2('2.1  Structure — Muscular Hydrostat')
    bdy('The trunk is a fusion of the elongated nose and upper lip. It is a MUSCULAR HYDROSTAT — generates all movement through coordinated muscle contractions, with no skeletal support.')
    pb('Up to 150,000 separate muscle fascicles (not just 6,000 circular muscles)')
    pb('Four muscle groups: longitudinal (elongation), radial (narrowing), transverse (lateral bend), oblique (torsion/rotation)')
    pb('No bones, no cartilage — shape changes rely on near-incompressibility of muscle tissue')
    pb('A unique proboscis nerve runs along both sides; abundant blood vessels enable engorgement-based stiffening')
    h2('2.2  Asian vs African Trunk Tip')
    dtbl(['Feature','Asian','African'],[('Finger-like processes','ONE (upper lip only)','TWO (upper + lower lip)'),
         ('Gripping','Wrap-around grasp','Pinch grip'),('Hindfoot hooves','5','3')],wds=[5,6,6])
    h2('2.3  Functions')
    dtbl(['Function','Detail'],[
        ('Respiration','Primary airway — breathing through trunk nostrils'),
        ('Olfaction','2,000+ olfactory receptor genes; water detected up to 12 km'),
        ('Water intake','Holds 8–12 litres per fill; for drinking, bathing, spraying'),
        ('Load carrying','Carries up to 270 kg; picks up objects as small as a pin'),
        ('Daily feeding','Processes ~150 kg of food daily'),
        ('Communication','Trumpeting, rumbling, social touch gestures'),
        ('Combat','Striking, pushing, throwing in male-male conflict')],wds=[4,13])
    kyb('KEY: 150,000 muscle fascicles, no bones — breathes, smells water 12 km away, carries 270 kg, picks up a pin.')
    story.append(PageBreak())

    # S3 SKELETON
    h1('3.  Skeletal System')
    pi(6,'Slide 6 — Appendicular skeleton and 18 nails',13)
    pi(7,'Slide 7 — Articulated elephant skeleton',13)
    pi(8,'Slide 8 — Bone cross-section: Elephant vs Horse',13)
    h2('3.1  Overview')
    pb('Total bones: 326–351; Asian elephants: 19–20 rib pairs (African: 21)')
    pb('No collarbone — shoulder blade suspended by muscular sling (absorbs impact per step)')
    pb('Vertebrae: tight joints limit backbone flexibility; cervical vertebrae elongated for trunk support')
    pb('18 nails total (digitigrade stance); limbs function as vertical pillars')
    h2('3.2  Bone Microstructure')
    dtbl(['Feature','Elephant','Horse/Cattle'],
         [('Medullary cavity','ABSENT — no hollow space','Present — large hollow'),
          ('Internal fill','Spongy bone + red marrow throughout','Compact cortex, hollow centre'),
          ('Compact bone','THINNER than domestic animals','Thick cortical bone'),
          ('Haemopoietic','More abundant throughout bone','Confined to epiphyses')],
         wds=[5,6,6])
    kyb('NECROPSY: Thin compact bone + no marrow cavity = NORMAL. Do NOT diagnose as osteoporosis or nutritional bone disease.')
    story.append(PageBreak())

    # S4 FOOT
    h1('4.  Foot Anatomy')
    pi(9,'Slide 9 — Foot skeletal anatomy: Prepollex and Prehallux',13)
    h2('4.1  Structure')
    pb('Semi-digitigrade posture: walks on toes but appears flat due to fibro-fatty cushion pad')
    pb('Forefoot: Radio-Ulna → Carpal → Metacarpal → Phalanges (Digits I–III) + Prepollex')
    pb('Hindfoot: Tibia-Fibula → Tarsal → Metatarsal → Phalanges (Digits I–III) + Prehallux')
    h2('4.2  The Sesamoid "Sixth Digit"')
    bdy('The pre-hallux/pre-pollex is a specialized sesamoid bone embedded in the fat pad — NOT a true articulating toe. It acts as an internal support strut and lever for load distribution.')
    pb('Foot pad compresses under load and expands when weight is removed — shock absorption')
    pb('Distributes 3–5 tonnes across a wide surface, reducing ground pressure per unit area')
    pb('Enables near-silent movement despite enormous body weight')
    pb('Front foot circumference (FFC) accounts for 86% of variance in body weight (validated)')
    kyb('FIELD: Front Foot Circumference from ground print → Height = 2 × FFC. Fastest field estimate at mortality site.')
    story.append(PageBreak())

    # S5 THORAX
    h1('5.  Thorax & Rib Cage')
    pi(10,'Slide 10 — Thoracic skeleton reaching to os coxae level',13)
    h2('5.1  Rib Count')
    dtbl(['Parameter','Asian Elephant','African Elephant'],
         [('Total rib pairs','19–20','21'),('Sternal ribs','6','6'),
          ('Asternal ribs','9','9'),('Floating ribs','~4–5','~6'),
          ('Sternum','Keel present; xiphoid bends ventrally','Similar')],wds=[5.5,5.5,6])
    h2('5.2  No Pleural Space — Critical Unique Feature')
    bdy('Elephants are the ONLY mammals with no true pleural space. Both pleural layers are fused by dense connective tissue. Lungs are physically adhered to the chest wall. Breathing is driven entirely by diaphragm movement.')
    kyb('CRITICAL: (1) STERNAL RECUMBENCY = FATAL — abdominal organs crush diaphragm → respiratory arrest. '
        '(2) NO THORACOCENTESIS possible. (3) ANAESTHESIA: ventilation must account for diaphragm-driven breathing — IPPV differs from other large mammals. '
        'ALWAYS maintain lateral recumbency.', danger=True)
    story.append(PageBreak())

    # S6 SKULL
    h1('6.  Skull Morphology & Sexual Dimorphism')
    pi(11,'Slide 11 — Skull: frontal view, male vs female',13)
    pi(12,'Slide 12 — Skull: lateral view and mandible',13)
    pi(13,'Slide 13 — Skull photographs: male (left) vs female (right)',13)
    h2('6.1  Skull Architecture')
    pb('Skull filled with extensive honeycomb diploic sinuses — reduce weight while maintaining rigidity')
    pb('Incisive fossa (premaxilla) = deep depression housing tusk alveoli (roots)')
    pb('Apparent forehead "dome" is mostly air sinuses, not brain — true brain case is small and posterior')
    h2('6.2  Sexual Dimorphism — Frontal View')
    dtbl(['Feature','Male','Female'],
         [('Parieto-occipital crest','Concave / depressed on dorsal border','Rounded and convex'),
          ('Frontal bone','Narrow, "pinched" above nares','Wider forehead'),
          ('External nares','High above orbit; lateral edge slopes','Dumb-bell shape'),
          ('Incisive fossa','Deep, narrow, "scooped out"','Slopes gently'),
          ('Tusk alveoli','Larger and stouter','Absent or reduced')],wds=[5,6,6])
    h2('6.3  Lateral View & Mandible')
    dtbl(['Feature','Male','Female'],
         [('Frontal','Slightly concave','Rounded'),
          ('Temporal line','Robust muscle attachment marks','Smooth'),
          ('Premaxillaries','Large','Smaller'),
          ('Mandible chin (symphysis)','Elongated, dropped, thick and broad','Thin, short, pointed')],
         wds=[5,6,6])
    kyb('PRACTICAL: Skull alone allows sex determination from a decomposed carcass. Dimorphism increases with age — first 2 years skulls are similar between sexes.')
    story.append(PageBreak())

    # S7 AGE
    h1('7.  Age Estimation — Molar Progression')
    pi(14,'Slide 14 — Molar table and skull cross-section for age assessment',13)
    bdy('Horizontal molar progression — unique to proboscideans. Six molar sets develop at the back of the jaw and move forward as each preceding molar wears out. Maximum 2 molars in wear simultaneously per half-jaw.')
    h2('7.1  Molar Table (Asian Elephant)')
    dtbl(['Molar','Enamel Plates','Appearance Age','Replacement Age','Notes'],
         [('M1','4','4 months','2–2.5 yrs','Deciduous; worn quickly'),
          ('M2','8','6 months','6 yrs','Milk tooth'),
          ('M3','12','3 yrs','12 yrs','First permanent-like'),
          ('M4','12 (wider)','8 yrs','25 yrs','Wider lamellae'),
          ('M5','16','20 yrs','50–60 yrs','Longest in use'),
          ('M6','24','40 yrs','Life long','Never replaced')],
         wds=[1.5,3,3.5,3.5,5.5])
    pb('African elephant M6 worn by ~47 years; Asian elephant M6 lasts to ~60–70 years')
    pb('Count lamellae (enamel plates) + assess wear gradient to estimate age from molar alone')
    kyb('When M6 is exhausted (~60–70 yrs), elephant dies of starvation. Document molar status on ALL mortality forms.')
    story.append(PageBreak())

    # S8 DENTITION
    h1('8.  Dentition — Tusks & Ivory')
    pi(15,'Slide 15 — Dentition: tusks and molar cross-sections',13)
    pi(16,'Slide 16 — Tusk structure: cementum, dentine, pulp, enamel',13)
    h2('8.1  Tusk Structure (outer → inner)')
    dtbl(['Layer','Composition','Notes'],
         [('Cementum','Bone-like, acellular','Thin outer cover; protects dentine'),
          ('Enamel','Calcium phosphate crystals','TIP ONLY; wears off quickly'),
          ('Dentine','Mineralized collagen + hydroxyapatite','~90% of tusk = IVORY'),
          ('Pulp cavity','Connective tissue, blood vessels, nerves','Where ivory is formed continuously')],
         wds=[3.5,5.5,8])
    pb('Only 2/3 of tusk length is visible; 1/3 is embedded in incisive fossa of premaxilla')
    pb('Tusk growth: ~10–15 cm/year in adult bulls; permanent, never shed')
    pb('Makhna = tuskless male (common in Sri Lanka; rare in India)')
    h2('8.2  Schreger Lines')
    pi(20,'Slide 20 — Schreger lines in ivory cross-section',13)
    bdy('Schreger lines = characteristic cross-hatching (chevrons/engine-turning) on polished ivory cross-sections. Results from 3D arrangement of mineralized collagen fibrils in dentine.')
    pb('Outer Schreger lines: near cementum — clearly visible')
    pb('Inner Schreger lines: near pulp cavity — faintly visible')
    pb('Elephant ivory: average intersection angle = 115° ("V" chevron shape)')
    pb('Mammoth ivory: smaller angle — distinguishable from elephant')
    pb('Hippo/walrus/boar ivory: NO Schreger lines — conclusively rules out elephant/mammoth')
    kyb('FORENSIC: Schreger lines confirm elephant ivory identity under UV black light. Gold standard under CITES Appendix I and Wildlife Protection Act 1972 (India). Required in all seizure reports.')
    story.append(PageBreak())

    # S9 SKIN
    h1('9.  Skin, Eyes & Integumentary Glands')
    pi(17,'Slide 17 — Skin, mammary glands and temporal gland',13)
    h2('9.1  Skin')
    pb('Deeply wrinkled (up to 2.5 cm thick over back); wrinkles increase surface area for heat loss')
    pb('NO body sweat glands — only a few clustered around the toenails')
    pb('Thermoregulation: ear flapping (blood cooling), mud/water bathing, shade-seeking')
    kyb('FIELD WARNING: No body sweat glands = high hyperthermia risk during capture/transport. Monitor temperature; spray water on ears; minimize sun exposure.', danger=True)
    h2('9.2  Eyes')
    pb('No lacrimal apparatus — eye moisturized by Harderian gland in orbit')
    pb('Robust nictitating membrane (third eyelid) — moves mediolaterally to clean cornea')
    h2('9.3  Mammary Glands')
    pb('TWO pectoral mammary glands between front legs — unusual placement (most mammals inguinal/abdominal)')
    pb('Calves suckle with mouth (not trunk), reaching up between mother\'s forelegs')
    pb('Lactation: up to 4–5 years; ~11–12 L/day peak milk production')
    h2('9.4  Temporal Gland — Musth')
    pb('Modified APOCRINE SWEAT GLAND between eye and ear; secretes cholesterol, phenol, cresol, farnesol')
    pb('In musth bulls: secretes thick "temporin" (dark, tar-like); testosterone up to 60× normal')
    pb('Musth signs: temporin secretion + continuous urine dribbling (green) + aggression')
    kyb('SAFETY: Bull in musth = EXTREMELY DANGEROUS. Dark temporal secretion + urine dribbling = musth. Extreme caution required — even trained captive elephants are unpredictable in musth.')
    story.append(PageBreak())

    # S10 INTERNAL
    h1('10.  Internal Organs')
    pi(18,'Slide 18 — Full internal organ diagram (labelled)',13)
    pi(19,'Slide 19 — Heart, reproductive system, respiratory anatomy',13)
    h2('10.1  Digestive System')
    pb('Monogastric HINDGUT FERMENTATION (like horses — cecum & large intestine ferment cellulose)')
    pb('Bowel length: up to 35 m; digestive efficiency ~40%; 150–200 kg plant food daily')
    pb('NO GALL BLADDER — bile drains directly from liver into duodenum via bile duct')
    pb('Water intake: 80–200 L/day; dung output: ~120 kg/day (16–18 boluses/day)')
    h2('10.2  Urinary System')
    pb('MULTIPYRAMIDAL LOBULATED KIDNEYS (like cetaceans and bears — NOT smooth like most mammals)')
    pb('Urine: 10–15 urinations/day; 6–18 L total; green-tinged in musth bulls')
    h2('10.3  Cardiovascular')
    dtbl(['Parameter','Value'],
         [('Heart weight','12–21 kg (up to 30 lbs)'),
          ('Heart rate','~30 beats/min (resting)'),
          ('Apex','BIFID (double-pointed) — unique among mammals'),
          ('Blood volume','~160 L in 5-tonne elephant')],wds=[5,12])
    pb('Bifid apex = NORMAL anatomy — do NOT misdiagnose as congenital defect at necropsy')
    h2('10.4  Reproductive System')
    dtbl(['Feature','Male','Female'],
         [('Testes','INTRAABDOMINAL — near kidneys; NO SCROTUM','Two ovaries; cyclical activity'),
          ('Uterus','—','Bicornuate (two-horned)'),
          ('Gestation','—','~22 months — longest of any land mammal'),
          ('Interbirth interval','—','4–5 years')],wds=[4,6.5,6.5])
    h2('10.5  Brain & Nervous System')
    dtbl(['Feature','Elephant','Human'],
         [('Brain weight','3.5–5.5 kg','~1.4 kg'),
          ('Total neurons','~257 billion','~86 billion'),
          ('Temporal lobes','Largest of any mammal','Prominent but relatively smaller'),
          ('Cognitive ability','Tool use, empathy, grief, mirror self-recognition','Yes')],
         wds=[5,6,6])
    h2('10.6  Respiratory')
    pb('ONLY mammal with no pleural space — lungs fused to chest wall via connective tissue')
    pb('Breathing = diaphragm-driven; very thick diaphragm generates all respiratory pressure')
    kyb('NECROPSY KEY POINTS: No gall bladder | Intraabdominal testes | Bifid heart apex | No pleural cavity | Multipyramidal kidneys | 35 m intestine | Hindgut fermenter | 22-month gestation | 257-billion-neuron brain')
    story.append(PageBreak())

    # S11 HEIGHT/WEIGHT
    h1('11.  Field Estimation of Height & Weight')
    pi(21,'Slide 21 — Height from front foot circumference',13)
    pi(22,'Slide 22 — Weight from body girth measurements',13)
    h2('11.1  Height Estimation')
    pb('Formula: Shoulder Height = 2 × Front Foot Circumference (same units)')
    pb('Refined formula: SH (cm) = 1.17 × FFC (cm) + 75.73')
    pb('FFC accounts for 86% of variance in body weight (validated in Sumatran elephants)')
    pb('FFC vs shoulder height correlation: R = 0.809 (strong); FFC vs body length: R = 0.769')
    pb('Measurable from fresh footprint impression — no direct elephant contact needed')
    h2('11.2  Weight Formulae')
    dtbl(['Formula (kg)','Parameters','Application'],
         [('12.8 (G + Ng) − 4281','G = Chest girth (cm), Ng = Neck girth (cm)','General — both sexes'),
          ('18 × HG − 3336','HG = Heart girth (cm)','Male-specific'),
          ('15 × HG − 2562','HG = Heart girth (cm)','Female-specific'),
          ('1010 + 0.036 (L × G)','L = Forehead-to-tail (cm), G = Chest girth (cm)','Two-parameter formula')],
         wds=[5,6.5,5.5])
    kyb('MANDATORY: Record height (from FFC footprint) and weight (from HG) in ALL mortality investigation forms. Specify which formula used.')

    # REFERENCES
    h1('12.  References & Sources')
    pb('Nigam P. (2026). Biological and Anatomical Aspects of Elephants [PPT]. WII Dehradun.')
    pb('Shoshani J & Tassy P (1996). The Proboscidea. Oxford University Press.')
    pb('Sukumar R (2003). The Living Elephants. Oxford University Press.')
    pb('IUCN SSC AESG (2020). Elephas maximus Red List Assessment.')
    pb('Herring SM et al. (2021). Elephant trunk biomechanics. Current Biology.')
    pb('Loo AHB et al. (2024). Sexual Dimorphism in Asian Elephants (PMC12383435).')
    pb('Herculano-Houzel S et al. (2014). Elephant brain in numbers. Front Neuroanatomy. PMC4053853.')
    pb('West JB (2001). Elephant respiratory system adaptations. ResearchGate 13921092.')
    pb('Sreetharan M et al. (2016). Body weight formulation in Asian elephant. ResearchGate 299053386.')
    pb('CITES Ivory Identification Guide. cites.org/eng/resources/pub/E-Ivory-guide.pdf')
    hr()
    story.append(Paragraph('Notes from Dr. Parag Nigam PPT (WII) | Web-elaborated with peer-reviewed literature | June 2026 | Raigarh Training Program', sFT))

    doc.build(story)
    print(f'  ✓  {OUT_P}  ({os.path.getsize(OUT_P)//1024} KB)')


if __name__ == '__main__':
    print('Building elaborated Elephant Anatomy Notes...\n')
    print('  → Word document...')
    build_docx()
    print('  → PDF document...')
    build_pdf()
    print('\nDone.')

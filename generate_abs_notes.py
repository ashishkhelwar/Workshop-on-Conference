#!/usr/bin/env python3
"""
Generate comprehensive notes from Prof. Dr. A B Shrivastava's presentation:
"Postmortem Examination of Asian Elephant"
Outputs: ABS_Elephant_Necropsy_Notes.docx  and  ABS_Elephant_Necropsy_Notes.pdf
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
SLIDES = '/home/user/Workshop-on-Conference/abs_slides'
OUT_D  = os.path.join(DIR, 'ABS_Elephant_Necropsy_Notes.docx')
OUT_P  = os.path.join(DIR, 'ABS_Elephant_Necropsy_Notes.pdf')

DARK  = RGBColor(0x1B, 0x43, 0x32)
MED   = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT = RGBColor(0x52, 0xB7, 0x88)
TINT  = RGBColor(0xD8, 0xF3, 0xDC)
TINT2 = RGBColor(0xEA, 0xF7, 0xEE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x55, 0x55, 0x55)
REDL  = RGBColor(0xFA, 0xE0, 0xD8)
RED   = RGBColor(0x8B, 0x00, 0x00)
NAVY  = RGBColor(0x1A, 0x2E, 0x44)

def rgb_hex(rgb): return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'
def slide(n): return os.path.join(SLIDES, f'page_{n:02d}.png')

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
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(13); run.font.bold = True
    run.font.color.rgb = WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def sec2(doc, text):
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(MED))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(10.5); run.font.bold = True
    run.font.color.rgb = WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def sec3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(1)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(10); run.font.bold = True
    run.font.color.rgb = MED

def para(doc, text, size=9.5, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4):
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
        cr = cp.add_run(caption); cr.font.name = 'Calibri'; cr.font.size = Pt(8)
        cr.font.italic = True; cr.font.color.rgb = MUTED

def keybox(doc, text, danger=False):
    bg = rgb_hex(REDL) if danger else rgb_hex(TINT)
    fg = RED if danger else DARK
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, bg)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(5)
    run = p.add_run(text); run.font.name = 'Calibri'; run.font.size = Pt(9)
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
def build_docx():
    doc = Document()
    s = doc.sections[0]
    s.page_width=Cm(21); s.page_height=Cm(29.7)
    s.left_margin=s.right_margin=Cm(2.0); s.top_margin=s.bottom_margin=Cm(1.8)
    doc.core_properties.title  = 'Postmortem Examination of Asian Elephant — Prof. Dr. A B Shrivastava'
    doc.core_properties.author = 'Prof. Dr. A B Shrivastava, NDVSU Jabalpur'

    # TITLE BANNER
    tbl = doc.add_table(rows=1, cols=1); tbl.style='Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(20); p.paragraph_format.space_after=Pt(20)
    r0 = p.add_run('LEARNING FROM DEAD\n')
    r0.font.name='Calibri'; r0.font.size=Pt(9); r0.font.bold=True; r0.font.color.rgb=LIGHT
    r1 = p.add_run('Postmortem Examination of Asian Elephant\n')
    r1.font.name='Calibri'; r1.font.size=Pt(18); r1.font.bold=True; r1.font.color.rgb=WHITE
    r2 = p.add_run('Comprehensive Study Notes with Slide Images\n')
    r2.font.name='Calibri'; r2.font.size=Pt(10); r2.font.color.rgb=TINT
    r3 = p.add_run('Prof. Dr. A B Shrivastava  ·  Founder Director, School of Wildlife Forensic and Health\n')
    r3.font.name='Calibri'; r3.font.size=Pt(10); r3.font.bold=True; r3.font.color.rgb=WHITE
    r4 = p.add_run('Nanaji Deshmukh Veterinary Science University, Jabalpur 482001, M.P.')
    r4.font.name='Calibri'; r4.font.size=Pt(9); r4.font.italic=True; r4.font.color.rgb=TINT
    doc.add_paragraph()

    keybox(doc,
        'Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  ·  Technical Support: WII Dehradun\n'
        'Lab Partners: ICAR-IVRI & NDVSU Jabalpur  ·  Notes elaborated with peer-reviewed literature')

    # AUTHOR BOX
    tbl2 = doc.add_table(rows=1, cols=1); tbl2.style='Table Grid'
    cell2 = tbl2.rows[0].cells[0]; shade_cell(cell2, rgb_hex(TINT2))
    p2 = cell2.paragraphs[0]
    p2.paragraph_format.space_before=Pt(6); p2.paragraph_format.space_after=Pt(6)
    r = p2.add_run('ABOUT THE PRESENTER\n')
    r.font.name='Calibri'; r.font.size=Pt(9); r.font.bold=True; r.font.color.rgb=DARK
    r2 = p2.add_run(
        'Prof. Dr. Avadh Bihari Shrivastava is a pioneer in Wildlife Forensic and Health in India. '
        'He is the Founder Director of the School of Wildlife Forensic and Health at Nanaji Deshmukh '
        'Veterinary Science University (NDVSU), Jabalpur. He serves as Honorary Member on the State '
        'Wildlife Boards of Chhattisgarh and Bihar, and is an Honorary Board Member of the Management '
        'Committee of ICAR-NIHSAD. He received the Amrita Devi Vishnoi Award for Wildlife Conservation '
        'in 2005 and leads the ICAR Niche Area of Excellence on Wildlife Forensic and Health Management. '
        'He was felicitated as an Outstanding Veterinarian by the Hon. Minister, GOI for Animal Husbandry '
        'on World Veterinary Day, 29 April 2023 at Vigyan Bhawan, New Delhi. His authored/edited works '
        'include: Manual on Postmortem Examination of Felids; Learning from Dead (with Dr. Parag Nigam); '
        'Big Cats; Necropsy & Carcass Disposal of Asian Elephant: Recommended Operating Procedure; and '
        'Caring for Elephants: Managing Health & Welfare in Captivity.')
    r2.font.name='Calibri'; r2.font.size=Pt(9); r2.font.color.rgb=BLACK
    doc.add_paragraph()
    img(doc, 1, 'Slide 1 — Title slide: NDVSU Jabalpur and author credentials', 13)
    page_break(doc)

    # ─── SECTION 1: WILDLIFE HEALTH MANAGEMENT ────────────────────────────────
    sec1(doc, '1.  Wildlife Health Management — Foundations')
    img(doc, 2, 'Slide 2 — Wildlife Health Management as a Multidisciplinary Approach', 13)

    sec2(doc, '1.1  Definition')
    para(doc,
        'Wildlife Health Management is a branch of Veterinary Science that deals with veterinary '
        'interventions in wild fauna — specifically health monitoring, disease management, scientific '
        'immobilisation, and habitat manipulation — in order to achieve conservation strategies that '
        'maintain healthy populations or ensure conservation of particular species. (Shrivastav, 2010)')

    sec2(doc, '1.2  Multidisciplinary Nature')
    para(doc,
        'Wildlife Health Management is inherently multidisciplinary. It integrates expertise from '
        'eight major scientific domains, all converging on the central goal of maintaining healthy '
        'wildlife populations:')
    dtable(doc,
        ['Discipline', 'Relevance to Elephant Health Management'],
        [('Wildlife Pathology','Core of mortality investigation; disease identification from gross and histopathological findings'),
         ('Wildlife Anatomy','Essential for recognising normal vs pathological anatomy during necropsy; species-specific features'),
         ('Wildlife Clinics & Ethology','Clinical signs pre-mortem and normal behavioural baselines to identify deviations'),
         ('Wildlife Parasitology','Internal/external parasite identification; zoonotic risk assessment'),
         ('Genetic Management of Small Populations','Conservation genetics; inbreeding depression; population viability analysis'),
         ('Animal Biotechnology','PCR-based pathogen detection; DNA forensics; vaccine development (e.g., EEHV vaccines)'),
         ('Wildlife Microbiology','Bacterial/viral culture; antimicrobial resistance profiling; zoonosis risk'),
         ('Wildlife Nutrition','Nutritional deficiency diseases; body condition scoring; digestive health')],
        widths=[5, 12])

    sec2(doc, '1.3  Importance in Conservation')
    para(doc,
        'Wildlife health is often the "silent" conservation tool — consistently under-resourced yet '
        'critical. Population-level disease events can be as devastating as habitat loss. Systematic '
        'necropsy data from deceased animals builds epidemiological baselines, identifies emerging '
        'threats (EEHV, TB, anthrax), and informs captive management protocols. In India, the '
        'Elephant Task Force (2010) and Project Elephant guidelines mandate systematic mortality '
        'investigation for all Schedule I species including elephants.')
    keybox(doc,
        'KEY PRINCIPLE: Wildlife Health is an important, still-growing discipline — yet often ignored. '
        'Though an important component for conservation of wildlife. Every elephant death is a data point '
        'that can protect the living population. Systematic, scientific necropsy is not optional — it is a '
        'conservation imperative.')
    page_break(doc)

    # ─── SECTION 2: HISTORY OF POSTMORTEM ────────────────────────────────────
    sec1(doc, '2.  History of Postmortem Examination')
    img(doc, 3, 'Slide 3 — Introduction: Necropsy vs Autopsy terminology; standard protocol requirements', 13)
    img(doc, 4, 'Slide 4 — Professional quotes on necropsy importance; "Carcass never tells lie"', 13)

    sec2(doc, '2.1  Definition')
    para(doc,
        'Post-mortem examination is the examination of external surfaces and internal organs for the '
        'presence of pathological changes or abnormality in a carcass to ascertain the cause of death. '
        'The term NECROPSY is used for animals and birds; AUTOPSY is used for humans. Both derive from '
        'Greek: "nekros" (dead) + "opsis" (a seeing) — literally "seeing the dead."')

    sec2(doc, '2.2  Historical Milestones')
    dtable(doc,
        ['Era / Person', 'Contribution'],
        [('Sushruta, 2500 BC','Sushruta Samhita documented systematic methods for dissection of human cadavers in ancient India — earliest systematic approach to internal anatomy'),
         ('Roman physician Antistius, 44 BC','Performed earliest documented autopsies on Julius Caesar; identified and documented 23 stab wounds; first forensic pathology record'),
         ('Catholic Church, 1410','Ordered autopsy on Pope Alexander V to determine if he was poisoned; established medicolegal precedent'),
         ('Surgeon Bulkley, 1680','Performed first documented postmortem examination in India'),
         ('Modern Era','Development of standardised necropsy protocols; histopathology; molecular diagnostics; digital documentation standards')],
        widths=[4, 13])

    sec2(doc, '2.3  Wildlife Necropsy vs Clinical Autopsy')
    bullet(doc, '"Postmortem examination is an art of disease diagnosis" — requires scientific and systematic approach')
    bullet(doc, 'Gross pathological findings alone and correlation with history may not be sufficient for diagnosis')
    bullet(doc, 'Confirmative diagnosis requires laboratory support: biological samples must be collected in appropriate preservatives')
    bullet(doc, 'Badly putrefied samples or fresh samples in unsuitable preservatives are useless for lab examination')
    bullet(doc, '"Doctors who perform necropsies or who regularly witness postmortem examinations, learnt to solve their doubts in comparison to those who are not dealing necropsy are floating in the air." — Dr A B Shrivastav, 2014')
    bullet(doc, '"Carcass never tells lie" — Dr Satpati. Every lesion, every finding carries diagnostic truth.')
    bullet(doc, 'Carcasses of wild animals are SELDOM found in suitable condition — the pathologist must work with what is available')

    sec2(doc, '2.4  Staff Requirements for Elephant Necropsy')
    dtable(doc,
        ['Role', 'Minimum Number', 'Responsibilities'],
        [('Veterinarians / Wildlife Pathologists','2–3','Lead necropsy; gross pathological examination; interpretation; report writing'),
         ('Supporting Staff','4','Manual labour: positioning, skinning, organ removal, labelling'),
         ('Photographer','1','Continuous photographic documentation; scale bar in all shots; video recording'),
         ('Sample Collection Personnel','1','Label, fix, preserve and package biological samples correctly')],
        widths=[5, 3, 9])
    page_break(doc)

    # ─── SECTION 3: NECROPSY OBJECTIVES ──────────────────────────────────────
    sec1(doc, '3.  Necropsy Objectives & Pre-Necropsy Evaluation')
    img(doc, 5, 'Slide 5 — Necropsy Objectives and Pre-necropsy Evaluation', 13)

    sec2(doc, '3.1  Necropsy Objectives')
    bullet(doc, 'To know all possible lesions of disease or abnormality present in the carcass')
    bullet(doc, 'To correlate lesions with clinical and laboratory findings')
    bullet(doc, 'To understand the sequence of disease events — what happened first, what followed')
    bullet(doc, 'To prevent or control disease in the healthy living population by identifying the pathogen or cause')
    para(doc,
        'In the context of Schedule I species (including elephant), systematic and sincere PM examination '
        'is a legal and ethical obligation under the Wildlife Protection Act 1972. It provides evidence '
        'for legal proceedings (poaching, electrocution, train-kill), conservation management decisions '
        '(disease control), and scientific research.')

    sec2(doc, '3.2  Pre-Necropsy Evaluation')
    sec3(doc, 'a. Examine the Necropsy Request Letter for:')
    bullet(doc, 'Specific lesions in different organs or systems suspected by the referring officer', level=1)
    bullet(doc, 'Whether it is a cosmetic or routine necropsy (legal vs scientific)', level=1)
    bullet(doc, 'Special requests: sample collection for specific investigations, cultures, photographs', level=1)
    sec3(doc, 'b. Carcass Identification:')
    bullet(doc, 'Ensure correct carcass is being necropsied — identity by microchip/ear notch/GPS collar/physical description', level=1)
    bullet(doc, 'Record: species, sex, estimated age, location GPS coordinates, date and time of death (if known)', level=1)
    sec3(doc, 'c. Clinical and Circumstantial History:')
    bullet(doc, 'Probable cause of death (as reported by field staff)', level=1)
    bullet(doc, 'Clinical signs observed prior to death and any treatment given', level=1)
    bullet(doc, 'Circumstances of death — found in water, near railway track, near village, etc.', level=1)
    bullet(doc, 'Time elapsed since death (post-mortem interval) — critical for autolysis assessment', level=1)
    keybox(doc,
        'LEGAL REMINDER: PM examinations of Schedule I species (including Asian elephant — Elephas maximus) '
        'must be performed systematically, sincerely and seriously — not as a routine chore. '
        'Under WPA 1972 Section 49, improper or negligent necropsy of a protected species can be a '
        'criminal offence. Every finding must be documented and signed by the performing veterinarian.')
    page_break(doc)

    # ─── SECTION 4: PROTOCOL & EQUIPMENT ─────────────────────────────────────
    sec1(doc, '4.  Protocol for PM Examination & Equipment')
    img(doc, 6, 'Slide 6 — PM Protocol flowchart; field necropsy photographs', 13)
    img(doc, 7, 'Slide 7 — Equipment lists: documentation items and surgical instruments', 13)

    sec2(doc, '4.1  General Protocol — Step-by-Step Flow')
    dtable(doc,
        ['Step', 'Action', 'Notes'],
        [('1','Obtain letter from competent authority','DFO/CCF authorisation mandatory; legal protection for veterinarian'),
         ('2','Assess facilities available','Field vs laboratory setting; natural light vs artificial; water access'),
         ('3','Measurements','Body weight (if possible), body length, girth, tusk length, foot circumference'),
         ('4a','External Observations','Gross external examination before any incision'),
         ('4b','Internal Observations','Systematic cavity-by-cavity examination'),
         ('5','Gross Interpretation','Correlate all gross findings; form differential diagnosis list'),
         ('6','Sample Collection','Tissues for histopathology, microbiology, virology, toxicology'),
         ('7','Biological Samples for Lab','Package with correct fixatives; label with case ID, date, organ'),
         ('8a','Report Writing','Tentative cause of death with supporting findings'),
         ('8b','Determination of Cause of Death','Final cause pending lab results; interim report if needed')],
        widths=[1, 4.5, 11])

    sec2(doc, '4.2  General Considerations')
    bullet(doc, 'Postmortem MUST be performed in GOOD DAYLIGHT — artificial light misses subtle colour changes (haemorrhage, icterus, cyanosis)')
    bullet(doc, 'Standard LARGE ANIMAL necropsy instruments — domestic animal instruments are inadequate for elephant-scale tissue')
    bullet(doc, 'Logistics support: vehicle access, manpower for positioning, clear working area around carcass')
    bullet(doc, 'Protective clothing for ALL personnel: waterproof overalls, gloves (double-layered), goggles, face masks, gumboots')
    bullet(doc, 'Documentation kit: GPS, camera, video recorder, forms, ballpen')
    bullet(doc, 'Sample collection kit: fixatives (10% buffered formalin), preservatives (70% ethanol, DMSO), sterile tubes, swabs, biohazard bags')
    bullet(doc, 'Metal detector: mandatory — checks for bullets/pellets/metallic foreign bodies in carcass before incision')

    sec2(doc, '4.3  Equipment Required — Documentation Items')
    dtable(doc,
        ['S.No.', 'Item', 'Minimum No.'],
        [('1','Copy of Necropsy Protocol','1'),
         ('2','Hand-held GPS (for recording exact death location)','1'),
         ('3','Digital camera (with macro capability)','1'),
         ('4','Digital video camera','1'),
         ('5','Clip board','2'),
         ('6','Measuring tape (cloth/flexible)','1'),
         ('7','Plastic ruler 15 cm (clear markings, as scale bar in photos)','2'),
         ('8','Vernier callipers (for precise measurements: lamellae, lesion size)','1'),
         ('9','Portable weighing machine 250 kg capacity','1'),
         ('10','Necropsy format (pre-printed forms)','5'),
         ('11','Ballpen (permanent ink)','2'),
         ('12','Pencil rubber','1'),
         ('13','Metal detector','1')],
        widths=[1.5, 10.5, 2.5])

    sec2(doc, '4.4  Equipment Required — Surgical Instruments (Best SS Quality)')
    dtable(doc,
        ['S.No.', 'Instrument', 'Qty'],
        [('1','Sharp high-quality necropsy knife SS','4'),
         ('2','Skinning knife curved SS','2'),
         ('3','Autopsy knife curved SS','2'),
         ('4','Slicing knife 22 mm blade SS','1'),
         ('5','Knife sharpener stone or steel','1'),
         ('6','Bard Parker Handle and blades (No. 20, 22, 26 BP)','5 each'),
         ('7','Small plain forceps','2'),
         ('8','Artery Forceps straight 203 mm SS','2'),
         ('9','Dissecting Forceps 200 mm long SS','2'),
         ('10','Large Mayo dissecting scissors fine point 215 mm','2'),
         ('11','Bone Cutter Compound action 266 mm','1'),
         ('12','Hack saw or bone saw blade 254 mm','1'),
         ('13','Chisels 8½" × 1¼" (22.00 cm with blade 3.00 cm)','1'),
         ('14','Hammer Wrench end 200 mm','1'),
         ('15','Portable autopsy saw (Electric/battery)','1'),
         ('16','Axe (Roofing axe SS) 60 mm blade','1'),
         ('17','Spirit lamp SS or gas burner (for flaming instruments)','1'),
         ('18','Measuring tape SS','1')],
        widths=[1.5, 11, 2])
    page_break(doc)

    # ─── SECTION 5: EXTERNAL EXAMINATION ─────────────────────────────────────
    sec1(doc, '5.  External Examination')
    img(doc, 8, 'Slide 8 — External examination protocol; photograph of carcass with rigor mortis', 13)
    img(doc, 9, 'Slide 9 — External examination details: skin, orifices, temporal glands, foot pad', 13)

    sec2(doc, '5.1  History Collection')
    bullet(doc, 'Information on probable cause of death, clinical signs and treatment given, if known')
    bullet(doc, 'Information on circumstances of death — location type, proximity to human habitation, railway, powerlines')
    bullet(doc, 'Last seen alive time: critical for calculating post-mortem interval (PMI) and assessing autolysis')

    sec2(doc, '5.2  Initial External Survey')
    bullet(doc, 'BODY CONDITION: Record Body Condition Score (BCS) — prominent ribs, depression in lumbar/buccal region, distinct temporal fossa, loose skin = poor health/emaciation')
    bullet(doc, 'RIGOR MORTIS: Stiffening of the carcass; develops soon after death; assess degree')
    bullet(doc, 'EXTERNAL INJURIES: Characterize every wound, bruise, burn or cut — shape, size, depth, edges')
    bullet(doc, 'DOCUMENTATION: Photograph every external finding with scale bar BEFORE manipulation')
    bullet(doc, 'ANY OTHER OBSERVATION: Unusual posture, presence of scavengers, soil disturbance, drag marks')

    sec2(doc, '5.3  Detailed External Examination — 10-Point Protocol')
    sec3(doc, 'i. Sex Identification')
    bullet(doc, 'Examine male/female external organs — penis, scrotal region, vulva, mammary glands', level=1)
    bullet(doc, 'Determine if female is pregnant (abdominal distension, mammary engorgement), lactating, or dry', level=1)
    bullet(doc, 'Note: pregnant females may not show obvious abdominal enlargement until late gestation (22-month gestation)', level=1)

    sec3(doc, 'ii. Nutritional Status Assessment')
    bullet(doc, 'Prominent ribs visible/palpable → poor fat reserves → chronic undernutrition', level=1)
    bullet(doc, 'Depression in lumbar region → gluteal muscle wasting', level=1)
    bullet(doc, 'Depression in buccal (cheek) region → masseter muscle wasting', level=1)
    bullet(doc, 'Distinct temporal fossa ("sunken temples") → chronic poor condition', level=1)
    bullet(doc, 'Loose, wrinkled, excess skin → severe emaciation — skin hangs in folds', level=1)

    sec3(doc, 'iii. Fractures and Dislocations')
    bullet(doc, 'If possible, search for dislocations and fractures — especially limb bones, ribs, skull', level=1)
    bullet(doc, 'Fractures suggest HEC (Human-Elephant Conflict) injuries, fall, or train impact', level=1)

    sec3(doc, 'iv. Post-mortem Changes')
    bullet(doc, 'ALGOR MORTIS: Cooling of body to ambient temperature after death (rate varies with ambient temp)', level=1)
    bullet(doc, 'RIGOR MORTIS: Usually appears within 1–4 hours after death; lasts 16–24 hrs (up to 48 hrs); less marked in emaciated/septicaemic animals', level=1)
    bullet(doc, 'LIVOR MORTIS (Cadaveric Lividity / Hypostatic Congestion): Irregular patches in subcutaneous tissues on the side on which animal is lying — NORMAL POST-MORTEM CHANGE, not pathological haemorrhage', level=1)
    bullet(doc, 'AUTOLYTIC CHANGES: Decomposition begins immediately after death; rate depends on ambient moisture, temperature, and PMI', level=1)

    sec3(doc, 'v. Skin Examination')
    bullet(doc, 'External parasites: ticks (Haemaphysalis, Amblyomma spp.), lice', level=1)
    bullet(doc, 'Cutaneous filariasis: nodular swellings, especially around legs and ventral abdomen', level=1)
    bullet(doc, 'Pox lesions: characteristic crusted papulovesicular eruptions on trunk, ears, periocular skin', level=1)
    bullet(doc, 'Oedematous swellings: pitting oedema especially of dependent limbs (heart failure, hypoproteinaemia)', level=1)
    bullet(doc, 'Emphysematous crepitation: gas under skin — indicates post-mortem putrefaction or gas-forming bacterial infection (Clostridium)', level=1)
    bullet(doc, 'Burns: superficial (singeing of hair, skin hyperaemia) vs deep (charring) — critical in electrocution/lightning', level=1)
    bullet(doc, 'Warts: viral papillomata; common in young elephants, usually benign', level=1)
    bullet(doc, 'Visible mucous membranes (conjunctiva, oral): assess pallor (anaemia), congestion (septicaemia), cyanosis (respiratory/cardiac failure), inflammatory signs', level=1)

    sec3(doc, 'vi. Injury Examination')
    bullet(doc, 'Bullet wounds: entry (small, round, inverted edges) vs exit (larger, everted, irregular edges)', level=1)
    bullet(doc, 'Intra-species fighting injuries: tusk wounds in musth bulls; deep puncture lacerations', level=1)
    bullet(doc, 'Mauling by large carnivores: in calves — deep claw/bite marks from tiger/leopard', level=1)
    bullet(doc, 'Captive elephants: injuries inflicted by mahouts using ankush (bull hook) — distinctive puncture wounds, bruising', level=1)
    bullet(doc, 'Train impact injuries: severe bilateral fractures, visceral crush injuries, skin abrasion patterns consistent with vehicle contact', level=1)

    sec3(doc, 'vii. Dung Bolus of Rectum')
    bullet(doc, 'Examine dung bolus at the rectum — it is an indicator of:', level=1)
    bullet(doc, 'Digestive status: normal formed bolus (healthy) vs liquid/absent (diarrhoea, impaction)', level=2)
    bullet(doc, 'Dentition status: coarsely undigested material = poor molar function (dental exhaustion in old animals)', level=2)
    bullet(doc, 'Hydration status: dry, hard bolus = dehydration; moist/liquid = diarrhoea', level=2)
    bullet(doc, 'Parasites: tape worm proglottids, oxyurid eggs may be visible grossly', level=2)

    sec3(doc, 'viii. Natural Orifices')
    bullet(doc, 'Discharges from nostrils, mouth, ears, vulva/prepuce, anus — note colour, consistency, odour', level=1)
    bullet(doc, 'Oral cavity: examine for ulcers (Foot-and-Mouth Disease — FMD), haemorrhagic lesions (EEHV), anthrax lesions, foreign bodies', level=1)
    bullet(doc, 'EEHV oral lesions: characteristic haemorrhagic plaques on tongue, gingiva in young calves', level=1)

    sec3(doc, 'ix. Temporal Glands — Musth Examination')
    bullet(doc, 'Temporal glands (one on each side of head, between eye and ear)', level=1)
    bullet(doc, 'In musth: gland swollen, actively secreting dark oily substance — examine duct and gland for inflammation', level=1)
    bullet(doc, 'Abnormal temporal gland secretion (outside musth) may indicate infection, toxin, neurological disease', level=1)

    sec3(doc, 'x. Foot Pad and Nails')
    bullet(doc, 'Examine for injuries: cracks, abscesses, overgrowth (captive elephants)', level=1)
    bullet(doc, 'Healthy appearance: smooth, well-worn, even distribution of wear', level=1)
    bullet(doc, 'Abnormal: deep fissures, purulent discharge (osteomyelitis risk), disproportionate wear (lameness/musculoskeletal disease)', level=1)
    page_break(doc)

    # ─── SECTION 6: DENTITION ─────────────────────────────────────────────────
    sec1(doc, '6.  Dentition & Age Determination')
    img(doc, 10, 'Slide 10 — Molar eruption table and lamellae count for age estimation', 13)

    sec2(doc, '6.1  Unique Horizontal Molar Progression')
    para(doc,
        'Elephants develop six successive sets of molar teeth (M1–M6) on each side of the upper '
        'and lower jaw (24 molar positions total). Unlike vertical tooth replacement in all other '
        'mammals, elephants use HORIZONTAL MOLAR PROGRESSION: new molars develop at the posterior '
        'of the jaw and move FORWARD as older teeth wear down. Worn tooth fragments shed from the '
        'front of the jaw. When M6 (the final molar) is exhausted, the animal can no longer chew '
        'food — it progressively starves. This mechanism sets the biological maximum lifespan at '
        'approximately 60–70 years for Asian elephants.')

    sec2(doc, '6.2  Molar Eruption Table (Dr. A B Shrivastava / Shoshani & Eisenberg)')
    dtable(doc,
        ['Molar', 'Eruption Age', 'Lamellae (Enamel Plates)', 'Period of Active Use', 'Notes'],
        [('M1 (Deciduous)','~4 months','5 laminae','0–1 year','Shed rapidly; very small'),
         ('M2 (Deciduous)','~1–2 years','7 laminae','1–4 years','Overlap with M1 briefly'),
         ('M3','~6 years','10 laminae','4–15 years','First large permanent molar'),
         ('M4','~15 years','10 laminae (WIDER)','15–28 years','Same count as M3 — wider lamellae distinguish it'),
         ('M5','~28 years','12 laminae','28–47 years','Longest use; prime adulthood'),
         ('M6 (Final)','~47 years','13 laminae','47 years → death','Never replaced; exhaustion = death')],
        widths=[2, 2.5, 3.5, 3.5, 5])
    bullet(doc, 'At any time: maximum 2 molars in simultaneous wear on any one side of any one jaw')
    bullet(doc, 'PERMANENT TUSKS: protrude beyond the lips at approximately 30 months; continue growing throughout life')
    bullet(doc, 'Tusk growth rate: ~15–17 cm per year in bulls (variable); used as supplementary age indicator')
    bullet(doc, 'Makhna bulls (tuskless males): tusk alveoli small/absent; confirm maleness by other skull features')
    keybox(doc,
        'NECROPSY AGE ESTIMATION PROTOCOL:\n'
        '1. Open jaw; identify active molar (flat worn occlusal surface)\n'
        '2. Count enamel plates (lamellae) using a probe after cleaning\n'
        '3. Distinguish M3 (10 narrow plates) from M4 (10 WIDE plates) by lamellae width\n'
        '4. Assess wear gradient: anterior plates more worn = tooth in later stage\n'
        '5. Check for erupting molar behind active molar = near upper age of current set\n'
        '6. Cross-reference with body size, temporal hollowing, tusk size, skin wrinkling\n'
        '7. Give age as a RANGE with confidence: e.g., "M5 in wear, ~60% worn → est. 35–45 years"')
    page_break(doc)

    # ─── SECTION 7: INTERNAL ANATOMY ──────────────────────────────────────────
    sec1(doc, '7.  Internal Anatomy of the Elephant')
    img(doc, 11, 'Slide 11 — Labelled internal anatomy diagram (cross-sectional view)', 13)

    sec2(doc, '7.1  Overview of Internal Organ Systems')
    para(doc,
        'The internal anatomy of the elephant is broadly similar to other large mammals but with '
        'several critically important unique features that directly affect necropsy technique, '
        'interpretation of findings, and differential diagnosis.')
    dtable(doc,
        ['System', 'Key Organs', 'Elephant-Specific Notes'],
        [('Respiratory','Trachea, Lungs (+ Pleura)','NO pleural space — lungs fused to chest wall; diaphragm-only breathing; bifid heart apex'),
         ('Cardiovascular','Heart (12–21 kg), major vessels','Bifid (double-pointed) cardiac apex — NORMAL; proboscideal artery prominent'),
         ('Digestive','Pharynx, oesophagus, stomach, intestines, caecum, rectum, liver, pancreas','Simple (monogastric) stomach 100–140 cm long; cecum large ~90 L; GI tract >20 m'),
         ('Urogenital','Kidneys, bladder, uterus/testes','Kidneys multi-lobulated (renculated); testes permanently abdominal — no scrotal descent'),
         ('Nervous','Brain, spinal cord','Largest brain of any land mammal — 4–6 kg; well-developed temporal lobes'),
         ('Musculoskeletal','19–20 ribs, spine, limbs, skull','No pleural space; pneumatised skull; 19–20 thoracic vertebrae'),
         ('Lymphatic','Superficial + deep lymph nodes','Standard large mammal pattern; key nodes for TB/EEHV diagnosis')],
        widths=[3, 4.5, 9])

    sec2(doc, '7.2  Unique Anatomical Features Critical for Necropsy')
    bullet(doc, 'PLEURAL FUSION: No pleural space — firm lung-chest wall adhesion is NORMAL (not pleuritis); no thoracocentesis possible')
    bullet(doc, 'BIFID HEART APEX: Double-pointed cardiac apex — characteristic of elephants; do NOT record as cardiac anomaly')
    bullet(doc, 'ABDOMINAL TESTES: Male elephants retain testes permanently in the abdomen adjacent to kidneys — they do NOT descend into a scrotum (cryptorchidism in other species, but NORMAL in elephants)')
    bullet(doc, 'TOENAIL COUNT: Asian elephant — 5 toenails front, 4 rear (commonly); African — 4 front, 3 rear')
    bullet(doc, 'CARDIAC WEIGHT: 12–21 kg — enormous; heart/body weight ratio similar to other mammals')
    bullet(doc, 'TEMPORAL GLAND: Between eye and ear; secretes in musth; bilateral; examine at necropsy')
    page_break(doc)

    # ─── SECTION 8: SKINNING & INTERNAL EXAMINATION ────────────────────────────
    sec1(doc, '8.  Skinning of the Carcass & Internal Examination Procedure')
    img(doc, 12, 'Slide 12 — Field photographs: skinning of elephant carcass with team', 13)

    sec2(doc, '8.1  Skinning Technique')
    para(doc,
        'In a healthy animal, the elephant skin is THICK but FLEXIBLE and easily moved over the '
        'underlying tissues. In emaciated or diseased animals, the skin may adhere tightly. Proper '
        'skinning of one lateral surface is the standard elephant necropsy approach in field conditions '
        'where the carcass cannot be turned.')
    bullet(doc, 'Position carcass in lateral recumbency (right or left — whichever is accessible)')
    bullet(doc, 'Make a long median incision from the angle of the mandible along the dorsal midline to the tail base')
    bullet(doc, 'Reflect the skin over the ENTIRE lateral thoracic region and extending to the lower abdominal and other suspected regions')
    bullet(doc, 'Examine the SUBCUTANEOUS TISSUES immediately: look for abscesses, wounds, haemorrhages, oedema, parasitic cysts')
    bullet(doc, 'Examine SUPERFICIAL MUSCLES: haemorrhage patterns (electrocution), atrophy (chronic disease), abscesses')
    bullet(doc, 'Identify and incise SUPERFICIAL LYMPH NODES: submandibular, parotid, prescapular, femoral')
    bullet(doc, 'Healthy lymph node: small, firm, pale/cream coloured')
    bullet(doc, 'Pathological: enlarged, haemorrhagic, caseous (TB), gelatinous (oedema), suppurative')

    sec2(doc, '8.2  Opening the Thoracic Cavity')
    bullet(doc, 'The elephant has 19–20 (Asian) or 21 (African) pairs of ribs forming the thoracic cage')
    bullet(doc, 'Cut through the intercostal muscles and ribs on the lateral surface')
    bullet(doc, 'Observe: lungs WILL appear firmly attached to the chest wall — this is NORMAL (fused pleura)')
    bullet(doc, 'Any fluid between lung surface and chest wall is PATHOLOGICAL')
    bullet(doc, 'Examine the pericardial sac before opening: distension, haemopericardium, fibrinous deposits')
    bullet(doc, 'Remove the heart: examine size, weight, epicardium, myocardium, endocardium, valves')
    bullet(doc, 'Examine the trachea: mucus, parasites (Mammomonogamus), foreign bodies')
    bullet(doc, 'Examine lungs: colour, consistency, consolidation areas, parasites (Protostrongylus), tuberculosis nodules')

    sec2(doc, '8.3  Opening the Abdominal Cavity')
    para(doc,
        'The elephant has approximately 20 pairs of ribs. Draw a vertical straight line between the last rib '
        'and the lower abdominal region. Make a vertical incision down to the ground surface and open the cavity.')
    bullet(doc, 'On opening: note smell, colour of peritoneal fluid, presence of fibrin strands, blood')
    bullet(doc, 'Examine the omentum and mesentery for fat stores (good condition = fat-laden)')
    bullet(doc, 'Identify all organs in situ before removing any')
    bullet(doc, 'Photograph the opened cavity with scale bar')
    page_break(doc)

    # ─── SECTION 9: DIGESTIVE SYSTEM ──────────────────────────────────────────
    sec1(doc, '9.  Digestive System Examination')

    sec2(doc, '9.1  Anatomy of the Elephant Digestive System')
    para(doc,
        'The elephant is a MONOGASTRIC (simple-stomached) herbivore — a hindgut fermenter. Despite '
        'an enormous intake (150–300 kg fresh forage/day), the digestive efficiency is relatively '
        'low (~40–45%), which necessitates near-continuous feeding.')
    dtable(doc,
        ['Organ / Segment', 'Key Features', 'Necropsy Examination Points'],
        [('Pharynx','Common passage for food and air','Foreign bodies, ulcers, FMD lesions'),
         ('Oesophagus','Long; may show strictures in older animals','Perforation, parasites, foreign bodies'),
         ('Stomach (monogastric)','100–140 cm long; 40 cm diameter; simple sac','Contents: moisture, food material, gut parasites; focal ulcerations or gastritis; Gongylonema parasites in mucosa'),
         ('Small Intestine','Very long; site of primary digestion and absorption','Intussusception, volvulus; haemorrhage (salmonellosis); parasites (Quilonia, Pfenderius)'),
         ('Caecum','LARGE — ~90 L capacity; primary site of hindgut fermentation','Bloat/tympany; impaction; parasitic nodules'),
         ('Large Intestine','Long; water absorption','Colitis, ulcerations; tapeworm segments'),
         ('Rectum','Terminal; dung bolus formed here','Diarrhoea, impaction, rectal prolapse'),
         ('Liver','36–45 kg; multilobulated','Abscesses, fatty infiltration, TB granulomas, fascioliasis'),
         ('Pancreas','Elongated; associated with duodenum','Pancreatitis; parasitic cysts (uncommon)'),
         ('Salivary Glands','Parotid, mandibular, sublingual','EEHV necrosis; ranula'),
         ('Teeth / Tongue','Molar teeth — primary age indicator','See Section 6; tongue for EEHV lesions, FMD')],
        widths=[3.5, 5, 8])

    sec2(doc, '9.2  Stomach Examination Protocol')
    bullet(doc, 'Open along the greater curvature and drain contents into container')
    bullet(doc, 'Examine contents for: food material type (normal foraging vs abnormal items), moisture content, gut parasites (Physaloptera, Gongylonema), protozoal oocysts')
    bullet(doc, 'Examine mucosa for: focal ulcerations, diffuse gastritis, haemorrhage, parasitic nodules')
    bullet(doc, 'pH of gastric contents: pH 1.5–3.0 normal; elevated pH = poor acid secretion / alkali ingestion')
    bullet(doc, 'Collect swabs from gastric mucosa for bacterial culture (Salmonella, Clostridium, Campylobacter)')
    page_break(doc)

    # ─── SECTION 10: SYSTEMATIC EXAMINATION ───────────────────────────────────
    sec1(doc, '10.  Systematic Organ Examination')
    img(doc, 13, 'Slide 13 — Systematic examination checklist; lymph node locations', 13)

    sec2(doc, '10.1  Respiratory System')
    bullet(doc, 'TRACHEA: large-diameter; inspect mucosa for haemorrhage, parasites (Mammomonogamus elephantis), exudate')
    bullet(doc, 'LUNGS: examine each lobe; colour (pink-grey normal; red/consolidated = pneumonia; pale/emphysematous; dark/hyperaemic); texture (spongy vs firm); cut surface findings')
    bullet(doc, 'TB lesions: grey-white focal caseous nodules distributed throughout lung parenchyma — MUST be sampled for Mycobacterium tuberculosis complex culture and PCR')
    bullet(doc, 'EEHV lesions (calves): haemorrhagic/necrotic foci in lung parenchyma; endothelial cell necrosis on histopathology')
    bullet(doc, 'Collect: lung tissue in formalin (histopathology) and fresh (virology/microbiology); tracheal swab; bronchial lavage')

    sec2(doc, '10.2  Urogenital System')
    bullet(doc, 'KIDNEYS: multi-lobulated (renculated structure); examine for infarcts, abscesses, nephritis, TB granulomas')
    bullet(doc, 'BLADDER: examine for cystitis, haemorrhage, calculi')
    bullet(doc, 'UTERUS (females): check gravidity; examine endometrium, myometrium; sample for reproductive pathogens')
    bullet(doc, 'TESTES (males): located ABDOMINALLY adjacent to kidneys — normal; examine for orchitis, tumour')
    bullet(doc, 'ADRENAL GLANDS: enlarged/haemorrhagic in septicaemia; cortical atrophy in chronic disease')

    sec2(doc, '10.3  Musculoskeletal System')
    bullet(doc, 'MUSCLES: examine for pallor (myopathy), haemorrhage (trauma/electrocution), oedema, calcification (nutritional myopathy — white muscle disease)')
    bullet(doc, 'BONES: long bone fractures; vertebral fractures/dislocations; periosteal reactions; osteomyelitis (common in captive foot pad disease)')
    bullet(doc, 'JOINTS: examine for septic arthritis, degenerative joint disease (older animals)')

    sec2(doc, '10.4  Reproductive System')
    bullet(doc, 'FEMALE: examine uterus (bifurcate at cervix into two uterine horns); if pregnant: fetal age, placenta')
    bullet(doc, 'MALE: testes abdominally; epididymis; accessory glands; penis sheath examination')
    bullet(doc, 'Reproductive tract pathology: endometritis, pyometra, tumours (uncommon), trauma')

    sec2(doc, '10.5  Nervous System')
    bullet(doc, 'BRAIN: heaviest of any land mammal (4–6 kg); access by removing calvarium with saw')
    bullet(doc, 'Examine for: haemorrhage (epidural, subdural, intraparenchymal), oedema, softening (encephalitis), Negri bodies (rabies — histopathology mandatory)')
    bullet(doc, 'SPINAL CORD: examine at multiple levels for myelitis, haemorrhage, compression')
    bullet(doc, 'Collect: brain stem, hippocampus, cerebellum in 10% buffered formalin for histopathology; fresh brain for virology (rabies FA test)')
    page_break(doc)

    # ─── SECTION 11: LYMPH NODES ──────────────────────────────────────────────
    sec1(doc, '11.  Lymph Node Examination')
    img(doc, 14, 'Slide 14 — Histopathology: intra-nuclear inclusion bodies in EEHV; lymph node locations', 13)

    sec2(doc, '11.1  Importance in Elephant PM Examination')
    para(doc,
        'Superficial lymph nodes are critically important in elephant postmortem examination for '
        'detecting infectious diseases such as Tuberculosis (TB) and Elephant Endotheliotropic '
        'Herpesvirus (EEHV). Lymph node locations in the elephant are largely similar to other large '
        'mammals, but their depth under the thick skin makes external palpation in live animals '
        'difficult — they are more accessible at necropsy.')

    sec2(doc, '11.2  Superficial Lymph Nodes')
    dtable(doc,
        ['Lymph Node', 'Location', 'Diseases to Check'],
        [('Mandibular (Submandibular)','Ventral border of lower jaw, just under skin; examined after incising between mandibles during oral cavity inspection','TB (caseous granulomas); strangles-like infection; EEHV'),
         ('Parotid','Just below the ear, near the parotid salivary gland','Parotid abscess; systemic disease; TB'),
         ('Superficial Cervical','Lateral side of neck, slightly cranial to shoulder','TB; trypanosomiasis; systemic infection'),
         ('Prescapular','Just ahead of the shoulder joint','Systemic disease screening; TB; lymphoma'),
         ('Femoral','Area close to head of femur (inguinal region)','Pelvic/hindlimb infections; TB; lymphosarcoma')],
        widths=[3.5, 5, 8])

    sec2(doc, '11.3  Deep / Internal Lymph Nodes')
    dtable(doc,
        ['Lymph Node', 'Location', 'Key Diagnostic Use'],
        [('Bronchial (Tracheobronchial)','Junction where bronchi split from trachea (carina)','MANDATORY sample for mycobacterial culture (TB); EEHV PCR; systemic viral disease'),
         ('Hepatic & Splenic','Near liver and spleen, respectively','Systemic infection or haemorrhage; TB hepatic involvement; EEHV'),
         ('Mesenteric','Clusters in the mesentery of small/large intestine','Intestinal infections (Salmonella, Johne disease-like); enteritis; parasitic disease')],
        widths=[3.5, 5, 8])

    sec2(doc, '11.4  Histopathology — EEHV Inclusion Bodies')
    para(doc,
        'Elephant Endotheliotropic Herpesvirus (EEHV) is the leading infectious cause of death in '
        'captive elephant calves worldwide. The definitive histopathological diagnosis is the '
        'identification of INTRA-NUCLEAR INCLUSION BODIES (Cowdry Type A) in vascular endothelial '
        'cells of multiple organs — most consistently in heart, tongue, trunk skin, liver, and spleen.')
    bullet(doc, 'Gross: petechial/ecchymotic haemorrhages on multiple serosal surfaces; haemopericardium; oedematous head and neck (particularly EEHV1A)')
    bullet(doc, 'Histopathology: swollen endothelial cells with large eosinophilic intranuclear inclusion bodies surrounded by clear halo (arrow markers in slide)')
    bullet(doc, 'PCR confirmation: trunk wash, blood, and tissue samples — send fresh (unfixed) for EEHV DNA PCR')
    bullet(doc, 'Seven EEHV species known (EEHV1–7); EEHV1A and EEHV4 most commonly fatal')
    bullet(doc, 'Vaccine development: T cell-inducing heterologous vaccines are currently under trial (as noted in slide)')
    keybox(doc,
        'EEHV SAMPLING PROTOCOL at necropsy:\n'
        '• Trunk wash / nasal swab (fresh) → EEHV PCR\n'
        '• Blood (EDTA) → haematology + EEHV PCR\n'
        '• Heart, tongue, trunk skin, liver, spleen → 10% formalin (histopathology)\n'
        '• Heart, tongue, trunk skin (fresh, snap-frozen) → EEHV PCR / EM\n'
        '• Lymph nodes (fresh) → EEHV PCR\n'
        '• Median survival after clinical signs appear: ~36 hours — early sampling is critical', danger=True)
    page_break(doc)

    # ─── SECTION 12: DIFFERENTIAL DIAGNOSIS ───────────────────────────────────
    sec1(doc, '12.  Differential Diagnosis — Diseases Causing Sudden Death')
    img(doc, 15, 'Slide 15 — Differential diagnosis table; Rabies case at Panna Tiger Reserve', 13)

    sec2(doc, '12.1  Diseases with Sudden Onset and Rapid Death')
    dtable(doc,
        ['Disease', 'Causative Agent', 'Key PM Findings', 'Samples Required'],
        [('Haemorrhagic Septicaemia','Pasteurella multocida type B (or E)','Extensive haemorrhagic areas in subcutaneous tissues, serous surfaces, lymph nodes; pulmonary oedema; splenomegaly','Blood (anaerobic); lung, spleen, liver for culture; fresh tissue for PCR'),
         ('Salmonellosis','Salmonella spp. (S. typhimurium, S. dublin)','Haemorrhagic enteritis; watery diarrhoea with or without blood; mesenteric lymph node haemorrhage; hepatic necrosis','Intestinal content; mesenteric lymph nodes; blood for culture; faeces for PCR'),
         ('Enterotoxaemia','Clostridium perfringens type C/D','Haemorrhagic enteritis; diarrhoea leads to dehydration and death; gas in intestinal lumen; rapid autolysis','Intestinal content (fresh, frozen) for toxin ELISA; intestinal mucosa for PCR'),
         ('Encephalomyocarditis (EMC)','EMC Virus (Cardiovirus)','Cardiac necrosis; white/pale foci in myocardium; encephalitis; respiratory distress sometimes','Heart (fresh + formalin); brain (fresh + formalin); blood for serology and PCR'),
         ('Rabies','Rabies Lyssavirus','Behavioural signs (below); brain stem Negri bodies; non-suppurative encephalitis','Brain stem (fresh, frozen) for FA test; brain in formalin for Negri body histology'),
         ('Anthrax','Bacillus anthracis','Sudden death; blood-stained discharges from orifices; splenomegaly; blood fails to clot; DO NOT OPEN CARCASS until anthrax excluded','Blood smear (Giemsa/McFadyean stain); peripheral blood culture; CAUTION — zoonosis')],
        widths=[3.5, 3, 5.5, 4.5])

    sec2(doc, '12.2  Case Report — Rabies in Semi-Captive Elephant at Panna Tiger Reserve')
    para(doc,
        'Prof. Dr. Shrivastava documented a confirmed case of Rabies in a semi-captive elephant at '
        'Panna Tiger Reserve — one of the very few documented cases of rabies in elephants. The '
        'clinical progression was rapid and characteristic:')
    dtable(doc,
        ['Day', 'Clinical Signs Observed'],
        [('Day 1 (Initially)','Off feed; restlessness; drooling of saliva (hypersalivation)'),
         ('Day 3','Restricted jaw movement; protrusion of tongue (progressive paresis)'),
         ('Day 4','Hyperaemic conjunctiva (bloodshot eyes — autonomic involvement)'),
         ('Day 5','Hydrophobia; loud but changed, distorted trumpeting (laryngeal paralysis)'),
         ('Day 6','Lateral recumbency and death (ascending paralysis complete)'),
         ('Post-mortem','Proper carcass disposal mandatory — deep burial or incineration; carcass biohazardous')],
        widths=[3, 13.5])
    bullet(doc, 'Rabies diagnosis in elephant: histopathology for Negri bodies in hippocampus and cerebellum; direct FA test on brain stem')
    bullet(doc, 'Source of infection: likely bite from a rabid domestic dog (common vector in India)')
    bullet(doc, 'ZOONOSIS RISK: Rabies virus present in saliva; ALL personnel who had contact must receive post-exposure prophylaxis (PEP) immediately')
    page_break(doc)

    # ─── SECTION 13: TUBERCULOSIS ──────────────────────────────────────────────
    sec1(doc, '13.  Tuberculosis in Free-Range Asian Elephants')
    img(doc, 16, 'Slide 16 — Gross lesions of TB in free-range Asian elephant (photos by Dr. Parag Nigam); decomposed carcass PM', 13)

    sec2(doc, '13.1  TB in Elephants — Overview')
    para(doc,
        'Tuberculosis caused by Mycobacterium tuberculosis (human strain) is increasingly documented '
        'in both captive and free-ranging Asian elephants in India. The disease is a significant '
        'zoonotic risk to mahouts, forest staff, and veterinarians. TB in elephants typically '
        'presents as a chronic, progressive disease with non-specific clinical signs until advanced stages.')

    sec2(doc, '13.2  Gross PM Lesions of Elephant TB')
    bullet(doc, 'LUNGS: Multiple grey-white to caseous nodules (granulomas) of varying size distributed throughout parenchyma — typically 5 mm to 5 cm diameter')
    bullet(doc, 'PLEURA/PERITONEUM: Miliary (millet-seed) nodules on serosal surfaces; fibrous adhesions')
    bullet(doc, 'LIVER: Caseous granulomas; hepatomegaly')
    bullet(doc, 'LYMPH NODES: Enlarged, caseous, calcified (in chronic cases); tracheobronchial LN most commonly affected')
    bullet(doc, 'As shown in the slide: lung cross-section with multiple pale nodular granulomas throughout the parenchyma (right image); pleural/peritoneal involvement (left lower image)')

    sec2(doc, '13.3  TB Diagnostic Protocol at Necropsy')
    bullet(doc, 'Collect tracheobronchial lymph nodes (fresh + formalin) as PRIORITY — highest mycobacterial burden')
    bullet(doc, 'Collect lung tissue from multiple nodular lesions (fresh + formalin)')
    bullet(doc, 'Nasal/trunk wash (fresh) — for culture and PCR; useful for inter-elephant transmission assessment')
    bullet(doc, 'Impression smears from cut lymph node: Ziehl-Neelsen stain for acid-fast bacilli')
    bullet(doc, 'Samples to ICAR-NRC on Mithun / ICAR-IVRI for culture (8–12 weeks incubation) + PCR (species confirmation)')
    bullet(doc, 'TB lesions in decomposed carcass: caseous/calcified nodules persist — collect even from advanced autolysed carcasses')
    keybox(doc,
        'ZOONOSIS WARNING — ELEPHANT TB:\n'
        'Mycobacterium tuberculosis in elephants is the HUMAN strain — it is fully infectious to humans '
        'by respiratory route. All PM personnel must wear:\n'
        '• N95 or higher respiratory protection (NOT surgical mask)\n'
        '• Double gloves + waterproof gown\n'
        '• Eye protection (goggles)\n'
        'All personnel with elephant contact should undergo regular tuberculin test and chest X-ray. '
        'Post-exposure notification mandatory if contact with open TB lesions occurred.', danger=True)
    page_break(doc)

    # ─── SECTION 14: HCN POISONING ────────────────────────────────────────────
    sec1(doc, '14.  Case Study — HCN Poisoning in Asian Elephants')
    img(doc, 19, 'Slide 19 — HCN poisoning case report (Zoo Print 2010); felicitation of Dr. Shrivastava', 13)

    sec2(doc, '14.1  Hydrocyanic Acid (HCN) Poisoning')
    para(doc,
        'Hydrocyanic acid (prussic acid) poisoning in domestic and captive herbivores is commonly '
        'caused by consumption of cyanogenic glycoside-containing plants, especially Sorghum '
        '(jowar/sorghum bicolor) and Sudangrass. The cyanogenic glycoside content varies by '
        'plant part, season (highest in young shoots after wilting/frosting), and growth stage. '
        'When ingested, plant enzymes release HCN which binds cytochrome oxidase → inhibits '
        'cellular respiration → rapid death.')

    sec2(doc, '14.2  Case — Five Adult Captive Elephants, Circus, Tahalpur')
    bullet(doc, 'Five adult captive elephants were fed large quantities of fresh Jowar (Sorghum) during their circus stay — animals were not accustomed to Sorghum')
    bullet(doc, 'Clinical signs: restlessness, diarrhoea — elephants could not be controlled; condition gradually became serious')
    bullet(doc, 'One aged elephant became critical; the other four showed early signs of recovery')
    bullet(doc, 'Treatment given: Sodium thiosulphate 50 gm dissolved in water and given orally through drinking water; repeated after 12 hours')
    bullet(doc, 'Additional treatment: 1 litre 5% dextrose saline + Rice and Tab Diulin through rectum via tube')
    bullet(doc, 'Outcome: 5th elephant showed signs of recovery next morning; started drinking water and eating fresh green grass')
    bullet(doc, 'Body temperature during illness: 97–98°F (slightly subnormal — characteristic of HCN)')
    bullet(doc, 'Source publication: Zoo Print vol. xxv, 6 June 2010')

    sec2(doc, '14.3  HCN Poisoning — PM Findings')
    bullet(doc, 'Bright cherry-red colour of blood and tissues (due to cyanmethaemoglobin formation) — pathognomonic')
    bullet(doc, 'Smell of bitter almonds from stomach contents and blood')
    bullet(doc, 'Rapid rigor mortis (lactic acid accumulation inhibited)')
    bullet(doc, 'Congested viscera; petechial haemorrhages')
    bullet(doc, 'Diagnosis: Chemical analysis of stomach contents / blood for HCN/cyanide levels')
    keybox(doc,
        'TOXICOLOGY SAMPLING for HCN POISONING:\n'
        '• Stomach contents (sealed container, refrigerated or frozen)\n'
        '• Liver and kidney (50g each, frozen)\n'
        '• Blood (10 mL, fluoride-oxalate tube, frozen)\n'
        '• Plant material suspected as source (labelled)\n'
        'Send to forensic/toxicology laboratory (IVRI Izatnagar / FSL Sagar) with suspected diagnosis.')
    page_break(doc)

    # ─── SECTION 15: REFERENCES ───────────────────────────────────────────────
    sec1(doc, '15.  Key References & Recommended Reading')

    sec2(doc, '15.1  Works by Prof. Dr. A B Shrivastava')
    bullet(doc, 'Shrivastav AB & Sharma RK (2008). A Manual of Wildlife Health Management in Protected Areas. CVAH, JNKVV, Jabalpur')
    bullet(doc, 'Shrivastav AB & Singh KP (Ed.) (2011). Big Cats. InTech Open Access Publisher')
    bullet(doc, 'Shrivastav AB & Nigam P (2019). Learning from Dead: Necropsy Essentials for Large Felids. Published, Jabalpur')
    bullet(doc, 'Shrivastav AB (2020). Manual on Postmortem Examination of Felids. NDVSU, Jabalpur')
    bullet(doc, 'Nigam P, Habib J & Pandey H (Ed.) (2021). Caring for Elephants: Managing Health & Welfare in Captivity')
    bullet(doc, 'MoEFCC/WII (2020). Necropsy and Carcass Disposal of Asian Elephant: Recommended Operating Procedure. GoI')
    bullet(doc, 'Shrivastav AB (2010). Management of Hydrocyanic Acid Poisoning in Asian Elephants. Zoo Print vol. xxv, 6 June 2010')

    sec2(doc, '15.2  Peer-Reviewed Literature')
    bullet(doc, 'Fowler ME & Mikota SK (2006). Biology, Medicine and Surgery of Elephants. Blackwell Publishing, Iowa')
    bullet(doc, 'Mikota SK et al. (2001). Elephants TB. International Zoo Yearbook 37: 122–135')
    bullet(doc, 'Richman LK et al. (2000). Novel Endotheliotropic Herpesviruses Fatal for Asian and African Elephants. Science 288: 1171–1176')
    bullet(doc, 'West JB (2001). Anatomical Basis for Unusual Properties of the Lung in an Extreme Environment. Respiration Physiology 127: 1–11')
    bullet(doc, 'Sukumar R (2003). The Living Elephants: Evolutionary Ecology, Behaviour & Conservation. Oxford University Press')
    bullet(doc, 'Vidya TNC & Sukumar R (2005). Social Organisation of Asian Elephant. Proceedings Royal Society London B 272: 3011–3020')
    bullet(doc, 'MoEFCC (2017). Gajah: Securing the Future for Elephants in India. Project Elephant, Government of India')
    bullet(doc, 'Lynsdale CL et al. (2024). Elephant molar eruption timeline. Scientific Reports, PMC update')
    bullet(doc, 'Loo AHB et al. (2024). Sexual dimorphism in Asian elephant skeletal morphology. PMC12383435')

    para(doc,
        'Notes prepared from the presentation of Prof. Dr. A B Shrivastava (06-06-2026), elaborated '
        'with peer-reviewed literature and current guidelines. Training Program: Essentials for '
        'Mortality Investigation of Asian Elephant, Chhattisgarh Forest Department, 5–6 June 2026, Raigarh.',
        size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(OUT_D)
    print(f'  ✓  {OUT_D}  ({os.path.getsize(OUT_D)//1024} KB)')


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD PDF
# ══════════════════════════════════════════════════════════════════════════════
def build_pdf():
    W, H = A4
    doc = SimpleDocTemplate(OUT_P, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.8*cm, bottomMargin=1.8*cm)
    styles = getSampleStyleSheet()
    story = []

    DK = colors.HexColor('#1B4332'); MD = colors.HexColor('#2D6A4F')
    LT = colors.HexColor('#52B788'); TN = colors.HexColor('#D8F3DC')
    T2 = colors.HexColor('#EAF7EE'); RD = colors.HexColor('#FAE0D8')
    WH = colors.white; MT = colors.HexColor('#555555')
    DRD = colors.HexColor('#8B0000'); NY = colors.HexColor('#1A2E44')

    def ST(name, **kw):
        s = ParagraphStyle(name, parent=styles['Normal'])
        for k, v in kw.items(): setattr(s, k, v)
        return s

    sH1  = ST('H1', fontSize=12, textColor=WH, leading=16, fontName='Helvetica-Bold')
    sH2  = ST('H2', fontSize=10, textColor=WH, leading=13, fontName='Helvetica-Bold')
    sH3  = ST('H3', fontSize=9.5, textColor=MD, leading=13, fontName='Helvetica-Bold', spaceAfter=2)
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
    sTIT = ST('TT', fontSize=18, textColor=WH, leading=24, fontName='Helvetica-Bold', alignment=TA_CENTER)
    sSUB = ST('SB', fontSize=10, textColor=LT, leading=14, fontName='Helvetica-Oblique', alignment=TA_CENTER)
    sSB2 = ST('SC', fontSize=9, textColor=WH, leading=12, fontName='Helvetica-Bold', alignment=TA_CENTER)
    CW = W - 4*cm

    def h1(txt):
        story.append(Spacer(1, 0.2*cm))
        t = Table([[Paragraph(txt, sH1)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                               ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                               ('LEFTPADDING',(0,0),(-1,-1),8)]))
        story.append(t); story.append(Spacer(1, 0.12*cm))

    def h2(txt):
        story.append(Spacer(1, 0.1*cm))
        t = Table([[Paragraph(txt, sH2)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),MD),
                               ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
                               ('LEFTPADDING',(0,0),(-1,-1),6)]))
        story.append(t); story.append(Spacer(1, 0.08*cm))

    def h3(txt):
        story.append(Paragraph(txt, sH3))

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
        story.append(t); story.append(Spacer(1, 0.1*cm))

    def pi(n, cap='', w=13):
        path = slide(n)
        if os.path.exists(path):
            story.append(Spacer(1, 0.15*cm))
            ri = RLImage(path, width=w*cm, height=w*cm*0.65)
            ri.hAlign = 'CENTER'; story.append(ri)
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
        story.append(t); story.append(Spacer(1, 0.15*cm))

    def hr(): story.append(HRFlowable(width='100%', thickness=0.5, color=LT, spaceAfter=4))

    # TITLE
    tb = Table([[Paragraph('LEARNING FROM DEAD', sSB2)],
                [Paragraph('Postmortem Examination of Asian Elephant', sTIT)],
                [Paragraph('Comprehensive Study Notes with Slide Images', sSUB)],
                [Paragraph('Prof. Dr. A B Shrivastava  ·  Founder Director, School of Wildlife Forensic and Health', sSUB)],
                [Paragraph('Nanaji Deshmukh Veterinary Science University, Jabalpur 482001, M.P.', sSUB)]],
               colWidths=[CW])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),
                             ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
                             ('LEFTPADDING',(0,0),(-1,-1),12)]))
    story.append(Spacer(1, 0.3*cm)); story.append(tb); story.append(Spacer(1, 0.25*cm))
    kyb('Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  ·  Technical Support: WII Dehradun')
    pi(1, 'Slide 1 — Title slide: NDVSU Jabalpur and credentials of Prof. Dr. A B Shrivastava', 13)
    story.append(PageBreak())

    # S1
    h1('1.  Wildlife Health Management — Foundations')
    pi(2, 'Slide 2 — Wildlife Health Management: Multidisciplinary Approach diagram', 13)
    h2('1.1  Definition')
    bdy('Wildlife Health Management is a branch of Veterinary Science dealing with veterinary interventions in wild fauna — health monitoring, disease management, scientific immobilisation, and habitat manipulation to achieve conservation strategies for healthy populations. (Shrivastav, 2010)')
    h2('1.2  Multidisciplinary Disciplines')
    dtbl(['Discipline','Relevance to Elephant Health'],
         [('Wildlife Pathology','Core of mortality investigation; gross and histopathological disease ID'),
          ('Wildlife Anatomy','Normal vs pathological anatomy at necropsy; species-specific features'),
          ('Wildlife Clinics & Ethology','Pre-mortem clinical signs; normal behavioural baselines'),
          ('Wildlife Parasitology','Internal/external parasite ID; zoonotic risk'),
          ('Genetic Mgt of Small Populations','Conservation genetics; inbreeding; PVA'),
          ('Animal Biotechnology','PCR diagnostics; DNA forensics; EEHV vaccine development'),
          ('Wildlife Microbiology','Bacterial/viral culture; AMR profiling; zoonosis'),
          ('Wildlife Nutrition','Nutritional deficiency diseases; body condition scoring')],
         wds=[5, 12])
    kyb('KEY: Wildlife Health is often ignored — yet every elephant death is data that can protect the living population. Systematic necropsy is not optional — it is a conservation imperative. "Carcass never tells lie." — Dr Satpati')
    story.append(PageBreak())

    # S2
    h1('2.  History of Postmortem Examination')
    pi(3, 'Slide 3 — Introduction: Necropsy (animals) vs Autopsy (humans); standard protocol requirements', 13)
    pi(4, 'Slide 4 — Professional quotes on necropsy importance; "Carcass never tells lie" — Dr Satpati', 13)
    h2('2.1  Historical Milestones')
    dtbl(['Era / Person','Contribution'],
         [('Sushruta, 2500 BC','Sushruta Samhita: systematic human cadaver dissection in ancient India'),
          ('Roman physician Antistius, 44 BC','Earliest documented autopsy — Julius Caesar; 23 wounds identified; first forensic pathology'),
          ('Catholic Church, 1410','Autopsy on Pope Alexander V to determine poisoning; medicolegal precedent'),
          ('Surgeon Bulkley, 1680','First documented postmortem in India'),
          ('Modern Era','Standardised protocols; histopathology; molecular diagnostics; digital documentation')],
         wds=[4, 13])
    h2('2.2  Key Principles')
    pb('NECROPSY (animals & birds) vs AUTOPSY (humans) — same process, different terminology')
    pb('PM is an ART of disease diagnosis — scientific and systematic approach is essential')
    pb('Gross findings + history alone may be insufficient — laboratory confirmation required')
    pb('Badly putrefied samples or fresh samples in wrong preservatives are useless')
    pb('Staff: 2–3 vets + 4 supporting + 1 photographer + 1 sample collection personnel')
    story.append(PageBreak())

    # S3
    h1('3.  Necropsy Objectives & Pre-Necropsy Evaluation')
    pi(5, 'Slide 5 — Necropsy Objectives; Pre-necropsy Evaluation checklist', 13)
    h2('3.1  Necropsy Objectives')
    pb('To know ALL possible lesions of disease or abnormality')
    pb('To CORRELATE lesions with clinical and laboratory findings')
    pb('To understand the SEQUENCE of disease events')
    pb('To PREVENT or CONTROL disease in the healthy living population')
    h2('3.2  Pre-Necropsy Evaluation Checklist')
    dtbl(['Step','Action','Key Points'],
         [('1','Examine necropsy request letter','Specific lesions desired? Cosmetic vs routine? Special samples needed?'),
          ('2','Identify carcass','Species, sex, microchip, GPS collar, physical markings — ensure correct carcass'),
          ('3','Collect clinical history','Cause of death (as reported), clinical signs, treatment given, PMI'),
          ('4','Assess PM interval','Critical for autolysis grade and sample quality assessment'),
          ('5','Legal authorisation','DFO/CCF letter mandatory for Schedule I species')],
         wds=[1.5, 4, 11.5])
    kyb('LEGAL: PM examinations of Schedule I animals (including Asian elephant) must be performed systematically, sincerely and seriously — NOT a routine chore. Under WPA 1972, negligent necropsy is a criminal offence.')
    story.append(PageBreak())

    # S4
    h1('4.  Protocol for PM Examination & Equipment')
    pi(6, 'Slide 6 — PM Protocol general considerations flowchart; field necropsy photographs', 13)
    pi(7, 'Slide 7 — Equipment lists: documentation items (13) and surgical instruments (18)', 13)
    h2('4.1  General Considerations')
    pb('Perform in GOOD DAYLIGHT — artificial light misses subtle colour changes (icterus, cyanosis)')
    pb('Standard LARGE ANIMAL necropsy instruments — domestic instruments are inadequate')
    pb('Protective clothing: waterproof overalls, double gloves, goggles, face mask, gumboots — for ALL personnel')
    pb('Sample collection kit: 10% buffered formalin, 70% ethanol, sterile swabs, EDTA tubes, biohazard bags')
    pb('METAL DETECTOR: mandatory before any incision — check for bullets/metallic foreign bodies')
    h2('4.2  PM Protocol Steps')
    dtbl(['Step','Action'],
         [('1','Letter from competent authority (DFO/CCF)'),
          ('2','Assess facilities — field vs laboratory; natural light; water access'),
          ('3','Measurements: weight, length, girth, tusk, foot circumference'),
          ('4','External observations — before any incision'),
          ('5','Internal observations — cavity by cavity, system by system'),
          ('6','Gross interpretation — correlate all findings; differential diagnosis'),
          ('7','Sample collection — tissues for histopathology, culture, PCR, toxicology'),
          ('8a','Report writing — tentative cause of death + all gross findings'),
          ('8b','Final cause of death — after laboratory results')],
         wds=[1.5, 15.5])
    h2('4.3  Equipment — Documentation (13 Items)')
    dtbl(['S.No.','Item','No.'],
         [('1','Copy of Necropsy Protocol','1'), ('2','Hand-held GPS','1'),
          ('3','Digital camera','1'), ('4','Digital video camera','1'),
          ('5','Clip board','2'), ('6','Measuring tape','1'),
          ('7','Plastic ruler 15 cm (scale bar for photos)','2'), ('8','Vernier callipers','1'),
          ('9','Portable weighing machine 250 kg','1'), ('10','Necropsy format (forms)','5'),
          ('11','Ballpen','2'), ('12','Pencil rubber','1'), ('13','Metal detector','1')],
         wds=[1.5, 13, 2.5])
    h2('4.4  Equipment — Surgical Instruments SS Quality (18 Items)')
    dtbl(['S.No.','Instrument','No.'],
         [('1','Sharp high-quality necropsy knife SS','4'), ('2','Skinning knife curved SS','2'),
          ('3','Autopsy knife curved SS','2'), ('4','Slicing knife 22 mm blade SS','1'),
          ('5','Knife sharpener stone or steel','1'), ('6','Bard Parker Handle & blades No.20,22,26','5 each'),
          ('7','Small plain forceps','2'), ('8','Artery Forceps straight 203 mm SS','2'),
          ('9','Dissecting Forceps 200 mm long SS','2'), ('10','Large Mayo scissors 215 mm fine point','2'),
          ('11','Bone Cutter Compound action 266 mm','1'), ('12','Hack saw/bone saw blade 254 mm','1'),
          ('13','Chisels 8½" × 1¼" (22 cm, blade 3 cm)','1'), ('14','Hammer Wrench end 200 mm','1'),
          ('15','Portable autopsy saw (Electric/battery)','1'), ('16','Axe (Roofing axe SS) 60 mm blade','1'),
          ('17','Spirit lamp SS or gas burner','1'), ('18','Measuring tape SS','1')],
         wds=[1.5, 13, 2.5])
    story.append(PageBreak())

    # S5
    h1('5.  External Examination')
    pi(8, 'Slide 8 — External examination: history, body condition, rigor mortis, injuries; carcass photograph', 13)
    pi(9, 'Slide 9 — Skin examination, orifices, temporal glands, dung bolus, post-mortem changes', 13)
    h2('5.1  Initial Survey')
    pb('HISTORY: probable cause of death, clinical signs, treatment given, circumstances, PMI')
    pb('BODY CONDITION: prominent ribs, lumbar/buccal depression, distinct temporal fossa, loose skin = poor health')
    pb('RIGOR MORTIS: appears 1–4 hrs after death; lasts 16–24 hrs (up to 48 hrs); less marked in emaciated/septicaemic animals')
    pb('LIVOR MORTIS (Cadaveric Lividity): irregular subcutaneous patches on lying side — NORMAL, not haemorrhage')
    pb('DOCUMENTATION: photograph EVERY finding with scale bar BEFORE any manipulation')
    h2('5.2  Detailed 10-Point External Protocol')
    dtbl(['Point','Examination','Key Findings to Document'],
         [('i','Sex — male/female external organs; pregnant/lactating?','Gravid uterus; mammary engorgement; scrotal absence (normal in males)'),
          ('ii','Nutritional status','Prominent ribs; temporal/lumbar/buccal depression; loose skin → emaciation'),
          ('iii','Fractures & dislocations','Limbs, ribs, skull — HEC injury, train impact, fall'),
          ('iv','Post-mortem changes (algor/rigor/livor/autolysis)','Degree of PM changes → estimate PMI'),
          ('v','Skin: parasites, filariasis, pox, oedema, emphysema, burns, warts, mucous membranes','Crepitation (gas gangrene/Clostridium); cherry-red (CO/HCN); cyanosis'),
          ('vi','Injury: bullets, intra-species, carnivore mauling (calves), ankush (captive)','Entry vs exit wounds; mauling patterns; ankush punctures'),
          ('vii','Dung bolus of rectum','Coarse undigested material = dental exhaustion; dry = dehydrated; liquid = diarrhoea'),
          ('viii','Natural orifices — discharges; oral cavity (FMD, EEHV, anthrax)','EEHV haemorrhagic oral lesions in calves; FMD vesicles; anthrax black discharge'),
          ('ix','Temporal glands — musth status','Active secretion in musth; swelling/discharge outside musth = pathological'),
          ('x','Foot pads and nails — injuries, fissures, abscess','Captive: foot pad disease, osteomyelitis; wild: normal even wear')],
         wds=[1,4.5,11.5])
    story.append(PageBreak())

    # S6
    h1('6.  Dentition & Age Determination')
    pi(10, 'Slide 10 — Molar eruption table; lamellae count for age estimation; internal organ anatomy diagram', 13)
    h2('6.1  Horizontal Molar Progression — Unique to Elephants')
    bdy('Six successive molar sets (M1–M6) develop sequentially at the BACK of the jaw and move FORWARD. When M6 (the final molar) wears out, the animal can no longer chew → starvation → death. This sets the biological maximum lifespan at ~60–70 years.')
    h2('6.2  Molar Eruption Table')
    dtbl(['Molar','Eruption Age','Lamellae','Active Use Period','Notes'],
         [('M1','~4 months','5','0–1 yr','Deciduous; shed rapidly'),
          ('M2','~1–2 yrs','7','1–4 yrs','Milk tooth'),
          ('M3','~6 yrs','10','4–15 yrs','First large molar'),
          ('M4','~15 yrs','10 WIDER','15–28 yrs','Same count as M3 but WIDER lamellae'),
          ('M5','~28 yrs','12','28–47 yrs','Longest in use; prime adulthood'),
          ('M6','~47 yrs','13','47 yrs–death','Final molar; never replaced')],
         wds=[2,2.5,3,3.5,6])
    pb('Permanent tusks protrude beyond lips at ~30 months; grow throughout life')
    pb('Count enamel plates (lamellae) with probe AFTER cleaning — do not estimate visually')
    pb('Distinguish M3 (10 narrow plates) vs M4 (10 WIDE plates) — different age ranges')
    story.append(PageBreak())

    # S7
    h1('7.  Internal Anatomy & Skinning')
    pi(11, 'Slide 11 — Labelled internal anatomy diagram of elephant (cross-sectional)', 13)
    pi(12, 'Slide 12 — Field photographs: skinning of elephant carcass team procedure', 13)
    h2('7.1  Unique Anatomical Points Critical for Necropsy')
    pb('NO PLEURAL SPACE: lungs fused to chest wall — firm adhesion is NORMAL; no thoracocentesis possible')
    pb('BIFID HEART APEX: double-pointed cardiac apex — distinctive and normal; do not record as anomaly')
    pb('ABDOMINAL TESTES: males retain testes permanently in abdomen near kidneys — NORMAL (not cryptorchidism)')
    pb('CARDIAC WEIGHT: 12–21 kg; proboscideal artery prominent in thoracic cavity')
    pb('TEMPORAL GLAND: between eye and ear; musth secretion; examine bilaterally at necropsy')
    h2('7.2  Skinning Protocol')
    pb('Long median dorsal incision from mandible angle to tail base')
    pb('Reflect skin over entire lateral thoracic + lower abdominal + suspected regions')
    pb('Examine subcutaneous tissues: abscesses, haemorrhage, oedema, parasitic cysts')
    pb('Examine muscles: pallor (myopathy), haemorrhage (electrocution), atrophy')
    pb('Incise superficial lymph nodes: mandibular, parotid, prescapular, femoral')
    story.append(PageBreak())

    # S8
    h1('8.  Digestive System & Systematic Organ Examination')
    h2('8.1  Digestive System Anatomy')
    bdy('Elephant is MONOGASTRIC (simple-stomached) hindgut fermenter. Digestive efficiency ~40–45% of enormous daily intake (150–300 kg fresh forage). GI components: pharynx → oesophagus → stomach → small intestine → caecum (~90 L) → large intestine → rectum → anus.')
    dtbl(['Organ','Key Features','Necropsy Examination Points'],
         [('Stomach','100–140 cm long; 40 cm diameter','Contents (moisture, parasites); focal ulcers/gastritis; Gongylonema in mucosa'),
          ('Small Intestine','Primary digestion/absorption; very long','Intussusception; haemorrhage (salmonellosis); Quilonia/Pfenderius parasites'),
          ('Caecum','~90 L; primary hindgut fermentation','Bloat; impaction; parasitic nodules'),
          ('Liver','36–45 kg; multilobulated','Abscesses; fatty change; TB granulomas; Fasciola'),
          ('Lymph Nodes (mesenteric)','Immune barrier for gut pathogens','Salmonella; Johne disease; parasitic')],
         wds=[3,5,9])
    h2('8.2  Systematic Organ Examination Checklist')
    dtbl(['System','Organs','Key Examination Points'],
         [('Respiratory','Trachea, Lungs','Mucosa (haemorrhage, parasites); lung lobes (TB nodules, EEHV, consolidation)'),
          ('Urogenital','Kidneys, Bladder, Uterus/Testes','Kidneys renculated-multilobulated; testes abdominal in males (NORMAL); cystitis; endometritis'),
          ('Musculoskeletal','Muscles, Bones, Joints','Haemorrhage (electrocution); osteomyelitis (captive foot disease); fractures'),
          ('Reproductive','Uterus, Ovaries / Testes','Bifurcate uterus; gravidity; orchitis'),
          ('Nervous','Brain, Spinal Cord','Negri bodies (rabies); haemorrhage; oedema')],
         wds=[3,3.5,10.5])
    story.append(PageBreak())

    # S9
    h1('9.  Lymph Nodes & Histopathology')
    pi(13, 'Slide 13 — Systematic examination list; superficial lymph node locations in elephant', 13)
    pi(14, 'Slide 14 — Histopathology: EEHV intra-nuclear inclusion bodies (A & B); deep lymph nodes', 13)
    h2('9.1  Superficial Lymph Nodes')
    dtbl(['Lymph Node','Location','Key Diseases'],
         [('Mandibular','Ventral border of lower jaw, under skin','TB caseous granulomas; EEHV; strangles-like'),
          ('Parotid','Below ear, near parotid salivary gland','TB; systemic infection'),
          ('Superficial Cervical','Lateral neck, cranial to shoulder','TB; trypanosomiasis'),
          ('Prescapular','Just ahead of shoulder joint','Systemic disease; TB; lymphoma'),
          ('Femoral','Near head of femur (inguinal region)','TB; pelvic infections; lymphosarcoma')],
         wds=[3.5,5.5,8])
    h2('9.2  Deep / Internal Lymph Nodes')
    dtbl(['Lymph Node','Location','Diagnostic Use'],
         [('Bronchial (Tracheobronchial)','At carina — junction of bronchi/trachea','MANDATORY: mycobacterial culture (TB); EEHV PCR'),
          ('Hepatic & Splenic','Near liver and spleen','Systemic infection; TB hepatic involvement'),
          ('Mesenteric','Mesentery of small/large intestine','Intestinal infections; enteritis; parasites')],
         wds=[3.5,5.5,8])
    h2('9.3  EEHV — Histopathological Diagnosis')
    bdy('Elephant Endotheliotropic Herpesvirus (EEHV) is the leading infectious cause of death in captive elephant calves worldwide. Definitive diagnosis: INTRA-NUCLEAR INCLUSION BODIES (Cowdry Type A) in vascular endothelial cells of heart, tongue, trunk skin, liver, spleen.')
    pb('Gross: petechial/ecchymotic haemorrhages on serosal surfaces; haemopericardium; oedematous head/neck')
    pb('Histopathology: swollen endothelial cells with large eosinophilic intranuclear inclusions surrounded by clear halo')
    pb('PCR confirmation: trunk wash, blood, tissue samples — must be FRESH (unfixed)')
    pb('7 EEHV species (EEHV1–7); EEHV1A and EEHV4 most commonly fatal; median survival ~36 hrs')
    pb('Vaccine: T cell-inducing heterologous vaccines currently under trial')
    kyb('EEHV SAMPLING: trunk wash (fresh) + blood (EDTA) + heart/tongue/trunk skin (fresh frozen + formalin) + lymph nodes (fresh) → send to IVRI/national EEHV reference laboratory. Time critical — act within 36 hrs of signs.', danger=True)
    story.append(PageBreak())

    # S10
    h1('10.  Differential Diagnosis & Case Studies')
    pi(15, 'Slide 15 — Differential diagnosis: sudden death diseases; Rabies case at Panna Tiger Reserve', 13)
    pi(16, 'Slide 16 — TB lesions in free-range Asian elephant (Photo: Dr. Parag Nigam); decomposed PM', 13)
    h2('10.1  Differential Diagnosis — Sudden Onset Rapid Death')
    dtbl(['Disease','Agent','Key PM Finding','Priority Sample'],
         [('Haemorrhagic Septicaemia','Pasteurella multocida B/E','Extensive haemorrhages; pulmonary oedema; splenomegaly','Blood anaerobic; lung; spleen for culture + PCR'),
          ('Salmonellosis','Salmonella spp.','Haemorrhagic enteritis; watery diarrhoea ± blood; mesenteric LN haemorrhage','Intestinal content; LN; blood culture; faeces PCR'),
          ('Enterotoxaemia','Clostridium perfringens C/D','Haemorrhagic enteritis; gas in gut; rapid autolysis','Intestinal content frozen for toxin ELISA; PCR'),
          ('Encephalomyocarditis','EMC Virus','Pale foci in myocardium; encephalitis; respiratory signs','Heart + brain fresh + formalin; blood serology + PCR'),
          ('Rabies','Rabies Lyssavirus','Negri bodies in brain stem; non-suppurative encephalitis','Brain stem fresh (FA test); brain formalin (histology)')],
         wds=[3,3.5,5.5,5])
    h2('10.2  Rabies Case — Panna Tiger Reserve (Dr. A B Shrivastava)')
    dtbl(['Day','Clinical Signs'],
         [('Day 1','Off feed; restlessness; drooling of saliva (hypersalivation)'),
          ('Day 3','Restricted jaw movement; protrusion of tongue (paresis)'),
          ('Day 4','Hyperaemic conjunctiva (autonomic involvement)'),
          ('Day 5','Hydrophobia; loud but changed, distorted trumpeting (laryngeal paralysis)'),
          ('Day 6','Lateral recumbency and death (ascending paralysis complete)'),
          ('Post-mortem','Proper disposal — deep burial or incineration; biohazardous; PEP for all contacts')],
         wds=[2.5,14.5])
    h2('10.3  TB Lesions in Free-Range Asian Elephant')
    pb('Causative agent: Mycobacterium tuberculosis (HUMAN strain) — fully zoonotic')
    pb('Gross: grey-white caseous nodular granulomas in lungs; miliary nodules on pleura/peritoneum; caseous/calcified lymph nodes')
    pb('Collect: tracheobronchial LN (priority); lung nodules; trunk wash → culture (8–12 weeks) + PCR')
    pb('ALL personnel: N95 mask + double gloves + goggles; mandatory post-exposure TB screening')
    h2('10.4  HCN Poisoning — Captive Elephants (Zoo Print 2010)')
    pb('Cause: Sorghum (Jowar) fed to animals unaccustomed to it — cyanogenic glycosides released')
    pb('Signs: restlessness, diarrhoea, subnormal temperature 97–98°F')
    pb('Treatment: Sodium thiosulphate 50 gm oral; dextrose saline + Diulin rectally')
    pb('PM: cherry-red blood/tissues; bitter almonds smell; congested viscera')
    story.append(PageBreak())

    # S11: REFERENCES
    h1('11.  Key References & Recommended Reading')
    pi(17, 'Slide 17 — Published works of Prof. Dr. A B Shrivastava (Vol. 1)', 13)
    pi(18, 'Slide 18 — Published works: Learning from Dead; Caring for Elephants; Necropsy SOP', 13)
    h2('11.1  Works by Prof. Dr. A B Shrivastava')
    pb('Shrivastav AB & Sharma RK (2008). A Manual of Wildlife Health Management in Protected Areas. CVAH, JNKVV, Jabalpur')
    pb('Shrivastav AB & Singh KP (Ed.) (2011). Big Cats. InTech Open Access')
    pb('Shrivastav AB & Nigam P (2019). Learning from Dead: Necropsy Essentials for Large Felids')
    pb('Shrivastav AB (2020). Manual on Postmortem Examination of Felids. NDVSU, Jabalpur')
    pb('MoEFCC/WII (2020). Necropsy and Carcass Disposal of Asian Elephant: Recommended Operating Procedure')
    pb('Nigam P, Habib J & Pandey H (Ed.) (2021). Caring for Elephants: Managing Health & Welfare in Captivity')
    pb('Shrivastav AB (2010). HCN Poisoning in Asian Elephants. Zoo Print vol. xxv, 6 June 2010')
    h2('11.2  Peer-Reviewed Literature')
    pb('Fowler ME & Mikota SK (2006). Biology, Medicine and Surgery of Elephants. Blackwell, Iowa')
    pb('Mikota SK et al. (2001). Tuberculosis in elephants. International Zoo Yearbook 37: 122–135')
    pb('Richman LK et al. (2000). Novel Endotheliotropic Herpesviruses Fatal to Asian & African Elephants. Science 288: 1171')
    pb('West JB (2001). Anatomical Basis for Unusual Lung Properties in an Extreme Environment. Respir Physiol 127: 1–11')
    pb('Sukumar R (2003). The Living Elephants. Oxford University Press')
    pb('MoEFCC (2017). Gajah: Securing the Future for Elephants in India. Project Elephant, GoI')

    hr()
    story.append(Paragraph(
        'Prof. Dr. A B Shrivastava, NDVSU Jabalpur  |  Presentation: 06-06-2026  |  '
        'Training Program: Mortality Investigation of Asian Elephant, Raigarh, Chhattisgarh  |  '
        'Notes elaborated with peer-reviewed literature', sFT))

    doc.build(story)
    print(f'  ✓  {OUT_P}  ({os.path.getsize(OUT_P)//1024} KB)')


if __name__ == '__main__':
    print('Building ABS Elephant Necropsy Notes...\n')
    print('  → Word document...')
    build_docx()
    print('  → PDF document...')
    build_pdf()
    print('\nDone.')

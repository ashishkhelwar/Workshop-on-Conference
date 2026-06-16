#!/usr/bin/env python3
"""
Generate Workshop_Proceedings_2026.docx — complete book in a single Word document.
All chapters built directly into one master doc to avoid style conflicts.
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DIR  = '/home/user/Workshop-on-Conference'
OUT  = os.path.join(DIR, 'Workshop_Proceedings_2026.docx')

# ── Palette ───────────────────────────────────────────────────────────────────
DARK   = RGBColor(0x1B, 0x43, 0x32)
MED    = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT  = RGBColor(0x52, 0xB7, 0x88)
TINT   = RGBColor(0xD8, 0xF3, 0xDC)
TINT2  = RGBColor(0xEA, 0xF7, 0xEE)
RED    = RGBColor(0xC0, 0x39, 0x2B)
REDL   = RGBColor(0xFA, 0xDB, 0xD8)
ORANGE = RGBColor(0xF4, 0xA2, 0x61)
GOLD   = RGBColor(0xC9, 0xA8, 0x4C)
NAVY   = RGBColor(0x1A, 0x2E, 0x4A)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
MUTED  = RGBColor(0x55, 0x55, 0x55)


def rgb_hex(rgb):
    return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'


# ═══════════════════════════════════════════════════════════════════════════════
# Primitive helpers (all take `doc` as first arg)
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


def para(doc, text, size=9.5, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color or BLACK
    return p


def bullet(doc, text, size=9, level=0):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.4)
    p.paragraph_format.first_line_indent = Cm(-0.3)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(f'•  {text}')
    run.font.name = 'Calibri'
    run.font.size = Pt(size)
    run.font.color.rgb = BLACK


def chapter_header(doc, num, title, subtitle='', author=''):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(8)

    r0 = p.add_run(f'CHAPTER {num}' if num else 'WORKSHOP OVERVIEW')
    r0.font.name = 'Calibri'; r0.font.size = Pt(8); r0.font.bold = True
    r0.font.color.rgb = LIGHT
    p.add_run('\n')
    r1 = p.add_run(title)
    r1.font.name = 'Calibri'; r1.font.size = Pt(16); r1.font.bold = True
    r1.font.color.rgb = WHITE
    if subtitle:
        p.add_run('\n')
        r2 = p.add_run(subtitle)
        r2.font.name = 'Calibri'; r2.font.size = Pt(9.5); r2.font.italic = True
        r2.font.color.rgb = TINT
    if author:
        p.add_run('\n\n')
        r3 = p.add_run(author)
        r3.font.name = 'Calibri'; r3.font.size = Pt(8.5); r3.font.color.rgb = TINT
    doc.add_paragraph()


def h1(doc, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(MED))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(11); run.font.bold = True
    run.font.color.rgb = WHITE
    doc.add_paragraph()


def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(10); run.font.bold = True
    run.font.color.rgb = MED


def keybox(doc, text, danger=False, gold=False):
    bg  = rgb_hex(REDL) if danger else ('FFF8E1' if gold else rgb_hex(TINT))
    fg  = RED if danger else (GOLD if gold else DARK)
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
    doc.add_paragraph()


def table(doc, headers, rows, col_widths=None):
    n = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n)
    tbl.style = 'Table Grid'
    # Header
    for i, h in enumerate(headers):
        shade_cell(tbl.rows[0].cells[i], rgb_hex(MED))
        p = tbl.rows[0].cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
        run = p.add_run(str(h))
        run.font.name = 'Calibri'; run.font.size = Pt(8.5); run.font.bold = True
        run.font.color.rgb = WHITE
    # Rows
    for ri, row in enumerate(rows):
        bg = rgb_hex(TINT2) if ri % 2 == 1 else 'FFFFFF'
        for ci, val in enumerate(row):
            shade_cell(tbl.rows[ri+1].cells[ci], bg)
            p = tbl.rows[ri+1].cells[ci].paragraphs[0]
            p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
            if isinstance(val, tuple):
                txt, bld = val
                run = p.add_run(str(txt)); run.font.bold = bld
            else:
                run = p.add_run(str(val))
            run.font.name = 'Calibri'; run.font.size = Pt(8.5); run.font.color.rgb = BLACK
    # Widths
    if col_widths:
        for row in tbl.rows:
            for ci2, cell in enumerate(row.cells):
                if ci2 < len(col_widths):
                    cell.width = Cm(col_widths[ci2])
    doc.add_paragraph()


# ═══════════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def add_title_page(doc):
    # Main banner
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(14)
    r0 = p.add_run('WORKSHOP PROCEEDINGS\n')
    r0.font.name = 'Calibri'; r0.font.size = Pt(9); r0.font.bold = True; r0.font.color.rgb = LIGHT
    r1 = p.add_run('Workshop on Essentials for Mortality Investigation of Asian Elephant\n')
    r1.font.name = 'Calibri'; r1.font.size = Pt(20); r1.font.bold = True; r1.font.color.rgb = WHITE
    r2 = p.add_run('5–6 June 2026  ·  Raigarh, Chhattisgarh')
    r2.font.name = 'Calibri'; r2.font.size = Pt(10.5); r2.font.italic = True; r2.font.color.rgb = TINT
    doc.add_paragraph()

    # Event details
    dtbl = doc.add_table(rows=1, cols=4)
    dtbl.style = 'Table Grid'
    for i, (lbl, val) in enumerate([
        ('Organised by', 'CG Forest Dept'),
        ('Technical Support', 'WII Dehradun'),
        ('Lab Partners', 'ICAR-IVRI & NDVSU'),
        ('Participants', '84 Officers'),
    ]):
        shade_cell(dtbl.rows[0].cells[i], rgb_hex(TINT))
        pp = dtbl.rows[0].cells[i].paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.paragraph_format.space_before = Pt(5); pp.paragraph_format.space_after = Pt(5)
        rv = pp.add_run(val + '\n'); rv.font.name = 'Calibri'; rv.font.size = Pt(11)
        rv.font.bold = True; rv.font.color.rgb = DARK
        rl = pp.add_run(lbl); rl.font.name = 'Calibri'; rl.font.size = Pt(7.5); rl.font.color.rgb = MUTED
    doc.add_paragraph()

    # Table of Contents
    para(doc, 'TABLE OF CONTENTS', size=11, bold=True, color=DARK,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)

    toc_entries = [
        ('Overview',   'Workshop Overview & Inaugural Proceedings',
         'CG Forest Department + Senior Officers'),
        ('Chapter 1',  'Elephant Mortality Analysis in Chhattisgarh (2021–2026)',
         'Dr. Parag Nigam (WII Dehradun)'),
        ('Chapter 2',  'Biological & Anatomical Aspects of the Asian Elephant',
         'Dr. Parag Nigam (WII Dehradun)'),
        ('Chapter 3',  'Infectious Diseases of Asian Elephants',
         'Dr. M. Karikalan (ICAR-IVRI)'),
        ('Chapter 4',  'Biological Sample Collection for Wildlife Disease Diagnosis',
         'Dr. M. Karikalan (ICAR-IVRI)'),
        ('Chapter 5',  'Non-Infectious Diseases in Asian Elephants',
         'Dr. Karikalan Mathesh (ICAR-IVRI)'),
        ('Chapter 6',  'Non-Infectious Pathology in Asian Elephants',
         'Prof. Dr. A. B. Shrivastava (NDVSU)'),
        ('Chapter 7',  'Postmortem Examination of the Asian Elephant',
         'Prof. Dr. A. B. Shrivastav (NDVSU)'),
    ]
    table(doc,
        ['Section', 'Title', 'Author / Resource Person'],
        [[(tag, True), title, author] for tag, title, author in toc_entries],
        col_widths=[3, 10, 4])

    # Founding quote
    keybox(doc,
        '"The carcass never tells a lie — but you must know how to ask the right questions."\n'
        '— Dr. R. K. Satpati, Wildlife Institute of India\n\n'
        '"Doctors who perform necropsies gain wisdom that no textbook can teach."\n'
        '— Prof. Dr. A. B. Shrivastav, NDVSU Jabalpur', gold=True)

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════

def add_overview(doc):
    chapter_header(doc, '', 'Workshop Overview & Inaugural Proceedings',
        'Raigarh, Chhattisgarh  |  5–6 June 2026',
        'Organised by: Chhattisgarh Forest Department  |  Technical Support: WII Dehradun')

    h1(doc, '1. Workshop at a Glance')
    table(doc, ['Parameter', 'Details'],
        [['Title', 'Workshop on Essentials for Mortality Investigation of Asian Elephant'],
         ['Dates', '5–6 June 2026 (Two days)'],
         ['Venue', 'Raigarh, Chhattisgarh'],
         ['Organised by', 'Chhattisgarh Forest Department'],
         ['Technical Support', 'Wildlife Institute of India (WII), Dehradun'],
         ['Laboratory Partners', 'ICAR-IVRI, Bareilly  ·  NDVSU, Jabalpur'],
         ['Total Participants', '84 Forest Officers and Wildlife Veterinarians'],
         ['Target Audience', 'DFOs, RFOs, Wildlife Veterinarians, Field Staff from elephant-affected divisions'],
         ['Context', 'CG elephant population ~451 (2026); 49 deaths in 2021–2026 — capacity building critical']],
        col_widths=[4.5, 12.5])

    h1(doc, '2. Background & Rationale')
    para(doc,
        'Chhattisgarh has emerged as a significant elephant range state, with the population '
        'growing from 24 individuals (2001) to an estimated 451 elephants (2026). Between 2021 '
        'and 2026, 49 elephant deaths were recorded across Dharamjaigarh (DH) and Raigarh (RG) '
        'Forest Divisions. 2025-26 saw 12 deaths — the highest in a single year. Electrocution '
        '(47%) and drowning (27%) are the dominant causes — both largely preventable. This workshop '
        'addresses the critical gap in systematic necropsy and mortality investigation capacity.')
    keybox(doc,
        '49 elephant deaths in 5 years — 74% preventable. '
        'Building field capacity for systematic investigation is the first step toward evidence-based prevention.')

    h1(doc, '3. Workshop Objectives')
    table(doc, ['Theme', 'Learning Objectives'],
        [['Biology & Ecology', 'Understand biology, anatomy, behaviour, ecology; population dynamics in CG'],
         ['Necropsy & Pathology', 'Systematic postmortem examination; gross pathological findings; cause of death determination'],
         ['Biosafety', 'PPE protocols; zoonotic risks at necropsy; biohazardous material management'],
         ['Sample Collection', 'Correct collection, preservation, transport; chain of custody for forensic samples'],
         ['Disease Diagnosis', 'Key infectious (EEHV, TB, anthrax) and non-infectious (electrocution, drowning, CPA) causes'],
         ['Surveillance & Response', 'Elephant surveillance systems; carcass disposal; site remediation; PM report writing']],
        col_widths=[4, 13])

    h1(doc, '4. Resource Persons')
    table(doc, ['Name', 'Designation & Institution', 'Topics Covered'],
        [['Prof. Dr. A. B. Shrivastav', 'Professor & Head, Wildlife Health Mgmt, NDVSU Jabalpur',
          'PM Examination; Non-Infectious Pathology; Toxicology; HCN Poisoning Cases'],
         ['Dr. Parag Nigam', 'Senior Scientist, WII Dehradun',
          'Elephant Ecology & Population Biology; CG Mortality Statistics'],
         ['Dr. Karikalan Mathesh', 'Principal Scientist, ICAR-IVRI Bareilly',
          'Sample Collection Protocols; Non-Infectious Diseases; Bandhavgarh CPA Case Study'],
         ['Dr. Tapendra Saini', 'Scientist, Wildlife Health Programme, WII Dehradun',
          'Infectious Diseases; EEHV Surveillance; Disease Monitoring Systems'],
         ['Dr. Chandra Prakash Sharma', 'Scientist, Conservation Biology, WII Dehradun',
          'Field Investigation; Carcass Disposal & Site Remediation']],
        col_widths=[4, 5.5, 7.5])

    h1(doc, '5. Two-Day Programme Schedule')
    table(doc, ['Day', 'Time', 'Session / Topic', 'Resource Person'],
        [['Day 1\n5 June', '09:00–10:00', 'Inauguration; Welcome address; Overview of CG elephant situation',
          'CCF, CG Forest Dept'],
         ['', '10:00–11:30', 'CG Elephant Population & Mortality Statistics (2021–2026)',
          'Dr. Parag Nigam (WII)'],
         ['', '11:30–13:00', 'Biological & Anatomical Aspects of Asian Elephants',
          'Dr. Parag Nigam (WII)'],
         ['', '14:00–15:30', 'Non-Infectious Diseases: Electrocution, Drowning, Toxicoses, Bandhavgarh Case',
          'Dr. Karikalan Mathesh (ICAR-IVRI)'],
         ['', '15:30–17:00', 'Infectious Diseases & Surveillance: EEHV, TB, Anthrax, Rabies',
          'Dr. Tapendra Saini (WII)'],
         ['', '17:00–18:00', 'Practical Demonstration: PM Examination Techniques',
          'Dr. A. B. Shrivastav (NDVSU)'],
         ['Day 2\n6 June', '09:00–10:30', 'Biological Sample Collection: master protocol, preservation, chain of custody',
          'Dr. Karikalan Mathesh (ICAR-IVRI)'],
         ['', '10:30–12:00', 'Non-Infectious Pathology: Poisoning, Pyometra, Hyperthermia, Anaemia',
          'Dr. A. B. Shrivastav (NDVSU)'],
         ['', '12:00–13:00', 'Postmortem Examination — Step-by-step workflow; Instruments; Documentation',
          'Dr. A. B. Shrivastav (NDVSU)'],
         ['', '14:00–15:30', 'Field Investigation Case Studies: Gurda Drowning; CPA Bandhavgarh; Panna Rabies',
          'All resource persons'],
         ['', '15:30–16:30', 'Carcass Disposal & Site Remediation; Environmental Sampling Protocol',
          'Dr. C. P. Sharma (WII)'],
         ['', '16:30–17:30', 'Recommendations, Action Plan & Valediction',
          'CCF, CG + All Resource Persons']],
        col_widths=[2.5, 2.5, 9.5, 4.5])

    h1(doc, '6. Partner Institutions')
    table(doc, ['Institution', 'Role', 'Key Contribution'],
        [['Chhattisgarh Forest Department', 'Organiser & Host',
          'Funding, logistics, participant mobilisation, field mortality records (2021–2026)'],
         ['Wildlife Institute of India (WII), Dehradun', 'Technical Support',
          'Population ecology, surveillance system design, 3 resource persons'],
         ['ICAR-IVRI, Bareilly', 'Laboratory Partner — Pathology & Diagnosis',
          'Diagnostic services: EEHV PCR, histopathology, toxicology, bacteriology, virology'],
         ['NDVSU, Jabalpur', 'Laboratory Partner — Wildlife Pathology',
          'Wildlife PM protocols, non-infectious pathology, toxicology case expertise']],
        col_widths=[4, 3.5, 9.5])

    h1(doc, '7. Inaugural Address — Forest Minister Shri Kedar Kashyap')
    para(doc,
        'The workshop was formally inaugurated by Hon\'ble Forest Minister Shri Kedar Kashyap, '
        'whose special initiative drove the organisation of this national-level event in response '
        'to the recent incidents of elephant calf deaths in Raigarh and Dharamjaigarh Forest Divisions.')
    para(doc,
        'The elephant population in Chhattisgarh has been growing continuously over the past '
        'five years, with approximately 450 elephants now present across Surguja, Bilaspur, '
        'Raipur, and Durg divisions. The Department of Forest and Climate Change is continuously '
        'working for the conservation, enhancement, and protection of these elephants while '
        'ensuring the safety of local communities, and is striving to bring human-elephant '
        'conflict to zero — with positive outcomes already achieved.')
    para(doc,
        'The workshop aims to scientifically investigate the causes of wild elephant deaths, '
        'provide practical training in mortality examination, sample collection and safe dispatch '
        'to laboratories, and strengthen carcass disposal protocols and health surveillance '
        'preparedness across all elephant-affected districts of the state.')

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — Mortality Analysis
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter1(doc):
    chapter_header(doc, '1', 'Elephant Mortality Analysis in Chhattisgarh (2021–2026)',
        'Trends, Causes, Demographics & Priority Recommendations',
        'Chhattisgarh Forest Department  |  Technical Support: WII Dehradun')

    h1(doc, '1. Elephant Population Status in Chhattisgarh')
    para(doc,
        'Chhattisgarh\'s elephant population has grown from 24 individuals (2001) to an '
        'estimated 451 in 2026 — a CAGR of ~13%. Resident breeding populations are established '
        'across Dharamjaigarh (DH) and Raigarh (RG) Forest Divisions.')
    table(doc, ['Year', 'Population', 'Remarks'],
        [['2001', '24', 'First transient elephants from Odisha'],
         ['2005', '123', 'Rapid establishment of resident herds'],
         ['2007', '122', 'Stable — consolidation phase'],
         ['2015', '247', 'Range expansion into new areas'],
         ['2017', '247', 'Stable; human-elephant conflict rising'],
         ['2021', '279', 'Post-COVID survey; mortality increasing'],
         [('2026', True), ('~451 (est.)', True), ('Highest ever; CAGR ≈ 13%', True)]],
        col_widths=[2.5, 3.5, 11])

    h1(doc, '2. Elephant Casualty Analysis (2021–2026)')
    keybox(doc,
        'TOTAL: 49 Elephant Deaths | DH Division: 27 | RG Division: 22 | '
        '2025-26: 12 deaths (RECORD HIGH) — Immediate intervention required', danger=True)
    table(doc, ['Year', 'DH', 'RG', 'Total', 'Remarks'],
        [['2021-22', '2', '2', '4', 'Baseline — low mortality'],
         ['2022-23', '7', '5', '12', 'Surge — monsoon related'],
         ['2023-24', '3', '3', '6', 'Relatively low year'],
         ['2024-25', '6', '4', '10', 'Rising trend resumes'],
         ['2025-26', '7', '5', ('12 — RECORD', True), 'Record — electrocution predominant'],
         ['2026-27*', '2', '3', '5*', 'Ongoing (as of June 2026)'],
         [('TOTAL', True), ('27', True), ('22', True), ('49', True), 'Cumulative 2021–2026']],
        col_widths=[2.5, 1.8, 1.8, 2.2, 8.7])
    para(doc, 'Human deaths in Human-Elephant Conflict: 45 total (DH: 36 | RG: 9)', bold=True)

    h1(doc, '3. Cause of Death Analysis')
    table(doc, ['Cause', 'Count', '%', 'Key Mechanism'],
        [['Electrocution', '23', '47%', 'Stray power lines, illegal electric fencing around crops'],
         ['Drowning', '13', '27%', 'Calves unable to exit water bodies; steep banks, dams'],
         ['Natural / Old Age', '4', '8%', 'Molar exhaustion, senility'],
         ['Fall / Trauma', '4', '8%', 'Steep terrain, mine shafts, road/rail conflict'],
         ['Other / Undetermined', '5', '10%', 'Toxicology pending, disease, inter-elephant conflict']],
        col_widths=[4, 2, 2, 9])
    keybox(doc, 'Electrocution + Drowning = 74% of all deaths — both are PREVENTABLE', danger=True)

    h1(doc, '4. Demographic Analysis')
    table(doc, ['Age Category', 'Count', '%', 'Key Vulnerability'],
        [['Calf (0–2 yr)', '23', '50%', 'Drowning (cannot exit steep banks), electrocution'],
         ['Juvenile (2–5 yr)', '5', '11%', 'Separation from herd; crop field foraging'],
         ['Sub-adult (5–15 yr)', '2', '4%', 'Dispersing males — power line exposure'],
         ['Adult (15–40 yr)', '11', '24%', 'Electrocution in bulls; cow mortality'],
         ['Old (>40 yr)', '5', '11%', 'Molar exhaustion, starvation, senility']],
        col_widths=[3.5, 2, 2, 9.5])
    table(doc, ['Sex', 'Count', '%', 'Notable Pattern'],
        [['Male', '23', '51%', '48% of male deaths caused by electrocution'],
         ['Female', '22', '49%', '33% of female deaths caused by electrocution']],
        col_widths=[3, 2, 2, 10])
    keybox(doc, 'CRITICAL: Calves (0-2 yr) = 50% of all deaths and 92% of drowning deaths.')

    h1(doc, '5. Seasonal Variation')
    table(doc, ['Season', 'Months', 'Drowning', 'Electrocution', 'Key Driver'],
        [['Dry Season', 'Jan–May', '8', '6', 'Low water — calves trapped in drying pools'],
         ['Monsoon', 'Jun–Sep', '1', '5', 'Flooded rivers; reduced power line visibility'],
         [('Harvest (PEAK)', True), 'Oct–Dec', ('4', True), ('10', True),
          ('PEAK: Illegal electric fencing to protect paddy/maize crops', True)],
         [('TOTAL', True), '—', ('13', True), ('21*', True), '*excludes 2 unconfirmed']],
        col_widths=[3.5, 2.5, 2.5, 3, 5.5])
    para(doc, 'October is the single deadliest month (8 deaths). Oct–Dec = 42% of annual deaths.', italic=True)

    h1(doc, '6. Range-wise Distribution')
    table(doc, ['Forest Range', 'Division', 'Elec.', 'Drown.', 'Other', 'Total', 'Status'],
        [[('Ghargoda', True), 'RG', '8', '5', '2', ('15', True), ('CRITICAL', True)],
         [('Chhal', True), 'DH', '7', '5', '2', ('14', True), ('CRITICAL', True)],
         ['Dharamjaigarh', 'DH', '3', '2', '1', '6', 'HIGH'],
         ['Kharsia', 'RG', '2', '1', '1', '4', 'MODERATE'],
         ['Tamnar', 'RG', '2', '1', '1', '4', 'MODERATE'],
         ['Other Ranges', '—', '1', '—', '5', '6', 'Monitor'],
         [('TOTAL', True), '—', ('23', True), ('13', True), ('13', True), ('49', True), '—']],
        col_widths=[3.5, 2, 2, 2.5, 2, 2, 3])

    h1(doc, '7. Drowning — Post-Mortem Analysis')
    keybox(doc,
        'KEY: 13 drowning deaths. 92% were calves. '
        'ARSENIC DETECTED in 2 specimens — Tamnar Range, Dec 2025', danger=True)
    table(doc, ['PM Finding', 'Result', 'Significance'],
        [['Frothy discharge', 'ALL 13 cases', 'Hallmark of antemortem drowning'],
         ['Waterlogged lungs', 'ALL 13 cases', 'Lung weight 3–5× normal'],
         ['Water in trachea', 'ALL 13 cases', 'Rules out post-mortem artefact'],
         ['GI water content', 'ALL 13 cases', 'Swallowed water while alive'],
         [('Diatom test', True), ('POSITIVE — all tested', True), 'Confirmed antemortem drowning'],
         [('Arsenic', True), ('DETECTED — 2 specimens', True), 'Tamnar Range Dec 2025 — investigation initiated'],
         ['EEHV / Nitrate / HMs', 'NEGATIVE all cases', 'Infection and contamination excluded'],
         ['HCN / Organochlorine', 'NEGATIVE all cases', 'Toxicological causes excluded']],
        col_widths=[4.5, 4, 8.5])

    h1(doc, '8. Case Study — Gurda Calf Drowning (01 June 2026)')
    table(doc, ['Parameter', 'Details'],
        [['Date', '01 June 2026'],
         ['Location', 'Gurda River sandbank, Kharsia Range, Raigarh Van Mandal'],
         ['GPS', '22.0439°N, 83.1313°E'],
         ['Victim', 'Male calf, estimated age 12–18 months'],
         ['PM Findings', 'Waterlogged lungs, frothy tracheal discharge, water in stomach; no external trauma'],
         ['Diatom Test', 'POSITIVE — Naviculaceae spp. in lung and bone marrow'],
         [('Cause of Death', True), ('Confirmed drowning — asphyxia due to water inhalation', True)],
         ['Follow-up', 'Water sample collected for arsenic; site flagged for earthen ramp installation']],
        col_widths=[4.5, 12.5])

    h1(doc, '9. Key Recommendations & Priority Action Plan')
    table(doc, ['#', 'Priority Action', 'Timeline', 'Agency'],
        [['1', 'Environmental water sampling: Rabo & Panikshet dams + Tamnar Range for arsenic/heavy metals', 'Immediate', 'CG Forest Dept + ICAR-IVRI'],
         ['2', 'Drowning prevention infrastructure: earthen ramps at hotspots (Ghargoda & Chhal priority)', '1–3 months', 'CG Forest Dept + PWD'],
         ['3', 'Power-line audit: complete audit of illegal electric fencing and stray HV lines in all corridors', '1–6 months', 'CG Forest Dept + CSPDCL'],
         ['4', 'Oct–Dec enforcement: anti-fencing squads with weekly intelligence during harvest season', 'Seasonal', 'Forest Dept + Police'],
         ['5', 'Jan–May calf monitoring: intensive surveillance in dry season — highest drowning risk', 'Seasonal', 'WII + CG Forest Dept'],
         ['6', 'Mandatory PM within 24 hrs: SOP with digital reporting to State WL Office', 'Immediate policy', 'PCCF (WL), CG'],
         ['7', 'Annual EEHV surveillance: PCR + serology across all herds in DH & RG Divisions', 'Annual', 'ICAR-IVRI + WII'],
         ['8', 'Quarterly review meetings: inter-departmental review — Forest, Police, Revenue, Power Depts', 'Quarterly', 'PCCF (WL) + All Depts']],
        col_widths=[0.8, 9.5, 2.5, 4.2])

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Anatomy
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter2(doc):
    chapter_header(doc, '2', 'Biological & Anatomical Aspects of the Asian Elephant',
        'Taxonomy, Morphology, Physiology & Specialised Systems',
        'Compiled from WII Training Materials  |  Workshop 2026')

    h1(doc, '1. Taxonomy & Classification')
    table(doc, ['Taxonomic Rank', 'Classification'],
        [['Kingdom', 'Animalia'], ['Phylum', 'Chordata'], ['Class', 'Mammalia'],
         ['Order', 'Proboscidea'], ['Family', 'Elephantidae'], ['Genus', 'Elephas'],
         ['Species', 'Elephas maximus'],
         ['Sub-species (India)', 'Elephas maximus indicus (Indian Elephant)']],
        col_widths=[5, 12])

    h1(doc, '2. Physical Characteristics — Asian vs African Elephant')
    table(doc, ['Parameter', 'Asian Elephant', 'African Elephant'],
        [['Body Length', '5.5–6.5 m', '6–7.5 m'],
         ['Shoulder Height', '2.5–3.0 m (male)', '3.2–4.0 m (male)'],
         ['Body Weight', '3,500–5,000 kg (male)', '4,000–7,000 kg (male)'],
         ['Head Profile', 'Double dome (two bumps on crown)', 'Single dome (one smooth dome)'],
         ['Ear Shape', 'Smaller, rounded — resembles map of India', 'Larger — map of Africa'],
         ['Trunk Tip', 'One finger (single prehensile lobe)', 'Two lips / two fingers'],
         ['Tusk Prevalence', 'Males mainly; some females (tushes)', 'Both sexes commonly'],
         ['Toe Nails', '5 front / 4 hind', '4 front / 3 hind'],
         ['Skin', 'Grey — pink depigmented patches on ears/trunk', 'Grey — less depigmentation']],
        col_widths=[4, 6, 7])

    h1(doc, '3. The Trunk — Proboscis')
    para(doc,
        'The trunk is a fusion of the upper lip and nose — over 150,000 muscle units, no bone. '
        'It is the elephant\'s most versatile organ, performing sensory, feeding, drinking, '
        'communication, and defensive functions simultaneously.')
    table(doc, ['Function', 'Details'],
        [['Olfaction', 'Primary sensory organ — smell range up to 19–20 km'],
         ['Drinking', 'Holds 8–10 L per inhalation; total 150–200 L/day'],
         ['Feeding', 'Plucks, strips, breaks vegetation — up to 150 kg fodder/day'],
         ['Bathing & dusting', 'Sprays water/dust for thermoregulation and ectoparasite control'],
         ['Communication', 'Trumpeting, rumbling; trunk-in-mouth = greeting/submission'],
         ['Seismic detection', 'Detects infrasound vibrations through trunk pressed to ground'],
         ['Tool use', 'Throws objects; plugs waterholes; rubs against trees'],
         ['Defence', 'Strikes, grapples, throws at perceived threats']],
        col_widths=[4.5, 12.5])

    h1(doc, '4. Molar Teeth & Age Estimation')
    para(doc,
        'Elephants cycle through 6 molar sets (M1–M6) in horizontal progression — '
        'unique among land mammals. Only one or two molars are functional at a time per jaw quadrant.')
    table(doc, ['Molar Set', 'Age in Wear', 'Laminae', 'Notes'],
        [['M1 (dp2)', '0–2 years', '3–4', 'Tiny; usually shed before examination'],
         ['M2 (dp3)', '2–4 years', '4', 'Small — lower jaw of calves'],
         ['M3 (dp4)', '4–10 years', '5–6', 'Main tooth in juveniles; distinct worn front edge'],
         ['M4 (M1)', '8–22 years', '7–8', 'Sub-adult to young adult — most common in CG casualties'],
         ['M5 (M2)', '15–45 years', '9–10', 'Adult — large, wide, deeply worn ridges'],
         ['M6 (M3)', '30+ years', '12–14', 'Final set — exhaustion → starvation → death']],
        col_widths=[2.5, 2.5, 2.5, 9.5])
    keybox(doc,
        'Molar exhaustion is the primary cause of "old age" death in elephants. '
        'When M6 wears out, the elephant can no longer chew — death follows from malnutrition.')

    h1(doc, '5. Ear Morphology & Thermoregulation')
    table(doc, ['Feature', 'Details'],
        [['Ear area', 'Asian: ~0.5 m² per ear | African: ~1.0 m²'],
         ['Mechanism', 'Flapping increases convective heat loss; blood cools as it flows through dense ear vessels'],
         ['Temperature', 'Ear surface 2–4°C cooler than core body temperature'],
         ['Temporal gland', 'Between eye and ear; swells during musth — secretes temporal fluid']],
        col_widths=[4.5, 12.5])

    h1(doc, '6. Digestive System — Hindgut Fermenters')
    para(doc,
        'Elephants are hindgut fermenters — cellulose fermentation occurs in the large intestine '
        'and caecum. Digestive efficiency is only 40–50% (vs ruminants ~65%), requiring '
        'enormous food intake: 150–200 kg fresh vegetation and 150–200 L water daily.')
    table(doc, ['Segment', 'Capacity / Key Details'],
        [['Stomach', 'Simple monogastric; capacity ~100 L; no forestomach'],
         ['Small intestine', '~19 m length; primary nutrient absorption'],
         ['Caecum', 'Large; major fermentation chamber; capacity ~100 L'],
         ['Large intestine', '~10 m; water reabsorption and secondary fermentation'],
         ['Daily intake', '150–200 kg vegetation | 150–200 L water | 16–18 hrs foraging']],
        col_widths=[4, 13])

    h1(doc, '7. Reproductive System')
    table(doc, ['Parameter', 'Female (Cow)', 'Male (Bull)'],
        [['Sexual maturity', '8–12 years', '12–15 years (social maturity ~20 yrs)'],
         ['Oestrous cycle', '13–17 weeks — longest of all mammals', 'Musth: annual 2–3 month high-testosterone period'],
         ['Gestation', '22 months — longest of all land mammals', '—'],
         ['Birth interval', '4–6 years', '—'],
         ['Litter size', 'Singleton; twins very rare (<1%)', '—'],
         ['Lifespan (wild)', '60–70 years', '50–60 years (injuries reduce bull lifespan)']],
        col_widths=[3.5, 6.5, 7])

    h1(doc, '8. Sensory Capabilities')
    table(doc, ['Sense', 'Capability'],
        [['Olfaction', 'Exceptional — detects water at 19 km, predators, conspecifics, musth individuals'],
         ['Hearing', 'Detects infrasound (1–20 Hz) over 10+ km; seismic detection through feet and trunk'],
         ['Vision', 'Poor colour vision (dichromat); good in dim light; poor at distance'],
         ['Touch', 'Highly sensitive — trunk tip, ears, foot soles (seismic vibration detection)'],
         ['Taste', 'Selective — rejects bitter/toxic plants; geophagy for minerals']],
        col_widths=[3.5, 13.5])

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — Infectious Diseases
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter3(doc):
    chapter_header(doc, '3', 'Infectious Diseases of Asian Elephants',
        'Aetiology, Pathology, Diagnosis & Control',
        'Dr. M. Karikalan  |  ICAR-IVRI, Bareilly')

    h1(doc, '1. Introduction')
    para(doc,
        'Infectious diseases are a growing threat to Asian elephant conservation. Both captive '
        'and wild populations face viral, bacterial, and parasitic pathogens. Many are zoonotic, '
        'posing risk to handlers and veterinary staff. Systematic necropsy, sampling, and laboratory '
        'diagnosis are essential for identifying and managing these threats.')

    h1(doc, '2. EEHV — Elephant Endotheliotropic Herpesvirus (MOST FATAL)')
    keybox(doc,
        'EEHV is the leading infectious cause of death in captive Asian elephant calves worldwide. '
        'Mortality rate >85% once clinical signs appear. Targets calves 1–8 years of age.', danger=True)
    table(doc, ['Feature', 'Details'],
        [['Causative Agent', 'EEHV1A, 1B, 4, 5, 6 (subfamily Betaherpesviridae; genus Proboscivirus)'],
         ['Host', 'Asian elephants — latent in adults; lethal in calves 1–8 years'],
         ['Transmission', 'Direct contact with oral secretions; adult-to-calf likely'],
         ['Pathogenesis', 'Vascular endothelial tropism → haemorrhagic disease → DIC → shock'],
         ['Clinical Signs', 'Sudden lethargy, oedema (head/neck/limbs), cyanotic tongue, haemorrhagic discharge'],
         ['Gross PM Lesions', 'Generalised haemorrhage, oedema, hepatomegaly, splenomegaly, myocarditis'],
         ['Histopathology', 'Intranuclear herpesviral inclusion bodies in endothelial cells — PATHOGNOMONIC'],
         ['Diagnosis', 'qPCR on EDTA blood/trunk wash; IHC on tissue (spleen, heart)'],
         ['Treatment', 'Famciclovir (antiviral); supportive IV fluids; early diagnosis critical'],
         ['CG Surveillance', 'EEHV tested: NEGATIVE in all 13 CG drowning deaths (2021–2026)']],
        col_widths=[4, 13])

    h1(doc, '3. Tuberculosis (TB) — Mycobacterium tuberculosis')
    keybox(doc,
        'Elephant TB is a ZOONOSIS of highest concern. Handlers and veterinary staff are at risk '
        'from aerosol infection via trunk secretions and breath. PPE is NON-NEGOTIABLE.', danger=True)
    table(doc, ['Feature', 'Details'],
        [['Causative Agent', 'Mycobacterium tuberculosis (human strain); M. bovis less common'],
         ['Transmission', 'Aerosol from trunk secretions; direct contact; contaminated feed/water'],
         ['Clinical Signs', 'Weight loss, weakness, intermittent trunk discharge; often subclinical for years'],
         ['PM Lesions', 'Granulomata in lungs, thoracic LN, liver, spleen; cavitation in advanced cases'],
         ['Histopathology', 'Caseous necrosis, Langhans giant cells, lymphocytic infiltration'],
         ['Diagnosis', 'ElephantTB STAT-PAK ELISA; trunk wash culture (MGIT, BSL-3); PCR'],
         ['Zoonotic Risk', 'HIGH — N95 mask, double gloves, full PPE mandatory at necropsy'],
         ['Surveillance', 'Annual trunk wash culture mandatory for all captive elephants (MoEFCC)']],
        col_widths=[4, 13])

    h1(doc, '4. Anthrax — Bacillus anthracis')
    keybox(doc, 'DO NOT OPEN carcass if anthrax suspected — sporulation causes environmental contamination.', danger=True)
    table(doc, ['Feature', 'Details'],
        [['Presentation', 'Peracute death; bloody orifice discharge; bloating; NO rigor mortis'],
         ['Diagnosis', 'Blood smear — McFadyean stain; FAT; PCR (from closed carcass)'],
         ['Zoonotic Risk', 'EXTREME — cutaneous, pulmonary, GI anthrax in humans possible'],
         ['Disposal', 'Incinerate carcass in situ; burial with lime discouraged (spores survive)']],
        col_widths=[3.5, 13.5])

    h1(doc, '5. Other Bacterial Diseases')
    table(doc, ['Pathogen', 'Presentation', 'Key Samples'],
        [['Salmonella spp.', 'Septicaemia, haemorrhagic enteritis; sudden death in calves', 'Intestine, spleen, liver'],
         ['Pasteurella multocida', 'Haemorrhagic septicaemia, pneumonia — captive/stressed animals', 'Lung, lymph nodes, blood'],
         ['Clostridium perfringens', 'Enterotoxaemia, sudden death; haemorrhagic enteritis', 'Intestinal contents (no fixative)'],
         ['Leptospira spp.', 'Jaundice, haemolysis, renal failure — waterborne exposure', 'Kidney, urine, serum (MAT)']],
        col_widths=[4, 7, 6])

    h1(doc, '6. Viral Diseases — Other')
    table(doc, ['Disease', 'Agent', 'Key PM Finding', 'Zoonotic?'],
        [['Elephant Pox', 'Parapoxvirus / Orthopoxvirus', 'Nodular/pustular lesions on trunk, mouth, genitalia', 'YES — handlers'],
         ['EMCV', 'Encephalomyocarditis Virus', 'Myocardial necrosis, pericardial effusion, sudden death', 'Low risk'],
         ['Foot-and-Mouth', 'Aphthovirus', 'Vesicles on feet/trunk/mouth; lameness', 'Very low'],
         ['Rabies', 'Lyssavirus', 'Progressive behavioural change; Negri bodies in brain neurons', 'YES — fatal']],
        col_widths=[3, 3, 6.5, 4.5])

    h1(doc, '7. Parasitic Diseases')
    table(doc, ['Group', 'Species', 'Site', 'Clinical Impact', 'Diagnosis'],
        [['Nematodes', 'Quilonia, Murshidia, Choniangium spp.', 'Large intestine', 'Colic, anaemia in heavy load', 'Faecal flotation, PM'],
         ['Trematodes', 'Brumptia bicaudata', 'Caecum/large intestine', 'Usually subclinical', 'Faecal sediment, PM'],
         ['Protozoa', 'Trypanosoma spp.', 'Blood', 'Emaciation, rarely fatal', 'Blood smear, PCR'],
         ['Ectoparasites', 'Haemaphysalis, Amblyomma ticks; mange mites', 'Skin', 'Anaemia, skin lesions', 'Skin scraping, tick ID']],
        col_widths=[3, 4, 2.5, 4, 3.5])

    h1(doc, '8. Zoonotic Risk at Necropsy — Safety Summary')
    keybox(doc,
        'ALL elephant necropsies carry zoonotic risk. PPE is NON-NEGOTIABLE: double gloves, '
        'N95 mask, eye protection, gown, waterproof boots. Wash + disinfect with 70% alcohol after PM.', danger=True)
    table(doc, ['Disease', 'Risk', 'Route', 'PPE Required'],
        [['Tuberculosis', 'HIGH', 'Aerosol from trunk secretions, breath', 'N95, full PPE, BSL-3 sample handling'],
         ['Anthrax', 'EXTREME', 'Cutaneous, aerosol, ingestion', 'DO NOT OPEN — call BSL-3 specialist'],
         ['Elephant Pox', 'MODERATE', 'Direct contact with lesions', 'Gloves, eye protection'],
         ['Rabies', 'HIGH', 'Bite wound, brain tissue contact', 'Double gloves, face shield for brain exam'],
         ['Leptospirosis', 'MODERATE', 'Urine, kidney tissue contact', 'Waterproof gloves, eye shield']],
        col_widths=[3.5, 2, 5, 6.5])

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 4 — Sample Collection
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter4(doc):
    chapter_header(doc, '4', 'Collection of Biological Materials for Wildlife Disease Diagnosis',
        'Sampling Protocols, Preservation, Packing & Referral',
        'Dr. M. Karikalan  |  ICAR-IVRI, Bareilly')

    h1(doc, '1. Why We Collect Biological Materials')
    para(doc,
        'Biological samples are the irreplaceable foundation of wildlife disease diagnosis. '
        'Without properly collected, preserved, and transported samples, even the most advanced '
        'laboratory cannot establish a definitive cause of death. The pipeline: '
        'Field observation → Sample collection → Chain of custody → Lab analysis → Diagnosis → Management.')
    keybox(doc,
        'RULE 1: Collect early — within 6 hrs of death ideally. '
        'RULE 2: Collect widely — minimum 15 sample types per case. '
        'RULE 3: Label everything — sample ID, date, GPS, animal ID on EVERY tube.')

    h1(doc, '2. Master Sample-Collection Table')
    keybox(doc, 'Collect ALL sample types from EVERY elephant PM — even if cause seems obvious.')
    table(doc, ['Sample Type', 'Volume', 'Container', 'Preservation', 'Tests'],
        [['EDTA Blood', '5–10 mL', 'Purple-top tube', 'Ice 4°C — DO NOT freeze', 'CBC, PCR (EEHV, TB), haematology'],
         ['Serum', '10 mL', 'Red-top → aliquot', 'Centrifuge; freeze at -20°C', 'ELISA, serology, biochemistry'],
         ['Urine', '20–50 mL', 'Sterile container', 'Refrigerate or freeze', 'Urinalysis, toxicology, leptospira'],
         ['Trunk/Nasal Swab', '2 swabs', 'VTM', 'Ice — ship within 24 hrs', 'EEHV, Herpesvirus, Influenza PCR'],
         ['Faeces', '30–50 g', 'Sterile container', 'Refrigerate; fix portion in formalin', 'Parasitology, bacteriology'],
         ['Lung (fresh)', '5×5 cm', 'Sterile zip-lock', '-20°C', 'Histopath, bacteriology, virology'],
         ['Lung (fixed)', '5×5 cm', '10% NBF jar', 'Room temp', 'Histopathology'],
         ['Liver', '5×5 cm each', 'Zip-lock + NBF jar', '-20°C fresh; RT fixed', 'Histopath, toxicology, culture'],
         ['Spleen', '5×5 cm each', 'Zip-lock + NBF jar', '-20°C fresh; RT fixed', 'PCR (EEHV/TB), histopath, culture'],
         ['Kidney', '5×5 cm each', 'Zip-lock + NBF jar', '-20°C fresh; RT fixed', 'Histopath, leptospira, toxicology'],
         ['Heart', '5×5 cm each', 'Zip-lock + NBF jar', '-20°C fresh; RT fixed', 'EMCV, bacterial culture, histopath'],
         ['Lymph nodes', '1–2 nodes', 'Zip-lock + NBF jar', '-20°C fresh; RT fixed', 'TB, EEHV, bacterial culture'],
         ['Brain', 'Half brain', 'NBF + fresh zip-lock', '-20°C fresh; RT fixed', 'Rabies, histopath, NiV, PCR'],
         ['Bone marrow', '5–10 mL', 'EDTA tube or zip-lock', 'Freeze -20°C', 'Diatom test, haematology, toxicology'],
         ['Stomach contents', '100–200 mL', 'Sterile wide-mouth jar', 'Freeze -20°C', 'Toxicology (all classes)'],
         ['Water/soil', '500 mL / 200 g', 'Sterile bottles', 'Refrigerate', 'Arsenic, heavy metals, cyanobacterial toxins']],
        col_widths=[3.5, 2.5, 3, 3.5, 4.5])

    h1(doc, '3. 10% Neutral Buffered Formalin (NBF) — Preparation')
    table(doc, ['Component', 'Amount / Details'],
        [['40% Formaldehyde solution', '100 mL'],
         ['NaH₂PO₄·H₂O (monobasic sodium phosphate)', '3.5 g'],
         ['Na₂HPO₄ anhydrous (dibasic sodium phosphate)', '6.5 g'],
         ['Distilled water', 'Make up to 1,000 mL'],
         ['Final pH', '7.0–7.4 (neutral)'],
         ['Tissue:Formalin ratio', '1:10 — 1 part tissue to 10 parts formalin'],
         ['Maximum tissue thickness', '1 cm slices for adequate penetration within 24–48 hrs']],
        col_widths=[7, 10])
    keybox(doc,
        'CRITICAL: Slice tissue to max 1 cm before fixing. Too little formalin or too thick '
        'tissue → autolysis in centre. Over-fixing (>72 hrs) → DNA degradation for PCR.')

    h1(doc, '4. Toxicological Sampling')
    table(doc, ['Sample', 'Amount', 'Target Toxins'],
        [['Stomach/rumen contents', '100–200 mL — FREEZE', 'ALL toxins — primary toxicology sample'],
         ['Liver', '100–200 g — FREEZE', 'Metals, organochlorine, alkaloids, CPA, aflatoxins'],
         ['Kidney', '50–100 g — FREEZE', 'Heavy metals (Pb, Hg, Cd, As)'],
         ['EDTA blood', '10 mL — FREEZE', 'Organophosphate, nitrate, anticoagulants'],
         ['Urine', '50 mL — FREEZE', 'Metal metabolites, pesticide residues'],
         ['Bone marrow', '5–10 g — FREEZE', 'Chronic heavy metal exposure'],
         ['Feed/fodder', '500 g — FREEZE', 'Mycotoxins (CPA, aflatoxin), pesticides'],
         ['Water', '500 mL — glass bottle', 'Arsenic, cyanobacterial toxins, nitrate'],
         ['Soil', '200 g — sterile bag', 'Arsenic, persistent organic pollutants']],
        col_widths=[4, 3.5, 9.5])

    h1(doc, '5. 10-Step Packing Protocol')
    for step in [
        '1. Label ALL containers before collection — waterproof marker; never adhesive labels alone',
        '2. Fill primary container — leave 10% headspace for expansion during freezing',
        '3. Seal with parafilm + tape — double-seal all liquid samples',
        '4. Wrap in absorbent material (cotton/paper) — enough to absorb total sample volume if spilled',
        '5. Place in secondary leak-proof container (zip-lock or screw-top)',
        '6. Pack in triple-wall corrugated box with ice packs (minimum 2 kg ice per case)',
        '7. Insert completed sample submission form INSIDE box (not only on outside)',
        '8. Seal outer box with security tape — sign across seal for chain of custody',
        '9. Label outer box: BIOLOGICAL SPECIMEN — FRAGILE — KEEP COOL',
        '10. Notify laboratory before dispatch — confirm receipt within 24 hrs of arrival',
    ]:
        bullet(doc, step)
    doc.add_paragraph()

    h1(doc, '6. National Referral Laboratories')
    table(doc, ['Laboratory', 'Tests Available', 'Contact'],
        [['ICAR-IVRI, Bareilly (UP)', 'EEHV PCR, histopath, bacteriology, toxicology, serology, virology',
          '0581-2301502 | ivri@icar.org.in'],
         ['NDVSU, Jabalpur (MP)', 'Wildlife pathology, PM diagnosis, toxicology, histopathology',
          '0761-2600204'],
         ['WII, Dehradun (UK)', 'Wildlife disease surveillance, population health, ecology',
          '0135-2640112'],
         ['NCDC, New Delhi', 'Zoonotic diseases — anthrax, rabies, TB confirmation, public health',
          '011-23921401']],
        col_widths=[4, 9, 4])

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 5 — Non-Infectious Diseases
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter5(doc):
    chapter_header(doc, '5', 'Non-Infectious Diseases in Asian Elephants',
        'Toxicoses, Physical Trauma, Nutritional Deficiencies & Field Investigation',
        'Dr. Karikalan Mathesh  |  ICAR-IVRI, Bareilly')

    h1(doc, '1. Background — Biological Vulnerability of Elephants')
    table(doc, ['Factor', 'Implication for Non-Infectious Disease'],
        [['20 copies of TP53 gene', 'Cancer resistance (Peto\'s Paradox) — very rare in elephants'],
         ['Large body mass', 'Requires enormous food intake → higher exposure to contaminated feed'],
         ['Hindgut fermentation', 'Mycotoxins amplified by gut flora; longer transit time'],
         ['Low metabolic rate', 'Slower toxin clearance than smaller mammals'],
         ['Indiscriminate feeding (stressed)', 'Captive/crop-raiding elephants consume contaminated grain'],
         ['Sensitive endothelium', 'Vascular endothelium highly susceptible to oxidative toxin damage']],
        col_widths=[5, 12])

    h1(doc, '2. Case Study — Mass Mortality, Bandhavgarh NP (October 2024)')
    keybox(doc,
        'October 2024: 10 Asian elephant deaths in 4 days in Bandhavgarh Tiger Reserve. '
        'CONFIRMED: Cyclopiazonic Acid (CPA) toxicosis from Kodo millet (Paspalum scrobiculatum). '
        'LC-MS confirmed at ICRISAT, Hyderabad.', danger=True)
    para(doc,
        'A herd of ~10 elephants fed on Kodo millet crop fields at the edge of the reserve. '
        'Within 12–24 hrs: sudden collapse, ataxia, hypersalivation, depression, recumbency. '
        'Rapid deaths over 4 days. No infectious disease in the area.')
    h2(doc, 'Gross PM Findings')
    table(doc, ['Organ', 'Gross Finding'],
        [['Liver', 'Pale, friable, enlarged; centrilobular necrosis on cut section'],
         ['Kidneys', 'Pale, swollen; cortical pallor'],
         ['Intestines', 'Haemorrhagic enteritis; reddened mucosa with petechiae'],
         ['Lungs', 'Congested, oedematous (secondary to cardiovascular shock)'],
         ['Heart', 'Petechiae on epicardium; myocardial pallor in some animals']],
        col_widths=[4, 13])
    h2(doc, 'Toxicology Results — LC-MS (ICRISAT Hyderabad)')
    table(doc, ['Sample', 'CPA Result', 'Level'],
        [['Stomach contents', 'POSITIVE', 'High (>50 ppb)'],
         ['Liver', 'POSITIVE', 'Moderate (10–25 ppb)'],
         ['Kodo millet (field sample)', 'POSITIVE', 'Very high (>200 ppb) — contaminated grain'],
         ['EEHV PCR / Heavy metals / Pesticides', 'ALL NEGATIVE', '—']],
        col_widths=[6, 4, 7])

    h1(doc, '3. Cyclopiazonic Acid (CPA) — Key Facts')
    table(doc, ['Parameter', 'Details'],
        [['Producing fungi', 'Aspergillus flavus, A. oryzae, Penicillium cyclopium'],
         ['Substrate', 'Kodo millet (Paspalum scrobiculatum), maize, groundnut, sorghum'],
         ['Peak risk season', 'Post-monsoon harvest (Oct–Dec) — wet grain in humid storage'],
         ['Mechanism', 'Inhibits Ca²⁺-ATPase pump (SERCA) → intracellular calcium disruption → cell death'],
         ['Target organs', 'Liver, kidney, heart, GI tract'],
         ['Detection', 'LC-MS/MS (gold standard); ELISA; TLC for screening'],
         ['Prevention', 'Prevent elephant access to Kodo fields Oct–Dec; moisture-controlled storage (<14%)']],
        col_widths=[4.5, 12.5])

    h1(doc, '4. Electrocution')
    keybox(doc,
        'Electrocution = 47% of CG elephant deaths (2021–2026). 23 deaths confirmed. '
        'Oct–Dec peak — illegal electric fencing to protect paddy/maize crops.', danger=True)
    table(doc, ['Parameter', 'Lightning Strike', 'High Voltage (HV) Line', 'Low Voltage (LV) Fence'],
        [['Voltage', '>100 million V', '11 kV–132 kV', '220 V–440 V AC'],
         ['Entry wound', 'Large irregular char mark', 'Deep char at contact point', 'Small or absent'],
         ['Herd effect', 'YES — side-potential kills multiple', 'Step-potential affects nearby', 'Direct contact only'],
         ['Scene evidence', 'Split trees; no lines', 'Broken line; fused wire ends', 'Illegal fence wire at scene'],
         ['PM key finding', 'Lichtenberg marks; haemorrhage', 'Char + linear muscle haemorrhage', 'Cardiac arrest; subtle']],
        col_widths=[3.5, 4, 4.5, 5])

    h1(doc, '5. Lightning Side-Potential (Herd Mortality)')
    para(doc,
        'When lightning strikes near a herd, ground current radiates in concentric circles. '
        'Front and back legs are at different potentials — current flows through the body. '
        'Calves and smaller animals are most susceptible. Multiple simultaneous deaths at the '
        'same location during/after a storm strongly indicates lightning side-potential.')

    h1(doc, '6. Nutritional Deficiencies')
    table(doc, ['Deficiency', 'Mechanism', 'Clinical Signs', 'PM Findings', 'Key Sample'],
        [['Iron (Fe)', 'Reduced haemoglobin; anaemia', 'Pallor, weakness, tachycardia', 'Thin watery blood; pale marrow', 'CBC, serum iron, ferritin'],
         ['Vit. E / Selenium', 'Oxidative muscle damage', 'White muscle disease, sudden death', 'Pale white streaks in cardiac/skeletal muscle', 'Serum selenium, muscle biopsy'],
         ['Calcium/Phosphorus', 'Bone resorption', 'Pathological fractures, stiff gait', 'Soft/rubbery bones', 'Serum Ca/P; bone biopsy'],
         ['Copper (Cu)', 'Enzyme dysfunction, demyelination', 'Depigmentation, weakness, diarrhoea', 'Swaybacker lesions; low hepatic copper', 'Liver, serum copper']],
        col_widths=[2.5, 4, 3.5, 3.5, 3.5])

    h1(doc, '7. Field Investigation Framework')
    table(doc, ['Phase', 'Action Items'],
        [['Scene Assessment', 'GPS; photograph scene before disturbing; note carcass position, vegetation damage, wire/equipment present'],
         ['History', 'When last seen alive; feed/water sources; recent weather; herd composition; unusual activity (crop-raiding, musth)'],
         ['External Examination', 'Char marks, wounds, tusk damage, skin condition, orifice discharge, body condition score, age estimate'],
         ['PM Examination', 'Systematic organ examination; photograph all lesions; weigh organs where possible'],
         ['Sample Collection', 'All samples from master list; maintain cold chain; double-label every sample'],
         ['Environmental Samples', 'Water (nearby sources), soil (around carcass), feed/fodder from last known feeding site'],
         ['Documentation', 'Complete PM report with GPS, photographs, sample list; chain of custody form for all samples'],
         ['Reporting', 'Verbal report to CF/PCCF within 24 hrs; written report within 72 hrs']],
        col_widths=[3.5, 13.5])

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 6 — Non-Infectious Pathology
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter6(doc):
    chapter_header(doc, '6', 'Non-Infectious Pathology in Asian Elephants',
        'Toxicoses, Electrocution, Reproductive Disorders & Metabolic Diseases',
        'Prof. Dr. A. B. Shrivastava  |  NDVSU, Jabalpur')

    h1(doc, '1. Routes of Poisoning')
    table(doc, ['Route', 'Sources', 'Examples in Elephants'],
        [['Ingestion', 'Contaminated feed, water bodies, toxic plants, bait',
          'Kodo millet (CPA), cyanobacterial toxins, toxic plants, HCN plants'],
         ['Inhalation', 'Industrial fumes, pesticide spray, wildfire smoke',
          'Organophosphate aerosol, CO from generators'],
         ['Skin Absorption', 'Pesticidal dip, topical application, contaminated mud',
          'Organochlorine absorption, caustic burns']],
        col_widths=[3, 5, 9])

    h1(doc, '2. Mycotoxins — CPA & Kodo Millet Pathology')
    h2(doc, 'Organ-level Pathology in CPA Toxicosis')
    table(doc, ['Organ', 'Gross Finding', 'Histopathology'],
        [['Liver', 'Pale, enlarged; centrilobular necrosis', 'Hepatocyte necrosis, vacuolation, bile duct proliferation'],
         ['Kidneys', 'Pale, swollen cortex', 'Proximal tubular degeneration, cast formation'],
         ['Heart', 'Pale myocardium', 'Myofibre necrosis, interstitial oedema, mononuclear infiltration'],
         ['GI Tract', 'Haemorrhagic gastroenteritis', 'Villous blunting, mucosal erosion, crypt necrosis']],
        col_widths=[3, 6, 8])
    h2(doc, 'Cyanobacterial (Blue-Green Algae) Toxins')
    table(doc, ['Feature', 'Details'],
        [['Organisms', 'Microcystis aeruginosa, Anabaena, Oscillatoria — bloom in stagnant warm water'],
         ['Toxins', 'Microcystins (liver), Anatoxins (neurotoxic), Cylindrospermopsin (kidney)'],
         ['Gross PM', 'Pale necrotic liver; swollen kidneys; GI haemorrhage; blood fails to clot'],
         ['Diagnosis', 'ELISA for microcystin in water/liver; LC-MS for quantification'],
         ['CG Relevance', 'Dam/pond environments in Tamnar/Kharsia — potential arsenic co-contamination suspected']],
        col_widths=[3.5, 13.5])
    h2(doc, 'Toxic Plants')
    table(doc, ['Plant', 'Toxic Principle', 'Clinical Effects', 'PM Findings'],
        [['Lantana camara', 'Lantadene A & B (triterpenoids)', 'Photosensitisation, jaundice', 'Cholestasis, bile duct proliferation'],
         ['Calotropis procera', 'Calotoxin (cardiac glycoside)', 'Cardiac arrest, hypersalivation', 'Cardiac changes, haemorrhage'],
         ['Datura spp.', 'Scopolamine, atropine', 'Dilated pupils, tachycardia, coma', 'No specific lesion; stomach contents key'],
         ['Castor bean (Ricinus)', 'Ricin (cytotoxin)', 'Acute organ failure, haemorrhage, death', 'Severe GI and organ haemorrhage']],
        col_widths=[4, 3.5, 4.5, 5])

    h1(doc, '3. HCN (Hydrocyanic Acid) Poisoning')
    table(doc, ['Feature', 'Details'],
        [['Sources', 'Young sorghum, cassava, bamboo shoots, Johnson grass, Prunus seeds'],
         ['Mechanism', 'CN⁻ binds cytochrome c oxidase → inhibits cellular respiration → histotoxic anoxia'],
         ['Speed', 'Peracute — death within minutes to 2 hrs; animals found dead without warning'],
         ['Clinical Signs', 'Bright red mucosae (oxyhemoglobin), hyperpnoea, collapse, convulsions'],
         ['Gross PM', 'Cherry-red blood and organs; no rigor mortis; bitter almond smell'],
         ['Diagnosis', 'Conway microdiffusion on fresh stomach contents — must run within hours'],
         ['Treatment', 'Sodium nitrite (3 mg/kg IV) + Sodium thiosulfate (660 mg/kg IV) — emergency antidote']],
        col_widths=[4, 13])
    h2(doc, 'Jabalpur Case — 5 Captive Elephants (Circus)')
    table(doc, ['Parameter', 'Details'],
        [['Feed implicated', 'Freshly cut sorghum — drought-stressed young plants with high HCN'],
         ['Clinical signs', 'Bright red mucosae; hyperpnoea; collapse within 30 min of feeding'],
         ['Treatment', 'Sodium nitrite IV + Sodium thiosulfate IV; supportive care'],
         [('Outcome', True), ('3 survived; 2 died within 2 hrs. Conway test POSITIVE in deceased.', True)]],
        col_widths=[4.5, 12.5])

    h1(doc, '4. Electrocution — Pathological Terminology')
    table(doc, ['Term', 'Definition', 'PM Significance'],
        [['Joule heating', 'Heat generated in tissue by electrical current', 'Causes muscle necrosis along current path'],
         ['Ventricular fibrillation', 'Cardiac arrhythmia from AC at 50 Hz', 'Primary cause of death — AC more dangerous than DC'],
         ['Flash burns', 'Burns from electrical arc — no direct contact needed', 'Superficial burns without entry/exit wounds'],
         ['Step potential', 'Voltage gradient on ground near HV line', 'Multiple animals electrocuted without touching line'],
         ['Touch potential', 'Voltage between contact point and ground', 'Single animal — leans on energised object']],
        col_widths=[3.5, 5, 8.5])

    h1(doc, '5. Pyometra in Female Elephants')
    table(doc, ['Parameter', 'Details'],
        [['Definition', 'Accumulation of pus in the uterus — life-threatening if untreated'],
         ['Affected group', 'Captive adult cows; long inter-calving intervals; hormonal manipulation'],
         ['Common organisms', 'E. coli, Streptococcus, Staphylococcus, Pseudomonas, Clostridium spp.'],
         ['PM Findings', 'Uterus massively distended with foul-smelling purulent exudate; wall thickened, friable; adhesions'],
         ['Histopathology', 'Suppurative endometritis, glandular destruction, bacterial colonies, oedema'],
         ['Treatment', 'Oxytocin (drainage), PGF2α (luteolysis), broad-spectrum antibiotics; surgical drainage']],
        col_widths=[4, 13])

    h1(doc, '6. Hyperthermia')
    table(doc, ['Parameter', 'Details'],
        [['Normal rectal temp', '35.5–37.5°C'],
         ['Danger threshold', '>38.5°C (concern); >39.5°C (critical)'],
         ['Predisposing factors', 'Restricted water access, direct sun, unventilated transport, exertion in heat, musth'],
         ['Mechanism', 'Core temp rises → cerebral oedema → neuronal dysfunction → seizures → death'],
         ['Gross PM', 'Cerebral oedema, petechiae, congestion of all organs; rapid decomposition'],
         ['Cooling', 'Shade + continuous cold water (IV + external) + ice packs on head/ears/legs']],
        col_widths=[4, 13])

    h1(doc, '7. Iron Deficiency Anaemia')
    table(doc, ['Parameter', 'Details'],
        [['Risk group', 'Captive calves on restricted diet; calves born to iron-deficient cows'],
         ['Signs', 'Pallor, weakness, tachycardia, poor growth, pica (eating soil — geophagy)'],
         ['Diagnosis', 'CBC: low PCV, Hb, MCV, MCH; low serum iron; high TIBC; low ferritin'],
         ['PM Findings', 'Pale thin watery blood; pale mucosae and muscle; hypoplastic bone marrow'],
         ['Treatment', 'Iron dextran IM (10–20 mg/kg); dietary supplementation; mineral licks']],
        col_widths=[4, 13])

    h1(doc, '8. Quick Reference — Non-Infectious Conditions')
    table(doc, ['Condition', 'Key PM Finding', 'Key Sample', 'Diagnosis Method'],
        [['CPA Toxicosis', 'Pale liver, haemorrhagic enteritis', 'Stomach contents, liver', 'LC-MS for CPA'],
         ['HCN Poisoning', 'Cherry-red blood, bitter almond smell', 'Stomach contents (fresh)', 'Conway microdiffusion'],
         ['Cyanobacterial toxin', 'Liver necrosis, GI haemorrhage', 'Water, liver', 'ELISA/LC-MS microcystin'],
         ['Electrocution', 'Char marks at entry/exit, cardiac arrest', 'Skin at marks; heart', 'Gross PM + scene evidence'],
         ['Pyometra', 'Pus-filled uterus, adhesions', 'Uterine pus', 'Culture + sensitivity'],
         ['Hyperthermia', 'Cerebral oedema, congestion, rapid decomp', 'Brain, vitreous humour', 'Histopath; temp at PM'],
         ['Iron deficiency', 'Pale watery blood, pale bone marrow', 'EDTA blood, bone marrow', 'CBC, serum iron, ferritin'],
         ['Toxic plants', 'Liver/GI/cardiac changes (variable)', 'Stomach contents, liver', 'LC-MS; botanical ID']],
        col_widths=[4, 4.5, 3.5, 5])

    page_break(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 7 — Postmortem Examination
# ═══════════════════════════════════════════════════════════════════════════════

def add_chapter7(doc):
    chapter_header(doc, '7', 'Postmortem Examination of the Asian Elephant',
        'Principles, Procedure, Documentation & Differential Diagnosis',
        'Prof. Dr. A. B. Shrivastav  |  NDVSU, Jabalpur')

    keybox(doc,
        '"The carcass never tells a lie — but you must know how to ask the right questions."\n'
        '  — Dr. R. K. Satpati, Wildlife Institute of India', gold=True)

    h1(doc, '1. Key Definitions')
    table(doc, ['Term', 'Definition'],
        [['Necropsy', 'Postmortem examination of an animal (Gr: nekros = dead; opsis = view)'],
         ['Cause of Death (CoD)', 'Pathological condition or injury directly responsible for death'],
         ['Manner of Death', 'Natural, accidental, homicidal, suicidal, undetermined'],
         ['Contributing Factor', 'Condition that worsened outcome but was not the direct cause'],
         ['Time Since Death (TSD)', 'Estimated interval — based on PM changes, temperature, entomology'],
         ['Chain of Custody', 'Documented record of sample handling from collection to laboratory'],
         ['Rigor Mortis', 'Temporary muscle stiffening 2–6 hrs post-death; resolves by 24–36 hrs'],
         ['Livor Mortis', 'Purple discolouration of dependent surfaces due to blood pooling'],
         ['Algor Mortis', 'Body temperature drop post-death (~1°C/hr in still air at 20°C)']],
        col_widths=[4.5, 12.5])

    h2(doc, 'Six Key Principles of Elephant Necropsy')
    for p in [
        '1. SPEED: PM within 6 hours of death ideally — tropical climate causes rapid decomposition. Max 12 hours.',
        '2. SAFETY: PPE mandatory — double gloves, N95 mask, eye protection, gown, waterproof boots.',
        '3. SYSTEMATIC: Fixed sequence every time — external → thorax → abdomen → head. Never skip steps.',
        '4. SAMPLING: Collect ALL samples from master list BEFORE organ examination begins.',
        '5. DOCUMENTATION: Photograph every finding before disturbing. GPS + written field notes throughout.',
        '6. CHAIN OF CUSTODY: Label every sample immediately. Fill submission form. Witness signatures on forensic samples.',
    ]:
        bullet(doc, p)
    doc.add_paragraph()

    h1(doc, '2. Pre-Necropsy Preparation')
    table(doc, ['Category', 'Requirements'],
        [['Team', 'Min. 4 persons: PM lead veterinarian, scribe, photographer, sample handler + 2–4 field staff'],
         ['PPE', 'Double gloves, N95 masks (6+ per person), full gown/PPE suit, goggles, waterproof boots'],
         ['Instruments', '2 large PM knives, hand saw/bone saw, rib shears, forceps (toothed + plain), spreader'],
         ['Sample supplies', 'EDTA tubes, red-top tubes, sterile zip-locks, NBF jars (pre-filled), VTM, swabs'],
         ['Cold chain', 'Ice box with ice packs (min. 2 kg ice per case); freezer access within 6 hrs preferred'],
         ['Documentation', 'Field notebook, waterproof markers, GPS device, camera with date/GPS metadata, PM report form']],
        col_widths=[3.5, 13.5])

    h1(doc, '3. Step-by-Step PM Workflow')
    table(doc, ['Step', 'Action', 'Key Observations / Notes'],
        [['1. Scene', 'GPS; photos before disturbing; position, orientation, environment, evidence (wire, tracks)',
          'Note electric wire, water body, tracks, vegetation damage'],
         ['2. External Exam', 'Body condition; skin; wounds; orifices; sex; age estimate from size',
          'Char marks, trauma, discharge, dehydration — all photographed with scale'],
         ['3. Measurements', 'Shoulder height, head length, tusk length/weight, body weight estimate',
          'Required for age estimation, sex confirmation, forensic record'],
         ['4. PM Changes', 'Rigor, livor, decomposition stage, bloat, skin slippage',
          'Estimate time since death; affects sample quality'],
         ['5. Blood Collection', 'Jugular/cardiac puncture for EDTA + serum before any incision',
          'CRITICAL — do before opening carcass'],
         ['6. Skin Incision', 'Ventral midline jaw to perineum; reflect skin laterally',
          'Examine subcutaneous tissue, mammary gland, muscle'],
         ['7. Thoracic Cavity', 'Cut ribs; note lung position, fluid, adhesions; examine pericardium',
          'Drowning: lungs; Electrocution: heart; EMCV: myocarditis'],
         ['8. Abdominal Cavity', 'Open xiphoid to pubis; assess organs in situ before removal',
          'Liver, spleen, GI tract, reproductive organs, kidneys'],
         ['9. Organ Exam', 'Remove and examine each organ; note size, weight, texture, colour',
          'Collect fresh + fixed samples from every organ'],
         ['10. Head', 'Remove head; saw calvarium; brain; oral cavity; molar teeth',
          'Age by molar; brain for rabies/NiV; turbinates for herpes'],
         ['11. Molar Age', 'Identify molar set (M1–M6) in wear; count laminae',
          'Record which M is present in each jaw quadrant'],
         ['12. Lymph nodes', 'Survey superficial + deep nodes systematically',
          'Enlargement, abscess, necrosis — key TB/EEHV indicator']],
        col_widths=[1.5, 6.5, 9])

    h1(doc, '4. Post-Mortem Changes — TSD Estimation')
    table(doc, ['PM Change', 'Onset', 'Duration', 'Use for TSD'],
        [['Algor mortis', 'Immediate — 1°C/hr', 'Until ambient temp', 'Core temp vs ambient → estimate hrs post-death'],
         ['Rigor mortis', '2–6 hrs (faster in heat)', 'Resolves 24–48 hrs', 'Present = <24 hrs; absent after resolution = >48 hrs'],
         ['Livor mortis', '1–3 hrs', 'Fixed by 8–12 hrs', 'Blanches = <8 hrs; fixed = >12 hrs']],
        col_widths=[3.5, 3.5, 3.5, 6.5])

    h1(doc, '5. Molar Age Estimation Guide')
    table(doc, ['Molar Set', 'Age in Wear', 'Laminae', 'Field Identification'],
        [['M1 (dp2)', '0–2 years', '3–4', 'Tiny; shed before examination in most cases'],
         ['M2 (dp3)', '2–4 years', '4', 'Small — lower jaw of calves'],
         ['M3 (dp4)', '4–10 years', '5–6', 'Medium — main tooth in juveniles; worn front edge'],
         ['M4 (M1)', '8–22 years', '7–8', 'Sub-adult to young adult — most common in CG casualties'],
         ['M5 (M2)', '15–45 years', '9–10', 'Adult — large, wide, deeply worn ridges'],
         ['M6 (M3)', '30+ years', '12–14', 'Old — final set; wear indicates remaining lifespan']],
        col_widths=[2.5, 2.5, 2.5, 9.5])

    h1(doc, '6. Instruments & Equipment')
    table(doc, ['Instrument', 'Purpose', 'Qty'],
        [['Postmortem knife (large)', 'Primary incisions, organ sectioning', '2 (one spare)'],
         ['Butcher / boning knife', 'Muscle dissection, skinning', '2'],
         ['Hand saw / reciprocating bone saw', 'Rib cuts, calvarium opening', '1'],
         ['Rib shears / heavy scissors', 'Costal cartilage, pericardium', '1 pair'],
         ['Enterotome (intestinal scissors)', 'Opening stomach and intestines', '1'],
         ['Forceps (toothed + plain)', 'Tissue handling, lymph node dissection', '2 pairs each'],
         ['Spreader / retractor', 'Holding cavity open during examination', '2'],
         ['Scale (spring balance)', 'Organ weights (10 kg capacity)', '1'],
         ['Rope & pulleys', 'Positioning carcass — essential for elephant size', '10 m × 4'],
         ['Tarpaulin sheet', 'Working surface under carcass; sample table', '2 (4×4 m)'],
         ['Generator + lights', 'If PM after sunset', 'As available']],
        col_widths=[5, 7, 5])

    h1(doc, '7. External Examination — 11-Point Checklist')
    table(doc, ['#', 'Parameter', 'What to Look For'],
        [['1', 'Body Condition', 'Emaciated / Poor / Fair / Good / Obese; muscle wastage'],
         ['2', 'Sex', 'External genitalia; inter-mammary distance (female); tusk presence'],
         ['3', 'Age Estimate', 'Body size class; molar palpation; shoulder height'],
         ['4', 'Skin', 'Wounds, char marks, ulcers, pox lesions, depigmentation'],
         ['5', 'Head & Face', 'Eye clarity, temporal gland swelling, depigmentation patterns'],
         ['6', 'Trunk', 'Nasal/oral discharge — character, colour, smell; swab for culture/PCR'],
         ['7', 'Feet', 'Sole condition, nail cracks, arthritis, pad injury; electrocution marks'],
         ['8', 'Tail', 'Length, condition; cut tail = poaching indicator'],
         ['9', 'Tusk', 'Present/absent; length, weight; saw cuts = poaching; tip damage'],
         ['10', 'Genitalia', 'Female: lactation, pregnancy, vulval discharge; Male: musth, scrotal abnormalities'],
         ['11', 'Orifices', 'Nasal: froth/blood. Oral: ulcers, wear. Anus: haemorrhage, content colour']],
        col_widths=[0.8, 3.5, 12.7])

    h1(doc, '8. Lymph Node Survey')
    table(doc, ['Node', 'Location', 'Drains / Significance'],
        [['Parotid LN', 'Ventral to ear, lateral to masseter', 'Head, ear, parotid gland'],
         ['Submandibular LN', 'Under jaw, near salivary gland', 'Lower jaw, tongue, floor of mouth'],
         ['Prescapular LN', 'Cranial to shoulder joint', 'Forelimb, shoulder, neck'],
         ['Mediastinal LN', 'Thoracic cavity, tracheal bifurcation', 'TB — most enlarged here; EEHV; lung'],
         ['Mesenteric LN', 'Root of mesentery', 'Salmonella, Clostridium, intestinal TB'],
         ['Hepatic/Portal LN', 'Hepatic hilum, portal vein', 'Liver disease, TB, EEHV']],
        col_widths=[3.5, 5, 8.5])

    h1(doc, '9. EEHV — Histopathological Findings')
    table(doc, ['Organ', 'Histopathological Finding'],
        [['Blood vessel endothelium', 'Intranuclear herpesviral inclusion bodies (Cowdry type A) — PATHOGNOMONIC'],
         ['Heart', 'Myocarditis; endothelial inclusions in cardiac vessels; myofibre degeneration'],
         ['Tongue/mouth', 'Ulceration; haemorrhage; endothelial inclusions in submucosal vessels'],
         ['Liver', 'Periportal haemorrhage; hepatocyte degeneration; sinusoidal endothelial inclusions'],
         ['Spleen', 'Lymphoid depletion; haemorrhage; endothelial inclusions'],
         ['Lymph nodes', 'Haemorrhage; lymphoid depletion; fibrinous exudate']],
        col_widths=[4, 13])

    h1(doc, '10. Differential Diagnosis — Key Elephant Deaths')
    table(doc, ['Condition', 'Key Distinguishing PM Finding', 'Confirmatory Test'],
        [['EEHV haemorrhagic disease', 'Intranuclear inclusions in endothelium; generalised haemorrhage; calf 1–8 yrs', 'qPCR (blood/spleen); IHC'],
         ['Tuberculosis', 'Granulomata in lungs/LN; caseous necrosis; Langhans giant cells', 'Trunk wash culture (MGIT); ELISA; PCR'],
         ['Anthrax', 'Peracute death; bloody orifice discharge; no rigor — DO NOT OPEN', 'McFadyean stain; FAT; PCR (BSL-3)'],
         ['CPA Toxicosis', 'Pale friable liver; haemorrhagic enteritis; millet in stomach', 'LC-MS for CPA in stomach/liver'],
         ['Electrocution', 'Char marks at entry/exit; cardiac arrest; no organ-specific pathology', 'Scene + gross PM + wire analysis'],
         ['Drowning', 'Waterlogged lungs; frothy trachea; water in GI; no char marks', 'Diatom test (bone marrow)'],
         ['Rabies', 'Aggression/behaviour change ante-mortem; found in forest', 'Seller\'s stain + FAT + PCR on brain'],
         ['HCN Poisoning', 'Cherry-red blood; bitter almond smell; peracute death', 'Conway microdiffusion (fresh stomach contents)']],
        col_widths=[4, 6.5, 6.5])

    h1(doc, '11. PM Report — Documentation Checklist')
    table(doc, ['Section', 'Items to Include'],
        [['Case ID', 'Case No., Date, Time, GPS, Forest Division, Range, Beat'],
         ['Animal Details', 'Species, Sex, Age class, Body weight estimate, Tusk status, ID marks'],
         ['History', 'Date/time found, last seen alive, reporting person, circumstances'],
         ['External Exam', 'All 11-point checklist items; wound measurements; photographs with scale'],
         ['PM Changes', 'Rigor/livor/algor status; decomposition stage; estimated TSD'],
         ['Thoracic Cavity', 'Fluid volumes; lung (L/R separately); heart; pericardium; mediastinal LN'],
         ['Abdominal Cavity', 'Liver; spleen; kidneys; GI tract (each segment); reproductive organs'],
         ['Head', 'Brain; molar teeth (M1–M6); nasal turbinates; tongue; eyes'],
         ['Samples Collected', 'Complete list with container, volume, preservation, cold chain status'],
         ['Provisional CoD', 'Based on gross PM — to be confirmed by laboratory results'],
         ['Recommendations', 'Any immediate management action; environmental investigation needed'],
         ['Signatures', 'Lead vet, assisting staff, forest officer present, date, official stamp']],
        col_widths=[4, 13])

    keybox(doc,
        '"Doctors who perform necropsies gain wisdom that no textbook can teach. '
        'The postmortem examination is the final clinical act — performed for the living, not the dead."\n'
        '  — Prof. Dr. A. B. Shrivastav, NDVSU Jabalpur (2014)', gold=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width   = Cm(21)
    sec.page_height  = Cm(29.7)
    sec.left_margin  = sec.right_margin  = Cm(2.0)
    sec.top_margin   = sec.bottom_margin = Cm(1.8)
    doc.core_properties.title  = 'Workshop Proceedings — Mortality Investigation of Asian Elephant 2026'
    doc.core_properties.author = 'Chhattisgarh Forest Department'

    print('  Adding title page & TOC...')
    add_title_page(doc)

    print('  Adding Overview...')
    add_overview(doc)

    print('  Adding Chapter 1 — Mortality Analysis...')
    add_chapter1(doc)

    print('  Adding Chapter 2 — Anatomy...')
    add_chapter2(doc)

    print('  Adding Chapter 3 — Infectious Diseases...')
    add_chapter3(doc)

    print('  Adding Chapter 4 — Sample Collection...')
    add_chapter4(doc)

    print('  Adding Chapter 5 — Non-Infectious Diseases...')
    add_chapter5(doc)

    print('  Adding Chapter 6 — Non-Infectious Pathology...')
    add_chapter6(doc)

    print('  Adding Chapter 7 — Postmortem Examination...')
    add_chapter7(doc)

    out = os.path.join(DIR, 'Workshop_Proceedings_2026.docx')
    doc.save(out)
    size_kb = os.path.getsize(out) // 1024
    print(f'\n  ✓  Workshop_Proceedings_2026.docx  ({size_kb} KB)')

    # Quick verification
    check = Document(out)
    print(f'  ✓  Verified: {len(check.paragraphs)} paragraphs, {len(check.tables)} tables')


if __name__ == '__main__':
    print('Building complete proceedings DOCX (single document)...\n')
    build()

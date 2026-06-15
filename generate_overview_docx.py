#!/usr/bin/env python3
"""
Generate Workshop Overview as a standalone Word (.docx) file.
Workshop on Essentials for Mortality Investigation of Asian Elephant
Chhattisgarh Forest Department | 5–6 June 2026, Raigarh
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT_DIR = '/home/user/Workshop-on-Conference'

DARK   = RGBColor(0x1B, 0x43, 0x32)
MED    = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT  = RGBColor(0x52, 0xB7, 0x88)
TINT   = RGBColor(0xD8, 0xF3, 0xDC)
TINT2  = RGBColor(0xEA, 0xF7, 0xEE)
RED    = RGBColor(0xC0, 0x39, 0x2B)
REDL   = RGBColor(0xFA, 0xDB, 0xD8)
ORANGE = RGBColor(0xF4, 0xA2, 0x61)
GOLD   = RGBColor(0xC9, 0xA8, 0x4C)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
MUTED  = RGBColor(0x55, 0x55, 0x55)
NAVY   = RGBColor(0x1A, 0x2E, 0x4A)


def rgb_hex(rgb):
    return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'


def new_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width   = Cm(21)
    sec.page_height  = Cm(29.7)
    sec.left_margin  = sec.right_margin  = Cm(2.0)
    sec.top_margin   = sec.bottom_margin = Cm(1.8)
    doc.core_properties.title  = 'Workshop Overview — Mortality Investigation of Asian Elephant'
    doc.core_properties.author = 'Chhattisgarh Forest Department'
    _define_styles(doc)
    return doc


def _define_styles(doc):
    styles = doc.styles

    def _style(name, base_name, size, bold=False, italic=False,
               color=None, space_b=0, space_a=6, align=None):
        try:
            s = styles[name]
        except KeyError:
            s = styles.add_style(name, 1)
        s.base_style = styles[base_name] if base_name in styles else None
        f = s.font
        f.name = 'Calibri'
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        if color:
            f.color.rgb = color
        pf = s.paragraph_format
        pf.space_before = Pt(space_b)
        pf.space_after  = Pt(space_a)
        if align:
            pf.alignment = align

    _style('OV_Title',  'Normal', 20, bold=True,   color=WHITE, space_a=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('OV_Sub',    'Normal', 10, italic=True,  color=TINT,  space_a=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('OV_H1',     'Normal', 11, bold=True,    color=WHITE, space_b=8, space_a=2)
    _style('OV_H2',     'Normal', 10, bold=True,    color=MED,   space_b=6, space_a=2)
    _style('OV_Body',   'Normal',  9.5, color=BLACK, space_a=4)
    _style('OV_Bullet', 'Normal',  9,  color=BLACK,  space_a=2)
    _style('OV_TH',     'Normal',  8.5, bold=True, color=WHITE,  space_a=0, space_b=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('OV_TD',     'Normal',  8.5, color=BLACK, space_a=0, space_b=0)
    _style('OV_TDC',    'Normal',  8.5, color=BLACK, space_a=0, space_b=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('OV_TDB',    'Normal',  8.5, bold=True, color=DARK,  space_a=0, space_b=0)
    _style('OV_Caption','Normal',  8,  italic=True, color=MUTED, space_a=4, align=WD_ALIGN_PARAGRAPH.CENTER)


def shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def add_banner(doc, title, subtitle='', org=''):
    """Full-width dark green banner for document header."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]
    p.style = doc.styles['OV_Title']

    # Workshop label
    r0 = p.add_run('WORKSHOP OVERVIEW')
    r0.font.size = Pt(8)
    r0.font.color.rgb = LIGHT
    r0.font.bold = True
    p.add_run('\n')

    # Main title
    r1 = p.add_run(title)
    r1.font.size = Pt(18)
    r1.font.bold = True
    r1.font.color.rgb = WHITE

    if subtitle:
        p.add_run('\n')
        r2 = p.add_run(subtitle)
        r2.font.size = Pt(10)
        r2.font.italic = True
        r2.font.color.rgb = TINT

    if org:
        p.add_run('\n\n')
        r3 = p.add_run(org)
        r3.font.size = Pt(8.5)
        r3.font.color.rgb = TINT

    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(8)
    doc.add_paragraph()


def add_h1(doc, text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(MED))
    p = cell.paragraphs[0]
    p.style = doc.styles['OV_H1']
    run = p.add_run(text)
    run.font.color.rgb = WHITE
    run.font.bold = True
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    doc.add_paragraph()


def add_h2(doc, text):
    p = doc.add_paragraph(style='OV_H2')
    p.paragraph_format.left_indent = Cm(0.3)
    run = p.add_run(text)
    run.font.color.rgb = MED
    run.font.bold = True


def add_body(doc, text, bold=False, italic=False, align=None):
    p = doc.add_paragraph(style='OV_Body')
    run = p.add_run(text)
    run.font.bold = bold
    run.font.italic = italic
    if align:
        p.paragraph_format.alignment = align
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style='OV_Bullet')
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.4)
    p.paragraph_format.first_line_indent = Cm(-0.3)
    p.add_run(f'• {text}')


def add_keybox(doc, text, danger=False, gold=False):
    bg = rgb_hex(REDL) if danger else ('FFF8E1' if gold else rgb_hex(TINT))
    border_col = RED if danger else (GOLD if gold else LIGHT)
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, bg)
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = RED if danger else (GOLD if gold else DARK)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    doc.add_paragraph()


def add_table(doc, headers, rows, col_widths=None):
    n = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n)
    tbl.style = 'Table Grid'

    hcells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        shade_cell(hcells[i], rgb_hex(MED))
        p = hcells[i].paragraphs[0]
        p.style = doc.styles['OV_TH']
        run = p.add_run(str(h))
        run.font.color.rgb = WHITE
        run.font.bold = True
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after  = Pt(3)

    for ri, row in enumerate(rows):
        cells = tbl.rows[ri + 1].cells
        bg = rgb_hex(TINT2) if ri % 2 == 1 else 'FFFFFF'
        for ci, val in enumerate(row):
            shade_cell(cells[ci], bg)
            p = cells[ci].paragraphs[0]
            p.style = doc.styles['OV_TD']
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after  = Pt(2)
            if isinstance(val, tuple):
                text, bold_flag = val
                run = p.add_run(str(text))
                run.font.bold = bold_flag
            else:
                p.add_run(str(val))

    if col_widths:
        for r2 in tbl.rows:
            for ci2, cell in enumerate(r2.cells):
                if ci2 < len(col_widths):
                    cell.width = Cm(col_widths[ci2])

    doc.add_paragraph()


def add_speaker_card(doc, name, designation, institution, topics):
    """Speaker profile card."""
    tbl = doc.add_table(rows=1, cols=2)
    tbl.style = 'Table Grid'
    # Name cell
    name_cell = tbl.rows[0].cells[0]
    shade_cell(name_cell, rgb_hex(NAVY))
    p = name_cell.paragraphs[0]
    r1 = p.add_run(name)
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = WHITE
    p.add_run('\n')
    r2 = p.add_run(designation)
    r2.font.size = Pt(8)
    r2.font.italic = True
    r2.font.color.rgb = TINT
    p.add_run('\n')
    r3 = p.add_run(institution)
    r3.font.size = Pt(8)
    r3.font.color.rgb = LIGHT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    name_cell.width = Cm(6)

    # Topics cell
    topic_cell = tbl.rows[0].cells[1]
    shade_cell(topic_cell, rgb_hex(TINT2))
    pt = topic_cell.paragraphs[0]
    rt = pt.add_run('Topics: ')
    rt.font.size = Pt(8.5)
    rt.font.bold = True
    rt.font.color.rgb = DARK
    rt2 = pt.add_run(topics)
    rt2.font.size = Pt(8.5)
    rt2.font.color.rgb = BLACK
    pt.paragraph_format.space_before = Pt(4)
    pt.paragraph_format.space_after  = Pt(4)

    doc.add_paragraph()


# ═══════════════════════════════════════════════════════════════════════════════
# Build Overview Document
# ═══════════════════════════════════════════════════════════════════════════════

def build_overview():
    doc = new_doc()

    add_banner(doc,
        'Workshop on Essentials for Mortality Investigation of Asian Elephant',
        'Raigarh, Chhattisgarh  |  5–6 June 2026',
        'Organised by: Chhattisgarh Forest Department\n'
        'Technical Support: Wildlife Institute of India (WII), Dehradun\n'
        'Laboratory Partners: ICAR-IVRI, Bareilly  ·  NDVSU, Jabalpur')

    add_h1(doc, '1. Workshop at a Glance')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Title', 'Workshop on Essentials for Mortality Investigation of Asian Elephant'],
         ['Dates', '5–6 June 2026 (Two days)'],
         ['Venue', 'Raigarh, Chhattisgarh'],
         ['Organised by', 'Chhattisgarh Forest Department'],
         ['Technical Support', 'Wildlife Institute of India (WII), Dehradun'],
         ['Laboratory Partners', 'ICAR-IVRI, Bareilly  ·  NDVSU, Jabalpur'],
         ['Total Participants', '84 Forest Officers and Wildlife Veterinarians'],
         ['Target Audience', 'Divisional Forest Officers, Range Forest Officers, Wildlife Veterinarians, Field Staff'],
         ['Language', 'Hindi and English'],
         ['Context', 'CG elephant population has grown to ~451 (2026); 49 deaths recorded 2021–2026 — capacity building urgently needed']],
        col_widths=[4.5, 12.5])

    add_h1(doc, '2. Background & Rationale')
    add_body(doc,
        'Chhattisgarh has emerged as a significant elephant range state over the past two '
        'decades, with the population growing from 24 individuals (2001) to an estimated '
        '451 elephants (2026). This rapid expansion has been accompanied by increasing '
        'human-elephant conflict and a rising trend in elephant mortality.')
    add_body(doc,
        'Between 2021 and 2026, a total of 49 elephant deaths were recorded across '
        'Dharamjaigarh (DH) and Raigarh (RG) Forest Divisions. Alarmingly, the year '
        '2025-26 recorded 12 deaths — the highest in a single year. The dominant causes '
        '— electrocution (47%) and drowning (27%) — are largely preventable with targeted '
        'interventions. However, field officers currently lack standardised training in '
        'systematic necropsy, evidence collection, and forensic documentation.')
    add_body(doc,
        'This workshop directly addresses that gap. It is the first dedicated training '
        'programme on elephant mortality investigation organised by the Chhattisgarh '
        'Forest Department, and brings together national experts in wildlife pathology, '
        'disease surveillance, and forensic veterinary science.')
    add_keybox(doc,
        'This workshop is a response to 49 elephant deaths in 5 years — '
        '74% of which were preventable. Building field capacity for systematic investigation '
        'is the first step toward evidence-based prevention.')

    add_h1(doc, '3. Workshop Objectives')
    add_table(doc,
        ['Theme', 'Learning Objectives'],
        [['Biology & Ecology',
          'Understand the biology, anatomy, behaviour, and ecology of Asian elephants; '
          'appreciate population dynamics specific to Chhattisgarh'],
         ['Necropsy & Pathology',
          'Perform systematic postmortem examination; identify gross pathological findings; '
          'distinguish infectious from non-infectious causes of death'],
         ['Biosafety',
          'Follow PPE protocols; understand zoonotic risks at necropsy; '
          'manage biohazardous materials safely'],
         ['Sample Collection',
          'Collect, preserve, and transport biological samples correctly; '
          'maintain chain of custody for forensic/legal purposes'],
         ['Disease Diagnosis',
          'Identify key infectious (EEHV, TB, anthrax) and non-infectious (electrocution, '
          'drowning, CPA toxicosis) causes of elephant mortality'],
         ['Surveillance & Response',
          'Implement elephant surveillance systems; establish protocols for carcass disposal '
          'and site remediation; complete PM reports for official records']],
        col_widths=[4, 13])

    add_h1(doc, '4. Resource Persons')
    add_body(doc, 'Five national experts served as resource persons for the two-day programme:')
    doc.add_paragraph()

    add_speaker_card(doc,
        'Prof. Dr. A. B. Shrivastav',
        'Professor & Head, Department of Wildlife Health Management',
        'NDVSU (Nanaji Deshmukh Veterinary Science University), Jabalpur (MP)',
        'Postmortem Examination of Asian Elephants; Non-Infectious Pathology; '
        'Toxicology; HCN Poisoning Case Studies')

    add_speaker_card(doc,
        'Dr. Parag Nigam',
        'Senior Scientist, Wildlife Institute of India',
        'WII, Dehradun (Uttarakhand)',
        'Elephant Ecology & Population Biology; '
        'CG Elephant Population Status & Mortality Data')

    add_speaker_card(doc,
        'Dr. Karikalan Mathesh',
        'Principal Scientist, Animal Science Division',
        'ICAR-IVRI (Indian Veterinary Research Institute), Bareilly (UP)',
        'Biological Sample Collection Protocols; Non-Infectious Diseases; '
        'Bandhavgarh Mass Mortality Case Study (CPA Toxicosis)')

    add_speaker_card(doc,
        'Dr. Tapendra Saini',
        'Scientist, Wildlife Health Programme',
        'WII, Dehradun (Uttarakhand)',
        'Infectious Diseases of Asian Elephants; EEHV Surveillance; '
        'Disease Monitoring Systems')

    add_speaker_card(doc,
        'Dr. Chandra Prakash Sharma',
        'Scientist, Conservation Biology Division',
        'WII, Dehradun (Uttarakhand)',
        'Field Investigation Framework; Carcass Disposal & Site Remediation; '
        'Conservation Biology of Asian Elephants')

    add_h1(doc, '5. Two-Day Programme Schedule')
    add_table(doc,
        ['Day', 'Time', 'Session / Topic', 'Resource Person'],
        # Day 1
        [['Day 1\n5 June 2026', 'Morning\n09:00–10:00',
          'Inauguration; Welcome address; Overview of CG elephant situation',
          'Chief Conservator of Forests (WL), CG + Forest Officers'],
         ['', '10:00–11:30',
          'CG Elephant Population & Mortality Statistics (2021–2026): trends, hotspots, key findings',
          'Dr. Parag Nigam (WII)'],
         ['', '11:30–13:00',
          'Biological & Anatomical Aspects of Asian Elephants',
          'Dr. Parag Nigam (WII)'],
         ['', 'Afternoon\n14:00–15:30',
          'Non-Infectious Diseases in Asian Elephants (Electrocution, Drowning, Toxicoses, Bandhavgarh case)',
          'Dr. Karikalan Mathesh (ICAR-IVRI)'],
         ['', '15:30–17:00',
          'Infectious Diseases & Surveillance (EEHV, TB, Anthrax, Rabies)',
          'Dr. Tapendra Saini (WII)'],
         ['', '17:00–18:00',
          'Practical Demonstration: PM Examination Techniques (model)',
          'Dr. A. B. Shrivastav (NDVSU)'],
         # Day 2
         ['Day 2\n6 June 2026', 'Morning\n09:00–10:30',
          'Biological Sample Collection: master protocol, preservation, packing, chain of custody',
          'Dr. Karikalan Mathesh (ICAR-IVRI)'],
         ['', '10:30–12:00',
          'Non-Infectious Pathology: poisoning, pyometra, hyperthermia, iron deficiency',
          'Dr. A. B. Shrivastav (NDVSU)'],
         ['', '12:00–13:00',
          'Postmortem Examination — Step-by-step workflow; Instruments; Documentation',
          'Dr. A. B. Shrivastav (NDVSU)'],
         ['', 'Afternoon\n14:00–15:30',
          'Field Investigation Case Studies: Gurda drowning, CPA Bandhavgarh, Panna rabies',
          'All resource persons'],
         ['', '15:30–16:30',
          'Carcass Disposal & Site Remediation; Environmental sampling protocol',
          'Dr. C. P. Sharma (WII)'],
         ['', '16:30–17:30',
          'Recommendations, Action Plan & Valediction',
          'CCF (WL) CG + All Resource Persons']],
        col_widths=[2.5, 2.5, 9.5, 4.5])

    add_h1(doc, '6. Partner Institutions')
    add_table(doc,
        ['Institution', 'Role', 'Key Contribution'],
        [['Chhattisgarh Forest Department',
          'Organiser & Host',
          'Funding, logistics, participant mobilisation, field data (mortality records 2021–2026)'],
         ['Wildlife Institute of India (WII), Dehradun',
          'Technical Support & Knowledge Partner',
          'Population ecology expertise, surveillance systems design, resource persons (3)'],
         ['ICAR-IVRI, Bareilly',
          'Laboratory Partner — Pathology & Diagnosis',
          'Diagnostic laboratory services: EEHV PCR, histopathology, toxicology, bacteriology, virology'],
         ['NDVSU, Jabalpur',
          'Laboratory Partner — Wildlife Pathology',
          'Wildlife postmortem protocols, non-infectious pathology, toxicology case expertise']],
        col_widths=[4, 3.5, 9.5])

    add_h1(doc, '7. Participants')
    add_body(doc,
        'A total of 84 participants attended the two-day workshop representing '
        'field staff from both Dharamjaigarh (DH) and Raigarh (RG) Forest Divisions.')
    add_table(doc,
        ['Category', 'Count', 'Division'],
        [['Divisional Forest Officers (DFOs)', '4', 'DH + RG'],
         ['Conservators of Forest', '2', 'DH + RG'],
         ['Range Forest Officers (RFOs)', '18', 'DH + RG'],
         ['Deputy Rangers / Forest Guards', '28', 'DH + RG'],
         ['Wildlife Veterinarians', '6', 'State + Divisions'],
         ['Wildlife Veterinary Assistants', '12', 'DH + RG'],
         ['Lab Technicians / Support Staff', '8', 'ICAR-IVRI + NDVSU'],
         ['WII Researchers', '6', 'WII Dehradun'],
         [('TOTAL', True), ('84', True), '—']],
        col_widths=[6, 3, 8])

    add_h1(doc, '8. Expected Outcomes')
    outcomes = [
        'All participating forest officers trained in the standard elephant necropsy protocol',
        'Standardised PM reporting format adopted across both DH and RG Forest Divisions',
        'Chain of custody procedures for biological samples established and practiced',
        'Field officers able to distinguish electrocution vs. drowning vs. disease vs. toxicosis',
        'Network established between CG Forest Dept, WII, ICAR-IVRI and NDVSU for future case referrals',
        'Awareness of EEHV surveillance protocols — annual screening to begin from FY 2026-27',
        'Action plan for drowning prevention infrastructure and power-line audit agreed and documented',
        'Environmental water sampling protocol for suspected toxic water bodies initiated',
    ]
    for o in outcomes:
        add_bullet(doc, o)
    doc.add_paragraph()

    add_keybox(doc,
        '"The carcass never tells a lie — but you must know how to ask the right questions."\n'
        '— Dr. R. K. Satpati, Wildlife Institute of India\n\n'
        '"Doctors who perform necropsies gain wisdom that no textbook can teach."\n'
        '— Dr. A. B. Shrivastav, NDVSU Jabalpur', gold=True)

    # Save
    path = os.path.join(OUT_DIR, 'Workshop_Overview_2026.docx')
    doc.save(path)
    size_kb = os.path.getsize(path) // 1024
    print(f'  ✓  Workshop_Overview_2026.docx  ({size_kb} KB)')


if __name__ == '__main__':
    build_overview()

#!/usr/bin/env python3
"""
Generate all 7 Workshop chapters as Word (.docx) files.
Workshop on Essentials for Mortality Investigation of Asian Elephant
Chhattisgarh Forest Department | 5–6 June 2026, Raigarh
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT_DIR = '/home/user/Workshop-on-Conference'

# ── Colours ───────────────────────────────────────────────────────────────────
DARK   = RGBColor(0x1B, 0x43, 0x32)   # deep forest green
MED    = RGBColor(0x2D, 0x6A, 0x4F)   # mid green
LIGHT  = RGBColor(0x52, 0xB7, 0x88)   # bright green
TINT   = RGBColor(0xD8, 0xF3, 0xDC)   # light green tint
TINT2  = RGBColor(0xEA, 0xF7, 0xEE)   # very light green
RED    = RGBColor(0xC0, 0x39, 0x2B)   # danger red
REDL   = RGBColor(0xFA, 0xDB, 0xD8)   # light red
ORANGE = RGBColor(0xF4, 0xA2, 0x61)   # orange
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
MUTED  = RGBColor(0x55, 0x55, 0x55)

def rgb_hex(rgb: RGBColor) -> str:
    return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'


# ═══════════════════════════════════════════════════════════════════════════════
# Document helpers
# ═══════════════════════════════════════════════════════════════════════════════

def new_doc(title: str, author: str = 'Chhattisgarh Forest Department') -> Document:
    doc = Document()
    sec = doc.sections[0]
    sec.page_width   = Cm(21)
    sec.page_height  = Cm(29.7)
    sec.left_margin  = sec.right_margin  = Cm(2.0)
    sec.top_margin   = sec.bottom_margin = Cm(1.8)
    doc.core_properties.title  = title
    doc.core_properties.author = author
    _define_styles(doc)
    return doc


def _define_styles(doc: Document):
    styles = doc.styles

    def _style(name, base_name, size, bold=False, color=None, space_b=0, space_a=6, align=None, italic=False):
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
        return s

    _style('WS_Title',   'Normal', 18, bold=True, color=WHITE,  space_a=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('WS_Sub',     'Normal', 10, italic=True, color=TINT,  space_a=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('WS_H1',      'Normal', 11, bold=True, color=WHITE,  space_b=8, space_a=2)
    _style('WS_H2',      'Normal', 10, bold=True, color=DARK,   space_b=6, space_a=2)
    _style('WS_Body',    'Normal',  9.5, color=BLACK, space_a=4)
    _style('WS_Bold',    'Normal',  9.5, bold=True, color=BLACK, space_a=4)
    _style('WS_Bullet',  'Normal',  9,  color=BLACK, space_a=2)
    _style('WS_Caption', 'Normal',  8,  italic=True, color=MUTED, space_a=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('WS_TH',      'Normal',  8.5, bold=True, color=WHITE,  space_a=0, space_b=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('WS_TD',      'Normal',  8.5, color=BLACK, space_a=0, space_b=0)
    _style('WS_TDC',     'Normal',  8.5, color=BLACK, space_a=0, space_b=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    _style('WS_TDB',     'Normal',  8.5, bold=True, color=DARK,  space_a=0, space_b=0)
    _style('WS_Note',    'Normal',  8.5, italic=True, color=RED, space_a=3)


def shade_cell(cell, hex_color: str):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def cell_border(cell, sides='all', color='CCCCCC', sz='4'):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in (['top', 'left', 'bottom', 'right'] if sides == 'all' else sides):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), color)
        tcBorders.append(el)
    tcPr.append(tcBorders)


def add_chapter_header(doc: Document, num: str, title: str, subtitle: str = '', author: str = ''):
    """Dark green banner as a table row."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]
    p.style = doc.styles['WS_Title']
    run = p.add_run(f'CHAPTER {num}')
    run.font.size = Pt(8)
    run.font.color.rgb = LIGHT
    p.add_run('\n')
    r2 = p.add_run(title)
    r2.font.size = Pt(16)
    r2.font.bold = True
    r2.font.color.rgb = WHITE
    if subtitle:
        p.add_run('\n')
        r3 = p.add_run(subtitle)
        r3.font.size = Pt(9.5)
        r3.font.italic = True
        r3.font.color.rgb = TINT
    if author:
        p.add_run('\n\n')
        r4 = p.add_run(author)
        r4.font.size = Pt(8.5)
        r4.font.color.rgb = TINT
    cell.paragraphs[0].paragraph_format.space_before = Pt(6)
    cell.paragraphs[0].paragraph_format.space_after  = Pt(6)
    doc.add_paragraph()


def add_h1(doc: Document, text: str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(MED))
    p = cell.paragraphs[0]
    p.style = doc.styles['WS_H1']
    run = p.add_run(text)
    run.font.color.rgb = WHITE
    run.font.bold = True
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    doc.add_paragraph()


def add_h2(doc: Document, text: str):
    p = doc.add_paragraph(style='WS_H2')
    p.paragraph_format.left_indent = Cm(0.3)
    run = p.add_run(text)
    run.font.color.rgb = MED
    run.font.bold = True


def add_body(doc: Document, text: str, bold=False, italic=False, color=None):
    p = doc.add_paragraph(style='WS_Bold' if bold else 'WS_Body')
    run = p.add_run(text)
    if italic:
        run.font.italic = True
    if color:
        run.font.color.rgb = color
    return p


def add_bullet(doc: Document, text: str, level=0):
    p = doc.add_paragraph(style='WS_Bullet')
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.4)
    p.paragraph_format.first_line_indent = Cm(-0.3)
    p.add_run(f'• {text}')
    return p


def add_keybox(doc: Document, text: str, danger=False):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, rgb_hex(REDL) if danger else rgb_hex(TINT))
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = RED if danger else DARK
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    doc.add_paragraph()


def add_table(doc: Document, headers: list, rows: list,
              col_widths: list = None, alt_row=True) -> None:
    n_cols = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n_cols)
    tbl.style = 'Table Grid'

    # Header row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        shade_cell(hdr_cells[i], rgb_hex(MED))
        p = hdr_cells[i].paragraphs[0]
        p.style = doc.styles['WS_TH']
        run = p.add_run(str(h))
        run.font.color.rgb = WHITE
        run.font.bold = True
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after  = Pt(3)

    # Data rows
    for ri, row in enumerate(rows):
        cells = tbl.rows[ri + 1].cells
        bg = rgb_hex(TINT2) if (alt_row and ri % 2 == 1) else 'FFFFFF'
        for ci, cell_text in enumerate(row):
            shade_cell(cells[ci], bg)
            p = cells[ci].paragraphs[0]
            p.style = doc.styles['WS_TD']
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after  = Pt(2)
            if isinstance(cell_text, tuple):
                text, bold_flag = cell_text
                run = p.add_run(str(text))
                run.font.bold = bold_flag
            else:
                p.add_run(str(cell_text))

    # Column widths
    if col_widths:
        for ri2, row in enumerate(tbl.rows):
            for ci2, cell in enumerate(row.cells):
                if ci2 < len(col_widths):
                    cell.width = Cm(col_widths[ci2])

    doc.add_paragraph()


def sp(doc: Document):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)


def save(doc: Document, filename: str):
    path = os.path.join(OUT_DIR, filename)
    doc.save(path)
    size_kb = os.path.getsize(path) // 1024
    print(f'  ✓  {filename}  ({size_kb} KB)')
    return path


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — Workshop Overview & Elephant Mortality Analysis
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter1():
    doc = new_doc('Chapter 1 — Workshop Overview & Elephant Mortality Analysis')
    add_chapter_header(doc, '1',
        'Workshop Overview & Elephant Mortality Analysis',
        'Chhattisgarh 2021–2026: Trends, Causes & Recommendations',
        'Chhattisgarh Forest Department  |  Technical Support: WII Dehradun')

    add_h1(doc, '1. Workshop Background & Objectives')
    add_body(doc,
        'The Workshop on Essentials for Mortality Investigation of Asian Elephant was organised '
        'by the Chhattisgarh Forest Department with technical support from the Wildlife Institute '
        'of India (WII), Dehradun, and laboratory partners ICAR-IVRI, Bareilly and NDVSU, '
        'Jabalpur. The two-day programme (5–6 June 2026, Raigarh) brought together 84 field '
        'officers and wildlife veterinarians to build capacity in systematic elephant necropsy, '
        'sample collection, disease diagnosis, and evidence-based mortality investigations.')

    add_table(doc,
        ['Statistic', 'Value'],
        [['Participants', '84'],
         ['Duration', '2 days (5–6 June 2026)'],
         ['Venue', 'Raigarh, Chhattisgarh'],
         ['Resource Persons', '5 expert faculty'],
         ['Partner Institutions', '3 (CG Forest Dept, WII, ICAR-IVRI/NDVSU)']],
        col_widths=[6, 10])

    add_h2(doc, 'Workshop Objectives')
    add_table(doc,
        ['Theme', 'Topics Covered'],
        [['Biology & Ecology', 'Biology, behaviour, ecology of Asian elephants; population dynamics in CG'],
         ['Pathology & Disease', 'Necropsy procedures, biosafety, sample collection, infectious & non-infectious diseases'],
         ['Surveillance & Response', 'Elephant surveillance systems, disposal protocols, site remediation, evidence documentation']],
        col_widths=[5, 12])

    add_h2(doc, 'Resource Persons')
    add_table(doc,
        ['Name', 'Institution', 'Expertise'],
        [['Dr. A. B. Shrivastav', 'NDVSU, Jabalpur', 'Wildlife Pathology, Elephant PM Examination'],
         ['Dr. Parag Nigam', 'WII, Dehradun', 'Elephant Ecology & Population Biology'],
         ['Dr. Karikalan Mathesh', 'ICAR-IVRI, Bareilly', 'Veterinary Pathology, Sample Diagnostics'],
         ['Dr. Tapendra Saini', 'WII, Dehradun', 'Wildlife Surveillance & Disease Monitoring'],
         ['Dr. Chandra Prakash Sharma', 'WII, Dehradun', 'Conservation Biology & Field Investigation']],
        col_widths=[5, 5, 7])

    add_h1(doc, '2. Elephant Population Status in Chhattisgarh')
    add_body(doc,
        'Chhattisgarh has witnessed remarkable elephant population growth over two decades. '
        'From just 24 individuals in 2001 (transient from Odisha/Jharkhand), the population '
        'has grown to an estimated 451 in 2026 — a CAGR of approximately 13%. Resident breeding '
        'populations are established across Dharamjaigarh (DH) and Raigarh (RG) Divisions.')
    add_table(doc,
        ['Year', 'Population Count', 'Remarks'],
        [['2001', '24', 'First recorded transient elephants from Odisha'],
         ['2005', '123', 'Rapid establishment of resident herds'],
         ['2007', '122', 'Stable — consolidation phase'],
         ['2015', '247', 'Continued range expansion into new areas'],
         ['2017', '247', 'Stable; human-elephant conflict rising'],
         ['2021', '279', 'Post-COVID survey — increased mortality recorded'],
         ['2026', '~451 (est.)', 'Highest ever; detailed census ongoing | CAGR ≈ 13%']],
        col_widths=[2.5, 4, 10.5])

    add_h1(doc, '3. Elephant Casualty Analysis (2021–2026)')
    add_keybox(doc,
        'TOTAL: 49 Elephant Deaths | DH Division: 27 | RG Division: 22 | '
        '2025-26: 12 deaths (RECORD HIGH) — Immediate intervention required', danger=True)
    add_table(doc,
        ['Year', 'DH Division', 'RG Division', 'Total', 'Remarks'],
        [['2021-22', '2', '2', '4', 'Baseline year — low mortality'],
         ['2022-23', '7', '5', '12', 'Surge in deaths — monsoon related'],
         ['2023-24', '3', '3', '6', 'Relatively low year'],
         ['2024-25', '6', '4', '10', 'Rising trend resumes'],
         ['2025-26', '7', '5', ('12 — RECORD', True), 'Record high — electrocution predominant'],
         ['2026-27*', '2', '3', '5*', 'Ongoing year (as of June 2026)'],
         [('TOTAL', True), ('27', True), ('22', True), ('49', True), 'Cumulative 2021-2026']],
        col_widths=[2.5, 2.5, 2.5, 2.2, 7.3])
    add_body(doc, 'Human deaths in Human-Elephant Conflict: 45 total (DH: 36 | RG: 9) during 2021–2026.', bold=True)

    add_h1(doc, '4. Cause of Death Analysis')
    add_table(doc,
        ['Cause of Death', 'Count', 'Percentage', 'Key Mechanism'],
        [['Electrocution', '23', '47%', 'Stray power lines, illegal electric fencing around crops'],
         ['Drowning', '13', '27%', 'Calves unable to exit water bodies; steep banks, dams'],
         ['Natural / Old Age', '4', '8%', 'Multi-molar loss, senility — natural attrition'],
         ['Fall / Trauma', '4', '8%', 'Steep terrain, mine shafts, road/rail conflict'],
         ['Other / Undetermined', '5', '10%', 'Toxicology pending, disease, inter-elephant conflict']],
        col_widths=[4, 2, 3, 8])
    add_keybox(doc, 'Electrocution + Drowning = 74% of all deaths — both are PREVENTABLE', danger=True)

    add_h1(doc, '5. Demographic Analysis of Casualties')
    add_table(doc,
        ['Age Category', 'Count', '%', 'Key Vulnerability'],
        [['Calf (0–2 yr)', '23', '50%', 'Drowning (calves cannot exit steep banks), electrocution'],
         ['Juvenile (2–5 yr)', '5', '11%', 'Separation from herd, foraging near crop fields'],
         ['Sub-adult (5–15 yr)', '2', '4%', 'Dispersing males — increased exposure to power lines'],
         ['Adult (15–40 yr)', '11', '24%', 'Electrocution in bulls; old cow mortality'],
         ['Old (>40 yr)', '5', '11%', 'Natural senility, molar exhaustion, starvation']],
        col_widths=[3.5, 2, 2, 9.5])
    add_table(doc,
        ['Sex', 'Count', '%', 'Notable Pattern'],
        [['Male', '23', '51%', '48% of male deaths caused by electrocution'],
         ['Female', '22', '49%', '33% of female deaths caused by electrocution']],
        col_widths=[3, 2, 2, 10])
    add_keybox(doc, 'CRITICAL: Calves (0-2 yr) = 50% of all deaths and 92% of drowning deaths. '
                    'Drowning prevention infrastructure is the highest-impact single intervention.')

    add_h1(doc, '6. Seasonal Variation in Mortality')
    add_table(doc,
        ['Season', 'Months', 'Drowning', 'Electrocution', 'Key Driver'],
        [['Dry Season', 'Jan–May', '8', '6', 'Low water levels — calves trapped in drying pools'],
         ['Monsoon', 'Jun–Sep', '1', '5', 'Flooded rivers, reduced visibility of power lines'],
         [('Harvest Season (PEAK)', True), 'Oct–Dec', ('4', True), ('10', True),
          ('PEAK: Illegal electric fencing to protect paddy/maize crops', True)],
         [('TOTAL', True), '—', ('13', True), ('21*', True), '*excludes 2 unconfirmed electrocution deaths']],
        col_widths=[4, 2.5, 2.5, 3, 5])
    add_body(doc, 'October is the single deadliest month (8 deaths). Oct–Dec harvest season = 42% of annual deaths.', italic=True)

    add_h1(doc, '7. Range-wise Distribution of Deaths')
    add_table(doc,
        ['Forest Range', 'Division', 'Electrocution', 'Drowning', 'Other', 'Total', 'Status'],
        [[('Ghargoda', True), 'RG', '8', '5', '2', ('15', True), ('CRITICAL', True)],
         [('Chhal', True), 'DH', '7', '5', '2', ('14', True), ('CRITICAL', True)],
         ['Dharamjaigarh', 'DH', '3', '2', '1', '6', 'HIGH'],
         ['Kharsia', 'RG', '2', '1', '1', '4', 'MODERATE'],
         ['Tamnar', 'RG', '2', '1', '1', '4', 'MODERATE'],
         ['Other Ranges', '—', '1', '—', '5', '6', 'Monitor'],
         [('TOTAL', True), '—', ('23', True), ('13', True), ('13', True), ('49', True), '—']],
        col_widths=[3.5, 2, 2.5, 2.5, 2, 2, 2.5])
    add_body(doc, 'Human conflict hotspots: Chhal (10 deaths) > Borojh (9) > Lailungaan (8)', bold=True)

    add_h1(doc, '8. Suspected Drowning — Post-Mortem Analysis')
    add_keybox(doc,
        'KEY FINDING: 13 drowning deaths (27%). 92% were calves. '
        'ARSENIC DETECTED in 2 specimens — Tamnar Range, Dec 2025 (File F.2-19/DI/NRC/2025-26/CWL)', danger=True)
    add_table(doc,
        ['PM Finding', 'Result in All Cases', 'Significance'],
        [['Frothy discharge', 'Present — ALL 13 cases', 'Hallmark of antemortem drowning'],
         ['Waterlogged lungs', 'Present — ALL 13 cases', 'Lung weight 3–5× normal'],
         ['Water in trachea', 'Present — ALL 13 cases', 'Rules out post-mortem artefact'],
         ['GI water content', 'Large volume — ALL cases', 'Swallowed water while struggling'],
         [('Diatom test', True), ('POSITIVE — all tested', True), 'Bone marrow dissemination = confirmed antemortem drowning'],
         [('Arsenic', True), ('DETECTED in 2 specimens', True), 'Tamnar Range, Dec 2025 — environmental investigation initiated'],
         ['EEHV', 'NEGATIVE all cases', 'Viral haemorrhagic disease ruled out'],
         ['Nitrate-Nitrite', 'NEGATIVE all cases', 'Fertiliser contamination ruled out'],
         ['Heavy metals (Pb/Hg/Cd)', 'NEGATIVE all cases', 'Industrial metals not implicated'],
         ['Organochlorine/phosphate', 'NEGATIVE all cases', 'Pesticide poisoning excluded'],
         ['HCN (Cyanide)', 'NEGATIVE all cases', 'Plant/industrial cyanide excluded']],
        col_widths=[4.5, 4, 8.5])

    add_h1(doc, '9. Case Study — Gurda Calf Drowning (01 June 2026)')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Date', '01 June 2026'],
         ['Location', 'Gurda River sandbank, Kharsia Range, Raigarh Van Mandal'],
         ['GPS', '22.0439°N, 83.1313°E'],
         ['Victim', 'Male calf, estimated age 12–18 months'],
         ['Discovery', 'Calf found separated from herd on exposed sandbank after overnight flooding'],
         ['PM Findings', 'Waterlogged lungs, frothy tracheal discharge, water in stomach (large volume), no external trauma'],
         ['Diatom Test', 'POSITIVE — Naviculaceae spp. in lung and bone marrow'],
         [('Cause of Death', True), ('Confirmed drowning (asphyxia due to water inhalation)', True)],
         ['Follow-up', 'Water sample collected for arsenic analysis; site flagged for earthen ramp installation']],
        col_widths=[4.5, 12.5])

    add_h1(doc, '10. Two-Day Workshop Programme')
    add_table(doc,
        ['Day / Session', 'Topics', 'Resource Person'],
        [['Day 1 — Morning', 'Inauguration & Overview | CG Population & Mortality Statistics | Biological & Anatomical Aspects',
          'Forest Officers, CG; Dr. Parag Nigam (WII)'],
         ['Day 1 — Afternoon', 'Non-Infectious Diseases | Infectious Diseases & Surveillance | Practical: PM Techniques',
          'Dr. Karikalan Mathesh (ICAR-IVRI); Dr. Tapendra Saini (WII)'],
         ['Day 2 — Morning', 'Sample Collection & Chain of Custody | Non-Infectious Pathology | Drowning & Electrocution',
          'Dr. A. B. Shrivastav (NDVSU); Dr. C. P. Sharma (WII)'],
         ['Day 2 — Afternoon', 'Case Studies | Carcass Disposal & Site Remediation | Recommendations & Valediction',
          'All resource persons; CG Forest Dept Officers']],
        col_widths=[4, 9, 4])

    add_h1(doc, '11. Key Recommendations & Priority Action Plan')
    add_table(doc,
        ['#', 'Priority Action', 'Timeline', 'Agency'],
        [['1', 'Environmental Water Sampling: Rabo & Panikshet dams + Tamnar Range water bodies for arsenic/heavy metals', 'Immediate', 'CG Forest Dept + ICAR-IVRI'],
         ['2', 'Drowning Prevention Infrastructure: Earthen ramps at all drowning hotspots (Ghargoda & Chhal priority)', '1–3 months', 'CG Forest Dept + PWD'],
         ['3', 'Power-Line Audit: Complete audit of illegal electric fencing and stray HV lines in all elephant corridors', '1–6 months', 'CG Forest Dept + CSPDCL'],
         ['4', 'Oct–Dec Enforcement: Anti-fencing squads with weekly intelligence during harvest season', 'Seasonal', 'Forest Dept + Police'],
         ['5', 'Jan–May Calf Monitoring: Intensive calf surveillance in dry season when drowning risk is highest', 'Seasonal', 'WII + CG Forest Dept'],
         ['6', 'Mandatory PM within 24 hrs: SOP mandating complete PM + sample collection within 24 hrs of death, with digital reporting', 'Policy — immediate', 'PCCF (WL), CG'],
         ['7', 'Annual EEHV Surveillance: Annual PCR + serological surveillance across all herds in DH and RG Divisions', 'Annual', 'ICAR-IVRI + WII'],
         ['8', 'Quarterly Review Meetings: Inter-departmental review of mortality data with Forest, Police, Revenue, Power Depts', 'Quarterly', 'PCCF (WL), CG — All Depts']],
        col_widths=[0.8, 9.5, 2.7, 4])

    add_h1(doc, 'Summary Statistics at a Glance')
    add_table(doc,
        ['Metric', 'Value', 'Metric', 'Value'],
        [['Study Period', '2021–2026 (5 years)', 'Total Elephant Deaths', '49'],
         ['DH Division Deaths', '27 (55%)', 'RG Division Deaths', '22 (45%)'],
         ['Electrocution Deaths', '23 (47%)', 'Drowning Deaths', '13 (27%)'],
         ['Calf Deaths (0-2 yr)', '23 of 46 (50%)', 'Male Deaths', '23 of 45 (51%)'],
         ['Peak Death Month', 'October (8 deaths)', 'Peak Year', '2022-23 & 2025-26 (12 each)'],
         ['Drowning: Calves', '12/13 = 92%', 'Arsenic Positives', '2 specimens (Tamnar, Dec 2025)'],
         ['Human Deaths (HEC)', '45 (DH: 36 | RG: 9)', 'Pop. Growth 2001-26', '24 → 451 (CAGR ≈ 13%)']],
        col_widths=[4.5, 4, 4.5, 4])

    save(doc, 'Workshop_Chapter1_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — Biological & Anatomical Aspects
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter2():
    doc = new_doc('Chapter 2 — Biological & Anatomical Aspects of the Asian Elephant')
    add_chapter_header(doc, '2',
        'Biological & Anatomical Aspects of the Asian Elephant',
        'Taxonomy, Morphology, Physiology, and Specialised Systems',
        'Compiled from WII Training Materials | Workshop 2026')

    add_h1(doc, '1. Taxonomy & Classification')
    add_table(doc,
        ['Taxonomic Rank', 'Classification'],
        [['Kingdom', 'Animalia'],
         ['Phylum', 'Chordata'],
         ['Class', 'Mammalia'],
         ['Order', 'Proboscidea'],
         ['Family', 'Elephantidae'],
         ['Genus', 'Elephas'],
         ['Species', 'Elephas maximus'],
         ['Sub-species (India)', 'Elephas maximus indicus (Indian Elephant)']],
        col_widths=[5, 12])

    add_h1(doc, '2. Physical Characteristics')
    add_table(doc,
        ['Parameter', 'Asian Elephant', 'African Elephant'],
        [['Body Length', '5.5–6.5 m', '6–7.5 m'],
         ['Shoulder Height', '2.5–3.0 m (male)', '3.2–4.0 m (male)'],
         ['Body Weight', '3,500–5,000 kg (male)', '4,000–7,000 kg (male)'],
         ['Ear Shape', 'Smaller, rounded — map of India', 'Larger, map of Africa'],
         ['Head Profile', 'Double dome (two bumps)', 'Single dome (one bump)'],
         ['Trunk Tip', 'One finger (prehensile)', 'Two lips/fingers'],
         ['Tusk Prevalence', 'Males mainly; some females (tushes)', 'Both sexes'],
         ['Skin Colour', 'Grey — depigmented patches on ears/trunk', 'Grey — less depigmentation'],
         ['Skin Texture', 'Wrinkled, sparse hair', 'Wrinkled, very sparse hair'],
         ['Toe Nails', '5 front, 4 hind (Asian)', '4 front, 3 hind (African)']],
        col_widths=[4, 5.5, 7.5])

    add_h1(doc, '3. The Trunk — Proboscis')
    add_body(doc,
        'The trunk (proboscis) is a fusion of the upper lip and nose — the elephant\'s '
        'most versatile organ. It contains over 150,000 muscle units with no bone.')
    add_table(doc,
        ['Trunk Function', 'Details'],
        [['Breathing & Smell', 'Primary olfactory organ; smell range up to 20 km'],
         ['Drinking', 'Holds 8–10 litres per inhalation; total consumption 150–200 L/day'],
         ['Feeding', 'Plucks grass, strips bark, breaks branches — up to 150 kg fodder/day'],
         ['Bathing & Dusting', 'Sprays water for thermoregulation; dust as UV/ectoparasite protection'],
         ['Communication', 'Trumpeting, rumbling, contact greeting between individuals'],
         ['Tool use', 'Throws objects, plugs waterholes, rubs against trees'],
         ['Tactile sense', 'Highly sensitive fingertip-like tip for fine manipulation'],
         ['Defence', 'Strikes, grapples, throws objects at perceived threats'],
         ['Seismic detection', 'Detects infrasound vibrations through trunk pressed to ground'],
         ['Social bonding', 'Trunk-in-mouth greeting is a sign of submission/trust']],
        col_widths=[4.5, 12.5])

    add_h1(doc, '4. Molar Teeth & Age Estimation')
    add_body(doc,
        'Elephants have polyphyodont dentition — they cycle through 6 sets of molars (M1–M6) '
        'in a progressive horizontal replacement unique among mammals. Only one molar '
        '(or parts of two) is functional at a time per jaw quadrant.')
    add_table(doc,
        ['Molar Set', 'Eruption Age', 'Laminae Count', 'Last Use Age'],
        [['M1 (dp2)', 'Birth – 2 yrs', '3–4', '~2 years'],
         ['M2 (dp3)', '2–5 years', '4', '~4 years'],
         ['M3 (dp4)', '4–10 years', '5–6', '~10 years'],
         ['M4 (M1)', '8–15 years', '7–8', '~22 years'],
         ['M5 (M2)', '15–30 years', '9–10', '~45 years'],
         ['M6 (M3)', '30+ years', '12–14', 'Final set — exhaustion leads to starvation/death']],
        col_widths=[2.5, 3, 3.5, 8])
    add_keybox(doc, 'Molar exhaustion is the primary cause of death from "old age" in elephants. '
                    'When M6 is fully worn, the elephant can no longer chew — death follows from starvation/malnutrition.')

    add_h1(doc, '5. Ear Morphology & Thermoregulation')
    add_table(doc,
        ['Feature', 'Details'],
        [['Ear area', 'Asian: ~0.5 m² per ear | African: ~1.0 m² per ear'],
         ['Blood vessel density', 'Dense network of superficial blood vessels on posterior surface'],
         ['Thermoregulation mechanism', 'Flapping ears increases convective heat loss; blood cools as it flows through ear'],
         ['Temperature difference', 'Ear surface is 2–4°C cooler than core body temperature'],
         ['Behaviour', 'Frequent ear flapping in heat; ears draped over body in cold'],
         ['Temporal gland', 'Located between eye and ear; swells during musth in males — secretes musth fluid']],
        col_widths=[5, 12])

    add_h1(doc, '6. Skin')
    add_table(doc,
        ['Feature', 'Details'],
        [['Thickness', '2.5 cm at thickest (back/sides); very thin behind ears and at joints'],
         ['Folds & wrinkles', 'Surface area ×10 compared to smooth skin — traps moisture, mud, and parasite-repelling dust'],
         ['Hair', 'Sparse — mainly around mouth, ear margins, and tail tip in adults; calves have more hair'],
         ['Pigmentation', 'Generally grey; depigmented pink patches common on trunk, ears, face — normal variation'],
         ['Subcutaneous fat', 'Minimal compared to body mass — poor insulator; elephant relies on ears for temperature regulation'],
         ['Skin diseases', 'Elephant pox (PCPV), dermatitis, scabies — assessed during PM external examination']],
        col_widths=[4, 13])

    add_h1(doc, '7. Digestive System')
    add_body(doc,
        'Elephants are hindgut fermenters — cellulose fermentation occurs in the large intestine '
        'and caecum, NOT in a rumen. This makes them less efficient (only 40–50% digestive '
        'efficiency) compared to ruminants, requiring enormous food intake.')
    add_table(doc,
        ['Segment', 'Capacity / Details'],
        [['Oral Cavity', '6 molars per quadrant (horizontal replacement); muscular tongue; no canines'],
         ['Oesophagus', 'Muscular; connects to simple stomach; relatively short'],
         ['Stomach', 'Simple monogastric; capacity ~100 L; no forestomach compartments'],
         ['Small Intestine', 'Length ~19 m; primary nutrient absorption site'],
         ['Caecum', 'Large; major fermentation site; capacity ~100 L'],
         ['Large Intestine', 'Length ~10 m; water reabsorption and fermentation'],
         ['Rectum', 'Terminal; dung boluses formed here — inspected at PM'],
         ['Daily Intake', '150–200 kg of fresh vegetation | 150–200 L water | 16–18 hrs foraging/day']],
        col_widths=[4, 13])

    add_h1(doc, '8. Reproductive System')
    add_table(doc,
        ['Parameter', 'Female (Cow)', 'Male (Bull)'],
        [['Sexual Maturity', '8–12 years', '12–15 years (social maturity ~20 yrs)'],
         ['Oestrous Cycle', '13–17 weeks (longest of all mammals)', 'Musth: annual 2–3 month period of heightened testosterone'],
         ['Gestation', '22 months (longest of all land mammals)', '—'],
         ['Birth Interval', '4–6 years', '—'],
         ['Litter Size', 'Usually singleton; twins very rare', '—'],
         ['Lactation', '4–5 years', '—'],
         ['Lifespan (wild)', '60–70 years', '50–60 years (bulls die earlier due to injuries)'],
         ['Breeding Season', 'Non-seasonal — year-round', 'Musth peaks during monsoon in India']],
        col_widths=[4, 6, 7])

    add_h1(doc, '9. Sensory Capabilities')
    add_table(doc,
        ['Sense', 'Capability / Notes'],
        [['Olfaction (Smell)', 'Exceptional — best sense; detects water at 19 km, predators, conspecifics, musth'],
         ['Hearing', 'Detects infrasound (1–20 Hz) over 10+ km; seismic detection through feet and trunk'],
         ['Vision', 'Poor colour vision (dichromat); good in low light; poor at long distances'],
         ['Touch', 'Highly sensitive skin especially trunk tip, ears, feet sole (seismic)'],
         ['Taste', 'Selective — rejects bitter/toxic plants; prefers specific mineral-rich soils (geophagy)']],
        col_widths=[4, 13])

    save(doc, 'Workshop_Chapter2_Anatomy_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — Infectious Diseases
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter3():
    doc = new_doc('Chapter 3 — Infectious Diseases of Asian Elephants')
    add_chapter_header(doc, '3',
        'Infectious Diseases of Asian Elephants',
        'Aetiology, Pathology, Diagnosis & Control',
        'Dr. M. Karikalan  |  ICAR-IVRI, Bareilly')

    add_h1(doc, '1. Introduction — Disease Burden in Asian Elephants')
    add_body(doc,
        'Infectious diseases pose a significant and growing threat to Asian elephant '
        'conservation. Both captive and wild populations face risks from viral, bacterial, '
        'and parasitic pathogens. Many diseases are zoonotic, posing risks to handlers '
        'and veterinary staff. Systematic necropsy, sampling, and laboratory diagnosis '
        'are essential for identifying and managing these threats.')

    add_h1(doc, '2. Viral Diseases')
    add_h2(doc, 'A. Elephant Endotheliotropic Herpesvirus (EEHV) — MOST FATAL')
    add_keybox(doc,
        'EEHV is the leading infectious cause of death in captive Asian elephant calves worldwide. '
        'Mortality rate >85% once clinical signs appear. Targets calves 1–8 years of age.', danger=True)
    add_table(doc,
        ['Feature', 'Details'],
        [['Causative Agent', 'EEHV1A, 1B, 4, 5, 6 (subfamily Betaherpesviridae; genus Proboscivirus)'],
         ['Host', 'Asian elephants primarily; latent in adults; lethal in calves'],
         ['Age Group', 'Calves 1–8 years most susceptible; adults are asymptomatic carriers'],
         ['Transmission', 'Direct contact with oral secretions; adult-to-calf transmission likely'],
         ['Incubation', 'Days to weeks; rapid progression once clinical'],
         ['Pathogenesis', 'Vascular endothelial tropism → haemorrhagic disease → DIC → shock'],
         ['Clinical Signs', 'Sudden lethargy, oedema (head/neck/limbs), cyanotic tongue, haemorrhagic discharge'],
         ['Gross PM Lesions', 'Generalised haemorrhage, oedema, hepatomegaly, splenomegaly, myocarditis'],
         ['Histopathology', 'Herpesviral intranuclear inclusions in endothelial cells of blood vessels'],
         ['Diagnosis', 'PCR on EDTA blood/trunk secretions; qPCR for quantification; IHC on tissue'],
         ['Treatment', 'Famciclovir (antiviral); supportive care; early diagnosis critical'],
         ['Prevention', 'Regular PCR screening of calves; isolation of sick animals; hygiene protocols'],
         ['Surveillance in CG', 'EEHV tested: NEGATIVE in all 13 drowning deaths (2021–2026)']],
        col_widths=[4, 13])

    add_h2(doc, 'B. Elephant Pox (Parapoxvirus / PCPV)')
    add_table(doc,
        ['Feature', 'Details'],
        [['Causative Agent', 'Parapoxvirus (PCPV — Pseudocowpox Virus); Orthopoxvirus (rare)'],
         ['Presentation', 'Nodular/pustular lesions on trunk, mouth, genitalia, skin'],
         ['Zoonotic Risk', 'YES — handlers can develop nodular lesions on hands; PPE mandatory'],
         ['Diagnosis', 'Lesion scraping for EM/PCR; Orthopox can be diagnosed by IHC'],
         ['Treatment', 'Supportive; secondary bacterial infections require antibiotics'],
         ['PM Importance', 'Pox lesions noted during external examination; samples for PCR/EM']],
        col_widths=[4, 13])

    add_h2(doc, 'C. Encephalomyocarditis Virus (EMCV)')
    add_table(doc,
        ['Feature', 'Details'],
        [['Causative Agent', 'Encephalomyocarditis Virus (Cardiovirus, Picornaviridae)'],
         ['Reservoir', 'Rodents (rats, mice) — primary reservoir; contaminated feed/water'],
         ['Clinical Signs', 'Sudden death; cardiac failure; neurological signs; myocarditis'],
         ['PM Lesions', 'Myocardial necrosis, myocarditis, pulmonary oedema, pericardial effusion'],
         ['Diagnosis', 'Virus isolation; PCR; IHC for EMCV antigen in heart tissue'],
         ['Zoonotic Risk', 'Low in healthy adults; immunocompromised persons at risk']],
        col_widths=[4, 13])

    add_h2(doc, 'D. Foot-and-Mouth Disease (FMD)')
    add_table(doc,
        ['Feature', 'Details'],
        [['Causative Agent', 'Aphthovirus — serotypes O, A, C, SAT1/2/3, Asia1'],
         ['Significance', 'Primarily a livestock disease; elephants susceptible — sporadic outbreaks'],
         ['Clinical Signs', 'Vesicles on feet, trunk, mouth; lameness; reluctance to move; salivation'],
         ['PM Lesions', 'Erosions/ulcers on tongue, gums, coronary band of feet'],
         ['Diagnosis', 'Vesicular fluid/epithelium for ELISA, PCR, virus isolation'],
         ['Control', 'Vaccination in livestock around elephant habitats; movement restriction']],
        col_widths=[4, 13])

    add_h1(doc, '3. Bacterial Diseases')
    add_h2(doc, 'A. Tuberculosis (TB) — Mycobacterium tuberculosis')
    add_keybox(doc,
        'Elephant TB is a ZOONOSIS of highest public health concern. '
        'Mahouts, handlers and veterinary staff are at risk of airborne infection from '
        'trunk secretions and breath of infected elephants.', danger=True)
    add_table(doc,
        ['Feature', 'Details'],
        [['Causative Agent', 'Mycobacterium tuberculosis (human strain); M. bovis less common'],
         ['Transmission', 'Aerosol from trunk secretions; direct contact; contaminated feed/water'],
         ['Clinical Signs', 'Weight loss, weakness, intermittent trunk discharge, respiratory distress; often subclinical'],
         ['PM Lesions', 'Granulomata in lungs, thoracic LN, liver, spleen; cavitation in advanced cases'],
         ['Histopathology', 'Caseous necrosis, Langhans giant cells, lymphocytic infiltration'],
         ['Diagnosis', 'ELISA (ElephantTB STAT-PAK), trunk wash culture (BSL-3), PCR, MGIT'],
         ['Zoonotic Risk', 'HIGH — PPE (N95 mask, gloves, gown) MANDATORY during necropsy'],
         ['Treatment', 'Anti-TB regimen (isoniazid, rifampicin, ethambutol) — long-term, complex in elephants'],
         ['Surveillance', 'Annual trunk wash culture for all captive elephants is mandatory (MoEFCC guidelines)']],
        col_widths=[4, 13])

    add_h2(doc, 'B. Anthrax (Bacillus anthracis)')
    add_table(doc,
        ['Feature', 'Details'],
        [['Causative Agent', 'Bacillus anthracis — spore-forming, Gram-positive rod'],
         ['Risk Areas', 'Soil-borne; enzootic in parts of Karnataka, Andhra Pradesh; CG reports rare'],
         ['Presentation', 'Peracute death; bloody discharge from body orifices; bloating; no rigor mortis'],
         ['PM Protocol', 'DO NOT OPEN carcass if anthrax suspected — risk of sporulation and environmental contamination'],
         ['Diagnosis', 'Blood smear (McFadyean stain — blue-black rods with pink capsule), FAT, PCR'],
         ['Zoonotic Risk', 'EXTREME — cutaneous, gastrointestinal, pulmonary anthrax in humans'],
         ['Disposal', 'Carcass must be incinerated in situ; burial with lime strongly discouraged']],
        col_widths=[4, 13])

    add_h2(doc, 'C. Salmonellosis, Pasteurellosis, and Other Bacterial Infections')
    add_table(doc,
        ['Pathogen', 'Common Presentation', 'Key Samples for Diagnosis'],
        [['Salmonella spp.', 'Septicaemia, haemorrhagic enteritis, sudden death in calves', 'Intestinal contents, spleen, liver'],
         ['Pasteurella multocida', 'Haemorrhagic septicaemia, pneumonia — especially stressed/captive animals', 'Lung, lymph nodes, blood'],
         ['Clostridium perfringens', 'Enterotoxaemia, sudden death; haemorrhagic enteritis', 'Intestinal contents (fresh — no fixative)'],
         ['Streptococcus spp.', 'Septicaemia, endocarditis, joint infection, skin abscess', 'Blood, joint fluid, abscess swab'],
         ['E. coli', 'Diarrhoea in calves; secondary infections', 'Faeces, intestine'],
         ['Leptospira spp.', 'Jaundice, haemolytic anaemia, renal failure — waterborne', 'Kidney, urine, serum (MAT)']],
        col_widths=[3.5, 6.5, 7])

    add_h1(doc, '4. Parasitic Diseases')
    add_table(doc,
        ['Parasite Group', 'Species', 'Site', 'Clinical Impact', 'Diagnosis'],
        [['Nematodes', 'Quilonia spp., Murshidia spp., Choniangium spp.', 'Large intestine', 'Colic, weight loss, anaemia in heavy burden', 'Faecal flotation, PM intestinal exam'],
         ['Trematodes', 'Brumptia bicaudata', 'Caecum, large intestine', 'Usually subclinical; heavy loads cause enteritis', 'Faecal sedimentation, PM'],
         ['Cestodes', 'Anoplocephala manubriata', 'Small intestine', 'Mild; rarely cause mortality', 'Faecal exam, PM intestine'],
         ['Protozoa', 'Trypanosoma spp.', 'Blood', 'Nagana-like syndrome; emaciation; rarely fatal', 'Blood smear, PCR'],
         ['Ectoparasites', 'Haemaphysalis, Amblyomma ticks; lice; mange mites', 'Skin', 'Anaemia, skin lesions, vector for pathogens', 'Skin scraping, tick collection']],
        col_widths=[3, 3.5, 2.5, 4, 4])

    add_h1(doc, '5. EEHV Surveillance Protocol — Field Guide')
    add_table(doc,
        ['Step', 'Action', 'Sample/Method'],
        [['1', 'Monitor calves 1–8 years: check for lethargy, oedema, discoloured tongue daily', 'Clinical observation'],
         ['2', 'Collect EDTA blood at first clinical sign — do not delay', '5–10 mL EDTA tube on ice'],
         ['3', 'Trunk wash (saline lavage) — collect in sterile container', '10 mL saline; aspirate and collect'],
         ['4', 'Ship samples on ice to ICAR-IVRI Bareilly within 24 hrs', 'Cold chain mandatory'],
         ['5', 'At PM: collect spleen, lymph node, heart, liver in 10% NBF and RNAlater', 'Fixed + fresh tissue'],
         ['6', 'Run qPCR for EEHV1A, 1B, 4, 5, 6 subtypes', 'ICAR-IVRI diagnostic lab'],
         ['7', 'Document GPS coordinates, herd composition, other calves in contact', 'Field report + photographs']],
        col_widths=[0.8, 8.5, 7.7])

    add_h1(doc, '6. Zoonotic Disease Risk at Necropsy — Safety Summary')
    add_keybox(doc,
        'ALL elephant necropsies carry zoonotic risk. PPE is NON-NEGOTIABLE: '
        'gloves (double), N95 mask, eye protection, gown, boot covers. '
        'Wash hands with soap + disinfect with 70% alcohol after every PM.', danger=True)
    add_table(doc,
        ['Disease', 'Risk Level', 'Route of Transmission', 'PPE Required'],
        [['Tuberculosis', 'HIGH', 'Aerosol from trunk secretions, breath', 'N95 mask, full PPE, BSL-3 sample handling'],
         ['Anthrax', 'EXTREME', 'Cutaneous contact, aerosol, ingestion', 'Do NOT open — call for specialist support'],
         ['Elephant Pox', 'MODERATE', 'Direct contact with lesions', 'Gloves, eye protection'],
         ['Salmonellosis', 'LOW-MOD', 'Faecal-oral contamination', 'Gloves, hand hygiene'],
         ['Leptospirosis', 'MODERATE', 'Urine, kidney tissue contact', 'Waterproof gloves, eye shield'],
         ['EEHV', 'NONE (humans)', 'Not zoonotic', 'Standard gloves only for EEHV cases']],
        col_widths=[3.5, 2.5, 5, 6])

    save(doc, 'Workshop_Chapter3_Infectious_Diseases_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 4 — Biological Sample Collection
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter4():
    doc = new_doc('Chapter 4 — Biological Sample Collection for Wildlife Disease Diagnosis')
    add_chapter_header(doc, '4',
        'Collection of Biological Materials for Wildlife Disease Diagnosis',
        'Sampling Protocols, Preservation, Packing & Referral',
        'Dr. M. Karikalan  |  ICAR-IVRI, Bareilly')

    add_h1(doc, '1. Why We Collect Biological Materials — The Diagnostic Pipeline')
    add_body(doc,
        'Biological samples are the irreplaceable foundation of wildlife disease diagnosis. '
        'Without properly collected, preserved, and transported samples, even the most advanced '
        'laboratory cannot establish a definitive cause of death. The diagnostic pipeline runs: '
        'Field observation → Sample collection → Chain of custody → Laboratory analysis → '
        'Definitive diagnosis → Management response.')
    add_keybox(doc,
        'RULE 1: Collect early — within 6 hrs of death ideally. '
        'RULE 2: Collect widely — minimum 15+ sample types per case. '
        'RULE 3: Label everything — sample ID, date, GPS, animal ID on every tube.')

    add_h2(doc, 'How Disease Shows Up: Gene → Gross')
    add_table(doc,
        ['Level', 'What Changes', 'Detected By'],
        [['Gene/Molecule', 'DNA mutation, protein dysfunction, toxin binding', 'PCR, sequencing, ELISA, LC-MS'],
         ['Cell', 'Degeneration, necrosis, inclusion bodies, inflammation', 'Histopathology (H&E staining)'],
         ['Tissue', 'Haemorrhage, necrosis, infarct, oedema, abscess', 'Gross PM + histopathology'],
         ['Organ', 'Size change, colour, texture, weight abnormality', 'Gross PM + organ weight'],
         ['Animal', 'Clinical signs: fever, weakness, discharge, behavioural change', 'Clinical examination']],
        col_widths=[3, 6, 8])

    add_h1(doc, '2. Master Sample-Collection Table')
    add_keybox(doc, 'Collect ALL sample types listed below from EVERY elephant PM — even if cause seems obvious. '
                    'Multiple samples prevent diagnostic gaps when unexpected findings emerge.')
    add_table(doc,
        ['Sample Type', 'Volume/Amount', 'Container', 'Preservation', 'Tests'],
        [['EDTA Blood', '5–10 mL', 'Purple-top tube', 'Ice (4°C) — DO NOT freeze', 'CBC, PCR (EEHV, TB), haematology'],
         ['Serum (clotted blood)', '10 mL', 'Red-top tube', 'Centrifuge → freeze serum at -20°C', 'Serology, ELISA, biochemistry'],
         ['Urine', '20–50 mL', 'Sterile container', 'Refrigerate or freeze', 'Urinalysis, toxicology, leptospira'],
         ['Nasal/Trunk Swab', '2 swabs per site', 'Viral transport medium (VTM)', 'Ice — ship within 24 hrs', 'EEHV, Herpesvirus, Influenza PCR'],
         ['Faecal Sample', '30–50 g', 'Sterile container', 'Refrigerate; fix portion in 10% formalin', 'Parasitology, bacteriology'],
         ['Lung tissue', '5 × 5 cm block', 'Zip-lock bag (fresh) + NBF jar (fixed)', '-20°C fresh; RT in NBF', 'Histopath, bacteriology, virology'],
         ['Liver tissue', '5 × 5 cm block', 'Same as lung', '-20°C fresh; RT in NBF', 'Histopath, toxicology, bacteriology'],
         ['Spleen tissue', '5 × 5 cm block', 'Same as lung', '-20°C fresh; RT in NBF', 'PCR (EEHV, TB), histopath, culture'],
         ['Kidney tissue', '5 × 5 cm block', 'Same as lung', '-20°C fresh; RT in NBF', 'Histopath, leptospira, toxicology'],
         ['Heart tissue', '5 × 5 cm block', 'Same as lung', '-20°C fresh; RT in NBF', 'EMCV, bacterial culture, histopath'],
         ['Lymph node (mesenteric)', '1–2 nodes', 'Same as above', '-20°C fresh; RT in NBF', 'TB, EEHV, bacterial culture, histo'],
         ['Brain tissue', 'Half brain', 'NBF (fixed) + fresh in zip-lock', '-20°C fresh; RT in NBF', 'Rabies (fresh), histopath, NiV'],
         ['Bone marrow (femur/rib)', '5–10 mL aspirate or bone fragment', 'EDTA tube or zip-lock', 'Freeze', 'Diatom test, haematology, toxicology'],
         ['Stomach contents', '100–200 mL', 'Sterile wide-mouth jar', 'Freeze at -20°C', 'Toxicology (pesticide, metal, alkaloid)'],
         ['Water/soil sample', '500 mL water; 200 g soil', 'Sterile bottles', 'Refrigerate', 'Environmental toxicology, arsenic, heavy metals']],
        col_widths=[3.5, 3, 3, 3.5, 4])

    add_h1(doc, '3. Histopathological Examination Protocol')
    add_body(doc, '10% Neutral Buffered Formalin (NBF) Recipe:')
    add_table(doc,
        ['Component', 'Amount'],
        [['40% Formaldehyde solution (formalin)', '100 mL'],
         ['Sodium dihydrogen phosphate monohydrate (NaH₂PO₄·H₂O)', '3.5 g'],
         ['Disodium hydrogen phosphate anhydrous (Na₂HPO₄)', '6.5 g'],
         ['Distilled water', 'Make up to 1,000 mL (1 litre)'],
         ['Final pH', '7.0–7.4 (neutral)'],
         ['Tissue:Formalin ratio', '1:10 (1 part tissue to 10 parts formalin)'],
         ['Tissue thickness', 'Maximum 1 cm slices for adequate penetration']],
        col_widths=[8, 9])
    add_keybox(doc,
        'CRITICAL: Tissue in formalin is fixed permanently within 24–48 hrs. '
        'Too little formalin → autolysis in centre. Too thick → formalin does not penetrate. '
        'Slice tissue to 1 cm max thickness before fixing.')

    add_h1(doc, '4. Toxicological Sampling')
    add_table(doc,
        ['Sample', 'Amount', 'Container', 'Target Toxins'],
        [['Stomach/rumen contents', '100–200 mL', 'Sterile jar — freeze', 'All toxins — primary sample'],
         ['Liver', '100–200 g', 'Zip-lock — freeze', 'Metals, organochlorine, alkaloids, CPA'],
         ['Kidney', '50–100 g', 'Zip-lock — freeze', 'Heavy metals (Pb, Hg, Cd, As)'],
         ['Blood (EDTA)', '10 mL', 'EDTA — freeze', 'Organophosphate, nitrate, anticoagulants'],
         ['Urine', '50 mL', 'Sterile — freeze', 'Metals, pesticide metabolites'],
         ['Bone marrow', '5–10 g', 'Zip-lock — freeze', 'Chronic heavy metal exposure (Pb, Hg)'],
         ['Feed/fodder sample', '500 g', 'Zip-lock — freeze', 'Mycotoxins (CPA, aflatoxin), pesticide residues'],
         ['Water sample', '500 mL', 'Sterile bottle', 'Arsenic, cyanobacterial toxins, nitrate'],
         ['Soil sample', '200 g', 'Sterile bag', 'Arsenic, persistent organic pollutants']],
        col_widths=[4, 2.5, 3.5, 7])
    add_keybox(doc,
        'DO NOT mix samples. DO NOT use plastic containers for metal analysis (use glass). '
        'Label: animal ID, sample type, GPS, date, time, collector name.')

    add_h1(doc, '5. Bacteriological & Virological Examination')
    add_table(doc,
        ['Test Type', 'Samples Required', 'Transport Conditions', 'Turnaround'],
        [['Aerobic culture', 'Spleen, lung, liver, LN — fresh sterile', 'Ice (4°C) — 24 hrs max', '3–7 days'],
         ['Anaerobic culture', 'Intestinal contents — special anaerobic swabs', 'Anaerobic transport medium', '3–7 days'],
         ['Virus isolation', 'Lung, spleen, brain — fresh or in VTM', '-70°C or on dry ice', '1–3 weeks'],
         ['PCR (bacterial)', 'Any tissue — fresh or fixed', 'Ice or freeze', '3–5 days'],
         ['PCR (viral — EEHV)', 'EDTA blood, trunk wash, spleen', 'Ice — urgent', '24–48 hrs (ICAR-IVRI)'],
         ['ELISA (serology)', 'Serum (2 samples 3 wks apart)', 'Freeze serum', '1–3 days']],
        col_widths=[4, 4.5, 4, 4.5])

    add_h1(doc, '6. Packing & Transport')
    add_h2(doc, '10-Step Packing Protocol')
    steps = [
        '1. Label ALL containers before collection — use waterproof marker, never adhesive labels alone',
        '2. Fill primary container (tube/jar) — leave 10% headspace for expansion',
        '3. Seal with parafilm + tape — double-seal for liquid samples',
        '4. Wrap in absorbent material (cotton wool/paper) — enough to absorb total volume',
        '5. Place in secondary leak-proof container (zip-lock or screw-top)',
        '6. Pack secondary containers in triple-wall corrugated box with ice packs',
        '7. Insert completed sample submission form INSIDE box (not on outside only)',
        '8. Seal box with security tape — sign across seal',
        '9. Label outer box: BIOLOGICAL SPECIMEN — FRAGILE — KEEP COOL',
        '10. Notify laboratory before dispatch — confirm receipt within 24 hrs',
    ]
    for step in steps:
        add_bullet(doc, step)
    doc.add_paragraph()

    add_h1(doc, '7. Quick Master Reference')
    add_table(doc,
        ['Priority', 'Sample', 'Container', 'Temp', 'Do NOT'],
        [['URGENT', 'EDTA blood', 'Purple top', '4°C (ice)', 'Freeze whole blood'],
         ['URGENT', 'Trunk swab', 'VTM', '4°C (ice)', 'Dry swab in plain tube'],
         ['HIGH', 'Lung/Spleen/LN (fresh)', 'Sterile zip-lock', '-20°C', 'Add formalin to fresh tissue'],
         ['HIGH', 'Lung/Liver (fixed)', '10% NBF in jar', 'Room temp', 'Over-fix (>72 hrs) or freeze in NBF'],
         ['HIGH', 'Stomach contents', 'Wide-mouth sterile jar', '-20°C', 'Add preservatives'],
         ['HIGH', 'Serum', 'Red top → aliquot', '-20°C', 'Haemolyse — centrifuge early'],
         ['MOD', 'Bone marrow', 'EDTA or dry sterile', '-20°C', 'Air-dry; contaminate'],
         ['MOD', 'Faeces', 'Sterile container', '4°C', 'Use household container'],
         ['MOD', 'Urine', 'Sterile container', '4°C/-20°C', 'Use urine dipstick container for culture']],
        col_widths=[2, 3, 3.5, 2.5, 6])

    add_h1(doc, '8. National Referral Laboratories')
    add_table(doc,
        ['Laboratory', 'Tests', 'Contact'],
        [['ICAR-IVRI, Bareilly (UP)', 'EEHV PCR, histopathology, bacteriology, toxicology, serology, virology',
          'Dir: 0581-2301502 | ivri@icar.org.in'],
         ['NDVSU, Jabalpur (MP)', 'Wildlife pathology, toxicology, PM diagnosis, histopath',
          '0761-2600204'],
         ['WII, Dehradun (UK)', 'Wildlife disease surveillance, population health, ecological studies',
          '0135-2640112'],
         ['NRC on Equines, Hisar', 'Equid diseases, some elephant pathogens as referral',
          '01662-276702'],
         ['NCDC, Delhi', 'Zoonotic disease, public health — anthrax, rabies, TB confirmation',
          '011-23921401']],
        col_widths=[4, 8, 5])

    save(doc, 'Workshop_Chapter4_Sampling_Protocols_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 5 — Non-Infectious Diseases
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter5():
    doc = new_doc('Chapter 5 — Non-Infectious Diseases in Asian Elephants')
    add_chapter_header(doc, '5',
        'Non-Infectious Diseases in Asian Elephants',
        'Toxicoses, Physical Trauma, Nutritional Deficiencies & Field Investigation',
        'Dr. Karikalan Mathesh  |  ICAR-IVRI, Bareilly')

    add_h1(doc, '1. Background — Why Elephants Are Biologically Distinct')
    add_body(doc,
        'Understanding elephant biology is essential to interpreting non-infectious disease '
        'pathology. Several unique features make elephants both resistant to some conditions '
        '(e.g. cancer — Peto\'s Paradox) and exceptionally vulnerable to others (e.g. '
        'mycotoxin toxicosis, electrocution, heat stress).')
    add_h2(doc, 'Cancer Resistance — Peto\'s Paradox')
    add_body(doc,
        'Despite their massive body size and long lifespan, elephants rarely develop cancer. '
        'This appears to be due to 20 copies of the TP53 tumour-suppressor gene (humans have 2). '
        'Elephants also show enhanced p53-mediated apoptosis — damaged cells are eliminated '
        'before malignant transformation. This is one of the most remarkable evolutionary '
        'adaptations in mammalian oncology.')
    add_h2(doc, 'High Susceptibility to Toxicity')
    add_table(doc,
        ['Factor', 'Implication'],
        [['Large body mass', 'Requires enormous food intake → higher exposure to contaminated feed'],
         ['Hindgut fermentation', 'Mycotoxins in feed amplified by gut flora; longer gut transit time'],
         ['Low metabolic rate', 'Slower toxin clearance compared to smaller mammals'],
         ['Indiscriminate feeding (stressed)', 'Captive/crop-raiding elephants consume contaminated grain'],
         ['Rumen bypass', 'No rumen biotransformation of toxins — absorbed directly from intestine'],
         ['Sensitive endothelium', 'Vascular endothelium highly susceptible to oxidative toxin damage']],
        col_widths=[5, 12])

    add_h1(doc, '2. Case Study — Mass Mortality at Bandhavgarh NP (Oct 2024)')
    add_keybox(doc,
        'October 2024: 10 Asian elephant deaths in Bandhavgarh Tiger Reserve over 4 days. '
        'Final diagnosis: Cyclopiazonic Acid (CPA) toxicosis from Kodo millet (Paspalum scrobiculatum). '
        'Confirmed by LC-MS at ICRISAT, Hyderabad.', danger=True)
    add_h2(doc, 'History & Field Observations')
    add_body(doc,
        'Herd of ~10 elephants observed feeding on Kodo millet crop fields at edge of reserve. '
        'Within 12–24 hrs: sudden collapse, ataxia, hypersalivation, behavioural depression, '
        'recumbency. Rapid deaths over 4 days. No infectious disease outbreak in area.')
    add_h2(doc, 'Gross PM Findings')
    add_table(doc,
        ['System / Organ', 'Gross Finding'],
        [['Forestomach/Rumen equivalent', 'N/A (hindgut fermenter) — stomach had large volume of millet grain'],
         ['Liver', 'Pale, friable, enlarged — centrilobular necrosis on cut section'],
         ['Kidneys', 'Pale, swollen — cortical pallor'],
         ['Intestines', 'Haemorrhagic enteritis — reddened mucosa with petechiae'],
         ['Lungs', 'Congested, oedematous — secondary to cardiovascular shock'],
         ['Heart', 'Petechiae on epicardium; myocardial pallor in some animals'],
         ['Brain', 'Congestion; petechiae — consistent with hypoxia/shock']],
        col_widths=[5, 12])
    add_h2(doc, 'Toxicology Results (LC-MS — ICRISAT Hyderabad)')
    add_table(doc,
        ['Sample', 'CPA Detected', 'Level'],
        [['Stomach contents', 'YES', 'High (>50 ppb)'],
         ['Liver', 'YES', 'Moderate (10–25 ppb)'],
         ['Kodo millet from field', 'YES', 'Very high (>200 ppb — contaminated grain)'],
         ['Serum', 'YES', 'Detectable'],
         ['EEHV PCR', 'NEGATIVE', '—'],
         ['Organochlorine/Phosphate', 'NEGATIVE', '—'],
         ['Heavy metals (Pb/Hg/Cd/As)', 'NEGATIVE', '—']],
        col_widths=[5, 4, 8])

    add_h1(doc, '3. Cyclopiazonic Acid (CPA) — Key Facts')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Producing fungi', 'Aspergillus flavus, A. oryzae, Penicillium cyclopium — common soil fungi'],
         ['Substrate', 'Kodo millet (Paspalum scrobiculatum), maize, groundnut, sorghum'],
         ['Conditions for growth', 'High humidity, temperature 25–37°C, pre-harvest or storage damage'],
         ['Mechanism of toxicity', 'Inhibits Ca²⁺-ATPase pump (SERCA) → disrupts intracellular calcium → cell death'],
         ['Target organs', 'Liver (necrosis), kidney (tubular damage), heart (myocardial degeneration), GI tract'],
         ['LD50 (rat)', '36 mg/kg bodyweight (acute)'],
         ['Historical case', 'Kodo poisoning known in India since 1917 — "Kodua poisoning" in humans eating contaminated millet'],
         ['Season of risk', 'Post-monsoon harvest (Oct–Dec) — wet grain in field; humid storage'],
         ['Detection', 'LC-MS/MS (most sensitive); ELISA available; TLC for screening']],
        col_widths=[5, 12])
    add_h2(doc, 'Prevention & Control')
    bullets = [
        'Avoid allowing elephants to access Kodo millet fields — especially post-monsoon harvest',
        'Crop monitoring: mycological testing of grain during harvest season',
        'Moisture-controlled storage — <14% grain moisture inhibits fungal growth',
        'Rapid autopsy + LC-MS testing of first death in any cluster event',
        'Liaison with forest department to map Kodo millet cultivation areas within/adjacent to elephant habitats',
    ]
    for b in bullets:
        add_bullet(doc, b)
    doc.add_paragraph()

    add_h1(doc, '4. Electrocution')
    add_keybox(doc,
        'Electrocution = 47% of all elephant deaths in Chhattisgarh (2021–2026). '
        '23 confirmed electrocution deaths. Oct–Dec peak — illegal fencing to protect paddy/maize crops.', danger=True)
    add_h2(doc, 'Comparison of Injury Patterns')
    add_table(doc,
        ['Parameter', 'Lightning Strike', 'High Voltage (HV) Line', 'Low Voltage (LV) Fence'],
        [['Voltage', '>100 million V', '11 kV–132 kV', '220 V–440 V'],
         ['Mechanism', 'Flash-over; side-potential herd deaths', 'Direct contact; step potential', 'Prolonged contact; cardiac arrest'],
         ['Entry wound', 'Large irregular char mark', 'Deep char at contact point', 'Small char or absent'],
         ['Exit wound', 'Multiple; on feet (ground contact)', 'Typically on feet', 'Feet — small'],
         ['Internal organs', 'Haemorrhage throughout; visceral rupture', 'Linear haemorrhage along current path', 'Cardiac changes primary'],
         ['Herd effect', 'YES — side-potential can kill multiple', 'Step-potential affects nearby animals', 'Direct contact only'],
         ['PM smell', 'Burnt hair/skin smell', 'Burnt smell at entry/exit', 'May be subtle'],
         ['Scene evidence', 'Split trees; scorched ground; no lines', 'Broken power line; fused wire ends', 'Illegal fence wire at scene']],
        col_widths=[4, 4, 4, 5])
    add_h2(doc, 'PM Findings in Electrocution')
    add_table(doc,
        ['Finding', 'Significance'],
        [['Char marks at entry/exit', 'Pathognomonic — document with photograph and GPS'],
         ['Metallodermic marks', 'Imprint of wire/equipment on skin'],
         ['Muscle haemorrhage along current path', 'Joule heating effect in tissues'],
         ['Petechial haemorrhage — heart, lungs, brain', 'Cardiorespiratory arrest secondary to ventricular fibrillation'],
         ['Arborescent (Lichtenberg) marks', 'Lightning specific — branching red skin marks'],
         ['Rapid decomposition', 'Heat from current accelerates autolysis — PM within 6 hrs essential'],
         ['No significant internal pathology', 'May be seen in LV fence deaths — external findings are key']],
        col_widths=[6, 11])

    add_h1(doc, '5. Lightning Side-Potential (Herd Mortality)')
    add_body(doc,
        'When lightning strikes near a herd, ground current radiates outward in concentric '
        'circles (step potential / side flash). Front legs and back legs are at different '
        'potentials, creating a current path through the body. Calves and smaller animals '
        'are most susceptible. Multiple simultaneous deaths at same location during/after storm '
        'should raise immediate suspicion of lightning side-potential.')
    add_table(doc,
        ['Indicator', 'Details'],
        [['Multiple deaths simultaneously', 'Lightning — same location, same time (storm)'],
         ['Concentric position of carcasses', 'Radiate from central strike point'],
         ['Split trees / burnt vegetation', 'Lightning strike point evidence'],
         ['Skin findings', 'Lichtenberg marks (arborescent patterns) on some individuals'],
         ['Season', 'Pre-monsoon / monsoon (April–September in India)'],
         ['PM findings', 'Similar to HV — haemorrhage, cardiac arrest; may be less localised']],
        col_widths=[5, 12])

    add_h1(doc, '6. Nutritional Deficiencies')
    add_table(doc,
        ['Deficiency', 'Mechanism', 'Clinical Signs', 'PM Findings', 'Field Sampling'],
        [['Iron (Fe)', 'Reduced haemoglobin; anaemia', 'Pallor, weakness, tachycardia, collapse', 'Pale mucosae, thin watery blood, iron-poor marrow', 'Blood (CBC, serum iron, ferritin), bone marrow'],
         ['Calcium/Phosphorus', 'Bone resorption, osteomalacia', 'Bone pain, fractures, fracture sites, stiff gait', 'Soft/rubbery bones, pathological fractures', 'Serum Ca/P, bone biopsy'],
         ['Iodine', 'Hypothyroidism', 'Goitre, weight gain, poor coat, reproductive failure', 'Enlarged thyroid gland', 'Thyroid tissue, serum T3/T4'],
         ['Vitamin E/Selenium', 'Oxidative damage to muscle', 'White muscle disease, weakness, sudden death', 'Pale/white cardiac and skeletal muscle — white streaks', 'Serum selenium, muscle biopsy'],
         ['Copper (Cu)', 'Enzyme dysfunction, demyelination', 'Depigmentation, weakness, diarrhoea, nervous signs', 'Swaybacker lesions in brain; liver copper low', 'Liver, serum copper, brain']],
        col_widths=[2.5, 4, 4, 3.5, 3])

    add_h1(doc, '7. Field Investigation Framework')
    add_table(doc,
        ['Phase', 'Action Items'],
        [['Scene Assessment', 'GPS; photograph scene before disturbing; note carcass position, orientation, vegetation damage, wire/equipment present'],
         ['History', 'When last seen alive; feed/water sources; recent weather; herd composition; any unusual activity (raiding, musth)'],
         ['External Examination', 'Char marks, wounds, tusk damage, skin condition, orifice discharge, body condition score, age estimation'],
         ['PM Examination', 'Systematic organ examination; document gross findings; photograph all lesions; weigh organs if possible'],
         ['Sample Collection', 'Collect ALL samples from master list; maintain cold chain; double-label every sample'],
         ['Environmental Samples', 'Water (nearby sources), soil (around carcass), feed/fodder from last known feeding site'],
         ['Documentation', 'Complete PM report with GPS, photographs, sample list; chain of custody form for all samples'],
         ['Preliminary Findings', 'Verbal report to CF/PCCF within 24 hrs; written report within 72 hrs; lab results to follow']],
        col_widths=[3.5, 13.5])

    save(doc, 'Workshop_Chapter5_NonInfectious_Diseases_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 6 — Non-Infectious Pathology
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter6():
    doc = new_doc('Chapter 6 — Non-Infectious Pathology in Asian Elephants')
    add_chapter_header(doc, '6',
        'Non-Infectious Pathology in Asian Elephants',
        'Toxicoses, Electrocution, Reproductive Disorders & Metabolic Diseases',
        'Prof. Dr. A. B. Shrivastava  |  NDVSU, Jabalpur')

    add_h1(doc, '1. Elephant Poisoning in India — Overview')
    add_body(doc,
        'Poisoning (toxicosis) is an under-investigated cause of elephant mortality in India. '
        'Confirmatory diagnosis requires systematic toxicological sampling and laboratory '
        'analysis. The three main routes of exposure are ingestion (most common), inhalation, '
        'and skin absorption.')
    add_table(doc,
        ['Route', 'Sources', 'Examples in Elephants'],
        [['Ingestion', 'Contaminated feed, water bodies, toxic plants, bait', 'Kodo millet (CPA), cyanobacterial toxins, toxic plants, HCN plants'],
         ['Inhalation', 'Industrial fumes, pesticide spray, wildfire smoke', 'Organophosphate aerosol, CO from generator'],
         ['Skin Absorption', 'Pesticidal dip, topical application, contaminated mud', 'Organochlorine skin absorption, caustic burns']],
        col_widths=[3, 5, 9])

    add_h1(doc, '2. Mycotoxins & Biological Toxins')
    add_h2(doc, 'A. Crop-Borne Mycotoxins — CPA & Kodo Millet')
    add_body(doc,
        'Cyclopiazonic Acid (CPA) from Kodo millet (Paspalum scrobiculatum) is the leading '
        'documented mycotoxin causing elephant deaths in India (Bandhavgarh 2024). '
        'See Chapter 5 for full case details. Key pathological findings:')
    add_table(doc,
        ['Organ', 'Pathological Change', 'Histopathology'],
        [['Liver', 'Pale, enlarged; centrilobular necrosis', 'Centrilobular hepatocyte necrosis, vacuolation, bile duct proliferation'],
         ['Kidneys', 'Pale, swollen cortex', 'Proximal tubular degeneration, necrosis, cast formation'],
         ['Heart', 'Pale myocardium', 'Myofibre necrosis, interstitial oedema, mononuclear infiltration'],
         ['GI Tract', 'Haemorrhagic gastroenteritis', 'Villous blunting, mucosal erosion, crypt necrosis']],
        col_widths=[3, 6, 8])
    add_h2(doc, 'When Does Contamination Occur?')
    add_table(doc,
        ['Stage', 'Risk Level', 'Notes'],
        [['Pre-harvest (wet field)', 'HIGH', 'Fungal sporulation in standing water between crop rows'],
         ['At harvest (hand-cutting)', 'HIGH', 'Fungal hyphae concentrated in harvested grain'],
         ['Storage (damp conditions)', 'VERY HIGH', 'Amplification in sealed containers with moisture'],
         ['Dry storage (<14% moisture)', 'LOW', 'Inhibits fungal growth — proper storage protects']],
        col_widths=[5, 3, 9])
    add_h2(doc, 'B. Cyanotoxins — Cyanobacterial (Blue-Green Algae) Toxins')
    add_table(doc,
        ['Feature', 'Details'],
        [['Producing organism', 'Microcystis aeruginosa, Anabaena, Oscillatoria — bloom in stagnant warm water'],
         ['Season', 'Summer months (April–June), post-monsoon eutrophic ponds'],
         ['Toxins produced', 'Microcystins (liver damage), Anatoxins (neurotoxic), Cylindrospermopsin (kidney)'],
         ['Gross PM findings', 'Liver — pale, necrotic; kidney — swollen; gut haemorrhage; blood fails to clot'],
         ['Diagnosis', 'ELISA for microcystin in water/liver; LC-MS for quantification'],
         ['CG relevance', 'Dam/pond environments in Tamnar/Kharsia Ranges — potential arsenic co-contamination']],
        col_widths=[4, 13])
    add_h2(doc, 'C. Toxic Plants')
    add_table(doc,
        ['Plant', 'Toxic Principle', 'Clinical Effects', 'PM Findings'],
        [['Lantana camara', 'Lantadene A & B (triterpenoids)', 'Photosensitisation, jaundice, GI upset', 'Bile duct proliferation, cholestasis, skin necrosis'],
         ['Calotropis procera (Aak)', 'Calotoxin, calactin (cardiac glycosides)', 'Cardiac arrest, hypersalivation, convulsions', 'Haemorrhage, cardiac changes'],
         ['Datura spp. (Dhatura)', 'Scopolamine, atropine (alkaloids)', 'Dilated pupils, tachycardia, hyperthermia, coma', 'Stomach contents; no specific lesion'],
         ['Castor bean (Ricinus communis)', 'Ricin (cytotoxin)', 'Acute organ failure, haemorrhage, death', 'Gastroenteritis, organ haemorrhage'],
         ['Oleander (Nerium)', 'Oleandrin (cardiac glycoside)', 'Cardiac arrhythmia, death', 'Cardiac haemorrhage'],
         ['Plumeria (Temple flower)', 'Plumericin, isoplumericin', 'GI irritation, rarely fatal', 'Gastroenteritis'],
         ['Parthenium hysterophorus', 'Parthenin (sesquiterpene)', 'Contact dermatitis, photosensitisation', 'Skin lesions, liver']],
        col_widths=[3.5, 3.5, 5, 5])

    add_h1(doc, '3. Hydrocyanic Acid (HCN) Poisoning')
    add_table(doc,
        ['Feature', 'Details'],
        [['Sources', 'Sorghum (young plants, drought-stressed), cassava, bamboo shoots, Johnson grass, Prunus seeds'],
         ['Mechanism', 'CN⁻ binds cytochrome c oxidase → inhibits cellular respiration → histotoxic anoxia despite normal blood O₂'],
         ['Speed of action', 'Peracute — death within minutes to 2 hrs; animals may be found dead without premonitory signs'],
         ['Clinical signs', 'Anxiety, hyperpnoea, staggering, bright red mucosae (oxyhemoglobin), collapse, convulsions, death'],
         ['Gross PM findings', 'Bright cherry-red blood and organs (oxyhemoglobin), haemorrhage, no rigor mortis'],
         ['Smell', 'Bitter almonds — detectable in stomach contents and rumen at PM'],
         ['Diagnosis', 'Conway microdiffusion method on fresh stomach contents; must be run within hours'],
         ['Treatment (live animal)', 'Sodium nitrite (3 mg/kg IV) + Sodium thiosulfate (660 mg/kg IV) — emergency antidote']],
        col_widths=[4, 13])
    add_h2(doc, 'Jabalpur Case Study — 5 Captive Elephants')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Setting', 'Captive circus facility, Jabalpur'],
         ['Year', 'Historical case (Dr. Shrivastav personal records)'],
         ['Number affected', '5 elephants presented with sudden collapse within 30 min of feeding'],
         ['Feed implicated', 'Freshly cut Sorghum (jowar) — drought-stressed young plants'],
         ['Clinical signs', 'Rapid onset; bright red mucosae; hyperpnoea; collapse; 2 died before treatment'],
         ['Treatment (3 survivors)', 'Sodium nitrite IV + Sodium thiosulfate IV; supportive care (IV fluids, oxygen)'],
         ['Diagnosis confirmed', 'Conway test POSITIVE for HCN on stomach lavage from deceased animals'],
         ['Outcome', '3 survived; 2 died within 2 hrs of first signs']],
        col_widths=[4.5, 12.5])

    add_h1(doc, '4. Electrocution Terminology & Pathology')
    add_table(doc,
        ['Term', 'Definition', 'PM Significance'],
        [['Electrocution', 'Death caused by electrical current — any voltage', 'Confirmed by char marks + scene evidence + cardiac arrest'],
         ['Joule heating', 'Heat generated in tissue by current flow', 'Causes muscle necrosis along current path'],
         ['Ventricular fibrillation', 'Cardiac arrhythmia caused by AC current at 50 Hz', 'Primary cause of death — AC current more dangerous than DC'],
         ['Flash burns', 'Burns from electrical arc discharge — no direct contact needed', 'Superficial burns without entry/exit wounds'],
         ['Step potential', 'Voltage gradient on ground surface near high-voltage line', 'Multiple animals electrocuted without touching line'],
         ['Touch potential', 'Voltage between contact point and distant ground', 'Single animal — grabs or leans on energised object']],
        col_widths=[3.5, 5, 8.5])

    add_h1(doc, '5. Pyometra in Female Elephants')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Definition', 'Accumulation of pus in the uterus — life-threatening if untreated'],
         ['Affected group', 'Captive adult cows; long inter-calving intervals; hormonal manipulation'],
         ['Common organisms', 'E. coli, Streptococcus, Staphylococcus, Pseudomonas, Clostridium spp.'],
         ['Predisposing factors', 'Delayed cycling, hormonal imbalance, retained foetal membranes, uterine trauma, repeat failed mating'],
         ['Clinical signs', 'Purulent vaginal discharge, abdominal distension, anorexia, systemic fever, weight loss'],
         ['PM Findings', 'Uterus massively distended with foul-smelling purulent exudate; uterine wall thickened, friable; adhesions'],
         ['Histopathology', 'Uterine wall: suppurative endometritis, glandular destruction, bacterial colonies, oedema'],
         ['Treatment (live animal)', 'Oxytocin (drainage), PGF2α (luteal regression), broad-spectrum antibiotics; surgical drainage in severe cases']],
        col_widths=[4, 13])

    add_h1(doc, '6. Hyperthermia')
    add_body(doc,
        'Elephants are homeotherms but have limited thermoregulatory capacity due to their '
        'large body mass-to-surface area ratio. They cannot sweat like humans — primary heat '
        'dissipation is through ear vasodilation, bathing, and mud-wallowing. '
        'Captive elephants with restricted access to water and shade are at highest risk.')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Normal rectal temperature', '35.5–37.5°C'],
         ['Hyperthermia threshold', '>38.5°C (clinical concern); >39.5°C (danger)'],
         ['Predisposing factors', 'Restricted water access, direct sun exposure, transport without ventilation, exertion in heat, musth'],
         ['Mechanism', 'Core temperature rises → cerebral oedema → neuronal dysfunction → seizures → death'],
         ['Clinical signs', 'Temporal gland discharge, frantic ear-flapping, trunk spraying, ataxia, collapse, convulsions'],
         ['Gross PM findings', 'Cerebral oedema, petechiae, congestion of all organs; rapid decomposition due to high body temp'],
         ['Cooling protocols', 'Shade immediately; continuous cold water (IV + external); ice packs on head/ears/legs; monitoring'],
         ['PM sampling', 'Brain (fixed immediately), vitreous humour (temperature marker), core temp at PM site']],
        col_widths=[4, 13])

    add_h1(doc, '7. Iron Deficiency Anaemia')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Risk group', 'Captive calves on restricted diet; calves born to iron-deficient cows'],
         ['Normal haematocrit', '32–40% (adult); calves may be lower'],
         ['Signs of iron deficiency', 'Pallor of mucosae, weakness, tachycardia, poor growth, pica (eating soil — geophagy)'],
         ['Diagnostic tests', 'CBC: low PCV, Hb, MCV, MCH; serum iron low; TIBC elevated; serum ferritin low'],
         ['PM findings', 'Pale thin watery blood; pale mucosae, muscle; small spleen; hypoplastic bone marrow'],
         ['Treatment', 'Iron dextran IM (10–20 mg/kg); dietary supplementation; mineral licks; treat underlying GI parasites'],
         ['Geophagy significance', 'Normal behaviour for mineral supplementation; should not be suppressed in captive animals']],
        col_widths=[4, 13])

    add_h1(doc, '8. Quick Reference — Non-Infectious Conditions Summary')
    add_table(doc,
        ['Condition', 'Key PM Finding', 'Key Sample', 'Diagnosis Method'],
        [['CPA Toxicosis', 'Pale liver, haemorrhagic enteritis', 'Stomach contents, liver', 'LC-MS for CPA'],
         ['HCN Poisoning', 'Cherry-red blood, bitter almond smell', 'Stomach contents (fresh)', 'Conway microdiffusion'],
         ['Cyanobacterial toxin', 'Liver necrosis, GI haemorrhage', 'Water, liver', 'ELISA/LC-MS microcystin'],
         ['Electrocution', 'Char marks, cardiac arrest', 'Skin at marks; heart', 'Gross PM + scene evidence'],
         ['Pyometra', 'Pus-filled uterus, adhesions', 'Uterine pus', 'Culture + sensitivity'],
         ['Hyperthermia', 'Cerebral oedema, congestion', 'Brain, vitreous', 'Histopath; temp at PM'],
         ['Iron deficiency', 'Pale watery blood, pale bone marrow', 'EDTA blood, bone marrow', 'CBC, serum iron, ferritin'],
         ['Toxic plants', 'Liver/GI/cardiac changes (variable)', 'Stomach contents, liver', 'LC-MS; botanical ID']],
        col_widths=[4, 4.5, 3.5, 5])

    save(doc, 'Workshop_Chapter6_NonInfectious_Pathology_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 7 — Postmortem Examination
# ═══════════════════════════════════════════════════════════════════════════════

def build_chapter7():
    doc = new_doc('Chapter 7 — Postmortem Examination of the Asian Elephant')
    add_chapter_header(doc, '7',
        'Postmortem Examination of the Asian Elephant',
        'Principles, Procedure, Documentation & Differential Diagnosis',
        'Prof. Dr. A. B. Shrivastav  |  NDVSU, Jabalpur')

    add_keybox(doc,
        '"The carcass never tells a lie — but you must know how to ask the right questions."'
        '  — Dr. R. K. Satpati, Wildlife Institute of India')

    add_h1(doc, '1. Introduction & Definitions')
    add_body(doc,
        'Postmortem (PM) examination — necropsy — is the systematic, methodical '
        'examination of a dead animal to determine the cause of death, manner of death, '
        'and contributing factors. In wildlife forensics, the necropsy report may be the '
        'primary evidence in legal proceedings.')
    add_table(doc,
        ['Term', 'Definition'],
        [['Necropsy', 'Postmortem examination of an animal (Gr: nekros = dead, opsis = view)'],
         ['Autopsy', 'Postmortem examination of a human (same methodology — different subject)'],
         ['Cause of Death (CoD)', 'The pathological condition or injury directly responsible for death'],
         ['Manner of Death', 'Natural, accidental, homicidal, suicidal, undetermined'],
         ['Contributing Factor', 'A condition that worsened the outcome but was not the direct cause'],
         ['Time Since Death (TSD)', 'Estimated interval since death — based on PM changes, temperature, entomology'],
         ['Chain of Custody', 'Documented chronological record of sample handling from collection to lab'],
         ['Rigor Mortis', 'Temporary muscle stiffening 2–6 hrs post-death; resolves by 24–36 hrs'],
         ['Livor Mortis', 'Purple discolouration of dependent (lowest) body surfaces due to blood pooling'],
         ['Algor Mortis', 'Body temperature drop post-death (~1°C/hr in still air at 20°C)']],
        col_widths=[4.5, 12.5])

    add_h2(doc, 'Six Key Principles of Elephant Necropsy')
    principles = [
        '1. SPEED: PM within 6 hours of death ideally — tropical climate causes rapid decomposition. Maximum 12 hours.',
        '2. SAFETY: PPE mandatory — gloves (double), N95 mask, eye protection, gown, waterproof boots.',
        '3. SYSTEMATIC: Follow a fixed sequence every time — external → internal (thorax → abdomen → head). Never skip steps.',
        '4. SAMPLING: Collect ALL samples from the master list before organ examination — samples come first, findings second.',
        '5. DOCUMENTATION: Photograph every finding before disturbing. GPS coordinates of site. Written notes in field notebook.',
        '6. CHAIN OF CUSTODY: Label every sample immediately. Fill submission form. Witness signature on all forensic samples.',
    ]
    for p in principles:
        add_bullet(doc, p)
    doc.add_paragraph()

    add_h1(doc, '2. Pre-Necropsy Preparation')
    add_table(doc,
        ['Category', 'Requirements'],
        [['Team', 'Minimum 4 persons: 1 veterinarian (PM lead), 1 assistant (scribing), 1 photographer, 1 sample handler + 2–4 mahouts/field staff for positioning'],
         ['Documentation kit', 'Field notebook, permanent markers, sample labels, GPS device or phone, camera (charged), body measurement tape'],
         ['PPE', 'Double gloves, N95 masks (min. 6 per person), full gown/PPE suit, eye shield/goggles, waterproof boots'],
         ['Instruments', '2 large knives (postmortem knives, sharpened), hand saw or bone saw, rib shears or heavy scissors, spreader, forceps, sample jars'],
         ['Sample supplies', 'EDTA tubes, red-top tubes, sterile zip-locks, NBF jars (pre-filled 10%), VTM tubes, sterile swabs, wide-mouth sterile containers'],
         ['Cold chain', 'Ice box with ice packs (minimum 2 kg ice per case), sealed cold packs; freezer access within 6 hrs preferred'],
         ['Legal documents', 'PM requisition letter, chain of custody forms, official field report template, camera with date/GPS metadata']],
        col_widths=[4, 13])

    add_h1(doc, '3. Post-Mortem Examination — Step-by-Step Workflow')
    add_table(doc,
        ['Step', 'Action', 'Key Observations'],
        [['1. Scene Assessment', 'GPS, photographs of scene, position of body, surrounding environment, evidence (wire, tracks)', 'Note any electric wire, water body, tracks, disturbance, vegetation damage'],
         ['2. External Examination', 'Body condition score; skin; wounds; orifices; sex; age estimate', 'Char marks, trauma, discharge, dehydration, skin lesions — all photographed'],
         ['3. Body Measurements', 'Shoulder height, head length, tusk length/weight, body weight estimate', 'Required for age estimation, sex confirmation, forensic records'],
         ['4. PM Change Assessment', 'Rigor, livor, decomposition stage, bloat, skin slippage', 'Estimate time since death; affects sample viability'],
         ['5. Blood Collection', 'Jugular/cardiac puncture for EDTA + serum tubes before opening', 'Critical — do before any incision'],
         ['6. Skin Incision', 'From jaw to perineum along ventral midline; reflect skin laterally', 'Examine subcutaneous tissue, mammary glands, muscle'],
         ['7. Thoracic Cavity', 'Cut through ribs; note lung position, fluid, adhesions; examine pericardium', 'Assess lungs (drowning), heart (electrocution/EMCV), fluid volumes'],
         ['8. Abdominal Cavity', 'Open from xiphoid to pubis; assess organs in situ before removal', 'Assess liver, spleen, GI tract, reproductive organs, kidney'],
         ['9. Organ Examination', 'Remove and examine each organ systematically; note size, weight, texture, colour', 'Collect fresh + fixed samples from each organ'],
         ['10. Head Examination', 'Remove head; saw calvarium; examine brain; examine oral cavity, teeth', 'Age by molar; brain for rabies/NiV; nasal turbinates for herpes'],
         ['11. Molar Age Estimation', 'Identify which molar set is in wear; count laminae', 'Record which M (M1–M6) is present in each jaw quadrant'],
         ['12. Lymph Node Survey', 'Sample superficial + deep lymph nodes systematically', 'Enlargement, abscessation, necrosis — key TB/EEHV indicator']],
        col_widths=[3, 5.5, 8.5])

    add_h1(doc, '4. Post-Mortem Changes — Time Estimation')
    add_table(doc,
        ['PM Change', 'Onset', 'Duration', 'Use for TSD Estimation'],
        [['Algor mortis (body cooling)', 'Immediate — 1°C/hr in still air at 20°C', 'Until ambient temp reached', 'Core temp at PM vs ambient → estimate hrs post-death'],
         ['Rigor mortis', '2–6 hrs post-death (faster in heat)', 'Complete by 12 hrs; resolves by 24–48 hrs', 'Present = <24 hrs; absent after resolution = >48 hrs or very early'],
         ['Livor mortis (lividity)', '1–3 hrs post-death', 'Fixed by 8–12 hrs', 'Blanches = <8 hrs; fixed = >12 hrs; position of body tells repositioning']],
        col_widths=[4, 4, 3.5, 5.5])

    add_h1(doc, '5. Molar Age Estimation Guide')
    add_table(doc,
        ['Molar Set', 'Age in Wear', 'Laminae Count', 'Field Identification'],
        [['M1 (dp2)', '0–2 years', '3–4', 'Tiny — often shed before examination; calf only'],
         ['M2 (dp3)', '2–4 years', '4', 'Small — seen in lower jaw of young calves'],
         ['M3 (dp4)', '4–10 years', '5–6', 'Medium — main tooth in juveniles; distinct front edge worn'],
         ['M4 (M1)', '8–22 years', '7–8', 'Sub-adult to young adult — most common in CG casualties'],
         ['M5 (M2)', '15–45 years', '9–10', 'Adult elephant — large, wide; deeply worn ridges'],
         ['M6 (M3)', '30+ years', '12–14', 'Old elephant — last set; wear indicates remaining lifespan']],
        col_widths=[2.5, 2.5, 3, 9])

    add_h1(doc, '6. Instruments & Equipment List')
    add_table(doc,
        ['Instrument', 'Use', 'Quantity'],
        [['Postmortem knife (large)', 'Primary incisions, organ sectioning', '2 (one spare)'],
         ['Butcher knife / boning knife', 'Muscle dissection, skinning', '2'],
         ['Hand saw or reciprocating bone saw', 'Rib cuts, calvarium opening', '1'],
         ['Rib shears / heavy scissors', 'Costal cartilage, pericardium', '1 pair'],
         ['Enterotome (intestinal scissors)', 'Opening intestines and stomach', '1'],
         ['Brain knife', 'Sectioning brain', '1'],
         ['Forceps (toothed & plain)', 'Tissue handling, lymph node dissection', '2 pairs each'],
         ['Spreader / retractor', 'Holding cavity open during examination', '2'],
         ['Steel ruler/measuring tape', 'Body measurements, wound dimensions', '1 each'],
         ['Scale (spring balance)', 'Organ weights', '1 (10 kg capacity)'],
         ['Hacksaw', 'Tusk/bone cutting', '1'],
         ['Grinding stone', 'Sharpening knives in field', '1'],
         ['Rope & pulleys', 'Positioning carcass — essential for elephant size', '10 m rope × 4'],
         ['Tarpaulin sheet', 'Working surface under carcass; sample table', '2 (4 × 4 m)'],
         ['Generator + lights', 'If PM after sunset', 'As available'],
         ['Chainsaw/axe', 'Carcass disposal after PM', 'As required']],
        col_widths=[5, 7.5, 4.5])

    add_h1(doc, '7. External Examination Checklist (11 Points)')
    add_table(doc,
        ['#', 'Parameter', 'What to Look For / Record'],
        [['1', 'Body Condition', 'Emaciated / Poor / Fair / Good / Obese; muscle wastage'],
         ['2', 'Sex Identification', 'External genitalia; inter-mammary distance (females); tusk presence/absence'],
         ['3', 'Age Estimation', 'Body size class; molar palpation; shoulder height — correlated to age chart'],
         ['4', 'Skin Condition', 'Wounds, char marks, ulcers, pox lesions, depigmentation patterns'],
         ['5', 'Head & Face', 'Eyes (corneal clarity), temporal gland swelling, depigmentation pattern on trunk/face'],
         ['6', 'Trunk Examination', 'Discharge (nasal, oral) — character, colour, smell; swab for culture/PCR'],
         ['7', 'Feet', 'Sole condition, nail cracks, arthritis, pad injury; entry/exit wounds for electrocution'],
         ['8', 'Tail', 'Length, condition; note if cut (poaching indicator)'],
         ['9', 'Tusk', 'Present/absent; length, weight, tip condition; saw cuts (poaching); damage pattern'],
         ['10', 'Genitalia', 'Female: lactation, pregnancy signs, vulval discharge; Male: scrotal abnormalities, musth'],
         ['11', 'Body Orifices', 'Nasal: discharge / froth / blood. Oral: ulcers, abnormal wear. Anus: haemorrhage, odour, content colour']],
        col_widths=[0.8, 3.5, 12.7])

    add_h1(doc, '8. Lymph Node Survey')
    add_h2(doc, 'Superficial Lymph Nodes')
    add_table(doc,
        ['Node', 'Location', 'Drains (Region)'],
        [['Parotid LN', 'Ventral to ear, lateral to masseter', 'Head, ear, parotid gland'],
         ['Submandibular LN', 'Under jaw, near salivary gland', 'Lower jaw, tongue, floor of mouth'],
         ['Prescapular LN', 'Cranial to shoulder joint', 'Forelimb, shoulder, neck'],
         ['Inguinal LN', 'Groin/medial thigh', 'Hindlimb, mammary gland (female), prepuce (male)'],
         ['Popliteal LN', 'Caudal to stifle joint', 'Distal hindlimb, foot']],
        col_widths=[3.5, 5.5, 8])
    add_h2(doc, 'Deep Lymph Nodes')
    add_table(doc,
        ['Node', 'Location', 'Clinical Significance'],
        [['Mediastinal LN (cranial)', 'Thoracic cavity, near tracheal bifurcation', 'TB (most enlarged here); EEHV; lung pathology'],
         ['Mesenteric LN', 'Root of mesentery — GI tract', 'Salmonella, Clostridium, intestinal TB, Johnes disease'],
         ['Hepatic/Portal LN', 'Hepatic hilum, near portal vein', 'Liver disease, TB, EEHV haemorrhagic disease']],
        col_widths=[4, 5, 8])

    add_h1(doc, '9. EEHV Histopathological Features')
    add_body(doc,
        'Elephant Endotheliotropic Herpesvirus (EEHV) causes haemorrhagic disease primarily '
        'in calves 1–8 years. Histopathology is essential for confirmation when PCR '
        'is unavailable or negative in decomposed samples.')
    add_table(doc,
        ['Organ', 'Histopathological Finding'],
        [['Blood vessel endothelium', 'Intranuclear herpesviral inclusion bodies (Cowdry type A) in endothelial cells — PATHOGNOMONIC'],
         ['Heart', 'Myocarditis; endothelial inclusions in cardiac vessels; myofibre degeneration'],
         ['Tongue/mouth', 'Ulceration; endothelial inclusions in submucosal vessels; haemorrhage'],
         ['Liver', 'Hepatocyte degeneration; periportal haemorrhage; endothelial inclusions in sinusoids'],
         ['Spleen', 'Lymphoid depletion; haemorrhage; endothelial inclusions'],
         ['Lung', 'Oedema; haemorrhage; endothelial inclusions in alveolar vessels'],
         ['Lymph nodes', 'Haemorrhage; lymphoid depletion; fibrinous exudate']],
        col_widths=[4, 13])

    add_h1(doc, '10. Differential Diagnosis — Key Elephant Deaths')
    add_table(doc,
        ['Disease/Condition', 'Key Distinguishing PM Finding', 'Confirmatory Test'],
        [['EEHV haemorrhagic disease', 'Intranuclear inclusions in endothelium; generalised haemorrhage; calf 1–8 yrs', 'qPCR (blood, spleen); IHC for EEHV antigen'],
         ['Tuberculosis (TB)', 'Granulomata in lungs/LN; caseous necrosis; Langhans cells in histo', 'Trunk wash culture (MGIT); PCR; ELISA (ElephantTB STAT-PAK)'],
         ['Anthrax', 'Peracute death; bloody orifice discharge; no rigor mortis; DO NOT OPEN', 'McFadyean stain (blood smear); FAT; PCR — call BSL-3 support'],
         ['CPA Toxicosis', 'Pale friable liver; haemorrhagic enteritis; no specific inclusions; millet in stomach', 'LC-MS for CPA in stomach contents and liver'],
         ['Electrocution', 'Char marks at entry/exit; cardiac arrest; no organ-specific pathology', 'Scene investigation + gross PM + wire/equipment analysis'],
         ['Drowning', 'Waterlogged lungs; frothy tracheal discharge; water in GI; no char marks', 'Diatom test (bone marrow); exclude other causes'],
         ['Rabies', 'Behavioural changes ante-mortem; aggression; carcass found in forest', 'Seller\'s stain (brain smear); FAT; PCR on brain'],
         ['HCN Poisoning', 'Cherry-red blood; bitter almond smell; peracute death', 'Conway microdiffusion (fresh stomach contents) — run immediately']],
        col_widths=[4, 6.5, 6.5])

    add_h2(doc, 'Panna Tiger Reserve — Rabies Case (Reference Case)')
    add_table(doc,
        ['Parameter', 'Details'],
        [['Location', 'Panna Tiger Reserve, Madhya Pradesh'],
         ['Clinical signs', 'Progressive behavioural change: restlessness → aggression → inability to swallow → paralysis → death'],
         ['PM findings', 'No specific gross lesion; mild cerebral congestion'],
         ['Diagnosis', 'Seller\'s stain: Negri bodies in Purkinje cells and pyramidal neurons of hippocampus'],
         ['FAT', 'Positive for Rabies antigen'],
         ['Significance', 'Demonstrates that wildlife rabies occurs in elephants — usually transmitted via bite from infected dog or wild carnivore'],
         ['PPE Note', 'FULL PPE for brain examination when rabies suspected — zoonotic and fatal']],
        col_widths=[4, 13])

    add_h1(doc, '11. PM Report — Documentation Checklist')
    add_table(doc,
        ['Section', 'Items to Include'],
        [['Case Identification', 'Case No., Date, Time, GPS of site, Forest Division, Range, Beat'],
         ['Animal Details', 'Species, Sex, Age class, Body weight estimate, Tusk status, ID marks (deformities, notches)'],
         ['History', 'Date/time found dead, last seen alive, reporting person, circumstances, recent herd activity'],
         ['External Examination', 'All 11-point checklist items; wound measurements; photographs with scale'],
         ['PM Changes', 'Rigor/livor/algor status; decomposition stage; estimated time since death'],
         ['Thoracic Cavity', 'Fluid volumes; lung (left/right separately); heart; pericardium; mediastinal LN'],
         ['Abdominal Cavity', 'Liver; spleen; kidneys; GI tract (each segment); reproductive organs; mesenteric LN'],
         ['Head', 'Brain; molar teeth (M1–M6 — which in wear, which quadrants); nasal turbinates; tongue; eyes'],
         ['Samples Collected', 'Complete list with container type, volume, preservation method, and cold chain status'],
         ['Provisional CoD', 'Based on gross PM — to be confirmed by laboratory'],
         ['Recommendations', 'Any immediate management action required; environmental investigation needed'],
         ['Signatures', 'Lead veterinarian, assisting staff, forest officer present, date and official stamp']],
        col_widths=[4, 13])

    add_keybox(doc,
        '"Doctors who perform necropsies gain wisdom that no textbook can teach. '
        'The postmortem examination is the final clinical act — performed for the living, not the dead."'
        '  — Dr. A. B. Shrivastav, NDVSU Jabalpur (2014)')

    save(doc, 'Workshop_Chapter7_Postmortem_Examination_2026.docx')


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('Generating all chapters as Word (.docx) files...\n')
    build_chapter1()
    build_chapter2()
    build_chapter3()
    build_chapter4()
    build_chapter5()
    build_chapter6()
    build_chapter7()
    print('\nAll 7 chapters generated successfully.')

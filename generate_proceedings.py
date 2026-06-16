#!/usr/bin/env python3
"""
Generate complete Workshop Proceedings as a single book:
  - Workshop_Proceedings_2026.pdf  (merged PDF with title page)
  - Workshop_Proceedings_2026.docx (merged Word document)
"""

import os
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas as rl_canvas
from pdfrw import PdfReader, PdfWriter, PageMerge

from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docxcompose.composer import Composer

DIR = '/home/user/Workshop-on-Conference'
PW, PH = A4

# ── Colours ───────────────────────────────────────────────────────────────────
C_DARK  = HexColor('#1B4332')
C_MED   = HexColor('#2D6A4F')
C_LIGHT = HexColor('#52B788')
C_TINT  = HexColor('#D8F3DC')
C_BG    = HexColor('#BF4B1A')   # terracotta (matches overview style)
C_NAVY  = HexColor('#1A2840')
C_GOLD  = HexColor('#C9A84C')

# ═══════════════════════════════════════════════════════════════════════════════
# PDF — Title page + merger
# ═══════════════════════════════════════════════════════════════════════════════

def make_title_page(path):
    """Draw a standalone title page PDF."""
    c = rl_canvas.Canvas(path, pagesize=A4)

    # Background
    c.setFillColor(C_BG)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)

    # White card
    margin = 24
    c.setFillColor(white)
    c.roundRect(margin, margin, PW - 2*margin, PH - 2*margin, 14, fill=1, stroke=0)

    # Top dark green stripe
    c.setFillColor(C_DARK)
    c.roundRect(margin, PH - margin - 80, PW - 2*margin, 80, 14, fill=1, stroke=0)
    c.rect(margin, PH - margin - 80, PW - 2*margin, 40, fill=1, stroke=0)

    # Proceedings label
    c.setFillColor(C_LIGHT)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(PW/2, PH - margin - 28, 'WORKSHOP PROCEEDINGS')

    # Gold divider
    c.setFillColor(C_GOLD)
    c.rect(margin + 40, PH - margin - 50, PW - 2*margin - 80, 2, fill=1, stroke=0)

    # Main title
    c.setFillColor(C_DARK)
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(PW/2, PH - margin - 85, 'Workshop on Essentials for')
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(PW/2, PH - margin - 110, 'Mortality Investigation of')
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(PW/2, PH - margin - 135, 'Asian Elephant')

    # Subtitle underline
    c.setFillColor(C_LIGHT)
    c.rect(PW/2 - 130, PH - margin - 148, 260, 2, fill=1, stroke=0)

    # Elephant silhouette (simple geometric)
    ex, ey = PW/2, PH/2 + 30
    c.setFillColor(HexColor('#E8F5EC'))
    # Body ellipse
    c.ellipse(ex - 90, ey - 50, ex + 90, ey + 50, fill=1, stroke=0)
    # Head
    c.ellipse(ex + 55, ey + 10, ex + 130, ey + 70, fill=1, stroke=0)
    # Ear
    c.ellipse(ex + 78, ey + 15, ex + 155, ey + 90, fill=1, stroke=0)
    # Trunk (vertical rectangle + curve area)
    c.roundRect(ex + 108, ey - 30, 14, 60, 6, fill=1, stroke=0)
    # Legs
    for lx in [ex - 55, ex - 20, ex + 15, ex + 50]:
        c.roundRect(lx, ey - 88, 18, 42, 4, fill=1, stroke=0)

    c.setFillColor(C_MED)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PW/2, PH/2 - 60, '◆   Chhattisgarh Forest Department   ◆')

    # Meta boxes row
    bw = 110
    bh = 44
    bys = [
        ('Date', '5–6 June 2026'),
        ('Venue', 'Raigarh, CG'),
        ('Participants', '84 Officers'),
        ('Chapters', '8 Modules'),
    ]
    total_bw = len(bys) * bw + (len(bys)-1) * 10
    bx_start = (PW - total_bw) / 2
    by = PH/2 - 120
    for i, (lbl, val) in enumerate(bys):
        bx = bx_start + i * (bw + 10)
        c.setFillColor(C_TINT)
        c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=0)
        c.setStrokeColor(C_LIGHT)
        c.setLineWidth(0.8)
        c.roundRect(bx, by, bw, bh, 6, fill=0, stroke=1)
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 13)
        c.drawCentredString(bx + bw/2, by + 24, val)
        c.setFont('Helvetica', 7.5)
        c.setFillColor(HexColor('#555555'))
        c.drawCentredString(bx + bw/2, by + 10, lbl)

    # Organised by block
    org_y = by - 40
    c.setFillColor(C_DARK)
    c.roundRect(margin + 30, org_y - 10, PW - 2*margin - 60, 34, 6, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PW/2, org_y + 13, 'Organised by: Chhattisgarh Forest Department')
    c.setFont('Helvetica', 8)
    c.drawCentredString(PW/2, org_y + 2,
        'Technical Support: WII Dehradun  ·  Lab Partners: ICAR-IVRI & NDVSU Jabalpur')

    # Contents list
    cy = org_y - 30
    c.setFillColor(C_MED)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(PW/2, cy, 'CONTENTS')
    cy -= 14

    chapters = [
        ('Overview', 'Workshop Overview & Inaugural Proceedings'),
        ('Chapter 1', 'Elephant Mortality Analysis in Chhattisgarh (2021–2026)'),
        ('Chapter 2', 'Biological & Anatomical Aspects of the Asian Elephant'),
        ('Chapter 3', 'Infectious Diseases of Asian Elephants'),
        ('Chapter 4', 'Biological Sample Collection for Wildlife Disease Diagnosis'),
        ('Chapter 5', 'Non-Infectious Diseases in Asian Elephants'),
        ('Chapter 6', 'Non-Infectious Pathology in Asian Elephants'),
        ('Chapter 7', 'Postmortem Examination of the Asian Elephant'),
    ]
    for tag, title in chapters:
        c.setFillColor(C_MED)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(margin + 36, cy, tag)
        c.setFillColor(HexColor('#222222'))
        c.setFont('Helvetica', 8)
        c.drawString(margin + 36 + 70, cy, title)
        cy -= 12

    # Footer
    c.setFillColor(C_DARK)
    c.rect(margin, margin, PW - 2*margin, 26, fill=1, stroke=0)
    c.roundRect(margin, margin, PW - 2*margin, 26, 14, fill=0, stroke=0)
    c.setFillColor(C_TINT)
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(PW/2, margin + 9,
        'Department of Forest & Climate Change, Government of Chhattisgarh')

    c.showPage()
    c.save()
    print(f'  ✓  Title page generated')


def build_pdf():
    title_path = os.path.join(DIR, '_title_page_tmp.pdf')
    make_title_page(title_path)

    files = [
        title_path,
        os.path.join(DIR, 'Workshop_Overview_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter1_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter2_Anatomy_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter3_Infectious_Diseases_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter4_Sampling_Protocols_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter5_NonInfectious_Diseases_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter6_NonInfectious_Pathology_2026.pdf'),
        os.path.join(DIR, 'Workshop_Chapter7_Postmortem_Examination_2026.pdf'),
    ]

    writer = PdfWriter()
    total_pages = 0
    for fpath in files:
        if not os.path.exists(fpath):
            print(f'  ⚠  Missing: {fpath} — skipping')
            continue
        reader = PdfReader(fpath)
        writer.addpages(reader.pages)
        total_pages += len(reader.pages)

    out = os.path.join(DIR, 'Workshop_Proceedings_2026.pdf')
    writer.write(out)
    os.remove(title_path)

    size_kb = os.path.getsize(out) // 1024
    print(f'  ✓  Workshop_Proceedings_2026.pdf  ({total_pages} pages, {size_kb} KB)')


# ═══════════════════════════════════════════════════════════════════════════════
# DOCX — Title page + docxcompose merge
# ═══════════════════════════════════════════════════════════════════════════════

DARK_RGB   = RGBColor(0x1B, 0x43, 0x32)
MED_RGB    = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT_RGB  = RGBColor(0x52, 0xB7, 0x88)
TINT_RGB   = RGBColor(0xD8, 0xF3, 0xDC)
WHITE_RGB  = RGBColor(0xFF, 0xFF, 0xFF)
GOLD_RGB   = RGBColor(0xC9, 0xA8, 0x4C)
NAVY_RGB   = RGBColor(0x1A, 0x2E, 0x4A)
MUTED_RGB  = RGBColor(0x55, 0x55, 0x55)


def shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(__import__('docx.enum.text', fromlist=['WD_BREAK']).WD_BREAK.PAGE)


def build_title_docx():
    """Create title page + TOC as a standalone Word doc."""
    doc = Document()
    sec = doc.sections[0]
    sec.page_width   = Cm(21)
    sec.page_height  = Cm(29.7)
    sec.left_margin  = sec.right_margin  = Cm(2.0)
    sec.top_margin   = sec.bottom_margin = Cm(1.8)

    # ── Title page ─────────────────────────────────────────────────────────────
    # Full-width dark green banner
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]
    shade_cell(cell, '1B4332')
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(12)

    r0 = p.add_run('WORKSHOP PROCEEDINGS')
    r0.font.name = 'Calibri'
    r0.font.size = Pt(9)
    r0.font.bold = True
    r0.font.color.rgb = LIGHT_RGB
    p.add_run('\n')

    r1 = p.add_run('Workshop on Essentials for')
    r1.font.name = 'Calibri'
    r1.font.size = Pt(22)
    r1.font.bold = True
    r1.font.color.rgb = WHITE_RGB
    p.add_run('\n')

    r2 = p.add_run('Mortality Investigation of Asian Elephant')
    r2.font.name = 'Calibri'
    r2.font.size = Pt(22)
    r2.font.bold = True
    r2.font.color.rgb = WHITE_RGB

    doc.add_paragraph()

    # Event details table
    dtbl = doc.add_table(rows=1, cols=4)
    dtbl.style = 'Table Grid'
    details = [
        ('Date', '5–6 June 2026'),
        ('Venue', 'Raigarh, Chhattisgarh'),
        ('Participants', '84 Officers'),
        ('Chapters', '8 Modules'),
    ]
    for i, (lbl, val) in enumerate(details):
        c2 = dtbl.rows[0].cells[i]
        shade_cell(c2, 'D8F3DC')
        pp = c2.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.paragraph_format.space_before = Pt(6)
        pp.paragraph_format.space_after  = Pt(6)
        rv = pp.add_run(val + '\n')
        rv.font.name = 'Calibri'
        rv.font.size = Pt(14)
        rv.font.bold = True
        rv.font.color.rgb = DARK_RGB
        rl = pp.add_run(lbl)
        rl.font.name = 'Calibri'
        rl.font.size = Pt(8)
        rl.font.color.rgb = MUTED_RGB
    doc.add_paragraph()

    # Organised by
    org_tbl = doc.add_table(rows=1, cols=1)
    org_tbl.style = 'Table Grid'
    org_cell = org_tbl.rows[0].cells[0]
    shade_cell(org_cell, '1B4332')
    op = org_cell.paragraphs[0]
    op.alignment = WD_ALIGN_PARAGRAPH.CENTER
    op.paragraph_format.space_before = Pt(6)
    op.paragraph_format.space_after  = Pt(6)
    or1 = op.add_run('Organised by: Chhattisgarh Forest Department\n')
    or1.font.name = 'Calibri'
    or1.font.size = Pt(10)
    or1.font.bold = True
    or1.font.color.rgb = WHITE_RGB
    or2 = op.add_run('Technical Support: WII Dehradun  ·  Laboratory Partners: ICAR-IVRI & NDVSU Jabalpur')
    or2.font.name = 'Calibri'
    or2.font.size = Pt(8.5)
    or2.font.color.rgb = TINT_RGB
    doc.add_paragraph()

    # Contents heading
    ch = doc.add_paragraph()
    ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rch = ch.add_run('TABLE OF CONTENTS')
    rch.font.name = 'Calibri'
    rch.font.size = Pt(11)
    rch.font.bold = True
    rch.font.color.rgb = DARK_RGB

    # TOC table
    toc_tbl = doc.add_table(rows=9, cols=3)
    toc_tbl.style = 'Table Grid'
    toc_entries = [
        ('Overview',   'Workshop Overview & Inaugural Proceedings',                        ''),
        ('Chapter 1',  'Elephant Mortality Analysis in Chhattisgarh (2021–2026)',           'Dr. Parag Nigam (WII)'),
        ('Chapter 2',  'Biological & Anatomical Aspects of the Asian Elephant',             'Dr. Parag Nigam (WII)'),
        ('Chapter 3',  'Infectious Diseases of Asian Elephants',                            'Dr. M. Karikalan (ICAR-IVRI)'),
        ('Chapter 4',  'Biological Sample Collection for Wildlife Disease Diagnosis',       'Dr. M. Karikalan (ICAR-IVRI)'),
        ('Chapter 5',  'Non-Infectious Diseases in Asian Elephants',                        'Dr. Karikalan Mathesh (ICAR-IVRI)'),
        ('Chapter 6',  'Non-Infectious Pathology in Asian Elephants',                       'Prof. Dr. A. B. Shrivastava (NDVSU)'),
        ('Chapter 7',  'Postmortem Examination of the Asian Elephant',                      'Prof. Dr. A. B. Shrivastav (NDVSU)'),
    ]
    # Header
    hdrs = ['Section', 'Title', 'Author / Resource Person']
    hrow = toc_tbl.rows[0].cells
    for i, h in enumerate(hdrs):
        shade_cell(hrow[i], '2D6A4F')
        hp = hrow[i].paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        hp.paragraph_format.space_before = Pt(3)
        hp.paragraph_format.space_after  = Pt(3)
        hr_ = hp.add_run(h)
        hr_.font.name = 'Calibri'
        hr_.font.size = Pt(8.5)
        hr_.font.bold = True
        hr_.font.color.rgb = WHITE_RGB

    for ri, (tag, title, author) in enumerate(toc_entries):
        row = toc_tbl.rows[ri + 1].cells
        bg = 'EAF7EE' if ri % 2 == 1 else 'FFFFFF'
        for ci in range(3):
            shade_cell(row[ci], bg)
        for ci, txt in enumerate([tag, title, author]):
            pp2 = row[ci].paragraphs[0]
            pp2.paragraph_format.space_before = Pt(3)
            pp2.paragraph_format.space_after  = Pt(3)
            r_ = pp2.add_run(txt)
            r_.font.name = 'Calibri'
            r_.font.size = Pt(8.5)
            r_.font.bold = (ci == 0)
            r_.font.color.rgb = DARK_RGB if ci == 0 else RGBColor(0x1A, 0x1A, 0x1A)

    # Set column widths
    for row in toc_tbl.rows:
        row.cells[0].width = Cm(3)
        row.cells[1].width = Cm(10)
        row.cells[2].width = Cm(4)

    doc.add_paragraph()

    # Quote
    qtbl = doc.add_table(rows=1, cols=1)
    qtbl.style = 'Table Grid'
    qcell = qtbl.rows[0].cells[0]
    shade_cell(qcell, '1A2E4A')
    qp = qcell.paragraphs[0]
    qp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    qp.paragraph_format.space_before = Pt(8)
    qp.paragraph_format.space_after  = Pt(8)
    qr1 = qp.add_run('"The carcass never tells a lie — but you must know how to ask the right questions."\n')
    qr1.font.name = 'Calibri'
    qr1.font.size = Pt(10)
    qr1.font.bold = True
    qr1.font.italic = True
    qr1.font.color.rgb = WHITE_RGB
    qr2 = qp.add_run('— Dr. R. K. Satpati, Wildlife Institute of India')
    qr2.font.name = 'Calibri'
    qr2.font.size = Pt(8.5)
    qr2.font.color.rgb = GOLD_RGB

    # Page break before first chapter
    add_page_break(doc)

    path = os.path.join(DIR, '_title_page_tmp.docx')
    doc.save(path)
    return path


def build_docx():
    title_path = build_title_docx()
    print('  ✓  Title page + TOC generated')

    docx_files = [
        os.path.join(DIR, 'Workshop_Overview_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter1_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter2_Anatomy_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter3_Infectious_Diseases_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter4_Sampling_Protocols_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter5_NonInfectious_Diseases_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter6_NonInfectious_Pathology_2026.docx'),
        os.path.join(DIR, 'Workshop_Chapter7_Postmortem_Examination_2026.docx'),
    ]

    master = Document(title_path)
    composer = Composer(master)

    for fpath in docx_files:
        if not os.path.exists(fpath):
            print(f'  ⚠  Missing: {fpath} — skipping')
            continue
        chapter_doc = Document(fpath)
        composer.append(chapter_doc)

    out = os.path.join(DIR, 'Workshop_Proceedings_2026.docx')
    composer.save(out)
    os.remove(title_path)

    size_kb = os.path.getsize(out) // 1024
    print(f'  ✓  Workshop_Proceedings_2026.docx  ({size_kb} KB)')


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('Building complete proceedings book...\n')
    print('── PDF ──────────────────────────────')
    build_pdf()
    print('\n── Word ─────────────────────────────')
    build_docx()
    print('\nDone.')

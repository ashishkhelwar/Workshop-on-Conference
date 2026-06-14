#!/usr/bin/env python3
"""
Generate Chapter 4: Collection of Biological Materials for Wildlife Disease Diagnosis
Based on notes from Dr. M. Karikalan, ICAR-IVRI
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable
import os

# ── Colour palette ────────────────────────────────────────────────────────────
C_DARK   = HexColor('#1B4332')   # deep forest green — headers, rules
C_MED    = HexColor('#2D6A4F')   # mid green — subheadings, table headers
C_LIGHT  = HexColor('#52B788')   # bright green — accents
C_TINT   = HexColor('#D8F3DC')   # very light green — key boxes, table rows
C_TINT2  = HexColor('#EAF7EE')   # even lighter — alternate table row
C_ORANGE = HexColor('#F4A261')   # warm orange — warning/note boxes
C_ORNG_L = HexColor('#FFF0E6')   # light orange — warning box bg
C_GOLD   = HexColor('#E9C46A')   # gold — tip indicators
C_BODY   = HexColor('#1A1A1A')   # near-black body text
C_MUTED  = HexColor('#555555')   # muted / captions
C_WHITE  = colors.white

PW, PH = A4

OUT = '/home/user/Workshop-on-Conference/Workshop_Chapter4_Sampling_Protocols_2026.pdf'


# ═══════════════════════════════════════════════════════════════════════════════
# Custom Flowables
# ═══════════════════════════════════════════════════════════════════════════════

class ChapterHeader(Flowable):
    """Full-width chapter title banner in forest green."""
    def __init__(self, chapter_num, title, subtitle='', author=''):
        Flowable.__init__(self)
        self.chapter_num = chapter_num
        self.title = title
        self.subtitle = subtitle
        self.author = author

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 110

    def draw(self):
        c = self.canv
        w, h = self.aw, 110
        # Background
        c.setFillColor(C_DARK)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        # Accent strip
        c.setFillColor(C_LIGHT)
        c.rect(0, h - 6, w, 6, fill=1, stroke=0)
        # Chapter tag
        c.setFillColor(C_LIGHT)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(14, h - 22, f'CHAPTER {self.chapter_num}')
        # Title
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 18)
        c.drawString(14, h - 48, self.title)
        # Subtitle
        if self.subtitle:
            c.setFillColor(HexColor('#A8D5B5'))
            c.setFont('Helvetica', 10.5)
            c.drawString(14, h - 64, self.subtitle)
        # Author
        if self.author:
            c.setFillColor(HexColor('#88BF9E'))
            c.setFont('Helvetica', 9)
            c.drawString(14, h - 80, self.author)
        # Bottom line
        c.setFillColor(HexColor('#88BF9E'))
        c.setFont('Helvetica', 8.5)
        c.drawString(14, 10,
            'Workshop on Essentials for Mortality Investigation of Asian Elephant  ·  '
            'Chhattisgarh Forest Department  ·  June 2026')


class SectionHeading(Flowable):
    """Dark green section heading with left accent bar."""
    def __init__(self, text, level=1):
        Flowable.__init__(self)
        self.text = text
        self.level = level

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 28 if self.level == 1 else 22

    def draw(self):
        c = self.canv
        h = 28 if self.level == 1 else 22
        if self.level == 1:
            c.setFillColor(C_DARK)
            c.rect(0, 0, self.aw, h, fill=1, stroke=0)
            c.setFillColor(C_LIGHT)
            c.rect(0, 0, 5, h, fill=1, stroke=0)
            c.setFillColor(C_WHITE)
            c.setFont('Helvetica-Bold', 12)
            c.drawString(14, 9, self.text)
        else:
            c.setFillColor(C_MED)
            c.rect(0, h - 4, self.aw, 4, fill=1, stroke=0)
            c.setFillColor(C_MED)
            c.setFont('Helvetica-Bold', 11)
            c.drawString(0, 0, self.text)


class KeyBox(Flowable):
    """Light green shaded key-point or note box."""
    def __init__(self, lines, title=None, width=None, warning=False):
        Flowable.__init__(self)
        self.lines = lines if isinstance(lines, list) else [lines]
        self.title = title
        self._width = width
        self.warning = warning

    def wrap(self, aw, ah):
        self.aw = self._width or aw
        line_h = 13
        self._h = (len(self.lines) * line_h) + (18 if self.title else 0) + 18
        return self.aw, self._h

    def draw(self):
        c = self.canv
        bg = C_ORNG_L if self.warning else C_TINT
        border = C_ORANGE if self.warning else C_LIGHT
        c.setFillColor(bg)
        c.roundRect(0, 0, self.aw, self._h, 4, fill=1, stroke=0)
        c.setStrokeColor(border)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, self.aw, self._h, 4, fill=0, stroke=1)
        c.setFillColor(C_DARK if not self.warning else HexColor('#8B3A00'))
        c.rect(0, 0, 4, self._h, fill=1, stroke=0)
        y = self._h - 13
        if self.title:
            c.setFont('Helvetica-Bold', 9.5)
            c.setFillColor(C_DARK if not self.warning else HexColor('#8B3A00'))
            c.drawString(12, y, self.title)
            y -= 15
        c.setFont('Helvetica', 9)
        c.setFillColor(C_BODY)
        for line in self.lines:
            c.drawString(12, y, line)
            y -= 13


# ═══════════════════════════════════════════════════════════════════════════════
# Style sheet
# ═══════════════════════════════════════════════════════════════════════════════

def make_styles():
    s = getSampleStyleSheet()

    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=10,
        textColor=C_BODY, alignment=TA_JUSTIFY, leading=14.5, spaceAfter=5)

    bold_body = ParagraphStyle('BoldBody', parent=body,
        fontName='Helvetica-Bold')

    sub = ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=10.5,
        textColor=C_MED, spaceBefore=10, spaceAfter=3, leading=14)

    note = ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=9,
        textColor=C_MUTED, leading=13, spaceAfter=4)

    bullet = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9.8,
        textColor=C_BODY, leading=14, leftIndent=14, bulletIndent=0,
        spaceAfter=3, alignment=TA_JUSTIFY)

    cell_hdr = ParagraphStyle('CellHdr', fontName='Helvetica-Bold', fontSize=9,
        textColor=C_WHITE, alignment=TA_CENTER, leading=12)

    cell_body = ParagraphStyle('CellBody', fontName='Helvetica', fontSize=8.8,
        textColor=C_BODY, alignment=TA_LEFT, leading=12)

    cell_bold = ParagraphStyle('CellBold', fontName='Helvetica-Bold', fontSize=8.8,
        textColor=C_DARK, alignment=TA_LEFT, leading=12)

    recipe = ParagraphStyle('Recipe', fontName='Helvetica', fontSize=9,
        textColor=C_BODY, leading=13, leftIndent=8)

    return dict(body=body, bold_body=bold_body, sub=sub, note=note,
                bullet=bullet, cell_hdr=cell_hdr, cell_body=cell_body,
                cell_bold=cell_bold, recipe=recipe)


# ═══════════════════════════════════════════════════════════════════════════════
# Table builder helpers
# ═══════════════════════════════════════════════════════════════════════════════

def make_table(headers, rows, ST, col_widths=None, use_zebra=True):
    """Build a styled table with dark green header."""
    cw = col_widths
    n = len(headers)
    total_w = sum(col_widths) if col_widths else None

    # Header row
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for i, row in enumerate(rows):
        data.append([
            Paragraph(str(cell), ST['cell_bold'] if j == 0 else ST['cell_body'])
            for j, cell in enumerate(row)
        ])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('TEXTCOLOR',  (0, 0), (-1, 0), C_WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 9),
        ('ALIGN',      (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_TINT2]),
        ('GRID',       (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('LINEBELOW',  (0, 0), (-1, 0), 1.2, C_LIGHT),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
    ]
    if use_zebra:
        style.append(('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_TINT2]))
    t.setStyle(TableStyle(style))
    return t


def recipe_table(headers, rows, col_widths, ST):
    """Compact recipe/ingredient table."""
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([Paragraph(str(c), ST['cell_body']) for c in row])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_MED),
        ('TEXTCOLOR',  (0, 0), (-1, 0), C_WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_TINT2]),
        ('GRID',       (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING',   (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 3),
    ]))
    return t


def sp(n=6):
    return Spacer(1, n)


def hr():
    return HRFlowable(width='100%', thickness=0.6,
                      color=HexColor('#CCCCCC'), spaceAfter=4, spaceBefore=4)


def p(text, ST, style='body'):
    return Paragraph(text, ST[style])


def b(text, ST):
    return Paragraph(f'• {text}', ST['bullet'])


def num(n, text, ST):
    return Paragraph(f'<b>{n}.</b> {text}', ST['bullet'])


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE TEMPLATE (header / footer)
# ═══════════════════════════════════════════════════════════════════════════════

def on_page(canvas, doc):
    canvas.saveState()
    # Header rule
    canvas.setStrokeColor(C_DARK)
    canvas.setLineWidth(1.5)
    canvas.line(doc.leftMargin, PH - doc.topMargin + 8,
                PW - doc.rightMargin, PH - doc.topMargin + 8)
    canvas.setFillColor(C_MED)
    canvas.setFont('Helvetica-Bold', 7.5)
    canvas.drawString(doc.leftMargin,
                      PH - doc.topMargin + 11,
                      'Chapter 4: Collection of Biological Materials for Wildlife Disease Diagnosis')
    canvas.drawRightString(PW - doc.rightMargin,
                           PH - doc.topMargin + 11,
                           'Dr. M. Karikalan · ICAR-IVRI')
    # Footer
    canvas.setStrokeColor(HexColor('#CCCCCC'))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, doc.bottomMargin - 6,
                PW - doc.rightMargin, doc.bottomMargin - 6)
    canvas.setFillColor(C_MUTED)
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(doc.leftMargin, doc.bottomMargin - 14,
        'Workshop on Essentials for Mortality Investigation of Asian Elephant  ·  '
        'Chhattisgarh Forest Department  ·  Raigarh  ·  June 2026')
    canvas.drawRightString(PW - doc.rightMargin, doc.bottomMargin - 14,
                           f'Page {doc.page}')
    canvas.restoreState()


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

def build_story(ST):
    story = []
    W = PW - 3.4 * cm   # usable text width ≈ 155mm

    # ── CHAPTER HEADER ────────────────────────────────────────────────────────
    story.append(ChapterHeader(
        '4',
        'Collection of Biological Materials',
        'for Wildlife Disease Diagnosis',
        'Dr. M. Karikalan, Senior Scientist (Veterinary Pathology)  ·  '
        'Centre for Wildlife Conservation, Management & Disease Surveillance  ·  ICAR-IVRI, Bareilly'
    ))
    story.append(sp(14))

    # ── SECTION 1: WHY WE COLLECT ─────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('1.  Why We Collect Biological Materials — The Diagnostic Pipeline'),
        sp(6),
        p('Wildlife disease diagnosis works through several layers of investigation, each '
          'requiring specific biological materials collected at the right time, with the right '
          'preservation method, and dispatched to the appropriate laboratory. Understanding this '
          'diagnostic pipeline is essential before selecting which samples to collect.', ST),
        sp(4),
    ]))

    story.append(p('The diagnostic pipeline encompasses:', ST))
    for line in [
        '<b>Clinical observations</b> of the live or recently dead animal.',
        '<b>General health parameters</b> — invasive (haemato-biochemical profile) and '
        'non-invasive (scat/dung analysis).',
        '<b>Collection of specific biological materials</b> from diseased or dead animals.',
        '<b>Post-mortem (necropsy) examination</b> — gross lesions, histopathology '
        '(including histochemistry and immuno-histochemistry), microbiology (microscopy, '
        'culture, biochemical reactions, serological ID, molecular biology / PCR), '
        'toxicology, and parasitology.',
    ]:
        story.append(b(line, ST))
    story.append(sp(10))

    story.append(KeepTogether([
        SectionHeading('How Disease Shows Up: Gene → Gross', level=2),
        sp(6),
        p('Lesions develop in a sequence from the molecular level outward. Knowing this '
          'hierarchy tells you which diagnostic test detects what — and therefore which '
          'sample to collect and preserve.', ST),
        sp(6),
    ]))

    lesion_table = make_table(
        ['Level', 'What Changes', 'How It Is Detected'],
        [
            ['1. Gene / Molecular',
             'DNA mutation, epigenetic & gene-expression changes, abnormal protein synthesis',
             'Not visible by light microscopy — requires PCR / molecular methods'],
            ['2. Ultrastructural',
             'Mitochondrial swelling, RER dilatation, ribosome detachment, membrane blebbing, chromatin clumping',
             'Electron microscopy only'],
            ['3. Light-Microscopic',
             'Cellular swelling, fatty change, necrosis, apoptosis, inflammation, fibrosis, hyperplasia / dysplasia / neoplasia',
             'Routine histopathology (H&E stain)'],
            ['4. Gross (Macroscopic)',
             'Organ enlargement, tumour mass, ulcer, infarct, haemorrhage, abscess, tissue necrosis',
             'Visible to the naked eye at necropsy'],
        ],
        ST,
        col_widths=[W * 0.20, W * 0.46, W * 0.34],
    )
    story.append(lesion_table)
    story.append(sp(4))
    story.append(KeyBox(
        ['Molecular lesion  →  Ultrastructural lesion  →  Microscopic lesion  →  Gross lesion',
         'Most field investigations start at the gross level — but PCR can detect molecular lesions',
         'before any gross changes appear. Collect samples for BOTH.'],
        title='Key Concept: Lesion Hierarchy',
    ))
    story.append(sp(12))

    # ── SECTION 2: CLINICAL SAMPLES ───────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('2.  Clinical Examination & the Samples It Generates'),
        sp(6),
        p('Common clinical workups include physical examination, haematology, serum biochemistry, '
          'urine examination, faecal examination, biopsy/FNAC, lateral flow assay, X-ray, and '
          'ultrasonography. For each workup, specific biological materials must be collected '
          'correctly to obtain valid results.', ST),
        sp(6),
        p('<b>Clinical samples commonly collected from elephants:</b>', ST),
    ]))
    for line in [
        '<b>Blood in anticoagulant vials</b> — EDTA <i>or</i> heparin (4–5 mL)',
        '<b>Serum</b> in a plain tube (allow to clot, then separate)',
        '<b>Faecal / rectal swabs or dung</b>',
        '<b>Ocular / nasal / oral swabs</b> — with or without Viral Transport Medium (VTM)',
        '<b>Trunk wash fluids</b> — critical for TB and EEHV diagnosis in elephants',
        '<b>Skin scrapings / hair follicles</b>',
        '<b>Any lesions</b> — abscess / wound discharge / tissue biopsy',
    ]:
        story.append(b(line, ST))
    story.append(sp(4))
    story.append(KeyBox(
        ['Always plan around two questions before collecting any sample:',
         '(1) Which laboratory test is intended for this sample?',
         '(2) What biosafety precautions and preservation method are required?'],
        title='Planning Rule',
    ))
    story.append(sp(12))

    # ── SECTION 3: MASTER TABLE ────────────────────────────────────────────────
    story.append(SectionHeading('3.  Master Sample-Collection Table'))
    story.append(sp(6))
    story.append(p('For each sample type: why you collect it, how to preserve / collect it, '
                   'and how to store and transport it to the laboratory.', ST))
    story.append(sp(6))

    master_rows = [
        ['Blood', 'Infections, anaemia, general health',
         '5–6 mL in EDTA vial', '4–8 °C (refrigerated)'],
        ['Blood smear', 'Blood parasites, cell abnormalities',
         'Methanol-fixed blood smear on clean glass slide', 'Wrap in dry soft paper; room temperature'],
        ['Plasma', 'Toxicity & drug-metabolite analysis',
         '5–6 mL in heparin vial; transfer plasma to sterile tubes', '–20 °C / –80 °C, or dry ice'],
        ['Serum', 'Infections (antigen & antibody), health parameters, hormones',
         '5–6 mL in plain serum vial; after clotting transfer serum to sterile tubes',
         '4–8 °C short term; –20/–80 °C long term; dry ice for transport'],
        ['Dung (faeces)', 'Parasites',
         '20 g in sterile vial / zip-lock; worms in 10% formalin or 70% ethanol',
         '4–8 °C; room temperature'],
        ['Dung', 'Digestive disorders',
         '100–200 g in sterile vial', '4–8 °C'],
        ['Dung', 'Hormone analysis',
         '100–200 g in sterile vial / zip-lock', '4–8 °C'],
        ['Urine', 'Kidney function, UTIs',
         '20–30 mL aseptically in sterile vial', '4–8 °C'],
        ['Urine', 'Bacterial infections (e.g. Leptospira)',
         'Drops into a tube with specific bacterial media (e.g. Leptospira media)', '4–8 °C'],
        ['Saliva', 'Bacterial & viral infections',
         '1–2 mL in sterile tubes or sterile swabs', '4–8 °C (bacteria); –20/–80 °C (viruses)'],
        ['Nasal discharge / trunk wash', 'Respiratory disease, esp. TB & EEHV',
         '20–30 mL trunk wash using normal saline in sterile vial',
         '–20/–80 °C for EEHV & TB; 4–8 °C for bacteria'],
        ['Ocular discharge', 'Eye infections',
         'Sterile tube/swab, ± specific media', '4–8 °C (bacteria); –20/–80 °C (viruses)'],
        ['Biopsy tissue / skin swabs', 'Skin & tissue diseases',
         'Swabs aseptically ± transport media; tissues in 10% buffered formalin',
         '4–8 °C for swabs; room temperature for formalin-fixed tissue'],
    ]

    story.append(make_table(
        ['Sample', 'Purpose', 'Preservative / Collection Method', 'Storage & Transport'],
        master_rows, ST,
        col_widths=[W * 0.16, W * 0.22, W * 0.36, W * 0.26],
    ))
    story.append(sp(12))

    # ── SECTION 4: EXAMINATION-SPECIFIC PROTOCOLS ─────────────────────────────
    story.append(SectionHeading('4.  Examination-Specific Protocols'))
    story.append(sp(8))

    # 4a Histopathology
    story.append(KeepTogether([
        SectionHeading('4a.  Histopathological Examination', level=2),
        sp(6),
    ]))
    for line in [
        'Collect tissue <b>soon after death</b>; fix <b>immediately</b> in <b>10% buffered formalin</b>.',
        'Take several pieces — from the <b>centre</b> and from the <b>edge of the lesion</b> at the '
        'junction with healthy tissue (especially critical for large lesions).',
        'Tissue thickness: <b>0.5–1 cm</b>; formalin volume must be at least '
        '<b>10–15× the volume of the tissue</b> (minimum ratio: 10× the tissue amount).',
        'Use a <b>sharp instrument</b> (scalpel, knife, or razor) for a clean, crush-free cut.',
        'Always include <b>lesion tissue plus adjacent healthy tissue</b> in the same block.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(KeepTogether([
        p('<b>Preparing 10% Neutral Buffered Formalin (NBF)</b>', ST),
        sp(4),
        p('Commercial (saturated) formalin ≈ 37–40% formaldehyde. '
          '<b>10% NBF ≈ 4% formaldehyde</b> — this is the standard histopathology fixative. '
          'Tissue : fixative ratio = <b>1 : 10</b> at minimum (e.g. 10 g tissue in 100 mL of 10% NBF).', ST),
        sp(6),
    ]))

    story.append(recipe_table(
        ['Ingredient', 'Quantity'],
        [
            ['Saturated formalin (37–40% formaldehyde)', '100 mL'],
            ['Distilled water', '900 mL'],
            ['Sodium phosphate monobasic (NaH₂PO₄·H₂O)', '4.0 g'],
            ['Sodium phosphate dibasic (Na₂HPO₄)', '6.5 g'],
            ['TOTAL', '1,000 mL (1 litre)'],
        ],
        col_widths=[W * 0.70, W * 0.30], ST=ST,
    ))
    story.append(sp(6))
    story.append(p('<b>Method:</b> Dissolve both phosphate salts fully in ~800 mL distilled water '
                   '→ add 100 mL saturated formalin → top up to 1,000 mL → mix → label '
                   '(name, concentration, date, preparer).', ST))
    story.append(p('<b>Simpler unbuffered version:</b> 100 mL saturated formalin + 900 mL distilled water '
                   '(≈ 4% formaldehyde) — adequate when buffered NBF is unavailable in the field.', ST))
    story.append(sp(4))
    story.append(KeyBox(
        ['Use clean glass or plastic containers.',
         'Dissolve phosphate salts BEFORE adding formalin.',
         'Store at room temperature, tightly capped; label with name, concentration, and date.'],
        title='Preparation Notes',
    ))
    story.append(sp(10))

    # 4b Bacteriology / Virology
    story.append(KeepTogether([
        SectionHeading('4b.  Bacteriological & Virological Examination', level=2),
        sp(6),
    ]))
    for line in [
        'Keep everything <b>free from contamination</b>; use <b>sterile instruments</b> '
        '(scalpels, scissors, syringes, bottles, slides, swabs, polythene bags).',
        '<b>Disinfect skin</b> before the primary incision to prevent surface contamination.',
        'Sear the organ surface (e.g. heart) with a <b>hot iron spatula</b> before sampling '
        'heart blood — to sterilise the surface and eliminate external contamination.',
        'Sample <b>abnormal areas</b> near the <b>edge of affected tissue</b> where live organisms '
        'are most likely still viable.',
        '<b>Appropriate samples:</b> whole blood, serum, CSF, pus, abscess/nodule areas, '
        'intestinal contents (within a tied loop), smears of pus or infected tissue.',
    ]:
        story.append(b(line, ST))
    story.append(sp(6))
    story.append(p('<b>For virology:</b> use 5–10× volume of sterile 50% buffered glycerol, '
                   'chilled PBS (pH 7.4), or Viral Transport Medium (VTM). Other acceptable '
                   'preservatives: RNA Later, 70% ethanol (for PCR-based detection).', ST))
    story.append(p('<b>Transport:</b> bacteria at 4 °C; viruses at 4 °C or on dry ice / frozen.', ST))
    story.append(p('<b>Heart-blood smears:</b> heat-fix for bacteria only; fix in absolute methanol '
                   'for haemoparasites.', ST))
    story.append(sp(10))

    # 4c Parasitology
    story.append(KeepTogether([
        SectionHeading('4c.  Parasitological Examination', level=2),
        sp(6),
    ]))
    for line in [
        '<b>Blood smears</b> on clean glass slides — fix in <b>absolute methanol</b>.',
        '<b>Skin scrapings</b> → preserve in <b>10% KOH</b>.',
        '<b>2 g faeces</b> → <b>70% ethyl alcohol</b> for molecular work; <b>formalin</b> '
        'for morphology-based identification.',
        '<b>Larvae, worms, maggots</b> → <b>70% alcohol</b> or <b>10% formalin</b> '
        '(room temperature).',
        '<b>Protozoan diseases</b> → lymph nodes, blood, and faecal sample in <b>5% formalin</b>.',
    ]:
        story.append(b(line, ST))
    story.append(sp(10))

    # 4d Toxicology
    story.append(KeepTogether([
        SectionHeading('4d.  Toxicological Examination', level=2),
        sp(6),
    ]))
    for line in [
        'Collect <b>≥ 100 g of stomach + intestinal contents</b> and <b>≥ 100 g of liver + kidney</b> '
        'in a glass container with saturated salt solution* or ice.',
        'Also collect <b>environmental samples</b> — baits, feed/fodder, water sources near '
        'the mortality site.',
        '<b>Pack each sample type separately</b> in an ice box; do not mix organ samples with '
        'GI contents or environmental samples.',
        'All containers must be <b>serially numbered, properly labelled, and kept under safe custody</b> '
        '— chain of custody is legally critical in forensic cases.',
    ]:
        story.append(b(line, ST))
    story.append(sp(4))
    story.append(KeyBox(
        ['*Saturated salt solution is NOT used when toxicants must be quantified.',
         'For quantitative toxicology: use sterile containers / zip-locks and deep-freeze at –20 °C.'],
        title='⚠  Important — Qualitative vs. Quantitative Toxicology',
        warning=True,
    ))
    story.append(sp(8))

    # Toxicology sample guide table
    story.append(p('<b>Toxicology sample guide — ante-mortem, post-mortem, and environmental:</b>', ST))
    story.append(sp(6))

    tox_rows = [
        # ante-mortem section
        ['ANTE-MORTEM', '', ''],
        ['Whole blood', '5–10 mL', 'EDTA or heparin vial'],
        ['Serum', '5–10 mL', 'Remove from clot; use trace-element tubes for zinc assays'],
        ['Urine', '25–50 mL', 'Plastic screw-capped tube'],
        ['GI contents', '≥ 100 g each', 'Representative stomach/rumen contents; faeces'],
        ['Hair', '1–2 g', 'Clean zip-lock pouch'],
        ['Milk', '30 mL', 'Sterile collection tube'],
        ['CSF', '1–2 mL', 'Sterile tube; refrigerate immediately'],
        # post-mortem section
        ['POST-MORTEM', '', ''],
        ['Blood/serum/urine (from heart)', 'As ante-mortem', 'As per ante-mortem guidelines above'],
        ['Liver', '100–250 g', 'Plastic container; –20 °C'],
        ['Kidney', '100–250 g', 'Plastic container; –20 °C'],
        ['Brain', 'One half', 'Sagittal cut; plastic; –20 °C'],
        ['Fat', '100 g', 'Foil inside plastic bag; –20 °C'],
        ['GI contents', '≥ 100 g each', 'Representative samples; PACKAGE SEPARATELY from organs'],
        ['Ocular fluid / eyeball', 'As much as possible', 'Aqueous fluid preferred; or whole eyeball'],
        ['Bone', '≥ 100 g', 'For heavy metal analysis'],
        ['Spleen', '100 g', 'As for liver'],
        ['Lung', '100 g', 'As for liver'],
        ['Hair or skin', '—', 'If dermal exposure suspected'],
        # environmental section
        ['ENVIRONMENTAL', '', ''],
        ['Bait / source material', '200 mL or g', 'Clean jar / whirl-pak; label precisely'],
        ['Feed', '≥ 500 g', 'Composite sample per lot/batch'],
        ['Plants', 'Whole or representative', 'Fresh-pressed-dried, or frozen'],
        ['Water', '≥ 1 L', 'Clean glass jar; plastic lid for metals analysis'],
    ]

    # Mark section headers differently
    tox_data = []
    section_rows = []
    for i, row in enumerate(tox_rows):
        if row[1] == '' and row[2] == '':
            # Section header row
            tox_data.append([Paragraph(row[0], ParagraphStyle(
                'sec', fontName='Helvetica-Bold', fontSize=9,
                textColor=C_WHITE, alignment=TA_LEFT)),
                Paragraph('', ST['cell_body']),
                Paragraph('', ST['cell_body'])])
            section_rows.append(i + 1)  # +1 for header row
        else:
            tox_data.append([
                Paragraph(row[0], ST['cell_bold']),
                Paragraph(row[1], ST['cell_body']),
                Paragraph(row[2], ST['cell_body']),
            ])

    tox_hdr = [Paragraph(h, ST['cell_hdr']) for h in
               ['Sample', 'Amount', 'Notes']]
    tox_full = [tox_hdr] + tox_data

    tox_t = Table(tox_full,
                  colWidths=[W * 0.28, W * 0.18, W * 0.54],
                  repeatRows=1)
    section_style = [
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('TEXTCOLOR',  (0, 0), (-1, 0), C_WHITE),
        ('GRID',       (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING',   (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_TINT2]),
    ]
    for r in section_rows:
        section_style += [
            ('BACKGROUND', (0, r), (-1, r), C_MED),
            ('TEXTCOLOR',  (0, r), (-1, r), C_WHITE),
            ('SPAN',       (0, r), (-1, r)),
        ]
    tox_t.setStyle(TableStyle(section_style))
    story.append(tox_t)
    story.append(sp(10))

    # 4e Pregnancy / deficiency
    story.append(KeepTogether([
        SectionHeading('4e.  Pregnancy Diagnosis & Deficiency Diseases', level=2),
        sp(6),
        p('<b>Pregnancy diagnosis</b> in carnivores and elephants: collect '
          '<b>100–150 g of dung</b> plus serum samples for hormone analysis.', ST),
        sp(3),
        p('<b>Deficiency diseases:</b> collect <b>serum samples</b> for macro- and '
          'micro-nutrient assessment.', ST),
        sp(12),
    ]))

    # ── SECTION 5: ELEPHANT-SPECIFIC ──────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('5.  Elephant-Specific Collection Notes'),
        sp(6),
    ]))
    for line in [
        '<b>Blood:</b> drawn from an <b>ear vein</b>; make blood smears immediately and fix in '
        '70% / absolute methanol.',
        '<b>Trunk wash fluid:</b> the elephant draws water into the trunk, washes the inside, '
        'and the used water is expelled into a clean container. This is the critical sample for '
        '<b>TB and EEHV</b> diagnosis and should be stored at –20/–80 °C.',
        '<b>Rectal and oral swabs:</b> collected with sterile swab sticks, placed in zip-lock '
        'pouches (± VTM); store in RNA storage tubes or RNA Later as needed for molecular '
        'diagnosis of EEHV.',
    ]:
        story.append(b(line, ST))
    story.append(sp(4))
    story.append(KeyBox(
        ['Trunk wash is the MOST IMPORTANT sample for EEHV and TB diagnosis in elephants.',
         'Freeze at –80 °C (or on dry ice for transport) if EEHV is suspected.',
         'Do not refrigerate only — EEHV degrades rapidly at 4 °C.'],
        title='Elephant Priority Sample: Trunk Wash',
        warning=True,
    ))
    story.append(sp(12))

    # ── SECTION 6: PACKING & TRANSPORT ────────────────────────────────────────
    story.append(SectionHeading('6.  Packing & Transport'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Preferred Method — Fresh & Frozen Tissue', level=2),
        sp(6),
    ]))
    for i, line in enumerate([
        'Place <b>absorbent material</b> (cat litter or paper towel) in the outer bag to absorb spills.',
        'Tissues → individual, sterile, <b>labelled</b> plastic bottles or whirl-type bags.',
        'Containers + <b>frozen refrigerant packs</b> → heavy plastic bag labelled with contents.',
        'Bag → <b>insulated cooler</b> for shipment.',
        '<b>Specimen submission sheet + all documents</b> → envelope → plastic bag → taped to the '
        '<b>outside</b> of the package.',
    ], 1):
        story.append(num(chr(96 + i), line, ST))
    story.append(sp(10))

    story.append(SectionHeading('10-Step Packing Protocol (Zoonotic / General Samples)', level=2))
    story.append(sp(6))
    for i, line in enumerate([
        'Collect preferred samples with <b>all biosafety precautions</b> (gloves, mask, PPE).',
        '<b>Label</b> specimens (animal name/species, age, gender, specimen ID, date, site).',
        '<b>Parafilm-seal</b> the neck of all vials and containers.',
        'Cover vials with <b>absorbent material (cotton)</b>.',
        'Put tubes/vials in a <b>zip-lock pouch</b> and seal.',
        'Place that pouch inside a <b>plastic container or another zip-lock</b> and seal tightly.',
        'Put the container in a <b>thermocol box surrounded by hard-frozen gel packs</b>.',
        'Put the <b>history form</b> in a separate zip-lock pouch inside the thermocol box.',
        '<b>Close and seal</b> the thermocol box with adhesive tape.',
        'Write the <b>address of the testing laboratory</b> clearly on top of the box.',
    ], 1):
        story.append(num(i, line, ST))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading("Do's and Don'ts", level=2),
        sp(6),
    ]))
    dos_donts = make_table(
        ["Do ✓", "Don't ✗"],
        [
            ['Use clean, properly labelled, leak-proof containers',
             'Submit organs wrapped in plain plastic wrap'],
            ['Use adequate fixative (10× formalin for histopath)',
             'Use dirty or leaking jars / bottles'],
            ['Parafilm-seal vial necks before packing',
             'Under-fix tissue (too little formalin or too thick)'],
            ['Maintain cold chain — refrigerate bacteria; freeze viruses',
             'Ship a whole head or carcass loose in a leaking, poorly packed box'],
            ['Include a complete history form and transport certificate',
             'Mix samples from different organ types in the same container'],
            ['Serial-number and record all forensic/toxicology samples',
             'Break chain of custody for forensic samples'],
        ],
        ST,
        col_widths=[W * 0.50, W * 0.50],
        use_zebra=True,
    )
    story.append(dos_donts)
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Transport Certificate', level=2),
        sp(6),
        p('Include a signed certificate with every shipment stating that the samples are '
          '<b>non-corrosive, non-inflammable, and non-infectious</b>. The certificate must name '
          'the sender, species, sample type, origin, destination laboratory, and preservation '
          'method (ice gel packs / dry ice).', ST),
        sp(4),
        KeyBox(
            ['Sample wording: "Certified that samples of an Asian elephant (blood and trunk secretions)',
             'from [site], [date], are being transported by [scientist name] to ICAR-IVRI, Bareilly,',
             'for health examination; securely packed in sterile containers with frozen gel packs."'],
            title='Example Certificate Wording',
        ),
        sp(12),
    ]))

    # ── SECTION 7: QUICK MASTER REFERENCE ─────────────────────────────────────
    story.append(SectionHeading('7.  Essentials for Biological Sampling — Quick Master Reference'))
    story.append(sp(6))

    qmr_rows = [
        ['Haematology', 'Whole blood', 'EDTA/heparin vial; ice pack 4–8 °C',
         'Gently rotate to mix; do not keep at room temp for long'],
        ['Serum biochemistry', 'Serum', 'Serum tube ± clot activator/gel; 4–8 °C or freeze',
         'Handle gently; AVOID haemolysis'],
        ['Histopathology', 'Tissues — liver, lung, kidney, spleen, heart, stomach, intestine, '
         'brain, lymph node, tumours (normal + abnormal)',
         '10% NBF; leak-proof container; room temperature',
         '0.5–1 cm thick; formalin:tissue ratio ≥ 10:1; include lesion + healthy margin'],
        ['Bacteriology', 'Organs, ocular/rectal/naso- & oro-pharyngeal swabs, heart blood, '
         'exudates, intestinal loops, urine',
         'Refrigerate 4–8 °C; nutrient broth / peptone water / PBS',
         'Avoid contamination; sample type varies by suspected disease'],
        ['Virology', 'Organs (small pieces), swabs, exudates, trunk wash, body fluids',
         'VTM or PBS (pH 7.4); 50% glycerol saline',
         'Refrigerate or dry ice; varies by disease'],
        ['Parasitology — endoparasites', 'Nematodes, trematodes, cestodes',
         '70% alcohol or 5–10% formalin', 'Room temperature'],
        ['Parasitology — ectoparasites', 'External parasites (ticks, mites, flies)',
         '10% KOH or 70% alcohol', 'Room temperature'],
        ['Parasitology — blood', 'Blood parasites',
         'Methanol-fixed blood smear', 'Glass slide at room temperature'],
        ['Toxicology', '~100 g organs, GI contents, blood, fat, water, fodder, feed',
         'Qualitative: saturated salt solution.\nQuantitative: sterile containers; deep freeze –20 °C',
         'Refrigerate for qualitative; freeze for quantitative; separate containers'],
        ['Pregnancy diagnosis', 'Serum, scat/dung (100–200 g)',
         'Plastic container / zip-lock; 4–8 °C', 'Refrigerate'],
        ['Genetic / species ID', 'Tissues, blood, hair follicles, dung, bone marrow',
         'Blood in EDTA; hair in pouches; tissue in 70% ethanol or dry ice',
         'Refrigerate blood; freeze tissue/marrow; hair at room temp in dry pouch'],
    ]

    story.append(make_table(
        ['Diagnostic Activity', 'Specimen', 'Preservative / Container', 'Key Notes'],
        qmr_rows, ST,
        col_widths=[W * 0.18, W * 0.20, W * 0.32, W * 0.30],
    ))
    story.append(sp(12))

    # ── SECTION 8: WHERE TO SEND SAMPLES ──────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('8.  Where to Send Samples'),
        sp(6),
    ]))

    story.append(SectionHeading('Services Available at ICAR-IVRI, Bareilly', level=2))
    story.append(sp(4))
    for line in [
        'PCR diagnosis of important infectious diseases (EEHV, TB, Anthrax, FMD, Rabies, etc.)',
        'Bacterial isolation & antibiotic sensitivity testing (ABST)',
        'Toxicological investigations (qualitative and quantitative)',
        'Parasitology — endo-, ecto-, and haemoprotozoan parasites',
        'Pregnancy diagnosis via dung samples',
        'Necropsy, histopathology, and clinical pathology (blood, urine)',
        'Serodiagnosis of TB, Leptospirosis, and other infections',
    ]:
        story.append(b(line, ST))
    story.append(sp(4))
    story.append(KeyBox(
        ['Contact: In-charge, Centre for Wildlife',
         'ICAR-IVRI, Izatnagar, Bareilly — cwlincharge@gmail.com'],
        title='ICAR-IVRI Contact',
    ))
    story.append(sp(8))

    story.append(SectionHeading('National Referral Laboratories by Specialty', level=2))
    story.append(sp(6))

    ref_rows = [
        ['General wildlife / referral',
         'National Referral Centre on Wildlife Health / Centre for Wildlife, ICAR-IVRI, Izatnagar'],
        ['Exotic viral diseases (e.g. Avian Influenza)',
         'ICAR-NIHSAD, Bhopal'],
        ['Foot and Mouth Disease (FMD)',
         'ICAR-Directorate on FMD, Bhubaneswar; IVRI Bengaluru'],
        ['Toxicology',
         'CSIR-Indian Institute of Toxicology Research (IITR), Lucknow'],
        ['Forensic & molecular identification',
         'Wildlife Institute of India (WII), Dehradun; CSIR-CCMB, Hyderabad'],
        ['Poisoning incl. NSAIDs & avian forensic cases',
         'SACON, Coimbatore (southern campus of WII)'],
        ['Regional diagnostic labs (DADF)',
         'Bangalore (KVAFSU Hebbal), Jalandhar, Pune (Aundh), Guwahati (Khanapara, NE region)'],
        ['State veterinary universities / specialized centres',
         'TANUVAS Chennai; KVASU Pookode Wayanad; OUAT Bhubaneswar; School of Wildlife Forensic & '
         'Health, Jabalpur (NDVSU); ICAR-NIVEDI Bengaluru'],
    ]

    story.append(make_table(
        ['Specialty', 'Recommended Laboratory'],
        ref_rows, ST,
        col_widths=[W * 0.32, W * 0.68],
    ))
    story.append(sp(14))

    # ── KEY TAKEAWAYS ──────────────────────────────────────────────────────────
    story.append(SectionHeading('Key Takeaways'))
    story.append(sp(8))
    story.append(KeyBox([
        '1. Match the sample, preservative, and cold-chain to the intended test — the same',
        '   organ goes into formalin for histopath, VTM for virology, and salt solution / freezer',
        '   for toxicology.',
        '2. Fix histology tissue IMMEDIATELY, thinly (0.5–1 cm), in 10× formalin volume,',
        '   including both lesion and healthy margin.',
        '3. Sterility and anti-contamination technique are critical for all microbiology samples.',
        '4. Label, document, and cold-chain every sample; always include a transport certificate.',
        '5. Toxicology and forensic samples require serial numbering and strict chain of custody.',
        '6. Trunk wash is the priority sample for EEHV and TB in elephants — freeze immediately.',
    ], title='Chapter Summary — Biological Sample Collection'))

    return story


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=1.7 * cm, rightMargin=1.7 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title='Chapter 4: Collection of Biological Materials for Wildlife Disease Diagnosis',
        author='Dr. M. Karikalan, ICAR-IVRI',
    )
    ST = make_styles()
    story = build_story(ST)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    main()

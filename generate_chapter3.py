#!/usr/bin/env python3
"""
Chapter 3: Infectious Diseases of Asian Elephants
Based on: DOCX lecture notes (Dr. M. Karikalan, VBSC SH_1_3) +
          PDF presentation (Infectious Diseases of Asian Elephants, 2026)
"""

import os, io
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable

# ── Colour palette (forest green) ───────────────────────────────────────────
C_DARK   = colors.HexColor('#1B4332')
C_MED    = colors.HexColor('#2D6A4F')
C_LIGHT  = colors.HexColor('#52B788')
C_PALE   = colors.HexColor('#D8F3DC')
C_ACCENT = colors.HexColor('#B7E4C7')
C_TEXT   = colors.HexColor('#1A1A2E')
C_SUB    = colors.HexColor('#40916C')
C_WARN   = colors.HexColor('#D62828')
C_BOX    = colors.HexColor('#F0FFF4')
C_ORANGE = colors.HexColor('#E76F51')

PAGE_W, PAGE_H = A4
MARGIN = 2.2 * cm
INNER_W = PAGE_W - 2 * MARGIN

PDF_PAGES = '/tmp/ch3_pages_j'  # rendered JPEG pages from the source PDF
PDF_EXT = '.jpg'


# ── Styles ───────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()
    def ps(name, **kw):
        return ParagraphStyle(name, parent=base['Normal'], **kw)

    return {
        'ch_label': ps('ch_label', fontSize=14, textColor=C_LIGHT,
                       fontName='Helvetica-Bold', spaceAfter=4, alignment=TA_CENTER),
        'title': ps('title', fontSize=28, textColor=colors.white,
                    fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=6, leading=34),
        'subtitle': ps('subtitle', fontSize=14, textColor=C_ACCENT,
                       fontName='Helvetica', alignment=TA_CENTER, spaceAfter=10, leading=18),
        'author': ps('author', fontSize=11, textColor=C_ACCENT,
                     fontName='Helvetica', alignment=TA_CENTER, spaceAfter=5),
        'section': ps('section', fontSize=16, textColor=C_DARK,
                      fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=8, leading=20),
        'subsec': ps('subsec', fontSize=13, textColor=C_MED,
                     fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6, leading=16),
        'subsubsec': ps('subsubsec', fontSize=11, textColor=C_SUB,
                        fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4, leading=14),
        'body': ps('body', fontSize=10.5, textColor=C_TEXT, fontName='Helvetica',
                   spaceBefore=4, spaceAfter=4, leading=15, alignment=TA_JUSTIFY),
        'bullet': ps('bullet', fontSize=10.5, textColor=C_TEXT, fontName='Helvetica',
                     spaceBefore=2, spaceAfter=2, leading=14, leftIndent=14,
                     firstLineIndent=-8),
        'caption': ps('caption', fontSize=9, textColor=C_MED, fontName='Helvetica-Oblique',
                      alignment=TA_CENTER, spaceBefore=3, spaceAfter=8),
        'key_point': ps('key_point', fontSize=10.5, textColor=C_DARK, fontName='Helvetica-Bold',
                        spaceBefore=3, spaceAfter=3, leading=14, leftIndent=10),
        'warn': ps('warn', fontSize=10.5, textColor=C_WARN, fontName='Helvetica-Bold',
                   spaceBefore=3, spaceAfter=3, leading=14, leftIndent=10),
        'table_hdr': ps('table_hdr', fontSize=9.5, textColor=colors.white,
                        fontName='Helvetica-Bold', alignment=TA_CENTER),
        'table_cell': ps('table_cell', fontSize=9, textColor=C_TEXT,
                         fontName='Helvetica', alignment=TA_LEFT, leading=12),
        'table_cell_c': ps('table_cell_c', fontSize=9, textColor=C_TEXT,
                           fontName='Helvetica', alignment=TA_CENTER, leading=12),
    }


# ── Helper: embed a PDF page as figure ───────────────────────────────────────
def pdf_page_img(page_num, width=INNER_W, caption=None, styles=None):
    """Embed rendered PDF page (1-indexed) with optional caption."""
    fname = os.path.join(PDF_PAGES, f'page_{page_num:02d}{PDF_EXT}')
    if not os.path.exists(fname):
        return []
    try:
        pil = PILImage.open(fname)
        # Rotate 90° clockwise
        pil = pil.transpose(PILImage.Transpose.ROTATE_270)
        pw, ph = pil.size
        aspect = ph / pw
        h = width * aspect
        # Cap height
        if h > 14 * cm:
            h = 14 * cm
            width = h / aspect
        buf = io.BytesIO()
        pil.save(buf, format='JPEG', quality=82)
        buf.seek(0)
        items = [Image(buf, width=width, height=h)]
        if caption and styles:
            items.append(Paragraph(caption, styles['caption']))
        return items
    except Exception:
        return []


def pdf_page_half(page_num, side_width=INNER_W * 0.48, caption=None, styles=None):
    """Return image at half-page width."""
    return pdf_page_img(page_num, width=side_width, caption=caption, styles=styles)


# ── Helper: crop a rendered page ─────────────────────────────────────────────
def pdf_page_crop(page_num, left_frac=0, top_frac=0, right_frac=1, bottom_frac=1,
                  width=INNER_W, caption=None, styles=None):
    """Crop a fraction of a rendered PDF page."""
    fname = os.path.join(PDF_PAGES, f'page_{page_num:02d}{PDF_EXT}')
    if not os.path.exists(fname):
        return []
    try:
        pil = PILImage.open(fname)
        # Crop first, then rotate 90° clockwise
        pw, ph = pil.size
        box = (int(pw * left_frac), int(ph * top_frac),
               int(pw * right_frac), int(ph * bottom_frac))
        cropped = pil.crop(box)
        cropped = cropped.transpose(PILImage.Transpose.ROTATE_270)
        buf = io.BytesIO()
        cropped.save(buf, format='JPEG', quality=82)
        buf.seek(0)
        cw, ch = cropped.size
        aspect = ch / cw
        h = width * aspect
        if h > 12 * cm:
            h = 12 * cm
            width = h / aspect
        items = [Image(buf, width=width, height=h)]
        if caption and styles:
            items.append(Paragraph(caption, styles['caption']))
        return items
    except Exception:
        return []


# ── Helper: two images side by side ──────────────────────────────────────────
def two_images(items_left, items_right, col_width=INNER_W * 0.49):
    """Place two image+caption groups in a two-column table."""
    left_cell = items_left
    right_cell = items_right
    t = Table([[left_cell, right_cell]],
              colWidths=[col_width, col_width])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


# ── Info box ─────────────────────────────────────────────────────────────────
def info_box(lines, styles, bg=None, border=None, title=None):
    bg = bg or C_PALE
    border = border or C_LIGHT
    data = []
    if title:
        data.append([Paragraph(f'<b>{title}</b>', styles['key_point'])])
    for ln in lines:
        data.append([Paragraph(ln, styles['bullet'])])
    t = Table(data, colWidths=[INNER_W - 1.2 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 1.2, border),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [bg, colors.HexColor('#E8F8F0')]),
    ]))
    return t


def warn_box(lines, styles, title='⚠ Important'):
    bg = colors.HexColor('#FFF5F5')
    border = C_WARN
    data = []
    data.append([Paragraph(f'<b>{title}</b>', styles['warn'])])
    for ln in lines:
        data.append([Paragraph(ln, styles['bullet'])])
    t = Table(data, colWidths=[INNER_W - 1.2 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 1.5, border),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


# ── Header / Footer ──────────────────────────────────────────────────────────
CHAPTER_TITLE = 'Chapter 3 — Infectious Diseases of Asian Elephants · Bilaspur 2026'


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header bar
    canvas.setFillColor(C_DARK)
    canvas.rect(0, h - 1.2 * cm, w, 1.2 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(MARGIN, h - 0.75 * cm, CHAPTER_TITLE)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawRightString(w - MARGIN, h - 0.75 * cm, 'Chhattisgarh Forest Department')
    # Footer
    canvas.setFillColor(C_MED)
    canvas.rect(0, 0, w, 0.8 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(w / 2, 0.25 * cm,
        f'Workshop on Elephant Mortality Investigation and Management · 2026 · Page {doc.page}')
    canvas.restoreState()


# ── Cover page ───────────────────────────────────────────────────────────────
def cover_page(styles):
    story = []
    # Full-width dark green cover block
    data = [[Paragraph('CHAPTER 3', styles['ch_label'])],
            [Paragraph('Infectious Diseases of<br/>Asian Elephants', styles['title'])],
            [Spacer(1, 0.3 * cm)],
            [Paragraph('Resource Person: Dr. M. Karikalan, MVSc, PhD', styles['author'])],
            [Paragraph('Assistant Professor, Dept. of Wildlife Science, VBSC & AH, Namakkal', styles['author'])],
            [Spacer(1, 0.5 * cm)],
            [Paragraph('Workshop on Elephant Mortality Investigation and Management', styles['subtitle'])],
            [Paragraph('Chhattisgarh Forest Department · Bilaspur · June 2026', styles['subtitle'])],
           ]
    cover = Table(data, colWidths=[INNER_W + 2 * MARGIN - 0.1 * cm])
    cover.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(cover)
    story.append(Spacer(1, 0.5 * cm))

    # Cover figure: title page of presentation
    imgs = pdf_page_img(1, width=INNER_W, caption='Source presentation: Infectious Diseases of Asian Elephants (Dr. M. Karikalan, 2026)', styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.4 * cm))

    # Key facts box
    kf = [
        '• <b>Species:</b> Asian Elephant (<i>Elephas maximus</i>) — Endangered (IUCN)',
        '• <b>Wild population:</b> ~22,446 individuals across 13 range countries',
        '• <b>India:</b> Largest population; Schedule I (Wildlife Protection Act 1972); CITES Appendix I',
        '• <b>Scope of lecture:</b> Infectious, parasitic and management-related diseases — diagnosis, treatment and prevention in wild and captive populations',
        '• <b>Lecture series:</b> VBSC SH_1_3 — compiled and presented for field veterinarians and forest officers',
    ]
    story.append(info_box(kf, styles, title='Overview'))
    story.append(PageBreak())
    return story


# ── Section 1: Introduction ──────────────────────────────────────────────────
def section_introduction(styles):
    story = [Paragraph('1. Introduction', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Wildlife disease investigation has emerged as a critical pillar of conservation medicine. '
        'The Asian elephant, already classified as Endangered on the IUCN Red List, faces an escalating '
        'burden of infectious and non-infectious diseases, many of which are poorly understood in wild populations. '
        'Mortality from preventable or treatable diseases represents a significant threat that can be mitigated '
        'through timely diagnosis, skilled post-mortem examination, and preparedness of field veterinarians.',
        styles['body']))

    story.append(Paragraph('1.1 Epidemiological Terminology', styles['subsec']))
    story.append(Paragraph(
        'A clear understanding of disease epidemiology is essential for fieldwork. Key terms used throughout '
        'this chapter are defined below:', styles['body']))

    terms = [
        ['Term', 'Definition'],
        ['Emerging Disease', 'A disease appearing in a population for the first time, or rapidly increasing in incidence/geographic range'],
        ['Re-emerging Disease', 'A previously known disease that has reappeared after a period of decline, often in new geographic areas or host species'],
        ['Transboundary Disease', 'Infectious disease that spreads across national or ecosystem boundaries, requiring multi-jurisdictional response (e.g., FMD, HS)'],
        ['Zoonosis', 'Disease transmissible between vertebrate animals and humans (e.g., TB, Rabies, Anthrax, Leptospirosis)'],
        ['Spillover', 'Transmission of a pathogen from a reservoir host to a new (incidental) host species'],
        ['Pathogenicity', 'Ability of a pathogen to cause disease in the host'],
        ['Virulence', 'Severity of disease caused by a pathogen; degree of harm inflicted on the host'],
    ]
    col_w = [3.5 * cm, INNER_W - 3.5 * cm]
    t = Table([[Paragraph(r[0], styles['table_hdr'] if i == 0 else styles['table_cell']),
                Paragraph(r[1], styles['table_hdr'] if i == 0 else styles['table_cell'])]
               for i, r in enumerate(terms)],
              colWidths=col_w)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('BACKGROUND', (0, 1), (-1, -1), C_BOX),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BOX, C_PALE]),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    # Taxonomy table from page 2
    story.append(Paragraph('1.2 Taxonomy of the Asian Elephant', styles['subsec']))
    tax = [
        ['Kingdom', 'Animalia'],
        ['Phylum', 'Chordata'],
        ['Class', 'Mammalia'],
        ['Order', 'Proboscidea'],
        ['Family', 'Elephantidae'],
        ['Genus', 'Elephas'],
        ['Species', 'Elephas maximus'],
        ['Subspecies', 'E. m. indicus (Indian), E. m. maximus (Sri Lankan), E. m. sumatranus (Sumatran), E. m. borneensis (Borneo)'],
    ]
    col_w2 = [3.5 * cm, INNER_W - 3.5 * cm]
    t2 = Table([[Paragraph(r[0], styles['table_cell']),
                 Paragraph(r[1], styles['table_cell'])]
                for r in tax], colWidths=col_w2)
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), C_PALE),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('1.3 Spectrum of Disease', styles['subsec']))
    story.append(Paragraph(
        'Elephant diseases are broadly categorised into infectious and non-infectious conditions. '
        'This distinction is fundamental for triage at a casualty site — while infectious conditions '
        'require diagnostic sampling and biosafety precautions, non-infectious causes (trauma, electrocution, '
        'nutritional deficiency) require different response protocols.',
        styles['body']))

    # Spectrum from page 3 & 6
    spec = [
        ['Infectious Diseases', 'Non-Infectious Conditions'],
        ['Viral: EEHV, Rabies, FMD, Poxvirus, EMCV', 'Electrocution (illegal/accidental)'],
        ['Bacterial: Tuberculosis, Haemorrhagic Septicaemia, Anthrax, Clostridial infections, Leptospirosis', 'Drowning / Water body falls'],
        ['Parasitic: Helminths (Fasciola, Strongyles, Amphistomes), Protozoa (Balantidium, Haemoparasites)', 'Trauma / Fall from height'],
        ['Fungal: Aspergillosis (captive)', 'Obesity and nutritional deficiency'],
        ['', 'Inter-elephant conflict / musth-related injury'],
        ['', 'Captive management failures (chaining, overwork)'],
    ]
    col_w3 = [INNER_W / 2, INNER_W / 2]
    t3 = Table([[Paragraph(r[0], styles['table_hdr'] if i == 0 else styles['table_cell']),
                 Paragraph(r[1], styles['table_hdr'] if i == 0 else styles['table_cell'])]
                for i, r in enumerate(spec)], colWidths=col_w3)
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_MED),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#E8F8F0')),
        ('BACKGROUND', (1, 1), (1, -1), colors.HexColor('#FFF8F0')),
        ('BOX', (0, 0), (-1, -1), 0.8, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t3)
    story.append(PageBreak())
    return story


# ── Section 2: EEHV ─────────────────────────────────────────────────────────
def section_eehv(styles):
    story = [Paragraph('2. Elephant Endotheliotropic Herpesvirus (EEHV)', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'EEHV is the single most important viral disease in elephants. It causes acute haemorrhagic disease '
        'characterised by a peracute clinical course — an apparently healthy calf can die within 24–72 hours '
        'of first signs. Understanding EEHV biology, diagnosis, and treatment is therefore a priority '
        'competency for any field or zoo veterinarian working with elephants.',
        styles['body']))

    story.append(Paragraph('2.1 Classification and Subtypes', styles['subsec']))
    story.append(Paragraph(
        'EEHV belongs to the family <i>Herpesviridae</i>, subfamily <i>Betaherpesvirinae</i>. '
        'In Asian elephants, the clinically important subtypes are:',
        styles['body']))
    story.append(info_box([
        '• <b>EEHV-1A / 1B</b> — Most virulent; responsible for majority of fatal cases in Asia and North America',
        '• <b>EEHV-4</b> — Second most common in Asian elephants; documented fatal cases',
        '• <b>EEHV-5</b> — Occasionally detected; less frequently fatal',
        '• <b>EEHV-2, 3, 6, 7</b> — Primarily documented in African elephants; lower risk in Asian species',
        '• <b>Carrier state:</b> Adult elephants are latent carriers with virus persisting in nerve ganglia; '
          'disease triggers in calves when maternal antibody wanes (between 1–18 years of age)',
    ], styles, title='EEHV Subtypes Relevant to Asian Elephants'))
    story.append(Spacer(1, 0.3 * cm))

    # Herpesvirus classification from page 7
    story.append(Paragraph('Figure 2.1 — Herpesvirus family classification and EEHV phylogenetic tree',
                            styles['caption']))
    imgs = pdf_page_crop(7, 0, 0.05, 1, 0.95, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('2.2 Historical Timeline and India Cases', styles['subsec']))
    story.append(Paragraph(
        'EEHV haemorrhagic disease (EEHV-HD) was first recognised in 1995 at the Smithsonian National Zoo, '
        'Washington DC, in an Asian elephant calf. Since then, multiple fatal cases have been documented '
        'globally and in India:', styles['body']))

    timeline = [
        ['Year', 'Event / Location'],
        ['1995', 'First EEHV-HD case recognised — Smithsonian National Zoo, USA'],
        ['2007', 'First confirmed EEHV case in India — Kerala (retrospective diagnosis)'],
        ['2008–2015', 'Cases documented in Tamil Nadu (Anamalai Tiger Reserve, Mudumalai)'],
        ['2021', 'Chhattisgarh: EEHV-1A positive detected (qPCR from calf death)'],
        ['2023', 'Chhattisgarh: Second positive case — active surveillance programme initiated'],
        ['2024', 'mRNA-based EEHV vaccine enters trial phase — Houston Zoo, USA'],
    ]
    cw = [2.5 * cm, INNER_W - 2.5 * cm]
    t = Table([[Paragraph(r[0], styles['table_hdr'] if i == 0 else styles['table_cell_c']),
                Paragraph(r[1], styles['table_hdr'] if i == 0 else styles['table_cell'])]
               for i, r in enumerate(timeline)], colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BOX, C_PALE]),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    # EEHV phylogeny page 8
    story.append(Paragraph('Figure 2.2 — EEHV phylogenetic relationships and fatal haemorrhagic disease history',
                            styles['caption']))
    imgs = pdf_page_crop(8, 0, 0.05, 1, 0.95, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('2.3 Pathomechanism and Vulnerable Age Groups', styles['subsec']))
    story.append(Paragraph(
        'The host preference of EEHV is age-dependent. Calves between 1 and 18 years are the primary '
        'victims of fatal disease. Adult elephants harbour the virus as latent carriers but rarely develop '
        'clinical disease. The pathomechanism involves endothelial cell tropism — the virus infects cells '
        'lining blood vessels, causing massive vascular damage:', styles['body']))

    path = [
        '1. <b>Viral entry:</b> EEHV infects endothelial cells of capillaries and venules',
        '2. <b>Vascular damage:</b> Endothelial lysis → capillary leakage → haemorrhage into tissues',
        '3. <b>Cytokine storm:</b> Systemic inflammatory response → hypotension → shock',
        '4. <b>Organ failure:</b> Myocardial, hepatic and renal involvement → death within hours to days',
        '5. <b>Gross lesions:</b> Epicardial haemorrhages, tongue cyanosis, oedema of face/tongue, petechiation',
    ]
    story.append(info_box(path, styles, title='Pathomechanism Cascade'))
    story.append(Spacer(1, 0.3 * cm))

    imgs = pdf_page_crop(9, 0, 0.05, 1, 0.95, width=INNER_W, styles=styles)
    story.append(Paragraph('Figure 2.3 — EEHV host preference by age group and pathomechanism cascade',
                            styles['caption']))
    story.extend(imgs)
    story.append(PageBreak())

    story.append(Paragraph('2.4 Clinical Signs', styles['subsec']))
    story.append(Paragraph(
        'EEHV-HD presents as a peracute haemorrhagic syndrome. The time from first clinical signs to death '
        'may be as short as 12–36 hours. The following signs have been documented in confirmed cases:',
        styles['body']))

    clin = [
        '• <b>Generalised oedema</b> of the head, face, and neck — especially dramatic periorbital and '
          'submandibular swelling (hallmark sign)',
        '• <b>Tongue cyanosis:</b> Blue-purple discolouration of the tongue mucosa (visible in live animal)',
        '• <b>Open-mouth breathing</b> and respiratory distress due to oropharyngeal oedema',
        '• <b>Weakness, recumbency,</b> reluctance to walk — rapid deterioration to lateral recumbency',
        '• <b>Pyrexia</b> (fever >38.5°C) often the first sign detected during routine morning observation',
        '• <b>Tachycardia</b> and hypotension in late stages',
        '• <b>Bloody discharge</b> from natural orifices may occur terminally',
        '• Death within 24–72 hours of first signs in untreated or late-detected cases',
    ]
    story.append(info_box(clin, styles, title='Clinical Signs of EEHV-HD'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 2.4 — Clinical photographs: EEHV-HD in a calf (Nandankanan Zoological Park)',
                            styles['caption']))
    # Pages 11-12 contain clinical photos
    imgs_left = pdf_page_crop(11, 0, 0.08, 0.5, 0.92, width=INNER_W * 0.49, styles=styles)
    imgs_right = pdf_page_crop(11, 0.5, 0.08, 1.0, 0.92, width=INNER_W * 0.49, styles=styles)
    if imgs_left and imgs_right:
        story.append(two_images(imgs_left, imgs_right))
    else:
        imgs = pdf_page_img(11, width=INNER_W, styles=styles)
        story.extend(imgs)
    story.append(Paragraph(
        'Left: Facial/periorbital oedema in affected calf. Right: Recumbency and open-mouth breathing.',
        styles['caption']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('2.5 Post-mortem Findings', styles['subsec']))
    story.append(Paragraph(
        'Necropsy of EEHV-HD cases reveals characteristic gross and histopathological changes. '
        'A thorough and documented post-mortem examination is essential for laboratory confirmation '
        'and to rule out other causes of sudden death in young elephants:', styles['body']))

    pm = [
        '• <b>Tongue:</b> Diffuse cyanosis/necrosis; villous thickening; dark blue-black discolouration on cut section',
        '• <b>Heart:</b> Epicardial and endocardial petechiae and ecchymoses; myocardial pallor and mottling',
        '• <b>Liver:</b> Congestion; occasional petechiae; hepatocellular swelling',
        '• <b>Lung:</b> Congestion and oedema; interstitial haemorrhage; frothy exudate in airways',
        '• <b>Lymph nodes:</b> Markedly enlarged, haemorrhagic; mesenteric LN especially affected',
        '• <b>Kidney:</b> Cortical pallor, perivascular haemorrhage',
        '• <b>Spleen:</b> Usually unremarkable or mildly enlarged',
        '• <b>Brain:</b> Usually negative (important for rabies differential exclusion)',
    ]
    story.append(info_box(pm, styles, title='Gross Post-Mortem Lesions'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph(
        'Figure 2.5 — PM photographs: tongue cyanosis (ERRC Surajpur), epicardial haemorrhages (MTR Nilgiris), '
        'and myocardial lesions (BBBP Ranchi, Nandankanan)', styles['caption']))
    imgs = pdf_page_img(12, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('2.6 Histopathology', styles['subsec']))
    story.append(Paragraph(
        'Histopathological examination confirms the endotheliotropic nature of EEHV. '
        'Representative tissues should be fixed in 10% neutral buffered formalin immediately at necropsy. '
        'Characteristic findings on H&E staining include:', styles['body']))

    histo = [
        '• <b>Tongue mucosa:</b> Intranuclear inclusion bodies in endothelial cells; mucosal ulceration; '
          'sub-epithelial haemorrhage; intravascular fibrin thrombi',
        '• <b>Myocardium:</b> Perivascular lymphocytic infiltration; myocyte necrosis; '
          'endothelial swelling with inclusion bodies (H&E ×200)',
        '• <b>Pulmonary sinusoids:</b> Endothelial inclusions; alveolar capillary congestion; '
          'occasional fibrin thrombi',
        '• <b>Renal vessels:</b> Glomerular and interstitial haemorrhage; endothelial inclusions',
        '• <b>Diagnostic significance:</b> Intranuclear inclusions are pathognomonic for herpesvirus; '
          'their presence in multiple tissues confirms EEHV-HD',
    ]
    story.append(info_box(histo, styles, title='Histopathological Findings (H&E)'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 2.6 — Histopathology: H&E sections (×200) from EEHV-HD cases',
                            styles['caption']))
    imgs = pdf_page_img(13, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Paragraph(
        'Clockwise from top-left: Tongue mucosa, myocardium, pulmonary sinusoids, renal vessels — '
        'showing intranuclear inclusion bodies and vascular damage (H&E ×200)',
        styles['caption']))
    story.append(PageBreak())

    story.append(Paragraph('2.7 Laboratory Diagnosis: qPCR', styles['subsec']))
    story.append(Paragraph(
        'Quantitative PCR (qPCR) is the gold standard for EEHV diagnosis, both in live animals (antemortem) '
        'and at necropsy (postmortem). Understanding the CT value interpretation is essential for field '
        'veterinarians:', styles['body']))

    qpcr = [
        ['Sample Type', 'Use', 'Interpretation'],
        ['Whole blood (EDTA)', 'Antemortem surveillance; monitoring in sick calves', 'CT <30: Active viraemia (treat immediately); CT 30–37: Low-level positive / carrier; CT >37: Negative or below detection'],
        ['Bone marrow aspirate', 'Best postmortem sample; highest viral load in active EEHV-HD', 'Highest sensitivity — preferred for PM diagnosis'],
        ['Trunk wash', 'Detection of viral shedding in carriers/adults', 'Used for herd surveillance; lower sensitivity than blood PCR'],
        ['Heart / Tongue / Lymph node', 'PM tissue samples for qPCR and histopathology', 'Heart and tongue show highest viral copy numbers in EEHV-HD'],
        ['Liver / Lung / Kidney', 'Supplementary PM tissues', 'Variable viral loads; important for severity assessment'],
    ]
    cw = [2.8 * cm, 4.5 * cm, INNER_W - 7.3 * cm]
    t = Table([[Paragraph(r[i], styles['table_hdr'] if row == 0 else styles['table_cell'])
                for i in range(3)]
               for row, r in enumerate(qpcr)], colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BOX, C_PALE]),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 2.7 — Tissue viral load data (qPCR) and qPCR vs conventional PCR comparison',
                            styles['caption']))
    imgs = pdf_page_img(14, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('2.8 Treatment Protocol', styles['subsec']))
    story.append(Paragraph(
        'EEHV-HD is a veterinary emergency. Treatment must begin immediately on clinical suspicion — '
        'do not wait for PCR results. Early intervention dramatically improves survival odds. '
        'The treatment protocol used at leading elephant centres in India:', styles['body']))

    treat = [
        '• <b>Famciclovir</b> 5.5–8 mg/kg BID orally — antiviral prodrug (converted to penciclovir); '
          'inhibits viral DNA polymerase; first-line agent; must be pre-positioned at elephant camps',
        '• <b>Acyclovir</b> IV — used in severe cases when oral famciclovir cannot be administered; '
          'acts at same target as famciclovir; give via slow IV infusion',
        '• <b>Fluid therapy:</b> Isotonic crystalloids (Ringer\'s Lactate, Normal Saline) via IV; '
          'volume resuscitation for vascular leakage; monitor urine output',
        '• <b>Anti-inflammatory:</b> Dexamethasone (cautious use) or Meloxicam for inflammatory cascade',
        '• <b>Gastric protectants:</b> Omeprazole / Pantoprazole — prevent stress-related gastric lesions',
        '• <b>Supportive care:</b> Shade, quiet environment, soft browse/fruit, mahout presence to reduce stress',
        '• <b>Monitoring:</b> Temperature every 4 hours; blood qPCR every 24–48 hours; '
          'decreasing CT value = improving; CBC and chemistry every 48 hours if possible',
    ]
    story.append(info_box(treat, styles, title='EEHV Treatment Protocol (Field & Zoo)'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(warn_box([
        'Famciclovir and Acyclovir must be pre-positioned at all elephant camps and zoos housing calves. '
        'Delay in starting antiviral treatment is the most common cause of treatment failure.',
        'Do NOT use corticosteroids as first-line agents — they may accelerate viral replication.',
        'Quarantine the affected calf; test all herd members for viraemia; notify State and Central authorities.',
    ], styles, title='CRITICAL: EEHV Emergency Response'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 2.8 — EEHV treatment protocol and monitoring/prevention framework',
                            styles['caption']))
    imgs_t = pdf_page_img(15, width=INNER_W * 0.48, styles=styles)
    imgs_m = pdf_page_img(16, width=INNER_W * 0.48, styles=styles)
    if imgs_t and imgs_m:
        story.append(two_images(imgs_t, imgs_m))
    else:
        story.extend(pdf_page_img(15, width=INNER_W, styles=styles))
        story.extend(pdf_page_img(16, width=INNER_W, styles=styles))
    story.append(Paragraph(
        'Left: Treatment protocol summary. Right: Monitoring, prevention and vaccine development update '
        '(mRNA EEHV vaccine currently in trial at Houston Zoo, USA).',
        styles['caption']))
    story.append(PageBreak())
    return story


# ── Section 3: Rabies ────────────────────────────────────────────────────────
def section_rabies(styles):
    story = [Paragraph('3. Rabies in Elephants', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Rabies, caused by <i>Lyssavirus</i> (negative-sense ssRNA, family Rhabdoviridae), is a fatal '
        'zoonotic neurological disease. While uncommon in elephants, confirmed and suspected cases have '
        'been documented in captive individuals, typically following contact with infected dogs, foxes, '
        'or bats. The invariably fatal outcome and zoonotic risk make it a priority differential diagnosis '
        'in any elephant with acute neurological signs.',
        styles['body']))

    story.append(Paragraph('3.1 Transmission and Clinical Features', styles['subsec']))
    trans = [
        '• <b>Transmission:</b> Bite of a rabid dog (most common in captive elephants in India); rarely from fox or bat',
        '• <b>Incubation:</b> Variable (weeks to months); virus travels along peripheral nerves to CNS',
        '• <b>Clinical signs:</b> Sudden behavioural change; aggression alternating with depression; '
          'hypersalivation; dysphagia; photophobia; incoordination; seizures; coma; death',
        '• <b>Differential diagnosis:</b> EEHV (young calves), HS, OP poisoning, musth-related aggression',
        '• <b>Prognosis:</b> 100% fatal once clinical signs appear; no treatment available',
    ]
    story.append(info_box(trans, styles))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('3.2 Diagnosis', styles['subsec']))
    diag = [
        '• <b>Sample:</b> Brain tissue (cerebellum, hippocampus, brainstem) — ONLY sample for rabies diagnosis',
        '• <b>FAT (Fluorescent Antibody Test):</b> Gold standard; requires fresh brain; fluorescent microscopy',
        '• <b>Histopathology:</b> Negri bodies — eosinophilic intracytoplasmic inclusions in Purkinje cells '
          'and hippocampal neurons (H&E ×400)',
        '• <b>Seller\'s stain:</b> Rapid field stain for Negri bodies (methylene blue + basic fuchsin); '
          'Negri bodies appear magenta against blue background (×1000)',
        '• <b>RT-PCR:</b> Most sensitive; gel electrophoresis shows diagnostic band; can use preserved tissue',
        '• <b>Biosafety:</b> Handle brain samples with gloves, mask, and eye protection; '
          'post-exposure prophylaxis for exposed personnel',
    ]
    story.append(info_box(diag, styles, title='Rabies Diagnostic Protocol'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 3.1 — Rabies: transmission cycle, Negri body histology and diagnostic methods',
                            styles['caption']))
    imgs = pdf_page_img(17, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Paragraph(
        'Top row: Rabies transmission cycle; H&E ×400 — Negri bodies in neurons; Seller\'s stain ×1000. '
        'Bottom row: FAT (Fluorescent Antibody Test) smear; RT-PCR gel showing diagnostic band.',
        styles['caption']))
    story.append(PageBreak())
    return story


# ── Section 4: FMD ───────────────────────────────────────────────────────────
def section_fmd(styles):
    story = [Paragraph('4. Foot and Mouth Disease (FMD)', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'FMD is caused by <i>Aphthovirus</i> (Picornaviridae), with seven known serotypes (O, A, C, SAT1, '
        'SAT2, SAT3, Asia1). While elephants are not primary hosts, spillover from infected livestock is '
        'documented — particularly in forest fringes where elephant corridors overlap with grazing areas. '
        'FMD rarely causes death in elephants, but severe cases with secondary septicaemia can be fatal.',
        styles['body']))

    fmd = [
        '• <b>Clinical signs:</b> Vesicular lesions on feet and trunk tip; lameness; reluctance to walk; '
          'drooling if oral lesions present; fever in acute phase',
        '• <b>Lesion appearance:</b> Fluid-filled blisters (vesicles) → rupture → raw erosions → secondary bacterial infection',
        '• <b>Diagnosis:</b> Clinical appearance of vesicles; virus isolation; RT-PCR from vesicular fluid; '
          'ELISA for serology; probe-based antigen detection kit (IVRI Mukteswar)',
        '• <b>Control:</b> FMD vaccination of all surrounding livestock; strict movement restrictions; '
          'lime disinfection of premises; isolation of affected animals',
        '• <b>Significance in elephants:</b> Captive Indian elephants reported with FMD; '
          'secondary septicaemia is the main cause of mortality risk',
    ]
    story.append(info_box(fmd, styles, title='FMD in Elephants — Key Points'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 4.1 — FMD vesicular lesions and isolation protocol',
                            styles['caption']))
    imgs = pdf_page_img(18, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(PageBreak())
    return story


# ── Section 5: Poxvirus ──────────────────────────────────────────────────────
def section_pox_emcv(styles):
    story = [Paragraph('5. Poxvirus and Encephalomyocarditis Virus (EMCV)', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph('5.1 Poxvirus (Cowpox/Elephantpox)', styles['subsec']))
    story.append(Paragraph(
        'Elephants can be infected with cowpox virus (a member of <i>Orthopoxvirus</i>), '
        'typically through contact with infected rodents or dairy cattle. The condition is sometimes '
        'called "elephantpox" but is genetically cowpox virus. Cases are documented in zoos across '
        'Europe and in India.', styles['body']))
    pox = [
        '• <b>Lesions:</b> Papular/vesicular eruptions on skin — trunk, ears, periocular region, feet; '
          'heal over 2–4 weeks in uncomplicated cases; gross lung lesions in severe systemic pox',
        '• <b>Diagnosis:</b> Clinical appearance; electron microscopy of skin scrapings; PCR; histopathology '
          '(H&E: eosinophilic intracytoplasmic inclusions — Guarnieri bodies)',
        '• <b>Treatment:</b> Symptomatic; wound care; antibiotics for secondary infection; tecovirimat (antiviral) in severe cases',
        '• <b>Zoonosis:</b> Cowpox is a zoonotic virus; mahouts and keepers handling lesions must use PPE',
    ]
    story.append(info_box(pox, styles))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph('Figure 5.1 — Poxvirus: vesicular skin lesions on Asian elephant',
                            styles['caption']))
    imgs = pdf_page_img(20, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('5.2 Encephalomyocarditis Virus (EMCV)', styles['subsec']))
    story.append(Paragraph(
        'EMCV (Cardiovirus, Picornaviridae) causes acute myocarditis and sudden cardiac death, '
        'predominantly in zoo elephants. The virus is transmitted via rodent contamination of food and water. '
        'A fatal case was documented at Delhi Zoo (India). The virus replicates in myocardial cells, '
        'causing haemorrhagic myocarditis.', styles['body']))
    emcv = [
        '• <b>Source:</b> Rats and mice (reservoir hosts); contaminated feed and water troughs',
        '• <b>Clinical signs:</b> Sudden death or acute cardiac failure; weakness; collapse; '
          'occasionally preceded by brief respiratory distress',
        '• <b>PM findings:</b> Haemorrhagic myocarditis; pale myocardium; pericardial effusion',
        '• <b>Diagnosis:</b> Virus isolation; serology (ELISA); histopathology; rodent control as prevention',
    ]
    story.append(info_box(emcv, styles))
    story.append(PageBreak())
    return story


# ── Section 6: Tuberculosis ──────────────────────────────────────────────────
def section_tb(styles):
    story = [Paragraph('6. Tuberculosis (TB) in Elephants', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Tuberculosis caused by <i>Mycobacterium tuberculosis</i> (human strain) is the primary mycobacterial '
        'disease in captive elephants globally. Importantly, TB in elephants is a reverse zoonosis — humans '
        'with active TB infect elephants, not vice versa in most documented cases. However, infected elephants '
        'can shed bacilli and theoretically transmit to in-contact humans (mahouts, vets). '
        'The disease is chronic, slowly progressive, and often clinically silent for years.',
        styles['body']))

    story.append(Paragraph('6.1 Diagnosis', styles['subsec']))
    diag = [
        '<b>Trunk wash (TW):</b>',
        '• Standard antemortem test — 3 trunk washes (saline lavage) on 3 consecutive mornings; pooled sample',
        '• Culture on Lowenstein-Jensen medium (takes 6–8 weeks); PCR (faster — 48–72 hours)',
        '• Sensitivity 60–70% for culture; PCR more sensitive but needs validation',
        '',
        '<b>Serology (MAPIA / ElephantTB STAT-PAK):</b>',
        '• Multi-Antigen Print ImmunoAssay; lateral flow assay using recombinant antigens',
        '• Detects antibodies — useful for screening but cannot distinguish active from latent disease',
        '• Serial testing increases sensitivity; single negative test does not rule out TB',
        '',
        '<b>PM diagnosis:</b>',
        '• Gross miliary TB lesions in lung, lymph nodes (acid-fast staining, Ziehl-Neelsen)',
        '• PCR on lymph node tissue; IS6110 insertion sequence target (M. tuberculosis specific)',
    ]
    story.append(info_box(diag, styles, title='TB Diagnostic Protocol (CWL IVRI)'))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph('Figure 6.1 — TB diagnostics: acid-fast staining, PCR gel and LFA kit',
                            styles['caption']))
    imgs_tb1 = pdf_page_img(21, width=INNER_W * 0.49, styles=styles)
    imgs_tb2 = pdf_page_img(22, width=INNER_W * 0.49, styles=styles)
    if imgs_tb1 and imgs_tb2:
        story.append(two_images(imgs_tb1, imgs_tb2))
    else:
        story.extend(pdf_page_img(21, width=INNER_W, styles=styles))
        story.extend(pdf_page_img(22, width=INNER_W, styles=styles))
    story.append(Paragraph(
        'Left: Acid-fast bacilli (blue stain) in sputum/trunk wash; IS6110 PCR gel; LFA kit (TB STAT-PAK). '
        'Right: USDA recommended diagnostic flowchart; free-range elephant lung with miliary TB lesions.',
        styles['caption']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('6.2 Treatment', styles['subsec']))
    treat = [
        '• <b>3-drug regimen</b> (minimum 12 months; ideally 18–24 months for elephants):',
        '  — Isoniazid (INH): 100 mg/day or 4–5 mg/kg',
        '  — Pyrazinamide (PZA): 500 mg/day or 25–30 mg/kg (first 2 months)',
        '  — Rifampicin (RIF): 600 mg/day or 10–15 mg/kg',
        '• Drugs given in banana/jaggery boluses; observed administration (OAT) essential',
        '• Monitor liver enzymes (AST, ALT) monthly — hepatotoxicity risk',
        '• Pyridoxine (Vitamin B6) supplementation to prevent INH-related neuropathy',
        '• Restrict movement and contact with other elephants during treatment',
    ]
    story.append(info_box(treat, styles, title='TB Treatment Protocol (Anti-Tubercular Therapy)'))
    story.append(Spacer(1, 0.3 * cm))
    story.append(warn_box([
        'TB in elephants is a notifiable disease. Report to Chief Wildlife Warden and nearest IVRI/veterinary institute.',
        'Mahouts caring for TB-positive elephants must undergo chest X-ray and sputum test; anti-TB prophylaxis if indicated.',
        'Three negative trunk wash cultures at monthly intervals required before declaring an elephant TB-free.',
    ], styles, title='TB: Regulatory and Biosafety Requirements'))
    story.append(PageBreak())
    return story


# ── Section 7: Anthrax ───────────────────────────────────────────────────────
def section_anthrax(styles):
    story = [Paragraph('7. Anthrax', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Anthrax is caused by <i>Bacillus anthracis</i>, a Gram-positive, aerobic spore-forming bacterium. '
        'It causes peracute to acute disease in elephants, with death occurring within hours of the onset of '
        'signs. Anthrax outbreaks in wildlife are typically associated with specific anthrax-prone "hot zones" '
        'where spores persist in the soil for decades.', styles['body']))

    ant = [
        '• <b>Peracute/acute course:</b> An apparently healthy elephant found dead; or brief signs of '
          'unsteadiness, collapse, death within 1–6 hours',
        '• <b>Pathognomonic gross sign:</b> Non-clotting, tarry (dark, watery) blood from all natural orifices '
          '(mouth, trunk, anus, vulva)',
        '• <b>DO NOT open the carcass</b> on site — sporulation occurs on air contact; '
          'opening the carcass contaminate the entire site for 30–50 years',
        '• <b>Staining:</b> Polychrome methylene blue (McFadyean reaction) — bamboo-rod shaped bacilli with '
          'blue capsule in blood smear; pathognomonic',
        '• <b>Spore persistence:</b> Anthrax spores (endospores) survive in soil for 30–100 years; '
          'heavy rainfall or soil disturbance can expose buried carcasses and release spores',
        '• <b>Epidemics:</b> Outbreaks tend to occur in hot, dry seasons followed by rainfall; '
          'documented in Joyepur Forest Range, Dibrugarh, Assam (elephants and ungulates)',
    ]
    story.append(info_box(ant, styles, title='Anthrax — Key Field Points'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 7.1 — Anthrax: carcass findings, polychrome methylene blue staining, '
                            'and field investigation (Joyepur Forest Range, Assam)', styles['caption']))
    imgs = pdf_page_img(23, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(warn_box([
        'DO NOT perform a full necropsy on a suspected anthrax carcass in the field.',
        'WHO/OIE Standard: BURN the carcass and all contaminated material; do NOT bury '
        '(burial accelerates sporulation and permanently contaminates the burial site).',
        'All persons at scene must wear full PPE: gloves, N95 mask, goggles, boot covers.',
        'Collect only a peripheral blood smear and blood in sealed vials for lab confirmation.',
        'Notify Chief Wildlife Warden, IVRI, and District Collector (Section 38P, WPA 1972).',
        'Vaccinate all livestock in a 5-km radius with Sterne strain anthrax vaccine immediately.',
    ], styles, title='ANTHRAX EMERGENCY PROTOCOL — CRITICAL'))
    story.append(PageBreak())
    return story


# ── Section 8: Haemorrhagic Septicaemia ─────────────────────────────────────
def section_hs(styles):
    story = [Paragraph('8. Haemorrhagic Septicaemia (HS)', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Haemorrhagic Septicaemia is caused by <i>Pasteurella multocida</i> type B:2 (and occasionally E:2). '
        'HS is primarily a disease of bovids (cattle, buffalo), but elephants are susceptible — '
        'particularly captive/semi-captive animals under stress. The disease is peracute and '
        'characterised by sudden high fever, respiratory distress, and death within 24–48 hours. '
        'Outbreaks in elephants have been investigated in Kalahandi district, Odisha and Kartapat WLS.',
        styles['body']))

    hs = [
        '• <b>Predisposing factors:</b> Physical stress (translocation, overwork, musth), nutritional deficiency, '
          'heavy rainfall season, contact with infected cattle',
        '• <b>Clinical signs:</b> High fever (40–42°C); oedematous swelling of head/neck/brisket; '
          'respiratory distress; profuse salivation; tympanitis; death in 24–48 hours',
        '• <b>PM findings:</b> Severe haemorrhagic pneumonia; peracute congestion of all organs; '
          'haemorrhagic lymph nodes; subcutaneous gelatinous oedema',
        '• <b>Histopathology:</b> Bipolar organism (oval shape with bipolar staining — "safety pin" appearance) '
          'on Gram stain or Leishman stain',
        '• <b>Best diagnostic sample:</b> Bone marrow aspirate from femur or rib '
          '(taken within hours of death before lysis; highest yield)',
        '• <b>Treatment:</b> Penicillin G 20,000 IU/kg IM; Tetracycline; Sulphonamides; '
          'fluid therapy; anti-inflammatory (Meloxicam)',
        '• <b>Prevention:</b> HS vaccination of all livestock in a 2-km radius; '
          'separate elephant water sources from cattle wallows',
    ]
    story.append(info_box(hs, styles, title='HS — Diagnosis and Management'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 8.1 — HS: bipolar organisms (Leishman stain), haemorrhagic lung lesions, '
                            'and Kalahandi field investigation', styles['caption']))
    imgs_l = pdf_page_img(24, width=INNER_W * 0.49, styles=styles)
    imgs_r = pdf_page_img(25, width=INNER_W * 0.49, styles=styles)
    if imgs_l and imgs_r:
        story.append(two_images(imgs_l, imgs_r))
    else:
        story.extend(pdf_page_img(24, width=INNER_W, styles=styles))
        story.extend(pdf_page_img(25, width=INNER_W, styles=styles))
    story.append(Paragraph(
        'Left: Bipolar staining of <i>P. multocida</i>; gross PM lung lesions; haemorrhagic lymphadenopathy. '
        'Right: Field investigation at Kartapat WLS — trackers, necropsy team, and carcass disposal operations.',
        styles['caption']))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 8.2 — HS control: livestock vaccination and bone marrow sampling protocol',
                            styles['caption']))
    imgs = pdf_page_img(26, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(PageBreak())
    return story


# ── Section 9: Clostridial ───────────────────────────────────────────────────
def section_clostridial(styles):
    story = [Paragraph('9. Clostridial Infections', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Clostridial diseases are caused by Gram-positive, anaerobic, spore-forming bacilli of the genus '
        '<i>Clostridium</i>. Several species are pathogenic in elephants, producing potent toxins that cause '
        'rapid multiorgan failure:', styles['body']))

    clos = [
        ['Species', 'Disease', 'Key Features'],
        ['C. difficile', 'Pseudomembranous enterocolitis', 'Watery/haemorrhagic diarrhoea; pseudomembrane on colonic mucosa; associated with antibiotic use'],
        ['C. perfringens (Type A/D)', 'Enterotoxaemia', 'Sudden death; bloat; haemorrhagic enteritis; toxin detection by ELISA from intestinal contents'],
        ['C. tetani', 'Tetanus', 'Muscular rigidity; lockjaw; opisthotonus; triggered by wound infection; rare in elephants'],
        ['C. botulinum', 'Botulism', 'Flaccid paralysis; toxin from contaminated feed; peracute death possible'],
        ['C. chauvoei', 'Blackleg (rare)', 'Gas gangrene of muscle; crepitation on palpation; acute febrile death'],
    ]
    cw = [3 * cm, 3.5 * cm, INNER_W - 6.5 * cm]
    t = Table([[Paragraph(r[i], styles['table_hdr'] if row == 0 else styles['table_cell'])
                for i in range(3)]
               for row, r in enumerate(clos)], colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BOX, C_PALE]),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    story.append(warn_box([
        'When handling intestines of suspected Clostridial cases: do NOT open intestinal loops in the field. '
        'Intestinal contents must be sealed and sent to laboratory immediately under cold chain.',
        'Clostridial toxins dissipate rapidly after death — intestinal samples must be collected within '
        '1–2 hours of death for toxin ELISA to be meaningful.',
    ], styles, title='Field Note: Clostridial Sample Collection'))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph('Figure 9.1 — Clostridial: C. difficile enterocolitis (gross mucosa), tetanus, '
                            'and published case literature', styles['caption']))
    imgs = pdf_page_img(27, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(PageBreak())
    return story


# ── Section 10: Leptospirosis ────────────────────────────────────────────────
def section_lepto(styles):
    story = [Paragraph('10. Leptospirosis', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        '<i>Leptospira</i> spp. (spirochete bacteria) cause leptospirosis, a globally important zoonosis. '
        'The disease is transmitted through water or soil contaminated by urine of infected animals '
        '(rodents, cattle, dogs). Elephants are exposed at contaminated water bodies, river banks, '
        'and during monsoon flooding. The IVRI Leptospirosis Laboratory maintains 21 serovars for diagnosis.', styles['body']))

    lepto = [
        '• <b>Transmission:</b> Contact with contaminated water/soil through skin abrasions, mucous membranes, '
          'or ingestion; rodents are primary reservoir; cattle/dogs amplify hosts',
        '• <b>Clinical signs in elephants:</b> Fever; icterus (jaundice); haemoglobinuria (red urine); '
          'haemorrhagic manifestations; abortion in females; in severe cases, acute renal failure and death',
        '• <b>Diagnosis:</b> MAT (Microscopic Agglutination Test) — paired samples 2 weeks apart; '
          '4-fold rise in titre diagnostic; Latex Agglutination Test (LAT) for field screening; '
          'darkfield microscopy of urine; PCR on blood/urine',
        '• <b>Treatment:</b> Penicillin G (effective if early); Doxycycline 5 mg/kg; supportive fluid therapy',
        '• <b>Prevention:</b> Avoid water body access during monsoon floods; rodent control; '
          'vaccination of working elephants (available in some countries)',
    ]
    story.append(info_box(lepto, styles))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 10.1 — Leptospirosis: transmission cycle, MAT serovars panel, '
                            'and Latex Agglutination Test', styles['caption']))
    imgs = pdf_page_img(28, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(PageBreak())
    return story


# ── Section 11: Parasitic Diseases ──────────────────────────────────────────
def section_parasites(styles):
    story = [Paragraph('11. Parasitic Diseases', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Parasitic diseases in elephants encompass a wide range of helminths, protozoa, and ectoparasites. '
        'While rarely causing acute mortality in healthy adults, parasitic burdens contribute to debilitation, '
        'secondary infections, and increased susceptibility to other diseases — particularly in captive elephants '
        'on restricted diets or in poor body condition.',
        styles['body']))

    story.append(Paragraph('11.1 Helminth Parasites', styles['subsec']))
    helm = [
        ['Parasite', 'Type', 'Location', 'Clinical Significance'],
        ['Fasciola jacksoni', 'Trematode (Liver fluke)', 'Bile ducts / Liver', 'Fasciolosis: hepatomegaly, biliary fibrosis, emaciation; Fasciola eggs with bile in faeces'],
        ['Pseudodiscus collinsi', 'Amphistome (rumen fluke)', 'Large intestine / Caecum', 'Heavy burdens → colitis; diarrhoea; seen on PM as reddish-brown flukes attached to mucosa'],
        ['Strongylus spp. / Strongyles', 'Nematode', 'Anterior/posterior intestine', 'Colitis, protein loss; larvicidal migration causes hepatic tracking'],
        ['Toxocara (in calves)', 'Nematode', 'Small intestine', 'Visceral larva migrans; pot-belly; poor growth in calves'],
        ['Oxyuris (pinworm)', 'Nematode', 'Rectum', 'Tail rubbing; anal irritation; common in captive elephants'],
    ]
    cw = [3.2 * cm, 2.5 * cm, 2.8 * cm, INNER_W - 8.5 * cm]
    t = Table([[Paragraph(r[i], styles['table_hdr'] if row == 0 else styles['table_cell'])
                for i in range(4)]
               for row, r in enumerate(helm)], colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BOX, C_PALE]),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 11.1 — Helminth parasites: Pseudodiscus collinsi (amphistome), '
                            'GI nematodes (Strongyle), and Fasciola jacksoni eggs and flukes',
                            styles['caption']))
    imgs = pdf_page_img(29, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('11.2 Protozoal Parasites', styles['subsec']))
    proto = [
        '• <b>Balantidium coli/suis:</b> Large ciliated protozoan; infects colon; causes yellow diarrhoea; '
          'photomicrograph shows cysts and trophozoites; '
          'Treatment: Metronidazole 15–25 mg/kg BID for 5 days + Omeprazole',
        '• <b>Haemoparasites:</b> Trypanosoma spp. found in blood smears; transmitted by biting flies; '
          'associated with emaciation, anaemia, lymphadenopathy; treated with Diminazene aceturate',
        '• <b>Sarcocystis:</b> Intramuscular cysts; incidental finding at necropsy in most cases',
        '• <b>Amoeba:</b> Entamoeba spp. occasionally detected in faecal smears; '
          'significance unclear in elephants',
    ]
    story.append(info_box(proto, styles, title='Protozoal Parasites'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 11.2 — Protozoal parasites: Balantidium cyst microscopy, '
                            'yellow diarrhoea case, blood smear with haemoparasite',
                            styles['caption']))
    imgs = pdf_page_img(30, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(PageBreak())
    return story


# ── Section 12: Surgical & Non-Infectious ────────────────────────────────────
def section_surgical(styles):
    story = [Paragraph('12. Surgical and Non-Infectious Conditions', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Beyond infectious disease, field and zoo veterinarians frequently encounter traumatic, '
        'degenerative and management-related conditions. These require hands-on surgical skills and '
        'a good knowledge of elephant anatomy:', styles['body']))

    surg = [
        '• <b>Sinus wound / abscess:</b> Common in captive elephants; secondary to bullhook injuries, '
          'trauma or tusk injuries; requires debridement, irrigation with povidone-iodine, and systemic antibiotics; '
          'may need surgical debridement under chemical restraint (Etorphine / Medetomidine)',
        '• <b>Corneal opacity / eye conditions:</b> Corneal ulcers from foreign bodies, trauma or infection; '
          'treatment: topical antibiotic + atropine; assess retinal integrity; '
          'ophthalmoscopy under chemical restraint',
        '• <b>Foot problems:</b> Extremely common in captive elephants — overgrown nails, foot pad cracks, '
          'sole abscesses; caused by hard substrate, poor hygiene, inadequate exercise; '
          'treatment: trimming, foot soaks (copper sulphate/betadine), systemic antibiotics',
        '• <b>Dystocia:</b> Rare but life-threatening; calf mal-presentation; requires controlled delivery '
          'under sedation; pre-positioning of delivery assistance equipment recommended at breeding herds',
        '• <b>Colic / Impaction:</b> Abdominal pain; anorexia; reduced faecal output; treat with liquid paraffin '
          'per os, fluids, Buscopan; severe cases may require flank examination under sedation',
    ]
    story.append(info_box(surg, styles, title='Common Surgical and Management Conditions'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 12.1 — Surgical cases: sinus wound treatment (Dudhwa NP), '
                            'corneal opacity, foot nail overgrowth and pad cracks',
                            styles['caption']))
    imgs_l = pdf_page_img(31, width=INNER_W * 0.49, styles=styles)
    imgs_r = pdf_page_img(32, width=INNER_W * 0.49, styles=styles)
    if imgs_l and imgs_r:
        story.append(two_images(imgs_l, imgs_r))
    else:
        story.extend(pdf_page_img(31, width=INNER_W, styles=styles))
        story.extend(pdf_page_img(32, width=INNER_W, styles=styles))
    story.append(Paragraph(
        'Left: Sinus wound irrigation and debridement in elephant Roopakali (Dudhwa NP). '
        'Right: Corneal opacity assessment; overgrown foot nails; sole cracks in captive elephant.',
        styles['caption']))
    story.append(PageBreak())
    return story


# ── Section 13: Emerging Threats ─────────────────────────────────────────────
def section_emerging(styles):
    story = [Paragraph('13. Emerging Threats and Mass Mortality Events', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Wildlife disease ecology is constantly evolving. RNA viruses, climate-driven pathogen range shifts, '
        'and novel toxicological threats pose growing risks to elephant populations. '
        'Veterinarians and forest officers must remain alert to unusual mortality clusters that may signal '
        'emerging pathogen activity.', styles['body']))

    emerg = [
        '• <b>Cyanobacteria / Algal bloom toxins:</b> Botswana 2020 — largest documented elephant mass '
          'mortality event; 350 elephants died around waterholes; cyanobacterial toxins (suspected '
          'nodularin/microcystin or BMAA) implicated; elephants showed neurological signs before collapse',
        '• <b>Monkeypox (now Mpox):</b> Documented in captive elephants from Africa; can spillover to keepers; '
          'vesicular skin lesions; zoonotic potential elevated since smallpox vaccination stopped',
        '• <b>Novel RNA viruses:</b> Bat-origin coronaviruses (SARS-CoV-2 antibodies detected in some captive '
          'elephants in Belgium); Paramyxoviruses; Nipah (bats → elephants theoretically possible in Kerala)',
        '• <b>Climate change:</b> Shifts in mosquito vectors → altered arbovirus range; '
          'changes in grass/crop phenology affecting mycotoxin risk; increased heat stress mortality events',
        '• <b>Antibiotic resistance:</b> Elephants in close proximity to human settlements accumulate '
          'resistant bacteria; antibiotic sensitivity testing mandatory before treatment',
    ]
    story.append(info_box(emerg, styles, title='Emerging Threats to Asian Elephant Health'))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('Figure 13.1 — Botswana 2020: mass elephant mortality around waterhole (cyanobacteria)',
                            styles['caption']))
    imgs = pdf_page_img(33, width=INNER_W, styles=styles)
    story.extend(imgs)
    story.append(PageBreak())
    return story


# ── Section 14: Field Practices ──────────────────────────────────────────────
def section_field(styles):
    story = [Paragraph('14. Field Practice Principles and Preparedness', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'Effective disease diagnosis and management in the field requires structured protocols, '
        'appropriate equipment, and a systematic approach. The following principles should guide '
        'field veterinarians at any elephant casualty or sick elephant call:', styles['body']))

    story.append(Paragraph('14.1 Antibiotic Use and Sensitivity Testing', styles['subsec']))
    ab = [
        '• Always culture-based treatment when possible — empirical antibiotics only in emergencies',
        '• Collect swabs/tissue/blood for culture BEFORE starting antibiotics',
        '• Disk diffusion / Kirby-Bauer method for sensitivity testing (readily available at district labs)',
        '• Avoid broad-spectrum antibiotic overuse — accelerates resistance in zoonotic bacteria',
        '• Document all drug use: drug name, dose, route, duration, outcome — essential for case analysis',
    ]
    story.append(info_box(ab, styles))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('14.2 Documentation and Photography Protocol', styles['subsec']))
    doc = [
        '• <b>Photograph before touching:</b> Establish GPS location; photograph the scene and carcass position before examination',
        '• <b>Video documentation:</b> Record gross PM findings continuously; voice narrate observations',
        '• <b>Systematic PM photography:</b> Each body cavity; each organ; all lesions with scale bar',
        '• <b>Labelling:</b> Sample labels in waterproof ink; photograph each labelled sample with ID visible',
        '• <b>Chain of custody:</b> Log each sample handed over; signatures required',
        '• <b>Necropsy report:</b> Submit within 48 hours using standard DFO/CWL format',
    ]
    story.append(info_box(doc, styles))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph('14.3 Essential Field Kit', styles['subsec']))
    kit = [
        ['Category', 'Items'],
        ['Personal Protective Equipment', 'Nitrile gloves (×3 pairs/person), N95 mask, splash goggles, Tyvek suit, boot covers, biohazard waste bags'],
        ['Sample Collection', 'EDTA tubes, plain red-top tubes, formalin pots (10%), sterile swabs, viral transport media, bone marrow aspiration needle, labelled zip-lock bags'],
        ['Instruments', 'Scalpel (large handle + #22 blades), bone saw or hacksaw, forceps, scissors, ruler, weighing scale'],
        ['Diagnostics', 'Portable glucometer, haemoglobin meter, glass slides, Wright/Giemsa stain, Seller\'s stain, darkfield microscopy (if available)'],
        ['Communication', 'GPS unit, camera with macro lens, waterproof field notebook, contact list (IVRI, lab, WW office, PCCF)'],
        ['Cold Chain', 'Ice packs, insulated cool box, cold chain labels'],
    ]
    cw = [3.5 * cm, INNER_W - 3.5 * cm]
    t = Table([[Paragraph(r[0], styles['table_hdr'] if row == 0 else styles['table_cell']),
                Paragraph(r[1], styles['table_hdr'] if row == 0 else styles['table_cell'])]
               for row, r in enumerate(kit)], colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BOX, C_PALE]),
        ('BOX', (0, 0), (-1, -1), 0.5, C_MED),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, C_ACCENT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())
    return story


# ── Section 15: Conclusion ────────────────────────────────────────────────────
def section_conclusion(styles):
    story = [Paragraph('15. Conclusion and Key Take-Aways', styles['section'])]
    story.append(HRFlowable(width=INNER_W, thickness=2, color=C_LIGHT, spaceAfter=8))

    story.append(Paragraph(
        'The field of elephant health medicine in India is rapidly evolving, driven by increasing '
        'human–elephant interface, expanding captive elephant populations, and the emergence of novel '
        'pathogens. This chapter has presented the major infectious, parasitic, and management-related '
        'diseases of Asian elephants, with emphasis on field-relevant diagnostic and treatment protocols.',
        styles['body']))
    story.append(Spacer(1, 0.2 * cm))

    takeaways = [
        '<b>1. EEHV</b> is the highest-priority disease for calves and young elephants — famciclovir must '
          'be pre-positioned; early clinical recognition saves lives.',
        '<b>2. Anthrax</b> requires zero-necropsy protocol in the field — burn all material; never bury.',
        '<b>3. Tuberculosis</b> is a chronic silent killer and a two-way zoonotic risk — '
          'mandatory surveillance of working elephants and their handlers.',
        '<b>4. Rabies</b> — brain is the only diagnostic sample; full PPE mandatory; '
          'post-exposure prophylaxis for exposed personnel.',
        '<b>5. HS and Clostridial</b> — bone marrow is the gold-standard postmortem sample; '
          'collect before lysis.',
        '<b>6. Parasites</b> — regular faecal examination and strategic deworming are the cornerstone of '
          'captive elephant health maintenance.',
        '<b>7. Documentation</b> — systematic photography, GPS recording and rapid lab submission '
          'are as important as the clinical intervention itself.',
        '<b>8. Preparedness</b> — every elephant camp and zoo should maintain a preparedness kit, '
          'an emergency contact tree, and a supply of pre-positioned drugs (famciclovir, anthrax '
          'vaccine, HS vaccine, broad-spectrum antibiotics).',
    ]
    story.append(info_box(takeaways, styles, title='Key Take-Aways for Field Veterinarians'))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph('Acknowledgements', styles['subsec']))
    ack = [
        '• <b>Resource Person:</b> Dr. M. Karikalan, MVSc, PhD — Assistant Professor, Dept. of Wildlife Science, '
          'Veterinary College & Research Institute (VBSC), Namakkal, Tamil Nadu',
        '• <b>Institutions acknowledged:</b> Centre for Wildlife Studies (CWL), ICAR-IVRI, Wildlife Institute of India (WII), '
          'Nandankanan Zoological Park, MTR Nilgiris, ERRC Surajpur (Chhattisgarh), Dudhwa National Park',
        '• <b>Workshop organisers:</b> Chhattisgarh Forest Department; Project Elephant Division, MoEF&CC; '
          'PCCF (Wildlife) Chhattisgarh State',
        '• <b>Sponsors & Partners:</b> Central Zoo Authority (CZA), MoEF&CC, Dr Parag Nigam (WII)',
    ]
    story.append(info_box(ack, styles, bg=colors.HexColor('#F0F8FF'), border=C_MED))
    story.append(Spacer(1, 0.3 * cm))

    # Acknowledgements page from PDF
    story.append(Paragraph('Figure 15.1 — Acknowledgements page from the source presentation',
                            styles['caption']))
    imgs = pdf_page_img(34, width=INNER_W * 0.7, styles=styles)
    story.extend(imgs)
    return story


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    out = '/home/user/Workshop-on-Conference/Workshop_Chapter3_Infectious_Diseases_2026.pdf'
    doc = SimpleDocTemplate(
        out,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.4 * cm, bottomMargin=1.2 * cm,
        title='Chapter 3 — Infectious Diseases of Asian Elephants · Workshop Notes 2026',
        author='Chhattisgarh Forest Department',
        subject='Workshop on Elephant Mortality Investigation and Management, Bilaspur 2026',
    )
    styles = make_styles()
    story = []
    story += cover_page(styles)
    story += section_introduction(styles)
    story += section_eehv(styles)
    story += section_rabies(styles)
    story += section_fmd(styles)
    story += section_pox_emcv(styles)
    story += section_tb(styles)
    story += section_anthrax(styles)
    story += section_hs(styles)
    story += section_clostridial(styles)
    story += section_lepto(styles)
    story += section_parasites(styles)
    story += section_surgical(styles)
    story += section_emerging(styles)
    story += section_field(styles)
    story += section_conclusion(styles)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    size_kb = os.path.getsize(out) // 1024
    print(f'Chapter 3 PDF written: {out} ({size_kb} KB)')


if __name__ == '__main__':
    build()

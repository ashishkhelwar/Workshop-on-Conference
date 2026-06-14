#!/usr/bin/env python3
"""
Generate Chapter 5: Non-Infectious Diseases in Asian Elephants
Based on notes from Dr. Karikalan Mathesh, ICAR-IVRI
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
C_DARK   = HexColor('#1B4332')   # deep forest green
C_MED    = HexColor('#2D6A4F')
C_LIGHT  = HexColor('#52B788')
C_TINT   = HexColor('#D8F3DC')
C_TINT2  = HexColor('#EAF7EE')
C_ORANGE = HexColor('#F4A261')
C_ORNG_L = HexColor('#FFF0E6')
C_RED    = HexColor('#C0392B')
C_RED_L  = HexColor('#FDECEA')
C_GOLD   = HexColor('#E9C46A')
C_BODY   = HexColor('#1A1A1A')
C_MUTED  = HexColor('#555555')
C_WHITE  = colors.white

PW, PH = A4

OUT = '/home/user/Workshop-on-Conference/Workshop_Chapter5_NonInfectious_Diseases_2026.pdf'


# ═══════════════════════════════════════════════════════════════════════════════
# Custom Flowables
# ═══════════════════════════════════════════════════════════════════════════════

class ChapterHeader(Flowable):
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
        c.setFillColor(C_DARK)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        c.setFillColor(C_LIGHT)
        c.rect(0, h - 6, w, 6, fill=1, stroke=0)
        c.setFillColor(C_LIGHT)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(14, h - 22, f'CHAPTER {self.chapter_num}')
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 17)
        c.drawString(14, h - 46, self.title)
        if self.subtitle:
            c.setFillColor(HexColor('#A8D5B5'))
            c.setFont('Helvetica', 10)
            c.drawString(14, h - 62, self.subtitle)
        if self.author:
            c.setFillColor(HexColor('#88BF9E'))
            c.setFont('Helvetica', 9)
            c.drawString(14, h - 79, self.author)
        c.setFillColor(HexColor('#88BF9E'))
        c.setFont('Helvetica', 8.5)
        c.drawString(14, 10,
            'Workshop on Essentials for Mortality Investigation of Asian Elephant  ·  '
            'Chhattisgarh Forest Department  ·  June 2026')


class SectionHeading(Flowable):
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
    def __init__(self, lines, title=None, width=None, warning=False, danger=False):
        Flowable.__init__(self)
        self.lines = lines if isinstance(lines, list) else [lines]
        self.title = title
        self._width = width
        self.warning = warning
        self.danger = danger

    def wrap(self, aw, ah):
        self.aw = self._width or aw
        line_h = 13
        self._h = (len(self.lines) * line_h) + (18 if self.title else 0) + 18
        return self.aw, self._h

    def draw(self):
        c = self.canv
        if self.danger:
            bg, border, bar = C_RED_L, C_RED, C_RED
            text_col = HexColor('#7B0D0D')
        elif self.warning:
            bg, border, bar = C_ORNG_L, C_ORANGE, C_ORANGE
            text_col = HexColor('#8B3A00')
        else:
            bg, border, bar = C_TINT, C_LIGHT, C_DARK
            text_col = C_DARK
        c.setFillColor(bg)
        c.roundRect(0, 0, self.aw, self._h, 4, fill=1, stroke=0)
        c.setStrokeColor(border)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, self.aw, self._h, 4, fill=0, stroke=1)
        c.setFillColor(bar)
        c.rect(0, 0, 4, self._h, fill=1, stroke=0)
        y = self._h - 13
        if self.title:
            c.setFont('Helvetica-Bold', 9.5)
            c.setFillColor(text_col)
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
    cell_ctr = ParagraphStyle('CellCtr', fontName='Helvetica', fontSize=8.8,
        textColor=C_BODY, alignment=TA_CENTER, leading=12)
    return dict(body=body, sub=sub, note=note, bullet=bullet,
                cell_hdr=cell_hdr, cell_body=cell_body, cell_bold=cell_bold,
                cell_ctr=cell_ctr)


# ═══════════════════════════════════════════════════════════════════════════════
# Table / helper utilities
# ═══════════════════════════════════════════════════════════════════════════════

def make_table(headers, rows, ST, col_widths=None, use_zebra=True, first_bold=True):
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([
            Paragraph(str(cell), ST['cell_bold'] if (j == 0 and first_bold) else ST['cell_body'])
            for j, cell in enumerate(row)
        ])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('TEXTCOLOR',  (0, 0), (-1, 0), C_WHITE),
        ('ALIGN',      (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
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


def center_table(headers, rows, ST, col_widths=None):
    """Table with all columns centred."""
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([Paragraph(str(c), ST['cell_ctr']) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_DARK),
        ('TEXTCOLOR',  (0, 0), (-1, 0), C_WHITE),
        ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',     (0, 0), (-1, -1), 'TOP'),
        ('GRID',       (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('LINEBELOW',  (0, 0), (-1, 0), 1.2, C_LIGHT),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_TINT2]),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
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
# PAGE TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(C_DARK)
    canvas.setLineWidth(1.5)
    canvas.line(doc.leftMargin, PH - doc.topMargin + 8,
                PW - doc.rightMargin, PH - doc.topMargin + 8)
    canvas.setFillColor(C_MED)
    canvas.setFont('Helvetica-Bold', 7.5)
    canvas.drawString(doc.leftMargin, PH - doc.topMargin + 11,
                      'Chapter 5: Non-Infectious Diseases in Asian Elephants')
    canvas.drawRightString(PW - doc.rightMargin, PH - doc.topMargin + 11,
                           'Dr. Karikalan Mathesh  ·  ICAR-IVRI')
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
    W = PW - 3.4 * cm

    # ── CHAPTER HEADER ────────────────────────────────────────────────────────
    story.append(ChapterHeader(
        '5',
        'Non-Infectious Diseases in Asian Elephants',
        'Toxicology, Electrocution, Nutritional Disorders & Field Investigation Framework',
        'Dr. Karikalan Mathesh, Senior Scientist  ·  Centre for Wildlife Conservation, '
        'Management & Disease Surveillance  ·  ICAR-IVRI, Bareilly'
    ))
    story.append(sp(14))

    # ── SECTION 1: WHY ELEPHANTS ARE BIOLOGICALLY DISTINCT ────────────────────
    story.append(KeepTogether([
        SectionHeading('1.  Background — Why Elephants Are Biologically Distinct'),
        sp(6),
        p('Asian elephants are physiologically unique in two seemingly contradictory respects: '
          'they are extraordinarily resistant to cancer, yet highly vulnerable to poisoning. '
          'Understanding both traits is essential for interpreting necropsy findings and '
          'identifying non-infectious causes of mortality.', ST),
        sp(6),
    ]))

    # Cancer resistance
    story.append(KeepTogether([
        SectionHeading('Cancer Resistance — Peto\'s Paradox', level=2),
        sp(6),
        p('Despite enormous body size and a 60–70 year lifespan (far more cells and far more '
          'time for mutations than in small animals), elephants have a <b>remarkably low '
          'incidence of cancer</b>. The key mechanism:', ST),
    ]))
    for line in [
        '<b>Multiple TP53 copies</b> — elephants carry <b>20+ copies</b> of the TP53 '
        'tumour-suppressor gene ("guardian of the genome"), compared with just <b>1 copy '
        'in humans</b>.',
        '<b>Enhanced DNA-damage detection</b> — more TP53 enables faster, more accurate '
        'identification of cellular DNA errors.',
        '<b>Stronger apoptotic response</b> — damaged cells are eliminated by programmed '
        'self-destruction before they can proliferate into tumours.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    # High toxicity susceptibility
    story.append(KeepTogether([
        SectionHeading('High Susceptibility to Toxicity', level=2),
        sp(6),
        p('The same large body that should theoretically raise cancer risk instead makes '
          'elephants <b>highly prone to poisoning</b>. Several converging factors explain this:', ST),
    ]))
    tox_factors = [
        ['Dysfunctional CYP genes',
         'Cytochrome P450 (CYP) genes are dysfunctional → limited ability to biotransform '
         'and detoxify ingested toxins'],
        ['Massive daily intake',
         'Adults consume 100–300 kg of vegetation per day; toxic plants, contaminated fodder, '
         'pesticides, and mycotoxins are ingested in large amounts'],
        ['High water consumption',
         '100–200 L of water per day — polluted sources expose them to heavy metals, '
         'pesticides, cyanobacterial and industrial toxins'],
        ['Hindgut fermenters',
         'Sudden diet changes or spoiled feed disrupt gut microbiota and increase endogenous '
         'toxin production'],
        ['Non-selective feeding',
         'Explore environment with the trunk; may consume unfamiliar plants, crops, garbage, '
         'or treated material without discrimination'],
        ['Drug sensitivity',
         'Extremely sensitive to certain veterinary drugs and anaesthetics; incorrect dosing '
         'can cause respiratory depression, cardiac failure, or death'],
        ['Pollutant accumulation',
         'Long lifespan (60–70 yrs) allows progressive build-up of heavy metals (lead, '
         'mercury, arsenic) and persistent organic pollutants'],
    ]
    story.append(sp(6))
    story.append(make_table(
        ['Risk Factor', 'Mechanism / Consequence'],
        tox_factors, ST,
        col_widths=[W * 0.28, W * 0.72],
    ))
    story.append(sp(12))

    # ── SECTION 2: CASE STUDY — BANDHAVGARH 2024 ──────────────────────────────
    story.append(SectionHeading('2.  Case Study — Mass Mortality at Bandhavgarh NP (Oct 2024)'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('History & Field Observations', level=2),
        sp(6),
        p('<b>Incident:</b> Sudden death of <b>10 elephants from a herd of 13</b> on '
          '<b>31 October 2024</b>. During forest-department patrolling, several elephants '
          'were found recumbent with weak respiration; some were already dead.', ST),
        sp(4),
        p('<b>Location:</b> Salkhania beats of Pataur and Khitauli Ranges, Bandhavgarh '
          'National Park (Tiger Reserve), Madhya Pradesh.', ST),
        sp(4),
    ]))
    for line in [
        '<b>Heavy rainfall</b> during October 2024.',
        '<b>Kodo millet crops were unharvested</b> near forest boundaries — a critical '
        'epidemiological clue linking the elephants to fungal-contaminated grain.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Clinical Signs & Gross Necropsy', level=2),
        sp(6),
        p('<b>Clinical progression:</b> respiratory distress → ataxia → weakness → '
          'incoordination → recumbency → rapid collapse.', ST),
        sp(6),
    ]))
    gross_rows = [
        ['Lungs', 'Congestion and oedema'],
        ['Liver', 'Enlarged, congested and swollen'],
        ['Kidneys', 'Congested'],
        ['Body cavities', 'Serosanguinous (blood-tinged) fluid accumulation'],
        ['Multiple organs', 'Congestion and haemorrhages throughout'],
        ['Heart', 'Pale necrotic foci on the myocardium'],
    ]
    story.append(make_table(
        ['Organ / Site', 'Gross Finding'],
        gross_rows, ST,
        col_widths=[W * 0.25, W * 0.75],
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Histopathology', level=2),
        sp(6),
    ]))
    histo_rows = [
        ['Heart', 'Acute myocardiopathy — degeneration, vacuolation and necrosis of cardiac myofibres'],
        ['Liver', 'Hepatocellular degeneration — centrilobular necrosis, fatty change'],
        ['Kidney', 'Renal tubular necrosis with epithelial degeneration'],
        ['General', 'Congestion, haemorrhage and oedema throughout multiple organs'],
    ]
    story.append(make_table(
        ['Tissue', 'Histopathological Finding'],
        histo_rows, ST,
        col_widths=[W * 0.18, W * 0.82],
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Sample Collection & Investigation Pathway', level=2),
        sp(6),
    ]))
    samp_rows = [
        ['Tissues in 10% NBF', 'Formalin fixation', 'Histopathology'],
        ['Tissues on ice + heart blood', 'Chilled', 'Disease screening (EEHV, EMCV, HS, Clostridium)'],
        ['Stomach contents, liver, kidney, heart, fat', '—', 'Toxicology'],
        ['Hair follicles / nails', '—', 'Toxicology (chronic exposure indicators)'],
        ['Environmental samples (water, feed, fodder, grain)', '—', 'Toxicology'],
    ]
    story.append(make_table(
        ['Sample', 'Preservation', 'Purpose'],
        samp_rows, ST,
        col_widths=[W * 0.36, W * 0.20, W * 0.44],
    ))
    story.append(sp(6))
    story.append(p('<b>Toxicological methods:</b> conventional tests → thin-layer '
                   'chromatography (TLC) → <b>liquid chromatography–mass spectrometry (LC-MS)</b>.', ST))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Toxicology Results', level=2),
        sp(6),
        p('<b>Negative</b> for: HCN, nitrate-nitrite, heavy metals, organophosphates, '
          'organochlorines, pyrethroids, carbamates.', ST),
        sp(4),
        p('<b>Negative</b> for infectious causes: EEHV, pasteurellosis, other mycotoxins.', ST),
        sp(4),
        p('<b>Positive — Cyclopiazonic acid (CPA)</b>: detected in all pooled samples at '
          '<b>&gt;100 ppb</b> (Ref. CAD-877/2024-25, dated 05-11-2024). Results indicated '
          'the elephants had consumed large quantities of Kodo plant/grains.', ST),
        sp(8),
    ]))

    story.append(SectionHeading('LC-MS Confirmation (ICRISAT, Hyderabad)', level=2))
    story.append(sp(6))
    story.append(p('23 samples received 6 November 2024. High CPA detected in stomach '
                   'contents, tissues, and millet samples:', ST))
    story.append(sp(6))
    cpa_rows = [
        ['Kodo grain with straw (range)', '~1,567 – 12,874'],
        ['K-2 (Kodo grain + straw)', '12,874'],
        ['K-5 (Kodo grain + straw)', '10,667'],
        ['Vomit sample (C3, Kodo millet)', '4,486'],
    ]
    story.append(center_table(
        ['Sample Description', 'CPA (ppb)'],
        cpa_rows, ST,
        col_widths=[W * 0.65, W * 0.35],
    ))
    story.append(sp(8))
    story.append(KeyBox([
        'DIAGNOSIS: Toxicosis — Kodo millet (cyclopiazonic acid) poisoning.',
        'Pathophysiology: CPA caused acute cardiac injury (myocardiopathy) → cardiac',
        'arrest / heart failure → passive venous congestion → hypoxia → degeneration of',
        'parenchymatous organs (liver, kidney, spleen). Findings correlate fully with',
        'necropsy gross lesions and laboratory results.',
    ], title='Final Diagnosis & Pathophysiology'))
    story.append(sp(12))

    # ── SECTION 3: CPA ────────────────────────────────────────────────────────
    story.append(SectionHeading('3.  Cyclopiazonic Acid (CPA) — Key Facts'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Source, Chemistry & Toxicity', level=2),
        sp(6),
    ]))
    for line in [
        '<b>Source plant:</b> <i>Paspalum scrobiculatum</i> (kodo / koda millet). Grown mainly '
        'in Nepal; also India, Philippines, Indonesia, Vietnam, Thailand. Originated in West Africa.',
        '<b>CPA is a mycotoxin</b> — a secondary metabolite of fungi <b><i>Aspergillus</i></b> '
        'and <b><i>Penicillium</i></b>. Kodo seed is particularly infected by '
        '<i>A. flavus</i> and <i>A. tamarii</i>.',
        '<b>Chemistry:</b> α-cyclopiazonic acid, an indole-tetramic acid; molar mass ≈ 336.39 g/mol; '
        'PubChem CID 54682463.',
        '<b>Key hazard:</b> Ripe kodo can become intermittently poisonous ("Kiruku Varagu") without '
        'any visible change — fitness for consumption cannot be judged by appearance alone.',
        '<b>First human report</b> linking CPA to kodua poisoning: Rao & Husain (1985), '
        '<i>Mycopathologia</i>.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Historical Precedent — 1933', level=2),
        sp(6),
        p('R.C. Morris, <i>J. Bombay Nat. Hist. Soc.</i> (1934) documented the death of '
          '<b>14 elephants</b> near Vannathiparai Reserve Forest (December 1933) from kodo millet '
          '("Varagu") poisoning. The traditional antidote was <b>tamarind-water or buttermilk in '
          'large quantities</b>; one of three elephants given water and tamarind reportedly survived '
          '(unconfirmed). This demonstrates that Kodo poisoning of elephants is a long-recognised, '
          'recurring problem.', ST),
        sp(8),
    ]))

    story.append(KeepTogether([
        SectionHeading('Prevention & Control', level=2),
        sp(6),
    ]))
    for i, line in enumerate([
        '<b>Regulate agriculture</b> and enhance monitoring of fungal-infected cropping systems '
        'near forest boundaries.',
        '<b>Community awareness</b> — engage farmers and livestock owners around the reserve.',
        '<b>Prevent elephant access</b> to contaminated, unharvested millet fields.',
        '<b>Scientific surveillance</b> and systematic monitoring of kodo crops.',
        '<b>Inter-departmental coordination</b> between forest, agriculture, and revenue departments.',
    ], 1):
        story.append(num(i, line, ST))
    story.append(sp(6))
    story.append(KeyBox([
        'Correlate history with necropsy; survey and destroy fungal-infected Kodo residue;',
        'keep domestic animals and wildlife out of affected fields; conduct cropping/ambient studies;',
        'determine the LD50 of CPA in domestic and wild animals.',
        'ONE HEALTH ALERT: Cattle in the area were also affected. Watch for symptoms in humans —',
        'Kodua poisoning is a recognised human mycotoxicosis.',
    ], title='Advisory & One Health Angle', warning=True))
    story.append(sp(12))

    # ── SECTION 4: OTHER NON-INFECTIOUS CAUSES ────────────────────────────────
    story.append(SectionHeading('4.  Other Major Non-Infectious Causes of Elephant Mortality'))
    story.append(sp(8))

    # 4A Electrocution
    story.append(KeepTogether([
        SectionHeading('A.  Electrocution (Electrical Injury)', level=2),
        sp(6),
        p('Electrocution is one of the most commonly reported non-infectious causes of elephant '
          'death in India, particularly from power lines and illegal electrified fences.', ST),
        sp(6),
        p('<b>Mechanisms of damage:</b>', ST),
    ]))
    for line in [
        '<b>Direct:</b> cell depolarisation, electroporation of cell membranes.',
        '<b>Indirect / thermal:</b> current generates heat → thermal burns and coagulative necrosis.',
        '<b>Secondary mechanical:</b> violent muscle contraction or cardiac arrest causes falls '
        'and crush injuries.',
        'Final common pathway: <b>cell death (necrosis) and organ failure</b>.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(SectionHeading('Comparison of Injury Patterns', level=2))
    story.append(sp(6))
    elec_rows = [
        ['Voltage', '>30,000,000 V', '>1,000 V', '<1,000 V'],
        ['Current', '>200,000 A', '<1,000 A', '<240 A'],
        ['Cardiac arrest', 'Asystole', 'Ventricular fibrillation', 'Ventricular fibrillation'],
        ['Muscle contraction', 'Single (single jolt)', 'Depends on duration', 'Tetanic (sustained)'],
        ['Burns', 'Rare, superficial', 'Common, deep', 'Usually superficial'],
        ['Rhabdomyolysis', 'Uncommon', 'Very common', 'Common'],
        ['Mortality', 'Very high', 'Moderate', 'Low'],
    ]
    story.append(center_table(
        ['Feature', 'Lightning', 'High Voltage (>1 kV)', 'Low Voltage (<1 kV)'],
        elec_rows, ST,
        col_widths=[W * 0.26, W * 0.22, W * 0.28, W * 0.24],
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Current Magnitude & Physiological Effect', level=2),
        sp(6),
        p('Reference thresholds (general): 3 mA — noticeable shock; 10 mA — muscular contractions; '
          '30 mA — respiratory paralysis; 50 mA — heart paralysis (may be fatal); '
          '100 mA — ventricular fibrillation (fatal); 4 A — heart paralysis (fatal); '
          '5 A — tissue burning.', ST),
        sp(6),
        p('<b>Tissue resistance</b> determines the path and extent of injury. Nerves, blood, '
          'mucous membranes, and muscle have low resistance (higher injury). Tendons, fat, '
          'and bone have high resistance and are relatively spared.', ST),
        sp(8),
    ]))

    story.append(KeepTogether([
        SectionHeading('Field Findings & Post-Mortem Clues', level=2),
        sp(6),
        p('Of 10 reported electrocution cases in elephants: <b>6 from direct power-line '
          'contact (440–220 V)</b>, <b>4 from electrified fences</b>. Affected states: '
          'Uttar Pradesh (4), Tamil Nadu / Mudumalai NP (2), Uttarakhand (2), '
          'Chhattisgarh (2).', ST),
        sp(6),
    ]))
    for line in [
        '<b>Very rapid decomposition</b> and quick or absent rigor mortis.',
        '<b>Lightning / burn marks</b> — charred skin, lacerations along the current path '
        '(e.g. trunk burns in the Dudhwa NP case).',
    ]:
        story.append(b(line, ST))
    story.append(sp(12))

    # 4B Lightning
    story.append(KeepTogether([
        SectionHeading('B.  Lightning Side-Potential (Herd Mortality)', level=2),
        sp(6),
        p('A ground-strike lightning event creates a high-voltage point; current then spreads '
          'radially outward through the ground for <b>up to 100 m or more</b>. Elephants '
          'standing or lying on the ground become part of the electrical circuit. Current '
          'passes through the body between front and rear feet → <b>instant internal organ '
          'failure and death — without any direct lightning strike</b>. This mechanism '
          'explains multiple simultaneous deaths in closely grouped herds.', ST),
        sp(6),
    ]))
    story.append(KeyBox([
        'High-risk conditions: open grasslands, proximity to water bodies, thunderstorms,',
        'and tightly grouped herds.',
        'Documented in Assam (pre-monsoon / monsoon season).',
        'Investigate GPS clustering of carcasses and weather/storm records immediately.',
    ], title='Field Clue — Lightning Side-Potential'))
    story.append(sp(12))

    # 4C Infighting
    story.append(KeepTogether([
        SectionHeading('C.  Infighting / Tusk Injuries', level=2),
        sp(6),
        p('Penetrating tusk wounds from intraspecific combat are a recognised non-infectious '
          'cause of elephant mortality, particularly in adult males. Post-mortem examination '
          'reveals deep puncture wounds, haemorrhage, and secondary infection. '
          '(e.g. Najibabad Forest Division, Uttar Pradesh.)', ST),
        sp(12),
    ]))

    # 4D Nutritional
    story.append(KeepTogether([
        SectionHeading('D.  Nutritional Deficiencies', level=2),
        sp(6),
        p('Nutritional deficiency disease can be <b>primary</b> (inadequate dietary supply) '
          'or <b>secondary</b>, caused by one of several interfering mechanisms:', ST),
        sp(4),
    ]))
    nutr_rows = [
        ['Interference with intake', 'Pain on eating, dental disorders, jaw disease'],
        ['Interference with absorption', 'Chronic intestinal disease, parasitism, dysbiosis'],
        ['Interference with storage / utilization',
         'Liver disease impairing vitamin storage and metabolism'],
        ['Increased excretion', 'Renal disease, diarrhoea, heavy parasite burden'],
        ['Increased requirements', 'Pregnancy, lactation, rapid growth in calves'],
        ['Anti-nutritional substances',
         'Dietary inhibitors (e.g. phytates, oxalates) blocking nutrient uptake'],
    ]
    story.append(make_table(
        ['Mechanism of Secondary Deficiency', 'Examples / Notes'],
        nutr_rows, ST,
        col_widths=[W * 0.38, W * 0.62],
    ))
    story.append(sp(8))
    story.append(KeepTogether([
        p('<b>Clinical examples in elephants:</b>', ST),
        sp(4),
    ]))
    for line in [
        '<b>Hypocalcaemic tetany</b> and <b>rickets</b> / bone disorders (e.g. "Yogi" at '
        'Rajaji NP, Dehradun).',
        '<b>Corneal opacity and cataract</b> — chronic micronutrient deficiency.',
        '<b>Overgrown, cracked nails</b> and <b>cracked foot pads</b> — chronic nutritional '
        'and management deficiency in captive or managed animals.',
    ]:
        story.append(b(line, ST))
    story.append(sp(12))

    # 4E Decomposition
    story.append(KeepTogether([
        SectionHeading('E.  Advanced Decomposition / Skeletonization', level=2),
        sp(6),
        p('Late-discovered carcasses (e.g. Amangarh Tiger Reserve, Bijnor) substantially '
          'limit diagnostic yield. Advanced autolysis and scavenging destroy soft tissue '
          'lesions, preclude sampling for microbiology and virology, and compromise '
          'toxicological analysis. This underscores the critical importance of '
          '<b>early detection, rapid reporting, and prompt necropsy</b>.', ST),
        sp(12),
    ]))

    # ── SECTION 5: FIELD INVESTIGATION FRAMEWORK ──────────────────────────────
    story.append(SectionHeading('5.  Field Investigation Framework — Exam-Ready Checklist'))
    story.append(sp(8))
    story.append(p('When facing a suspected wildlife disease outbreak or mass mortality event, '
                   'the wildlife veterinarian must be able to address these six areas:', ST))
    story.append(sp(6))

    checklist = [
        ['1. First Response',
         'Secure the site. Ensure personnel safety and PPE. Notify field director and '
         'authorities. Prevent further access/exposure. Barricade and photograph the scene.'],
        ['2. Initial Field Investigation',
         'Record complete history: time of onset, clinical signs observed, GPS coordinates, '
         'environmental context (recent rainfall, crops nearby, water sources). Note '
         'scavenger activity and any other species affected (One Health).'],
        ['3. Essential Requirements',
         'PPE and biosafety kit; necropsy and sampling kit (scalpels, forceps, containers); '
         'cold chain (ice box, gel packs); fixatives (10% NBF vials); documentation '
         '(camera, field book); labelled containers; transport logistics and lab contacts.'],
        ['4. Samples for the Laboratory',
         'Fixed tissues for histopathology; chilled tissues + heart blood for disease '
         'screening; stomach contents, liver, kidney, heart, fat, hair/nails for toxicology; '
         'environmental water, feed, fodder, grain.'],
        ['5. Differential Diagnoses',
         'Infectious: EEHV, Pasteurellosis/HS, EMCV, clostridial disease.\n'
         'Toxic: mycotoxins/CPA, HCN, nitrate-nitrite, pesticides, heavy metals.\n'
         'Physical: electrocution, lightning side-potential, tusk injuries.\n'
         'Nutritional/metabolic deficiency.'],
        ['6. Prevention & Control',
         'Apply the five-point plan (regulate agriculture, community awareness, prevent '
         'access, scientific surveillance, inter-departmental coordination). Operate under '
         'a One Health framework linking wildlife, livestock, and human health.'],
    ]
    story.append(make_table(
        ['Area', 'Key Actions / Considerations'],
        checklist, ST,
        col_widths=[W * 0.20, W * 0.80],
    ))
    story.append(sp(12))

    # ── SECTION 6: KEY TAKEAWAYS ───────────────────────────────────────────────
    story.append(SectionHeading('6.  Key Takeaways'))
    story.append(sp(8))
    story.append(KeyBox([
        '1. Elephants resist CANCER (20+ TP53 copies) but are highly VULNERABLE TO TOXINS',
        '   (dysfunctional CYP genes + massive daily intake of vegetation and water).',
        '2. The Bandhavgarh 2024 die-off was toxicosis from cyclopiazonic acid (CPA) in',
        '   fungal-infected, unharvested Kodo millet after heavy rains — confirmed by LC-MS.',
        '3. Lesion pattern: acute myocardiopathy → circulatory failure → multi-organ',
        '   hypoxic/toxic degeneration (liver, kidney, spleen).',
        '4. Kodo millet poisoning is historically documented (since 1933) and has One Health',
        '   relevance: cattle and humans in the same area are also at risk.',
        '5. Other leading non-infectious causes in India: electrocution (power lines &',
        '   fences), lightning side-potential (herd deaths), infighting, and nutritional',
        '   / metabolic deficiencies.',
        '6. Early detection, prompt necropsy, and complete sampling are essential — late-',
        '   stage decomposition destroys diagnostic evidence.',
    ], title='Chapter Summary — Non-Infectious Diseases in Asian Elephants'))

    return story


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=1.7 * cm, rightMargin=1.7 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title='Chapter 5: Non-Infectious Diseases in Asian Elephants',
        author='Dr. Karikalan Mathesh, ICAR-IVRI',
    )
    ST = make_styles()
    story = build_story(ST)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    main()

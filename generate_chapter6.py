#!/usr/bin/env python3
"""
Generate Chapter 6: Non-Infectious Pathology in Asian Elephants
Based on notes from Prof. Dr. A. B. Shrivastava, NDVSU Jabalpur
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable

C_DARK   = HexColor('#1B4332')
C_MED    = HexColor('#2D6A4F')
C_LIGHT  = HexColor('#52B788')
C_TINT   = HexColor('#D8F3DC')
C_TINT2  = HexColor('#EAF7EE')
C_ORANGE = HexColor('#F4A261')
C_ORNG_L = HexColor('#FFF0E6')
C_RED    = HexColor('#C0392B')
C_RED_L  = HexColor('#FDECEA')
C_BODY   = HexColor('#1A1A1A')
C_MUTED  = HexColor('#555555')
C_WHITE  = colors.white

PW, PH = A4
OUT = '/home/user/Workshop-on-Conference/Workshop_Chapter6_NonInfectious_Pathology_2026.pdf'


# ── Custom Flowables ──────────────────────────────────────────────────────────

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
        self._h = (len(self.lines) * 13) + (18 if self.title else 0) + 18
        return self.aw, self._h

    def draw(self):
        c = self.canv
        if self.danger:
            bg, border, bar, tc = C_RED_L, C_RED, C_RED, HexColor('#7B0D0D')
        elif self.warning:
            bg, border, bar, tc = C_ORNG_L, C_ORANGE, C_ORANGE, HexColor('#8B3A00')
        else:
            bg, border, bar, tc = C_TINT, C_LIGHT, C_DARK, C_DARK
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
            c.setFillColor(tc)
            c.drawString(12, y, self.title)
            y -= 15
        c.setFont('Helvetica', 9)
        c.setFillColor(C_BODY)
        for line in self.lines:
            c.drawString(12, y, line)
            y -= 13


# ── Styles ────────────────────────────────────────────────────────────────────

def make_styles():
    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=10,
        textColor=C_BODY, alignment=TA_JUSTIFY, leading=14.5, spaceAfter=5)
    bullet = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=9.8,
        textColor=C_BODY, leading=14, leftIndent=14, spaceAfter=3, alignment=TA_JUSTIFY)
    note = ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=9,
        textColor=C_MUTED, leading=13, spaceAfter=4)
    cell_hdr = ParagraphStyle('CellHdr', fontName='Helvetica-Bold', fontSize=9,
        textColor=C_WHITE, alignment=TA_CENTER, leading=12)
    cell_body = ParagraphStyle('CellBody', fontName='Helvetica', fontSize=8.8,
        textColor=C_BODY, alignment=TA_LEFT, leading=12)
    cell_bold = ParagraphStyle('CellBold', fontName='Helvetica-Bold', fontSize=8.8,
        textColor=C_DARK, alignment=TA_LEFT, leading=12)
    cell_ctr = ParagraphStyle('CellCtr', fontName='Helvetica', fontSize=8.8,
        textColor=C_BODY, alignment=TA_CENTER, leading=12)
    return dict(body=body, bullet=bullet, note=note,
                cell_hdr=cell_hdr, cell_body=cell_body,
                cell_bold=cell_bold, cell_ctr=cell_ctr)


# ── Table helpers ─────────────────────────────────────────────────────────────

def make_table(headers, rows, ST, col_widths=None, first_bold=True):
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([
            Paragraph(str(cell), ST['cell_bold'] if (j == 0 and first_bold) else ST['cell_body'])
            for j, cell in enumerate(row)
        ])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), C_DARK),
        ('TEXTCOLOR',     (0, 0), (-1, 0), C_WHITE),
        ('ALIGN',         (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('GRID',          (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('LINEBELOW',     (0, 0), (-1, 0), 1.2, C_LIGHT),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [C_WHITE, C_TINT2]),
        ('LEFTPADDING',   (0, 0), (-1, -1), 5),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 5),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def two_col_table(left_hdr, right_hdr, rows, ST, col_widths, left_color=C_MED):
    """Two-column comparison table (e.g. Do/Don't, term/meaning)."""
    data = [[Paragraph(left_hdr, ST['cell_hdr']),
             Paragraph(right_hdr, ST['cell_hdr'])]]
    for row in rows:
        data.append([Paragraph(str(row[0]), ST['cell_bold']),
                     Paragraph(str(row[1]), ST['cell_body'])])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), C_DARK),
        ('TEXTCOLOR',     (0, 0), (-1, 0), C_WHITE),
        ('ALIGN',         (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('GRID',          (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('LINEBELOW',     (0, 0), (-1, 0), 1.2, C_LIGHT),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [C_WHITE, C_TINT2]),
        ('LEFTPADDING',   (0, 0), (-1, -1), 5),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 5),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def sp(n=6):   return Spacer(1, n)
def p(t, ST):  return Paragraph(t, ST['body'])
def b(t, ST):  return Paragraph(f'• {t}', ST['bullet'])
def num(n, t, ST): return Paragraph(f'<b>{n}.</b> {t}', ST['bullet'])


# ── Page template ─────────────────────────────────────────────────────────────

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(C_DARK)
    canvas.setLineWidth(1.5)
    canvas.line(doc.leftMargin, PH - doc.topMargin + 8,
                PW - doc.rightMargin, PH - doc.topMargin + 8)
    canvas.setFillColor(C_MED)
    canvas.setFont('Helvetica-Bold', 7.5)
    canvas.drawString(doc.leftMargin, PH - doc.topMargin + 11,
                      'Chapter 6: Non-Infectious Pathology in Asian Elephants')
    canvas.drawRightString(PW - doc.rightMargin, PH - doc.topMargin + 11,
                           'Prof. Dr. A. B. Shrivastava  ·  NDVSU, Jabalpur')
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


# ── Content ───────────────────────────────────────────────────────────────────

def build_story(ST):
    story = []
    W = PW - 3.4 * cm

    # CHAPTER HEADER
    story.append(ChapterHeader(
        '6',
        'Non-Infectious Pathology in Asian Elephants',
        'Poisoning, Electrocution, Reproductive & Metabolic Disorders',
        'Prof. Dr. A. B. Shrivastava, Founder Director  ·  School of Wildlife Forensic and Health  ·  '
        'Nanaji Deshmukh Veterinary Science University, Jabalpur (M.P.)'
    ))
    story.append(sp(14))

    # ── SECTION 1: ELEPHANT POISONING IN INDIA ────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('1.  Elephant Poisoning in India — Overview'),
        sp(6),
        p('Poisoning is one of the most severe threats to <b>pachyderms</b> — the large, '
          'thick-skinned mammals including elephants, rhinoceroses, and hippopotamuses. '
          'In India, unnatural causes such as electrocution and poisoning claim hundreds of '
          'elephant lives every year. Incidents arise primarily from human–wildlife conflict '
          'and illegal poaching, and parallel patterns are seen in Africa.', ST),
        sp(6),
    ]))
    story.append(two_col_table(
        'Route', 'Examples & Context',
        [
            ['Intentional',
             'Illegal poaching; retaliatory killing in human–elephant conflict areas. '
             'Deliberate placement of poisoned bait or contaminated food near crop fields.'],
            ['Accidental',
             'Elephants consuming mycotoxin-infected crops (e.g. kodo millet); '
             'drinking from algae-bloom water bodies; ingesting toxic plants unknowingly.'],
        ],
        ST, col_widths=[W * 0.22, W * 0.78],
    ))
    story.append(sp(12))

    # ── SECTION 2: MYCOTOXINS & BIOLOGICAL TOXINS ────────────────────────────
    story.append(SectionHeading('2.  Mycotoxins & Biological Toxins'))
    story.append(sp(8))

    # 2a Crop-borne mycotoxins
    story.append(KeepTogether([
        SectionHeading('A.  Crop-Borne Mycotoxins (CPA / Kodo Millet)', level=2),
        sp(6),
        p('Elephants raiding farm fields are highly susceptible to <b>mycotoxins</b> — '
          'secondary metabolites of moulds. The most clinically significant is '
          '<b>Cyclopiazonic Acid (CPA)</b>, produced by <i>Aspergillus</i> and '
          '<i>Penicillium</i> species infecting <b>kodo millet</b> crops.', ST),
        sp(6),
        p('<b>Pathological effects:</b> acute vascular damage, liver necrosis, and '
          'kidney necrosis, ultimately leading to multi-organ failure and death.', ST),
        sp(6),
    ]))
    story.append(KeyBox([
        'Key case — Bandhavgarh Tiger Reserve, MP: A herd of 13 elephants raided kodo',
        'millet crops; 10 elephants died. Forensic post-mortem and lab investigation',
        'confirmed accidental toxicity from fungal mycotoxins in infected crop.',
        '(Speaker note: 2 similar cases personally seen/treated in KTR camp elephants, 1997–98.)',
    ], title='Bandhavgarh Case Reference'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('When Does Contamination Occur?', level=2),
        sp(6),
        p('<b>Heavy or unseasonal rainfall</b> coinciding with grain maturation/harvest creates '
          'moist, warm conditions ideal for fungal colonisation. Unharvested grain in '
          'standing fields carries the highest risk.', ST),
        sp(6),
        p('<b>Management & Prevention:</b>', ST),
    ]))
    for i, line in enumerate([
        '<b>Good agricultural practices</b> — correct spacing, timely harvesting, and '
        'minimising field duration after maturity.',
        '<b>Biocontrol agents</b> — application of non-toxigenic fungal strains '
        '(<i>Aspergillus</i> spp.) to competitively exclude toxin-producing strains.',
        '<b>Post-harvest handling</b> — thorough drying and airtight storage to prevent '
        'moisture-driven fungal re-growth.',
    ], 1):
        story.append(num(i, line, ST))
    story.append(sp(10))

    # 2b Cyanotoxins
    story.append(KeepTogether([
        SectionHeading('B.  Cyanotoxins / Cyanobacteria', level=2),
        sp(6),
        p('<b>Toxic blue-green algae (cyanobacteria)</b> proliferate in stagnant, warm, '
          'nutrient-rich water bodies during <b>hot, dry seasons</b>. Dense blooms '
          'produce potent <b>neurotoxins and hepatotoxins</b> that can cause fatal '
          'mass die-offs — especially at elephant watering holes where large volumes '
          'of contaminated water are consumed rapidly.', ST),
        sp(8),
    ]))

    # 2c Toxic plants
    story.append(KeepTogether([
        SectionHeading('C.  Toxic Plants', level=2),
        sp(6),
        p('Elephants generally avoid toxic vegetation through learned behaviour, but '
          'unfamiliar environments, food scarcity, or captivity can lead to accidental '
          'ingestion. Key examples:', ST),
        sp(4),
    ]))
    plant_rows = [
        ['Oleander (<i>Nerium oleander</i>)',
         'Cardiac glycosides → fatal arrhythmia and cardiac arrest',
         'Cardiac'],
        ['Certain weeds / unfamiliar plants',
         'Variable alkaloids, glycosides → neurological signs',
         'Neurological'],
        ['Calcium oxalate plants\n(e.g. <i>Dieffenbachia</i>, aroids)',
         'Crystal penetration of oral/GI mucosa → intense swelling, irritation, and systemic distress if eaten in quantity',
         'Mechanical + systemic'],
    ]
    story.append(make_table(
        ['Plant / Group', 'Toxic Mechanism & Effect', 'System Affected'],
        plant_rows, ST,
        col_widths=[W * 0.26, W * 0.50, W * 0.24],
    ))
    story.append(sp(12))

    # ── SECTION 3: HCN POISONING ──────────────────────────────────────────────
    story.append(SectionHeading('3.  Hydrocyanic Acid (HCN) Poisoning'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Source & Risk Factors', level=2),
        sp(6),
        p('<b>Cyanogenic glycosides</b> in <b>jowar / sorghum (<i>Sorghum bicolor</i>)</b> '
          'are hydrolysed to release HCN (prussic acid). Risk is highest in:', ST),
        sp(4),
    ]))
    for line in [
        '<b>Young, rapidly growing plants</b> — glycoside content peaks before maturity.',
        '<b>Stunted or stressed plants</b> — e.g. following drought then autumn rains.',
        '<b>Leaves and stalks</b> — contain far more glycoside than grain.',
        'Feeding elephants <b>large, unfamiliar quantities</b> of fresh jowar at once '
        '(especially when regular feed is unavailable).',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Case Study — 5 Captive Elephants (Circus, Jabalpur)', level=2),
        sp(6),
        p('<i>Reference: Zoo Print, Vol. XXV, 6 June 2010.</i>', ST),
        sp(4),
        p('Five circus elephants were fed large quantities of fresh jowar (unavailability '
          'of regular feed). They developed <b>restlessness and diarrhoea</b>; routine '
          'anti-diarrhoeal treatment failed and condition worsened. HCN poisoning was '
          'suspected and the following treatment was instituted:', ST),
        sp(4),
    ]))
    treat_rows = [
        ['Step 1', 'Stopped jowar feeding immediately.'],
        ['Step 2', 'Dextrose saline (8–10 L) + 30 mL multivitamin injection (MVI) via ear vein.'],
        ['Step 3', 'Sodium thiosulphate (50 g) dissolved in water, given orally as antidote.'],
        ['Step 4', 'Treatment repeated at approximately 12-hour intervals.'],
        ['Step 5 (critical cases)',
         'Additional doses + cold dextrose saline + small ice pieces + Tab. Diadin per rectum.'],
        ['Outcome', 'Recovery achieved; all animals resumed drinking and grazing.'],
    ]
    story.append(make_table(
        ['Step', 'Action'],
        treat_rows, ST,
        col_widths=[W * 0.14, W * 0.86],
    ))
    story.append(sp(6))
    story.append(KeyBox([
        'Lesson: HCN poisoning here was accidental — caused by feeding large amounts of',
        'unfamiliar sorghum to elephants not accustomed to it, due to non-availability of',
        'regular food. Sodium thiosulphate is the key antidote (converts cyanide to thiocyanate).',
    ], title='Key Learning Point', warning=True))
    story.append(sp(12))

    # ── SECTION 4: ELECTROCUTION ──────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('4.  Electrocution'),
        sp(6),
        p('<b>Electrocution</b> is death or severe injury caused by an electric shock. '
          'The body becomes part of an electrical circuit; high voltage or current disrupts '
          'the body\'s natural electrical systems, commonly triggering '
          '<b>cardiac arrest or severe electrical burns</b>.', ST),
        sp(6),
    ]))
    story.append(two_col_table(
        'Term', 'Definition',
        [
            ['Electric Shock',
             'Physical sensation or injury from electricity — muscle spasms, minor burns. '
             'NON-FATAL.'],
            ['Electrocution',
             'An electric shock that is FATAL. The term implies death as the outcome.'],
        ],
        ST, col_widths=[W * 0.28, W * 0.72],
    ))
    story.append(sp(6))
    story.append(p('<i>A documented case of elephant electrocution was recorded in November 2020.</i>',
                   ST))
    story.append(sp(12))

    # ── SECTION 5: PYOMETRA ───────────────────────────────────────────────────
    story.append(SectionHeading('5.  Pyometra'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Definition & Affected Population', level=2),
        sp(6),
        p('Pyometra is a severe, life-threatening <b>uterine infection</b> marked by '
          'accumulation of pus and suppurative inflammation of the uterus. '
          'It occurs most commonly in <b>aging, nulliparous (never-given-birth) '
          'female elephants</b> and is linked to prolonged hormonal fluctuations '
          'and underlying reproductive issues.', ST),
        sp(8),
    ]))

    story.append(KeepTogether([
        SectionHeading('Causes & Pathophysiology', level=2),
        sp(6),
    ]))
    pyom_rows = [
        ['Hormonal changes',
         'Fluctuating progesterone levels → abnormally thickened uterine lining (endometrial '
         'hyperplasia) creates a nutrient-rich environment for bacterial growth.'],
        ['Bacterial infection',
         'Secondary invasion by organisms such as <i>E. coli</i> or '
         '<i>Enterococcus faecium</i> → suppurative inflammation and pus accumulation.'],
        ['Pre-existing conditions',
         'Cystic endometrial hyperplasia or benign tumours (leiomyomas) in older '
         'captive females predispose to pyometra.'],
    ]
    story.append(make_table(
        ['Factor', 'Mechanism / Details'],
        pyom_rows, ST,
        col_widths=[W * 0.26, W * 0.74],
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Treatment', level=2),
        sp(6),
    ]))
    for i, line in enumerate([
        '<b>Hormonal downregulation</b> — GnRH vaccines (e.g. Improvac) or Deslorelin '
        'implants to suppress reproductive cycles and reduce endometrial stimulation.',
        '<b>Aggressive antibiotic therapy</b> — broad-spectrum systemic antibiotics '
        'targeting specific isolated pathogens.',
        '<b>Uterine lavage</b> — flushing and draining the uterus to remove accumulated pus.',
        '<b>Homeopathic adjunct protocol practised:</b> Pyrogenium 1000 + Hepar Sulph 1000 '
        '+ Secale 1000.',
    ], 1):
        story.append(num(i, line, ST))
    story.append(sp(4))
    story.append(p('<i>Surgical management: vaginal vestibulotomy has been performed in '
                   'Asian elephant cases.</i>', ST))
    story.append(sp(12))

    # ── SECTION 6: HYPERTHERMIA ────────────────────────────────────────────────
    story.append(SectionHeading('6.  Hyperthermia'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Why Elephants Are Prone to Overheating', level=2),
        sp(6),
        p('Hyperthermia is a life-threatening condition arising from high environmental '
          'temperature, lack of access to water/shade, massive body volume, and the '
          'absence of conventional sweat glands. Three converging factors explain '
          'the heightened risk in elephants:', ST),
        sp(6),
    ]))
    heat_rows = [
        ['Square-Cube Law',
         'As body volume increases, metabolic heat production scales faster than the '
         'relatively smaller skin surface area available to dissipate it. Large size = '
         'excellent heat retention, poor heat loss.'],
        ['No sweat glands',
         'Elephants lack traditional eccrine sweat glands; only pores between the toes '
         'are present. They depend on transepidermal water loss through the skin — '
         'which requires ready access to drinking water.'],
        ['Continuous metabolic heat',
         'Sustained walking or exertion in direct sun generates metabolic heat faster '
         'than passive cooling can remove it, triggering hyperthermia in the absence '
         'of active cooling behaviour.'],
    ]
    story.append(make_table(
        ['Risk Factor', 'Explanation'],
        heat_rows, ST,
        col_widths=[W * 0.24, W * 0.76],
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Natural Cooling Mechanisms', level=2),
        sp(6),
    ]))
    for line in [
        '<b>Ear flapping</b> — the large, heavily vascularised pinnae act as thermal '
        'radiators. Rapid flapping increases convective heat loss from blood circulating '
        'through the ears, lowering overall body temperature.',
        '<b>Wallowing and water/mud spraying</b> — immersion or spraying with water '
        'provides powerful evaporative cooling; a residual mud coat shields the skin '
        'from solar radiation (natural sunscreen).',
        '<b>Saliva spraying</b> — self-spraying with trunk-collected saliva adds '
        'evaporative surface cooling.',
        '<b>Increased skin permeability</b> — the hide becomes more permeable during '
        'heat stress, allowing greater transepidermal evaporative cooling — but only '
        'if adequate drinking water is available.',
    ]:
        story.append(b(line, ST))
    story.append(sp(6))
    story.append(KeyBox([
        'Intervention: Provide unlimited cool drinking water and shade immediately.',
        'Apply cold water sprays to the skin, behind the ears, and on the feet.',
        'Move the animal out of direct sun; reduce physical exertion.',
        'In severe cases: cold dextrose saline IV, ice packs to ear margins.',
    ], title='Management of Hyperthermia', warning=True))
    story.append(sp(12))

    # ── SECTION 7: IRON DEFICIENCY ANAEMIA ────────────────────────────────────
    story.append(SectionHeading('7.  Iron Deficiency Anaemia'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Clinical Features & Diagnosis', level=2),
        sp(6),
        p('<b>Definition:</b> Qualitative and quantitative reduction in circulating red '
          'blood cells and haemoglobin. In elephants, chronic dietary deficiency or '
          'parasitism are common underlying causes.', ST),
        sp(6),
    ]))
    anaemia_rows = [
        ['Pale mucous membranes', 'Reduced haemoglobin → less colour in conjunctiva, oral mucosa'],
        ['Extreme weakness', 'Reduced oxygen-carrying capacity → poor cellular energy production'],
        ['Inability to walk / slow movement', 'Muscle hypoxia; severe cases cannot rise'],
        ['Blood smear — target cells', 'RBCs show central pallor with dense peripheral rim ("target cell" morphology'],
        ['Microcytic hypochromic RBCs', 'Small, pale cells on haematology — hallmark of iron-deficiency anaemia'],
        ['Low haemoglobin (Hb)', 'Confirmed on complete blood count (CBC)'],
    ]
    story.append(make_table(
        ['Finding', 'Significance'],
        anaemia_rows, ST,
        col_widths=[W * 0.36, W * 0.64],
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Treatment', level=2),
        sp(6),
    ]))
    for i, line in enumerate([
        '<b>Diet restoration</b> — full normal elephant ration: soyabeans, horse gram, '
        'napier grass, bamboo, leaves, grains, seasonal fruits.',
        '<b>Iron supplementation</b> — natural sources: jaggery (rich in iron), honey; '
        'plus oral or parenteral iron preparations as indicated.',
        '<b>Vitamin B12 injections</b> — essential cofactor for RBC maturation.',
        '<b>Multivitamin and mineral mixture</b> supplementation to correct '
        'concurrent micro-nutrient gaps.',
    ], 1):
        story.append(num(i, line, ST))
    story.append(sp(12))

    # ── SECTION 8: SUMMARY TABLE ──────────────────────────────────────────────
    story.append(SectionHeading('8.  Quick Reference — Conditions Covered'))
    story.append(sp(6))
    summary_rows = [
        ['Kodo millet poisoning',  'Toxic / mycotoxin',    'CPA from <i>Aspergillus</i>/<i>Penicillium</i>',
         'Liver/kidney necrosis, cardiac failure, rapid death'],
        ['HCN poisoning',          'Toxic / plant',        'Cyanogenic glycosides in sorghum/jowar',
         'Restlessness, diarrhoea, respiratory distress'],
        ['Cyanotoxins',            'Toxic / environmental','Cyanobacterial blooms in stagnant water',
         'Neuro- and hepatotoxicosis; mass die-offs'],
        ['Plant toxicity',         'Toxic / plant',        'Oleander (cardiac), calcium oxalate plants',
         'Cardiac arrhythmia, neurological signs, GI irritation'],
        ['Electrocution',          'Physical',             'Power-line / electrified-fence contact',
         'Cardiac arrest, burns; rapid decomposition post-mortem'],
        ['Pyometra',               'Reproductive',         'Hormonal + bacterial (uterine)',
         'Uterine pus, systemic sepsis; older captive females'],
        ['Hyperthermia',           'Thermal / metabolic',  'High temperature + no sweat glands',
         'Collapse, organ failure; respond to cooling measures'],
        ['Iron deficiency anaemia','Nutritional',          'Poor diet, parasitism, chronic disease',
         'Pale mucosae, weakness, microcytic hypochromic RBCs'],
    ]
    story.append(make_table(
        ['Condition', 'Category', 'Key Agent / Trigger', 'Hallmark Finding'],
        summary_rows, ST,
        col_widths=[W * 0.22, W * 0.17, W * 0.28, W * 0.33],
        first_bold=True,
    ))
    story.append(sp(14))

    # KEY TAKEAWAYS
    story.append(SectionHeading('Key Takeaways'))
    story.append(sp(8))
    story.append(KeyBox([
        '1. Elephant poisoning is both intentional (retaliation/poaching) and accidental',
        '   (mycotoxins, toxic plants, algal blooms) — field history is critical to distinguish.',
        '2. CPA from kodo millet is the most documented mycotoxin killing wild elephants',
        '   in India; heavy rainfall + unharvested grain = highest risk.',
        '3. HCN from jowar is treatable with sodium thiosulphate — suspect when standard',
        '   anti-diarrhoeal therapy fails after recent sorghum feeding.',
        '4. Electrocution means death; distinguish from non-fatal electric shock at necropsy',
        '   (burn marks, rapid decomposition, absent rigor mortis).',
        '5. Pyometra targets aging, nulliparous captive females — hormonal + antibiotic',
        '   treatment; surgical vestibulotomy in severe cases.',
        '6. Hyperthermia is unique to large-bodied, sweat-gland-deficient animals; first',
        '   response is water, shade, and active skin cooling.',
        '7. Iron deficiency anaemia: confirm with blood smear (target cells, microcytic',
        '   hypochromic RBCs); treat with diet correction + iron + B12.',
    ], title='Chapter Summary — Non-Infectious Pathology in Asian Elephants'))

    return story


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=1.7 * cm, rightMargin=1.7 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title='Chapter 6: Non-Infectious Pathology in Asian Elephants',
        author='Prof. Dr. A. B. Shrivastava, NDVSU Jabalpur',
    )
    ST = make_styles()
    story = build_story(ST)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    main()

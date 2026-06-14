#!/usr/bin/env python3
"""
Generate Chapter 7: Postmortem Examination of the Asian Elephant
Based on notes from Prof. Dr. A. B. Shrivastav, NDVSU Jabalpur
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
C_NAVY   = HexColor('#1A2840')
C_BODY   = HexColor('#1A1A1A')
C_MUTED  = HexColor('#555555')
C_WHITE  = colors.white

PW, PH = A4
OUT = '/home/user/Workshop-on-Conference/Workshop_Chapter7_Postmortem_Examination_2026.pdf'


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
    def __init__(self, lines, title=None, width=None, warning=False, danger=False, dark=False):
        Flowable.__init__(self)
        self.lines = lines if isinstance(lines, list) else [lines]
        self.title = title
        self._width = width
        self.warning = warning
        self.danger = danger
        self.dark = dark

    def wrap(self, aw, ah):
        self.aw = self._width or aw
        self._h = (len(self.lines) * 13) + (18 if self.title else 0) + 18
        return self.aw, self._h

    def draw(self):
        c = self.canv
        if self.dark:
            bg, border, bar, tc = C_NAVY, C_MED, C_LIGHT, C_WHITE
        elif self.danger:
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
        c.setFillColor(C_WHITE if self.dark else C_BODY)
        for line in self.lines:
            c.drawString(12, y, line)
            y -= 13


class QuoteBox(Flowable):
    """Dark navy quote card for memorable citations."""
    def __init__(self, quote, attribution='', width=None):
        Flowable.__init__(self)
        self.quote = quote
        self.attribution = attribution
        self._width = width

    def wrap(self, aw, ah):
        self.aw = self._width or aw
        lines = max(1, len(self.quote) // 80 + 1)
        self._h = lines * 14 + (16 if self.attribution else 0) + 24
        return self.aw, self._h

    def draw(self):
        c = self.canv
        c.setFillColor(C_NAVY)
        c.roundRect(0, 0, self.aw, self._h, 5, fill=1, stroke=0)
        c.setFillColor(C_LIGHT)
        c.rect(0, 0, 5, self._h, fill=1, stroke=0)
        y = self._h - 14
        c.setFont('Helvetica-BoldOblique', 10)
        c.setFillColor(C_WHITE)
        # simple word wrap
        words = self.quote.split()
        line, lines_out = '', []
        for w in words:
            test = (line + ' ' + w).strip()
            if c.stringWidth(test, 'Helvetica-BoldOblique', 10) < self.aw - 28:
                line = test
            else:
                lines_out.append(line)
                line = w
        if line:
            lines_out.append(line)
        for ln in lines_out:
            c.drawString(14, y, '“' + ln if ln == lines_out[0] else ln)
            y -= 14
        if lines_out:
            # close quote on last line already drawn
            pass
        if self.attribution:
            c.setFont('Helvetica-Bold', 8.5)
            c.setFillColor(C_LIGHT)
            c.drawString(14, y - 2, f'— {self.attribution}')


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
    cell_ctr_bold = ParagraphStyle('CellCtrBold', fontName='Helvetica-Bold', fontSize=8.8,
        textColor=C_DARK, alignment=TA_CENTER, leading=12)
    return dict(body=body, bullet=bullet, note=note,
                cell_hdr=cell_hdr, cell_body=cell_body,
                cell_bold=cell_bold, cell_ctr=cell_ctr, cell_ctr_bold=cell_ctr_bold)


# ── Table helpers ─────────────────────────────────────────────────────────────

def make_table(headers, rows, ST, col_widths=None, first_bold=True, center_all=False):
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for row in rows:
        r = []
        for j, cell in enumerate(row):
            if center_all:
                sty = ST['cell_ctr_bold'] if (j == 0 and first_bold) else ST['cell_ctr']
            else:
                sty = ST['cell_bold'] if (j == 0 and first_bold) else ST['cell_body']
            r.append(Paragraph(str(cell), sty))
        data.append(r)
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


def two_col_table(h1, h2, rows, ST, col_widths):
    data = [[Paragraph(h1, ST['cell_hdr']), Paragraph(h2, ST['cell_hdr'])]]
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
def n(t, ST):  return Paragraph(t, ST['note'])
def b(t, ST):  return Paragraph(f'• {t}', ST['bullet'])
def num(i, t, ST): return Paragraph(f'<b>{i}.</b> {t}', ST['bullet'])


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
                      'Chapter 7: Postmortem Examination of the Asian Elephant')
    canvas.drawRightString(PW - doc.rightMargin, PH - doc.topMargin + 11,
                           'Prof. Dr. A. B. Shrivastav  ·  NDVSU, Jabalpur')
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
        '7',
        'Postmortem Examination of the Asian Elephant',
        'Protocol, Equipment, Systematic Examination & Differential Diagnosis',
        'Prof. Dr. A. B. Shrivastav, Founder Director  ·  School of Wildlife Forensic and Health  ·  '
        'Nanaji Deshmukh Veterinary Science University, Jabalpur (M.P.)'
    ))
    story.append(sp(14))

    # ── SECTION 1: WILDLIFE HEALTH MANAGEMENT ────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('1.  Wildlife Health Management — Context'),
        sp(6),
        p('Wildlife health is an important but still-developing discipline that is often '
          'overlooked, even though it is a key component of wildlife conservation.', ST),
        sp(6),
        KeyBox([
            'Definition (Shrivastav, 2010): Wildlife Health Management is a branch of',
            'veterinary science dealing with veterinary interventions in wild fauna —',
            'health monitoring, disease management, scientific immobilization, and habitat',
            'manipulation — to achieve conservation strategies that maintain a healthy',
            'population or conserve a particular species.',
        ], title='Definition'),
        sp(12),
    ]))

    # ── SECTION 2: INTRODUCTION ───────────────────────────────────────────────
    story.append(SectionHeading('2.  Introduction to Postmortem Examination'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Terminology', level=2),
        sp(6),
    ]))
    story.append(two_col_table('Term', 'Definition', [
        ['Necropsy', 'Postmortem examination of animals and birds.'],
        ['Autopsy', 'Postmortem examination of humans.'],
    ], ST, col_widths=[W * 0.22, W * 0.78]))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Key Principles', level=2),
        sp(6),
    ]))
    for line in [
        'PM examination must be conducted as per a <b>standard protocol</b> and with '
        '<b>adequate facilities</b>.',
        'The carcass of a wild animal is <b>seldom found in a condition suitable</b> for '
        'PM examination — early detection and prompt response are critical.',
        '<b>Who should perform it?</b> An experienced wildlife veterinarian, or a '
        'veterinary pathologist with exposure to wildlife.',
        'Postmortem examination is an <b>art of disease diagnosis</b> — a scientific, '
        'systematic requirement for recording gross pathological changes in the carcass.',
        '<b>Gross lesions alone are not sufficient</b> for a definitive diagnosis. '
        'Laboratory support is essential: correct samples in appropriate preservatives.',
        'A badly putrefied sample — or even a fresh sample in an unsuitable preservative '
        '— will not be useful.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(sp(4))
    story.append(QuoteBox(
        '"Doctors who perform necropsies, or who regularly witness postmortem examinations, '
        'learn to solve their doubts — unlike those not dealing with necropsy, whose answers '
        'are left floating in the air."',
        attribution='Dr. A. B. Shrivastav, 2014'
    ))
    story.append(sp(6))
    story.append(QuoteBox(
        '"Carcass never tells a lie."',
        attribution='Dr. Satpati'
    ))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Staff Required', level=2),
        sp(6),
    ]))
    story.append(two_col_table('Role', 'Number', [
        ['Wildlife veterinarians', '2–3'],
        ['Supporting staff', '4'],
        ['Photographer', '1'],
        ['Sample collection specialist', '1'],
    ], ST, col_widths=[W * 0.65, W * 0.35]))
    story.append(sp(12))

    # ── SECTION 3: OBJECTIVES ─────────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('3.  Necropsy Objectives'),
        sp(6),
    ]))
    for i, line in enumerate([
        'Identify all possible <b>lesions of disease or abnormality</b>.',
        'Correlate lesions with <b>clinical and laboratory findings</b>.',
        'Understand the <b>sequence of disease events</b> (pathogenesis).',
        'Provide information to <b>prevent or control the disease</b> in the healthy population.',
    ], 1):
        story.append(num(i, line, ST))
    story.append(sp(12))

    # ── SECTION 4: PRE-NECROPSY ───────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('4.  Pre-Necropsy Evaluation'),
        sp(6),
        p('Before beginning, examine the <b>necropsy request letter</b> for:', ST),
        sp(4),
    ]))
    for line in [
        'Specific lesions desired in particular organs or systems.',
        'Whether a <b>cosmetic</b> (for display) or <b>routine</b> necropsy is required.',
        'Special requests — sample collection for specific investigations, cultures, '
        'photographs, radiographs, etc.',
    ]:
        story.append(b(line, ST))
    story.append(sp(6))
    for line in [
        '<b>Identify the carcass</b> positively before beginning — confirm the correct '
        'individual is being necropsied.',
        'Review all available <b>clinical and circumstantial history</b>.',
    ]:
        story.append(b(line, ST))
    story.append(sp(6))
    story.append(KeyBox([
        'PM examinations of Schedule I animals must be performed systematically,',
        'sincerely, and seriously — never as a routine chore.',
    ], warning=True))
    story.append(sp(12))

    # ── SECTION 5: PROTOCOL ───────────────────────────────────────────────────
    story.append(SectionHeading('5.  Protocol for PM Examination — General Workflow'))
    story.append(sp(8))

    workflow_rows = [
        ['1', 'Letter from the competent authority',
         'Legal authorisation before any PM is commenced'],
        ['2', 'Facilities',
         'Appropriate site — good daylight, space for large carcass, drainage'],
        ['3', 'Measurements',
         'Body length, girth, tusk length; use calibrated instruments'],
        ['4', 'Observation — External then Internal',
         'Systematic external examination before any incision; then internal organ systems'],
        ['5', 'Gross interpretation',
         'Record and interpret all gross lesions before collecting samples'],
        ['6', 'Sample collection',
         'Collect biological samples in correct preservatives immediately after gross review'],
        ['7', 'Laboratory submission',
         'Suitable samples dispatched with completed history form and transport certificate'],
        ['8', 'Report writing',
         'Tentative cause of death → confirmatory lab results → final determination'],
    ]
    story.append(make_table(
        ['Step', 'Action', 'Notes'],
        workflow_rows, ST,
        col_widths=[W * 0.06, W * 0.34, W * 0.60],
    ))
    story.append(sp(8))

    story.append(KeyBox([
        'Always perform in good daylight.',
        'Use standard large-animal necropsy instruments (stainless steel, sharp).',
        'Protective clothing (PPE) mandatory for all veterinary and support staff.',
        'Maintain photographic and video documentation throughout.',
    ], title='General Logistics — Non-Negotiable Requirements', warning=True))
    story.append(sp(12))

    # ── SECTION 6: EQUIPMENT ──────────────────────────────────────────────────
    story.append(SectionHeading('6.  Equipment Required'))
    story.append(sp(8))

    story.append(SectionHeading('Documentation & Measurement Items', level=2))
    story.append(sp(6))
    doc_rows = [
        ['Copy of necropsy protocol', '1'],
        ['Hand-held GPS', '1'],
        ['Digital camera', '1'],
        ['Digital video camera', '1'],
        ['Clipboard', '2'],
        ['Measuring tape', '1'],
        ['Plastic ruler 15 cm (clear markings)', '2'],
        ['Vernier calipers', '1'],
        ['Portable weighing machine (250 kg)', '1'],
        ['Necropsy format (data sheets)', '5'],
        ['Ballpen', '2'],
        ['Pencil + rubber', '1 set'],
        ['Metal detector', '1'],
    ]
    story.append(make_table(
        ['Item', 'Min. Qty'],
        doc_rows, ST,
        col_widths=[W * 0.78, W * 0.22],
        center_all=False,
    ))
    story.append(sp(8))

    story.append(SectionHeading('Instruments (Stainless Steel — Best Quality)', level=2))
    story.append(sp(6))
    instr_rows = [
        ['Sharp high-quality necropsy knife (SS)', '4'],
        ['Skinning knife, curved (SS)', '2'],
        ['Autopsy knife, curved (SS)', '2'],
        ['Slicing knife, 22 mm blade (SS)', '1'],
        ['Knife sharpener stone or steel', '1'],
        ['Bard-Parker handle + blades (No. 20, 22, 26)', '5 each'],
        ['Small plain forceps', 'As needed'],
        ['Artery forceps, straight 203 mm (SS)', '2'],
        ['Dissecting forceps, 200 mm (SS)', '2'],
        ['Large Mayo dissecting scissors, fine point 215 mm', '2'],
        ['Bone cutter, compound action 266 mm', '1'],
        ['Hack saw / bone saw blade 254 mm', '1'],
        ['Chisel 22 cm × 3 cm blade', '1'],
        ['Hammer, wrench end 200 mm', '1'],
        ['Portable autopsy saw (electric/battery)', '1'],
        ['Axe (roofing axe, SS) 60 mm blade', '1'],
        ['Spirit lamp (SS) or gas burner', '1'],
    ]
    story.append(make_table(
        ['Instrument', 'Min. Qty'],
        instr_rows, ST,
        col_widths=[W * 0.78, W * 0.22],
    ))
    story.append(sp(12))

    # ── SECTION 7: EXTERNAL EXAMINATION ──────────────────────────────────────
    story.append(SectionHeading('7.  External Examination'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('General Assessment', level=2),
        sp(6),
    ]))
    for line in [
        '<b>Body condition score</b> — assess fat cover, muscle mass.',
        '<b>Rigor mortis</b> — presence, degree, and stage.',
        '<b>External injuries</b> — characterize location, type, age of injury.',
        '<b>Documentation</b> — photograph every finding before disturbing.',
        '<b>Any other observation</b> relevant to circumstances of death.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(SectionHeading('Detailed Checklist (11 Points)', level=2))
    story.append(sp(6))
    ext_rows = [
        ['1. Sex identification',
         'Examine male/female external organs; note pregnancy, lactation, or dry status.'],
        ['2. Nutritional status',
         'Prominent ribs, depression in lumbar and buccal regions, distinct temporal fossa, '
         'and loose skin all indicate poor nutritional status.'],
        ['3. Fractures & dislocations',
         'Search for fractures and dislocations systematically where possible.'],
        ['4. Postmortem changes',
         'Assess algor mortis (cooling), rigor mortis (stiffening), livor mortis '
         '(gravitational blood pooling), and autolytic changes.'],
        ['5. Mucous membranes',
         'Examine for pallor (anaemia), congestion (hyperaemia), cyanosis (hypoxia), '
         'and inflammatory conditions.'],
        ['6. Skin',
         'Check for external parasites, cutaneous filariasis, pox lesions, oedematous '
         'swellings, emphysematous crepitation, injuries, burns, and warts.'],
        ['7. Injuries',
         'Look for bullet wounds, intraspecies fight injuries, large-carnivore mauling '
         '(especially in calves), and ankush (hook) injuries in captive elephants.'],
        ['8. Dung bolus at rectum',
         'Indicates digestive function, dentition status, and hydration — dry, hard '
         'pellets vs. loose, watery faeces are both informative.'],
        ['9. Natural orifices',
         'Check all orifices for discharges. Examine oral cavity for FMD lesions, '
         'EEHV ulcers, anthrax signs, etc.'],
        ['10. Temporal glands',
         'Examine for musth secretions in adult males — relevant to circumstances '
         'of death (fighting, restraint-related stress).'],
        ['11. Foot pads and nails',
         'Check for injuries, cracks, foreign bodies, and overall condition.'],
    ]
    story.append(make_table(
        ['Check', 'What to Assess'],
        ext_rows, ST,
        col_widths=[W * 0.22, W * 0.78],
    ))
    story.append(sp(12))

    # ── SECTION 8: POSTMORTEM CHANGES ────────────────────────────────────────
    story.append(SectionHeading('8.  Postmortem Changes'))
    story.append(sp(8))

    pm_rows = [
        ['Cadaveric lividity\n(Hypostatic congestion)',
         'Irregular patches of dark discolouration in subcutaneous tissues on the '
         'dependent (lower) side — particularly prominent in large animals like elephants '
         'due to large blood volume. Must be distinguished from true haemorrhages.',
         'Begins within 1–2 hours; fixed by 6–8 hours (cannot be moved by repositioning).'],
        ['Rigor mortis',
         'Progressive stiffening of muscle due to ATP depletion and actin-myosin crosslinking. '
         'Less marked in weak, emaciated, diseased, or septicaemic animals.',
         'Appears 1–4 hours post-death; lasts 16–24 hours; may persist up to 48 hours '
         'depending on temperature and nutritional state.'],
        ['Autolytic changes',
         'Cellular self-digestion by endogenous enzymes released from disrupted lysosomes. '
         'Rate depends on atmospheric moisture, temperature, and postmortem interval.',
         'Begins immediately after death; visible as green discolouration, gas bloat, '
         'softening of tissues, and odour.'],
    ]
    story.append(make_table(
        ['Change', 'Description', 'Timeline / Notes'],
        pm_rows, ST,
        col_widths=[W * 0.22, W * 0.45, W * 0.33],
    ))
    story.append(sp(12))

    # ── SECTION 9: DENTITION & AGE ────────────────────────────────────────────
    story.append(SectionHeading('9.  Dentition & Age Determination'))
    story.append(sp(8))

    story.append(KeepTogether([
        p('Elephants develop <b>six successive sets of molars (M1–M6)</b> that erupt and '
          'wear sequentially throughout life. Each set replaces the previous as it wears '
          'down — unlike most mammals where molars erupt once. The number of <b>laminae</b> '
          '(enamel ridges) increases with each molar and can be used to estimate age.', ST),
        sp(6),
    ]))
    molar_rows = [
        ['M1', '~1 year', '5'],
        ['M2', '~2 years', '7'],
        ['M3', '~6 years', '10'],
        ['M4', '~15 years', '10'],
        ['M5', '~28 years', '12'],
        ['M6', '~47 years', '13'],
    ]
    story.append(make_table(
        ['Molar', 'Approx. Age at Eruption', 'Laminae (Enamel Ridges)'],
        molar_rows, ST,
        col_widths=[W * 0.18, W * 0.44, W * 0.38],
        center_all=True,
    ))
    story.append(sp(6))
    story.append(KeyBox([
        'Permanent tusks protrude beyond the lips at approximately 30 months and',
        'continue growing throughout life — tusk length can supplement age estimation.',
        'Once M6 wears out (typically 60+ years), the elephant can no longer chew',
        'and eventually dies of malnutrition.',
    ], title='Tusk & Final Molar Note'))
    story.append(sp(12))

    # ── SECTION 10: SKINNING ──────────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('10.  Skinning the Carcass'),
        sp(6),
        p('In a healthy animal the skin is thick but flexible and moves easily over '
          'the underlying tissues. Proper skinning is essential before internal '
          'examination.', ST),
        sp(6),
    ]))
    for line in [
        'Remove the skin of <b>one side</b> — from the entire lateral thoracic region '
        'down to the lower abdominal and other suspected regions.',
        '<b>Examine subcutaneous tissues and superficial muscles</b> for abscesses, '
        'wounds, haemorrhages, and other pathological conditions.',
        'Identify and examine all <b>superficial lymph nodes</b> before proceeding '
        'to the thoracic and abdominal cavities.',
    ]:
        story.append(b(line, ST))
    story.append(sp(12))

    # ── SECTION 11: INTERNAL EXAMINATION ─────────────────────────────────────
    story.append(SectionHeading('11.  Internal Examination — Systematic Approach'))
    story.append(sp(8))

    sys_rows = [
        ['Respiratory', 'Trachea — examine for mucus, haemorrhage, foreign body.\n'
         'Lungs — consistency, colour, pleural surface, cut surface (oedema, consolidation, '
         'haemorrhage).'],
        ['Digestive', 'Pharynx, oesophagus, stomach, small intestine, large intestine, '
         'caecum, rectum, anus.\nAlso: molar teeth and tongue, salivary glands, '
         'liver, pancreas.\nNote: the elephant is a <b>simple-stomached (monogastric)</b> '
         'animal. Stomach length ≈ 100–140 cm; diameter ≈ 40 cm.\nExamine stomach contents '
         '— food material, moisture, parasites, ulcers, gastritis.'],
        ['Urogenital', 'Kidneys — size, colour, capsule, cut surface (cortex-medulla ratio).\n'
         'Bladder — distension, mucosa, content.'],
        ['Reproductive', 'Uterus — size, content, endometrium.\n'
         'Ovaries / testes — as appropriate.'],
        ['Musculoskeletal', 'Muscles — pallor, haemorrhage, necrosis, parasites.\n'
         'Bones — fractures, metabolic changes.'],
        ['Nervous', 'Brain — meninges, congestion, herniation, grey/white matter changes.'],
        ['Cardiovascular', 'Heart — size, epicardium, myocardium (cut surface), valves, '
         'great vessels.'],
    ]
    story.append(make_table(
        ['System', 'Key Organs & Examination Points'],
        sys_rows, ST,
        col_widths=[W * 0.18, W * 0.82],
    ))
    story.append(sp(6))
    story.append(KeyBox([
        'Abdominal cavity approach: draw a vertical line from the last rib to the lower',
        'abdomen; make a vertical incision down to ground surface to open the cavity.',
        'The elephant has TWENTY PAIRS of ribs (vs. 13 in most large mammals).',
    ], title='Anatomical Note — Elephant Abdomen'))
    story.append(sp(12))

    # ── SECTION 12: LYMPH NODES ───────────────────────────────────────────────
    story.append(SectionHeading('12.  Lymph Node Examination'))
    story.append(sp(8))
    story.append(p('Superficial lymph nodes are particularly important for detecting '
                   'infectious diseases such as <b>tuberculosis</b> and <b>EEHV</b>. '
                   'Thick elephant skin makes external palpation difficult; systematic '
                   'incision is required.', ST))
    story.append(sp(8))

    story.append(SectionHeading('Superficial Lymph Nodes', level=2))
    story.append(sp(6))
    surf_rows = [
        ['Mandibular',
         'At the ventral border of the lower jaw, just under the skin.',
         'Incise between the mandibles and pull the tongue forward during '
         'oral cavity inspection.'],
        ['Parotid',
         'Just below the ear, near the parotid salivary gland.',
         'Enlarged in head and neck infections.'],
        ['Superficial cervical',
         'On the lateral side of the neck, slightly cranial to the shoulder.',
         'Drains superficial neck structures.'],
        ['Prescapular',
         'Just ahead of the shoulder joint.',
         'Drains the forelimb and cranial thorax.'],
        ['Femoral',
         'Close to the head of the femur.',
         'Drains the hindlimb.'],
    ]
    story.append(make_table(
        ['Node', 'Location', 'Notes'],
        surf_rows, ST,
        col_widths=[W * 0.20, W * 0.38, W * 0.42],
    ))
    story.append(sp(8))

    story.append(SectionHeading('Deep / Internal Lymph Nodes', level=2))
    story.append(sp(6))
    deep_rows = [
        ['Bronchial\n(Tracheobronchial)',
         'At the carina — where the bronchi bifurcate from the trachea.',
         'MUST be sampled for mycobacterial culture (TB). First site of lung '
         'lymph drainage; enlarged and caseous in TB.'],
        ['Hepatic & splenic',
         'Near the liver (hepatic hilus) and spleen respectively.',
         'Checked for systemic infection, haemorrhage, and reactive hyperplasia.'],
        ['Mesenteric',
         'Clusters distributed in the mesentery throughout the bowel.',
         'Filter lymph from the intestines; trap bacteria, viruses, and antigens '
         'before they enter the bloodstream. Key in enteric infections.'],
    ]
    story.append(make_table(
        ['Node', 'Location', 'Clinical Significance'],
        deep_rows, ST,
        col_widths=[W * 0.20, W * 0.32, W * 0.48],
    ))
    story.append(sp(12))

    # ── SECTION 13: EEHV HISTOPATHOLOGY ──────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('13.  Histopathology Highlight — EEHV'),
        sp(6),
        p('<b>Elephant Endotheliotropic Herpesvirus (EEHV)</b> is one of the most '
          'dangerous pathogens of young Asian elephants. Histopathological examination '
          'of affected endothelial tissues — particularly from the tongue, heart, and '
          'trunk tip — may reveal <b>intranuclear inclusion bodies</b>, the hallmark '
          'of herpesvirus infection.', ST),
        sp(6),
    ]))
    story.append(KeyBox([
        'Intranuclear inclusion bodies in vascular endothelium = EEHV until proven otherwise.',
        'Collect trunk wash, oral and rectal swabs, and fresh endothelial-rich tissue',
        '(tongue tip, trunk tip) for PCR confirmation.',
        'A T-cell-inducing heterologous vaccine against EEHV is currently under trial study.',
    ], title='EEHV — Histopathology & Diagnosis'))
    story.append(sp(12))

    # ── SECTION 14: DIFFERENTIAL DIAGNOSIS ───────────────────────────────────
    story.append(SectionHeading('14.  Differential Diagnosis — Sudden Onset, Rapid Death'))
    story.append(sp(8))
    diff_rows = [
        ['Haemorrhagic septicaemia\n(Pasteurellosis)',
         'Extensive haemorrhagic areas throughout the carcass; acute gelatinous oedema '
         'in subcutaneous tissues of the neck and brisket.',
         'Swabs, blood smear, culture from lymph node and lung.'],
        ['Salmonellosis',
         'Watery diarrhoea with or without blood; small intestinal mucosal haemorrhage '
         'and necrosis; mesenteric lymph node enlargement.',
         'Intestinal loop culture; fresh faeces; mesenteric LN.'],
        ['Enterotoxaemia\n(Clostridial)',
         'Profuse diarrhoea leading to rapid dehydration and death; bloat; '
         'haemorrhagic intestinal contents.',
         'Intestinal loop in formalin; fresh intestinal content for toxin assay.'],
        ['Encephalomyocarditis\n(EMCV)',
         'Cardiac muscle pallor and necrosis; respiratory signs may be observed; '
         'sudden death in young/stressed elephants.',
         'Heart tissue (fresh and fixed); serum for virus isolation/PCR.'],
    ]
    story.append(make_table(
        ['Disease', 'Characteristic Finding', 'Key Samples'],
        diff_rows, ST,
        col_widths=[W * 0.24, W * 0.44, W * 0.32],
    ))
    story.append(sp(12))

    # ── SECTION 15: RABIES CASE ───────────────────────────────────────────────
    story.append(SectionHeading('15.  Case Example — Rabies in Semi-Captive Elephant (Panna TR)'))
    story.append(sp(8))
    story.append(p('A semi-captive elephant at Panna Tiger Reserve presented with the '
                   'following sequence of clinical signs:', ST))
    story.append(sp(6))
    rabies_rows = [
        ['Initially', 'Off feed, restlessness, excessive drooling of saliva.'],
        ['Day 3', 'Restricted jaw movement, protrusion of tongue.'],
        ['Day 4', 'Hyperaemic conjunctiva (intense reddening of the eyes).'],
        ['Day 5', 'Hydrophobia; loud but markedly changed/abnormal trumpeting.'],
        ['Day 6', 'Lateral recumbency and death.'],
        ['Post-death', 'Proper carcass disposal under biosafety protocols.'],
    ]
    story.append(make_table(
        ['Time Point', 'Clinical Event'],
        rabies_rows, ST,
        col_widths=[W * 0.18, W * 0.82],
    ))
    story.append(sp(6))
    story.append(KeyBox([
        'Rabies in elephants is rare but documented. Submit fresh brain tissue in two portions:',
        '(1) half in 10% NBF for histopathology (Negri body detection), (2) half fresh/frozen',
        'for fluorescent antibody test (FAT) or RT-PCR. Handle with full Level-3 PPE.',
        'Carcass disposal must follow zoonotic disease biosafety protocols.',
    ], title='Rabies — Sample & Biosafety Notes', danger=True))
    story.append(sp(12))

    # ── SECTION 16: OTHER CONDITIONS ─────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('16.  Other Conditions of Note'),
        sp(6),
    ]))
    other_rows = [
        ['Tuberculosis (TB)',
         'Gross lesions — caseous nodules in lung and tracheobronchial lymph nodes — '
         'documented in free-ranging Asian elephants. Always sample bronchial lymph nodes '
         'for mycobacterial culture.'],
        ['HCN (hydrocyanic acid) poisoning',
         'Common in herbivores fed sorghum/jowar species; cyanogenic glycoside content '
         'highest in young, rapidly growing leaves and stalks (after autumn rains or '
         'crop regrowth). Managed with sodium thiosulphate + supportive therapy. '
         '(Ref: Shrivastav, Zoo Print, Vol. XXV, June 2010.)'],
        ['Decomposed / waterlogged carcass',
         'Severely autolysed or submerged carcasses may make assessment "difficult to '
         'advise" — tissue architecture is destroyed, cultures contaminated, and '
         'toxicological results unreliable. Emphasises the value of early detection.'],
    ]
    story.append(make_table(
        ['Condition', 'Notes for PM Examination'],
        other_rows, ST,
        col_widths=[W * 0.24, W * 0.76],
    ))
    story.append(sp(14))

    # ── KEY TAKEAWAYS ─────────────────────────────────────────────────────────
    story.append(SectionHeading('Key Takeaways'))
    story.append(sp(8))
    story.append(KeyBox([
        '1. A wildlife necropsy is only as good as its protocol, facilities, and operator',
        '   experience. Always work in good daylight with complete PPE.',
        '2. Gross findings alone rarely yield a definitive diagnosis — confirmatory',
        '   diagnosis depends on correctly collected and preserved laboratory samples.',
        '3. For elephants: use molars/tusks for age estimation; remember the monogastric',
        '   stomach (100–140 cm); and always note the 20 pairs of ribs.',
        '4. Prioritise tracheobronchial lymph node sampling for TB and trunk wash /',
        '   endothelial tissue for EEHV PCR confirmation.',
        '5. Cadaveric lividity must be distinguished from true haemorrhagic lesions.',
        '6. Rabies carries zoonotic risk — handle with Level-3 PPE; dispose of carcass',
        '   under biosafety protocols.',
        '7. "The carcass never tells a lie" — but only if the necropsy is performed',
        '   promptly, systematically, and with full documentation.',
    ], title='Chapter Summary — Postmortem Examination of the Asian Elephant'))

    return story


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=1.7 * cm, rightMargin=1.7 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title='Chapter 7: Postmortem Examination of the Asian Elephant',
        author='Prof. Dr. A. B. Shrivastav, NDVSU Jabalpur',
    )
    ST = make_styles()
    story = build_story(ST)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    main()

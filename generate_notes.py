#!/usr/bin/env python3
"""Generate detailed PDF notes for the Workshop on Elephant Mortality Investigation."""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Colours ────────────────────────────────────────────────────────────────
DARK_GREEN  = colors.HexColor('#1B4332')
MID_GREEN   = colors.HexColor('#2D6A4F')
LIGHT_GREEN = colors.HexColor('#52B788')
PALE_GREEN  = colors.HexColor('#D8F3DC')
AMBER       = colors.HexColor('#D4870A')
RED         = colors.HexColor('#C0392B')
BLUE        = colors.HexColor('#2980B9')
SLATE       = colors.HexColor('#2C3E50')
LIGHT_GREY  = colors.HexColor('#ECF0F1')
MID_GREY    = colors.HexColor('#BDC3C7')
WHITE       = colors.white
BLACK       = colors.black

W, H = A4   # 595.27 x 841.89 pt

# ── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def sty(name, parent='Normal', **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    return s

COVER_TITLE   = sty('CoverTitle',   fontSize=28, textColor=WHITE,
                     leading=34, alignment=TA_CENTER, spaceAfter=8)
COVER_SUB     = sty('CoverSub',     fontSize=14, textColor=PALE_GREEN,
                     leading=18, alignment=TA_CENTER, spaceAfter=4)
COVER_DATE    = sty('CoverDate',    fontSize=11, textColor=LIGHT_GREEN,
                     alignment=TA_CENTER)

CHAP_TITLE    = sty('ChapTitle',    fontSize=18, textColor=DARK_GREEN,
                     leading=22, spaceBefore=14, spaceAfter=6,
                     fontName='Helvetica-Bold')
SECT_TITLE    = sty('SectTitle',    fontSize=13, textColor=MID_GREEN,
                     leading=17, spaceBefore=10, spaceAfter=4,
                     fontName='Helvetica-Bold')
SUB_TITLE     = sty('SubTitle',     fontSize=11, textColor=SLATE,
                     leading=15, spaceBefore=6, spaceAfter=3,
                     fontName='Helvetica-Bold')
BODY          = sty('Body',         fontSize=10, textColor=SLATE,
                     leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
BULLET        = sty('Bullet',       fontSize=10, textColor=SLATE,
                     leading=13, leftIndent=16, spaceAfter=3,
                     bulletIndent=4, bulletFontSize=10)
SMALL         = sty('Small',        fontSize=8.5, textColor=colors.grey,
                     leading=12, spaceAfter=2)
HIGHLIGHT     = sty('Highlight',    fontSize=10, textColor=DARK_GREEN,
                     leading=14, spaceAfter=4, fontName='Helvetica-Bold',
                     backColor=PALE_GREEN, borderPadding=(4,6,4,6))
CAPTION       = sty('Caption',      fontSize=9, textColor=colors.grey,
                     alignment=TA_CENTER, spaceAfter=6)
LABEL_RED     = sty('LabelRed',     fontSize=10, textColor=RED,
                     fontName='Helvetica-Bold')
LABEL_BLUE    = sty('LabelBlue',    fontSize=10, textColor=BLUE,
                     fontName='Helvetica-Bold')

# ── Helper functions ─────────────────────────────────────────────────────────
def H1(text):
    return Paragraph(text, CHAP_TITLE)

def H2(text):
    return Paragraph(text, SECT_TITLE)

def H3(text):
    return Paragraph(text, SUB_TITLE)

def P(text):
    return Paragraph(text, BODY)

def B(text, indent=0):
    s = ParagraphStyle('BulletI', parent=BULLET, leftIndent=16+indent)
    return Paragraph(f'• {text}', s)

def hi(text):
    return Paragraph(text, HIGHLIGHT)

def HR(col=MID_GREEN, w=1):
    return HRFlowable(width='100%', thickness=w, color=col, spaceAfter=6, spaceBefore=4)

def SP(h=6):
    return Spacer(1, h)

def section_header(text, bg=DARK_GREEN, fg=WHITE):
    data = [[Paragraph(f'<b>{text}</b>',
             ParagraphStyle('SH', fontSize=14, textColor=fg, leading=18))]]
    t = Table(data, colWidths=[W - 72])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ]))
    return t

def kv_table(rows, col_w=(90, None)):
    cw = [col_w[0]*mm, None]
    data = [[Paragraph(f'<b>{k}</b>', sty('K', fontSize=9.5, textColor=DARK_GREEN,
                                          fontName='Helvetica-Bold')),
             Paragraph(v, sty('V', fontSize=9.5, textColor=SLATE))]
            for k, v in rows]
    t = Table(data, colWidths=[35*mm, W-72-35*mm])
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS',  (0,0), (-1,-1), [WHITE, LIGHT_GREY]),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('GRID',          (0,0), (-1,-1), 0.3, MID_GREY),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return t

def data_table(header, rows, col_widths=None):
    h_style = ParagraphStyle('TH', fontSize=9, textColor=WHITE,
                              fontName='Helvetica-Bold', leading=12)
    d_style = ParagraphStyle('TD', fontSize=9, textColor=SLATE, leading=12)
    hrow = [Paragraph(h, h_style) for h in header]
    drows = [[Paragraph(str(c), d_style) for c in r] for r in rows]
    all_rows = [hrow] + drows
    t = Table(all_rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), DARK_GREEN),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ('GRID',          (0,0), (-1,-1), 0.4, MID_GREY),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return t

# ── Cover page background ────────────────────────────────────────────────────
def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_GREEN)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Decorative stripe
    canvas.setFillColor(MID_GREEN)
    canvas.rect(0, H*0.62, W, 6, fill=1, stroke=0)
    canvas.setFillColor(LIGHT_GREEN)
    canvas.rect(0, H*0.62-3, W, 3, fill=1, stroke=0)
    # Bottom band
    canvas.setFillColor(MID_GREEN)
    canvas.rect(0, 0, W, 60, fill=1, stroke=0)
    canvas.restoreState()

def normal_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(DARK_GREEN)
    canvas.rect(0, H-28, W, 28, fill=1, stroke=0)
    canvas.setFillColor(LIGHT_GREEN)
    canvas.rect(0, H-31, W, 3, fill=1, stroke=0)
    # Header text
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(36, H-19,
        'Workshop on Essentials of Mortality Investigation of Asian Elephant')
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(W-36, H-19, 'Bilaspur 2026 · Detailed Notes')
    # Footer
    canvas.setFillColor(DARK_GREEN)
    canvas.rect(0, 0, W, 24, fill=1, stroke=0)
    canvas.setFillColor(PALE_GREEN)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(36, 8, 'Chhattisgarh Forest Department · Wildlife Institute of India, Dehradun')
    canvas.drawRightString(W-36, 8, f'Page {doc.page}')
    canvas.restoreState()

# ── Build story ──────────────────────────────────────────────────────────────
story = []
WC = W - 72   # usable content width

# ════════════════════════════════════════════════════════════════════
# COVER
# ════════════════════════════════════════════════════════════════════
story.append(Spacer(1, 120))
story.append(Paragraph(
    'Workshop on Essentials of Mortality<br/>Investigation of Asian Elephant',
    COVER_TITLE))
story.append(Spacer(1, 16))
story.append(Paragraph('Detailed Workshop Notes', COVER_SUB))
story.append(Spacer(1, 8))
story.append(Paragraph('5<sup>th</sup>–6<sup>th</sup> June 2026', COVER_DATE))
story.append(Spacer(1, 24))

cover_info = ParagraphStyle('CI', fontSize=11, textColor=PALE_GREEN,
                             leading=16, alignment=TA_CENTER)
story.append(Paragraph('Dharamjaigarh &amp; Raigarh Van Mandals', cover_info))
story.append(Paragraph('Bilaspur Forest Circle · Chhattisgarh', cover_info))
story.append(Spacer(1, 32))

orgs = ParagraphStyle('Orgs', fontSize=10, textColor=LIGHT_GREEN,
                       leading=16, alignment=TA_CENTER)
story.append(Paragraph(
    'Organised by: <b>Chhattisgarh Forest Department</b><br/>'
    'Technical Support: <b>Wildlife Institute of India, Dehradun</b><br/>'
    'Laboratory Partner: <b>ICAR-IVRI, Izatnagar · NDVSU, Jabalpur</b>',
    orgs))
story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 1 — WORKSHOP OVERVIEW
# ════════════════════════════════════════════════════════════════════
story.append(section_header('1. Workshop Overview & Objectives'))
story.append(SP(10))

story.append(H2('1.1 Context'))
story.append(P(
    'This two-day residential workshop was convened by the Chhattisgarh Forest Department '
    'in partnership with the Wildlife Institute of India, Dehradun, to build technical '
    'capacity in elephant mortality investigation across the Bilaspur Forest Circle. '
    'The workshop brought together <b>84 participants</b> from the Forest Department and '
    'Veterinary Service Department of Chhattisgarh State.'))
story.append(SP(4))

story.append(H2('1.2 Objectives'))
story.append(B('<b>Biology, Behaviour &amp; Disease:</b> Build a comprehensive understanding of '
               'Chhattisgarh elephant biology and behaviour, and the major infectious and '
               'non-infectious diseases causing mortality.'))
story.append(B('<b>Necropsy, Biosafety &amp; Sample Handling:</b> Develop hands-on competency in '
               'field necropsy under biosafety and biosecurity protocols.'))
story.append(B('<b>Surveillance, Disposal &amp; Remediation:</b> Establish operational frameworks '
               'for active and passive health surveillance, carcass disposal and site decontamination.'))
story.append(SP(4))

story.append(H2('1.3 Expected Outcomes'))
story.append(B('<b>Field Necropsy Skills:</b> Position and systematically eviscerate heavy elephant '
               'carcasses in remote field settings.'))
story.append(B('<b>Sample &amp; Lab Protocols:</b> Hands-on experience with tissue fixative '
               'formulation and secure packaging for histopathology, toxicology and microbiology.'))
story.append(B('<b>Surveillance &amp; Forensics:</b> Implementation of field-validated carcass '
               'disposal and site decontamination protocols, standardised forensic reporting, and '
               'proactive health monitoring frameworks.'))
story.append(SP(8))

# ════════════════════════════════════════════════════════════════════
# SECTION 2 — RESOURCE PERSONS
# ════════════════════════════════════════════════════════════════════
story.append(section_header('2. Resource Persons'))
story.append(SP(10))

rps = [
    {
        'name': 'Dr. A. B. Shrivastav',
        'title': 'Founder Director, School of Wildlife Forensic & Health; Professor & Veterinary Pathologist',
        'org': 'Nanaji Deshmukh Veterinary Science University (NDVSU), Jabalpur',
        'expertise': 'Wildlife Health Management · Wildlife Forensics · Veterinary Pathology',
        'profile': (
            'A renowned wildlife-health expert and founder Director of the School of Wildlife '
            'Forensic &amp; Health at NDVSU, Jabalpur (est. 2009). An architect of wildlife-health '
            'management in Central India since 1994, Prof. Shrivastav has advised national agencies '
            'including WII, NTCA, CZA, WWF and WTI, and supports forest departments across nine states. '
            'Trained at WII and the US National Wildlife Health Center, he has led 11 national projects — '
            'among them pioneering centres on wildlife forensics and the Indo-US Wildlife Health '
            'Co-operative Programme. Recipient of the Saheed Amrita Devi Vishnoi Award; '
            '200 research papers, 60 Master\'s &amp; PhD scholars.'
        ),
    },
    {
        'name': 'Dr. Parag Nigam',
        'title': 'Senior Scientist &amp; Head, Wildlife Health Management',
        'org': 'Wildlife Institute of India, Dehradun',
        'expertise': 'Wildlife Health · Chemical Capture · Conservation Medicine',
        'profile': (
            'Veterinarian with nearly three decades of experience and former officer of the '
            'Indian Army\'s Remount &amp; Veterinary Corps. Led India\'s first tiger reintroduction '
            'at Sariska and large-scale Indian Gaur reintroduction. Leading authority on chemical '
            'capture of wild animals; over 100 peer-reviewed publications spanning drug-protocol '
            'standardisation, disease ecology and One Health. Member, IUCN SSC Veterinary Specialist Group.'
        ),
    },
    {
        'name': 'Dr. Karikalan Mathesh',
        'title': 'Senior Scientist, Centre for Wildlife Conservation, Management &amp; Disease Surveillance',
        'org': 'ICAR–Indian Veterinary Research Institute (IVRI), Bareilly',
        'expertise': 'Wildlife Pathology · Histopathology · Molecular Disease Diagnosis',
        'profile': (
            'Veterinary pathologist specialising in necropsy, histopathology, clinical pathology '
            'and molecular disease diagnosis in wild animals — particularly Asian elephants, '
            'wild carnivores and vultures. Led national research projects (ICAR, ICMR, DST-SERB, CZA, MoEF&amp;CC). '
            'Over 150 peer-reviewed articles; Murray Fowler International Scholarship Award and '
            'Best Wildlife Pathologist Award (IAVP &amp; AIZWV).'
        ),
    },
    {
        'name': 'Dr. Tapendra Saini',
        'title': 'Scientist C',
        'org': 'Wildlife Institute of India, Dehradun',
        'expertise': 'Animal Genetics &amp; Breeding · Conservation Breeding · Wildlife Genetics',
        'profile': (
            'Veterinarian with BVSc &amp; AH from SDAU, Gujarat and PG specialisation in Animal Genetics '
            '&amp; Breeding from IVRI, Bareilly. Previously with Central Silk Board on tasar silkworm '
            'breeding in Saranda Forest, Jharkhand. Joined WII as Scientist C in April 2025, '
            'contributing to wildlife conservation-breeding programmes and disease-management initiatives.'
        ),
    },
    {
        'name': 'Dr. Chandra Prakash Sharma',
        'title': 'Principal Technical Officer &amp; In-charge, Morphology Unit, WFCGC',
        'org': 'Wildlife Institute of India, Dehradun',
        'expertise': 'Wildlife Forensics · Morphological Identification · Crime-Scene Management',
        'profile': (
            'With WII since 1994; helped build the country\'s premier wildlife forensic facility through '
            'the WII–US Fish &amp; Wildlife collaborative project (1995–2001). MSc Forensic Science '
            '(Punjabi University) and PhD Wildlife Science (Saurashtra University). Expert in '
            'morphological identification of illegal wildlife products, crime-scene management and '
            'evidence collection. Serves as expert scientific witness in courts nationwide; '
            'leads hands-on training and mock crime-scene exercises for law-enforcement officers across India.'
        ),
    },
]

for rp in rps:
    story.append(KeepTogether([
        H2(rp['name']),
        P(f'<i>{rp["title"]}</i>'),
        SP(3),
        kv_table([
            ('Organisation', rp['org']),
            ('Expertise',    rp['expertise']),
        ]),
        SP(4),
        P(rp['profile']),
        SP(8),
    ]))

# ════════════════════════════════════════════════════════════════════
# SECTION 3 — PROGRAMME SCHEDULE
# ════════════════════════════════════════════════════════════════════
story.append(section_header('3. Workshop Programme Schedule'))
story.append(SP(10))
story.append(P('The workshop spanned two days with 18 technical sessions covering anatomy, '
               'pathology, forensics, sampling and field practice.'))
story.append(SP(6))

# Day 1
story.append(H2('Day 1 — 30 May 2026  (10:00–20:00+)'))
story.append(SP(4))

day1 = [
    ['Time', 'Session', 'Faculty'],
    ['10:00–11:00', 'Inauguration\nOfficial opening, workshop objectives, and introduction of experts & participants.', '—'],
    ['11:00–11:30', 'Elephant Status & Human-Elephant Interface in Chhattisgarh\nPopulation dynamics, corridor use, conflict and mortality trends.', 'PP, AM'],
    ['11:30–12:15', 'Biological & Anatomical Aspects of Elephants\nKey anatomical peculiarities relevant to field investigation.', 'PN'],
    ['12:15–13:00', 'Understanding Wildlife Mortalities: The Veterinary Perspective\nCarcass condition, natural vs unnatural death; ante/post-mortem changes & time of death.', 'PN'],
    ['14:00–15:30', 'Infectious Causes of Mortality in Elephants\nFatal infectious diseases: EEHV, EMC, FMD, Rabies, TB, Anthrax, Haemorrhagic Septicaemia.', 'KM, ABS'],
    ['15:30–16:30', 'Non-Infectious & Disaster Mortalities in Elephants\nElectrocution, lightning, train hits, infighting, and other natural disaster deaths.', 'ABS, KM'],
    ['16:30–17:30', 'Non-Infectious Diseases in Elephants\nMycotoxicosis, kodo millet poisoning, and environmental bio-toxins.', 'KM, PN'],
]

cw = [32*mm, WC-32*mm-22*mm, 22*mm]
d1_fmtd = [[Paragraph(str(c),
                ParagraphStyle('SC', fontSize=8.5, textColor=(WHITE if i==0 else SLATE),
                               leading=12, fontName=('Helvetica-Bold' if i==0 else 'Helvetica')))
             for c in row] for i, row in enumerate(day1)]
t = Table(d1_fmtd, colWidths=cw)
t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), DARK_GREEN),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
    ('GRID',          (0,0), (-1,-1), 0.4, MID_GREY),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(t)
story.append(SP(10))

story.append(H2('Day 2 — 31 May 2026  (09:30–17:30)'))
story.append(SP(4))

day2 = [
    ['Time', 'Session', 'Faculty'],
    ['09:30–10:15', 'Biosafety & Biosecurity Measures in Elephant Mortality\nDisease threats from carcasses, essential PPE, safe disposal, site sanitation & disinfection.', 'KM, TS, PN'],
    ['10:15–11:00', 'Equipment Familiarization & Site Preparation\nHeavy-duty necropsy equipment (chain saws, axes, winches) and establishing a secure perimeter.', 'ABS, KM, TS'],
    ['11:30–12:30', 'Comprehensive Sampling Protocols\nCollection, packaging, cold chain, transport & documentation. Tissue selection for histopathology, toxicology & microbiology.', 'KM, ABS, PC, TS'],
    ['12:30–13:00', 'Recording Information During Necropsy\nReport writing and photographic documentation standards.', 'KM, ABS'],
    ['14:00–14:45', 'Vetro-Legal & Forensic Aspects of Mortality Investigation\nInvestigation essentials for legal and forensic frameworks.', 'CP'],
    ['14:45–16:00', 'Practical: Crime Scene Investigation\nChain of custody, evidence collection, and legal procedures for ivory/tusk extraction.', 'CP, PN, AM, TS'],
    ['16:15–16:45', 'Panel Discussion\nCritical aspects of managing mortalities in elephants.', 'All'],
    ['16:45–17:30', 'Valedictory\nWorkshop recap, feedback collection, and closing ceremony.', '—'],
]

d2_fmtd = [[Paragraph(str(c),
                ParagraphStyle('SC2', fontSize=8.5, textColor=(WHITE if i==0 else SLATE),
                               leading=12, fontName=('Helvetica-Bold' if i==0 else 'Helvetica')))
             for c in row] for i, row in enumerate(day2)]
t2 = Table(d2_fmtd, colWidths=cw)
t2.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), DARK_GREEN),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT_GREY]),
    ('GRID',          (0,0), (-1,-1), 0.4, MID_GREY),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(t2)
story.append(SP(6))
story.append(P('<i>Faculty codes: ABS = Dr. A.B. Shrivastav · PN = Dr. Parag Nigam · KM = Dr. Karikalan Mathesh · '
               'TS = Dr. Tapendra Saini · CP = Dr. C.P. Sharma · PP = Paras Patel · AM = Asst. Manager</i>'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 4 — ELEPHANT STATUS & POPULATION
# ════════════════════════════════════════════════════════════════════
story.append(section_header('4. Elephant Status & Population — Chhattisgarh'))
story.append(SP(10))

story.append(H2('4.1 Population Trend (2001–2026)'))
story.append(P('The elephant population in Chhattisgarh has grown dramatically over the past two '
               'decades, from a founding population of just 24 individuals in 2001 to an estimated '
               '<b>451 elephants</b> in 2026 — representing a compound annual growth rate (CAGR) '
               'of approximately 13%.'))
story.append(SP(4))

pop_data = [
    ['Year', 'Estimated Population', 'Notes'],
    ['2001',  '24',  'Founding dispersal from Odisha/Jharkhand'],
    ['2005',  '123', 'First major census count'],
    ['2007',  '122', 'Stable'],
    ['2015',  '247', 'Significant increase'],
    ['2017',  '247', 'Stable — confirmed census'],
    ['2021',  '279', 'Official Census'],
    ['2026',  '~451 (est.)', 'Estimated; net +172 over 5-year study period'],
]
cw_pop = [25*mm, 45*mm, WC-70*mm]
story.append(data_table(pop_data[0], pop_data[1:], cw_pop))
story.append(SP(6))

story.append(H2('4.2 Key Population Facts'))
story.append(B('<b>Bilaspur Circle</b> hosts the largest concentration of elephants in Chhattisgarh.'))
story.append(B('<b>~10% CAGR</b> observed over the 2021–2026 study period (279 → 451).'))
story.append(B('<b>2025-26</b> recorded the highest single-year human-elephant conflict events '
               'in the five-year study period.'))
story.append(B('Population range spans <b>Dharamjaigarh</b> and <b>Raigarh Van Mandals</b>, '
               'with documented GPS tracking of herds and individual tuskers.'))
story.append(SP(4))

story.append(H2('4.3 Live GPS Tracking'))
story.append(P('The presentation includes a live Leaflet.js-based map displaying real-time and '
               'recent GPS telemetry data:'))
story.append(B('<b>17 GPS points</b> from herd elephants (shown in green).'))
story.append(B('<b>29 GPS points</b> from individual tusker elephants (shown in amber).'))
story.append(P('The tracking system enables near-real-time monitoring of elephant movement '
               'corridors and early-warning alerts for human-elephant conflict zones.'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 5 — ELEPHANT CASUALTIES: DATA ANALYSIS
# ════════════════════════════════════════════════════════════════════
story.append(section_header('5. Elephant Casualties — Five-Year Analysis (2021–2026)'))
story.append(SP(10))

story.append(H2('5.1 Year-wise Deaths — Both Divisions'))
story.append(P(
    'The five-year study period (2021-22 to 2025-26) with ongoing 2026-27 data recorded '
    '<b>49 confirmed elephant deaths</b> across Dharamjaigarh (DH) and Raigarh (RG) divisions.'))
story.append(SP(4))

deaths_data = [
    ['Year',      'DH Division', 'RG Division', 'Total', 'Notes'],
    ['2021-22',   '4',           '0',           '4',     'All DH'],
    ['2022-23',   '6',           '6',           '12',    'RG emerges'],
    ['2023-24',   '6',           '0',           '6',     'DH dominant'],
    ['2024-25',   '6',           '4',           '10',    'Both divisions active'],
    ['2025-26',   '1',           '11',          '12',    'RECORD year — RG peak'],
    ['2026-27*',  '4',           '1',           '5',     'Ongoing — all calves, suspected drowning'],
    ['TOTAL',     '27',          '22',           '49',   '5+ year study'],
]
cw_d = [25*mm, 28*mm, 28*mm, 20*mm, WC-101*mm]
story.append(data_table(deaths_data[0], deaths_data[1:], cw_d))
story.append(SP(4))
story.append(hi('⚠  2025-26 is the record year with 12 deaths. The 2026-27 cohort (5 deaths in '
                'first 3 months — all calves, all suspected drowning) signals an acute emerging threat.'))
story.append(SP(8))

story.append(H2('5.2 Cause of Death Analysis'))
story.append(P('Analysis of all 49 confirmed deaths reveals electrocution as the dominant '
               'anthropogenic cause:'))
story.append(SP(4))

cause_data = [
    ['Cause of Death',          'Count', 'Percentage', 'Key Risk Factor'],
    ['Electrocution',           '23',    '47%',         'Illegal / low-hung power lines near crop fields'],
    ['Suspected Drowning',      '13',    '27%',         'Dams, ponds, seasonal nalas — primarily calves'],
    ['Natural / Old Age',       '4',     '8%',          'Natural senescence'],
    ['Fall / Trauma',           '4',     '8%',          'Hills, nalas, infighting'],
    ['Other (incl. heat/sun)',  '5',     '10%',         'Heatstroke, weakness, undetrmined'],
]
cw_c = [52*mm, 18*mm, 28*mm, WC-98*mm]
story.append(data_table(cause_data[0], cause_data[1:], cw_c))
story.append(SP(6))

story.append(H2('5.3 Age Group Analysis'))
story.append(P('Age profiling reveals a disproportionate burden on the youngest individuals:'))
story.append(SP(4))

age_data = [
    ['Age Class',            'Count', 'Percentage', 'Conservation Significance'],
    ['Calf (0–2 yr)',        '23',    '50%',        'Highest single class — critical concern'],
    ['Juvenile (2–15 yr)',   '5',     '11%',        '39% under 15 yr combined'],
    ['Sub-adult (15–30 yr)', '2',     '4%',         'Low'],
    ['Adult (30–55 yr)',     '11',    '24%',        'Electrocution primary cause'],
    ['Old (55+ yr)',         '5',     '11%',        'Female-skewed longevity'],
]
cw_a = [45*mm, 18*mm, 28*mm, WC-91*mm]
story.append(data_table(age_data[0], age_data[1:], cw_a))
story.append(SP(4))
story.append(hi('KEY CONCERN: 50% of all deaths are calves (0–2 yr). Combined with juveniles, '
                '61% of deaths occur in individuals under 15 years — posing a direct long-term '
                'threat to population viability.'))
story.append(SP(8))

story.append(H2('5.4 Sex Profiling (45 confirmed records)'))
story.append(SP(4))

sex_data = [
    ['Sex',    'Count', 'Distribution', 'Leading Causes'],
    ['Male',   '23',    '52%',          'Electrocution (11), Suspected Drowning (6), Falls (3)'],
    ['Female', '22',    '49%',          'Electrocution (7), Suspected Drowning (5), Natural/Old age (3)'],
]
story.append(data_table(sex_data[0], sex_data[1:], [18*mm, 18*mm, 28*mm, WC-64*mm]))
story.append(SP(6))

story.append(H3('Critical Sex-Specific Patterns:'))
story.append(B('<b>Calf Vulnerability (12F vs 10M):</b> 55% of calf deaths are female. Raigarh: '
               '8 of 11 drowning deaths are young females (6 months–2 years).'))
story.append(B('<b>Electrocution (11M, 7F):</b> Males at higher risk — 48% of male deaths from '
               'electrocution vs 33% of females.'))
story.append(B('<b>Suspected Drowning (6M, 5F):</b> Female-skewed among calves — 5 of 6 drowning '
               'females are calves.'))
story.append(B('<b>Old Age Deaths (1M, 4F):</b> Female longevity evident — more females survive to 55+ years.'))
story.append(SP(8))

story.append(H2('5.5 Seasonal Variation'))
story.append(P('Monthly analysis reveals two distinct mortality peaks:'))
story.append(SP(4))

seasonal_data = [
    ['Month', 'Total Deaths', 'Drowning', 'Electrocution'],
    ['January',   '6',  '3', '2'],
    ['February',  '4',  '0', '0'],
    ['March',     '3',  '1', '2'],
    ['April',     '2',  '0', '1'],
    ['May',       '5',  '4', '0'],
    ['June',      '5',  '1', '1'],
    ['July',      '1',  '0', '1'],
    ['August',    '1',  '0', '1'],
    ['September', '3',  '0', '2'],
    ['October',   '8',  '1', '7'],
    ['November',  '6',  '2', '1'],
    ['December',  '5',  '2', '2'],
]
cw_s = [32*mm, 30*mm, 28*mm, WC-90*mm]
story.append(data_table(seasonal_data[0], seasonal_data[1:], cw_s))
story.append(SP(6))

story.append(H3('Key Seasonal Patterns:'))
story.append(B('<b>October peak (8 deaths):</b> Post-monsoon movement &amp; harvest season overlap. '
               'Oct–Dec = 42% of annual deaths.'))
story.append(B('<b>Electrocution — Oct–Dec dominates (10 deaths, 50%):</b> Electric fencing around '
               'standing crops is most active during this post-monsoon harvest window.'))
story.append(B('<b>Drowning — Jan–May dominates (8 deaths, 62%):</b> Dry season — pond banks are steep '
               'and water levels low, trapping young calves that fall in while drinking.'))
story.append(SP(8))

story.append(H2('5.6 Range-wise Distribution'))
story.append(P('Casualty hotspots by forest range/beat:'))
story.append(SP(4))

range_data = [
    ['Range / Beat',        'Division', 'Deaths', 'Risk Level', 'Elec', 'Drown', 'Other'],
    ['Ghargoda',            'Raigarh',       '15', 'CRITICAL',   '7',   '5',    '3'],
    ['Chhal',               'Dharamjaigarh', '14', 'CRITICAL',   '5',   '6',    '3'],
    ['Dharamjaigarh HQ',    'Dharamjaigarh', '7',  'HIGH',       '5',   '0',    '2'],
    ['Tamanar',             'Raigarh',       '5',  'MODERATE',   '4',   '1',    '0'],
    ['Borojh',              'Dharamjaigarh', '4',  'HIGH',       '1',   '0',    '3'],
    ['Lailungaan',          'Dharamjaigarh', '2',  'HIGH',       '0',   '0',    '2'],
    ['Baakaaruma',          'Dharamjaigarh', '1',  'MODERATE',   '1',   '0',    '0'],
    ['Raigarh HQ',          'Raigarh',       '1',  'LOW',        '0',   '1',    '0'],
    ['Kharsiya',            'Raigarh',       '1',  'LOW',        '0',   '1',    '0'],
]
cw_r = [38*mm, 38*mm, 18*mm, 25*mm, 15*mm, 15*mm, WC-149*mm]
story.append(data_table(range_data[0], range_data[1:], cw_r))
story.append(SP(4))
story.append(hi('IMMEDIATE ACTION REQUIRED: Chhal (DH) &amp; Ghargoda (RG) together account for '
                '29 deaths — 59% of all casualties. These two ranges require priority electrocution '
                'and drowning mitigation interventions.'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 6 — DROWNING ANALYSIS
# ════════════════════════════════════════════════════════════════════
story.append(section_header('6. Suspected Drowning Cases — Detailed Analysis'))
story.append(SP(10))

story.append(H2('6.1 Overview'))
story.append(P(
    'Suspected drowning is the second-leading cause of elephant mortality in the study area, '
    'accounting for <b>13 deaths (27%)</b>. Notably, <b>92% of drowning victims are calves '
    'or young individuals</b>, making this pattern the most acute threat to population '
    'recruitment and long-term viability.'))
story.append(SP(6))

story.append(H2('6.2 Gross Post-mortem Findings — All 13 Cases'))
story.append(P('The following PM findings were consistent across all or most suspected drowning cases:'))
story.append(SP(4))

pm_data = [
    ['PM Finding',                                          'Frequency'],
    ['Frothy nasal/oral discharge — emphysema aquosum',     'ALL CASES'],
    ['Lungs — waterlogged, heavy, congested, oedematous',   'ALL CASES'],
    ['Water in trachea &amp; bronchi',                      'ALL CASES'],
    ['Gastric content — large volume of water &amp; plant debris', 'ALL CASES'],
    ['Skin maceration / hide wrinkling',                    'CONSISTENT'],
    ['Petechial haemorrhages — conjunctiva / sub-pleural',  'VARIABLE'],
]
cw_pm = [WC*0.7, WC*0.3]
story.append(data_table(pm_data[0], pm_data[1:], cw_pm))
story.append(SP(6))

story.append(H2('6.3 Histopathology — Microscopic Confirmation'))
story.append(B('Pulmonary oedema — alveolar flooding with eosinophilic fluid.'))
story.append(B('Pulmonary haemorrhage — interstitial and alveolar spaces.'))
story.append(B('Hepatocyte degeneration — confirmed in 3 cases (Tamnar range, December 2025).'))
story.append(B('<b>Diatom test positive</b> — confirmatory for ante-mortem drowning in all tested cases.'))
story.append(B('Renal congestion — passive vascular engorgement.'))
story.append(SP(6))

story.append(H2('6.4 ARSENIC DETECTION — Critical Finding'))
story.append(SP(4))
arsenic_box = Table([[Paragraph(
    '<b>ARSENIC DETECTED</b><br/>ICAR-IVRI Lab Report · Tamnar Range, December 2025<br/><br/>'
    'Arsenic detected at elevated levels in visceral samples from <b>2 specimens in Raigarh Division</b> '
    '(Tamnar Range, December 2025). Histopathology confirmed hepatocyte degeneration. Both cases '
    'classified as suspected drowning — arsenic likely a contributing metabolic stress factor from '
    'contaminated dam water near industrial corridor. <b>Environmental sampling of Rabo / Panikshet '
    'dam catchments recommended immediately.</b>',
    ParagraphStyle('A', fontSize=10, textColor=colors.HexColor('#7B0000'), leading=15)
)]],
colWidths=[WC])
arsenic_box.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#FDECEA')),
    ('TOPPADDING',    (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING',   (0,0), (-1,-1), 12),
    ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ('BOX',           (0,0), (-1,-1), 1.5, RED),
]))
story.append(arsenic_box)
story.append(SP(6))

story.append(H2('6.5 Toxicology — Negative Findings'))
story.append(P('All tested samples (5 batches) returned <b>NEGATIVE</b> for the following:'))
story.append(B('EEHV (Elephant Endotheliotropic Herpesvirus) — Negative'))
story.append(B('Nitrate-Nitrite compounds — Negative'))
story.append(B('Organophosphate insecticides — Negative'))
story.append(B('Heavy metals (Pb, Hg, Cd) — Negative'))
story.append(B('Hydrogen Cyanide (HCN) — Negative'))
story.append(SP(4))
story.append(P('This clears the most common pesticide and industrial toxin hypotheses, '
               'narrowing the causal mechanism to drowning with possible arsenic co-exposure.'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 7 — PM REPORT SUMMARY
# ════════════════════════════════════════════════════════════════════
story.append(section_header('7. Post-mortem Report — Summary Analysis'))
story.append(SP(10))

story.append(H2('7.1 Lead Cause — PM Confirmed'))
story.append(P(
    '<b>Electrocution leading to Cardio-Respiratory Failure</b> is confirmed as the cause of '
    'death in <b>20 records (49%)</b> of PM-confirmed cases. Multiple simultaneous electrocution '
    'events were noted in 3 cases. Suspected Drowning is the second-leading confirmed cause '
    '(9 records, 22%).'))
story.append(SP(6))

story.append(H2('7.2 PM Cause Distribution'))
story.append(SP(4))

pm_cause = [
    ['Cause',              'PM-Confirmed Count', 'Percentage'],
    ['Electrocution',      '~20',                '49%'],
    ['Suspected Drowning', '~9',                 '22%'],
    ['Natural / Old Age',  '~5',                 '12%'],
    ['Trauma / Fall',      '~5',                 '12%'],
    ['Other',              '~2',                 '5%'],
]
story.append(data_table(pm_cause[0], pm_cause[1:], [WC*0.5, WC*0.27, WC*0.23]))
story.append(SP(6))

story.append(H2('7.3 Age Concern — Neonates &amp; Calves'))
story.append(P(
    'Calves (0–2 yr) account for <b>49% of all age-confirmed records</b> (22 of 45). '
    'This level of early juvenile mortality poses a <b>direct threat to long-term population '
    'viability</b>. The combination of drowning risk in young calves during the dry season '
    'and arsenic contamination in water bodies near industrial corridors requires immediate '
    'field intervention.'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 8 — LABORATORY REPORTS
# ════════════════════════════════════════════════════════════════════
story.append(section_header('8. Laboratory Report Analysis'))
story.append(SP(10))

story.append(H2('8.1 ICAR-IVRI &amp; NDVSU Reports'))
story.append(P(
    'Laboratory analyses were conducted by <b>ICAR-IVRI, Izatnagar</b> '
    '(File F.2-19/DI/NRC/2025-26/CWL) and the <b>School of Wildlife Forensic &amp; Health, '
    'NDVSU, Jabalpur</b> across five tested batches.'))
story.append(SP(6))

story.append(H2('8.2 Arsenic Detection'))
story.append(P(
    'Two specimens from Tamnar Range, Raigarh Division (December 2025) tested positive for '
    '<b>arsenic at elevated levels</b> in visceral samples. Histopathology confirmed hepatocyte '
    'degeneration — suggesting chronic or sub-acute arsenic poisoning likely from contaminated '
    'dam water near the industrial corridor. Environmental sampling of the Rabo and Panikshet '
    'dam catchments is recommended immediately.'))
story.append(SP(6))

story.append(H2('8.3 EEHV — Negative'))
story.append(P(
    'EEHV-I (Elephant Endotheliotropic Herpesvirus) PCR testing returned <b>NEGATIVE</b> in '
    'all tested samples, confirmed independently by NDVSU Jabalpur for Dharamjaigarh Division '
    'specimens. No viral haemorrhagic disease involvement — viral aetiology is ruled out. '
    'This is particularly significant given the high neonate mortality observed.'))
story.append(SP(6))

story.append(H2('8.4 Broad Toxicological Screen — Negative'))
story.append(P(
    'Five tested batches returned NEGATIVE results for: Nitrate-Nitrite compounds, '
    'Heavy metals (Pb, Hg, Cd), Organochlorine &amp; organophosphate insecticides, '
    'Hydrogen Cyanide (HCN). The most common pesticide and industrial toxin hypotheses '
    'are cleared.'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 9 — CASE STUDY: GURDA DROWNING
# ════════════════════════════════════════════════════════════════════
story.append(section_header('9. Case Study — Gurda Elephant Casualty (01 June 2026)'))
story.append(SP(10))

story.append(H2('9.1 Incident Details'))
story.append(SP(4))
story.append(kv_table([
    ('Date',            '01 June 2026'),
    ('Location',        'Gurda, Kharsia Range'),
    ('Division',        'Raigarh Van Mandal'),
    ('GPS Coordinates', '22.0439°N, 83.1313°E  (22°3′16″N 83°8′11″E)'),
    ('Elevation',       '256.04 ± 9.59 m'),
    ('Water Body',      'Gurda River / Sandbank'),
]))
story.append(SP(6))

story.append(H2('9.2 PM Report Summary'))
story.append(SP(4))
story.append(kv_table([
    ('Species',         'Asian Elephant (Elephas maximus)'),
    ('Age Class',       'Calf (0–2 yr)'),
    ('Cause of Death',  'Suspected Drowning'),
    ('Body Condition',  'Found on exposed riverbank sandbank'),
    ('Pattern',         'Consistent with dry-season drowning — steep bank, low water, young calf'),
]))
story.append(SP(6))

story.append(H2('9.3 Field Notes'))
story.append(P(
    'The calf was found on an exposed sandbank adjacent to the Gurda River water body in Kharsia '
    'Range, Raigarh Van Mandal. The incident is consistent with the established dry-season drowning '
    'pattern — when water levels are low and pond/river banks are steep, young calves that approach '
    'the water edge to drink can fall in and are unable to climb out. '
    'Field photographic documentation was secured at 10:56 and 11:03 hrs on 06-01-2026 '
    'from aerial and ground perspectives respectively.'))
story.append(SP(4))
story.append(P('<i>Field note (original): हाथी निगरानी परिसर गुर्दा — Gurda परिक्षेत्र, खरसिया वनमण्डल रायगढ़।</i>'))
story.append(SP(4))
story.append(hi('This case represents the 2026-27 cohort pattern — all 5 deaths in the current '
                'year are calves, all suspected drowning, all in the first 3 months of the year.'))

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════
# SECTION 10 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════
story.append(section_header('10. Key Findings, Recommendations & Action Points'))
story.append(SP(10))

story.append(H2('10.1 Priority Intervention Zones'))
story.append(SP(4))
story.append(B('<b>CRITICAL:</b> Chhal range (DH) and Ghargoda range (RG) — combined 29 deaths '
               '(59%). Immediate multi-agency intervention required.'))
story.append(B('<b>HIGH:</b> Dharamjaigarh HQ and Borojh (DH) — electrocution dominant. '
               'Line patrolling and insulator replacement urgently needed.'))
story.append(B('<b>MODERATE:</b> Tamanar (RG) — mixed electrocution and drowning; seasonal '
               'watch required Oct–Dec.'))
story.append(SP(6))

story.append(H2('10.2 Electrocution Mitigation'))
story.append(B('Survey and replacement of <b>low-hung power lines</b> in all elephant corridors, '
               'particularly within 1 km of identified hotspot ranges.'))
story.append(B('Seasonal enforcement campaign targeting <b>Oct–Dec</b> (crop harvest period) '
               'when illegal electric fencing is most active.'))
story.append(B('<b>Multi-simultaneous electrocution</b> events noted in 3 cases — indicates '
               'persistent illegal installations; criminal liability must be enforced.'))
story.append(SP(6))

story.append(H2('10.3 Drowning Prevention'))
story.append(B('Installation of <b>earthen ramps / exit points</b> at high-risk dam edges and '
               'ponds within confirmed elephant drinking zones.'))
story.append(B('<b>Fencing or barriers</b> at steep-banked water bodies identified as '
               'drowning sites (particularly Panikshet and Rabo dams, Raigarh).'))
story.append(B('Priority focus on Jan–May period — 62% of drownings occur in this window.'))
story.append(B('Real-time calf monitoring in herds using GPS data during dry season.'))
story.append(SP(6))

story.append(H2('10.4 Environmental Sampling'))
story.append(SP(4))
arsenic2 = Table([[Paragraph(
    '<b>IMMEDIATE: Environmental sampling of Rabo &amp; Panikshet dam catchments, Raigarh Division.</b><br/>'
    'Arsenic detected in 2 December 2025 specimens near industrial corridor. Water and sediment '
    'sampling required; results to be shared with Chhattisgarh Pollution Control Board for '
    'enforcement action.',
    ParagraphStyle('A2', fontSize=10, textColor=colors.HexColor('#7B0000'), leading=15)
)]],
colWidths=[WC])
arsenic2.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), colors.HexColor('#FDECEA')),
    ('TOPPADDING',    (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING',   (0,0), (-1,-1), 12),
    ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ('BOX',           (0,0), (-1,-1), 1.5, RED),
]))
story.append(arsenic2)
story.append(SP(6))

story.append(H2('10.5 Surveillance &amp; Reporting Enhancements'))
story.append(B('Standardised <b>Proforma-1 documentation</b> to be used consistently across '
               'all ranges — including GPS coordinates, age estimate, cause, and photo log.'))
story.append(B('All mortality events to trigger <b>mandatory PM within 24 hours</b> and '
               'sample dispatch to ICAR-IVRI within 48 hours with cold chain documentation.'))
story.append(B('Quarterly mortality review meetings at division level with range officers.'))
story.append(B('EEHV surveillance to continue annually given high neonate mortality — '
               'negative results must be systematically documented.'))
story.append(SP(8))

story.append(H2('10.6 Summary Statistics'))
story.append(SP(4))

summary_data = [
    ['Metric',                          'Value'],
    ['Study Period',                     '2021-22 to 2026-27 (ongoing)'],
    ['Total Elephant Deaths',            '49 confirmed'],
    ['Divisions Covered',                'Dharamjaigarh (27) + Raigarh (22)'],
    ['Leading Cause',                    'Electrocution — 23 deaths (47%)'],
    ['Second Cause',                     'Suspected Drowning — 13 deaths (27%)'],
    ['Most Vulnerable Age',              'Calves 0–2 yr — 23 deaths (50%)'],
    ['Deadliest Year',                   '2025-26 — 12 deaths (record)'],
    ['2026-27 Trend',                    '5 deaths in first 3 months — all calves'],
    ['Critical Hotspot Ranges',          'Chhal (14) + Ghargoda (15) = 59% of all deaths'],
    ['Drowning Seasonality',             'Jan–May = 62% of drowning deaths'],
    ['Electrocution Seasonality',        'Oct–Dec = 50% of electrocution deaths'],
    ['Arsenic Detected',                 '2 specimens — Tamnar Range, Dec 2025'],
    ['EEHV Status',                      'Negative (all batches)'],
    ['Toxicology',                       'Negative for all major toxins screened'],
    ['Workshop Participants',            '84 (Forest Dept + Veterinary Service Dept, CG)'],
]
story.append(data_table(summary_data[0], summary_data[1:],
                         [WC*0.45, WC*0.55]))

story.append(SP(14))
HR(DARK_GREEN, 1.5)
story.append(SP(6))
story.append(Paragraph(
    '<i>Data Sources: Official Proforma-1 Records, Dharamjaigarh &amp; Raigarh Divisions · '
    'PM Reports: ICAR-IVRI Izatnagar (File F.2-19/DI/NRC/2025-26/CWL) · '
    'GIS Data: Bilaspur Forest Division GIS Cell · Generated: 30 May 2026</i>',
    SMALL))
story.append(SP(4))
story.append(Paragraph(
    '<i>Organised by: Chhattisgarh Forest Department · '
    'Technical Support: Wildlife Institute of India, Dehradun · '
    'Laboratory: ICAR-IVRI, Izatnagar &amp; NDVSU, Jabalpur</i>',
    SMALL))

# ── Build PDF ────────────────────────────────────────────────────────────────
out = '/home/user/Workshop-on-Conference/Workshop_Notes_Elephant_Mortality_2026.pdf'

def on_page(canvas, doc):
    if doc.page == 1:
        cover_page(canvas, doc)
    else:
        normal_page(canvas, doc)

doc = SimpleDocTemplate(
    out,
    pagesize=A4,
    leftMargin=36, rightMargin=36,
    topMargin=48, bottomMargin=36,
    title='Workshop Notes — Mortality Investigation of Asian Elephant',
    author='Chhattisgarh Forest Department / WII',
    subject='Elephant Mortality Analysis 2021-2026',
)

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'PDF saved: {out}')
print(f'Size: {os.path.getsize(out)/1024:.1f} KB')

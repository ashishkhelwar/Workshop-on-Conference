#!/usr/bin/env python3
"""
Generate Chapter 3 Word file purely from the DOCX lecture notes
(Dr. M. Karikalan, VBSC SH_1_3). No images from the PDF presentation.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page setup: A4 ────────────────────────────────────────────────────────────
sec = doc.sections[0]
sec.page_width  = Cm(21)
sec.page_height = Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.5)
sec.top_margin  = sec.bottom_margin = Cm(2)

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN_DARK   = RGBColor(0x1B, 0x43, 0x32)
GREEN_MED    = RGBColor(0x2D, 0x6A, 0x4F)
GREEN_LIGHT  = RGBColor(0x52, 0xB7, 0x88)
RED_WARN     = RGBColor(0xD6, 0x28, 0x28)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK    = RGBColor(0x1A, 0x1A, 0x2E)

# ── Style helper ──────────────────────────────────────────────────────────────
def add_style(name, base_name='Normal', font='Calibri', size=11,
              bold=False, italic=False, color=None,
              before=0, after=6, align=None, line_spacing=None):
    st_names = [s.name for s in doc.styles]
    if name in st_names:
        st = doc.styles[name]
    else:
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    try:
        st.base_style = doc.styles[base_name]
    except Exception:
        pass
    st.font.name = font
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.italic = italic
    if color:
        st.font.color.rgb = color
    st.paragraph_format.space_before = Pt(before)
    st.paragraph_format.space_after  = Pt(after)
    if align is not None:
        st.paragraph_format.alignment = align
    return st

add_style('C3ChLabel',  size=13, bold=True,  color=GREEN_MED,   before=6,  after=4,  align=WD_ALIGN_PARAGRAPH.CENTER)
add_style('C3Title',    size=24, bold=True,  color=GREEN_DARK,  before=4,  after=8,  align=WD_ALIGN_PARAGRAPH.CENTER)
add_style('C3Author',   size=11,             color=GREEN_MED,   before=2,  after=3,  align=WD_ALIGN_PARAGRAPH.CENTER)
add_style('C3Abstract', size=10, italic=True,color=TEXT_DARK,   before=6,  after=4,  align=WD_ALIGN_PARAGRAPH.JUSTIFY)
add_style('C3KW',       size=9,              color=GREEN_MED,   before=2,  after=12, align=WD_ALIGN_PARAGRAPH.LEFT)
add_style('C3H1',       size=15, bold=True,  color=GREEN_DARK,  before=18, after=6)
add_style('C3H2',       size=12, bold=True,  color=GREEN_MED,   before=10, after=4)
add_style('C3Body',     size=10.5,           color=TEXT_DARK,   before=3,  after=5,  align=WD_ALIGN_PARAGRAPH.JUSTIFY)
add_style('C3Bullet',   size=10.5,           color=TEXT_DARK,   before=2,  after=2)
add_style('C3KeyBox',   size=10.5, bold=True,color=GREEN_DARK,  before=3,  after=3)
add_style('C3Warn',     size=10.5, bold=True,color=RED_WARN,    before=4,  after=4)
add_style('C3Note',     size=9,  italic=True,color=GREEN_MED,   before=4,  after=8)


# ── Helpers ───────────────────────────────────────────────────────────────────
def h1(text):
    p = doc.add_paragraph(style='C3H1')
    run = p.add_run(text)
    # Add bottom border via XML
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), '2D6A4F')
    pBdr.append(bottom)
    pPr.append(pBdr)

def h2(text):
    doc.add_paragraph(text, style='C3H2')

def body(text):
    doc.add_paragraph(text, style='C3Body')

def bullet(text, level=1):
    p = doc.add_paragraph(style='C3Bullet')
    p.paragraph_format.left_indent = Cm(level * 0.7)
    p.paragraph_format.first_line_indent = Cm(-0.4)
    p.add_run('• ' + text)

def key_box(lines, title=None):
    """Shaded key-points box as a 1-col table."""
    rows = (1 if title else 0) + len(lines)
    t = doc.add_table(rows=rows, cols=1)
    t.style = 'Table Grid'
    idx = 0
    if title:
        cell = t.rows[idx].cells[0]
        cell.text = title
        run = cell.paragraphs[0].runs[0]
        run.bold = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = GREEN_DARK
        _shade_cell(cell, 'B7E4C7')
        idx += 1
    for i, line in enumerate(lines):
        cell = t.rows[idx].cells[0]
        cell.text = line
        run = cell.paragraphs[0].runs[0]
        run.font.size = Pt(10)
        run.font.color.rgb = TEXT_DARK
        _shade_cell(cell, 'D8F3DC' if i % 2 == 0 else 'E8F8F0')
        idx += 1
    doc.add_paragraph('')

def warn_box(lines, title='⚠ Important'):
    rows = 1 + len(lines)
    t = doc.add_table(rows=rows, cols=1)
    t.style = 'Table Grid'
    cell = t.rows[0].cells[0]
    cell.text = title
    run = cell.paragraphs[0].runs[0]
    run.bold = True
    run.font.size = Pt(10.5)
    run.font.color.rgb = RED_WARN
    _shade_cell(cell, 'FFF5F5')
    for i, line in enumerate(lines):
        cell = t.rows[i + 1].cells[0]
        cell.text = line
        run = cell.paragraphs[0].runs[0]
        run.font.size = Pt(10)
        _shade_cell(cell, 'FFF5F5')
    doc.add_paragraph('')

def _shade_cell(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def add_table(headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    for i, hdr in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = hdr
        run = cell.paragraphs[0].runs[0]
        run.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = WHITE
        _shade_cell(cell, '1B4332')
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            cell = t.rows[r_i + 1].cells[c_i]
            cell.text = val
            run = cell.paragraphs[0].runs[0]
            run.font.size = Pt(9)
            _shade_cell(cell, 'D8F3DC' if r_i % 2 == 0 else 'E8F8F0')
    doc.add_paragraph('')

def spacer():
    doc.add_paragraph('')


# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_paragraph('CHAPTER 3', style='C3ChLabel')
doc.add_paragraph('Wildlife Disease Management\nand Elephant Health', style='C3Title')
spacer()
doc.add_paragraph('Dr. M. Karikalan', style='C3Author')
doc.add_paragraph('Senior Scientist, Centre for Wildlife', style='C3Author')
doc.add_paragraph('Compiled from VBSC Lecture Series, Sessions SH_1_3, Parts 1 & 2', style='C3Author')
spacer()
doc.add_paragraph('Workshop on Elephant Mortality Investigation and Management', style='C3Author')
doc.add_paragraph('Chhattisgarh Forest Department · Bilaspur · June 2026', style='C3Author')
spacer()
spacer()

# Abstract
h1('Abstract')
body(
    'This chapter compiles two lecture sessions on the investigation and management of disease in elephants, '
    'situated within the discipline of wildlife conservation medicine. It advances the thesis that mortality '
    'investigation is fundamentally a conservation tool, justifying thorough examination of even single deaths '
    'in endangered populations. The dominant infectious threat, elephant endotheliotropic herpesvirus (EEHV), '
    'is treated in detail: its endotheliotropic, haemorrhagic pathogenesis, its concentration in calves and '
    'juveniles, its asymptomatic adult carriers, and the diagnostic primacy of quantitative PCR with '
    'cycle-threshold (CT) values and bone-marrow sampling. Other significant agents are surveyed — rabies, '
    'anthrax, tuberculosis, haemorrhagic septicaemia, clostridial disease and parasitic burdens — together '
    'with the field cases that illustrate their diagnosis. Throughout, a single professional discipline is '
    'emphasised: systematic necropsy, correct sampling, biosecurity, documentation, laboratory collaboration, '
    'and the investigation of every death as preparedness against future outbreaks.'
)
doc.add_paragraph(
    'Keywords: Asian elephant · EEHV · conservation medicine · wildlife pathology · '
    'biosecurity · zoonosis · necropsy · bone marrow',
    style='C3KW'
)
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════════
h1('1  Introduction')

h2('1.1  The Conservation Rationale for Mortality Investigation')
body(
    'The material presented here is grounded in field and laboratory practice rather than textbook theory, '
    'on the principle that in wildlife work formal study takes one only so far and that most genuine understanding '
    'is acquired by handling cases as they arrive. Dr Karikalan\'s training touched on infectious disease — the '
    'doctoral work concerned infectious bovine rhinotracheitis (IBR) — but the career has been spent almost '
    'entirely on wildlife pathology, and that practical grounding informs the account throughout.'
)
body(
    'The governing question is why mortality should be investigated at all, and the answer is conservation. '
    'Successive Asian elephant census figures (across the 2012, 2017, 2022 and 2025 surveys) indicate a downward '
    'population trend. The precise numbers matter less than the principle they illustrate: a population under '
    'pressure means that every death carries weight, and the factors driving decline — whether infectious or '
    'non-infectious — must all be identified and addressed. This establishes the recurring thesis: in wildlife '
    'a single case matters. Whereas in livestock or human medicine an individual death may be statistically '
    'negligible, the loss of even one animal of an endangered species warrants full investigation. Conservation, '
    'in effect, lowers the threshold at which a death is taken seriously.'
)

h2('1.2  Epidemiological Terminology')
body(
    'Before any specific disease is discussed, the basic epidemiological vocabulary must be understood. '
    'An emerging disease is one appearing in a population for the first time, exemplified by Ebola, Nipah '
    'and lumpy skin disease (LSD). A re-emerging disease returns after a quiet interval, frequently with an '
    'altered clinical picture on each reappearance. A transboundary disease crosses geographical and species '
    'borders as animals and pathogens move, while a zoonotic disease passes between animals and humans — '
    'a two-way crossing that is a constant concern in shared environments.'
)
add_table(
    ['Term', 'Definition', 'Example'],
    [
        ['Emerging disease', 'Appears in a population for the first time or rises sharply in incidence/range', 'Ebola, Nipah, LSD, EEHV'],
        ['Re-emerging disease', 'Returns after a period of decline; presentation may shift on each occurrence', 'Lumpy skin disease, Anthrax'],
        ['Transboundary disease', 'Crosses national or ecosystem borders; requires multi-jurisdictional response', 'FMD, Haemorrhagic Septicaemia'],
        ['Zoonosis', 'Transmissible between vertebrate animals and humans (bidirectional)', 'TB, Rabies, Anthrax, Leptospirosis'],
        ['Epidemic', 'Above-normal occurrence within a defined population/area', 'Local EEHV calf deaths in a camp'],
        ['Pandemic', 'Epidemic spreading across countries or continents', 'COVID-19, Influenza'],
        ['Sporadic', 'Occasional cases with no clear pattern; in wildlife, every sporadic case must be investigated', 'Single anthrax death in a sanctuary'],
    ]
)
body(
    'In wildlife, even sporadic cases must be addressed seriously, precisely because the populations '
    'involved are small and vulnerable. The calculus differs entirely from livestock or human epidemiology.'
)
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 2. SPECTRUM OF DISEASE
# ═══════════════════════════════════════════════════════════════════════════════
h1('2  The Spectrum of Disease in Elephants')

h2('2.1  Infectious and Non-Infectious Categories')
body(
    'Both categories are consequential in elephants. On the infectious side the genuinely significant '
    'diseases are comparatively few; those repeatedly flagged as important are tuberculosis, haemorrhagic '
    'septicaemia (HS) and, above all, elephant endotheliotropic herpesvirus (EEHV), which constitutes '
    'the principal subject of this chapter.'
)
add_table(
    ['Category', 'Diseases / Conditions'],
    [
        ['Viral (infectious)', 'EEHV (most important), Rabies, Foot-and-Mouth Disease, Poxvirus (cowpox), EMCV, Emerging RNA viruses'],
        ['Bacterial (infectious)', 'Tuberculosis (M. tuberculosis), Haemorrhagic Septicaemia (Pasteurella), Anthrax (B. anthracis), Clostridial disease, Leptospirosis'],
        ['Parasitic (infectious)', 'Fasciola hepatica / F. jacksoni (liver fluke), Amphistomes (rumen flukes), Strongyles (GI nematodes), Balantidium coli, Haemoparasites'],
        ['Non-infectious', 'Electrocution, Drowning, Trauma / fall, Nutritional deficiency, Obesity (captive), Musth-related injury, Management failures'],
    ]
)

h2('2.2  Management-Related Disease in Captivity')
body(
    'On the non-infectious side, the conditions emphasised are electrocution, accidents and trauma, '
    'and nutritional or management problems — argued to deserve as much priority as infectious diseases. '
    'A substantial point concerns captive elephants specifically. In the wild an elephant walks many '
    'kilometres daily; in captivity it walks very few, with obesity and metabolic disturbance as the '
    'consequence. A vivid laboratory observation: blood drawn from captive animals can be so laden with '
    'fat that the serum will not separate cleanly and appears cloudy (lipaemic) — a direct index of '
    'the cholesterol and fat carried by under-exercised animals. Lack of exercise, obesity and '
    'nutritional deficiency are serious, management-driven problems unique to the captive setting.'
)
key_box([
    '• Captive elephants almost always carry some parasites — presence at necropsy does NOT by itself explain a death',
    '• Lipaemic serum (cloudy, fat-laden) in captive elephants = direct marker of under-exercise and poor management',
    '• Non-infectious causes (electrocution, drowning, trauma) deserve equal investigative rigour as infectious disease',
    '• Every death — infectious or non-infectious — must be fully investigated and documented',
], title='Key Principles: Non-Infectious Disease')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. EEHV
# ═══════════════════════════════════════════════════════════════════════════════
h1('3  Elephant Endotheliotropic Herpesvirus (EEHV)')
body(
    'EEHV is the single most important infectious disease of elephants worldwide. '
    'The greater part of this lecture is devoted to it, because its clinical course is so '
    'rapid and its management so preparation-dependent that it demands thorough understanding '
    'by every field veterinarian and forest officer responsible for elephants.'
)

h2('3.1  Virology and Pathogenesis')
body(
    'EEHV is a herpesvirus — a member of the large family classified into alpha, beta and gamma subfamilies '
    '— but it is highly host-restricted, causing disease in elephants and essentially nothing else. '
    'The name encodes the mechanism: endotheliotropic denotes a tropism for the endothelium, the inner '
    'lining of blood vessels. When the endothelium is attacked, the vessels are damaged and haemorrhage '
    'ensues — blood leaking into the tissues. This is why severe EEHV disease presents as a fulminant '
    'haemorrhagic syndrome, with massive internal bleeding and rapid cardiovascular collapse.'
)
key_box([
    '• Family: Herpesviridae (alpha/beta/gamma subfamilies) — EEHV is in the betaherpesvirus group',
    '• Host-restricted: causes disease only in elephants',
    '• Mechanism: endotheliotropism → endothelial cell lysis → vascular damage → haemorrhage into tissues',
    '• Clinical result: fulminant haemorrhagic syndrome → cardiovascular shock → death within 24–72 hours',
    '• Adults: latent carriers — harbour virus in nerve ganglia without clinical disease',
    '• Calves/juveniles (1–18 yrs): acute fatal disease when maternal antibody wanes',
], title='EEHV Biology')

h2('3.2  Host Susceptibility')
body(
    'EEHV is overwhelmingly a disease of calves and juveniles rather than adults. The window of '
    'vulnerability runs from roughly one year of age into the mid-to-late teens, with the gravest risk '
    'concentrated in the youngest animals. The upper bound is given loosely as around eighteen to twenty '
    'years. Adults are generally not killed by the virus; they typically act as carriers. The practical '
    'corollary: the period from approximately one to fifteen years is when an elephant must be watched '
    'most closely, with near-daily temperature monitoring and prompt response to any fever.'
)

h2('3.3  Viral Subtypes and the Asian Elephant')
body(
    'Multiple subtypes exist. Those relevant to Asian elephants — and the ones developed for screening in '
    'Indian laboratories — are EEHV-1 (with 1A and 1B variants), EEHV-4 and EEHV-5. EEHV-1A/1B are the '
    'most virulent and responsible for the majority of fatal cases. The disease is a particular threat to '
    'Asian elephants, with certain subtypes more dangerous in this species than in African elephants.'
)
add_table(
    ['Subtype', 'Primary Host', 'Virulence in Asian Elephant'],
    [
        ['EEHV-1A', 'Asian elephant', 'HIGHEST — most fatal cases globally and in India'],
        ['EEHV-1B', 'Asian elephant', 'High — documented fatal cases'],
        ['EEHV-4', 'Asian elephant', 'Significant — second most common in Asia; fatal cases documented'],
        ['EEHV-5', 'Asian elephant', 'Moderate — occasionally detected; less frequently fatal'],
        ['EEHV-2, 3, 6, 7', 'African elephant (primarily)', 'Lower risk in Asian species'],
    ]
)

h2('3.4  Historical Background and Research Status')
body(
    'EEHV was first characterised internationally around 1995 to 2002. There remains no commercially '
    'available vaccine and no commercial diagnostic kit, so diagnosis and management depend on in-house '
    'laboratory methods. Western institutions — the Smithsonian, National Zoo, and European zoos — '
    'treated EEHV as a priority early, their captive breeding programmes depending on calf survival. '
    'They pioneered the laboratory work and assisted the establishment of diagnostic capacity in India '
    '(a Kerala laboratory is credited for early Indian work). Within India, clusters of calf deaths '
    'were noted from around 2007–2008 in Kerala and Tamil Nadu, after which systematic screening began; '
    'mortality nonetheless continued to rise, motivating a broader national response.'
)

h2('3.5  Epidemiology in India and the Transboundary Dimension')
body(
    'Most adult Asian elephants are asymptomatic carriers, harbouring and shedding the virus without '
    'overt disease. Surveillance begun around 2015 expanded from early southern cases: positives and '
    'confirmed deaths were subsequently documented in Chhattisgarh (positives in 2021 and 2023) and in '
    'captive and semi-captive camps of northern India. The disease is present across captive facilities '
    'nationally — not confined to the south. Because Asian elephants move between north-eastern India '
    'and South-East Asian countries such as Thailand — which also reports EEHV including subtypes 4 '
    'and 5 — the virus can travel across that porous border. This transboundary dimension justifies '
    'screening all relevant subtypes locally.'
)
add_table(
    ['Year / Period', 'Event'],
    [
        ['1995–2002', 'EEHV first characterised internationally — Smithsonian National Zoo, USA'],
        ['2007–2008', 'First cluster of calf deaths in India — Kerala and Tamil Nadu'],
        ['~2015', 'Systematic national EEHV surveillance begins in India (Dr Karikalan\'s lab)'],
        ['2021', 'Chhattisgarh: first EEHV-positive detected (qPCR from calf death)'],
        ['2023', 'Chhattisgarh: second positive case — active surveillance programme initiated'],
        ['Ongoing', 'Vaccine trials at Pantnagar and Jamnagar, India; mRNA vaccine trial at Houston Zoo, USA'],
    ]
)

h2('3.6  Clinical Course and Field Management')
body(
    'The clinical reality of EEHV is that it progresses extremely rapidly. Once endothelial damage begins, '
    'a calf showing early signs — fever in particular — may deteriorate within hours. A documented case '
    'illustrates the urgency: a call came in around 10 p.m. from a remote camp, and by the time the '
    'attending veterinarian had assessed the calf, returned for medicine and come back, the therapeutic '
    'window had effectively closed. Because the disease is so rapid and camps are frequently distant from '
    'supplies, every elephant camp must be pre-equipped with emergency drugs and fluids in advance — '
    'there is no time to fetch them once symptoms appear.'
)
body(
    'This imperative drives a strong emphasis on biosecurity and husbandry discipline. Each calf should '
    'ideally have its own dedicated mahout and its own equipment, so that neither handlers nor gear move '
    'between animals. Shared equipment and relief arrangements create precisely the cross-contamination '
    'route that must be avoided. When a calf is affected, separation from the herd forms part of '
    'management. Antibody and antigen monitoring should continue throughout the at-risk period '
    '(approximately one to fifteen years). Stress is repeatedly implicated in triggering disease in '
    'carriers and in confounding test results, so its reduction is itself a prevention measure.'
)
key_box([
    '• Temperature check morning and evening for every calf under 15 years — fever is often the first sign',
    '• Camp must have pre-positioned emergency kit: famciclovir, IV fluids, syringes, thermometer',
    '• Each calf must have its own dedicated mahout and equipment — no shared gear',
    '• On any suspected case: isolate the calf, collect blood (EDTA) for qPCR immediately, start antivirals',
    '• Do not wait for qPCR result before beginning treatment — begin on clinical suspicion',
    '• Reduce all sources of stress: noise, new animals, transport, musth males nearby',
], title='EEHV Field Management Protocol')

h2('3.7  Diagnosis')
body(
    'The diagnostic centrepiece is real-time quantitative PCR (qPCR). An explicit parallel is drawn to '
    'COVID-19 testing: just as international travel required a proper RT-PCR result rather than a '
    'rapid alternative, EEHV diagnosis requires qPCR. The reason is the cycle threshold (CT) value, '
    'which is quantitative and permits estimation of viral load. This distinguishes an animal that is '
    'merely a carrier (low viral load = high CT value) from one with active, productive infection '
    '(high viral load = low CT value). A simple positive or negative result is insufficient — without '
    'the CT value, a harmless carrier cannot be told from an animal in the early stages of fatal disease.'
)
add_table(
    ['CT Value', 'Interpretation', 'Action'],
    [
        ['< 30', 'Active viraemia — HIGH viral load', 'Begin treatment IMMEDIATELY; isolate; notify authority'],
        ['30 – 37', 'Low-level positive / carrier state', 'Monitor daily; repeat qPCR in 48 hrs; watch for fever'],
        ['> 37', 'Negative / below detection threshold', 'Continue routine monitoring; repeat monthly'],
    ]
)
body(
    'A critical pathology principle: bone marrow carries the highest viral load and is therefore '
    'the ideal post-mortem sample, remaining diagnostic even when the carcass is partly decomposed. '
    'This principle generalises across multiple diseases — bone marrow should never be omitted at '
    'necropsy for suspected EEHV, anthrax or haemorrhagic septicaemia.'
)
body(
    'Gross post-mortem findings reflect the vascular, haemorrhagic nature of the disease: '
    'swelling of the head, jaw and face; cyanosis (blue discolouration notably of the tongue — '
    'described as especially prominent in EEHV and a useful pointer); and widespread internal '
    'haemorrhage including within the heart. Tongue cyanosis together with the haemorrhagic picture '
    'should always raise EEHV in a calf.'
)
add_table(
    ['Sample', 'Timing', 'Test', 'Notes'],
    [
        ['Whole blood (EDTA)', 'Antemortem — daily monitoring in sick calves', 'qPCR (CT value)', 'Most important antemortem sample; CT value essential'],
        ['Trunk wash (saline lavage)', 'Antemortem — surveillance/carrier detection in adults', 'qPCR', '3 washes on 3 consecutive mornings; pooled sample'],
        ['Bone marrow aspirate', 'Postmortem — FIRST choice', 'qPCR + culture', 'Highest viral load; remains positive in decomposed carcass'],
        ['Heart / Tongue', 'Postmortem', 'qPCR + histopathology (H&E)', 'Highest viral copy numbers; epicardial haemorrhage + tongue cyanosis are key gross lesions'],
        ['Lymph nodes (mesenteric)', 'Postmortem', 'qPCR + histopathology', 'Markedly enlarged and haemorrhagic in EEHV-HD'],
        ['Liver / Lung / Kidney', 'Postmortem', 'qPCR + histopathology', 'Variable viral loads; important for severity assessment'],
    ]
)

h2('3.8  Treatment and the Western Surveillance Model')
body(
    'There is no cure; management is supportive. Antiviral therapy — famciclovir or aciclovir type — '
    'combined with aggressive fluid support, is the mainstay, and the earlier it begins the better '
    'the prognosis. Affected calves weaken very quickly, often cease eating, and require intensive '
    'care without delay. Indian practice is contrasted with the American model, in which every zoo '
    'and captive facility maintains young elephants under close routine surveillance, performing '
    'roughly weekly trunk-wash monitoring so that any rise in viral load is detected early and '
    'treatment commenced before the calf crashes clinically.'
)
add_table(
    ['Drug / Intervention', 'Dose / Route', 'Role'],
    [
        ['Famciclovir', '5.5–8 mg/kg BID orally (in banana/jaggery bolus)', 'First-line antiviral; prodrug of penciclovir; inhibits viral DNA polymerase'],
        ['Aciclovir (Acyclovir)', 'IV slow infusion — for severe/oral-intolerant cases', 'Same antiviral mechanism; use when oral route not possible'],
        ['IV Fluid Therapy', 'Ringer\'s Lactate or Normal Saline IV drip', 'Volume resuscitation for vascular leakage and dehydration'],
        ['Meloxicam / NSAIDs', 'Anti-inflammatory dose', 'Reduce cytokine-mediated inflammatory damage; fever control'],
        ['Omeprazole / Pantoprazole', 'Oral or IV', 'Gastric protectants — prevent stress-related gastric erosion'],
        ['Vitamin C (Ascorbic acid)', 'IV or oral supplementation', 'Antioxidant support; endothelial protective role'],
        ['Dexamethasone', 'Cautious low-dose if needed', 'Anti-inflammatory; use sparingly — may worsen viraemia at high doses'],
    ]
)
body(
    'Vaccine and therapeutic trials are under way both internationally and in India (efforts at '
    'Pantnagar and Jamnagar are mentioned), and some candidates afford partial protection, but none '
    'is yet a finished solution. In the interim: strict biosecurity, supportive care and pre-positioned '
    'drugs in government camps will save calves now, irrespective of future products.'
)
warn_box([
    'Famciclovir MUST be pre-positioned at every elephant camp and zoo housing calves.',
    'Delay in starting antiviral therapy is the single most common cause of treatment failure in EEHV-HD.',
    'Do NOT use high-dose corticosteroids as first-line agents — may accelerate viral replication.',
    'Quarantine the affected calf; test all herd members for viraemia by qPCR; notify Chief Wildlife Warden.',
], title='⚠ EEHV — Critical Treatment Points')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. OTHER INFECTIOUS DISEASES
# ═══════════════════════════════════════════════════════════════════════════════
h1('4  Other Infectious Diseases')

h2('4.1  Rabies')
body(
    'Rabies is noted for wildlife reservoirs beyond the obvious carnivores, with mongooses, jackals '
    'and bats named as maintenance hosts. A difficult diagnostic case involved a captive spotted deer '
    'that died without an obvious bite wound or external sign; the explanation lay in flood water '
    'entering the enclosure and introducing mongooses as the source — a reminder that environmental '
    'and ecological context can account for otherwise baffling cases. The pathology lesson is that '
    'the brain is the only useful diagnostic sample, so it must be collected when rabies is on the '
    'differential, even though handlers are often reluctant to open the skull.'
)
key_box([
    '• Causative agent: Lyssavirus (negative-sense ssRNA; family Rhabdoviridae) — 100% fatal once clinical',
    '• Transmission in elephants: bite of rabid dog (most common in captive settings); occasionally fox or bat',
    '• Incubation: variable (weeks to months) — virus travels along peripheral nerves to CNS',
    '• Clinical signs: sudden behavioural change; aggression; hypersalivation; dysphagia; seizures; coma; death',
    '• BRAIN TISSUE IS THE ONLY DIAGNOSTIC SAMPLE — cerebellum, hippocampus, brainstem (must collect at necropsy)',
    '• Tests: FAT (Fluorescent Antibody Test) — gold standard; Seller\'s stain (rapid, field-applicable);',
    '  Negri bodies on H&E (eosinophilic intracytoplasmic inclusions in Purkinje cells); RT-PCR on brain',
    '• BIOSAFETY: full PPE (gloves, N95, goggles) for all brain handling; post-exposure prophylaxis for exposed personnel',
    '• Wild reservoirs to consider in forest settings: mongoose, jackal, bat — even without visible bite wound',
], title='Rabies — Diagnosis and Field Response')

h2('4.2  Foot-and-Mouth Disease')
body(
    'Foot-and-mouth disease (FMD; Aphthovirus, Picornaviridae; seven serotypes) is rarely reported '
    'as a cause of elephant death. A small number of reports exist (cases from the Kolkata area, '
    'managed with supportive treatment). While FMD-related mortality is possible via secondary '
    'bacterial septicaemia, it does not cause death on anything approaching the scale of EEHV. '
    'The principal concern is spillover from infected livestock at forest fringes. Vesicular lesions '
    'on the feet and trunk tip are the hallmark; diagnosis is by RT-PCR from vesicular fluid '
    'or antigen detection kit (IVRI Mukteswar). Control: vaccination of all surrounding livestock.'
)

h2('4.3  Anthrax')
body(
    'Anthrax is a per-acute, rapidly fatal, haemorrhagic disease — a major killer of African elephants '
    'in particular and a genuine differential for sudden death. A reported sudden death at the Delhi '
    'Zoo illustrates how readily anthrax and EEHV-like haemorrhagic disease can be confused, '
    'and why careful sampling — particularly bone and marrow — together with clinical history '
    'is essential for differentiation.'
)
body(
    'The classic sign at the carcass is thick, tarry, unclotted blood; this may appear at only one '
    'or two sites. The toxins prevent normal clotting, leaving blood thick, dark and tarry. '
    'The epidemiology is dominated by spore persistence: anthrax spores can survive in bone and '
    'soil for thirty years or more, and many modern outbreaks occur when construction or deep '
    'excavation disturbs old contaminated ground. Old contaminated areas must not be disturbed. '
    'Polychrome methylene blue staining of a peripheral blood smear shows the pathognomonic bamboo-rod '
    'shaped bacilli with blue capsule (McFadyean reaction).'
)
warn_box([
    'DO NOT perform a full necropsy on a suspected anthrax carcass in the field.',
    'Collect only peripheral blood smear and sealed blood vials for laboratory confirmation.',
    'WHO/OIE Standard: BURN the carcass and all contaminated material — do NOT bury.',
    '(Burial accelerates sporulation and permanently contaminates the burial site for 30+ years.)',
    'All personnel at scene: full PPE — gloves, N95, goggles, boot covers.',
    'Notify Chief Wildlife Warden, IVRI and District Collector immediately (Section 38P, WPA 1972).',
    'Vaccinate all livestock within 5 km radius with Sterne strain anthrax vaccine.',
], title='⚠ ANTHRAX EMERGENCY PROTOCOL — DO NOT OPEN CARCASS')

h2('4.4  Poxviruses and Emerging RNA Viruses')
body(
    'Pox infections (cowpox and related orthopoxviruses) occur occasionally in elephants; Uttarakhand '
    '(Rajaji captive-elephant context) is cited, with antibody having been found. Continued antibody '
    'and antigen monitoring is recommended so that emergence is caught early. '
    'Vesicular papular eruptions on skin (trunk, ears, periocular, feet) are the hallmark; '
    'histopathology shows eosinophilic intracytoplasmic Guarnieri bodies. Zoonotic risk to handlers '
    '— cowpox is transmissible to humans — requires PPE during case handling.'
)
body(
    'More broadly, the world increasingly contends with RNA viruses, which mutate readily and jump '
    'into new species. Monkeypox (Mpox) is offered as a current example. Rapidly changing RNA viruses '
    'seeking new hosts are identified as the emerging threat to watch. Encephalomyocarditis virus '
    '(EMCV — Cardiovirus, Picornaviridae), transmitted via rodent contamination of feed/water, '
    'causes acute myocarditis and sudden cardiac death in zoo elephants (fatal case at Delhi Zoo).'
)

h2('4.5  Tuberculosis')
body(
    'Tuberculosis is a serious zoonotic problem at the human–elephant interface, distinguished by '
    'its direction of spread: captive elephants frequently acquire human-strain tuberculosis '
    '(Mycobacterium tuberculosis) from their mahouts and handlers rather than the reverse. '
    'TB-positive elephants are reported regularly in the southern states and in captive settings, '
    'and an infected animal may appear outwardly healthy for a long period, revealing disease '
    'only at death (miliary TB lesions in lung at necropsy).'
)
body(
    'The correct samples are the trunk wash and serum. The trunk wash is collected repeatedly over '
    'three to four weeks and screened by culture (Lowenstein-Jensen medium; 6–8 weeks) and PCR '
    '(IS6110 insertion sequence — specific to M. tuberculosis). Only serial sampling permits a '
    'confident determination. Control measures: mahouts and handlers must be screened for '
    'tuberculosis at least annually. India currently lacks a clear, coordinated tuberculosis '
    'policy for captive wildlife — surveillance and control require government-level policy-making.'
)
add_table(
    ['Test', 'Sample', 'Notes'],
    [
        ['Trunk wash culture (LJ medium)', '3 washes, 3 consecutive mornings; pooled', '6–8 weeks for result; sensitivity 60–70%'],
        ['IS6110 PCR', 'Trunk wash or tissue', 'Result in 48–72 hrs; M. tuberculosis specific; more sensitive than culture'],
        ['ElephantTB STAT-PAK / MAPIA', 'Serum', 'Lateral flow; detects antibody; screening tool; cannot distinguish active from latent'],
        ['Ziehl-Neelsen (acid-fast stain)', 'Trunk wash smear or PM tissue', 'Rapid; acid-fast bacilli appear red/pink on blue background'],
        ['PCR on PM tissue', 'Lung / lymph node', 'Use when gross miliary lesions found; IS6110 PCR on fixed or frozen tissue'],
    ]
)
warn_box([
    'TB is a notifiable disease. Report to Chief Wildlife Warden and nearest IVRI / veterinary institute.',
    'Mahouts caring for TB-positive elephants must undergo chest X-ray and sputum test.',
    'Three consecutive negative trunk wash cultures at monthly intervals required before declaring an elephant TB-free.',
    'Treatment (3-drug ATT): Isoniazid 100 mg/day + Pyrazinamide 500 mg/day + Rifampicin 600 mg/day — minimum 12–18 months.',
], title='⚠ TB: Regulatory and Treatment Requirements')

h2('4.6  Haemorrhagic Septicaemia')
body(
    'Haemorrhagic septicaemia (HS) is a stress-triggered bacterial disease that may strike across all '
    'age groups. The causative organism — Pasteurella multocida type B:2 — is a normal inhabitant of '
    'the upper respiratory tract; disease erupts when the animal is stressed by transport, by a '
    'concurrent infection such as EEHV, or by other illness. A positive HS sample from an animal '
    'already dying of something else must not be over-interpreted, since the HS may be secondary; '
    'at other times, however, HS alone is the cause of death.'
)
body(
    'A field investigation at a wildlife sanctuary (Bhavani area, 2021) found an elephant carcass '
    'half-submerged in a stream; the diagnostic breakthrough came from bone marrow, which showed '
    'the characteristic bipolar-staining organisms of Pasteurella ("safety pin" appearance on '
    'Leishman or Gram stain). A contaminated water source was implicated. The control response — '
    'ring vaccination of surrounding animals and livestock, proper carcass disposal — resulted in '
    'no further cases.'
)
key_box([
    '• Causative agent: Pasteurella multocida type B:2 (occasionally E:2)',
    '• Triggers: transport stress, concurrent EEHV, overcrowding, nutritional deficiency, heavy rainfall season',
    '• Clinical: high fever (40–42°C); oedematous swelling of head/neck/brisket; respiratory distress; death in 24–48 hrs',
    '• PM: severe haemorrhagic pneumonia; peracute congestion; haemorrhagic lymph nodes; subcutaneous gelatinous oedema',
    '• Staining: bipolar organism ("safety pin") on Gram or Leishman stain — pathognomonic',
    '• BEST DIAGNOSTIC SAMPLE: bone marrow aspirate from femur or rib — taken within hours of death',
    '• Treatment: Penicillin G 20,000 IU/kg IM; Oxytetracycline; Sulphonamides; IV fluids; Meloxicam',
    '• Prevention: HS vaccination of all livestock within 2 km; separate elephant water sources from cattle wallows',
], title='Haemorrhagic Septicaemia — Field Protocol')

h2('4.7  Clostridial Diseases')
body(
    'Clostridia cause disease through toxin production, becoming dangerous when wounds, liver damage, '
    'or necrotic tissue create anaerobic conditions permitting proliferation. A case from Chhattisgarh '
    '(2022) demonstrated the entero-toxaemic form: a necrotic, haemorrhagic, friable intestine with '
    'ulcers and swollen mesenteric lymph nodes. These findings constitute reliable gross indicators. '
    'The procedural lesson is firm: at necropsy the intestine must always be opened, because the '
    'diagnosis is missed if the gut is not examined.'
)
add_table(
    ['Species', 'Disease', 'Key Gross Finding'],
    [
        ['C. difficile', 'Pseudomembranous enterocolitis', 'Haemorrhagic diarrhoea; pseudomembrane on colonic mucosa; associated with antibiotic use'],
        ['C. perfringens (Type A/D)', 'Enterotoxaemia', 'Sudden death; bloat; haemorrhagic, necrotic, friable intestine; swollen mesenteric LN'],
        ['C. tetani', 'Tetanus', 'Muscular rigidity; lockjaw; opisthotonus; triggered by wound infection (rare in elephants)'],
        ['C. botulinum', 'Botulism', 'Flaccid paralysis; toxin from contaminated feed; peracute death possible'],
    ]
)
warn_box([
    'DO NOT open intestinal loops of suspected Clostridial cases in the field.',
    'Collect sealed intestinal contents in sterile container within 1–2 hours of death for toxin ELISA.',
    'Clostridial toxins dissipate rapidly after death — delayed collection renders toxin detection useless.',
    'Always open the intestine at necropsy and examine the mucosa — do not skip this step.',
], title='⚠ Clostridial: Sample Collection and Necropsy Protocol')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. PARASITIC DISEASE
# ═══════════════════════════════════════════════════════════════════════════════
h1('5  Parasitic Disease')

h2('5.1  Helminth Burdens')
body(
    'The interpretation of parasitism begins from a crucial principle: captive elephants almost '
    'always carry some parasites, so their presence at necropsy does not by itself explain a death. '
    'The skill lies in distinguishing incidental parasitism from clinically significant disease, '
    'marked by emaciation, fluid accumulation in body cavities (transudate), and hypoproteinaemia. '
    'Liver flukes of the Fasciola type are particularly dangerous, causing hepatic fibrosis; the '
    'liver should always be examined carefully for fibrosis when incised at necropsy. Rumen and '
    'stomach flukes (amphistomes such as Pseudodiscus collinsi) are also commonly recovered, with '
    'migrating immature flukes producing toxic damage to the intestinal mucosa.'
)
add_table(
    ['Parasite', 'Type', 'Site', 'Significance / Gross Finding'],
    [
        ['Fasciola jacksoni', 'Trematode (liver fluke)', 'Bile ducts / Liver', 'Hepatic fibrosis; emaciation; Fasciola eggs in bile at necropsy; incise liver to detect'],
        ['Pseudodiscus collinsi', 'Amphistome (rumen fluke)', 'Large intestine / Caecum', 'Heavy burdens → colitis; reddish-brown flukes attached to mucosa at PM; immature flukes toxic'],
        ['Strongyles (GI nematodes)', 'Nematode', 'Small/large intestine', 'Protein loss enteropathy; hypoproteinaemia; larval hepatic migration; distinguish from incidental'],
        ['Oxyuris (pinworm)', 'Nematode', 'Rectum', 'Tail rubbing; anal irritation; common in captive elephants; rarely clinically significant'],
        ['Toxocara (in calves)', 'Nematode', 'Small intestine', 'Pot-belly; poor growth; visceral larva migrans; important in young captive calves'],
    ]
)
body(
    'Treatment of significant helminth burdens: Ivermectin (0.1–0.2 mg/kg SC or oral); Albendazole '
    '(10–15 mg/kg oral for Fasciola and Strongyles); Oxyclozanide for liver flukes. Strategic '
    'deworming 2–4 times per year is standard practice in well-managed captive facilities.'
)

h2('5.2  Protozoal and Blood Parasites')
body(
    'Amoebiasis (Entamoeba spp.) is essentially a hygiene problem, shared with humans and acquired '
    'from unhygienic feeding — which also transmits coccidia, rotavirus and other organisms. '
    'Treatment: Metronidazole 15–25 mg/kg BID for 5 days; improve fodder hygiene and water source.'
)
body(
    'A blood-parasite case is described: an elephant of approximately 35 years in the Nilgiris '
    '(Tamil Nadu) was found terminal and died within about half an hour, carrying an enormous tick '
    'burden. Tick-borne haemoparasites (Trypanosoma, Babesia, Theileria) brought the animal down '
    'rapidly. For blood parasites, a fresh wet-film examination of peripheral blood can be '
    'diagnostic immediately in the field. Tick control with acaricides (Amitraz wash, Ivermectin) '
    'is the prevention cornerstone.'
)
key_box([
    '• Principle: parasites at necropsy ≠ cause of death — look for emaciation + cavity fluid + hypoproteinaemia',
    '• Fasciola: always incise the liver at necropsy and palpate for fibrosis',
    '• Blood parasites: fresh wet film from peripheral blood = immediate field diagnosis',
    '• Tick burden: active acaricide control essential; heavy ticks = high haemoparasite risk',
    '• Balantidium coli: yellow diarrhoea; treat with Metronidazole + Omeprazole',
    '• Hygiene: clean water and uncontaminated fodder prevent amoeba, coccidia and rotavirus',
], title='Parasites — Key Principles')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 6. PRINCIPLES FOR FIELD PRACTICE
# ═══════════════════════════════════════════════════════════════════════════════
h1('6  Principles for Field Practice')
body(
    'Several broadly applicable principles close the lecture. On bacterial and foot problems the '
    'overriding message is not to treat blindly. Where there is a wound, abscess or non-healing '
    'infection, a pus or swab sample must be collected, sent to the laboratory and subjected to '
    'antibiotic-sensitivity testing rather than treated by guesswork. Chronic infections — '
    'such as deep sinus tracts — may require months of repeated sampling and adjusted treatment. '
    'Routine foot care (untrimmed nails, minor injuries, abscesses and lameness compounded by '
    'obesity) demands the same discipline: sample, identify, and treat appropriately.'
)
body(
    'A further theme is self-improvement and documentation. Every case should be photographed '
    'and a personal repository of post-mortem and clinical images assembled. Over five years of '
    'disciplined documentation each practitioner accumulates an archive that makes them an expert '
    'and a teacher. Remote consultation on good images often allows the laboratory to indicate '
    'a diagnosis. The practitioner must cultivate the habit of generating differentials — '
    'reasoning that a given sign could indicate one condition but might equally indicate another '
    '— rather than leaping to a single conclusion.'
)
key_box([
    '• Never treat a wound or abscess blind — culture first; antibiotic sensitivity testing before prescribing',
    '• Disk diffusion / Kirby-Bauer method available at district labs — use it routinely',
    '• Document every case: photograph scene, carcass position, gross PM findings, all samples',
    '• Voice narrate PM video — describe findings as you make them; review later with laboratory colleagues',
    '• Build a personal case archive — 5 years of disciplined documentation = expert-level competency',
    '• Generate differentials at every case — do not jump to one conclusion; list all possibilities, then eliminate',
    '• Submit necropsy report within 48 hours using standard DFO/CWL format',
    '• Maintain contact with a reference laboratory (IVRI, Wildlife Institute, CCMB, State lab)',
], title='Professional Practice Principles')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 7. EMERGING THREATS
# ═══════════════════════════════════════════════════════════════════════════════
h1('7  Emerging Threats and Preparedness')
body(
    'A concluding discussion ranged over emerging viruses and pandemic preparedness. The trend '
    'towards RNA viruses was reiterated, as was the vulnerability of a country with high population '
    'density and close human–animal contact to the next spillover event. Discussion touched on '
    'host adaptation through mutation and on whether agents such as EEHV might possess wider host '
    'ranges — the honest answer being that this cannot be settled without dedicated research.'
)
body(
    'Management answers returned to the core doctrine: reliance on qPCR and the distinction between '
    'an antibody-positive carrier and an animal with active infection; heavy reliance on biosecurity; '
    'environmental sampling as part of disease management; and acceptance that some mortality is '
    'unavoidable — the goal being not zero deaths but thorough investigation of every death so '
    'that lessons are carried forward.'
)
key_box([
    '• RNA viruses mutate readily and jump species — monitor for unusual mortality clusters and novel presentations',
    '• Monkeypox (Mpox): documented in captive elephants from Africa; vesicular skin lesions; zoonotic to handlers',
    '• SARS-CoV-2 antibodies detected in captive elephants (Belgium, 2021) — coronaviruses can infect elephants',
    '• Cyanobacteria/algal bloom toxins: Botswana 2020 — 350 elephants died around waterholes in single event',
    '• Climate change: shifts in vector range; altered disease seasonality; increased heat stress events',
    '• Key preparedness measure: investigate EVERY death thoroughly — preparedness is built one case at a time',
    '• Antibiotic resistance: mandatory sensitivity testing before treatment in elephants near human settlements',
], title='Emerging Threats — Key Awareness Points')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# 8. CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
h1('8  Conclusion')
body(
    'Mortality investigation in wildlife is fundamentally a conservation tool, and this is why '
    'even a single death is investigated thoroughly. Among elephant diseases, EEHV is the dominant '
    'infectious killer — a host-specific herpesvirus that destroys the lining of blood vessels and '
    'causes fatal haemorrhage in calves and juveniles up to about fifteen years of age, with adults '
    'serving as silent carriers. Because the disease is explosively rapid, survival depends on '
    'early detection by qPCR with CT values, pre-positioned emergency drugs at every camp, strict '
    'biosecurity with dedicated handlers, immediate supportive and antiviral therapy, and the '
    'collection of correct samples at necropsy — above all, bone marrow.'
)
body(
    'Surrounding EEHV are the other agents a wildlife pathologist must hold in mind: '
    'rabies (brain sample only; wild reservoirs including mongoose, jackal and bat); '
    'anthrax (per-acute haemorrhagic death, non-clotting tarry blood, spores persisting for '
    'decades — old burial sites must not be disturbed); foot-and-mouth disease; poxviruses and '
    'emerging RNA viruses; tuberculosis (a zoonosis from humans to elephants, requiring serial '
    'trunk washes and a national policy India still lacks); haemorrhagic septicaemia '
    '(stress-triggered Pasteurella, confirmable from bone marrow even in decomposed carcasses); '
    'and clostridial disease (haemorrhagic ulcerated gut with swollen lymph nodes — the intestine '
    'must always be opened at necropsy).'
)
body(
    'Parasites are nearly universal, so the discipline is to separate incidental burdens from '
    'genuine disease marked by emaciation, cavity fluid and hypoproteinaemia. Underlying all of '
    'it is one consistent professional discipline: collect the correct sample, perform a systematic '
    'necropsy, document every case, maintain contact with a laboratory, keep learning, and '
    'investigate every single death — because in conservation medicine, preparedness is built '
    'one case at a time.'
)
key_box([
    '1. EEHV — highest priority; pre-position famciclovir; early recognition saves lives',
    '2. Anthrax — zero-necropsy protocol; burn all material; never bury',
    '3. TB — chronic silent killer; mandatory surveillance of elephants and handlers; serial trunk washes',
    '4. Rabies — brain is the ONLY diagnostic sample; full PPE; post-exposure prophylaxis for exposed personnel',
    '5. HS / Clostridial — bone marrow is gold-standard PM sample; collect before lysis; always open gut at necropsy',
    '6. Parasites — distinguish incidental burden from clinical disease (emaciation + cavity fluid + hypoproteinaemia)',
    '7. Documentation — systematic photography, GPS, lab submission = as important as clinical intervention',
    '8. Preparedness — investigate EVERY death; build competency one case at a time',
], title='Summary: 8 Key Take-Aways for Field Veterinarians')

spacer()
doc.add_paragraph(
    'Note on sources: Compiled from audio recordings of lectures by Dr M. Karikalan '
    '(Senior Scientist, Centre for Wildlife), Sessions SH_1_3, Parts 1 and 2, '
    'each approximately 36 minutes. Technical content has been reconstructed and clarified '
    'from transcripts; the closing discussion was heavily degraded and is summarised. '
    'Specific figures, place names and proper nouns should be verified against the original '
    'lecture materials before any scholarly or published use.',
    style='C3Note'
)

# ── Save ──────────────────────────────────────────────────────────────────────
out = '/home/user/Workshop-on-Conference/Workshop_Chapter3_DOCX_Only_2026.docx'
doc.save(out)
print(f'Written: {out} ({os.path.getsize(out)//1024} KB)')

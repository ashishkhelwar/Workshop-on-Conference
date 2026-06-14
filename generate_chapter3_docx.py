#!/usr/bin/env python3
"""Generate Chapter 3 as a Word (.docx) file."""

import os, io
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image as PILImage

PDF_PAGES = '/tmp/ch3_pages_j'  # JPEG renders of source PDF (original, not rotated)

doc = Document()

# ── Page setup: A4 ────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Cm(21)
section.page_height = Cm(29.7)
section.left_margin = section.right_margin = Cm(2.5)
section.top_margin  = section.bottom_margin = Cm(2)

# ── Styles ────────────────────────────────────────────────────────────────────
styles = doc.styles

def set_style(style_name, base='Normal', font_name='Calibri', font_size=11,
              bold=False, italic=False, color=None, space_before=0, space_after=6, align=None):
    try:
        st = styles[style_name]
    except KeyError:
        st = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = styles[base] if base in [s.name for s in styles] else styles['Normal']
    st.font.name = font_name
    st.font.size = Pt(font_size)
    st.font.bold = bold
    st.font.italic = italic
    if color:
        st.font.color.rgb = RGBColor(*color)
    st.paragraph_format.space_before = Pt(space_before)
    st.paragraph_format.space_after  = Pt(space_after)
    if align:
        st.paragraph_format.alignment = align
    return st

set_style('CH3 Chapter Label', font_size=13, bold=True, color=(46, 106, 79), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
set_style('CH3 Title', font_size=24, bold=True, color=(27, 67, 50), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8)
set_style('CH3 Subtitle', font_size=12, color=(82, 183, 136), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4)
set_style('CH3 Section', font_size=15, bold=True, color=(27, 67, 50), space_before=18, space_after=6)
set_style('CH3 Subsection', font_size=12, bold=True, color=(45, 106, 79), space_before=10, space_after=4)
set_style('CH3 Body', font_size=10.5, space_before=3, space_after=4)
set_style('CH3 Bullet', font_size=10.5, space_before=2, space_after=2)
set_style('CH3 Caption', font_size=9, italic=True, color=(45, 106, 79), align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)
set_style('CH3 Warning', font_size=10.5, bold=True, color=(214, 40, 40), space_before=3, space_after=3)
set_style('CH3 Key', font_size=10.5, bold=True, color=(27, 67, 50), space_before=3, space_after=3)


def h(text, style='CH3 Section'):
    doc.add_paragraph(text, style=style)

def p(text, style='CH3 Body'):
    doc.add_paragraph(text, style=style)

def b(text):
    doc.add_paragraph(text, style='CH3 Bullet')

def cap(text):
    doc.add_paragraph(text, style='CH3 Caption')

def hr():
    doc.add_paragraph('─' * 80, style='CH3 Body')

def add_image_page(page_num, width_inches=5.5, caption_text=None):
    """Embed a rendered PDF page as an image."""
    fname = os.path.join(PDF_PAGES, f'page_{page_num:02d}.jpg')
    if not os.path.exists(fname):
        return
    try:
        doc.add_picture(fname, width=Inches(width_inches))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption_text:
            cap(caption_text)
    except Exception as e:
        p(f'[Image: PDF page {page_num} — {e}]')

def add_table(headers, rows, col_widths=None):
    """Add a formatted table."""
    ncols = len(headers)
    t = doc.add_table(rows=1 + len(rows), cols=ncols)
    t.style = 'Table Grid'
    # Header row
    hdr = t.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr[i].text = h_text
        run = hdr[i].paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9)
        # Dark green background
        tc = hdr[i]._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '1B4332')
        tcPr.append(shd)
    # Data rows
    for r_idx, row_data in enumerate(rows):
        row = t.rows[r_idx + 1].cells
        for c_idx, cell_text in enumerate(row_data):
            row[c_idx].text = cell_text
            row[c_idx].paragraphs[0].runs[0].font.size = Pt(9)
            if r_idx % 2 == 0:
                tc = row[c_idx]._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), 'D8F3DC')
                tcPr.append(shd)
    doc.add_paragraph('')


# ═══════════════════════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_paragraph('CHAPTER 3', style='CH3 Chapter Label')
doc.add_paragraph('Infectious Diseases of Asian Elephants', style='CH3 Title')
doc.add_paragraph('Resource Person: Dr. M. Karikalan, MVSc, PhD', style='CH3 Subtitle')
doc.add_paragraph('Assistant Professor, Dept. of Wildlife Science, VBSC & AH, Namakkal', style='CH3 Subtitle')
doc.add_paragraph('Workshop on Elephant Mortality Investigation and Management', style='CH3 Subtitle')
doc.add_paragraph('Chhattisgarh Forest Department · Bilaspur · June 2026', style='CH3 Subtitle')
doc.add_paragraph('')

add_image_page(1, width_inches=5.5, caption_text='Source presentation: Infectious Diseases of Asian Elephants (Dr. M. Karikalan, 2026)')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Introduction
# ═══════════════════════════════════════════════════════════════════════════════
h('1. Introduction')
p('Wildlife disease investigation has emerged as a critical pillar of conservation medicine. The Asian elephant, classified as Endangered on the IUCN Red List, faces an escalating burden of infectious and non-infectious diseases. Mortality from preventable or treatable diseases can be mitigated through timely diagnosis, skilled post-mortem examination, and preparedness of field veterinarians.')

h('1.1 Epidemiological Terminology', 'CH3 Subsection')
add_table(
    ['Term', 'Definition'],
    [
        ['Emerging Disease', 'A disease appearing in a population for the first time, or rapidly increasing in incidence/geographic range'],
        ['Re-emerging Disease', 'A previously known disease that has reappeared after decline, often in new geographic areas or host species'],
        ['Transboundary Disease', 'Infectious disease that spreads across national/ecosystem boundaries (e.g., FMD, HS)'],
        ['Zoonosis', 'Disease transmissible between vertebrate animals and humans (e.g., TB, Rabies, Anthrax, Leptospirosis)'],
        ['Spillover', 'Transmission of a pathogen from a reservoir host to a new incidental host species'],
        ['Virulence', 'Severity of disease caused by a pathogen; degree of harm inflicted on the host'],
    ]
)

h('1.2 Taxonomy of Asian Elephant', 'CH3 Subsection')
add_table(
    ['Classification', 'Value'],
    [
        ['Kingdom', 'Animalia'], ['Phylum', 'Chordata'], ['Class', 'Mammalia'],
        ['Order', 'Proboscidea'], ['Family', 'Elephantidae'], ['Genus', 'Elephas'],
        ['Species', 'Elephas maximus'],
        ['Subspecies', 'E. m. indicus (Indian), E. m. maximus (Sri Lankan), E. m. sumatranus (Sumatran), E. m. borneensis (Borneo)'],
    ]
)

h('1.3 Spectrum of Disease', 'CH3 Subsection')
add_table(
    ['Infectious Diseases', 'Non-Infectious Conditions'],
    [
        ['Viral: EEHV, Rabies, FMD, Poxvirus, EMCV', 'Electrocution (illegal/accidental)'],
        ['Bacterial: TB, Haemorrhagic Septicaemia, Anthrax, Clostridial, Leptospirosis', 'Drowning / Water body falls'],
        ['Parasitic: Fasciola, Strongyles, Amphistomes, Balantidium, Haemoparasites', 'Trauma / Fall from height'],
        ['Fungal: Aspergillosis (captive)', 'Obesity / Nutritional deficiency / Captive management failures'],
    ]
)

add_image_page(6, width_inches=5.5, caption_text='Fig 1.1 — Infectious vs Non-infectious disease classification')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — EEHV
# ═══════════════════════════════════════════════════════════════════════════════
h('2. Elephant Endotheliotropic Herpesvirus (EEHV)')
p('EEHV is the single most important viral disease in elephants. It causes acute haemorrhagic disease — an apparently healthy calf can die within 24–72 hours of first signs. Calves between 1–18 years are primarily affected; adult elephants are latent carriers.')

h('2.1 Classification and Subtypes', 'CH3 Subsection')
add_table(
    ['Subtype', 'Host', 'Significance'],
    [
        ['EEHV-1A / 1B', 'Asian elephant', 'Most virulent; majority of fatal cases in Asia and North America'],
        ['EEHV-4', 'Asian elephant', 'Second most common; documented fatal cases'],
        ['EEHV-5', 'Asian elephant', 'Occasionally detected; less frequently fatal'],
        ['EEHV-2, 3, 6, 7', 'African elephant', 'Lower risk in Asian species'],
    ]
)

add_image_page(7, width_inches=5.5, caption_text='Fig 2.1 — Herpesvirus family classification and EEHV position')
add_image_page(8, width_inches=5.5, caption_text='Fig 2.2 — EEHV phylogenetic tree and fatal haemorrhagic disease history')

h('2.2 Timeline: EEHV in India and Chhattisgarh', 'CH3 Subsection')
add_table(
    ['Year', 'Event'],
    [
        ['1995', 'First EEHV-HD case — Smithsonian National Zoo, USA'],
        ['2007', 'First confirmed case in India (Kerala, retrospective diagnosis)'],
        ['2008–2015', 'Cases in Tamil Nadu (Anamalai TR, Mudumalai)'],
        ['2021', 'Chhattisgarh: EEHV-1A positive detected (qPCR from calf death)'],
        ['2023', 'Chhattisgarh: Second positive case — active surveillance initiated'],
        ['2024', 'mRNA-based EEHV vaccine enters trial — Houston Zoo, USA'],
    ]
)

h('2.3 Pathomechanism', 'CH3 Subsection')
add_image_page(9, width_inches=5.5, caption_text='Fig 2.3 — EEHV host preference by age group and pathomechanism cascade')
b('1. EEHV infects endothelial cells of capillaries and venules')
b('2. Endothelial lysis → capillary leakage → haemorrhage into tissues')
b('3. Cytokine storm → hypotension → shock')
b('4. Myocardial, hepatic and renal involvement → death within hours to days')
b('5. Gross lesions: Epicardial haemorrhages, tongue cyanosis, facial oedema, petechiation')

h('2.4 Clinical Signs', 'CH3 Subsection')
b('• Generalised oedema of head, face and neck — especially periorbital and submandibular swelling (hallmark sign)')
b('• Tongue cyanosis: blue-purple discolouration (visible in live animal)')
b('• Open-mouth breathing and respiratory distress due to oropharyngeal oedema')
b('• Weakness, recumbency; rapid deterioration to lateral recumbency')
b('• Pyrexia (fever >38.5°C) often the first sign detected')
b('• Death within 24–72 hours in untreated or late-detected cases')

add_image_page(11, width_inches=5.5, caption_text='Fig 2.4 — Clinical photos: EEHV-HD in a calf (Nandankanan Zoological Park)')

h('2.5 Post-Mortem Findings', 'CH3 Subsection')
b('• Tongue: diffuse cyanosis/necrosis; dark blue-black discolouration on cut section')
b('• Heart: epicardial and endocardial petechiae and ecchymoses; myocardial mottling')
b('• Liver: congestion; occasional petechiae; hepatocellular swelling')
b('• Lung: congestion and oedema; interstitial haemorrhage')
b('• Lymph nodes: markedly enlarged, haemorrhagic')
b('• Kidney: cortical pallor, perivascular haemorrhage')
add_image_page(12, width_inches=5.5, caption_text='Fig 2.5 — PM photos: tongue cyanosis (ERRC Surajpur), epicardial haemorrhages, myocardial lesions')

h('2.6 Histopathology (H&E)', 'CH3 Subsection')
b('• Tongue mucosa: intranuclear inclusion bodies in endothelial cells; sub-epithelial haemorrhage')
b('• Myocardium: perivascular lymphocytic infiltration; myocyte necrosis; endothelial inclusions (H&E ×200)')
b('• Pulmonary sinusoids: endothelial inclusions; alveolar capillary congestion')
b('• Renal vessels: glomerular and interstitial haemorrhage; endothelial inclusions')
add_image_page(13, width_inches=5.5, caption_text='Fig 2.6 — Histopathology H&E ×200: tongue mucosa, myocardium, pulmonary sinusoids, renal vessels')

h('2.7 Laboratory Diagnosis: qPCR', 'CH3 Subsection')
add_table(
    ['Sample', 'Use', 'CT Value Interpretation'],
    [
        ['Whole blood (EDTA)', 'Antemortem surveillance; monitoring sick calves', 'CT <30: Active viraemia (treat immediately); CT 30–37: Low-level positive/carrier; CT >37: Negative'],
        ['Bone marrow aspirate', 'Best postmortem sample', 'Highest sensitivity — preferred for PM diagnosis'],
        ['Trunk wash', 'Detection of viral shedding in adults', 'Herd surveillance; lower sensitivity than blood PCR'],
        ['Heart / Tongue / Lymph node', 'PM tissue qPCR + histopathology', 'Heart and tongue — highest viral copy numbers in EEHV-HD'],
    ]
)
add_image_page(14, width_inches=5.5, caption_text='Fig 2.7 — Tissue viral load data (qPCR) and qPCR vs conventional PCR comparison')

h('2.8 Treatment Protocol', 'CH3 Subsection')
doc.add_paragraph('⚠ EEHV-HD is a veterinary emergency — begin treatment on clinical suspicion; do NOT wait for PCR results.', style='CH3 Warning')
b('• Famciclovir 5.5–8 mg/kg BID orally — antiviral prodrug; first-line agent; MUST be pre-positioned at all elephant camps')
b('• Acyclovir IV — in severe cases; slow IV infusion')
b('• Fluid therapy: Ringer\'s Lactate / Normal Saline IV — volume resuscitation for vascular leakage')
b('• Anti-inflammatory: Dexamethasone (cautious use) or Meloxicam')
b('• Gastric protectants: Omeprazole / Pantoprazole')
b('• Monitoring: Temperature every 4 hr; blood qPCR every 24–48 hr; CBC and chemistry every 48 hr')
add_image_page(15, width_inches=2.7, caption_text='Fig 2.8a — Treatment protocol')
add_image_page(16, width_inches=2.7, caption_text='Fig 2.8b — Monitoring, prevention and mRNA vaccine update')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Rabies
# ═══════════════════════════════════════════════════════════════════════════════
h('3. Rabies in Elephants')
p('Rabies (Lyssavirus, Rhabdoviridae) is a fatal zoonotic neurological disease. While uncommon in elephants, confirmed cases have been documented in captive individuals following contact with infected dogs. Invariably fatal once clinical signs appear.')
b('• Transmission: bite of rabid dog (most common); rarely fox or bat')
b('• Clinical signs: sudden behavioural change; aggression; hypersalivation; dysphagia; seizures; coma; death')
b('• Sample: BRAIN TISSUE ONLY (cerebellum, hippocampus, brainstem) for rabies diagnosis')
b('• FAT (Fluorescent Antibody Test): gold standard for diagnosis')
b('• Histopathology: Negri bodies (eosinophilic intracytoplasmic inclusions in Purkinje cells, H&E ×400)')
b('• Seller\'s stain: rapid field stain for Negri bodies (×1000 — appear magenta on blue background)')
b('• RT-PCR: most sensitive; can use preserved tissue')
b('• BIOSAFETY: handle brain with gloves, N95, eye protection; post-exposure prophylaxis for exposed persons')
add_image_page(17, width_inches=5.5, caption_text='Fig 3.1 — Rabies: transmission cycle, Negri body histology (H&E ×400), Seller\'s stain ×1000, FAT smear, RT-PCR gel')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — FMD
# ═══════════════════════════════════════════════════════════════════════════════
h('4. Foot and Mouth Disease (FMD)')
p('FMD (Aphthovirus, Picornaviridae; 7 serotypes) can spillover from infected livestock to elephants at forest fringes. Rarely causes death but severe cases with secondary septicaemia can be fatal.')
b('• Clinical signs: vesicular lesions on feet and trunk tip; lameness; drooling; fever')
b('• Diagnosis: clinical vesicles; RT-PCR from vesicular fluid; ELISA serology; antigen detection kit (IVRI Mukteswar)')
b('• Control: vaccination of all surrounding livestock; movement restrictions; lime disinfection')
add_image_page(18, width_inches=5.5, caption_text='Fig 4.1 — FMD: vesicular lesions on foot, isolation protocol')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Poxvirus & EMCV
# ═══════════════════════════════════════════════════════════════════════════════
h('5. Poxvirus and EMCV')
h('5.1 Poxvirus (Cowpox / Elephantpox)', 'CH3 Subsection')
p('Elephants can be infected with cowpox virus (Orthopoxvirus) from infected rodents or dairy cattle. Zoonotic risk — keepers must use PPE.')
b('• Lesions: papular/vesicular eruptions on skin (trunk, ears, periocular, feet); gross lung lesions in severe systemic cases')
b('• Diagnosis: electron microscopy; PCR; histopathology (Guarnieri bodies — eosinophilic intracytoplasmic inclusions)')
b('• Treatment: symptomatic; wound care; antibiotics for secondary infection; tecovirimat in severe cases')
add_image_page(20, width_inches=5.5, caption_text='Fig 5.1 — Poxvirus: vesicular skin lesions on Asian elephant skin and gross lung lesions')

h('5.2 Encephalomyocarditis Virus (EMCV)', 'CH3 Subsection')
p('EMCV (Cardiovirus, Picornaviridae) causes acute myocarditis and sudden cardiac death. Transmitted via rodent contamination of food/water. Fatal case documented at Delhi Zoo.')
b('• PM findings: haemorrhagic myocarditis; pale myocardium; pericardial effusion')
b('• Diagnosis: virus isolation; serology (ELISA); histopathology; rodent control as prevention')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Tuberculosis
# ═══════════════════════════════════════════════════════════════════════════════
h('6. Tuberculosis (TB)')
p('Mycobacterium tuberculosis (human strain) causes TB in captive elephants — primarily a reverse zoonosis (humans infect elephants). Chronic, slowly progressive, often clinically silent for years. Infected elephants can shed bacilli to mahouts.')

h('6.1 Diagnosis', 'CH3 Subsection')
b('• Trunk wash (TW): 3 washes on 3 consecutive mornings; pooled sample for culture (LJ medium, 6–8 weeks) or PCR')
b('• Serology: ElephantTB STAT-PAK / MAPIA — lateral flow assay; detects antibodies; serial testing increases sensitivity')
b('• PM: miliary TB lesions in lung/lymph nodes; Ziehl-Neelsen acid-fast staining; IS6110 PCR (M. tuberculosis specific)')
add_image_page(21, width_inches=2.7, caption_text='Fig 6.1a — Acid-fast staining, IS6110 PCR gel, LFA kit (TB STAT-PAK)')
add_image_page(22, width_inches=2.7, caption_text='Fig 6.1b — USDA diagnostic flowchart; free-range elephant lung with miliary TB lesions')

h('6.2 Treatment (Anti-Tubercular Therapy — minimum 12–18 months)', 'CH3 Subsection')
b('• Isoniazid (INH): 100 mg/day or 4–5 mg/kg')
b('• Pyrazinamide (PZA): 500 mg/day or 25–30 mg/kg (first 2 months)')
b('• Rifampicin (RIF): 600 mg/day or 10–15 mg/kg')
b('• Monitor liver enzymes monthly (AST, ALT) — hepatotoxicity risk')
b('• Pyridoxine (Vitamin B6) supplementation to prevent INH neuropathy')
doc.add_paragraph('⚠ TB is notifiable. Mahouts of TB-positive elephants must undergo chest X-ray. Three negative trunk wash cultures required before declaring TB-free.', style='CH3 Warning')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — Anthrax
# ═══════════════════════════════════════════════════════════════════════════════
h('7. Anthrax')
p('Caused by Bacillus anthracis (Gram-positive, aerobic, spore-forming). Causes peracute to acute disease; death within hours. Spores persist in soil 30–100 years.')
b('• Pathognomonic sign: non-clotting tarry (dark watery) blood from all natural orifices')
b('• DO NOT open the carcass in field — sporulation occurs on air contact; contaminates site for decades')
b('• Staining: polychrome methylene blue (McFadyean reaction) — bamboo-rod shaped bacilli with blue capsule; pathognomonic')
b('• Outbreaks occur in hot/dry seasons followed by rainfall; documented at Joyepur Forest Range, Dibrugarh, Assam')
add_image_page(23, width_inches=5.5, caption_text='Fig 7.1 — Anthrax: carcass findings, polychrome methylene blue staining (bamboo-rod bacilli), field investigation (Joyepur Forest Range, Assam)')
doc.add_paragraph('⚠ ANTHRAX EMERGENCY: BURN carcass and all material — do NOT bury. Full PPE. Notify Chief Wildlife Warden. Vaccinate all livestock within 5 km.', style='CH3 Warning')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — HS
# ═══════════════════════════════════════════════════════════════════════════════
h('8. Haemorrhagic Septicaemia (HS)')
p('Caused by Pasteurella multocida type B:2. Primarily a bovid disease but elephants are susceptible under stress. Peracute — death within 24–48 hours. Outbreaks investigated at Kalahandi, Odisha and Kartapat WLS.')
b('• Clinical signs: high fever (40–42°C); oedematous swelling of head/neck/brisket; respiratory distress; death in 24–48 hr')
b('• PM findings: severe haemorrhagic pneumonia; peracute congestion; haemorrhagic lymph nodes; subcutaneous gelatinous oedema')
b('• Staining: bipolar organism ("safety pin" appearance) on Gram or Leishman stain')
b('• Best diagnostic sample: BONE MARROW aspirate from femur or rib (taken within hours of death)')
b('• Treatment: Penicillin G 20,000 IU/kg IM; Tetracycline; Sulphonamides; fluid therapy; Meloxicam')
b('• Prevention: HS vaccination of all livestock within 2 km; separate elephant water sources from cattle wallows')
add_image_page(24, width_inches=2.7, caption_text='Fig 8.1a — HS: bipolar organisms (Leishman stain), haemorrhagic lung lesions, lymphadenopathy')
add_image_page(25, width_inches=2.7, caption_text='Fig 8.1b — HS field investigation: Kartapat WLS — trackers, necropsy team, carcass disposal')
add_image_page(26, width_inches=5.5, caption_text='Fig 8.2 — HS control: livestock vaccination and bone marrow sampling protocol')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — Clostridial
# ═══════════════════════════════════════════════════════════════════════════════
h('9. Clostridial Infections')
add_table(
    ['Species', 'Disease', 'Key Features'],
    [
        ['C. difficile', 'Pseudomembranous enterocolitis', 'Watery/haemorrhagic diarrhoea; pseudomembrane on colonic mucosa; associated with antibiotic use'],
        ['C. perfringens (Type A/D)', 'Enterotoxaemia', 'Sudden death; bloat; haemorrhagic enteritis; toxin detection by ELISA from intestinal contents'],
        ['C. tetani', 'Tetanus', 'Muscular rigidity; lockjaw; opisthotonus; triggered by wound infection'],
        ['C. botulinum', 'Botulism', 'Flaccid paralysis; toxin from contaminated feed; peracute death possible'],
    ]
)
doc.add_paragraph('⚠ Do NOT open intestinal loops in field for suspected Clostridial cases. Collect sealed intestinal samples within 1–2 hours of death for toxin ELISA.', style='CH3 Warning')
add_image_page(27, width_inches=5.5, caption_text='Fig 9.1 — Clostridial: C. difficile enterocolitis (gross mucosa), published case literature')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — Leptospirosis
# ═══════════════════════════════════════════════════════════════════════════════
h('10. Leptospirosis')
p('Leptospira spp. (spirochete) — globally important zoonosis. Transmitted through water/soil contaminated by urine of rodents, cattle, or dogs. IVRI maintains 21 serovars for diagnosis.')
b('• Clinical signs: fever; icterus (jaundice); haemoglobinuria (red urine); abortion in females; acute renal failure')
b('• Diagnosis: MAT (Microscopic Agglutination Test) — paired samples 2 weeks apart; 4-fold titre rise diagnostic')
b('• Latex Agglutination Test (LAT) for field screening; darkfield microscopy of urine; PCR on blood/urine')
b('• Treatment: Penicillin G (early); Doxycycline 5 mg/kg; supportive fluid therapy')
add_image_page(28, width_inches=5.5, caption_text='Fig 10.1 — Leptospirosis: transmission cycle, MAT serovars panel (IVRI, 21 serovars), Latex Agglutination Test')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11 — Parasites
# ═══════════════════════════════════════════════════════════════════════════════
h('11. Parasitic Diseases')
h('11.1 Helminth Parasites', 'CH3 Subsection')
add_table(
    ['Parasite', 'Type', 'Location', 'Significance'],
    [
        ['Fasciola jacksoni', 'Trematode (liver fluke)', 'Bile ducts / Liver', 'Fasciolosis: hepatomegaly; biliary fibrosis; Fasciola eggs in bile/faeces'],
        ['Pseudodiscus collinsi', 'Amphistome (rumen fluke)', 'Large intestine / Caecum', 'Heavy burdens → colitis; diarrhoea; flukes attached to mucosa at PM'],
        ['Strongylus spp.', 'Nematode', 'Anterior/posterior intestine', 'Colitis; protein loss; larval hepatic migration tracking'],
        ['Oxyuris (pinworm)', 'Nematode', 'Rectum', 'Tail rubbing; anal irritation; common in captive elephants'],
    ]
)
add_image_page(29, width_inches=5.5, caption_text='Fig 11.1 — Parasites: Pseudodiscus collinsi (amphistome), GI nematodes (Strongyle anterior/posterior), Fasciola jacksoni eggs and flukes')

h('11.2 Protozoal Parasites', 'CH3 Subsection')
b('• Balantidium coli/suis: large ciliated protozoan; causes yellow diarrhoea; cysts visible on microscopy')
b('• Treatment of Balantidiasis: Metronidazole 15–25 mg/kg BID for 5 days + Omeprazole')
b('• Haemoparasites: Trypanosoma spp. in blood smears; transmitted by biting flies; emaciation, anaemia')
b('• Treatment of haemoparasites: Diminazene aceturate')
add_image_page(30, width_inches=5.5, caption_text='Fig 11.2 — Protozoa: Balantidium cyst microscopy, yellow diarrhoea case, blood smear with haemoparasite, tick burden on tusker')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 12 — Surgical
# ═══════════════════════════════════════════════════════════════════════════════
h('12. Surgical and Non-Infectious Conditions')
b('• Sinus wound/abscess: debridement; irrigation with povidone-iodine; systemic antibiotics; surgical debridement under chemical restraint if needed (Etorphine / Medetomidine)')
b('• Corneal opacity: topical antibiotic + atropine; ophthalmoscopy under chemical restraint')
b('• Foot problems: overgrown nails, foot pad cracks, sole abscesses (caused by hard substrate, poor hygiene); trimming; foot soaks (copper sulphate/betadine); systemic antibiotics')
b('• Dystocia: controlled delivery under sedation; pre-position delivery equipment at breeding herds')
b('• Colic/Impaction: liquid paraffin per os; fluids; Buscopan; flank examination under sedation for severe cases')
add_image_page(31, width_inches=2.7, caption_text='Fig 12.1a — Sinus wound treatment: elephant Roopakali (Dudhwa NP)')
add_image_page(32, width_inches=2.7, caption_text='Fig 12.1b — Corneal opacity; overgrown foot nails; sole cracks in captive elephant')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 13 — Emerging Threats
# ═══════════════════════════════════════════════════════════════════════════════
h('13. Emerging Threats and Mass Mortality Events')
b('• Cyanobacteria/Algal bloom toxins: Botswana 2020 — 350 elephants died around waterholes; cyanobacterial toxins (nodularin/microcystin or BMAA) implicated; neurological signs before collapse')
b('• Mpox (Monkeypox): documented in captive elephants from Africa; vesicular skin lesions; zoonotic potential; keepers must use PPE')
b('• Novel RNA viruses: SARS-CoV-2 antibodies detected in captive elephants (Belgium); Paramyxoviruses; bat-origin pathogens')
b('• Climate change: shifting mosquito vectors; altered arbovirus range; increased heat stress mortality')
b('• Antibiotic resistance: mandatory sensitivity testing before treatment in elephants near human settlements')
add_image_page(33, width_inches=5.5, caption_text='Fig 13.1 — Botswana 2020: mass elephant mortality around waterhole (cyanobacteria / algal bloom toxins)')
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 14 — Field Practices
# ═══════════════════════════════════════════════════════════════════════════════
h('14. Field Practice Principles')
h('14.1 Antibiotic Use', 'CH3 Subsection')
b('• Culture-based treatment preferred; collect samples BEFORE starting antibiotics')
b('• Disk diffusion / Kirby-Bauer sensitivity testing at district labs')
b('• Document all drug use: drug name, dose, route, duration, outcome')

h('14.2 Documentation Protocol', 'CH3 Subsection')
b('• Photograph before touching: GPS location + scene + carcass position first')
b('• Video documentation: record gross PM findings continuously with voice narration')
b('• Systematic PM photography: each body cavity, organ, lesion with scale bar')
b('• Chain of custody: log each sample; signatures required at handover')
b('• Necropsy report: submit within 48 hours using standard DFO/CWL format')

h('14.3 Essential Field Kit', 'CH3 Subsection')
add_table(
    ['Category', 'Items'],
    [
        ['PPE', 'Nitrile gloves (×3 pairs), N95 mask, splash goggles, Tyvek suit, boot covers, biohazard waste bags'],
        ['Samples', 'EDTA tubes, plain tubes, formalin pots (10%), sterile swabs, viral transport media, bone marrow needle, labelled zip-lock bags'],
        ['Instruments', 'Scalpel (large handle + #22 blades), bone saw, forceps, scissors, ruler, weighing scale'],
        ['Diagnostics', 'Glass slides, Wright/Giemsa stain, Seller\'s stain, portable glucometer'],
        ['Communication', 'GPS unit, camera with macro lens, waterproof field notebook, contact list (IVRI, WW office, PCCF)'],
        ['Cold Chain', 'Ice packs, insulated cool box, cold chain labels'],
    ]
)
doc.add_page_break()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 15 — Conclusion
# ═══════════════════════════════════════════════════════════════════════════════
h('15. Conclusion and Key Take-Aways')
p('The field of elephant health medicine in India is rapidly evolving. This chapter has presented the major infectious, parasitic, and management-related diseases of Asian elephants with emphasis on field-relevant diagnostic and treatment protocols.')
add_table(
    ['#', 'Key Take-Away'],
    [
        ['1. EEHV', 'Highest priority for calves — pre-position famciclovir; early recognition saves lives'],
        ['2. Anthrax', 'Zero-necropsy protocol — burn all material; never bury'],
        ['3. TB', 'Chronic silent killer and two-way zoonotic risk — mandatory surveillance of elephants and handlers'],
        ['4. Rabies', 'Brain is the ONLY diagnostic sample; full PPE mandatory; PEP for exposed personnel'],
        ['5. HS / Clostridial', 'Bone marrow is gold-standard PM sample; collect before lysis'],
        ['6. Parasites', 'Regular faecal examination and strategic deworming — cornerstone of captive elephant health'],
        ['7. Documentation', 'Systematic photography, GPS recording and rapid lab submission are as important as clinical intervention'],
        ['8. Preparedness', 'Every camp/zoo must maintain: emergency drug kit (famciclovir, HS vaccine, anthrax vaccine, antibiotics), contact tree'],
    ]
)

h('Acknowledgements', 'CH3 Subsection')
b('• Resource Person: Dr. M. Karikalan, MVSc, PhD — Asst. Professor, Dept. of Wildlife Science, VBSC & AH, Namakkal')
b('• Institutions: CWL IVRI, Wildlife Institute of India (WII), Nandankanan ZP, MTR Nilgiris, ERRC Surajpur (CG), Dudhwa NP')
b('• Workshop organisers: Chhattisgarh Forest Department; Project Elephant, MoEF&CC; PCCF (Wildlife) CG State')
b('• Sponsors: Central Zoo Authority (CZA), MoEF&CC, Dr Parag Nigam (WII)')
add_image_page(34, width_inches=4.5, caption_text='Fig 15.1 — Acknowledgements page from the source presentation')


# ── Save ──────────────────────────────────────────────────────────────────────
out = '/home/user/Workshop-on-Conference/Workshop_Chapter3_Infectious_Diseases_2026.docx'
doc.save(out)
print(f'Word file written: {out} ({os.path.getsize(out)//1024} KB)')

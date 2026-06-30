#!/usr/bin/env python3
"""
Comprehensive notes from Prof. Dr. A B Shrivastava's presentation:
"Non-Infectious Pathology in Asian Elephants"
Outputs: ABS_Elephant_NonInfectious_Notes.docx  and  .pdf
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, Image as RLImage, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

DIR    = '/home/user/Workshop-on-Conference'
SLIDES = '/home/user/Workshop-on-Conference/abs2_slides'
OUT_D  = os.path.join(DIR, 'ABS_Elephant_NonInfectious_Notes.docx')
OUT_P  = os.path.join(DIR, 'ABS_Elephant_NonInfectious_Notes.pdf')

DARK  = RGBColor(0x1B, 0x43, 0x32); MED  = RGBColor(0x2D, 0x6A, 0x4F)
LIGHT = RGBColor(0x52, 0xB7, 0x88); TINT = RGBColor(0xD8, 0xF3, 0xDC)
TINT2 = RGBColor(0xEA, 0xF7, 0xEE); WHITE= RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1A, 0x1A, 0x1A); MUTED= RGBColor(0x55, 0x55, 0x55)
REDL  = RGBColor(0xFA, 0xE0, 0xD8); RED  = RGBColor(0x8B, 0x00, 0x00)

def rgb_hex(rgb): return f'{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}'
def slide(n): return os.path.join(SLIDES, f'page_{n:03d}.png')

# ── DOCX HELPERS ──────────────────────────────────────────────────────────────
def shade_cell(cell, hex_color):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color); tcPr.append(shd)

def page_break(doc):
    p = doc.add_paragraph(); run = p.add_run()
    br = OxmlElement('w:br'); br.set(qn('w:type'), 'page'); run._r.append(br)
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)

def sec1(doc, text):
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(13); run.font.bold = True; run.font.color.rgb = WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def sec2(doc, text):
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(MED))
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(10.5); run.font.bold = True; run.font.color.rgb = WHITE
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def sec3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(1)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(10); run.font.bold = True; run.font.color.rgb = MED

def para(doc, text, size=9.5, bold=False, italic=False, color=None,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4):
    p = doc.add_paragraph(); p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = 'Calibri'; run.font.size = Pt(size); run.font.bold = bold
    run.font.italic = italic; run.font.color.rgb = color or BLACK
    return p

def bullet(doc, text, level=0, size=9.5):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.5)
    p.paragraph_format.first_line_indent = Cm(-0.3)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(('◦  ' if level > 0 else '•  ') + text)
    run.font.name = 'Calibri'; run.font.size = Pt(size); run.font.color.rgb = BLACK

def img(doc, n, caption='', width_cm=15):
    path = slide(n)
    if os.path.exists(path):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(path, width=Cm(width_cm))
    if caption:
        cp = doc.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_after = Pt(6)
        cr = cp.add_run(caption); cr.font.name = 'Calibri'; cr.font.size = Pt(8)
        cr.font.italic = True; cr.font.color.rgb = MUTED

def keybox(doc, text, danger=False):
    bg = rgb_hex(REDL) if danger else rgb_hex(TINT); fg = RED if danger else DARK
    tbl = doc.add_table(rows=1, cols=1); tbl.style = 'Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, bg)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(5)
    run = p.add_run(text); run.font.name = 'Calibri'; run.font.size = Pt(9)
    run.font.bold = True; run.font.color.rgb = fg
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def dtable(doc, headers, rows, widths=None):
    n = len(headers)
    tbl = doc.add_table(rows=1 + len(rows), cols=n); tbl.style = 'Table Grid'
    for i, h in enumerate(headers):
        shade_cell(tbl.rows[0].cells[i], rgb_hex(MED))
        p = tbl.rows[0].cells[i].paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(str(h))
        run.font.name='Calibri'; run.font.size=Pt(8.5); run.font.bold=True; run.font.color.rgb=WHITE
    for ri, row in enumerate(rows):
        bg = rgb_hex(TINT2) if ri % 2 else 'FFFFFF'
        for ci, val in enumerate(row):
            shade_cell(tbl.rows[ri+1].cells[ci], bg)
            p = tbl.rows[ri+1].cells[ci].paragraphs[0]
            txt, bld = (val[0], val[1]) if isinstance(val, tuple) else (val, False)
            run = p.add_run(str(txt)); run.font.bold = bld
            run.font.name='Calibri'; run.font.size=Pt(8.5); run.font.color.rgb=BLACK
    if widths:
        for row in tbl.rows:
            for ci, cell in enumerate(row.cells):
                if ci < len(widths): cell.width = Cm(widths[ci])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ══════════════════════════════════════════════════════════════════════════════
def build_docx():
    doc = Document()
    s = doc.sections[0]
    s.page_width=Cm(21); s.page_height=Cm(29.7)
    s.left_margin=s.right_margin=Cm(2.0); s.top_margin=s.bottom_margin=Cm(1.8)
    doc.core_properties.title  = 'Non-Infectious Pathology in Asian Elephants — Prof. Dr. A B Shrivastava'
    doc.core_properties.author = 'Prof. Dr. A B Shrivastava, NDVSU Jabalpur'

    # TITLE BANNER
    tbl = doc.add_table(rows=1, cols=1); tbl.style='Table Grid'
    cell = tbl.rows[0].cells[0]; shade_cell(cell, rgb_hex(DARK))
    p = cell.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(20); p.paragraph_format.space_after=Pt(20)
    r0 = p.add_run('NON-INFECTIOUS DISEASE & TOXICOLOGY\n')
    r0.font.name='Calibri'; r0.font.size=Pt(9); r0.font.bold=True; r0.font.color.rgb=LIGHT
    r1 = p.add_run('Non-Infectious Pathology in Asian Elephants\n')
    r1.font.name='Calibri'; r1.font.size=Pt(18); r1.font.bold=True; r1.font.color.rgb=WHITE
    r2 = p.add_run('Comprehensive Study Notes with Slide Images\n')
    r2.font.name='Calibri'; r2.font.size=Pt(10); r2.font.color.rgb=TINT
    r3 = p.add_run('Prof. Dr. A B Shrivastava  ·  Founder Director, School of Wildlife Forensic and Health\n')
    r3.font.name='Calibri'; r3.font.size=Pt(10); r3.font.bold=True; r3.font.color.rgb=WHITE
    r4 = p.add_run('Nanaji Deshmukh Veterinary Science University, Jabalpur 482001, M.P.')
    r4.font.name='Calibri'; r4.font.size=Pt(9); r4.font.italic=True; r4.font.color.rgb=TINT
    doc.add_paragraph()

    keybox(doc,
        'Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  ·  Technical Support: WII Dehradun\n'
        'Lab Partners: ICAR-IVRI & NDVSU Jabalpur  ·  Notes elaborated with peer-reviewed literature')

    keybox(doc,
        'CONTENTS OF THIS DOCUMENT:\n'
        '  1. Introduction — Non-Infectious Pathology & Elephant Poisoning in India\n'
        '  2. Poisoning Statistics & Categories of Elephant Toxicity\n'
        '  3. Anthropogenic Poisons (Agrochemicals · Cyanide · Fertilizers & Heavy Metals)\n'
        '  4. Mycotoxins & Biological Toxins — Kodo Millet (CPA) · Cyanobacteria · Toxic Plants\n'
        '  5. HCN (Cyanide) Poisoning from Sorghum — Mechanism, Signs, Antidote, Prevention\n'
        '  6. Electrocution in Elephants\n'
        '  7. Pyometra\n'
        '  8. Hyperthermia & Heat Stress\n'
        '  9. Iron Deficiency Anaemia\n'
        '  10. References & Recommended Reading')
    img(doc, 1, 'Slide 1 — Title slide: Non-Infectious Pathology in Asian Elephants; Elephant Poisoning in India', 13)
    page_break(doc)

    # ─── SECTION 1: INTRODUCTION ──────────────────────────────────────────────
    sec1(doc, '1.  Introduction — Non-Infectious Pathology & Elephant Poisoning')

    sec2(doc, '1.1  Non-Infectious Disease in Elephants — Scope')
    para(doc,
        'Non-infectious pathology refers to disease and death NOT caused by transmissible pathogens '
        '(bacteria, viruses, fungi, parasites). In Asian elephants, non-infectious causes are '
        'overwhelmingly anthropogenic (human-caused) and represent the leading cause of unnatural '
        'elephant mortality in India. The major categories are poisoning (intentional and accidental), '
        'electrocution, metabolic/reproductive disorders (pyometra, hyperthermia), and nutritional '
        'deficiency (anaemia).')

    sec2(doc, '1.2  Elephant Poisoning in India — Overview')
    para(doc,
        'Poisoning is a severe threat to pachyderms. In India and across Africa, these incidents '
        'primarily stem from HUMAN-WILDLIFE CONFLICT and ILLEGAL POACHING. A "pachyderm" is a large, '
        'thick-skinned mammal — the term is most commonly used for elephants, rhinoceroses and '
        'hippopotamuses.')
    bullet(doc, 'Poisoning occurs INTENTIONALLY — via illegal poaching (for ivory/body parts) and human-elephant conflict retaliation (crop-raiding revenge)')
    bullet(doc, 'Poisoning also occurs ACCIDENTALLY — ingestion of agrochemicals, contaminated crops, toxic plants, or contaminated water')
    bullet(doc, 'In India, unnatural causes such as electrocution and poisoning claim HUNDREDS of elephant lives every year')
    bullet(doc, 'Elephants are BULK FORAGERS: their high daily food intake (150–300 kg) and water intake (100–200 L) make them highly susceptible to environmental toxins even at low concentrations')
    keybox(doc,
        'KEY CONCEPT: Non-infectious mortality in Indian elephants is largely PREVENTABLE. Unlike '
        'infectious disease, these deaths result from human activity — agrochemical misuse, illegal '
        'electric fencing, retaliatory poisoning, and habitat degradation. Mortality investigation '
        'that correctly identifies the cause is essential for legal action and prevention.')
    page_break(doc)

    # ─── SECTION 2: POISONING STATISTICS ──────────────────────────────────────
    sec1(doc, '2.  Poisoning Statistics & Categories of Toxicity')
    img(doc, 2, 'Slide 2 — Elephant poisoning deaths by state (1997–2005); three categories of toxicity', 13)

    sec2(doc, '2.1  Elephant Deaths by Poisoning Since 1997 (State-Wise)')
    para(doc, 'The following data documents elephant deaths attributed to poisoning across Indian states (Source: WTI Elephant Mortality Database):')
    dtable(doc,
        ['State', 'Years', 'Cases'],
        [('Assam','1997–2005','29'),
         ('Orissa','1997–2003','03'),
         ('West Bengal','1997–2004','03'),
         ('Arunachal Pradesh','1997–2005','02'),
         ('Jharkhand','2002–2003','02'),
         ('Karnataka','1997–2005','02'),
         ('Kerala','1997–2003','02'),
         ('Uttar Pradesh','1997–2004','02'),
         ('Uttaranchal','2001–2004','02'),
         ('Meghalaya','1997–2005','01'),
         ('Tamil Nadu','1997–2005','01'),
         ('TOTAL','1997–2005','49')],
        widths=[6, 5, 3])
    bullet(doc, 'Assam recorded the highest number of poisoning deaths (29 of 49 = 59%) — reflecting intense human-elephant conflict in tea-estate and agricultural landscapes')
    bullet(doc, 'Note: This dataset (1997–2005) represents DOCUMENTED cases only; actual figures are considered substantially higher due to under-reporting and undiagnosed deaths')

    sec2(doc, '2.2  Three Categories of Elephant Toxicity')
    para(doc, 'Elephant poisoning is often due to anthropogenic (human-caused) events and natural toxicities. Elephant toxicity primarily falls into three categories:')
    dtable(doc,
        ['Category', 'Description', 'Examples'],
        [('I. Agricultural / Plant Mycotoxins','Fungal toxins contaminating crops that elephants raid','Cyclopiazonic acid (CPA) on Kodo millet; aflatoxins'),
         ('II. Human-Wildlife Conflict Chemicals','Deliberately or accidentally deployed chemicals','Pesticides (organophosphates, carbamates), cyanide, urea'),
         ('III. Environmental Toxins','Naturally occurring toxins in environment','Cyanobacterial blooms (blue-green algae); toxic plants; heavy metals')],
        widths=[4.5, 6, 6.5])
    keybox(doc,
        'WHY ELEPHANTS ARE HIGHLY SUSCEPTIBLE: Elephants are BULK FORAGERS — they consume enormous '
        'quantities of vegetation (150–300 kg/day) and water (100–200 L/day). This high intake means '
        'that even toxins present at low environmental concentrations can be ingested in lethal total '
        'doses. Their hindgut fermentation also generates and releases toxins (e.g., HCN from cyanogenic '
        'glycosides) over an extended period.')

    sec2(doc, '2.3  National Mortality Data — Unnatural Causes (Lok Sabha, 2024)')
    para(doc,
        'Government data tabled in the Lok Sabha in July 2024 quantified elephant deaths from '
        'unnatural causes over a five-year period. These figures place poisoning in its proper '
        'context relative to the dominant unnatural killers — electrocution and train accidents:')
    dtable(doc,
        ['Unnatural Cause', 'Deaths (5 yrs)', 'Share', 'Worst-Affected States'],
        [('Electrocution','392','74.2%','Odisha 71, Assam 55, Karnataka 52, Tamil Nadu 49, Chhattisgarh 32, Jharkhand 30, Kerala 29'),
         ('Train accidents','73','13.8%','Assam 22, Odisha 16'),
         ('Poaching','50','9.5%','Odisha 17, Meghalaya 14, Tamil Nadu 10'),
         ('Poisoning','13','2.5%','Assam 10, Chhattisgarh 2, West Bengal 1'),
         ('TOTAL UNNATURAL','528','100%','All India')],
        widths=[3.5, 2, 1.5, 9.5])
    bullet(doc, 'ELECTROCUTION dominates — 392 of 528 (74%) of all unnatural elephant deaths; see Section 6')
    bullet(doc, 'POPULATION CONTEXT: The 2017 all-India synchronised census recorded 29,964 wild elephants — approximately 60% of the global wild Asian elephant population')
    bullet(doc, 'Chhattisgarh appears in the worst-affected list for both electrocution (32) and poisoning (2) — directly relevant to this training program')
    bullet(doc, 'NOTE: Ministry tallies are periodically revised; figures here reflect the July 2024 Lok Sabha reply (Source: Business Standard / The Week reporting of Lok Sabha Unstarred Question data)')
    page_break(doc)

    # ─── SECTION 3: ANTHROPOGENIC POISONS ─────────────────────────────────────
    sec1(doc, '3.  Anthropogenic Poisons')
    para(doc,
        'Human-elephant conflict may result in intentional or accidental poisonings. The principal '
        'anthropogenic poisons affecting elephants are agrochemicals, cyanide, and fertilizers/heavy metals.')

    sec2(doc, '3.1  Agrochemicals — Pesticides')
    bullet(doc, 'Elephants raiding crops/plantations consume dangerous levels of agrochemicals; pesticides are also used DELIBERATELY in baits (laced crops, fruit, salt) for retaliatory killing and poaching')
    bullet(doc, 'Most are deadly NEUROTOXINS: organophosphates (OPs) and carbamates; newer neonicotinoids also implicated')
    sec3(doc, 'Specific Compounds Implicated in Indian Wildlife Poisoning:')
    dtable(doc,
        ['Compound', 'Class', 'Toxicity / Notes'],
        [('Carbofuran ("Furadan")','Carbamate','Granular; widely available (esp. Kerala); a LEADING agent in deliberate wildlife baiting'),
         ('Monocrotophos','Organophosphate','Highly toxic — mammalian oral LD50 ~18–20 mg/kg; common in Indian poisonings; used on grain baits'),
         ('Aldicarb ("Temik")','Carbamate','One of the MOST acutely toxic carbamates; used in baiting'),
         ('Chlorpyrifos','Organophosphate','Less acutely toxic (LD50 ~500 mg/kg goats); cattle/exotic breeds notably susceptible'),
         ('Imidacloprid','Neonicotinoid','Systemic insecticide; implicated in death of a wild adult Asian elephant (Kerala)')],
        widths=[3.5, 2.5, 11])
    sec3(doc, 'OP vs Carbamate — Mechanism:')
    bullet(doc, 'BOTH inhibit acetylcholinesterase (AChE) → acetylcholine accumulates at muscarinic, nicotinic and CNS synapses', level=1)
    bullet(doc, 'OPs PHOSPHORYLATE AChE — binding becomes irreversible after "aging" (hours); carbamates CARBAMYLATE AChE reversibly — toxicity self-limiting (<24 h) if animal survives', level=1)
    sec3(doc, 'Clinical Signs — Cholinergic Toxidrome (DUMBELS):')
    bullet(doc, 'MUSCARINIC: Defecation, Urination, Miosis (pinpoint pupils), Bronchorrhoea/Bronchoconstriction, Emesis, Lacrimation, Salivation; bradycardia', level=1)
    bullet(doc, 'NICOTINIC: muscle fasciculations, tremors, weakness, flaccid paralysis', level=1)
    bullet(doc, 'CNS: depression, ataxia, seizures; DEATH from respiratory failure', level=1)
    sec3(doc, 'Diagnosis:')
    bullet(doc, 'Cholinesterase (ChE) activity in whole blood, BRAIN and retina — brain AChE depression to <50% of normal is DIAGNOSTIC', level=1)
    bullet(doc, 'Detect parent compound in stomach contents, liver, and bait material (GC-MS / LC-MS)', level=1)
    bullet(doc, 'CRITICAL: carbamate-inhibited ChE spontaneously reactivates — freeze samples FAST and analyse promptly to avoid false negatives', level=1)
    sec3(doc, 'Antidote Dosing (cattle/large-animal reference — extrapolate for elephant):')
    bullet(doc, 'ATROPINE: 0.6–1.0 mg/kg (cattle) — give ~⅓ IV, remainder IM/SC; repeat to effect ("atropinisation": pupil dilation, drying secretions, alertness)', level=1)
    bullet(doc, 'PRALIDOXIME (2-PAM): 20–50 mg/kg as 5% solution, slow IV (5–10 min) or IM — reactivates AChE; MUST be given EARLY (before aging); effective for OPs, generally not for carbamates', level=1)

    sec2(doc, '3.2  Cyanide')
    bullet(doc, 'Used in illegal poaching and mining operations — can cause rapid, fatal hypoxia (cellular asphyxiation)')
    bullet(doc, 'Poachers create "natural salt licks" laced with cyanide near waterholes — elephants attracted to salt are poisoned')
    bullet(doc, 'Mechanism: cyanide binds cytochrome c oxidase → blocks mitochondrial electron transport → cells cannot use oxygen → death')
    bullet(doc, 'See Section 5 for detailed HCN/cyanide poisoning from cyanogenic plants (sorghum)')

    sec2(doc, '3.3  Fertilizers / Heavy Metals')
    bullet(doc, 'Accidental UREA fertilizer toxicity: urea → ammonia in rumen/hindgut → ammonia toxicity → neurological signs, death')
    bullet(doc, 'Heavy metal contamination (ARSENIC, LEAD) can destroy gastrointestinal and renal integrity')
    sec3(doc, 'Heavy Metal Effects (web-elaborated):')
    bullet(doc, 'LEAD: damages nervous system (encephalopathy), GI tract (colic), kidneys; sources — paint, batteries, mining waste', level=1)
    bullet(doc, 'ARSENIC: damages GI mucosa (haemorrhagic enteritis), liver, kidneys; sources — pesticides, industrial effluent', level=1)
    bullet(doc, 'Chronic exposure: weight loss, anaemia, organ failure; Acute: severe GI haemorrhage, rapid death', level=1)
    keybox(doc,
        'TOXICOLOGY SAMPLING (Anthropogenic Poisons): Collect stomach/gut contents, liver, kidney, '
        'brain, and blood — refrigerate or freeze. For OP/carbamate: blood AChE level + gut contents. '
        'For heavy metals: liver and kidney (frozen) for atomic absorption spectroscopy. Always collect '
        'suspected bait/source material. Send to forensic laboratory (IVRI Izatnagar / State FSL) with '
        'a clear suspected-diagnosis note.')
    page_break(doc)

    # ─── SECTION 4: MYCOTOXINS ────────────────────────────────────────────────
    sec1(doc, '4.  Mycotoxins & Biological Toxins')
    img(doc, 3, 'Slide 3 — Mycotoxins (CPA / Kodo millet); cyanotoxins; toxic plants; Bandhavgarh Kodo case', 13)
    img(doc, 4, 'Slide 4 — Field photographs: Kodo millet crop raided; necropsy organ findings', 13)

    sec2(doc, '4.1  Crop-Borne Mycotoxins — Kodo Millet (Cyclopiazonic Acid)')
    para(doc,
        'Elephants raiding farm fields are highly susceptible to mycotoxins like Cyclopiazonic Acid '
        '(CPA). This fungal toxin often infects crops like Kodo millet (Paspalum scrobiculatum) and '
        'can cause acute vascular damage and liver/kidney necrosis.')
    bullet(doc, 'CPA is produced by fungi — primarily Aspergillus and Penicillium species')
    bullet(doc, 'Contamination occurs when heavy or unseasonal rainfall coincides with grain maturation/harvest, creating moist conditions favourable for fungal growth')
    bullet(doc, '"Kodo poisoning" / "Kodua poisoning" is a well-recognised syndrome in livestock and elephants in central India')

    sec2(doc, '4.2  CASE STUDY — Kodo Millet Poisoning, Bandhavgarh Tiger Reserve')
    keybox(doc,
        'RECENT CASE (Madhya Pradesh): A herd of 13 elephants raided the Kodo millet crops near '
        'Bandhavgarh Tiger Reserve. TEN ELEPHANTS DIED. Forensic postmortem and laboratory '
        'investigations revealed that the deaths were caused by accidental toxicity from eating crops '
        'infected with fungal mycotoxins (cyclopiazonic acid). Dr. Shrivastava notes: "I have seen / '
        'treated two cases in KTR (Kanha Tiger Reserve) during 1997–98."', danger=True)
    sec3(doc, 'What the Forensic Investigation Found (verified):')
    bullet(doc, 'Confirmed event: 10 wild elephants died over 3 days (29–31 October 2024) in Sankhani/Bakeli, Khitoli range, Bandhavgarh Tiger Reserve, Madhya Pradesh')
    bullet(doc, 'Samples (viscera, liver, kidney) sent to ICAR-IVRI Bareilly, WII Dehradun, MP State FSL Sagar, and CCMB Hyderabad')
    bullet(doc, 'IVRI toxicology report (5 Nov 2024): NO nitrates/nitrites, NO heavy metals, and NO pesticides (OP, organochlorine, pyrethroid, carbamate) detected')
    bullet(doc, 'CYCLOPIAZONIC ACID (CPA) was CONFIRMED in the viscera of all elephants → diagnosis: ingestion of large quantities of FUNGUS-INFECTED Kodo millet')
    bullet(doc, 'Key nuance: the FUNGUS (toxin) on the millet — not the millet grain itself — was the proximate cause ("fungus, not Kodo millet, responsible")')

    sec3(doc, 'CPA Mechanism & Pathology (web-elaborated):')
    bullet(doc, 'CPA is an indole-tetramic acid mycotoxin from Aspergillus flavus, A. tamarii and Penicillium spp. infesting Kodo millet')
    bullet(doc, 'Mechanism: potent inhibitor of Ca²⁺-dependent ATPases (SERCA) of the endo/sarcoplasmic reticulum → disrupts intracellular calcium gradients and the muscle contraction–relaxation cycle')
    bullet(doc, 'Effects: acute HEPATOTOXICITY, nephrotoxicity, and GI-tract effects; vascular damage; neurological signs (depression, loss of mobility)')
    bullet(doc, 'AFLATOXINS (related): Aspergillus flavus/parasiticus on grain — hepatotoxic/hepatocarcinogenic; hepatic necrosis, bile-duct proliferation, icterus, coagulopathy — a key differential in grain-associated die-offs')

    sec3(doc, 'Management of Kodo Millet Toxicity:')
    bullet(doc, 'Combination of preventive measures in cultivation, storage and processing')
    bullet(doc, 'Biocontrol agents — non-toxigenic fungal strains can competitively exclude toxigenic strains and reduce mycotoxin production')
    bullet(doc, 'Good agricultural practices and proper post-harvest handling: proper drying and airtight storage of Kodo grain')

    sec2(doc, '4.3  Cyanotoxins / Cyanobacteria (Blue-Green Algae)')
    bullet(doc, 'Toxic blue-green algae blooms in stagnant, seasonal water sources produce potent NEUROTOXINS and HEPATOTOXINS')
    bullet(doc, 'These have caused fatal die-offs; mass deaths occasionally linked to toxic algal blooms in watering holes')
    bullet(doc, 'Particularly common during HOT, DRY seasons when water sources shrink and concentrate nutrients')
    sec3(doc, 'Cyanotoxin Types (web-elaborated):')
    bullet(doc, 'MICROCYSTINS (hepatotoxins): produced by Microcystis — cause massive liver haemorrhage and necrosis', level=1)
    bullet(doc, 'ANATOXIN-a / SAXITOXINS (neurotoxins): cause rapid respiratory paralysis and death', level=1)
    bullet(doc, 'Note: The 2020 mass die-off of African elephants in Botswana (Okavango) was attributed to cyanobacterial neurotoxins in waterholes — a landmark example', level=1)

    sec2(doc, '4.4  Toxic Plants')
    bullet(doc, 'Elephants are generally ADEPT at avoiding toxic vegetation through learned behaviour and selective feeding')
    bullet(doc, 'However, ingestion of plants like OLEANDER (Nerium/Thevetia) or certain weeds can cause lethal cardiac or neurological effects')
    bullet(doc, 'Oleander contains cardiac glycosides (oleandrin) → cardiac arrhythmia, heart block, death — even small quantities lethal')
    bullet(doc, 'Some local toxic plants (those containing CALCIUM OXALATE crystals) cause localised severe irritation, swelling, and systemic distress if consumed in large quantities')
    page_break(doc)

    # ─── SECTION 5: HCN POISONING ─────────────────────────────────────────────
    sec1(doc, '5.  HCN (Cyanide) Poisoning from Sorghum')
    img(doc, 5, 'Slide 5 — HCN poisoning: mechanism, signs, risk factors, management & antidote', 13)
    img(doc, 6, 'Slide 6 — HCN poisoning case report (Zoo Print 2010, Dr. Shrivastava); Electrocution intro', 13)

    sec2(doc, '5.1  Overview & Mechanism')
    para(doc,
        'HCN (Hydrocyanic acid or prussic acid) poisoning in elephants occurs when they consume '
        'sorghum that is stressed (drought, frost, or trampling). Ingestion leads to RAPID CELLULAR '
        'ASPHYXIATION.')
    sec3(doc, 'The Mechanism:')
    bullet(doc, 'Sorghum species (Sorghum bicolor) contain a cyanogenic glucoside called DHURRIN')
    bullet(doc, 'When the plant is chewed or its cells are ruptured, plant enzymes (β-glucosidase) mix with dhurrin, releasing HYDROGEN CYANIDE')
    bullet(doc, 'The toxin is rapidly absorbed into the bloodstream and blocks cellular oxygen use (binds cytochrome c oxidase)')
    bullet(doc, 'Result: cells cannot use oxygen despite adequate blood oxygen → "histotoxic hypoxia" → forced anaerobic metabolism → profound LACTIC ACIDOSIS → death')
    bullet(doc, 'Approximate lethal dose (general mammalian): ~2–2.5 mg cyanide/kg body weight; onset within ~15–20 min')
    bullet(doc, 'CAUTION at necropsy: the classic cherry-red colour FADES rapidly after death and air exposure — it is SUGGESTIVE, not confirmatory; mucous membranes may turn cyanotic once respiration stops')

    sec2(doc, '5.2  Signs and Symptoms')
    bullet(doc, 'RAPID ONSET: Symptoms appear within minutes to a few hours of consumption')
    bullet(doc, 'BEHAVIOURAL CHANGES: Laboured and rapid breathing, staggering gait, muscle tremors, convulsions, recumbency, and sudden death')
    bullet(doc, 'PHYSICAL SIGNS: A distinct BITTER ALMOND smell; excessive salivation; and BRIGHT CHERRY-RED blood and mucous membranes')
    bullet(doc, 'IMPORTANT DISTINCTION: Cherry-red blood is characteristic of cyanide (oxygen remains bound to haemoglobin); contrast with NITRATE poisoning which causes BROWN (chocolate-coloured) blood from methaemoglobin')

    sec2(doc, '5.3  Risk Factors for Elephants')
    dtable(doc,
        ['Risk Factor', 'Detail'],
        [('Plant Height / Maturity','Young, dark green sorghum regrowth (usually <50 cm tall) holds the HIGHEST concentration of toxins'),
         ('Environmental Stress','Drought-stressed, wilted, or frost-damaged sorghum plants exhibit increased toxicity'),
         ('Digestive Process','Elephants are hindgut fermenters — large quantities of fresh, young, or stressed sorghum fodder quickly overwhelm their metabolic detoxification capacity')],
        widths=[4.5, 12.5])

    sec2(doc, '5.4  Management, Antidote & First Aid')
    sec3(doc, 'Immediate Management:')
    bullet(doc, 'REMOVE THE FOOD SOURCE: move the herd away from the sorghum field immediately')
    bullet(doc, 'ANTIDOTE THERAPY: administer specific cyanide antidote kit (Sodium Nitrite + Sodium Thiosulphate)')
    sec3(doc, 'Antidote & Treatment Protocol:')
    bullet(doc, 'SODIUM NITRITE: administered IV (e.g., 1 gm to 3 gm in 50 ml distilled water) — converts haemoglobin into methaemoglobin, which binds free cyanide to form cyanmethaemoglobin (drawing cyanide off cytochrome oxidase)')
    bullet(doc, 'SODIUM THIOSULPHATE: followed immediately by IV injection — converts cyanide into NON-TOXIC THIOCYANATE, which is safely excreted in urine')
    sec3(doc, 'Prevention:')
    bullet(doc, 'AVOID GRAZING/FEEDING YOUNG PLANTS: do not graze on sorghum less than 18–24 inches (45–60 cm) tall (or <7 weeks old) — concentrations are highest then')
    bullet(doc, 'WAIT AFTER WEATHER STRESS: avoid grazing immediately after a drought ends or a frost occurs — stress spikes the dhurrin content')
    bullet(doc, 'HAY vs PASTURE: Sorghum hay can be safer than fresh pasture (curing reduces HCN by roughly half) — but testing forage before feeding is highly advised')

    sec2(doc, '5.5  CASE STUDY — HCN Poisoning in Circus Elephants (Zoo Print, June 2010)')
    para(doc,
        'Documented by Dr. A B Shrivastava in "Management of Hydrocyanic Acid Poisoning in Asian '
        'Elephants" (Zoo Print vol. XXV, 6 June 2010):')
    bullet(doc, 'Five adult captive elephants were fed a large quantity of fresh Jowar (Sorghum) during their stay at a circus in Jabalpur — these elephants were not accustomed to Sorghum')
    bullet(doc, 'Signs: restlessness and diarrhoea; routine anti-diarrhoeal treatment failed; condition became serious')
    bullet(doc, 'One aged elephant became critical; immediate cessation of Jowar feeding; body temperature 97–98°F (subnormal)')
    bullet(doc, 'Treatment: 8–10 litres dextrose saline + 30 ml MVI via ear vein; Sodium thiosulphate 50 gm in water orally through drinking water, repeated after 12 hrs')
    bullet(doc, 'Aged elephant: given 3rd dose; cold dextrose saline 10 L + small pieces of ice + Tab. Diadin per rectum via tube')
    bullet(doc, 'Outcome: by the next morning the 5th (aged) elephant showed recovery — started drinking water and eating fresh green grass')
    bullet(doc, 'Reference: Radostits OM, Blood DC & Gay CC (1994). Veterinary Medicine, V edition. ELBS/Tindall')
    keybox(doc,
        'HCN TOXICOLOGY SAMPLING: Stomach contents (sealed, airtight, frozen — HCN is volatile and '
        'escapes); blood (10 mL fluoride-oxalate, frozen); liver and muscle (frozen); suspected plant '
        'material. Submit RAPIDLY to toxicology lab as cyanide degrades on storage. Note cherry-red '
        'tissue colour and bitter-almond odour at necropsy as supportive evidence.', danger=True)
    page_break(doc)

    # ─── SECTION 6: ELECTROCUTION ─────────────────────────────────────────────
    sec1(doc, '6.  Electrocution in Elephants')
    img(doc, 7, 'Slide 7 — Electrocution in an elephant (Nov 2020): field photographs and tusk removal', 13)
    img(doc, 9, 'Slide 9 — Electrocution case: carcass lifting, postmortem field photographs', 13)

    sec2(doc, '6.1  Definition & Mechanics')
    para(doc,
        'Electrocution is death or severe injury caused by an electric shock. It occurs when any '
        'individual becomes part of an electrical circuit. High levels of voltage and current disrupt '
        'the body\'s natural electrical systems, commonly triggering cardiac arrest or severe '
        'electrical burns.')
    dtable(doc,
        ['Term', 'Definition'],
        [('Electric Shock','A physical sensation or injury caused by electricity passing through the body (e.g., muscle spasms, minor burns). NON-FATAL injury'),
         ('Electrocution','An electric shock that is FATAL')],
        widths=[4, 13])

    sec2(doc, '6.2  Electrocution in Indian Elephants — Statistics')
    bullet(doc, 'Electrocution is the SINGLE LARGEST cause of unnatural elephant death in India')
    bullet(doc, 'Lok Sabha (July 2024): 392 of 528 unnatural deaths (74%) over 5 years were electrocution')
    bullet(doc, '2010–2020: electrocution killed 741 of 1,160 (≈64%) non-natural deaths; long-run share since 2009 ≈ 67%')
    bullet(doc, 'State-wise (2024 dataset): Odisha 71, Assam 55, Karnataka 52, Tamil Nadu 49, Chhattisgarh 32, Jharkhand 30, Kerala 29')
    bullet(doc, 'NOTE: headline 5-year figures (e.g., 348 in 2022 vs 392 in 2024) come from different reporting windows — do not sum across statements')

    sec2(doc, '6.3  Sources & Mechanisms')
    dtable(doc,
        ['Source', 'Description'],
        [('Illegal live-wire fences','Power illegally tapped ("hooking") from 11 kV HT or LT lines to electrify crop/home fences — the LEADING driver; deliberate, sometimes for poaching'),
         ('Sagging overhead lines','Low-hanging 11 kV lines (observed as low as ~1.5 m vs an ~3.3 m tall elephant) due to wide pole spacing, base erosion, waterlogging'),
         ('Solar-fence tampering','Bypassing the low-current pulsed energiser and connecting fence wire directly to mains — turns a legal, non-lethal deterrent into a lethal trap'),
         ('Accidental (legal lines)','Genuine accidental contact with sagging but legally installed transmission infrastructure in corridors')],
        widths=[4, 13])

    sec2(doc, '6.4  Postmortem / Necropsy Findings')
    bullet(doc, 'CURRENT MARK / ELECTRIC MARK (gross "gold standard"): crater-like skin elevation around a sunken pale centre at the contact point — trunk tip, feet, dorsum')
    bullet(doc, 'JOULE BURN: heat-generated burn — collagen denaturation + dermal oedema; singed hair; Grade III–IV burns, blistering, bone/muscle exposure')
    bullet(doc, 'METALLIZATION: microscopic conductor-metal particles deposited in skin at contact — reported in >50% of cases (detectable histochemically/SEM)')
    bullet(doc, 'HISTOPATHOLOGY: coagulative necrosis of epidermis; intra/sub-epidermal clefting; "NUCLEAR STREAMING" — elongation, palisading and hyperchromasia of basal epidermal nuclei aligned to current flow; dermal collagen homogenisation')
    bullet(doc, 'INTERNAL: generalised visceral congestion (brain, heart, lungs); pulmonary oedema; sub-epicardial/endocardial petechiae; myocardial necrosis; rhabdomyolysis; slow-clotting dark blood; bloody orifice discharge')
    bullet(doc, 'Dr. Shrivastava note: "Experience — charcoal powder" — charred contact tissue has a charcoal-like appearance')
    bullet(doc, 'CAVEAT: nuclear streaming and coagulative necrosis are NOT pathognomonic (also seen in flame/thermal burns); gross lesions may be ABSENT if contact area is wide or skin is wet — diagnosis leans on lesion + scene/circumstantial evidence')
    bullet(doc, 'Reference: Schulze C et al. (2016). Electrical Injuries in Animals: Causes, Pathogenesis, and Morphological Findings. Veterinary Pathology')

    sec2(doc, '6.5  Lightning Strike vs Man-Made Electrocution')
    dtable(doc,
        ['Feature', 'Lightning Strike', 'Man-Made Electrocution'],
        [('Skin marks','LICHTENBERG FIGURES — arborescent/fern-like pink-red "ferning" (pathognomonic); appear ~1 hr, fade 24–36 hr','DISCRETE deep contact/current burns at well-defined entry and exit'),
         ('Tissue damage','Superficial/transient — NOT true burns; minimal histology change','Focal DEEP charring; coagulative necrosis; metallization'),
         ('Number of animals','Often MULTIPLE animals down together','Usually single animal or a group along a wire line'),
         ('Scene','Open/exposed ground or under tall trees; split tree; storm history; scorched vegetation','Proximity to power line, hooked wire, or fence'),
         ('Entry/exit','Poorly defined','Well-defined (feet often = exit to ground)')],
        widths=[3, 7, 7])
    bullet(doc, 'NOTE: Lichtenberg figures are NOT burns — histology shows only subtle superficial dermal capillary dilatation, no deep damage; "magnetisation of nearby metal" is a low-confidence discriminator')

    sec2(doc, '6.6  Legal Framework')
    bullet(doc, 'WILDLIFE (PROTECTION) ACT 1972: elephant is Schedule I (highest protection); killing prosecuted under Section 51; often filed with IPC 429 and the Electricity Act')
    bullet(doc, 'ELECTRICITY ACT 2003: Section 161 (mandatory accident reporting & inquiry within ~24 hr); Section 135 (theft of electricity — illegal hooking); Section 146 (penalty for non-compliance)')
    bullet(doc, 'STRICT LIABILITY: NGT has held electricity utilities liable for elephant electrocution from their lines (e.g., CESU Odisha ordered to deposit ₹4 crore + maintain lines against sagging)')
    bullet(doc, 'GROUND CLEARANCE: MoEFCC 2010 committee recommended minimum 5.5 m clearance for ≤11 kV lines in vulnerable areas; Karnataka Elephant Task Force: 6.096 m (flat) / 9.144 m (sloping) terrain')
    bullet(doc, 'KARNATAKA HIGH COURT (26 Apr 2025, suo motu after elephant "Ashwathamma"): directed underground cabling in eco-sensitive zones; ban/replace illegal fences; AI/CCTV e-surveillance (Nagarahole pilot → statewide); enforce WPA & Electricity Act')
    keybox(doc,
        'ELECTROCUTION INVESTIGATION CHECKLIST:\n'
        '• Document the SCENE: photograph wires, poles, distance from carcass, sag height (measure!)\n'
        '• Locate and photograph ENTRY/EXIT current marks with scale bar; sample skin from burn margin\n'
        '• Histology: coagulative necrosis + nuclear streaming; look for metallization at contact point\n'
        '• Sample heart, lung (congestion/haemorrhage); document myocardial petechiae\n'
        '• RULE OUT lightning: search for Lichtenberg figures, multiple carcasses, storm evidence\n'
        '• Coordinate with electricity board / police — electrocution is punishable under WPA 1972 (Sec 51) + Electricity Act (Sec 135/161)\n'
        '• PREVENTION: convert illegal AC fences to legal pulsed SOLAR energisers (non-lethal short shock)', danger=True)
    page_break(doc)

    # ─── SECTION 7: PYOMETRA ──────────────────────────────────────────────────
    sec1(doc, '7.  Pyometra')
    img(doc, 8, 'Slide 8 — Pyometra in Asian elephants (clinical photograph; purulent vaginal discharge)', 13)
    img(doc, 10, 'Slide 10 — Vaginal vestibulotomy in Asian elephant: surgical management of pyometra', 13)

    sec2(doc, '7.1  Definition')
    para(doc,
        'Pyometra is a severe, life-threatening uterine infection characterised by the accumulation '
        'of PUS and severe inflammation in the uterus. It is most common in AGING, NULLIPAROUS '
        '(having never given birth) female elephants, and is often linked to prolonged hormonal '
        'fluctuations and underlying reproductive issues.')

    sec2(doc, '7.2  CEH–Pyometra Complex & Pathophysiology')
    bullet(doc, 'CYSTIC ENDOMETRIAL HYPERPLASIA (CEH) is the principal precursor lesion — present in ~67% of captive Asian elephants (vs 15% African) aged 26–57 yrs (Agnew, Munson & Ramsay, Vet Pathol 2004)')
    bullet(doc, 'CEH-pyometra complex (canine model): chronic progesterone (luteal) dominance → endometrial gland proliferation + cystic dilation → reduced uterine defence → fluid accumulation → bacterial colonisation → pyometra')
    bullet(doc, 'HORMONAL: CEH is "associated with prolonged phases of both estrogen and progesterone influence"; the long luteal phase (~6–12 weeks) maximises endometrial stimulation')
    bullet(doc, 'BACTERIAL: Escherichia coli (predominant), Streptococcus, Staphylococcus, Klebsiella, Proteus, Pseudomonas, Bacteroides — pure or mixed (largely extrapolated; elephant-specific culture series are sparse)')
    bullet(doc, 'CO-PATHOLOGY: Uterine LEIOMYOMAS are the most common reproductive tumour — more prevalent/larger in older nulliparous Asian elephants (reported 30–100%; one series 90% of neoplasia cases); ~13% uterine adenocarcinoma')

    sec2(doc, '7.3  Why Nulliparous Captive Females Are Predisposed')
    bullet(doc, 'ASYMMETRIC REPRODUCTIVE AGING (Hermes, Hildebrandt & Göritz 2004): prolonged non-reproductive periods + continuous endogenous steroid exposure → genital pathology, reduced fertility, eventual irreversible acyclicity (males not similarly affected)')
    bullet(doc, 'Repeated unbroken oestrous cycling (no pregnancy/lactation "rest") → cumulative unopposed progesterone/estrogen on the endometrium → CEH substrate')
    bullet(doc, 'Up to 14% of captive Asian (29% African) elephants are acyclic or cycle irregularly — a marker of this reproductive-health decline')

    sec2(doc, '7.4  Reproductive-Tract Anatomy — Why Drainage Is Hard')
    bullet(doc, 'The elephant has an EXCEPTIONALLY LONG vestibule (urogenital canal), ~1.0–1.4 m, opening between the hind legs')
    bullet(doc, 'A membranous HYMENAL constriction (orifice <2 cm) separates urogenital canal from vagina in nulliparous animals')
    bullet(doc, 'Total tract length (vulva-to-ovary) ranges 120–358 cm — this long, narrow, valved canal IMPEDES natural drainage and makes transcervical access very difficult, favouring closed-type pus accumulation')
    bullet(doc, 'ULTRASONOGRAPHY is the key diagnostic tool for endometrial cysts, CEH, leiomyoma, and intrauterine fluid/pyometra')

    sec2(doc, '7.5  Treatment')
    dtable(doc,
        ['Approach', 'Detail'],
        [('i. Hormonal Downregulation','GnRH vaccine (Improvac-type) → anti-GnRH antibodies block GnRH → ↓LH/FSH → suppress cyclicity & remove progesterone drive. Also Deslorelin (GnRH agonist) implants → pituitary down-regulation. EAZA: treat pyometra BEFORE GnRH vaccination'),
         ('ii. Aggressive Antibiotic Therapy','Broad-spectrum systemic antibiotics, ideally culture-guided'),
         ('iii. Uterine / Transcervical Lavage','Flushing the uterus with warm sterile saline to evacuate pus — constrained by the long urogenital canal/hymen'),
         ('iv. Prostaglandins (PGF2α)','Promote myometrial contraction & cervical relaxation to expel contents (minimally documented in elephants)'),
         ('v. Surgical Drainage','Vaginal vestibulotomy — surgical access through the long urogenital canal for lavage/drainage (slide 10)'),
         ('vi. Homeopathic (practised)','Pyrogenium 1000 + Hepar sulph 1000 + Secale 1000 (documented by Dr. Shrivastava)')],
        widths=[4.5, 12.5])
    bullet(doc, 'OVARIOHYSTERECTOMY is NOT practical in adult elephants — body size, vascularity, and extreme tract length (up to 358 cm) make it unfeasible; management is conservative/palliative')
    bullet(doc, 'PROGNOSIS: guarded to poor. Documented cases (deslorelin + antibiotics) showed short-term improvement but the animals later died (necropsy: enlarged uterus, leiomyoma). Advanced closed-cervix pyometra → uterine distension, rupture, peritonitis, sepsis, death')

    sec2(doc, '7.6  Luteal-Phase Caution & Prevention')
    bullet(doc, 'Elephant cycle: luteal (high-progesterone) phase ~6–12 weeks, follicular ~4–6 weeks; extended low-progesterone (>12 weeks) = acyclicity/"flatlining"')
    bullet(doc, 'Avoid GnRH-agonist implantation during the luteal (diestrus) phase — high progesterone increases pyometra risk')
    keybox(doc,
        'CLINICAL NOTE: Pyometra is a reproductive EMERGENCY in elephants. Toxins from the infected '
        'uterus (endotoxaemia) can cause septic shock and death. The long valved urogenital canal '
        'favours CLOSED-type pus accumulation and impairs drainage — raising mortality. In captive '
        'females, prevention centres on managed breeding or hormonal cycle suppression to break the '
        'CEH → pyometra cascade. Vaginal vestibulotomy provides surgical drainage when medical '
        'management fails; ovariohysterectomy is not feasible.')
    page_break(doc)

    # ─── SECTION 8: HYPERTHERMIA ──────────────────────────────────────────────
    sec1(doc, '8.  Hyperthermia & Heat Stress')

    sec2(doc, '8.1  Definition')
    para(doc,
        'Hyperthermia is a life-threatening condition caused by high environmental temperature, a '
        'lack of access to water or shade, massive body size, and lack of sweat glands. It is a '
        'serious welfare and mortality concern for both working/captive and free-ranging elephants '
        'during Indian summers.')

    para(doc,
        'Normal elephant core body temperature is comparatively LOW (~36.2 ± 0.5°C; working range ≈ 35.9–37°C) '
        'and they do NOT pant or sweat conventionally — making heat dissipation, not heat generation, the '
        'physiological challenge.', size=9.5, space_after=4)

    sec2(doc, '8.2  Why Elephants Are Prone to Overheating')
    bullet(doc, 'THE SQUARE-CUBE LAW: surface area scales as the square while volume/mass scales as the cube — so giants have proportionally little skin to dump metabolic heat. Heat dissipation problems set in above ~35°C ambient')
    bullet(doc, 'COMPENSATION: elephants\' thermal conductance is 3–5× higher than predicted allometrically, attributed to their lack of fur (offsets the low surface-area:volume disadvantage)')
    bullet(doc, 'HEAT STORAGE: during exercise in full sun (8–34.5°C ambient), 56–100% of active metabolic heat is STORED in core tissues and dumped later (often at night) — elephants "ride out" heat')
    bullet(doc, 'METABOLIC HEAT: continuous walking in hot sun without rest/water generates heat faster than it can be lost; modelling suggests arterial blood can rise ~5°C to potentially lethal levels after ~15 min locomotion at 26°C ambient')

    sec2(doc, '8.2b  The Sweat-Gland Question — Precise Science')
    bullet(doc, 'The claim "elephants have no sweat glands" is an OVERSIMPLIFICATION — they lack dense, body-wide conventional sweat glands, but specialised glands and high cutaneous water loss DO exist')
    bullet(doc, 'INTERDIGITAL GLANDS resembling human eccrine sweat glands occur between the toes/toenail cuticles of the Asian elephant — true sweat-gland tissue, but restricted to the feet (minimal thermoregulatory role)')
    bullet(doc, 'Elephants show very high CUTANEOUS EVAPORATIVE WATER LOSS (CEWL): 0.31–8.9 g·min⁻¹·m⁻² (Asian) — water diffuses through the bare skin itself, not via glands (Dunkin et al. 2013)')
    bullet(doc, 'SKIN MICRO-CRACKS: African elephant skin fractures into millions of true micro-channels that retain 5–10× more water/mud than a flat surface, prolonging evaporative cooling (Martins et al. 2018, Nature Comms)')

    sec2(doc, '8.3  Natural Cooling Mechanisms')
    dtable(doc,
        ['Mechanism', 'How It Works'],
        [('The Ears (thermal windows)','Large, thin, highly vascularised pinnae. Elephants vasodilate/"flood" the ears with blood, then flap to create convective + evaporative cooling; cooled blood returns to core. Up to ~100% of an African elephant\'s heat-loss need can be met by the pinnae (Phillips & Heath 1992)'),
         ('Wallowing & Spraying','Bathing in mud/water + trunk-spraying water = PRIMARY evaporative cooling. Water evaporation cools; residual mud blocks solar radiation and prolongs water retention'),
         ('Cutaneous Water Loss','Water diffuses through the bare skin itself; skin micro-channels hold applied water/mud. At 29–32°C ambient, evaporative cooling becomes the ONLY remaining avenue'),
         ('Body-wide thermal windows','Discrete hot vascular patches appear across the whole body surface (not just ears) as ambient temperature rises (Weissenböck et al. 2010)')],
        widths=[4, 13])

    sec2(doc, '8.4  How Heat Stress Kills (Pathophysiology)')
    bullet(doc, 'HEAT STROKE = core temperature >40°C plus CNS dysfunction, progressing to multi-organ failure')
    bullet(doc, 'Cascade: excess heat → protein denaturation, mitochondrial dysfunction, oxidative stress, release of DAMPs → systemic inflammatory response')
    bullet(doc, 'ENDOTHELIAL barrier disruption (unifying lesion) → vascular leak, oedema, microthrombi → impaired perfusion → ischaemic organ injury')
    bullet(doc, 'DIC (disseminated intravascular coagulation) reported in ~48% of severe heat-stroke cases — strongly linked to multi-organ dysfunction and death')
    bullet(doc, 'Organ-specific: liver (coagulopathy), kidney (rhabdomyolysis → AKI), heart (arrhythmia → circulatory collapse, irreversible shock)')

    sec2(doc, '8.5  Recent Heat-Wave Deaths in India')
    bullet(doc, 'April 2022, Karnataka: two ~15-yr-old elephants died within a week near Cauvery Wildlife Sanctuary — one of heat stroke (Chikkalahalli), one of suspected dehydration (Satnur range), amid drought + extreme heat')
    bullet(doc, 'Heat stroke is documented as a cause of death in captive juvenile elephants forced to work in heat without adequate water/shade')
    bullet(doc, '2024 Kerala: record summer heat reported to make captive temple elephants stressed and more aggressive — a heat-attributable welfare crisis')
    bullet(doc, 'CAUTION: not all elephant deaths in hot months are heat-related — Odisha\'s 106 elephant deaths in 2024–25 were largely electrocution, not heat')

    sec2(doc, '8.6  Prevention & Management')
    bullet(doc, 'Ensure constant access to SHADE and clean DRINKING WATER, especially 11 AM – 4 PM')
    bullet(doc, 'Provide wallowing pools / mud baths for captive elephants')
    bullet(doc, 'Avoid working/walking elephants during peak heat; reschedule to early morning or evening')
    bullet(doc, 'Recognise heat-stress signs: rapid breathing, intensified ear-flapping, lethargy, reluctance to move, collapse')
    bullet(doc, 'Emergency cooling: continuous water spraying (especially ears, head), move to shade, IV fluids')
    page_break(doc)

    # ─── SECTION 9: IRON DEFICIENCY ANAEMIA ───────────────────────────────────
    sec1(doc, '9.  Iron Deficiency Anaemia')
    img(doc, 11, 'Slide 11 — Iron Deficiency Anaemia: blood smear showing microcytic hypochromic target cells', 13)

    sec2(doc, '9.1  Definition')
    para(doc,
        'Anaemia is a qualitative and quantitative reduction in the quality (and oxygen-carrying '
        'capacity) of the blood. Iron deficiency anaemia results from inadequate iron for haemoglobin '
        'synthesis, producing characteristic microcytic, hypochromic red blood cells.')

    sec2(doc, '9.2  Clinical Signs Observed')
    bullet(doc, 'Pale mucous membranes (conjunctiva, oral mucosa)')
    bullet(doc, 'Extreme weakness; unable to walk; very slow walk and reduced activity')
    bullet(doc, 'Lethargy, exercise intolerance, reduced work capacity in captive elephants')

    sec2(doc, '9.3  Normal Haematology Reference Values (Indian Elephants)')
    para(doc, 'Reference intervals for Indian elephants (Elephas maximus indicus) under human care (Frontiers Vet Sci 2025; PMC12301552). Note: elephant RBCs are LARGE (high MCV) and relatively few in number:', size=9.5, space_after=3)
    dtable(doc,
        ['Parameter', 'Reference Interval', 'Note'],
        [('Haemoglobin (Hb)','8.62–16.78 g/dL','Low Hb confirms anaemia'),
         ('PCV / Haematocrit','21.73–49.25 %','Packed cell volume'),
         ('RBC count','1.77–4.9 ×10⁶/µL','Relatively LOW count (large cells)'),
         ('MCV','112.49–131.39 fL','HIGH — elephant RBCs are large'),
         ('MCH','39.3–62.39 pg','Mean cell haemoglobin'),
         ('MCHC','33.40–41.0 g/dL','Mean cell Hb concentration'),
         ('WBC (TLC)','9,912–29,475 cells/µL','Total leucocyte count'),
         ('Platelets','171.6–947.1 ×10³/µL','—')],
        widths=[4, 5, 8])
    bullet(doc, 'DISTINCTIVE MORPHOLOGY: elephants (Afrotheria) have HETEROPHILS instead of neutrophils, and a unique MONOCYTE with a bilobed/trilobed nucleus (peroxidase-positive); MONOCYTES are the most abundant leucocyte in healthy elephants')
    bullet(doc, 'Automated analysers are INACCURATE for elephant blood — a manual Wright/Giemsa differential is preferred')

    sec2(doc, '9.4  Diagnosis')
    bullet(doc, 'BLOOD EXAMINATION: Low Haemoglobin (Hb) below the reference interval')
    bullet(doc, 'BLOOD SMEAR: target cells (codocytes), hypochromia, microcytosis, anisocytosis (microcytic-hypochromic pattern supports iron deficiency by general veterinary principle)')
    bullet(doc, 'IRON PANEL: serum iron, ferritin, TIBC, transferrin saturation (low iron + high TIBC + low ferritin = deficiency); hepcidin in research settings')
    bullet(doc, 'PARASITOLOGY: faecal egg counts to identify blood-feeding helminths (see 9.2)')

    sec2(doc, '9.5  Causes of Anaemia in Elephants')
    bullet(doc, 'GI STRONGYLE NEMATODES (Murshidia, Quilonia, Bathmostomum, Equinurbia) → protein-losing gastroenteropathy → hypoalbuminaemia + anaemia')
    bullet(doc, 'HOOKWORMS: Bathmostomum sangeri (caecum/colon) and Grammocephalus hybridatus (bile duct/liver) — blood-feeders causing anaemia, weakness, hepatic insufficiency')
    bullet(doc, 'LIVER FLUKE Fasciola (Fascioloides) jacksoni — prevalence 18–62% in the Indomalayan region; causes anaemia + hypoproteinaemia, hepatic congestion/fibrosis')
    bullet(doc, 'NUTRITIONAL: iron, copper, cobalt deficiency (copper is needed for iron mobilisation); captive diets often deficient')
    bullet(doc, 'ANAEMIA OF CHRONIC DISEASE: especially chronic M. tuberculosis (iron-sequestration); EEHV in calves causes acute anaemia + thrombocytopenia')
    keybox(doc,
        'IRON OVERLOAD CAUTION: Iron storage disease (haemochromatosis-type) is a recognised problem '
        'in captive elephants from excess dietary iron. Crucially, blind iron supplementation can '
        'REACTIVATE latent infections such as M. tuberculosis (iron feeds the pathogen). Confirm true '
        'iron-deficiency with an iron panel BEFORE supplementing — do not supplement reflexively. '
        'Adult forage requirement: Cu 10, Fe 50, Co 0.1 mg/kg.', danger=True)

    sec2(doc, '9.6  Treatment')
    sec3(doc, '1. Diet Change — to full normal elephant diet:')
    bullet(doc, 'Soybeans, horse gram, Napier grass, bamboo, leaves, grains, fruits', level=1)
    sec3(doc, '2. Supplementation:')
    bullet(doc, 'IRON SUPPLEMENTS: Jaggery (gur), honey — traditional iron-rich supplements', level=1)
    bullet(doc, 'VITAMIN B12 INJECTIONS: supports erythropoiesis (red blood cell production)', level=1)
    bullet(doc, 'MULTIVITAMINS, Mineral mixture (M mixture)', level=1)
    keybox(doc,
        'INVESTIGATION NOTE: Iron deficiency anaemia in elephants is often SECONDARY — investigate '
        'the underlying cause: chronic blood loss (haematophagous parasites — ticks, lice, GI '
        'helminths such as Bathmostomum), nutritional inadequacy, or chronic disease. Treating only '
        'the anaemia without addressing the cause leads to relapse. Always run a parasitological '
        'examination (faecal egg count, ectoparasite check) alongside iron supplementation.')
    page_break(doc)

    # ─── SECTION 10: REFERENCES ───────────────────────────────────────────────
    sec1(doc, '10.  References & Recommended Reading')

    sec2(doc, '10.1  Works by Prof. Dr. A B Shrivastava')
    bullet(doc, 'Shrivastav AB (2010). Management of Hydrocyanic Acid Poisoning in Asian Elephants. Zoo Print vol. XXV, 6 June 2010')
    bullet(doc, 'Shrivastav AB & Sharma RK (2008). A Manual of Wildlife Health Management in Protected Areas. CVAH, JNKVV, Jabalpur')
    bullet(doc, 'Nigam P, Habib J & Pandey H (Ed.) (2021). Caring for Elephants: Managing Health & Welfare in Captivity')
    bullet(doc, 'MoEFCC/WII (2020). Necropsy and Carcass Disposal of Asian Elephant: Recommended Operating Procedure')

    sec2(doc, '10.2  Peer-Reviewed & Reference Literature')
    bullet(doc, 'Radostits OM, Blood DC & Gay CC (1994/2007). Veterinary Medicine: A Textbook of the Diseases of Cattle, Sheep, Pigs, Goats and Horses. ELBS/Tindall')
    bullet(doc, 'Fowler ME & Mikota SK (2006). Biology, Medicine and Surgery of Elephants. Blackwell, Iowa')
    bullet(doc, 'WTI (Wildlife Trust of India). Elephant Mortality Database — poisoning records 1997–2005')
    bullet(doc, 'Bengis RG et al. (2004). The role of wildlife in emerging and re-emerging zoonoses. Rev Sci Tech OIE')
    bullet(doc, 'Wang DZ (2008). Neurotoxins from marine and freshwater algae. Marine Drugs 6(2): 349–371')
    bullet(doc, 'Reference intervals for haematology & biochemistry in Indian elephants (Elephas maximus indicus) under human care (2025). Frontiers in Veterinary Science 12: 1602296 (PMC12301552)')
    bullet(doc, 'Schulze C, Peters M, Baumgärtner W, Wohlsein P (2016). Electrical Injuries in Animals: Causes, Pathogenesis, and Morphological Findings. Veterinary Pathology 53(5): 1018–1037')
    bullet(doc, 'Agnew DW, Munson L, Ramsay EC (2004). Cystic Endometrial Hyperplasia in Elephants. Veterinary Pathology 41(2): 179–183')
    bullet(doc, 'Hermes R, Hildebrandt TB, Göritz F (2004). Asymmetric reproductive aging in long-term captivity. Animal Reproduction Science 82–83: 49–60')
    bullet(doc, 'Landolfi JA et al. (2021). Reproductive Tract Neoplasia in Adult Female Asian Elephants. Veterinary Pathology 58(6)')
    bullet(doc, 'Dunkin RC et al. (2013). Climate influences thermal balance and water use in elephants. Journal of Experimental Biology 216: 2939–2952')
    bullet(doc, 'Martins AF et al. (2018). Bending cracks in African elephant skin. Nature Communications 9: 3865')
    bullet(doc, 'Rowe MF et al. (2013). Heat storage in Asian elephants during submaximal exercise. J Exp Biology 216: 1774–1785')
    bullet(doc, 'Mahato G et al. (2021). Heavy metal toxicosis in wild and captive elephants — review. Indian Journal of Veterinary Pathology')
    bullet(doc, 'Lok Sabha Unstarred Question reply (July 2024). Elephant deaths from unnatural causes 2019–2024. MoEFCC, Government of India')
    bullet(doc, 'Karnataka High Court (2025). Suo Motu W.P. on elephant electrocution ("Ashwathamma" case) — power-line management directions')
    bullet(doc, 'Project Elephant, MoEFCC (2017). Gajah: Securing the Future for Elephants in India')

    para(doc,
        'Notes prepared from the presentation of Prof. Dr. A B Shrivastava (06-06-2026), elaborated '
        'with peer-reviewed literature and current guidelines. Training Program: Essentials for '
        'Mortality Investigation of Asian Elephant, Chhattisgarh Forest Department, 5–6 June 2026, Raigarh.',
        size=8, italic=True, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER)

    doc.save(OUT_D)
    print(f'  ✓  {OUT_D}  ({os.path.getsize(OUT_D)//1024} KB)')


# ══════════════════════════════════════════════════════════════════════════════
#  BUILD PDF
# ══════════════════════════════════════════════════════════════════════════════
def build_pdf():
    W, H = A4
    doc = SimpleDocTemplate(OUT_P, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.8*cm, bottomMargin=1.8*cm)
    styles = getSampleStyleSheet(); story = []
    DK = colors.HexColor('#1B4332'); MD = colors.HexColor('#2D6A4F')
    LT = colors.HexColor('#52B788'); TN = colors.HexColor('#D8F3DC')
    T2 = colors.HexColor('#EAF7EE'); RD = colors.HexColor('#FAE0D8')
    WH = colors.white; MT = colors.HexColor('#555555'); DRD = colors.HexColor('#8B0000')

    def ST(name, **kw):
        s = ParagraphStyle(name, parent=styles['Normal'])
        for k, v in kw.items(): setattr(s, k, v)
        return s
    sH1 = ST('H1', fontSize=12, textColor=WH, leading=16, fontName='Helvetica-Bold')
    sH2 = ST('H2', fontSize=10, textColor=WH, leading=13, fontName='Helvetica-Bold')
    sH3 = ST('H3', fontSize=9.5, textColor=MD, leading=13, fontName='Helvetica-Bold', spaceAfter=2)
    sBD = ST('BD', fontSize=9, leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
    sBL = ST('BL', fontSize=9, leading=13, leftIndent=12, firstLineIndent=-9, spaceAfter=2)
    sBL2= ST('B2', fontSize=8.5, leading=12, leftIndent=24, firstLineIndent=-9, spaceAfter=1)
    sCAP= ST('CP', fontSize=7.5, textColor=MT, leading=10, alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=4)
    sKY = ST('KY', fontSize=8.5, textColor=DK, leading=12, fontName='Helvetica-Bold')
    sKYR= ST('KR', fontSize=8.5, textColor=DRD, leading=12, fontName='Helvetica-Bold')
    sFT = ST('FT', fontSize=7.5, textColor=MT, alignment=TA_CENTER, fontName='Helvetica-Oblique')
    sTD = ST('TD', fontSize=8, leading=11, spaceAfter=1)
    sTH = ST('TH', fontSize=8, leading=11, textColor=WH, fontName='Helvetica-Bold')
    sTIT= ST('TT', fontSize=17, textColor=WH, leading=23, fontName='Helvetica-Bold', alignment=TA_CENTER)
    sSUB= ST('SB', fontSize=10, textColor=LT, leading=14, fontName='Helvetica-Oblique', alignment=TA_CENTER)
    sSB2= ST('SC', fontSize=9, textColor=WH, leading=12, fontName='Helvetica-Bold', alignment=TA_CENTER)
    CW = W - 4*cm

    def h1(txt):
        story.append(Spacer(1, 0.2*cm))
        t = Table([[Paragraph(txt, sH1)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),('TOPPADDING',(0,0),(-1,-1),7),
                               ('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),8)]))
        story.append(t); story.append(Spacer(1, 0.12*cm))
    def h2(txt):
        story.append(Spacer(1, 0.1*cm))
        t = Table([[Paragraph(txt, sH2)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),MD),('TOPPADDING',(0,0),(-1,-1),3),
                               ('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),6)]))
        story.append(t); story.append(Spacer(1, 0.08*cm))
    def h3(txt): story.append(Paragraph(txt, sH3))
    def pb(txt, sub=False):
        prefix = '    ◦  ' if sub else '•  '
        story.append(Paragraph(prefix + txt, sBL2 if sub else sBL))
    def bdy(txt): story.append(Paragraph(txt, sBD))
    def kyb(txt, danger=False):
        ks = sKYR if danger else sKY; bg = RD if danger else TN
        t = Table([[Paragraph(txt, ks)]], colWidths=[CW])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('TOPPADDING',(0,0),(-1,-1),5),
                               ('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),8),
                               ('BOX',(0,0),(-1,-1),0.5,MD)]))
        story.append(t); story.append(Spacer(1, 0.1*cm))
    def pi(n, cap='', w=13):
        path = slide(n)
        if os.path.exists(path):
            story.append(Spacer(1, 0.15*cm))
            ri = RLImage(path, width=w*cm, height=w*cm*0.78); ri.hAlign = 'CENTER'
            story.append(ri)
            if cap: story.append(Paragraph(cap, sCAP))
            story.append(Spacer(1, 0.1*cm))
    def dtbl(hdrs, rows, wds=None):
        n = len(hdrs)
        if not wds: wds = [17/n]*n
        data = [[Paragraph(str(h), sTH) for h in hdrs]]
        for row in rows:
            data.append([Paragraph(str(v[0] if isinstance(v, tuple) else v), sTD) for v in row])
        t = Table(data, colWidths=[w*cm for w in wds])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),MD),('ROWBACKGROUNDS',(0,1),(-1,-1),[WH,T2]),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#BBBBBB')),('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),4),('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(t); story.append(Spacer(1, 0.15*cm))
    def hr(): story.append(HRFlowable(width='100%', thickness=0.5, color=LT, spaceAfter=4))

    # TITLE
    tb = Table([[Paragraph('NON-INFECTIOUS DISEASE & TOXICOLOGY', sSB2)],
                [Paragraph('Non-Infectious Pathology in Asian Elephants', sTIT)],
                [Paragraph('Comprehensive Study Notes with Slide Images', sSUB)],
                [Paragraph('Prof. Dr. A B Shrivastava  ·  School of Wildlife Forensic and Health', sSUB)],
                [Paragraph('Nanaji Deshmukh Veterinary Science University, Jabalpur 482001, M.P.', sSUB)]],
               colWidths=[CW])
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),DK),('TOPPADDING',(0,0),(-1,-1),12),
                            ('BOTTOMPADDING',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),12)]))
    story.append(Spacer(1, 0.3*cm)); story.append(tb); story.append(Spacer(1, 0.25*cm))
    kyb('Training Program: Essentials for Mortality Investigation of Asian Elephant\n'
        'Chhattisgarh Forest Department  ·  5–6 June 2026, Raigarh  ·  Technical Support: WII Dehradun')
    kyb('CONTENTS: 1 Intro  |  2 Poisoning Stats  |  3 Anthropogenic Poisons  |  4 Mycotoxins  |  '
        '5 HCN/Cyanide  |  6 Electrocution  |  7 Pyometra  |  8 Hyperthermia  |  9 Anaemia  |  10 References')
    pi(1, 'Slide 1 — Title slide; Elephant Poisoning in India introduction', 12)
    story.append(PageBreak())

    # S1
    h1('1.  Introduction — Non-Infectious Pathology & Elephant Poisoning')
    h2('1.1  Scope')
    bdy('Non-infectious pathology = disease/death NOT caused by transmissible pathogens. In Asian elephants these causes are overwhelmingly ANTHROPOGENIC and are the leading cause of unnatural elephant mortality in India: poisoning, electrocution, metabolic/reproductive disorders, and nutritional deficiency.')
    h2('1.2  Elephant Poisoning in India')
    bdy('Poisoning is a severe threat to pachyderms. Incidents primarily stem from HUMAN-WILDLIFE CONFLICT and ILLEGAL POACHING — intentionally (poaching, retaliation) or accidentally (agrochemicals, contaminated crops/water).')
    pb('Elephants are BULK FORAGERS — 150–300 kg food + 100–200 L water/day → highly susceptible to environmental toxins')
    pb('Unnatural causes (electrocution, poisoning) claim hundreds of elephant lives yearly in India')
    kyb('KEY: Non-infectious elephant mortality is largely PREVENTABLE — it results from human activity. Correct cause-of-death identification is essential for legal action and prevention.')
    story.append(PageBreak())

    # S2
    h1('2.  Poisoning Statistics & Categories of Toxicity')
    pi(2, 'Slide 2 — State-wise poisoning deaths (1997–2005, total 49); three categories of toxicity', 12)
    h2('2.1  Elephant Deaths by Poisoning, State-Wise (WTI Database)')
    dtbl(['State','Years','Cases'],
         [('Assam','1997–2005','29'),('Orissa','1997–2003','03'),('West Bengal','1997–2004','03'),
          ('Arunachal Pradesh','1997–2005','02'),('Jharkhand','2002–2003','02'),('Karnataka','1997–2005','02'),
          ('Kerala','1997–2003','02'),('Uttar Pradesh','1997–2004','02'),('Uttaranchal','2001–2004','02'),
          ('Meghalaya','1997–2005','01'),('Tamil Nadu','1997–2005','01'),('TOTAL','1997–2005','49')],
         wds=[7,6,4])
    pb('Assam = 29/49 (59%) — intense human-elephant conflict in tea-estate/agricultural landscapes')
    pb('Documented cases only — actual figures considered substantially higher (under-reporting)')
    h2('2.2  Three Categories of Elephant Toxicity')
    dtbl(['Category','Description','Examples'],
         [('I. Agricultural / Plant Mycotoxins','Fungal toxins on raided crops','Cyclopiazonic acid (CPA) on Kodo millet; aflatoxins'),
          ('II. Human-Wildlife Conflict Chemicals','Deliberate/accidental chemicals','Pesticides (organophosphates), cyanide, urea'),
          ('III. Environmental Toxins','Naturally occurring toxins','Cyanobacteria (blue-green algae); toxic plants; heavy metals')],
         wds=[4.5,6,6.5])
    kyb('SUSCEPTIBILITY: Bulk foraging (150–300 kg/day) means even low-concentration toxins reach lethal total doses. Hindgut fermentation also releases toxins (e.g. HCN) over an extended period.')
    h2('2.3  National Mortality Data — Unnatural Causes (Lok Sabha, 2024)')
    dtbl(['Unnatural Cause','Deaths (5 yr)','Share','Worst States'],
         [('Electrocution','392','74.2%','Odisha 71, Assam 55, Karnataka 52, TN 49, Chhattisgarh 32'),
          ('Train accidents','73','13.8%','Assam 22, Odisha 16'),
          ('Poaching','50','9.5%','Odisha 17, Meghalaya 14, TN 10'),
          ('Poisoning','13','2.5%','Assam 10, Chhattisgarh 2, WB 1'),
          ('TOTAL','528','100%','All India')],
         wds=[3.5,2.2,1.8,9])
    pb('Electrocution dominates (74%); poisoning is 2.5% of unnatural deaths (see Section 6)')
    pb('Population context: 2017 census = 29,964 wild elephants (~60% of global wild Asian elephants)')
    pb('Chhattisgarh appears for both electrocution (32) and poisoning (2) — directly relevant here')
    story.append(PageBreak())

    # S3
    h1('3.  Anthropogenic Poisons')
    h2('3.1  Agrochemicals — Pesticides (Neurotoxins)')
    pb('Crop-raiding consumption AND deliberate baiting (laced crops/fruit/salt) for retaliation/poaching')
    dtbl(['Compound','Class','Toxicity / Notes'],
         [('Carbofuran ("Furadan")','Carbamate','Granular; leading agent in deliberate wildlife baiting (esp. Kerala)'),
          ('Monocrotophos','Organophosphate','Highly toxic — oral LD50 ~18–20 mg/kg; common on grain baits'),
          ('Aldicarb ("Temik")','Carbamate','Among the most acutely toxic carbamates'),
          ('Chlorpyrifos','Organophosphate','Less acutely toxic (LD50 ~500 mg/kg goats)'),
          ('Imidacloprid','Neonicotinoid','Killed a wild adult Asian elephant (Kerala)')],
         wds=[3.5,2.5,11])
    pb('Mechanism: both inhibit acetylcholinesterase → ACh accumulates. OPs phosphorylate (irreversible after "aging"); carbamates carbamylate (reversible, <24 h)')
    pb('DUMBELS toxidrome: Defecation, Urination, Miosis, Bronchorrhoea, Emesis, Lacrimation, Salivation; fasciculation; death from respiratory failure')
    pb('Diagnosis: brain AChE depression <50% of normal = diagnostic; freeze samples FAST (carbamate ChE reactivates)')
    pb('ANTIDOTE: Atropine 0.6–1.0 mg/kg (cattle ref; ⅓ IV) + Pralidoxime/2-PAM 20–50 mg/kg slow IV (OP only, give early)')
    h2('3.2  Cyanide')
    pb('Used in illegal poaching/mining → rapid fatal hypoxia; poachers lace salt licks near waterholes')
    pb('Binds cytochrome c oxidase → blocks mitochondrial oxygen use (see Section 5 for detail)')
    h2('3.3  Fertilizers / Heavy Metals')
    pb('UREA toxicity → ammonia → neurological signs, death')
    pb('LEAD: encephalopathy, GI colic, kidney damage (paint, batteries, mining waste)')
    pb('ARSENIC: haemorrhagic enteritis, liver/kidney damage (pesticides, industrial effluent)')
    kyb('SAMPLING: gut contents, liver, kidney, brain, blood (frozen). OP/carbamate → blood AChE. Heavy metals → liver/kidney for AAS. Always collect suspected bait. Send to IVRI/State FSL with suspected-diagnosis note.')
    story.append(PageBreak())

    # S4
    h1('4.  Mycotoxins & Biological Toxins')
    pi(3, 'Slide 3 — Mycotoxins (CPA/Kodo); cyanotoxins; toxic plants; Bandhavgarh Kodo case', 12)
    pi(4, 'Slide 4 — Field photographs: raided Kodo millet crop; necropsy organ findings', 12)
    h2('4.1  Crop-Borne Mycotoxins — Kodo Millet (Cyclopiazonic Acid)')
    bdy('Elephants raiding farm fields are highly susceptible to mycotoxins like Cyclopiazonic Acid (CPA) — a fungal toxin (Aspergillus, Penicillium) that infects Kodo millet (Paspalum scrobiculatum) and causes acute vascular damage and liver/kidney necrosis. Contamination occurs when heavy/unseasonal rainfall coincides with grain maturation.')
    kyb('CASE — Bandhavgarh Tiger Reserve (MP): A herd raided Kodo millet crops; TEN wild elephants died over 3 days (29–31 Oct 2024), Khitoli range. IVRI report (5 Nov 2024): NO nitrates, NO heavy metals, NO pesticides — but CYCLOPIAZONIC ACID (CPA) confirmed in viscera of all. Verdict: fungus-infected Kodo millet (the fungus, not the grain). Dr. Shrivastava: "treated two cases in KTR during 1997–98."', danger=True)
    pb('CPA mechanism: indole-tetramic acid mycotoxin (Aspergillus/Penicillium); inhibits Ca²⁺-ATPase (SERCA) → disrupts calcium gradients → hepatotoxicity, nephrotoxicity, vascular damage')
    pb('Aflatoxins (differential): A. flavus on grain → hepatic necrosis, bile-duct proliferation, icterus, coagulopathy')
    pb('Management: preventive cultivation/storage; biocontrol (non-toxigenic fungal strains); proper drying + airtight storage of Kodo')
    h2('4.2  Cyanotoxins / Cyanobacteria (Blue-Green Algae)')
    pb('Toxic blue-green algae blooms in stagnant seasonal water → neurotoxins + hepatotoxins → fatal die-offs')
    pb('Common in hot, dry seasons when water sources shrink/concentrate')
    pb('Microcystins (hepatotoxins, Microcystis) → inhibit protein phosphatases → hepatocyte necrosis, intrahepatic haemorrhage')
    pb('Anatoxin-a (neurotoxin) → nicotinic ACh-receptor agonist → depolarising paralysis; Saxitoxins → block Na⁺ channels → flaccid paralysis')
    pb('2020 Botswana (Okavango): ≥330 African elephants died — tusks intact (poaching ruled out); cyanobacterial neurotoxins implicated; elephants drink up to 200 L/day → high toxin dose')
    h2('4.3  Toxic Plants')
    pb('Elephants generally avoid toxic vegetation, but oleander (cardiac glycosides) → fatal arrhythmia')
    pb('Calcium oxalate-containing plants → severe oral/GI irritation, swelling, systemic distress')
    story.append(PageBreak())

    # S5
    h1('5.  HCN (Cyanide) Poisoning from Sorghum')
    pi(5, 'Slide 5 — HCN poisoning: mechanism, signs, risk factors, management & antidote', 12)
    pi(6, 'Slide 6 — HCN case report (Zoo Print 2010); Electrocution introduction', 12)
    h2('5.1  Mechanism')
    bdy('HCN (prussic acid) poisoning occurs when elephants consume STRESSED sorghum (drought, frost, trampling) → rapid cellular asphyxiation. Sorghum (Sorghum bicolor) contains the cyanogenic glucoside DHURRIN. When chewed, plant enzymes mix with dhurrin → release hydrogen cyanide → binds cytochrome c oxidase → cells cannot use oxygen → histotoxic hypoxia → lactic acidosis → death. Lethal dose ~2–2.5 mg/kg; onset ~15–20 min. The cherry-red colour FADES after death — suggestive, not confirmatory.')
    h2('5.2  Signs & Symptoms')
    pb('RAPID ONSET: minutes to a few hours after consumption')
    pb('Laboured/rapid breathing, staggering gait, muscle tremors, convulsions, recumbency, sudden death')
    pb('BITTER ALMOND smell; excessive salivation; BRIGHT CHERRY-RED blood and mucous membranes')
    pb('DISTINCTION: cyanide → cherry-red blood; nitrate poisoning → brown (chocolate) blood')
    h2('5.3  Risk Factors')
    dtbl(['Risk Factor','Detail'],
         [('Plant height/maturity','Young dark-green regrowth (<50 cm tall) = highest toxin concentration'),
          ('Environmental stress','Drought-stressed, wilted, or frost-damaged plants are most toxic'),
          ('Digestive process','Hindgut fermenters; large quantities overwhelm detoxification capacity')],
         wds=[4.5,12.5])
    h2('5.4  Antidote & Prevention')
    pb('Remove food source immediately; move herd away from sorghum field')
    pb('SODIUM NITRITE IV (1–3 gm in 50 ml distilled water) → forms methaemoglobin → binds cyanide as cyanmethaemoglobin')
    pb('SODIUM THIOSULPHATE IV → converts cyanide to non-toxic thiocyanate → excreted in urine')
    pb('Prevention: avoid young plants (<45–60 cm); wait after drought/frost; hay safer than fresh pasture (test forage)')
    kyb('CASE — Circus elephants, Jabalpur (Zoo Print 2010, Dr. Shrivastava): 5 adults fed fresh Jowar (unaccustomed) → restlessness, diarrhoea, subnormal temp 97–98°F. Treated: dextrose saline + MVI; sodium thiosulphate 50 gm oral, repeated 12 hrs; cold saline + ice + Diadin per rectum. Aged elephant recovered next morning.', danger=True)
    story.append(PageBreak())

    # S6
    h1('6.  Electrocution in Elephants')
    pi(7, 'Slide 7 — Electrocution in an elephant (Nov 2020): field photographs', 12)
    pi(9, 'Slide 9 — Electrocution case: carcass handling and postmortem photographs', 12)
    h2('6.1  Definition & Mechanics')
    bdy('Electrocution = death/severe injury from electric shock; occurs when the animal becomes part of an electrical circuit. High voltage/current disrupts the body\'s electrical systems → cardiac arrest or severe electrical burns.')
    dtbl(['Term','Definition'],
         [('Electric Shock','Physical sensation/injury from electricity (muscle spasm, minor burns) — NON-FATAL'),
          ('Electrocution','An electric shock that is FATAL')],
         wds=[4,13])
    h2('6.2  Statistics (India)')
    pb('SINGLE LARGEST cause of unnatural elephant death — 392 of 528 (74%) over 5 years (Lok Sabha 2024); long-run share since 2009 ≈ 67%')
    pb('State-wise (2024): Odisha 71, Assam 55, Karnataka 52, Tamil Nadu 49, Chhattisgarh 32, Jharkhand 30, Kerala 29')
    h2('6.3  Sources & Mechanisms')
    dtbl(['Source','Description'],
         [('Illegal live-wire fences','Power "hooked" from 11 kV/LT lines to electrify crop fences — LEADING driver; deliberate'),
          ('Sagging overhead lines','Low 11 kV lines (as low as ~1.5 m vs ~3.3 m elephant) from wide pole spacing/erosion'),
          ('Solar-fence tampering','Bypassing the pulsed energiser → connecting to mains turns a legal fence lethal'),
          ('Accidental','Genuine contact with sagging legal lines in corridors')],
         wds=[4,13])
    h2('6.4  Postmortem Findings')
    pb('CURRENT/ELECTRIC MARK (gross gold standard): crater-like skin elevation around sunken pale centre at contact (trunk tip, feet, dorsum)')
    pb('JOULE BURN: collagen denaturation + dermal oedema; singed hair; METALLIZATION (conductor metal in skin) in >50% of cases')
    pb('HISTOLOGY: coagulative epidermal necrosis; "NUCLEAR STREAMING" of basal nuclei aligned to current flow; dermal collagen homogenisation')
    pb('INTERNAL: visceral congestion; pulmonary oedema; myocardial petechiae/necrosis; rhabdomyolysis; slow-clotting dark blood')
    pb('CAVEAT: nuclear streaming/necrosis NOT pathognomonic (also in flame burns); gross lesions may be absent if contact wide/skin wet (Schulze 2016)')
    h2('6.5  Lightning vs Man-Made Electrocution')
    dtbl(['Feature','Lightning','Man-Made'],
         [('Skin','LICHTENBERG (fern-like) figures — pathognomonic; fade 24–36 hr; NOT burns','Discrete deep contact/current burns; metallization'),
          ('Animals','Often multiple down together','Single or group along a wire'),
          ('Scene','Open ground/tall trees; storm; scorched vegetation','Near power line/hooked wire/fence'),
          ('Entry/exit','Poorly defined','Well-defined (feet = exit)')],
         wds=[2.5,7,7.5])
    h2('6.6  Legal Framework')
    pb('WPA 1972: elephant Schedule I; killing under Section 51 (+ IPC 429, Electricity Act)')
    pb('Electricity Act 2003: Sec 161 (accident report/inquiry), Sec 135 (theft — illegal hooking), Sec 146 (penalty)')
    pb('NGT strict liability of utilities (e.g. CESU Odisha ordered ₹4 crore + line maintenance)')
    pb('Clearance: MoEFCC 2010 min 5.5 m for ≤11 kV; Karnataka HC 2025 — underground cabling, ban illegal fences, AI/CCTV surveillance')
    kyb('INVESTIGATION: photograph scene (wires, poles, sag height, distance); current marks with scale bar; skin histology (coagulative necrosis + nuclear streaming + metallization); sample heart/lung; RULE OUT lightning (Lichtenberg figures, multiple carcasses); coordinate electricity board/police (WPA Sec 51 + Electricity Act Sec 135/161); PREVENT by converting illegal AC fences to pulsed SOLAR energisers.', danger=True)
    story.append(PageBreak())

    # S7
    h1('7.  Pyometra')
    pi(8, 'Slide 8 — Pyometra in Asian elephants (clinical photograph; purulent discharge)', 12)
    pi(10, 'Slide 10 — Vaginal vestibulotomy in Asian elephant: surgical drainage', 12)
    h2('7.1  Definition')
    bdy('Pyometra = severe, life-threatening uterine infection with accumulation of PUS and severe inflammation. Most common in AGING, NULLIPAROUS (never-bred) females, linked to prolonged hormonal fluctuation and reproductive issues.')
    h2('7.2  CEH–Pyometra Complex & Pathophysiology')
    pb('CEH (cystic endometrial hyperplasia) is the precursor — present in ~67% of captive Asian elephants aged 26–57 yr (Agnew et al. 2004)')
    pb('Chronic progesterone (luteal ~6–12 wk) dominance → endometrial proliferation/cysts → reduced defence → bacterial colonisation → pyometra')
    pb('Bacteria: E. coli (predominant), Streptococcus, Staphylococcus, Klebsiella, Proteus (extrapolated; elephant culture series sparse)')
    pb('Co-pathology: uterine LEIOMYOMAS most common tumour — larger/commoner in older nulliparous Asians (30–100%); ~13% adenocarcinoma')
    h2('7.3  Predisposition & Anatomy')
    pb('Asymmetric reproductive aging (Hermes et al. 2004): prolonged non-breeding + continuous steroid exposure → genital pathology, irreversible acyclicity')
    pb('Up to 14% captive Asian (29% African) elephants are acyclic/irregular')
    pb('Anatomy: urogenital canal ~1.0–1.4 m; hymenal orifice <2 cm; total tract up to 358 cm → impedes drainage, favours closed pyometra')
    pb('Ultrasonography is the key diagnostic tool (cysts, CEH, leiomyoma, intrauterine fluid)')
    h2('7.4  Treatment')
    dtbl(['Approach','Detail'],
         [('Hormonal downregulation','GnRH vaccine (Improvac) → ↓LH/FSH; Deslorelin implants. EAZA: treat pyometra BEFORE vaccinating'),
          ('Antibiotic therapy','Broad-spectrum, culture-guided'),
          ('Uterine/transcervical lavage','Warm saline flush — constrained by the long canal/hymen'),
          ('Prostaglandins (PGF2α)','Myometrial contraction + cervical relaxation (minimally documented in elephants)'),
          ('Surgical drainage','Vaginal vestibulotomy (slide 10)'),
          ('Homeopathic (practised)','Pyrogenium 1000 + Hepar sulph 1000 + Secale 1000 (Dr. Shrivastava)')],
         wds=[4,13])
    pb('Ovariohysterectomy NOT practical (body size, vascularity, tract up to 358 cm); prognosis guarded to poor — documented cases improved then died')
    kyb('Pyometra is a reproductive EMERGENCY — endotoxaemia → septic shock/death; the long valved canal favours CLOSED accumulation, raising mortality. Avoid GnRH-agonist implants during the luteal phase. Prevention: managed breeding or cycle suppression to break the CEH→pyometra cascade.')
    story.append(PageBreak())

    # S8
    h1('8.  Hyperthermia & Heat Stress')
    h2('8.1  Definition')
    bdy('Hyperthermia is a life-threatening condition from high environmental temperature, lack of access to water/shade, massive body size, and lack of sweat glands — a serious mortality concern during Indian summers.')
    bdy('Normal core temperature is LOW (~36.2 ± 0.5°C); elephants do NOT pant or sweat conventionally — heat DISSIPATION, not generation, is the challenge.')
    h2('8.2  Why Elephants Overheat')
    pb('SQUARE-CUBE LAW: surface area scales as square, mass as cube → little skin to dump heat; problems set in above ~35°C ambient')
    pb('Compensation: thermal conductance 3–5× higher than predicted (lack of fur); but 56–100% of exercise heat is STORED in core and dumped later')
    pb('Modelling: arterial blood can rise ~5°C to lethal levels after ~15 min locomotion at 26°C ambient')
    h2('8.2b  The Sweat-Gland Question (precise science)')
    pb('"No sweat glands" is an oversimplification: lack dense body-wide glands BUT have INTERDIGITAL eccrine-like glands (feet only)')
    pb('Very high cutaneous evaporative water loss (0.31–8.9 g/min/m², Asian) — water diffuses through bare skin, not glands (Dunkin 2013)')
    pb('Skin MICRO-CRACKS retain 5–10× more water/mud than flat skin, prolonging evaporative cooling (Martins 2018, Nature Comms)')
    h2('8.3  Natural Cooling Mechanisms')
    dtbl(['Mechanism','How It Works'],
         [('The Ears (thermal windows)','Vasodilate/flood ears with blood, flap for convective+evaporative cooling; up to ~100% of heat-loss need (Phillips & Heath 1992)'),
          ('Wallowing & Spraying','PRIMARY evaporative cooling; mud blocks solar radiation, prolongs water retention'),
          ('Cutaneous water loss','Through bare skin; at 29–32°C ambient, evaporation is the ONLY remaining avenue'),
          ('Body-wide windows','Hot vascular patches appear across whole body as ambient rises (Weissenböck 2010)')],
         wds=[4,13])
    h2('8.4  How Heat Stress Kills')
    pb('Heat stroke = core >40°C + CNS dysfunction → protein denaturation, oxidative stress, DAMPs → systemic inflammation')
    pb('Endothelial barrier disruption → vascular leak, microthrombi → ischaemic organ injury; DIC in ~48% of severe cases')
    pb('Organ failure: liver (coagulopathy), kidney (rhabdomyolysis→AKI), heart (arrhythmia→circulatory collapse)')
    h2('8.5  Recent India Cases & Management')
    pb('Apr 2022 Karnataka: 2 young elephants died near Cauvery WLS (heat stroke + dehydration) amid drought/extreme heat')
    pb('Constant SHADE + DRINKING WATER (esp. 11 AM–4 PM); wallowing pools; avoid work in peak heat')
    pb('Signs: rapid breathing, intensified ear-flapping, lethargy, collapse. Emergency: water spray (ears/head), shade, IV fluids')
    story.append(PageBreak())

    # S9
    h1('9.  Iron Deficiency Anaemia')
    pi(11, 'Slide 11 — Blood smear: microcytic hypochromic target cells (codocytes)', 12)
    h2('9.1  Definition & Signs')
    bdy('Anaemia = qualitative and quantitative reduction in blood quality / oxygen-carrying capacity. Iron deficiency → microcytic, hypochromic RBCs. Signs: pale mucous membranes, extreme weakness, unable to walk, very slow walk and reduced activity.')
    h2('9.2  Normal Haematology Reference Values (Indian Elephants)')
    dtbl(['Parameter','Reference Interval','Note'],
         [('Haemoglobin','8.62–16.78 g/dL','Low = anaemia'),
          ('PCV / Haematocrit','21.73–49.25 %','—'),
          ('RBC count','1.77–4.9 ×10⁶/µL','LOW count (large cells)'),
          ('MCV','112.49–131.39 fL','HIGH — large RBCs'),
          ('WBC (TLC)','9,912–29,475 /µL','—'),
          ('Platelets','171.6–947.1 ×10³/µL','—')],
         wds=[4,5,8])
    pb('Distinctive: HETEROPHILS (not neutrophils); unique bilobed/trilobed MONOCYTE (most abundant leucocyte). Automated analysers inaccurate — use manual Giemsa smear (Frontiers Vet Sci 2025)')
    h2('9.3  Diagnosis & Causes')
    pb('Low Hb; smear: target cells, hypochromia, microcytosis, anisocytosis; iron panel (serum iron, ferritin, TIBC); faecal egg counts')
    pb('Causes: GI strongyles (Murshidia, Quilonia, Bathmostomum) → protein-losing enteropathy; hookworms (B. sangeri caecum, Grammocephalus bile duct)')
    pb('Liver fluke Fasciola jacksoni (18–62% Indomalayan) → anaemia + hypoproteinaemia; nutritional (Fe/Cu/Co); chronic disease (TB iron-sequestration); EEHV in calves')
    kyb('IRON OVERLOAD CAUTION: haemochromatosis-type iron storage disease occurs in captive elephants; blind iron supplementation can REACTIVATE latent M. tuberculosis. Confirm true deficiency with an iron panel BEFORE supplementing. Forage requirement: Cu 10, Fe 50, Co 0.1 mg/kg.', danger=True)
    h2('9.4  Treatment')
    pb('Diet change to full normal elephant diet: soybeans, horse gram, Napier grass, bamboo, leaves, grains, fruits')
    pb('Iron supplements: Jaggery (gur), honey')
    pb('Vitamin B12 injections; Multivitamins + mineral mixture')
    kyb('INVESTIGATION: Iron deficiency anaemia is often SECONDARY — investigate chronic blood loss (ticks, lice, GI helminths), nutritional inadequacy, or chronic disease. Run a parasitological exam alongside iron supplementation to prevent relapse.')
    story.append(PageBreak())

    # S10
    h1('10.  References & Recommended Reading')
    h2('10.1  Works by Prof. Dr. A B Shrivastava')
    pb('Shrivastav AB (2010). Management of Hydrocyanic Acid Poisoning in Asian Elephants. Zoo Print vol. XXV, 6 June 2010')
    pb('Shrivastav AB & Sharma RK (2008). A Manual of Wildlife Health Management in Protected Areas. CVAH, JNKVV, Jabalpur')
    pb('Nigam P, Habib J & Pandey H (Ed.) (2021). Caring for Elephants: Managing Health & Welfare in Captivity')
    pb('MoEFCC/WII (2020). Necropsy and Carcass Disposal of Asian Elephant: Recommended Operating Procedure')
    h2('10.2  Peer-Reviewed & Reference Literature')
    pb('Radostits OM, Blood DC & Gay CC (1994/2007). Veterinary Medicine. ELBS/Tindall')
    pb('Fowler ME & Mikota SK (2006). Biology, Medicine and Surgery of Elephants. Blackwell, Iowa')
    pb('WTI. Elephant Mortality Database — poisoning records 1997–2005')
    pb('Wang DZ (2008). Neurotoxins from marine and freshwater algae. Marine Drugs 6(2): 349–371')
    pb('Schulze C et al. (2016). Electrical Injuries in Animals. Veterinary Pathology 53(5): 1018–1037')
    pb('Agnew DW, Munson L, Ramsay EC (2004). Cystic Endometrial Hyperplasia in Elephants. Vet Pathol 41(2): 179–183')
    pb('Hermes R, Hildebrandt TB, Göritz F (2004). Asymmetric reproductive aging. Anim Reprod Sci 82–83: 49–60')
    pb('Dunkin RC et al. (2013). Thermal balance & cutaneous water loss in elephants. J Exp Biol 216: 2939–2952')
    pb('Martins AF et al. (2018). Bending cracks in African elephant skin. Nature Communications 9: 3865')
    pb('Reference intervals for haematology in Indian elephants (2025). Frontiers Vet Sci 12: 1602296 (PMC12301552)')
    pb('Lok Sabha reply (July 2024). Elephant deaths from unnatural causes 2019–2024. MoEFCC, GoI')
    pb('Karnataka High Court (2025). Elephant electrocution suo motu directions ("Ashwathamma" case)')
    pb('Mahato G et al. (2021). Heavy metal toxicosis in elephants — review. Indian J Vet Pathology')
    pb('Project Elephant, MoEFCC (2017). Gajah: Securing the Future for Elephants in India')
    hr()
    story.append(Paragraph(
        'Prof. Dr. A B Shrivastava, NDVSU Jabalpur  |  Presentation: 06-06-2026  |  '
        'Training Program: Mortality Investigation of Asian Elephant, Raigarh, Chhattisgarh  |  '
        'Notes elaborated with peer-reviewed literature', sFT))

    doc.build(story)
    print(f'  ✓  {OUT_P}  ({os.path.getsize(OUT_P)//1024} KB)')


if __name__ == '__main__':
    print('Building ABS Non-Infectious Pathology Notes...\n')
    print('  → Word document...'); build_docx()
    print('  → PDF document...'); build_pdf()
    print('\nDone.')

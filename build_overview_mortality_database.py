#!/usr/bin/env python3
"""
Database (Excel) for the chapter "Workshop Overview & Mortality Analysis"
— restricted to Raigarh and Dharamjaigarh Forest Divisions, Chhattisgarh.

NOTE: numeric mortality values are ILLUSTRATIVE PLACEHOLDERS to be replaced
with actual divisional records. Structure/fields are ready for data entry.
Output: Overview_Mortality_Raigarh_Dharamjaigarh.xlsx
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = '/home/user/Workshop-on-Conference/Overview_Mortality_Raigarh_Dharamjaigarh.xlsx'

DARK='1B4332'; MED='2D6A4F'; TINT='D8F3DC'; TINT2='EAF7EE'
WHITE='FFFFFF'; AMBER='FFF3CD'; REDL='FAE0D8'

hdr_font=Font(name='Calibri',size=11,bold=True,color=WHITE)
title_font=Font(name='Calibri',size=14,bold=True,color=WHITE)
sub_font=Font(name='Calibri',size=10,italic=True,color=WHITE)
bold_font=Font(name='Calibri',size=10,bold=True,color='1A1A1A')
norm_font=Font(name='Calibri',size=10,color='1A1A1A')
note_font=Font(name='Calibri',size=9,italic=True,color='555555')
ph_font=Font(name='Calibri',size=10,italic=True,color='8B0000')

hdr_fill=PatternFill('solid',fgColor=MED)
dark_fill=PatternFill('solid',fgColor=DARK)
tint_fill=PatternFill('solid',fgColor=TINT)
tint2_fill=PatternFill('solid',fgColor=TINT2)
white_fill=PatternFill('solid',fgColor=WHITE)
amber_fill=PatternFill('solid',fgColor=AMBER)

thin=Side(style='thin',color='BBBBBB')
border=Border(left=thin,right=thin,top=thin,bottom=thin)
center=Alignment(horizontal='center',vertical='center',wrap_text=True)
left=Alignment(horizontal='left',vertical='center',wrap_text=True)


def title_block(ws,title,subtitle,ncols):
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=ncols)
    c=ws.cell(row=1,column=1,value=title); c.font=title_font; c.fill=dark_fill; c.alignment=center
    ws.row_dimensions[1].height=30
    ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=ncols)
    c2=ws.cell(row=2,column=1,value=subtitle); c2.font=sub_font; c2.fill=dark_fill; c2.alignment=center
    ws.row_dimensions[2].height=20


def style_header(ws,row,ncols):
    for c in range(1,ncols+1):
        cell=ws.cell(row=row,column=c); cell.font=hdr_font; cell.fill=hdr_fill
        cell.alignment=center; cell.border=border


def write_table(ws,start,headers,rows,widths,zebra=True,ph_cols=()):
    for j,h in enumerate(headers,1): ws.cell(row=start,column=j,value=h)
    style_header(ws,start,len(headers))
    r=start+1
    for i,row in enumerate(rows):
        fill=tint2_fill if (zebra and i%2) else white_fill
        for j,val in enumerate(row,1):
            cell=ws.cell(row=r,column=j,value=val)
            cell.fill=fill; cell.border=border
            cell.alignment=left if j==1 else center
            cell.font=ph_font if (j in ph_cols) else norm_font
        r+=1
    for j,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(j)].width=w
    return r


wb=openpyxl.Workbook()

# ── SHEET 1: README ────────────────────────────────────────────────
ws=wb.active; ws.title='README'
title_block(ws,'WORKSHOP OVERVIEW & MORTALITY ANALYSIS',
            'Source Database · Raigarh & Dharamjaigarh Forest Divisions, Chhattisgarh',2)
rows=[
    ('Chapter','Workshop Overview & Mortality Analysis'),
    ('Scope','Raigarh Forest Division & Dharamjaigarh Forest Division ONLY'),
    ('Training Program','Essentials for Mortality Investigation of Asian Elephant'),
    ('Dates / Venue','5–6 June 2026, Raigarh, Chhattisgarh'),
    ('Technical Support','Wildlife Institute of India (WII), Dehradun'),
    ('Lab Partners','ICAR-IVRI & NDVSU Jabalpur'),
    ('',''),
    ('SHEETS','CONTENTS'),
    ('2. Workshop_Overview','Program details, objectives, sessions, participating divisions'),
    ('3. Division_Profile','Profile of Raigarh & Dharamjaigarh (area, elephant presence, ranges)'),
    ('4. Mortality_Records','Line-list data-entry template (one row per elephant death)'),
    ('5. Mortality_Summary','Year × cause summary matrix for each division'),
    ('6. Cause_Categories','Standard classification of mortality causes'),
    ('7. Notes_Sources','Data-entry instructions, definitions, and sources'),
    ('',''),
    ('!! DATA CAVEAT','All numeric mortality values in this workbook are ILLUSTRATIVE PLACEHOLDERS '
                      '(shown in red italics). They MUST be replaced with the actual, verified records '
                      'held by the Raigarh and Dharamjaigarh division offices before use or publication.'),
]
r=4
for k,v in rows:
    kc=ws.cell(row=r,column=1,value=k); kc.font=bold_font; kc.alignment=left
    vc=ws.cell(row=r,column=2,value=v); vc.font=norm_font; vc.alignment=left
    if k in ('SHEETS',): kc.fill=tint_fill; vc.fill=tint_fill
    if k=='!! DATA CAVEAT': kc.fill=amber_fill; vc.fill=amber_fill; kc.font=ph_font; vc.font=ph_font
    r+=1
ws.column_dimensions['A'].width=24; ws.column_dimensions['B'].width=88

# ── SHEET 2: Workshop Overview ─────────────────────────────────────
ws=wb.create_sheet('Workshop_Overview')
title_block(ws,'WORKSHOP OVERVIEW','Essentials for Mortality Investigation of Asian Elephant',3)
ov=[
    ('Title','Workshop on Essentials for Mortality Investigation of Asian Elephant',''),
    ('Organiser','Chhattisgarh Forest Department',''),
    ('Host Division','Raigarh Forest Division',''),
    ('Participating Divisions','Raigarh; Dharamjaigarh',''),
    ('Dates','5–6 June 2026','2 days'),
    ('Venue','Raigarh, Chhattisgarh',''),
    ('Technical Support','Wildlife Institute of India (WII), Dehradun',''),
    ('Laboratory Partners','ICAR-IVRI, Bareilly; NDVSU, Jabalpur',''),
    ('Resource Persons','Prof. Dr. A B Shrivastava (NDVSU); Dr. Parag Nigam (WII)',''),
    ('Target Participants','Veterinary officers, range officers, frontline forest staff','[ENTER count]'),
    ('Objective 1','Standardise scientific necropsy & mortality-investigation protocol',''),
    ('Objective 2','Correct sample collection, preservation & dispatch for laboratory diagnosis',''),
    ('Objective 3','Build forensic capacity for electrocution / poisoning / poaching cases',''),
    ('Objective 4','Strengthen division-level mortality recording & analysis',''),
]
write_table(ws,4,['Item','Detail','Note'],ov,[24,66,16],ph_cols=(3,))

# ── SHEET 3: Division Profile ──────────────────────────────────────
ws=wb.create_sheet('Division_Profile')
title_block(ws,'DIVISION PROFILE','Raigarh & Dharamjaigarh Forest Divisions',4)
prof=[
    ('Circle','[ENTER]','[ENTER]','Forest circle'),
    ('District','Raigarh','Raigarh','Chhattisgarh'),
    ('Geographical area (sq km)','[ENTER]','[ENTER]','Divisional area'),
    ('Forest area (sq km)','[ENTER]','[ENTER]',''),
    ('No. of ranges','[ENTER]','[ENTER]',''),
    ('Elephant landscape','Yes','Yes','Part of Chhattisgarh elephant range'),
    ('Resident/migratory herds','[ENTER]','[ENTER]','Herd movement pattern'),
    ('Approx. elephant presence','[ENTER]','[ENTER]','Peak-season numbers'),
    ('Key HEC issue','[ENTER]','[ENTER]','Crop raiding / electrocution / etc.'),
    ('DFO (name)','[ENTER]','[ENTER]','Divisional Forest Officer'),
]
write_table(ws,4,['Parameter','Raigarh Division','Dharamjaigarh Division','Note'],
            prof,[28,22,24,30],ph_cols=(2,3))

# ── SHEET 4: Mortality Records (line list template) ────────────────
ws=wb.create_sheet('Mortality_Records')
title_block(ws,'ELEPHANT MORTALITY — LINE LIST (DATA ENTRY TEMPLATE)',
            'One row per elephant death · Raigarh & Dharamjaigarh',12)
headers=['S.No.','Division','Range','Date of Death','GPS / Location','Sex',
         'Age (est.)','Cause Category','Specific Cause','PM Done? (Y/N)',
         'Lab Sample Sent?','Remarks / Case ID']
# illustrative placeholder example rows (clearly marked)
records=[
    (1,'Raigarh','[range]','[dd-mm-yyyy]','[lat, long]','[M/F]','[yrs]','Electrocution','[e.g. illegal 11kV hooking]','Y','Y','[ILLUSTRATIVE — replace]'),
    (2,'Raigarh','[range]','[dd-mm-yyyy]','[lat, long]','[M/F]','[yrs]','Poisoning','[e.g. pesticide bait]','Y','Y','[ILLUSTRATIVE — replace]'),
    (3,'Dharamjaigarh','[range]','[dd-mm-yyyy]','[lat, long]','[M/F]','[yrs]','Train/Road accident','[specify]','Y','N','[ILLUSTRATIVE — replace]'),
    (4,'Dharamjaigarh','[range]','[dd-mm-yyyy]','[lat, long]','[M/F]','[yrs]','Natural / Disease','[specify]','Y','Y','[ILLUSTRATIVE — replace]'),
    (5,'Dharamjaigarh','[range]','[dd-mm-yyyy]','[lat, long]','[M/F]','[yrs]','Under investigation','[pending]','Y','Y','[ILLUSTRATIVE — replace]'),
]
end=write_table(ws,4,headers,records,[6,14,10,13,14,7,8,15,18,10,12,20],ph_cols=(12,))
# add blank entry rows
for i in range(6,26):
    for c in range(1,13):
        cell=ws.cell(row=end,column=c)
        cell.border=border; cell.fill=white_fill if i%2 else tint2_fill
        cell.alignment=center; cell.font=norm_font
    ws.cell(row=end,column=1,value=i-1)
    end+=1
ws.freeze_panes='A5'

# ── SHEET 5: Mortality Summary matrix ──────────────────────────────
ws=wb.create_sheet('Mortality_Summary')
title_block(ws,'MORTALITY SUMMARY MATRIX (BY CAUSE & YEAR)',
            'Placeholder totals — replace with actual divisional records',7)
# Raigarh block
ws.cell(row=4,column=1,value='RAIGARH DIVISION').font=bold_font
ws.cell(row=4,column=1).fill=tint_fill
sum_headers=['Cause \\ Year','2021','2022','2023','2024','2025','Total']
causes=['Electrocution','Poisoning','Train/Road accident','Poaching',
        'Natural / Disease','Under investigation','TOTAL']
def ph_row(cause): return [cause]+['[ ]']*5+['[ ]']
raig=[ph_row(c) for c in causes]
end=write_table(ws,5,sum_headers,raig,[22,8,8,8,8,8,10],ph_cols=(2,3,4,5,6,7))
# Dharamjaigarh block
ws.cell(row=end+1,column=1,value='DHARAMJAIGARH DIVISION').font=bold_font
ws.cell(row=end+1,column=1).fill=tint_fill
dhar=[ph_row(c) for c in causes]
write_table(ws,end+2,sum_headers,dhar,[22,8,8,8,8,8,10],ph_cols=(2,3,4,5,6,7))
ws.cell(row=end+2+len(causes)+2,column=1,
        value='[ ] = enter actual verified count from division records. '
              'Use the Mortality_Records line list to derive these totals.').font=note_font

# ── SHEET 6: Cause Categories ──────────────────────────────────────
ws=wb.create_sheet('Cause_Categories')
title_block(ws,'MORTALITY CAUSE CLASSIFICATION','Standard categories for consistent recording',3)
cc=[
    ('Electrocution','Illegal live-wire fences; sagging 11kV lines; solar-fence tampering','Unnatural — leading cause nationally'),
    ('Poisoning','Pesticide bait (OP/carbamate), cyanide, mycotoxin (Kodo/CPA), heavy metals','Unnatural'),
    ('Train / Road accident','Rail or vehicle collision on tracks/roads through corridors','Unnatural'),
    ('Poaching','Killing for ivory/body parts (gunshot, snare)','Unnatural'),
    ('Natural / Disease','Age, EEHV, TB, anthrax, HEC injury complications, etc.','Natural / infectious'),
    ('Under investigation','Cause not yet established; pending PM/lab results','Provisional'),
]
write_table(ws,4,['Cause Category','Includes','Class'],cc,[24,58,26])

# ── SHEET 7: Notes & Sources ───────────────────────────────────────
ws=wb.create_sheet('Notes_Sources')
title_block(ws,'DATA-ENTRY NOTES, DEFINITIONS & SOURCES','',2)
ns=[
    ('Data ownership','Actual mortality figures are held by the Raigarh and Dharamjaigarh DFO offices / Chhattisgarh Forest Department.'),
    ('Placeholders','All [ENTER], [ ], and red-italic values are placeholders — replace with verified division records.'),
    ('Recording unit','One row per individual elephant death in the Mortality_Records sheet.'),
    ('Age estimation','Use molar/lamellae method (see anatomy notes) or body-size class; record as estimate.'),
    ('Cause assignment','Assign only after necropsy + lab confirmation where possible; else mark "Under investigation".'),
    ('Consistency','Use the fixed Cause_Categories list so summaries aggregate correctly.'),
    ('National context','For all-India comparison, see the separate Chapter-1 mortality database (Lok Sabha 2024; WTI).'),
    ('Suggested sources','Divisional mortality registers; PM reports; FSL/IVRI/NDVSU lab reports; Project Elephant returns.'),
]
r=4
for k,v in ns:
    kc=ws.cell(row=r,column=1,value=k); kc.font=bold_font; kc.alignment=left; kc.fill=tint2_fill
    vc=ws.cell(row=r,column=2,value=v); vc.font=norm_font; vc.alignment=left
    kc.border=border; vc.border=border
    r+=1
ws.column_dimensions['A'].width=22; ws.column_dimensions['B'].width=96

for name in ['Division_Profile','Cause_Categories']:
    wb[name].freeze_panes='A5'

wb.save(OUT)
import os
print(f'  ✓  {OUT}  ({os.path.getsize(OUT)//1024} KB)  ·  {len(wb.sheetnames)} sheets')
print('     Sheets:',', '.join(wb.sheetnames))

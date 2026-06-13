#!/usr/bin/env python3
"""
Illustrated workshop notes — charts generated via matplotlib, embedded in ReportLab PDF.
"""

import os, io, textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

# ── Palette ────────────────────────────────────────────────────────────────────
DG   = '#1B4332'   # dark green
MG   = '#2D6A4F'   # mid green
LG   = '#52B788'   # light green
PG   = '#D8F3DC'   # pale green
AMB  = '#D4870A'   # amber
RED  = '#C0392B'   # red
BLUE = '#2980B9'   # blue
SL   = '#2C3E50'   # slate
LGR  = '#ECF0F1'   # light grey
MGR  = '#BDC3C7'   # mid grey

W, H = A4
WC   = W - 72      # usable width (pt)

# ── ReportLab styles ───────────────────────────────────────────────────────────
def sty(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_T = sty('CT', fontSize=26, textColor=colors.white,
               leading=32, alignment=TA_CENTER, fontName='Helvetica-Bold')
COVER_S = sty('CS', fontSize=13, textColor=colors.HexColor(PG),
               leading=18, alignment=TA_CENTER)
COVER_D = sty('CD', fontSize=11, textColor=colors.HexColor(LG), alignment=TA_CENTER)
CH1     = sty('H1', fontSize=17, textColor=colors.HexColor(DG),
               leading=21, spaceBefore=12, spaceAfter=5, fontName='Helvetica-Bold')
CH2     = sty('H2', fontSize=12, textColor=colors.HexColor(MG),
               leading=16, spaceBefore=8, spaceAfter=3, fontName='Helvetica-Bold')
CH3     = sty('H3', fontSize=10.5, textColor=colors.HexColor(SL),
               leading=14, spaceBefore=5, spaceAfter=2, fontName='Helvetica-Bold')
BODY    = sty('BD', fontSize=9.5, textColor=colors.HexColor(SL),
               leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
BUL     = sty('BL', fontSize=9.5, textColor=colors.HexColor(SL),
               leading=13, leftIndent=14, spaceAfter=3)
SM      = sty('SM', fontSize=8,   textColor=colors.grey, leading=11, spaceAfter=2)
HI_STY  = sty('HI', fontSize=9.5, textColor=colors.HexColor(DG),
               leading=13, fontName='Helvetica-Bold',
               backColor=colors.HexColor(PG))
CAP     = sty('CP', fontSize=8.5, textColor=colors.grey,
               alignment=TA_CENTER, spaceBefore=2, spaceAfter=6)

def P(t):  return Paragraph(t, BODY)
def B(t, i=0):
    s = sty(f'BLI{i}', parent=BUL, leftIndent=14+i)
    return Paragraph(f'• {t}', s)
def SP(h=6): return Spacer(1, h)
def HR(c=MG, w=0.8): return HRFlowable(width='100%', thickness=w,
                                         color=colors.HexColor(c), spaceAfter=5, spaceBefore=3)

def section_banner(text, bg=DG):
    row = [[Paragraph(f'<b>{text}</b>',
             sty('SB', fontSize=13, textColor=colors.white, leading=17))]]
    t = Table(row, colWidths=[WC])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor(bg)),
        ('TOPPADDING',    (0,0),(-1,-1), 9),
        ('BOTTOMPADDING', (0,0),(-1,-1), 9),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
    ]))
    return t

def info_table(rows):
    ks = sty('KS', fontSize=9, textColor=colors.HexColor(DG), fontName='Helvetica-Bold')
    vs = sty('VS', fontSize=9, textColor=colors.HexColor(SL))
    data = [[Paragraph(k, ks), Paragraph(v, vs)] for k, v in rows]
    t = Table(data, colWidths=[38*mm, WC-38*mm])
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0),(-1,-1), [colors.white, colors.HexColor(LGR)]),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 6),
        ('GRID',          (0,0),(-1,-1), 0.3, colors.HexColor(MGR)),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ]))
    return t

def dtable(header, rows, cw=None):
    hs = sty('TH', fontSize=8.5, textColor=colors.white,
              fontName='Helvetica-Bold', leading=11)
    ds = sty('TD', fontSize=8.5, textColor=colors.HexColor(SL), leading=11)
    hrow = [Paragraph(h, hs) for h in header]
    drows= [[Paragraph(str(c), ds) for c in r] for r in rows]
    t = Table([hrow]+drows, colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0), colors.HexColor(DG)),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor(LGR)]),
        ('GRID',          (0,0),(-1,-1), 0.35, colors.HexColor(MGR)),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ]))
    return t

def highlight_box(text, bg=PG, border=MG, tc=DG):
    row = [[Paragraph(text, sty('HB', fontSize=9.5, textColor=colors.HexColor(tc),
                                 leading=14, fontName='Helvetica-Bold'))]]
    t = Table(row, colWidths=[WC])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor(bg)),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
        ('BOX',           (0,0),(-1,-1), 1.2, colors.HexColor(border)),
    ]))
    return t

def alert_box(text):
    return highlight_box(text, bg='#FDECEA', border=RED, tc='#7B0000')

# ── Chart → ReportLab Image helper ────────────────────────────────────────────
def fig_to_rl(fig, width_pt, height_pt):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return Image(buf, width=width_pt, height=height_pt)

# ── Chart helpers ──────────────────────────────────────────────────────────────
def setup_ax(ax, title='', xlabel='', ylabel=''):
    ax.set_facecolor('#F7FAF8')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#BDC3C7')
    ax.tick_params(colors='#4A5568', labelsize=8)
    if title:  ax.set_title(title, fontsize=10, fontweight='bold', color=DG, pad=8)
    if xlabel: ax.set_xlabel(xlabel, fontsize=8, color='#4A5568')
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color='#4A5568')

# ══════════════════════════════════════════════════════════════════════════════
#  CHARTS
# ══════════════════════════════════════════════════════════════════════════════

# 1. Population trend line chart
def chart_population():
    years  = ['2001','2005','2007','2015','2017','2021','2026']
    pop    = [24, 123, 122, 247, 247, 279, 451]
    fig, ax = plt.subplots(figsize=(7,3), facecolor='white')
    ax.fill_between(years, pop, alpha=0.15, color=LG)
    ax.plot(years, pop, '-o', color=MG, linewidth=2.2, markersize=6,
            markerfacecolor=LG, markeredgecolor=DG, markeredgewidth=1)
    for x, y in zip(years, pop):
        ax.annotate(str(y), (x, y), textcoords='offset points',
                    xytext=(0, 9), ha='center', fontsize=8.5,
                    fontweight='bold', color=DG)
    setup_ax(ax, 'Elephant Population Trend — Chhattisgarh (2001–2026)',
             ylabel='Estimated Population')
    ax.set_ylim(0, 520)
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 160)

# 2. Year-wise deaths grouped bar
def chart_yearly_deaths():
    years  = ['2021-22','2022-23','2023-24','2024-25','2025-26','2026-27*']
    dh     = [4, 6, 6, 6, 1, 4]
    rg     = [0, 6, 0, 4, 11, 1]
    total  = [4,12, 6,10,12, 5]
    x = np.arange(len(years))
    w = 0.28
    fig, ax = plt.subplots(figsize=(7,3.2), facecolor='white')
    b1 = ax.bar(x-w, dh, w, label='Dharamjaigarh', color=MG, alpha=0.85)
    b2 = ax.bar(x,   rg, w, label='Raigarh',        color=AMB, alpha=0.85)
    b3 = ax.bar(x+w, total, w, label='Total',        color=SL, alpha=0.55)
    for bar in [*b1, *b2, *b3]:
        h = bar.get_height()
        if h:
            ax.text(bar.get_x()+bar.get_width()/2, h+0.2, str(int(h)),
                    ha='center', fontsize=7.5, color='#2C3E50')
    ax.set_xticks(x)
    ax.set_xticklabels(years, rotation=15, fontsize=8)
    setup_ax(ax, 'Year-wise Elephant Deaths — Both Divisions (2021–2026)',
             ylabel='Number of Deaths')
    ax.legend(fontsize=8, framealpha=0.5)
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=MGR)
    ax.set_ylim(0, 16)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 170)

# 3. Cause of death donut + bar side by side
def chart_cause():
    causes  = ['Electrocution','Suspected\nDrowning','Natural/\nOld Age','Fall/Trauma','Other']
    counts  = [23, 13, 4, 4, 5]
    palette = [RED, BLUE, LG, AMB, '#8E44AD']
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), facecolor='white')

    # Donut
    wedges, texts, autotexts = ax1.pie(
        counts, labels=None, autopct='%1.0f%%', startangle=90,
        colors=palette, pctdistance=0.72,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5))
    for at in autotexts:
        at.set_fontsize(8); at.set_color('white'); at.set_fontweight('bold')
    ax1.set_title('Cause Distribution', fontsize=9.5, fontweight='bold', color=DG)
    handles = [mpatches.Patch(color=c, label=f'{l} ({n})')
               for c,l,n in zip(palette,['Electrocution','Suspected Drowning','Natural/Old Age',
                                          'Fall/Trauma','Other'], counts)]
    ax1.legend(handles=handles, fontsize=7.2, loc='lower center',
               bbox_to_anchor=(0.5,-0.18), ncol=2, framealpha=0.4)

    # Horizontal bar
    y = np.arange(len(causes))
    bars = ax2.barh(y, counts, color=palette, alpha=0.85, edgecolor='white')
    for b in bars:
        w_ = b.get_width()
        ax2.text(w_+0.3, b.get_y()+b.get_height()/2,
                 f'{int(w_)}  ({int(w_/49*100)}%)',
                 va='center', fontsize=8, color=SL)
    ax2.set_yticks(y)
    ax2.set_yticklabels(['Electrocution','Drowning','Natural/\nOld Age','Fall/Trauma','Other'],
                         fontsize=8)
    ax2.set_xlabel('Deaths', fontsize=8)
    ax2.set_title('Count by Cause (n=49)', fontsize=9.5, fontweight='bold', color=DG)
    ax2.set_xlim(0, 30)
    ax2.spines[['top','right']].set_visible(False)
    ax2.set_facecolor('#F7FAF8')
    ax2.grid(axis='x', linestyle='--', alpha=0.4, color=MGR)
    fig.tight_layout(pad=1.5)
    return fig_to_rl(fig, WC, 185)

# 4. Age profile horizontal bar
def chart_age():
    groups  = ['Old (55+ yr)','Adult (30–55 yr)','Sub-adult\n(15–30 yr)','Juvenile\n(2–15 yr)','Calf (0–2 yr)']
    counts  = [5, 11, 2, 5, 23]
    palette = [LG, MG, AMB, '#E67E22', RED]
    fig, ax = plt.subplots(figsize=(6.5, 2.8), facecolor='white')
    bars = ax.barh(groups, counts, color=palette, alpha=0.85, edgecolor='white', height=0.55)
    for b in bars:
        w = b.get_width()
        ax.text(w+0.3, b.get_y()+b.get_height()/2,
                f'{int(w)}  ({int(w/46*100)}%)',
                va='center', fontsize=8.5, color=SL)
    ax.set_xlim(0, 28)
    ax.set_xlabel('Number of Deaths', fontsize=8)
    setup_ax(ax, 'Age-Group Distribution of Elephant Deaths (n=46 age-confirmed)')
    ax.spines[['top','right']].set_visible(False)
    ax.set_facecolor('#F7FAF8')
    ax.grid(axis='x', linestyle='--', alpha=0.4, color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 160)

# 5. Sex donut pair
def chart_sex():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 2.8), facecolor='white')

    # Males — cause breakdown
    mc = [11, 6, 3, 3]; ml = ['Electrocution\n(11)','Drowning\n(6)','Falls\n(3)','Other\n(3)']
    mpal = [RED, BLUE, AMB, LG]
    ax1.pie(mc, labels=ml, colors=mpal, startangle=90,
            wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5),
            textprops=dict(fontsize=7.5), labeldistance=1.15)
    ax1.set_title('Males — 23 deaths\n(52%)', fontsize=9, fontweight='bold', color=DG)

    # Females — cause breakdown
    fc = [7, 5, 3, 7]; fl = ['Electrocution\n(7)','Drowning\n(5)','Natural/Old\n(3)','Calves\n(12)']
    ax2.pie([7,5,3,8], labels=['Electrocution\n(7)','Drowning\n(5)','Natural\n(3)','Other/Calf\n(8)'],
            colors=[RED, BLUE, LG, AMB], startangle=90,
            wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5),
            textprops=dict(fontsize=7.5), labeldistance=1.15)
    ax2.set_title('Females — 22 deaths\n(49%)', fontsize=9, fontweight='bold', color=DG)

    fig.suptitle('Sex-wise Cause of Death Profile', fontsize=10, fontweight='bold', color=DG, y=1.02)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 175)

# 6. Seasonal line chart
def chart_seasonal():
    months  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    total   = [6, 4, 3, 2, 5, 5, 1, 1, 3, 8, 6, 5]
    drown   = [3, 0, 1, 0, 4, 1, 0, 0, 0, 1, 2, 2]
    elec    = [2, 0, 2, 1, 0, 1, 1, 1, 2, 7, 1, 2]
    x = np.arange(len(months))

    fig, ax = plt.subplots(figsize=(7.2, 3.2), facecolor='white')
    ax.fill_between(x, total, alpha=0.12, color=LG)
    ax.plot(x, total, '-o', color=MG, linewidth=2, markersize=5, label='Total Deaths')
    ax.plot(x, drown, '-s', color=BLUE, linewidth=1.6, markersize=5,
            linestyle='--', label='Drowning')
    ax.plot(x, elec,  '-^', color=RED, linewidth=1.6, markersize=5,
            linestyle='--', label='Electrocution')

    for i,(t,d,e) in enumerate(zip(total,drown,elec)):
        if t:  ax.annotate(str(t),(i,t),textcoords='offset points',xytext=(0,6),
                            ha='center',fontsize=7.5,color=MG,fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=8.5)
    ax.legend(fontsize=8, framealpha=0.5)
    setup_ax(ax, 'Monthly Distribution of Elephant Deaths — Seasonal Pattern', ylabel='Deaths')
    ax.set_ylim(0, 11)
    ax.axvspan(8.5, 11.5, alpha=0.07, color=RED, label='Elec peak')
    ax.axvspan(-0.5, 4.5, alpha=0.07, color=BLUE, label='Drown peak')
    ax.text(1.8,  9.5, 'Drowning Peak\n(Jan–May)', color=BLUE, fontsize=7.5,
            ha='center', style='italic')
    ax.text(10.0, 9.5, 'Electrocution\nPeak (Oct–Dec)', color=RED, fontsize=7.5,
            ha='center', style='italic')
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 180)

# 7. Range-wise horizontal bar (stacked)
def chart_range():
    ranges  = ['Kharsiya\n(RG)','Raigarh HQ\n(RG)','Baakaaruma\n(DH)',
               'Lailungaan\n(DH)','Borojh\n(DH)','Tamanar\n(RG)',
               'Dharamjaigarh\nHQ (DH)','Chhal\n(DH)','Ghargoda\n(RG)']
    elec    = [0, 0, 1, 0, 1, 4, 5, 5, 7]
    drown   = [1, 1, 0, 0, 0, 1, 0, 6, 5]
    other   = [0, 0, 0, 2, 3, 0, 2, 3, 3]
    y = np.arange(len(ranges))

    fig, ax = plt.subplots(figsize=(7, 4), facecolor='white')
    b1 = ax.barh(y, elec,  color=RED,  alpha=0.82, label='Electrocution', edgecolor='white')
    b2 = ax.barh(y, drown, left=elec, color=BLUE, alpha=0.82, label='Drowning', edgecolor='white')
    left2 = [e+d for e,d in zip(elec,drown)]
    b3 = ax.barh(y, other, left=left2, color=LG,  alpha=0.82, label='Other', edgecolor='white')

    totals = [e+d+o for e,d,o in zip(elec,drown,other)]
    for i,t in enumerate(totals):
        ax.text(t+0.15, i, f'  {t}', va='center', fontsize=8.5, fontweight='bold', color=SL)

    ax.set_yticks(y); ax.set_yticklabels(ranges, fontsize=8)
    ax.set_xlabel('Number of Deaths', fontsize=8)
    ax.legend(fontsize=8, framealpha=0.5, loc='lower right')
    setup_ax(ax, 'Range-wise Elephant Deaths — Stacked by Cause')
    ax.set_xlim(0, 20); ax.set_facecolor('#F7FAF8')
    ax.grid(axis='x', linestyle='--', alpha=0.4, color=MGR)
    ax.spines[['top','right']].set_visible(False)
    ax.axhline(6.5, color=RED, linewidth=0.8, linestyle=':', alpha=0.6)
    ax.text(16, 7.5, 'CRITICAL\nZones', color=RED, fontsize=7.5, style='italic')
    fig.tight_layout()
    return fig_to_rl(fig, WC, 210)

# 8. Division comparison bar
def chart_division():
    divs = ['Dharamjaigarh', 'Raigarh']
    elep = [27, 22]
    hum  = [36, 9]
    x = np.arange(2); w = 0.32
    fig, ax = plt.subplots(figsize=(5, 3), facecolor='white')
    b1 = ax.bar(x-w/2, elep, w, label='Elephant Deaths', color=MG, alpha=0.85)
    b2 = ax.bar(x+w/2, hum,  w, label='Human Deaths',    color=RED, alpha=0.75)
    for b in [*b1, *b2]:
        h = b.get_height()
        ax.text(b.get_x()+b.get_width()/2, h+0.5, str(int(h)),
                ha='center', fontsize=9, fontweight='bold', color=SL)
    ax.set_xticks(x); ax.set_xticklabels(divs, fontsize=9.5)
    ax.legend(fontsize=8.5, framealpha=0.5)
    setup_ax(ax, 'Division-wise Casualty Comparison', ylabel='Deaths')
    ax.set_ylim(0, 45); ax.set_facecolor('#F7FAF8')
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=MGR)
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    return fig_to_rl(fig, WC*0.65, 155)

# 9. PM cause distribution
def chart_pm_cause():
    causes = ['Electrocution','Suspected\nDrowning','Natural/\nOld Age','Trauma/\nFall','Other']
    pcts   = [49, 22, 12, 12, 5]
    palette= [RED, BLUE, LG, AMB, '#8E44AD']
    fig, ax = plt.subplots(figsize=(4.5, 3), facecolor='white')
    bars = ax.bar(causes, pcts, color=palette, alpha=0.85, edgecolor='white', width=0.55)
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x()+b.get_width()/2, h+0.5, f'{int(h)}%',
                ha='center', fontsize=9, fontweight='bold', color=SL)
    setup_ax(ax, 'PM-Confirmed Cause Distribution (%)', ylabel='% of PM records')
    ax.set_ylim(0, 58); ax.set_facecolor('#F7FAF8')
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=MGR)
    ax.spines[['top','right']].set_visible(False)
    ax.tick_params(axis='x', labelsize=8)
    fig.tight_layout()
    return fig_to_rl(fig, WC*0.65, 155)

# 10. Drowning seasonality bar
def chart_drown_season():
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    drown  = [3, 0, 1, 0, 4, 1, 0, 0, 0, 1, 2, 2]
    elec   = [2, 0, 2, 1, 0, 1, 1, 1, 2, 7, 1, 2]
    x = np.arange(12); w = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 3), facecolor='white')
    b1 = ax.bar(x-w/2, drown, w, label='Suspected Drowning', color=BLUE, alpha=0.82, edgecolor='white')
    b2 = ax.bar(x+w/2, elec,  w, label='Electrocution',      color=RED,  alpha=0.82, edgecolor='white')
    for b in [*b1,*b2]:
        h = b.get_height()
        if h:
            ax.text(b.get_x()+b.get_width()/2, h+0.1, str(int(h)),
                    ha='center', fontsize=7.5, color=SL)
    ax.set_xticks(x); ax.set_xticklabels(months, fontsize=8.5)
    ax.legend(fontsize=8.5, framealpha=0.5)
    setup_ax(ax, 'Season-wise Drowning vs Electrocution Deaths', ylabel='Deaths')
    ax.set_ylim(0, 9.5); ax.set_facecolor('#F7FAF8')
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=MGR)
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 165)

# ── Page decorators ────────────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(DG))
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor(MG))
    canvas.rect(0, H*0.60, W, 5, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor(LG))
    canvas.rect(0, H*0.60-3, W, 3, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor(MG))
    canvas.rect(0, 0, W, 50, fill=1, stroke=0)
    canvas.restoreState()

def normal_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(DG))
    canvas.rect(0, H-28, W, 28, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor(LG))
    canvas.rect(0, H-31, W, 3, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 7.5)
    canvas.drawString(36, H-19,
        'Workshop on Essentials of Mortality Investigation of Asian Elephant — Bilaspur 2026')
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(W-36, H-19, 'Illustrated Notes with Data Analysis')
    canvas.setFillColor(colors.HexColor(DG))
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor(PG))
    canvas.setFont('Helvetica', 7.5)
    canvas.drawString(36, 7, 'Chhattisgarh Forest Dept. · WII Dehradun · ICAR-IVRI')
    canvas.drawRightString(W-36, 7, f'Page {doc.page}')
    canvas.restoreState()

def on_page(canvas, doc):
    if doc.page == 1:
        cover_bg(canvas, doc)
    else:
        normal_page(canvas, doc)

# ══════════════════════════════════════════════════════════════════════════════
#  BUILD STORY
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ─── COVER ────────────────────────────────────────────────────────────────────
story += [
    SP(110),
    Paragraph('Workshop on Essentials of Mortality<br/>Investigation of Asian Elephant', COVER_T),
    SP(14),
    Paragraph('Illustrated Notes with Data Analysis &amp; Charts', COVER_S),
    SP(8),
    Paragraph('5<sup>th</sup>–6<sup>th</sup> June 2026', COVER_D),
    SP(22),
    Paragraph('Dharamjaigarh &amp; Raigarh Van Mandals · Bilaspur Forest Circle · Chhattisgarh',
              sty('CI', fontSize=11, textColor=colors.HexColor(PG), leading=16, alignment=TA_CENTER)),
    SP(28),
    Paragraph('<b>Organised by:</b> Chhattisgarh Forest Department<br/>'
              '<b>Technical Support:</b> Wildlife Institute of India, Dehradun<br/>'
              '<b>Laboratory Partner:</b> ICAR-IVRI, Izatnagar  ·  NDVSU, Jabalpur',
              sty('OG', fontSize=10, textColor=colors.HexColor(LG), leading=17, alignment=TA_CENTER)),
    PageBreak(),
]

# ─── SECTION 1: WORKSHOP OVERVIEW ────────────────────────────────────────────
story += [
    section_banner('1.  Workshop Overview'),
    SP(8),
    Paragraph('1.1  Context &amp; Participants', CH2),
    P('This two-day workshop was convened by the <b>Chhattisgarh Forest Department</b> in '
      'partnership with the <b>Wildlife Institute of India (WII), Dehradun</b> to strengthen '
      'technical capacity in elephant mortality investigation across the Bilaspur Forest Circle. '
      'It brought together <b>84 participants</b> from the Forest Department and Veterinary '
      'Service Department of Chhattisgarh State.'),
    SP(4),
    Paragraph('1.2  Objectives', CH2),
    B('<b>Biology, Behaviour &amp; Disease</b> — Comprehensive understanding of elephant biology, behaviour and major fatal diseases.'),
    B('<b>Necropsy, Biosafety &amp; Sample Handling</b> — Hands-on competency in field necropsy under biosafety and biosecurity protocols.'),
    B('<b>Surveillance, Disposal &amp; Remediation</b> — Operational frameworks for active/passive health surveillance, carcass disposal and site decontamination.'),
    SP(4),
    Paragraph('1.3  Expected Outcomes', CH2),
    B('<b>Field Necropsy Skills</b> — Position and systematically eviscerate heavy elephant carcasses in remote settings.'),
    B('<b>Sample &amp; Lab Protocols</b> — Tissue fixative formulation and secure packaging for histopathology, toxicology and microbiology.'),
    B('<b>Surveillance &amp; Forensics</b> — Field-validated disposal protocols, standardised forensic reporting and proactive health monitoring.'),
    SP(10),
]

# ─── SECTION 2: POPULATION STATUS ────────────────────────────────────────────
story += [
    section_banner('2.  Elephant Population Status — Chhattisgarh'),
    SP(8),
    Paragraph('2.1  Population Growth Trend (2001–2026)', CH2),
    P('The elephant population in Chhattisgarh has grown from a founding dispersal of '
      '<b>24 individuals</b> (2001) to an estimated <b>451 elephants</b> in 2026 — '
      'a compound annual growth rate (CAGR) of ~13% over 25 years. '
      'Bilaspur Circle hosts the largest concentration.'),
    SP(6),
    chart_population(),
    Paragraph('Figure 1: Elephant population trend 2001–2026 (Source: WII Census &amp; CG Forest Dept. Estimates)', CAP),
    SP(6),
    dtable(
        ['Year', 'Population', 'Notes'],
        [['2001','24','Founding dispersal from Odisha/Jharkhand'],
         ['2005','123','First major census count'],
         ['2015','247','Significant increase'],
         ['2021','279','Official Census (CAGR ~10% since 2005)'],
         ['2026','~451 est.','Net +172 over 5-year study period']],
        [22*mm, 28*mm, WC-50*mm]
    ),
    SP(4),
    highlight_box('2025-26 records the highest single-year human-elephant conflict events in the '
                  'five-year study period. Bilaspur Circle hosts the highest elephant density in CG.'),
    PageBreak(),
]

# ─── SECTION 3: CASUALTY OVERVIEW ────────────────────────────────────────────
story += [
    section_banner('3.  Elephant Casualties — Five-Year Overview (2021–2026)'),
    SP(8),
    Paragraph('3.1  Year-wise Deaths — Division Comparison', CH2),
    P('<b>49 confirmed elephant deaths</b> across five study years plus ongoing 2026-27 data. '
      'Dharamjaigarh (DH) division accounts for 27 deaths; Raigarh (RG) division for 22.'),
    SP(6),
    chart_yearly_deaths(),
    Paragraph('Figure 2: Year-wise elephant deaths by division. Bars show DH (green), RG (amber), Total (grey).', CAP),
    SP(4),
    dtable(
        ['Year','DH Division','RG Division','Total','Notable'],
        [['2021-22','4','0','4','All DH'],
         ['2022-23','6','6','12','RG emerges; first cluster year'],
         ['2023-24','6','0','6','DH dominant'],
         ['2024-25','6','4','10','Both divisions active'],
         ['2025-26','1','11','12','★ RECORD — RG peak'],
         ['2026-27*','4','1','5','Ongoing — all calves, all drowning'],
         ['TOTAL','27','22','49','5+ year study period']],
        [22*mm, 28*mm, 28*mm, 18*mm, WC-96*mm]
    ),
    SP(6),
    alert_box('⚠  2026-27 early signal: 5 deaths in first 3 months — all calves, all suspected drowning. '
              'Immediate field intervention required before peak dry-season period.'),
    SP(8),

    Paragraph('3.2  Division-wise Elephant vs Human Casualties', CH2),
    SP(4),
]

# Side-by-side: division chart + PM chart
div_img = chart_division()
pm_img  = chart_pm_cause()
pair_tbl = Table([[div_img, pm_img]], colWidths=[WC*0.52, WC*0.48])
pair_tbl.setStyle(TableStyle([
    ('VALIGN',  (0,0),(-1,-1), 'MIDDLE'),
    ('LEFTPADDING',  (0,0),(-1,-1), 0),
    ('RIGHTPADDING', (0,0),(-1,-1), 0),
]))
story += [
    pair_tbl,
    Paragraph('Figure 3 (left): Division-wise deaths. Figure 4 (right): PM-confirmed cause distribution.', CAP),
    SP(4),
    dtable(
        ['Division','Elephant Deaths','Human Deaths'],
        [['Dharamjaigarh','27','36'],['Raigarh','22','9'],['TOTAL','49','45']],
        [45*mm, 40*mm, WC-85*mm]
    ),
    PageBreak(),
]

# ─── SECTION 4: CAUSE OF DEATH ────────────────────────────────────────────────
story += [
    section_banner('4.  Cause of Death Analysis'),
    SP(8),
    chart_cause(),
    Paragraph('Figure 5: Cause of death — donut chart (left) and count with percentages (right). n = 49 deaths.', CAP),
    SP(6),
    dtable(
        ['Cause of Death','Count','%','Key Risk Factor / Mechanism'],
        [['Electrocution','23','47%','Illegal/low-hung power lines near crop fields; multi-simultaneous events in 3 cases'],
         ['Suspected Drowning','13','27%','Dams, ponds, seasonal nalas; 92% are calves / young'],
         ['Natural / Old Age','4','8%','Senescence; female-skewed (4F:1M)'],
         ['Fall / Trauma','4','8%','Hills, nalas, inter-elephant infighting'],
         ['Other (heat/sun)','5','10%','Heatstroke, weakness, undetermined']],
        [44*mm, 18*mm, 14*mm, WC-76*mm]
    ),
    SP(6),
    highlight_box('Electrocution (47%) + Suspected Drowning (27%) = 74% of all deaths. Both are '
                  'preventable with targeted infrastructure and field intervention.'),
    SP(8),
    Paragraph('4.1  PM-Confirmed Cause Notes', CH2),
    B('<b>20 PM records (49%)</b> confirm electrocution as cause of cardio-respiratory failure.'),
    B('Three cases show <b>multiple simultaneous electrocution events</b> — evidence of persistent illegal installations.'),
    B('<b>9 PM records (22%)</b> confirm suspected drowning; diatom test positive in all tested cases — confirmatory for ante-mortem drowning.'),
    PageBreak(),
]

# ─── SECTION 5: DEMOGRAPHICS ─────────────────────────────────────────────────
story += [
    section_banner('5.  Demographic Analysis — Age &amp; Sex Profile'),
    SP(8),
    Paragraph('5.1  Age Group Distribution', CH2),
    P('<b>50% of all deaths are calves (0–2 yr)</b> — the highest single age class. '
      'Combined with juveniles, <b>61% of deaths occur in individuals under 15 years</b>, '
      'posing a direct threat to long-term population viability.'),
    SP(5),
    chart_age(),
    Paragraph('Figure 6: Age-group distribution of elephant deaths (n=46 age-confirmed). '
              'Calf class (red) accounts for half of all deaths.', CAP),
    SP(6),
    dtable(
        ['Age Class','Count','%','Conservation Significance'],
        [['Calf (0–2 yr)','23','50%','HIGHEST single class — critical population concern'],
         ['Juvenile (2–15 yr)','5','11%','61% deaths under 15 yr combined'],
         ['Sub-adult (15–30 yr)','2','4%','Low — transitional phase'],
         ['Adult (30–55 yr)','11','24%','Electrocution primary; prime breeding cohort affected'],
         ['Old (55+ yr)','5','11%','Female-skewed longevity']],
        [45*mm, 18*mm, 14*mm, WC-77*mm]
    ),
    SP(8),
    Paragraph('5.2  Sex Profile', CH2),
    SP(4),
    chart_sex(),
    Paragraph('Figure 7: Sex-wise cause breakdown — males (left) and females (right). n = 45 sex-confirmed.', CAP),
    SP(6),
    dtable(
        ['Sex','Count','%','Key Patterns'],
        [['Male','23','52%','Wider age range (5–80 yr); electrocution highest (11 deaths)'],
         ['Female','22','49%','Concentrated at extremes — 12 calves + 4 old; 55% of calf deaths female']],
        [18*mm, 18*mm, 14*mm, WC-50*mm]
    ),
    SP(4),
    B('<b>Calf sex skew:</b> 55% of calf deaths are female. In Raigarh, 8 of 11 drowning deaths are young females (6 months–2 yr).'),
    B('<b>Male electrocution risk:</b> 48% of male deaths are electrocution vs 33% for females — males range farther into agricultural zones.'),
    B('<b>Female longevity:</b> More females survive to 55+ yr (4F vs 1M) — a natural pattern consistent with elephant biology.'),
    PageBreak(),
]

# ─── SECTION 6: SEASONAL ANALYSIS ────────────────────────────────────────────
story += [
    section_banner('6.  Seasonal Variation — Monthly &amp; Cause Patterns'),
    SP(8),
    Paragraph('6.1  Monthly Death Distribution', CH2),
    P('<b>October is the deadliest month</b> with 8 deaths, driven almost entirely by '
      'electrocution. The Oct–Dec window accounts for 42% of annual deaths. '
      'A secondary drowning peak occurs Jan–May during the dry season.'),
    SP(5),
    chart_seasonal(),
    Paragraph('Figure 8: Monthly distribution of total deaths (green), drowning (blue dashed), '
              'electrocution (red dashed). Shaded zones mark seasonal peaks.', CAP),
    SP(6),
    Paragraph('6.2  Season-wise Cause Breakdown', CH2),
    SP(4),
    chart_drown_season(),
    Paragraph('Figure 9: Monthly drowning vs electrocution deaths — highlighting opposing seasonal peaks.', CAP),
    SP(6),
    dtable(
        ['Season','Drowning','Electrocution','Key Driver'],
        [['Jan–May (Dry)','8 deaths (62%)','6 deaths (30%)','Low water, steep banks trap calves; crop fields quiet'],
         ['Jun–Sep (Monsoon)','1 death (8%)','5 deaths (25%)','Nalas swell; some fencing active'],
         ['Oct–Dec (Harvest)','4 deaths (31%)','10 deaths (50%)','Crop protection fencing at peak; post-monsoon movement']],
        [32*mm, 30*mm, 35*mm, WC-97*mm]
    ),
    SP(6),
    highlight_box('Drowning intervention window: Jan–May (62% of drowning deaths).  '
                  'Electrocution intervention window: Oct–Dec (50% of electrocution deaths).  '
                  'Targeting these seasonal windows maximises intervention impact.'),
    PageBreak(),
]

# ─── SECTION 7: RANGE-WISE ────────────────────────────────────────────────────
story += [
    section_banner('7.  Range-wise &amp; Geo Distribution'),
    SP(8),
    Paragraph('7.1  Range-wise Casualty Hotspots', CH2),
    P('Chhal (DH) and Ghargoda (RG) together account for <b>29 of 49 deaths (59%)</b>, '
      'making them CRITICAL intervention zones. Both show a mixed electrocution-drowning profile.'),
    SP(5),
    chart_range(),
    Paragraph('Figure 10: Range-wise deaths stacked by cause — electrocution (red), drowning (blue), other (green). '
              'Dashed line separates CRITICAL zones.', CAP),
    SP(6),
    dtable(
        ['Range / Beat','Division','Total','Risk','Elec','Drown','Other'],
        [['Ghargoda','Raigarh','15','CRITICAL','7','5','3'],
         ['Chhal','Dharamjaigarh','14','CRITICAL','5','6','3'],
         ['Dharamjaigarh HQ','Dharamjaigarh','7','HIGH','5','0','2'],
         ['Tamanar','Raigarh','5','MODERATE','4','1','0'],
         ['Borojh','Dharamjaigarh','4','HIGH','1','0','3'],
         ['Lailungaan','Dharamjaigarh','2','HIGH','0','0','2'],
         ['Baakaaruma','Dharamjaigarh','1','MODERATE','1','0','0'],
         ['Raigarh HQ + Kharsiya','Raigarh','2','LOW','0','2','0']],
        [38*mm, 38*mm, 18*mm, 25*mm, 15*mm, 18*mm, WC-152*mm]
    ),
    SP(4),
    Paragraph('7.2  Human Casualty Hotspots', CH2),
    dtable(
        ['Range / Beat','Division','Human Deaths'],
        [['Chhal (DH)','Dharamjaigarh','10'],
         ['Borojh (DH)','Dharamjaigarh','9'],
         ['Lailungaan (DH)','Dharamjaigarh','8'],
         ['Ghargoda (RG)','Raigarh','5'],
         ['Dharamjaigarh HQ','Dharamjaigarh','5'],
         ['Others','Both','8']],
        [55*mm, 55*mm, WC-110*mm]
    ),
    SP(4),
    alert_box('IMMEDIATE ACTION: Chhal &amp; Ghargoda ranges — combined 29 elephant + 15 human deaths '
              '(59% of all elephant casualties). Multi-agency enforcement, power-line audit, '
              'and drowning infrastructure are required in these two ranges above all others.'),
    PageBreak(),
]

# ─── SECTION 8: DROWNING DEEP-DIVE ───────────────────────────────────────────
story += [
    section_banner('8.  Suspected Drowning — Detailed PM &amp; Lab Analysis'),
    SP(8),
    P('<b>13 deaths (27%)</b> attributed to suspected drowning. <b>92% of victims are calves '
      'or young individuals.</b> The drowning cases cluster in Raigarh Division (dams, nalas) '
      'and Dharamjaigarh Division (ponds).'),
    SP(6),
    Paragraph('8.1  Gross Post-mortem Findings — All 13 Cases', CH2),
    dtable(
        ['PM Finding','Frequency / Notes'],
        [['Frothy nasal/oral discharge — emphysema aquosum','ALL CASES — pathognomonic for drowning'],
         ['Lungs — waterlogged, heavy, congested, oedematous','ALL CASES'],
         ['Water in trachea &amp; bronchi','ALL CASES'],
         ['Gastric content — large volume of water &amp; plant debris','ALL CASES'],
         ['Skin maceration / hide wrinkling','CONSISTENT — prolonged water immersion'],
         ['Petechial haemorrhages — conjunctiva / sub-pleural','VARIABLE']],
        [WC*0.55, WC*0.45]
    ),
    SP(6),
    Paragraph('8.2  Histopathology — Microscopic Confirmation', CH2),
    B('Pulmonary oedema — alveolar flooding with eosinophilic fluid.'),
    B('Pulmonary haemorrhage — interstitial and alveolar spaces.'),
    B('Hepatocyte degeneration — confirmed in <b>3 cases</b> (Tamnar Range, December 2025).'),
    B('<b>Diatom test POSITIVE</b> — confirmatory for ante-mortem (alive when entered water) drowning in all tested cases.'),
    B('Renal congestion — passive vascular engorgement.'),
    SP(6),
    alert_box('⚠  ARSENIC DETECTED — ICAR-IVRI Lab Report (File F.2-19/DI/NRC/2025-26/CWL)\n'
              'Arsenic at elevated levels in visceral samples from 2 specimens, Tamnar Range '
              '(Raigarh Division), December 2025. Histopathology confirmed hepatocyte degeneration. '
              'Arsenic likely a contributing metabolic stress factor from contaminated dam water near '
              'industrial corridor. Environmental sampling of Rabo / Panikshet dam catchments '
              'RECOMMENDED IMMEDIATELY.'),
    SP(6),
    Paragraph('8.3  Toxicology — Negative Findings (5 tested batches)', CH2),
    dtable(
        ['Toxin Screened','Result'],
        [['EEHV-I (Elephant Endotheliotropic Herpesvirus)','NEGATIVE — confirmed by ICAR-IVRI &amp; NDVSU Jabalpur'],
         ['Nitrate-Nitrite compounds','NEGATIVE'],
         ['Organochlorine &amp; Organophosphate insecticides','NEGATIVE'],
         ['Heavy metals (Lead, Mercury, Cadmium)','NEGATIVE'],
         ['Hydrogen Cyanide (HCN)','NEGATIVE']],
        [WC*0.55, WC*0.45]
    ),
    SP(4),
    highlight_box('EEHV-negative result is particularly significant given the high neonate mortality. '
                  'Viral haemorrhagic disease is ruled out as a contributing cause.'),
    PageBreak(),
]

# ─── SECTION 9: PROGRAMME & RESOURCE PERSONS ─────────────────────────────────
story += [
    section_banner('9.  Workshop Programme &amp; Resource Persons'),
    SP(8),
    Paragraph('9.1  Resource Persons', CH2),
    SP(4),
    dtable(
        ['Name','Institution','Expertise'],
        [['Dr. A. B. Shrivastav','NDVSU, Jabalpur','Wildlife Health, Forensics, Veterinary Pathology'],
         ['Dr. Parag Nigam','WII, Dehradun','Wildlife Health, Chemical Capture, Conservation Medicine'],
         ['Dr. Karikalan Mathesh','ICAR-IVRI, Bareilly','Wildlife Pathology, Histopathology, Molecular Diagnosis'],
         ['Dr. Tapendra Saini','WII, Dehradun','Animal Genetics, Conservation Breeding, Wildlife Genetics'],
         ['Dr. Chandra Prakash Sharma','WII, Dehradun','Wildlife Forensics, Morphological ID, Crime-Scene Management']],
        [52*mm, 52*mm, WC-104*mm]
    ),
    SP(8),
    Paragraph('9.2  Two-Day Programme at a Glance', CH2),
    SP(4),
    dtable(
        ['Time','Session','Faculty'],
        [['DAY 1 — 30 May 2026','',''],
        ['10:00–11:00','Inauguration','—'],
        ['11:00–11:30','Elephant Status &amp; Human-Elephant Interface in Chhattisgarh','PP, AM'],
        ['11:30–12:15','Biological &amp; Anatomical Aspects of Elephants','PN'],
        ['12:15–13:00','Understanding Wildlife Mortalities: Veterinary Perspective','PN'],
        ['14:00–15:30','Infectious Causes of Mortality (EEHV, FMD, TB, Anthrax, HS)','KM, ABS'],
        ['15:30–16:30','Non-Infectious &amp; Disaster Mortalities (Electrocution, Lightning, Train)','ABS, KM'],
        ['16:30–17:30','Non-Infectious Diseases (Mycotoxicosis, Kodo Millet, Bio-toxins)','KM, PN'],
        ['DAY 2 — 31 May 2026','',''],
        ['09:30–10:15','Biosafety &amp; Biosecurity in Elephant Mortality','KM, TS, PN'],
        ['10:15–11:00','Equipment Familiarization &amp; Site Preparation','ABS, KM, TS'],
        ['11:30–12:30','Comprehensive Sampling Protocols (tissue, cold chain, documentation)','KM, ABS, TS'],
        ['12:30–13:00','Recording Information During Necropsy','KM, ABS'],
        ['14:00–14:45','Vetro-Legal &amp; Forensic Aspects','CP'],
        ['14:45–16:00','Practical: Crime Scene Investigation &amp; Ivory/Tusk Extraction','CP, PN, TS'],
        ['16:15–16:45','Panel Discussion','All faculty'],
        ['16:45–17:30','Valedictory','—']],
    ),
    SP(4),
    Paragraph('<i>Faculty: ABS=Dr.Shrivastav · PN=Dr.Nigam · KM=Dr.Karikalan · '
              'TS=Dr.Saini · CP=Dr.C.P.Sharma · PP=Paras Patel · AM=Asst.Manager</i>', SM),
    PageBreak(),
]

# ─── SECTION 10: CASE STUDY ──────────────────────────────────────────────────
story += [
    section_banner('10.  Case Study — Gurda Calf Drowning · 01 June 2026'),
    SP(8),
    info_table([
        ('Date',        '01 June 2026'),
        ('Location',    'Gurda, Kharsia Range, Raigarh Van Mandal'),
        ('GPS',         '22.0439°N, 83.1313°E  (22°3′16″N 83°8′11″E)'),
        ('Elevation',   '256.04 ± 9.59 m'),
        ('Water Body',  'Gurda River / exposed sandbank'),
        ('Species',     'Asian Elephant (Elephas maximus)'),
        ('Age Class',   'Calf (0–2 yr)'),
        ('Sex',         'Not confirmed'),
        ('Cause',       'Suspected Drowning'),
    ]),
    SP(6),
    Paragraph('10.1  Field Observations', CH2),
    P('The calf was found on an exposed sandbank adjacent to the Gurda River in Kharsia Range. '
      'Photographic documentation was secured at 10:56 hrs (aerial view, 06-01-2026) and '
      '11:03 hrs (ground-level carcass view). The incident is consistent with the established '
      'dry-season drowning pattern — when water levels are low and riverbanks are steep, '
      'young calves approaching the water edge to drink can fall in and are unable to '
      'climb out independently.'),
    SP(4),
    P('<i>Original field note: हाथी निगरानी परिसर गुर्दा — Gurda परिक्षेत्र, खरसिया वनमण्डल रायगढ़।</i>'),
    SP(6),
    alert_box('This case represents the 2026-27 cohort trend — all 5 deaths in the current year '
              '(first 3 months only) are calves, all suspected drowning. The Gurda case is the '
              'southernmost recorded drowning event in Raigarh Division (22.04°N).'),
    SP(10),
]

# ─── SECTION 11: RECOMMENDATIONS ─────────────────────────────────────────────
story += [
    section_banner('11.  Key Findings &amp; Recommendations'),
    SP(8),
    Paragraph('11.1  Summary Statistics', CH2),
    SP(4),
    dtable(
        ['Metric','Value'],
        [['Study Period','2021-22 to 2026-27 (ongoing)'],
         ['Total Elephant Deaths','49 confirmed'],
         ['Leading Cause','Electrocution — 23 deaths (47%)'],
         ['Second Cause','Suspected Drowning — 13 deaths (27%)'],
         ['Most Vulnerable Age','Calves 0–2 yr — 23 deaths (50%)'],
         ['Deadliest Year','2025-26 — 12 deaths (record)'],
         ['2026-27 Early Signal','5 deaths in first 3 months — all calves, all drowning'],
         ['Critical Hotspots','Chhal (14) + Ghargoda (15) = 59% of all elephant deaths'],
         ['Drowning Seasonality','Jan–May = 62% of drowning deaths'],
         ['Electrocution Seasonality','Oct–Dec = 50% of electrocution deaths'],
         ['Arsenic Finding','Detected in 2 specimens — Tamnar Range, Dec 2025'],
         ['EEHV Status','Negative — all batches tested'],
         ['Toxicology','Negative — nitrates, organophosphates, heavy metals, HCN'],
         ['Workshop Participants','84 (Forest Dept + Veterinary Service Dept, CG)']],
        [WC*0.46, WC*0.54]
    ),
    SP(8),
    Paragraph('11.2  Priority Action Items', CH2),
    SP(4),
    B('<b>[IMMEDIATE] Environmental sampling</b> — Rabo &amp; Panikshet dam catchments (arsenic detection follow-up).'),
    B('<b>[IMMEDIATE] Drowning infrastructure</b> — earthen ramps/exit points at high-risk dam edges in Chhal &amp; Ghargoda.'),
    B('<b>[IMMEDIATE] Power-line audit</b> — survey of low-hung lines in all elephant corridors in critical ranges.'),
    B('<b>[Oct–Dec campaign]</b> — enforcement blitz on illegal crop-protection electric fencing during harvest season.'),
    B('<b>[Jan–May campaign]</b> — dry-season calf monitoring using GPS herd data; deploying watchers near known drowning sites.'),
    B('<b>Mandatory PM within 24 hrs</b> of mortality event + sample dispatch to ICAR-IVRI within 48 hrs with cold chain.'),
    B('Annual EEHV surveillance — document negative results systematically.'),
    B('Quarterly mortality review meetings at division level with all range officers.'),
    SP(10),
    HR(DG, 1.5),
    SP(5),
    Paragraph('<i>Data Sources: Official Proforma-1 Records, Dharamjaigarh &amp; Raigarh Divisions · '
              'PM Reports: ICAR-IVRI Izatnagar (File F.2-19/DI/NRC/2025-26/CWL) · '
              'GIS Data: Bilaspur Forest Division GIS Cell · Generated: June 2026</i>', SM),
    Paragraph('<i>Organised by: Chhattisgarh Forest Department · '
              'Technical Support: WII, Dehradun · Laboratory: ICAR-IVRI &amp; NDVSU, Jabalpur</i>', SM),
]

# ── Build PDF ──────────────────────────────────────────────────────────────────
out = '/home/user/Workshop-on-Conference/Workshop_Illustrated_Notes_2026.pdf'
doc = SimpleDocTemplate(
    out, pagesize=A4,
    leftMargin=36, rightMargin=36,
    topMargin=48, bottomMargin=36,
    title='Illustrated Workshop Notes — Elephant Mortality Investigation',
    author='Chhattisgarh Forest Department / WII',
    subject='Elephant Mortality Analysis 2021-2026 with Charts',
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'PDF: {out}')
print(f'Size: {os.path.getsize(out)/1024:.1f} KB')

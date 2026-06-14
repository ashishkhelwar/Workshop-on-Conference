#!/usr/bin/env python3
"""
Illustrated workshop notes with embedded GIS maps (no internet tiles needed).
Maps rendered via matplotlib from GPS coordinate data.
"""

import os, io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse
from matplotlib.lines import Line2D
import numpy as np

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
DG='#1B4332'; MG='#2D6A4F'; LG='#52B788'; PG='#D8F3DC'
AMB='#D4870A'; RED='#C0392B'; BLUE='#2980B9'; SL='#2C3E50'
LGR='#ECF0F1'; MGR='#BDC3C7'

W, H = A4
WC   = W - 72

# ── GPS Data (from data.js) ────────────────────────────────────────────────────
DH_HUMAN = [
    [22.408,83.187,'Krondha','2021-22'],[22.347,83.237,'Gersa','2021-22'],
    [22.449,83.114,'Koylar','2021-22'],[22.774,83.165,'Anchira','2021-22'],
    [22.774,83.165,'Anchira','2021-22'],[22.582,83.171,'Balpeda','2021-22'],
    [22.700,83.046,'Ongna','2021-22'],[22.414,83.264,'Ongna','2021-22'],
    [22.731,83.137,'Jaldega','2021-22'],[22.434,83.191,'Taraimaur','2021-22'],
    [22.687,83.272,'Ratnpur','2021-22'],[22.710,83.258,'Gidhkalo','2021-22'],
    [22.236,83.279,'Bojiya','2023-24'],[22.140,83.123,'Chhal','2023-24'],
    [22.313,83.091,'Chhal','2023-24'],[22.086,83.161,'Chhal','2023-24'],
    [22.588,83.998,'Pakargaon','2023-24'],[22.440,83.264,'Hati','2024-25'],
    [22.185,83.179,'Auranaara','2024-25'],[22.338,83.196,'Kudekela','2024-25'],
    [22.750,83.543,'Tejpur','2024-25'],[22.406,83.141,'Koylar','2024-25'],
    [22.631,83.243,'Balpeda','2024-25'],[22.4995,83.4307,'Baguadega','2024-25'],
    [22.612,83.766,'Amapali','2024-25'],[22.617,84.022,'Pakargaon','2025-26'],
    [22.618,84.025,'Pakargaon','2025-26'],[22.393,83.227,'Amgaon','2025-26'],
    [22.5144,83.4287,'Rairuma','2025-26'],[22.365,83.550,'Lailenga','2025-26'],
    [22.365,83.545,'Rajaaama','2025-26'],[22.372,83.804,'Rajaaama','2025-26'],
    [22.4056,83.170,'Krondha','2025-26'],[22.631,83.243,'Khambhar','2025-26'],
    [22.440,83.264,'Chhal','2025-26'],[22.762,83.323,'Kapu','2025-26'],
]
DH_ELEPHANT = [
    [22.198,83.166,'Electrocution','2021-22'],[22.589,83.101,'Natural death','2021-22'],
    [22.397,83.257,'Electrocution','2021-22'],[22.770,83.171,'Fall from hill','2021-22'],
    [22.320,83.752,'Lightning strike','2022-23'],[22.688,83.534,'Lightning strike','2022-23'],
    [22.688,83.534,'Electrocution','2022-23'],[22.648,83.496,'Old age/fall','2022-23'],
    [22.611,83.412,'Electrocution','2022-23'],[22.355,83.413,'Natural/old age','2022-23'],
    [22.174,83.152,'Electrocution','2023-24'],[22.290,83.146,'Inter-elephant conflict','2023-24'],
    [22.731,83.321,'Electrocution','2023-24'],[22.729,83.235,'Electrocution','2023-24'],
    [22.445,83.153,'Electrocution','2023-24'],[22.580,83.241,'Electrocution','2023-24'],
    [22.259,83.173,'Calf death at birth','2024-25'],[22.660,83.354,'Tusk injury','2024-25'],
    [22.322,83.096,'Suspected Drowning','2024-25'],[22.373,83.151,'Electrocution','2024-25'],
    [22.259,83.146,'Natural death','2024-25'],[22.284,83.137,'Suspected Drowning','2024-25'],
    [22.166,83.173,'Suspected Drowning','2025-26'],
    [22.359,83.452,'Cardiovascular shock','2026-27'],[22.146,83.212,'Suspected Drowning','2026-27'],
    [22.166,83.115,'Suspected Drowning','2026-27'],[22.100,83.159,'Suspected Drowning','2026-27'],
]
RG_HUMAN = [
    [22.113,83.350,'Samaruma','2021-22'],[22.455,83.646,'Pora','2022-23'],
    [22.455,83.646,'Baturaachhar','2022-23'],[22.121,83.222,'Kafarmaar','2022-23'],
    [22.096,83.708,'Kaantajharia','2023-24'],[22.069,83.373,'Jhingol','2024-25'],
    [22.126,83.266,'Tendumudi','2024-25'],[22.497,83.585,'Baraud','2024-25'],
    [22.170,83.388,'DehriDih','2025-26'],
]
RG_ELEPHANT = [
    [22.245,83.414,'Heatstroke','2022-23'],[22.215,83.470,'Electrocution','2022-23'],
    [22.165,83.510,'Electrocution','2022-23'],[22.090,83.420,'Sun stroke','2022-23'],
    [22.179,83.518,'Electrocution','2022-23'],[22.498,83.501,'Electrocution','2022-23'],
    [22.218,83.564,'Electrocution(3)','2024-25'],[22.104,83.243,'Suspected Drowning-Panikshet','2024-25'],
    [22.198,83.468,'Suspected Drowning-Rabo','2024-25'],[22.102,83.241,'Suspected Drowning-Panikshet','2024-25'],
    [22.211,83.470,'Brain injury','2025-26'],[22.152,83.494,'Suspected Drowning','2025-26'],
    [22.202,83.418,'Electrocution','2025-26'],[22.021,83.332,'Suspected Drowning','2025-26'],
    [21.985,83.462,'Suspected Drowning','2025-26'],[22.555,83.615,'Fell in nala','2025-26'],
    [22.065,83.392,'Weakness','2025-26'],[22.181,83.455,'Electrocution(2)','2025-26'],
    [22.138,83.120,'Suspected Drowning-Mond River','2026-27'],
]

def cause_color(c):
    c = c.lower()
    if 'electro' in c or 'lightning' in c: return RED
    if 'drown' in c: return BLUE
    if 'natural' in c or 'old age' in c or 'birth' in c: return LG
    return AMB

# ── Map drawing utilities ──────────────────────────────────────────────────────
def add_north_arrow(ax, x, y, size=0.025):
    ax.annotate('', xy=(x, y+size), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5))
    ax.text(x, y+size*1.6, 'N', ha='center', va='bottom',
            fontsize=8, fontweight='bold', color='#2C3E50')

def add_scale_bar(ax, x, y, length_deg, label):
    ax.plot([x, x+length_deg], [y, y], 'k-', lw=2.5, solid_capstyle='butt')
    ax.plot([x, x], [y-0.004, y+0.004], 'k-', lw=1.5)
    ax.plot([x+length_deg, x+length_deg], [y-0.004, y+0.004], 'k-', lw=1.5)
    ax.text(x+length_deg/2, y-0.012, label, ha='center', fontsize=7, color='#2C3E50')

def map_base(ax, title='', xlim=(82.95,84.10), ylim=(21.92,22.85)):
    """Draw base map with terrain colour, grid, labels."""
    ax.set_facecolor('#E8F4E8')
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)

    # Forest/terrain fill zones (approximate)
    forest = plt.Polygon([[82.95,21.92],[84.10,21.92],[84.10,22.85],[82.95,22.85]],
                          closed=True, facecolor='#C8DFC8', edgecolor='none', zorder=0)
    ax.add_patch(forest)

    # Water bodies — approximate Mond River (meanders E-W)
    mond_x = [83.05,83.12,83.18,83.25,83.32,83.38,83.44,83.50,83.57,83.65,83.72,83.80,83.90]
    mond_y = [22.10,22.09,22.11,22.10,22.08,22.09,22.07,22.08,22.06,22.05,22.07,22.06,22.05]
    ax.plot(mond_x, mond_y, color='#5DADE2', linewidth=2.2, alpha=0.7, zorder=1, label='_')
    ax.text(83.42, 21.98, 'Mond River', color='#2980B9', fontsize=6.5, style='italic',
            ha='center', rotation=-3, zorder=5)

    # Panikshet dam (oval)
    panikshet = Ellipse((83.24,22.10), 0.06, 0.03, color='#85C1E9', alpha=0.7, zorder=2)
    ax.add_patch(panikshet)
    ax.text(83.24, 22.07, 'Panikshet\nDam', color='#1A5276', fontsize=5.5, ha='center',
            zorder=6, fontweight='bold')

    # Rabo dam
    rabo = Ellipse((83.47,22.20), 0.05, 0.025, color='#85C1E9', alpha=0.7, zorder=2)
    ax.add_patch(rabo)
    ax.text(83.47, 22.17, 'Rabo Dam', color='#1A5276', fontsize=5.5, ha='center',
            zorder=6, fontweight='bold')

    # Hasdeo River (approx, northern part)
    hasdeo_x = [83.60,83.65,83.72,83.80,83.90,84.00,84.05]
    hasdeo_y = [22.65,22.60,22.58,22.55,22.52,22.50,22.48]
    ax.plot(hasdeo_x, hasdeo_y, color='#5DADE2', linewidth=1.8, alpha=0.6, zorder=1)
    ax.text(83.85, 22.56, 'Hasdeo R.', color='#2980B9', fontsize=6, style='italic',
            rotation=-8, zorder=5)

    # Division boundary (approximate line at lon ~83.38 N-S with variation)
    div_lons = [83.37,83.38,83.40,83.39,83.38,83.37,83.35]
    div_lats = [21.93,22.05,22.20,22.35,22.50,22.65,22.82]
    ax.plot(div_lons, div_lats, '--', color='#566573', linewidth=1.8,
            alpha=0.85, zorder=3, dashes=(6,3))
    ax.text(83.39, 22.44, 'Division\nBoundary', color='#566573', fontsize=6,
            rotation=88, ha='center', zorder=5)

    # Division labels
    ax.text(83.17, 22.80, 'DHARAMJAIGARH\nDIVISION', color='#1B4332', fontsize=7.5,
            fontweight='bold', ha='center', alpha=0.5, zorder=4)
    ax.text(83.65, 22.80, 'RAIGARH\nDIVISION', color='#7B3F00', fontsize=7.5,
            fontweight='bold', ha='center', alpha=0.5, zorder=4)

    # Grid
    ax.grid(True, linestyle=':', linewidth=0.5, color='#AEB6BF', alpha=0.6, zorder=0)
    ax.tick_params(labelsize=7.5, color='#4A5568')
    ax.set_xlabel('Longitude (°E)', fontsize=8, color='#4A5568')
    ax.set_ylabel('Latitude (°N)', fontsize=8, color='#4A5568')

    # Formatting lat/lon labels
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'{v:.2f}°'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'{v:.2f}°'))

    if title:
        ax.set_title(title, fontsize=9.5, fontweight='bold', color=DG, pad=6)

    # Spines
    for spine in ax.spines.values():
        spine.set_linewidth(1.2); spine.set_edgecolor('#2C3E50')


def add_range_labels(ax):
    """Approximate range centre labels."""
    labels = [
        (22.14, 83.13, 'Chhal\n(DH)'),
        (22.70, 83.20, 'DH HQ'),
        (22.62, 83.37, 'Borojh\n(DH)'),
        (22.36, 83.42, 'Lailungaan\n(DH)'),
        (22.50, 83.25, 'Baakaaruma\n(DH)'),
        (22.20, 83.45, 'Ghargoda\n(RG)'),
        (22.28, 83.57, 'Tamanar\n(RG)'),
        (22.18, 83.24, 'Kharsiya\n(RG)'),
    ]
    for lat, lon, name in labels:
        ax.text(lon, lat, name, fontsize=5.8, ha='center', va='center',
                color='#2C3E50', alpha=0.75,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor='#AEB6BF', alpha=0.65, linewidth=0.5),
                zorder=6)

# ── Chart helper ───────────────────────────────────────────────────────────────
def fig_to_rl(fig, w, h):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=200, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0); plt.close(fig)
    return Image(buf, width=w, height=h)

# ════════════════════════════════════════════════════════════════════
#  MAP 1 — Master Casualty Map (elephant + human deaths)
# ════════════════════════════════════════════════════════════════════
def map_master():
    fig, ax = plt.subplots(figsize=(8.5, 6.5), facecolor='white')
    map_base(ax, 'Master Casualty Map — Elephant &amp; Human Deaths (2021–2026)')

    # Plot elephant deaths (colour = cause)
    for pt in DH_ELEPHANT + RG_ELEPHANT:
        c = cause_color(pt[2])
        ax.plot(pt[1], pt[0], 'o', color=c, markersize=7, alpha=0.85,
                markeredgecolor='white', markeredgewidth=0.7, zorder=8)

    # Plot human deaths (triangle markers)
    for pt in DH_HUMAN + RG_HUMAN:
        ax.plot(pt[1], pt[0], '^', color='#F39C12', markersize=6.5, alpha=0.80,
                markeredgecolor='white', markeredgewidth=0.7, zorder=8)

    add_range_labels(ax)
    add_north_arrow(ax, 83.02, 22.76)
    add_scale_bar(ax, 83.05, 21.95, 0.18, '~20 km')

    legend_elements = [
        Line2D([0],[0], marker='o', color='w', markerfacecolor=RED,
               markersize=9, markeredgecolor='white', label='Elephant — Electrocution'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=BLUE,
               markersize=9, markeredgecolor='white', label='Elephant — Drowning'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=LG,
               markersize=9, markeredgecolor='white', label='Elephant — Natural/Other'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=AMB,
               markersize=9, markeredgecolor='white', label='Elephant — Trauma/Other'),
        Line2D([0],[0], marker='^', color='w', markerfacecolor='#F39C12',
               markersize=9, markeredgecolor='white', label='Human Death'),
        Line2D([0],[0], color='#5DADE2', linewidth=2, label='River'),
        Line2D([0],[0], color='#566573', linewidth=1.5, linestyle='--', label='Division Boundary'),
        mpatches.Patch(facecolor='#85C1E9', label='Dam / Water Body'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7,
              framealpha=0.92, edgecolor='#2C3E50', fancybox=True,
              title='Legend', title_fontsize=7.5)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 310)

# ════════════════════════════════════════════════════════════════════
#  MAP 2 — Elephant deaths only, cause-coded + year labels
# ════════════════════════════════════════════════════════════════════
def map_elephant_cause():
    fig, ax = plt.subplots(figsize=(8.5, 6), facecolor='white')
    map_base(ax, 'Elephant Deaths — Cause of Death &amp; Location (2021–2027)')

    year_markers = {'2021-22':'o','2022-23':'s','2023-24':'D',
                    '2024-25':'^','2025-26':'*','2026-27*':'P'}
    year_colors  = {'2021-22':'#2ECC71','2022-23':'#3498DB','2023-24':'#9B59B6',
                    '2024-25':'#F39C12','2025-26':'#E74C3C','2026-27*':'#E74C3C'}

    for pt in DH_ELEPHANT + RG_ELEPHANT:
        yr = pt[3]
        if yr == '2026-27': yr = '2026-27*'
        c  = cause_color(pt[2])
        m  = year_markers.get(yr, 'o')
        sz = 10 if yr == '2026-27*' else 8
        ax.plot(pt[1], pt[0], m, color=c, markersize=sz, alpha=0.88,
                markeredgecolor='white', markeredgewidth=0.8, zorder=8)

    add_range_labels(ax)
    add_north_arrow(ax, 83.02, 22.76)
    add_scale_bar(ax, 83.05, 21.95, 0.18, '~20 km')

    legend_elements = [
        mpatches.Patch(facecolor=RED,  label='Electrocution / Lightning'),
        mpatches.Patch(facecolor=BLUE, label='Suspected Drowning'),
        mpatches.Patch(facecolor=LG,   label='Natural / Old Age'),
        mpatches.Patch(facecolor=AMB,  label='Trauma / Other'),
        Line2D([0],[0], color='#5DADE2', linewidth=2, label='River'),
        mpatches.Patch(facecolor='#85C1E9', label='Dam / Water Body'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=7.5,
              framealpha=0.92, edgecolor='#2C3E50', title='Cause of Death',
              title_fontsize=8)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 285)

# ════════════════════════════════════════════════════════════════════
#  MAP 3 — Drowning hotspot map with water body emphasis
# ════════════════════════════════════════════════════════════════════
def map_drowning():
    all_pts = DH_ELEPHANT + RG_ELEPHANT
    drown_pts = [p for p in all_pts if 'drown' in p[2].lower()]

    fig, ax = plt.subplots(figsize=(8.5, 6), facecolor='white')
    map_base(ax, 'Drowning Hotspot Map — All Suspected Drowning Incidents (n=13)')

    # Background dim for non-drowning deaths
    for pt in all_pts:
        if 'drown' not in pt[2].lower():
            ax.plot(pt[1], pt[0], 'o', color='#BDC3C7', markersize=5,
                    alpha=0.4, markeredgecolor='none', zorder=7)

    # Drowning incidents with year-coded color
    yr_col = {'2021-22':'#AED6F1','2022-23':'#5DADE2','2023-24':'#2E86C1',
               '2024-25':'#1A5276','2025-26':'#0B2B47','2026-27':'#FF6B35'}
    for pt in drown_pts:
        c = yr_col.get(pt[3], BLUE)
        ax.plot(pt[1], pt[0], 'o', color=c, markersize=11, alpha=0.9,
                markeredgecolor='white', markeredgewidth=1.0, zorder=9)
        ax.plot(pt[1], pt[0], 'o', color=BLUE, markersize=15, alpha=0.2,
                markeredgecolor='none', zorder=8)

    # Label each drowning incident
    for i, pt in enumerate(drown_pts):
        loc = pt[2].split('-')[0].strip().replace('Suspected Drowning','').strip()
        if loc:
            ax.annotate(f'{loc[:12]}', (pt[1], pt[0]),
                       textcoords='offset points', xytext=(6, 4),
                       fontsize=5.5, color='#1A5276', zorder=10,
                       bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                                 alpha=0.6, edgecolor='none'))

    add_range_labels(ax)
    add_north_arrow(ax, 83.02, 22.76)
    add_scale_bar(ax, 83.05, 21.95, 0.18, '~20 km')

    yr_handles = [
        mpatches.Patch(facecolor=yr_col['2021-22'], label='2021-22'),
        mpatches.Patch(facecolor=yr_col['2022-23'], label='2022-23'),
        mpatches.Patch(facecolor=yr_col['2023-24'], label='2023-24'),
        mpatches.Patch(facecolor=yr_col['2024-25'], label='2024-25'),
        mpatches.Patch(facecolor=yr_col['2025-26'], label='2025-26'),
        mpatches.Patch(facecolor=yr_col['2026-27'], label='2026-27 ★'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor='#BDC3C7',
               markersize=7, label='Other deaths (dim)'),
        Line2D([0],[0], color='#5DADE2', linewidth=2, label='River'),
        mpatches.Patch(facecolor='#85C1E9', label='Dam'),
    ]
    ax.legend(handles=yr_handles, loc='lower right', fontsize=7,
              framealpha=0.92, edgecolor='#2C3E50', title='Drowning by Year',
              title_fontsize=7.5, ncol=2)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 285)

# ════════════════════════════════════════════════════════════════════
#  MAP 4 — Electrocution hotspot map
# ════════════════════════════════════════════════════════════════════
def map_electrocution():
    all_pts = DH_ELEPHANT + RG_ELEPHANT
    elec_pts = [p for p in all_pts if 'electro' in p[2].lower() or 'lightning' in p[2].lower()]

    fig, ax = plt.subplots(figsize=(8.5, 6), facecolor='white')
    map_base(ax, 'Electrocution Hotspot Map — All Electrocution &amp; Lightning Incidents (n=23+)')

    for pt in all_pts:
        if 'electro' not in pt[2].lower() and 'lightning' not in pt[2].lower():
            ax.plot(pt[1], pt[0], 'o', color='#BDC3C7', markersize=5,
                    alpha=0.35, markeredgecolor='none', zorder=7)

    yr_col = {'2021-22':'#FADBD8','2022-23':'#F1948A','2023-24':'#E74C3C',
               '2024-25':'#C0392B','2025-26':'#922B21','2026-27':'#641E16'}
    for pt in elec_pts:
        c = yr_col.get(pt[3], RED)
        # Lightning gets a star marker
        mk = '*' if 'lightning' in pt[2].lower() else 'o'
        sz = 13 if 'lightning' in pt[2].lower() else 11
        ax.plot(pt[1], pt[0], mk, color=c, markersize=sz, alpha=0.9,
                markeredgecolor='white', markeredgewidth=0.9, zorder=9)
        ax.plot(pt[1], pt[0], 'o', color=RED, markersize=16, alpha=0.15,
                markeredgecolor='none', zorder=8)

    add_range_labels(ax)
    add_north_arrow(ax, 83.02, 22.76)
    add_scale_bar(ax, 83.05, 21.95, 0.18, '~20 km')

    yr_handles = [
        mpatches.Patch(facecolor=yr_col['2021-22'], label='2021-22 (2 elec)'),
        mpatches.Patch(facecolor=yr_col['2022-23'], label='2022-23 (5 elec)'),
        mpatches.Patch(facecolor=yr_col['2023-24'], label='2023-24 (5 elec)'),
        mpatches.Patch(facecolor=yr_col['2024-25'], label='2024-25 (3 elec)'),
        mpatches.Patch(facecolor=yr_col['2025-26'], label='2025-26 (3 elec)'),
        Line2D([0],[0], marker='*', color='w', markerfacecolor=RED,
               markersize=10, label='Lightning strike'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor=RED,
               markersize=9, label='Electrocution'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor='#BDC3C7',
               markersize=6, label='Other deaths (dim)'),
    ]
    ax.legend(handles=yr_handles, loc='lower right', fontsize=7,
              framealpha=0.92, edgecolor='#2C3E50', title='Electrocution by Year',
              title_fontsize=7.5)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 285)

# ════════════════════════════════════════════════════════════════════
#  MAP 5 — Year-wise progression (4-panel small multiples)
# ════════════════════════════════════════════════════════════════════
def map_yearly_panels():
    all_e = DH_ELEPHANT + RG_ELEPHANT
    years = ['2021-22','2022-23','2023-24','2024-25','2025-26','2026-27']
    year_labels = ['2021-22 (4 deaths)','2022-23 (12 deaths)','2023-24 (6 deaths)',
                   '2024-25 (10 deaths)','2025-26 (12 deaths ★)','2026-27 (5 deaths, ongoing)']

    fig, axes = plt.subplots(2, 3, figsize=(9, 6.5), facecolor='white')
    fig.suptitle('Year-wise Elephant Death Progression (2021–2027)',
                 fontsize=11, fontweight='bold', color=DG, y=1.01)

    for ax, yr, lbl in zip(axes.flat, years, year_labels):
        ax.set_facecolor('#E8F4E8')
        ax.set_xlim(83.0, 84.05); ax.set_ylim(21.92, 22.85)

        # Simple forest background
        ax.add_patch(plt.Polygon([[83.0,21.92],[84.05,21.92],[84.05,22.85],[83.0,22.85]],
                                  closed=True, facecolor='#D5E8D5', edgecolor='none', zorder=0))
        # Panikshet
        ax.add_patch(Ellipse((83.24,22.10), 0.06, 0.03, color='#85C1E9', alpha=0.6, zorder=1))
        # Division boundary
        ax.plot([83.38,83.38,83.37], [21.93,22.50,22.82], '--', color='#566573',
                linewidth=1, alpha=0.7, zorder=2, dashes=(4,2))

        # All deaths dim
        for pt in all_e:
            ax.plot(pt[1], pt[0], 'o', color='#D0D3D4', markersize=3.5,
                    alpha=0.3, zorder=3)

        # Current year deaths highlighted
        yr_key = yr.replace('*','')
        pts = [p for p in all_e if p[3] == yr_key or (yr == '2026-27' and p[3] == '2026-27')]
        for pt in pts:
            c = cause_color(pt[2])
            ax.plot(pt[1], pt[0], 'o', color=c, markersize=8, alpha=0.92,
                    markeredgecolor='white', markeredgewidth=0.8, zorder=9)

        ax.set_title(lbl, fontsize=7.5, fontweight='bold', color=DG, pad=3)
        ax.tick_params(labelsize=5.5)
        ax.grid(True, linestyle=':', linewidth=0.4, color='#BDC3C7', alpha=0.5)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        if yr == '2025-26' or yr == '2026-27':
            ax.set_facecolor('#FDECEA')
            for patch in ax.patches[:1]:
                patch.set_facecolor('#F9EBEA')

    # Shared legend
    leg = [mpatches.Patch(facecolor=RED,  label='Electrocution'),
           mpatches.Patch(facecolor=BLUE, label='Drowning'),
           mpatches.Patch(facecolor=LG,   label='Natural/Other'),
           mpatches.Patch(facecolor=AMB,  label='Trauma'),
           mpatches.Patch(facecolor='#D0D3D4', label='Other years (dim)')]
    fig.legend(handles=leg, loc='lower center', ncol=5, fontsize=7,
               framealpha=0.9, bbox_to_anchor=(0.5,-0.03))
    fig.tight_layout()
    return fig_to_rl(fig, WC, 300)

# ════════════════════════════════════════════════════════════════════
#  MAP 6 — Human casualty map
# ════════════════════════════════════════════════════════════════════
def map_human():
    fig, ax = plt.subplots(figsize=(8.5, 6), facecolor='white')
    map_base(ax, 'Human Casualty Map — Human Deaths in HEI Incidents (2021–2026)')

    yr_col = {'2021-22':'#F9E79F','2022-23':'#F0B27A','2023-24':'#EB984E',
               '2024-25':'#E59866','2025-26':'#E67E22'}

    for pt in DH_ELEPHANT + RG_ELEPHANT:
        ax.plot(pt[1], pt[0], 'o', color='#D0D3D4', markersize=4.5,
                alpha=0.35, markeredgecolor='none', zorder=6)

    for pt in DH_HUMAN + RG_HUMAN:
        c = yr_col.get(pt[3], AMB)
        ax.plot(pt[1], pt[0], '^', color=c, markersize=10, alpha=0.9,
                markeredgecolor='#7D6608', markeredgewidth=0.8, zorder=9)
        ax.plot(pt[1], pt[0], '^', color=AMB, markersize=14, alpha=0.15,
                markeredgecolor='none', zorder=8)
        if pt[2] and len(pt[2]) < 12:
            ax.annotate(pt[2], (pt[1], pt[0]), textcoords='offset points',
                       xytext=(5,4), fontsize=5, color='#784212',
                       bbox=dict(boxstyle='round,pad=0.08', facecolor='#FFF9C4',
                                 alpha=0.7, edgecolor='none'), zorder=10)

    add_range_labels(ax)
    add_north_arrow(ax, 83.02, 22.76)
    add_scale_bar(ax, 83.05, 21.95, 0.18, '~20 km')

    yr_handles = [
        mpatches.Patch(facecolor=yr_col['2021-22'], label='2021-22 (13 deaths)'),
        mpatches.Patch(facecolor=yr_col['2022-23'], label='2022-23 (1 death)'),
        mpatches.Patch(facecolor=yr_col['2023-24'], label='2023-24 (7 deaths)'),
        mpatches.Patch(facecolor=yr_col['2024-25'], label='2024-25 (8 deaths)'),
        mpatches.Patch(facecolor=yr_col['2025-26'], label='2025-26 (16 deaths)'),
        Line2D([0],[0], marker='^', color='w', markerfacecolor=AMB, markersize=9,
               markeredgecolor='#7D6608', label='Human death'),
        Line2D([0],[0], marker='o', color='w', markerfacecolor='#D0D3D4', markersize=6,
               label='Elephant death (dim)'),
    ]
    ax.legend(handles=yr_handles, loc='lower right', fontsize=7,
              framealpha=0.92, edgecolor='#2C3E50', title='Human Deaths by Year',
              title_fontsize=7.5)
    fig.tight_layout()
    return fig_to_rl(fig, WC, 285)

# ══════════════════════════════════════════════════════════════════════════════
#  STANDARD CHARTS (from previous script)
# ══════════════════════════════════════════════════════════════════════════════
def setup_ax(ax, title='', ylabel=''):
    ax.set_facecolor('#F7FAF8')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#BDC3C7')
    ax.tick_params(colors='#4A5568', labelsize=8)
    if title: ax.set_title(title, fontsize=10, fontweight='bold', color=DG, pad=7)
    if ylabel: ax.set_ylabel(ylabel, fontsize=8, color='#4A5568')

def chart_population():
    years=[2001,2005,2007,2015,2017,2021,2026]; pop=[24,123,122,247,247,279,451]
    fig,ax=plt.subplots(figsize=(7,3),facecolor='white')
    ax.fill_between(range(len(years)),pop,alpha=0.15,color=LG)
    ax.plot(range(len(years)),pop,'-o',color=MG,linewidth=2.2,markersize=6,
            markerfacecolor=LG,markeredgecolor=DG,markeredgewidth=1)
    for i,(y,p) in enumerate(zip(years,pop)):
        ax.annotate(f'{p}', (i,p), textcoords='offset points', xytext=(0,9),
                    ha='center', fontsize=8.5, fontweight='bold', color=DG)
    ax.set_xticks(range(len(years))); ax.set_xticklabels(years,fontsize=8.5)
    setup_ax(ax,'Elephant Population Trend — Chhattisgarh 2001–2026',ylabel='Population')
    ax.set_ylim(0,520); ax.grid(axis='y',linestyle='--',alpha=0.4,color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig,WC,155)

def chart_yearly():
    years=['21-22','22-23','23-24','24-25','25-26','26-27*']
    dh=[4,6,6,6,1,4]; rg=[0,6,0,4,11,1]; tot=[4,12,6,10,12,5]
    x=np.arange(6); w=0.26
    fig,ax=plt.subplots(figsize=(7,3.2),facecolor='white')
    b1=ax.bar(x-w,dh,w,label='Dharamjaigarh',color=MG,alpha=0.85)
    b2=ax.bar(x,  rg,w,label='Raigarh',       color=AMB,alpha=0.85)
    b3=ax.bar(x+w,tot,w,label='Total',         color=SL,alpha=0.45)
    for b in [*b1,*b2,*b3]:
        h=b.get_height()
        if h: ax.text(b.get_x()+b.get_width()/2,h+0.2,str(int(h)),
                      ha='center',fontsize=7.5,color=SL)
    ax.set_xticks(x); ax.set_xticklabels(years,fontsize=8.5)
    ax.legend(fontsize=8,framealpha=0.5); ax.set_ylim(0,16)
    setup_ax(ax,'Year-wise Elephant Deaths — Both Divisions',ylabel='Deaths')
    ax.grid(axis='y',linestyle='--',alpha=0.4,color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig,WC,165)

def chart_cause():
    causes=['Electrocution','Suspected\nDrowning','Natural/\nOld Age','Fall/Trauma','Other']
    counts=[23,13,4,4,5]; pal=[RED,BLUE,LG,AMB,'#8E44AD']
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7.2,3.2),facecolor='white')
    wedges,_,auts=ax1.pie(counts,autopct='%1.0f%%',startangle=90,colors=pal,
                           pctdistance=0.72,wedgeprops=dict(width=0.55,edgecolor='white',linewidth=1.5))
    for at in auts: at.set_fontsize(8); at.set_color('white'); at.set_fontweight('bold')
    ax1.set_title('Cause Distribution',fontsize=9.5,fontweight='bold',color=DG)
    handles=[mpatches.Patch(color=c,label=f'{l} ({n})')
             for c,l,n in zip(pal,['Electrocution','Suspected Drowning','Natural/Old Age',
                                    'Fall/Trauma','Other'],counts)]
    ax1.legend(handles=handles,fontsize=6.5,loc='lower center',bbox_to_anchor=(0.5,-0.22),ncol=2,framealpha=0.4)
    y=np.arange(5)
    bars=ax2.barh(y,counts,color=pal,alpha=0.85,edgecolor='white')
    for b in bars:
        w_=b.get_width()
        ax2.text(w_+0.2,b.get_y()+b.get_height()/2,f'{int(w_)}  ({int(w_/49*100)}%)',
                 va='center',fontsize=8,color=SL)
    ax2.set_yticks(y); ax2.set_yticklabels(causes,fontsize=8)
    ax2.set_xlim(0,30); ax2.set_facecolor('#F7FAF8')
    ax2.set_title('Count by Cause (n=49)',fontsize=9.5,fontweight='bold',color=DG)
    ax2.spines[['top','right']].set_visible(False)
    ax2.grid(axis='x',linestyle='--',alpha=0.4,color=MGR)
    fig.tight_layout(pad=1.5)
    return fig_to_rl(fig,WC,185)

def chart_age():
    groups=['Old (55+ yr)','Adult (30–55 yr)','Sub-adult\n(15–30 yr)','Juvenile\n(2–15 yr)','Calf (0–2 yr)']
    counts=[5,11,2,5,23]; pal=[LG,MG,AMB,'#E67E22',RED]
    fig,ax=plt.subplots(figsize=(6.5,2.8),facecolor='white')
    bars=ax.barh(groups,counts,color=pal,alpha=0.85,edgecolor='white',height=0.55)
    for b in bars:
        w=b.get_width()
        ax.text(w+0.3,b.get_y()+b.get_height()/2,f'{int(w)}  ({int(w/46*100)}%)',
                va='center',fontsize=8.5,color=SL)
    ax.set_xlim(0,28)
    setup_ax(ax,'Age-Group Distribution of Elephant Deaths (n=46 confirmed)',ylabel='')
    ax.spines[['top','right']].set_visible(False); ax.set_facecolor('#F7FAF8')
    ax.grid(axis='x',linestyle='--',alpha=0.4,color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig,WC,155)

def chart_seasonal():
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    total=[6,4,3,2,5,5,1,1,3,8,6,5]
    drown=[3,0,1,0,4,1,0,0,0,1,2,2]
    elec =[2,0,2,1,0,1,1,1,2,7,1,2]
    x=np.arange(12)
    fig,ax=plt.subplots(figsize=(7.2,3.2),facecolor='white')
    ax.fill_between(x,total,alpha=0.12,color=LG)
    ax.plot(x,total,'-o',color=MG,linewidth=2,markersize=5,label='Total Deaths')
    ax.plot(x,drown,'-s',color=BLUE,linewidth=1.6,markersize=5,label='Drowning',dashes=(5,2))
    ax.plot(x,elec, '-^',color=RED, linewidth=1.6,markersize=5,label='Electrocution',dashes=(5,2))
    for i,t in enumerate(total):
        if t: ax.annotate(str(t),(i,t),textcoords='offset points',xytext=(0,6),
                          ha='center',fontsize=7.5,color=MG,fontweight='bold')
    ax.set_xticks(x); ax.set_xticklabels(months,fontsize=8.5)
    ax.legend(fontsize=8,framealpha=0.5); ax.set_ylim(0,11)
    ax.axvspan(8.5,11.5,alpha=0.07,color=RED)
    ax.axvspan(-0.5,4.5,alpha=0.07,color=BLUE)
    ax.text(1.8,9.5,'Drowning Peak\n(Jan–May)',color=BLUE,fontsize=7.5,ha='center',style='italic')
    ax.text(10.0,9.5,'Electrocution\nPeak (Oct–Dec)',color=RED,fontsize=7.5,ha='center',style='italic')
    setup_ax(ax,'Monthly Distribution — Total, Drowning &amp; Electrocution',ylabel='Deaths')
    ax.grid(axis='y',linestyle='--',alpha=0.4,color=MGR)
    fig.tight_layout()
    return fig_to_rl(fig,WC,175)

def chart_range():
    ranges=['Kharsiya\n(RG)','Raigarh HQ\n(RG)','Baakaaruma\n(DH)',
            'Lailungaan\n(DH)','Borojh\n(DH)','Tamanar\n(RG)',
            'DH HQ\n(DH)','Chhal\n(DH)','Ghargoda\n(RG)']
    elec=[0,0,1,0,1,4,5,5,7]; drown=[1,1,0,0,0,1,0,6,5]; other=[0,0,0,2,3,0,2,3,3]
    y=np.arange(len(ranges))
    fig,ax=plt.subplots(figsize=(7,3.8),facecolor='white')
    b1=ax.barh(y,elec,color=RED,alpha=0.82,label='Electrocution',edgecolor='white')
    b2=ax.barh(y,drown,left=elec,color=BLUE,alpha=0.82,label='Drowning',edgecolor='white')
    left2=[e+d for e,d in zip(elec,drown)]
    ax.barh(y,other,left=left2,color=LG,alpha=0.82,label='Other',edgecolor='white')
    totals=[e+d+o for e,d,o in zip(elec,drown,other)]
    for i,t in enumerate(totals):
        ax.text(t+0.1,i,f'  {t}',va='center',fontsize=8.5,fontweight='bold',color=SL)
    ax.set_yticks(y); ax.set_yticklabels(ranges,fontsize=8)
    ax.legend(fontsize=8,framealpha=0.5,loc='lower right')
    setup_ax(ax,'Range-wise Elephant Deaths — Stacked by Cause',ylabel='')
    ax.set_xlim(0,20); ax.set_facecolor('#F7FAF8')
    ax.grid(axis='x',linestyle='--',alpha=0.4,color=MGR)
    ax.spines[['top','right']].set_visible(False)
    ax.axhline(6.5,color=RED,linewidth=0.8,linestyle=':',alpha=0.7)
    ax.text(16,7.5,'CRITICAL',color=RED,fontsize=7.5,style='italic')
    fig.tight_layout()
    return fig_to_rl(fig,WC,195)

# ── ReportLab styles ───────────────────────────────────────────────────────────
def sty(name,**kw): return ParagraphStyle(name,**kw)
COVER_T=sty('CT',fontSize=25,textColor=colors.white,leading=31,alignment=TA_CENTER,fontName='Helvetica-Bold')
COVER_S=sty('CS',fontSize=12,textColor=colors.HexColor(PG),leading=17,alignment=TA_CENTER)
COVER_D=sty('CD',fontSize=10,textColor=colors.HexColor(LG),alignment=TA_CENTER)
CH1=sty('H1',fontSize=16,textColor=colors.HexColor(DG),leading=20,spaceBefore=10,spaceAfter=4,fontName='Helvetica-Bold')
CH2=sty('H2',fontSize=12,textColor=colors.HexColor(MG),leading=15,spaceBefore=7,spaceAfter=3,fontName='Helvetica-Bold')
BODY=sty('BD',fontSize=9.5,textColor=colors.HexColor(SL),leading=14,spaceAfter=4,alignment=TA_JUSTIFY)
BUL =sty('BL',fontSize=9.5,textColor=colors.HexColor(SL),leading=13,leftIndent=14,spaceAfter=3)
SM  =sty('SM',fontSize=7.5,textColor=colors.grey,leading=11,spaceAfter=2)
CAP =sty('CP',fontSize=8,textColor=colors.grey,alignment=TA_CENTER,spaceBefore=2,spaceAfter=6)

def P(t):  return Paragraph(t,BODY)
def B(t):  return Paragraph(f'• {t}',BUL)
def SP(h=6): return Spacer(1,h)
def HR(c=MG,w=0.8): return HRFlowable(width='100%',thickness=w,color=colors.HexColor(c),spaceAfter=5,spaceBefore=3)

def banner(text,bg=DG):
    row=[[Paragraph(f'<b>{text}</b>',sty('SB',fontSize=13,textColor=colors.white,leading=17))]]
    t=Table(row,colWidths=[WC])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor(bg)),
                            ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),
                            ('LEFTPADDING',(0,0),(-1,-1),12)]))
    return t

def itbl(rows):
    ks=sty('KS',fontSize=9,textColor=colors.HexColor(DG),fontName='Helvetica-Bold')
    vs=sty('VS',fontSize=9,textColor=colors.HexColor(SL))
    data=[[Paragraph(k,ks),Paragraph(v,vs)] for k,v in rows]
    t=Table(data,colWidths=[38*mm,WC-38*mm])
    t.setStyle(TableStyle([('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,colors.HexColor(LGR)]),
                            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
                            ('LEFTPADDING',(0,0),(-1,-1),6),
                            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor(MGR)),
                            ('VALIGN',(0,0),(-1,-1),'TOP')]))
    return t

def dtbl(header,rows,cw=None):
    hs=sty('TH',fontSize=8.5,textColor=colors.white,fontName='Helvetica-Bold',leading=11)
    ds=sty('TD',fontSize=8.5,textColor=colors.HexColor(SL),leading=11)
    hrow=[Paragraph(h,hs) for h in header]
    drows=[[Paragraph(str(c),ds) for c in r] for r in rows]
    t=Table([hrow]+drows,colWidths=cw)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(DG)),
                            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor(LGR)]),
                            ('GRID',(0,0),(-1,-1),0.35,colors.HexColor(MGR)),
                            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
                            ('LEFTPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP')]))
    return t

def hibox(text,bg=PG,border=MG,tc=DG):
    row=[[Paragraph(text,sty('HB',fontSize=9.5,textColor=colors.HexColor(tc),leading=14,fontName='Helvetica-Bold'))]]
    t=Table(row,colWidths=[WC])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor(bg)),
                            ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                            ('LEFTPADDING',(0,0),(-1,-1),10),
                            ('BOX',(0,0),(-1,-1),1.2,colors.HexColor(border))]))
    return t

def alertbox(text): return hibox(text,bg='#FDECEA',border=RED,tc='#7B0000')

# ── Page decorators ────────────────────────────────────────────────────────────
def cover_bg(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(DG)); canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setFillColor(colors.HexColor(MG)); canvas.rect(0,H*0.60,W,5,fill=1,stroke=0)
    canvas.setFillColor(colors.HexColor(LG)); canvas.rect(0,H*0.60-3,W,3,fill=1,stroke=0)
    canvas.setFillColor(colors.HexColor(MG)); canvas.rect(0,0,W,50,fill=1,stroke=0)
    canvas.restoreState()

def normal_page(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(DG)); canvas.rect(0,H-28,W,28,fill=1,stroke=0)
    canvas.setFillColor(colors.HexColor(LG)); canvas.rect(0,H-31,W,3,fill=1,stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold',7.5)
    canvas.drawString(36,H-19,'Chapter 1 — Mortality Investigation of Asian Elephant · Bilaspur 2026')
    canvas.setFont('Helvetica',7.5)
    canvas.drawRightString(W-36,H-19,'Notes with GIS Maps &amp; Data Charts')
    canvas.setFillColor(colors.HexColor(DG)); canvas.rect(0,0,W,22,fill=1,stroke=0)
    canvas.setFillColor(colors.HexColor(PG)); canvas.setFont('Helvetica',7.5)
    canvas.drawString(36,7,'CG Forest Dept. · WII Dehradun · ICAR-IVRI')
    canvas.drawRightString(W-36,7,f'Page {doc.page}')
    canvas.restoreState()

def on_page(canvas,doc):
    if doc.page==1: cover_bg(canvas,doc)
    else: normal_page(canvas,doc)

# ══════════════════════════════════════════════════════════════════════════════
print("Rendering charts..."); import sys; sys.stdout.flush()

print("  [1/12] Population trend chart")
pop_chart   = chart_population()
print("  [2/12] Year-wise deaths chart")
yr_chart    = chart_yearly()
print("  [3/12] Cause of death chart")
cause_chart = chart_cause()
print("  [4/12] Age profile chart")
age_chart   = chart_age()
print("  [5/12] Seasonal chart")
seas_chart  = chart_seasonal()
print("  [6/12] Range-wise chart")
range_chart = chart_range()
print("  [7/12] Master casualty map")
m1 = map_master()
print("  [8/12] Elephant cause map")
m2 = map_elephant_cause()
print("  [9/12] Drowning hotspot map")
m3 = map_drowning()
print("  [10/12] Electrocution hotspot map")
m4 = map_electrocution()
print("  [11/12] Year-wise progression panels")
m5 = map_yearly_panels()
print("  [12/12] Human casualty map")
m6 = map_human()
print("All charts rendered. Building PDF...")

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ─── COVER ────────────────────────────────────────────────────────────────────
story += [
    SP(90),
    Paragraph('CHAPTER 1',
              sty('CH_NUM', fontSize=14, textColor=colors.HexColor(LG),
                  leading=18, alignment=TA_CENTER, fontName='Helvetica-Bold',
                  spaceAfter=6)),
    Paragraph('─' * 38,
              sty('CH_RULE', fontSize=10, textColor=colors.HexColor(MG),
                  alignment=TA_CENTER, spaceAfter=10)),
    Paragraph('Workshop on Essentials of Mortality<br/>Investigation of Asian Elephant', COVER_T),
    SP(12),
    Paragraph('Illustrated Notes · GIS Maps · Data Analysis', COVER_S),
    SP(8),
    Paragraph('5<sup>th</sup>–6<sup>th</sup> June 2026', COVER_D),
    SP(20),
    Paragraph('Dharamjaigarh &amp; Raigarh Van Mandals · Bilaspur Forest Circle · Chhattisgarh',
              sty('CI',fontSize=11,textColor=colors.HexColor(PG),leading=16,alignment=TA_CENTER)),
    SP(26),
    Paragraph('<b>Organised by:</b> Chhattisgarh Forest Department<br/>'
              '<b>Technical Support:</b> Wildlife Institute of India, Dehradun<br/>'
              '<b>Laboratory:</b> ICAR-IVRI, Izatnagar  ·  NDVSU, Jabalpur',
              sty('OG',fontSize=10,textColor=colors.HexColor(LG),leading=17,alignment=TA_CENTER)),
    PageBreak(),
]

# ─── 1. WORKSHOP OVERVIEW ─────────────────────────────────────────────────────
story += [
    banner('1.  Workshop Overview &amp; Objectives'),
    SP(8),
    Paragraph('1.1  Background', CH2),
    P('This two-day workshop was convened by the <b>Chhattisgarh Forest Department</b> with '
      'technical support from <b>Wildlife Institute of India (WII), Dehradun</b> to build '
      'field-level capacity in elephant mortality investigation across the Bilaspur Forest Circle. '
      '<b>84 participants</b> attended from the Forest Department and Veterinary Service Department '
      'of Chhattisgarh State.'),
    SP(4),
    Paragraph('1.2  Objectives', CH2),
    B('<b>Biology, Behaviour &amp; Disease</b> — Understand elephant biology, behaviour, '
      'and the major infectious and non-infectious diseases causing mortality.'),
    B('<b>Necropsy, Biosafety &amp; Sampling</b> — Hands-on competency in field necropsy, '
      'tissue sampling, cold-chain documentation, and PPE protocols.'),
    B('<b>Surveillance, Disposal &amp; Forensics</b> — Operational frameworks for carcass '
      'disposal, site decontamination, standardised forensic reporting and health monitoring.'),
    SP(6),
    Paragraph('1.3  Resource Persons', CH2),
    SP(4),
    dtbl(['Name','Designation','Institution','Expertise'],
         [['Dr. A. B. Shrivastav','Founder Dir., School of Wildlife Forensic &amp; Health',
           'NDVSU, Jabalpur','Wildlife Health, Forensics, Pathology'],
          ['Dr. Parag Nigam','Sr. Scientist &amp; Head, Wildlife Health',
           'WII, Dehradun','Chemical Capture, Conservation Medicine'],
          ['Dr. Karikalan Mathesh','Sr. Scientist, CWCMDS',
           'ICAR-IVRI, Bareilly','Wildlife Pathology, Histopathology, Molecular Dx'],
          ['Dr. Tapendra Saini','Scientist C',
           'WII, Dehradun','Animal Genetics, Conservation Breeding'],
          ['Dr. C. P. Sharma','PTO &amp; In-charge, Morphology Unit',
           'WII, Dehradun','Wildlife Forensics, Crime-Scene Mgmt']],
         [44*mm,52*mm,38*mm,WC-134*mm]),
    PageBreak(),
]

# ─── 2. POPULATION STATUS ─────────────────────────────────────────────────────
story += [
    banner('2.  Elephant Population — Chhattisgarh (2001–2026)'),
    SP(8),
    P('The elephant population has grown from <b>24 individuals (2001)</b> to an estimated '
      '<b>451 elephants (2026)</b> — a CAGR of ~13% over 25 years. '
      'The 2021–2026 study period alone saw a <b>+62% increase (279 → 451)</b> at ~10% CAGR, '
      'driven by natural dispersal from Odisha and Jharkhand into Bilaspur Circle.'),
    SP(5),
    pop_chart,
    Paragraph('Figure 1: Population trend 2001–2026. Source: WII Census &amp; CG Forest Dept. Estimates.', CAP),
    SP(6),
    dtbl(['Year','Count','Notes'],
         [['2001','24','Founding dispersal from Odisha/Jharkhand'],
          ['2005','123','First major census count (+412% in 4 yrs)'],
          ['2015','247','Significant consolidation'],
          ['2021','279','Official Census — 10% CAGR since 2005'],
          ['2026','~451 est.','Net +172 over 5-year study period']],
         [22*mm,28*mm,WC-50*mm]),
    SP(4),
    hibox('Bilaspur Circle hosts the highest elephant density in CG. 2025-26 recorded '
          'the highest single-year human-elephant conflict events in the 5-year study period.'),
    PageBreak(),
]

# ─── 3. YEAR-WISE CASUALTIES ──────────────────────────────────────────────────
story += [
    banner('3.  Elephant Casualties — Year-wise Overview (2021–2026)'),
    SP(8),
    P('<b>49 confirmed elephant deaths</b> over the study period. Dharamjaigarh (DH) contributes '
      '27 deaths and Raigarh (RG) 22. The year 2025-26 is the <b>record year (12 deaths)</b>, '
      'driven by a sharp RG spike. The 2026-27 cohort (5 deaths in 3 months — all calves, '
      'all drowning) signals an accelerating acute threat.'),
    SP(5),
    yr_chart,
    Paragraph('Figure 2: Year-wise deaths by division — Dharamjaigarh (green), Raigarh (amber), Total (grey).', CAP),
    SP(6),
    dtbl(['Year','DH','RG','Total','Notable Pattern'],
         [['2021-22','4','0','4','All DH — founding year of RG dispersal'],
          ['2022-23','6','6','12','RG emerges; multi-cause cluster'],
          ['2023-24','6','0','6','DH dominant; RG quiet'],
          ['2024-25','6','4','10','Both divisions active; mixed causes'],
          ['2025-26','1','11','12','★ RECORD — RG electrocution &amp; drowning surge'],
          ['2026-27*','4','1','5','All calves, all drowning — ongoing'],
          ['TOTAL','27','22','49','5+ year study']],
         [22*mm,14*mm,14*mm,18*mm,WC-68*mm]),
    SP(4),
    alertbox('⚠  2026-27 early signal: all 5 deaths in first 3 months are calves (0–2 yr) '
             'from suspected drowning. Immediate dry-season intervention required.'),
    PageBreak(),
]

# ─── 4. CAUSE OF DEATH ────────────────────────────────────────────────────────
story += [
    banner('4.  Cause of Death Analysis'),
    SP(8),
    cause_chart,
    Paragraph('Figure 3: Cause distribution — donut (left) and count with percentages (right). n = 49.', CAP),
    SP(5),
    dtbl(['Cause','Count','%','Key Risk Factor'],
         [['Electrocution','23','47%','Illegal/low-hung power lines near crop fields; 3 multi-simultaneous events'],
          ['Suspected Drowning','13','27%','Dams, ponds, seasonal nalas; 92% calves/young'],
          ['Natural / Old Age','4','8%','Senescence; female-skewed (4F:1M)'],
          ['Fall / Trauma','4','8%','Hills, nalas, infighting'],
          ['Other (heat/sun/unknown)','5','10%','Heatstroke, cardiovascular shock, weakness']],
         [44*mm,16*mm,14*mm,WC-74*mm]),
    SP(5),
    hibox('Electrocution (47%) + Drowning (27%) = 74% of deaths — both fully preventable '
          'with targeted infrastructure, enforcement, and field monitoring.'),
    PageBreak(),
]

# ─── 5. DEMOGRAPHICS ──────────────────────────────────────────────────────────
story += [
    banner('5.  Demographic Analysis — Age &amp; Seasonal Profiles'),
    SP(8),
    Paragraph('5.1  Age Group Distribution', CH2),
    P('<b>50% of all deaths are calves (0–2 yr)</b>. With juveniles included, <b>61% of deaths '
      'occur below 15 years of age</b> — a direct long-term threat to population viability '
      'and recruitment.'),
    SP(5),
    age_chart,
    Paragraph('Figure 4: Age-group distribution. Calf class alone = 50% of all deaths.', CAP),
    SP(6),
    Paragraph('5.2  Seasonal Variation', CH2),
    P('<b>October is the deadliest month (8 deaths)</b>, driven by electrocution during crop-harvest '
      'electric fencing. Oct–Dec = 42% of all annual deaths. A secondary drowning peak occurs '
      'Jan–May when dry-season water levels are low and banks are steep.'),
    SP(5),
    seas_chart,
    Paragraph('Figure 5: Monthly deaths — total (green), drowning (blue), electrocution (red). '
              'Shaded zones mark seasonal peaks.', CAP),
    SP(5),
    dtbl(['Season','Drowning','Electrocution','Driver'],
         [['Jan–May (Dry)','8  (62%)','6  (30%)','Low water, steep banks; crop fields quiet'],
          ['Jun–Sep (Monsoon)','1  (8%)','5  (25%)','Nalas swell; some fencing active'],
          ['Oct–Dec (Harvest)','4  (31%)','10  (50%)','Crop protection fencing at maximum']],
         [30*mm,28*mm,35*mm,WC-93*mm]),
    PageBreak(),
]

# ─── 6. RANGE-WISE ────────────────────────────────────────────────────────────
story += [
    banner('6.  Range-wise Distribution'),
    SP(8),
    range_chart,
    Paragraph('Figure 6: Range-wise stacked deaths — electrocution (red), drowning (blue), other (green). '
              'Chhal + Ghargoda = CRITICAL zones.', CAP),
    SP(5),
    dtbl(['Range / Beat','Division','Total','Risk','Elec','Drown','Other'],
         [['Ghargoda','Raigarh','15','CRITICAL','7','5','3'],
          ['Chhal','Dharamjaigarh','14','CRITICAL','5','6','3'],
          ['Dharamjaigarh HQ','Dharamjaigarh','7','HIGH','5','0','2'],
          ['Tamanar','Raigarh','5','MODERATE','4','1','0'],
          ['Borojh','Dharamjaigarh','4','HIGH','1','0','3'],
          ['Lailungaan','Dharamjaigarh','2','HIGH','0','0','2'],
          ['Baakaaruma','Dharamjaigarh','1','MODERATE','1','0','0'],
          ['Raigarh HQ','Raigarh','1','LOW','0','1','0'],
          ['Kharsiya','Raigarh','1','LOW','0','1','0']],
         [38*mm,36*mm,16*mm,24*mm,15*mm,18*mm,WC-147*mm]),
    SP(5),
    alertbox('PRIORITY: Chhal (DH) + Ghargoda (RG) = 29 deaths (59% of all elephant casualties). '
             'These two ranges require the most urgent multi-agency intervention.'),
    PageBreak(),
]

# ─── 7. GIS: MASTER CASUALTY MAP ─────────────────────────────────────────────
story += [
    banner('7.  GIS Analysis — Casualty Geo-mapping'),
    SP(8),
    Paragraph('7.1  Master Casualty Map', CH2),
    P('All 49 elephant deaths and 45 human deaths geo-referenced and plotted. '
      'Elephant deaths are colour-coded by cause (electrocution = red, drowning = blue, '
      'natural = green, trauma = amber). Human deaths are shown as triangles. '
      'The division boundary (dashed) separates Dharamjaigarh (west) from Raigarh (east).'),
    SP(5),
    m1,
    Paragraph('Figure 7: Master casualty map — elephant deaths (circles, cause-coded) + '
              'human deaths (triangles, orange). All GPS-referenced mortality events 2021–2026.', CAP),
    SP(4),
    P('Key spatial observations:'),
    B('The western cluster (DH, lon 83.05–83.40) is dominated by <b>electrocution deaths</b> '
      'in the Chhal, Borojh and Dharamjaigarh HQ ranges.'),
    B('The central-eastern cluster (RG, lon 83.40–83.60) shows a <b>mixed drowning-electrocution '
      'pattern</b> concentrated around Ghargoda range and the Panikshet/Rabo dam corridor.'),
    B('Human deaths mirror elephant corridors, indicating shared forest-agriculture interface zones.'),
    PageBreak(),
]

# ─── 8. GIS: ELEPHANT CAUSE MAP ───────────────────────────────────────────────
story += [
    banner('8.  GIS — Elephant Deaths: Cause &amp; Spatial Pattern'),
    SP(8),
    m2,
    Paragraph('Figure 8: All 49 elephant deaths — colour coded by confirmed cause of death. '
              'Red = electrocution, Blue = drowning, Green = natural, Amber = trauma/other.', CAP),
    SP(5),
    Paragraph('8.1  Spatial Interpretation', CH2),
    B('<b>Electrocution cluster (red):</b> Concentrated in DH west (Chhal, DH HQ) and RG central '
      '(Ghargoda, Tamanar) — correlates with high-density agricultural zones and illegal crop-fence corridors.'),
    B('<b>Drowning cluster (blue):</b> Mainly RG division near Panikshet and Rabo dams, '
      'and Mond River nalas (DH south). All dry-season water trap locations.'),
    B('<b>Natural/old age deaths (green):</b> Scattered broadly — no geographic hotspot pattern.'),
    B('<b>Trauma/other (amber):</b> Sparse and scattered — no dominant cluster.'),
    PageBreak(),
]

# ─── 9. GIS: YEAR-WISE PANELS ─────────────────────────────────────────────────
story += [
    banner('9.  GIS — Year-wise Progression of Elephant Deaths (2021–2027)'),
    SP(8),
    m5,
    Paragraph('Figure 9: Year-wise small-multiple maps. Active year deaths shown in full colour; '
              'all other years dimmed. Red background = record/critical years (2025-26, 2026-27).', CAP),
    SP(5),
    Paragraph('9.1  Key Spatial Trends by Year', CH2),
    B('<b>2021-22:</b> Deaths confined to DH division only — all western half. RG corridor not yet active.'),
    B('<b>2022-23:</b> First RG deaths appear — electrocution cluster in central RG. Largest single-year count (12).'),
    B('<b>2023-24:</b> Returns to DH dominance — electrocution hotspot intensifies in DH south.'),
    B('<b>2024-25:</b> Both divisions active. First confirmed drowning cluster in RG dam zone.'),
    B('<b>2025-26 (RECORD):</b> Dramatic RG surge — 11 of 12 deaths are in RG, '
      'concentrated around Ghargoda and dam corridor. DH drops to 1 death.'),
    B('<b>2026-27 (ongoing):</b> 4 of 5 deaths in DH south — all calves, all drowning. '
      'New cluster emerging around Mond River nalas.'),
    PageBreak(),
]

# ─── 10. GIS: DROWNING MAP ────────────────────────────────────────────────────
story += [
    banner('10.  GIS — Drowning Hotspot Analysis'),
    SP(8),
    m3,
    Paragraph('Figure 10: Suspected drowning incidents (n=13) year-coded from light blue (2021-22) '
              'to orange (2026-27). Non-drowning deaths are dimmed. '
              'Note clustering around dam zones and river nalas.', CAP),
    SP(5),
    Paragraph('10.1  Drowning Incident Locations', CH2),
    dtbl(['Location / Water Body','Division','Year','Coordinates','Notes'],
         [['Panikshet Dam','Raigarh','2024-25','22.10°N 83.24°E','2 calves, consecutive'],
          ['Rabo Dam','Raigarh','2024-25','22.20°N 83.47°E','1 calf'],
          ['Panikshet Dam (repeat)','Raigarh','2024-25','22.10°N 83.24°E','1 calf'],
          ['Mond River nala (DH S)','Dharamjaigarh','2025-26','22.17°N 83.17°E','Arsenic area'],
          ['Ghargoda nala (RG)','Raigarh','2025-26','Multiple','4 calves cluster'],
          ['Mond River (Kharsia)','Raigarh','2026-27','22.14°N 83.12°E','Pelvic fracture noted'],
          ['Gurda River (DH S)','Dharamjaigarh','2026-27','22.04°N 83.13°E','Gurda case study'],
          ['Pond (DH south)','Dharamjaigarh','2026-27','22.17°N 83.12°E','2026-27 cohort']],
         [42*mm,28*mm,20*mm,38*mm,WC-128*mm]),
    SP(5),
    alertbox('ARSENIC DETECTION: Tamnar Range (Raigarh Division), December 2025 — '
             'arsenic found in visceral samples from 2 specimens near Rabo/Panikshet dam corridor. '
             'Environmental water sampling of these catchments is urgently required.'),
    PageBreak(),
]

# ─── 11. GIS: ELECTROCUTION MAP ───────────────────────────────────────────────
story += [
    banner('11.  GIS — Electrocution Hotspot Analysis'),
    SP(8),
    m4,
    Paragraph('Figure 11: All electrocution + lightning deaths — year-coded from pale red (2021-22) '
              'to dark red (2025-26). Stars = lightning strikes; circles = electrocution. '
              'Non-electrocution deaths dimmed.', CAP),
    SP(5),
    Paragraph('11.1  Electrocution Spatial Patterns', CH2),
    B('<b>DH western cluster:</b> Chhal range (DH south) — 5 electrocution deaths across multiple years, '
      'indicating persistent illegal low-hung lines in the Koylar-Chhal agricultural corridor.'),
    B('<b>DH HQ cluster:</b> 5 electrocution deaths in Dharamjaigarh HQ area — '
      'crop-field perimeter fencing in active cultivation zones.'),
    B('<b>RG central cluster:</b> Ghargoda and Tamanar ranges — 7+4 = 11 electrocution deaths, '
      'heaviest concentration; Ghargoda is the single deadliest range.'),
    B('<b>Lightning strikes (2022-23):</b> Two in DH east (lon 83.45–83.75) — isolated events.'),
    B('<b>Peak season Oct–Dec</b> (harvest) is when most electrocution events cluster.'),
    PageBreak(),
]

# ─── 12. GIS: HUMAN CASUALTY MAP ──────────────────────────────────────────────
story += [
    banner('12.  GIS — Human Casualty Map (HEI Deaths 2021–2026)'),
    SP(8),
    m6,
    Paragraph('Figure 12: Human deaths from human-elephant interface (HEI) incidents — '
              'year-coded triangles. Elephant deaths shown dimmed for spatial reference. '
              'Total 45 human deaths across both divisions.', CAP),
    SP(5),
    Paragraph('12.1  Human Casualty Spatial Notes', CH2),
    B('<b>DH division (36 human deaths):</b> Concentrated in the Chhal-Borojh-Lailungaan corridor '
      '(DH south-west) — same zone with high elephant electrocution deaths, confirming shared '
      'forest-agriculture interface.'),
    B('<b>RG division (9 human deaths):</b> Scattered across Ghargoda-Tamanar area; '
      'lower human casualties despite higher elephant mortality.'),
    B('<b>2021-22 peak (13 human deaths)</b> and <b>2025-26 peak (16 human deaths)</b> '
      'correlate with years of high elephant movement and crop-harvest season overlap.'),
    dtbl(['Division','Human Deaths','Elephant Deaths','Deadliest Range (Human)'],
         [['Dharamjaigarh','36','27','Chhal (10) &gt; Borojh (9) &gt; Lailungaan (8)'],
          ['Raigarh','9','22','Ghargoda (5) &gt; others']],
         [35*mm,28*mm,32*mm,WC-95*mm]),
    PageBreak(),
]

# ─── 13. PM & LAB ANALYSIS ────────────────────────────────────────────────────
story += [
    banner('13.  Post-mortem &amp; Laboratory Analysis'),
    SP(8),
    Paragraph('13.1  PM Cause Distribution (41 confirmed PM records)', CH2),
    dtbl(['Cause','PM-Confirmed','%'],
         [['Electrocution → Cardio-Respiratory Failure','~20','49%'],
          ['Suspected Drowning','~9','22%'],
          ['Natural / Old Age','~5','12%'],
          ['Trauma / Fall','~5','12%'],
          ['Other / Undetermined','~2','5%']],
         [WC*0.55,WC*0.25,WC*0.20]),
    SP(6),
    Paragraph('13.2  Drowning — Consistent PM Findings (all 13 cases)', CH2),
    dtbl(['PM Finding','Frequency'],
         [['Frothy nasal/oral discharge — emphysema aquosum','ALL CASES'],
          ['Lungs waterlogged, heavy, congested, oedematous','ALL CASES'],
          ['Water in trachea &amp; bronchi','ALL CASES'],
          ['Gastric content — large volume of water &amp; plant debris','ALL CASES'],
          ['Skin maceration / hide wrinkling','CONSISTENT'],
          ['Petechial haemorrhages — conjunctiva / sub-pleural','VARIABLE'],
          ['Diatom test POSITIVE — ante-mortem drowning confirmed','ALL TESTED CASES']],
         [WC*0.62,WC*0.38]),
    SP(6),
    Paragraph('13.3  Histopathology', CH2),
    B('Pulmonary oedema — alveolar flooding with eosinophilic fluid.'),
    B('Pulmonary haemorrhage — interstitial and alveolar spaces.'),
    B('<b>Hepatocyte degeneration</b> in 3 cases — Tamnar Range, December 2025.'),
    B('Renal congestion — passive vascular engorgement.'),
    SP(6),
    Paragraph('13.4  Laboratory Results (ICAR-IVRI + NDVSU, 5 batches)', CH2),
    dtbl(['Test / Agent','Result','Note'],
         [['Arsenic','DETECTED ⚠','2 specimens, Tamnar Range RG, Dec 2025 — elevated in viscera'],
          ['EEHV-I PCR','NEGATIVE','Confirmed by ICAR-IVRI &amp; NDVSU Jabalpur — viral aetiology ruled out'],
          ['Nitrate-Nitrite','NEGATIVE','All 5 batches'],
          ['Organophosphates / Organochlorines','NEGATIVE','All 5 batches'],
          ['Heavy metals (Pb, Hg, Cd)','NEGATIVE','All 5 batches'],
          ['Hydrogen Cyanide (HCN)','NEGATIVE','All 5 batches']],
         [48*mm,28*mm,WC-76*mm]),
    SP(5),
    alertbox('ARSENIC: Environmental sampling of Rabo &amp; Panikshet dam catchments recommended '
             'immediately. Results to be shared with CG Pollution Control Board for enforcement action.'),
    PageBreak(),
]

# ─── 14. CASE STUDY ───────────────────────────────────────────────────────────
story += [
    banner('14.  Case Study — Gurda Elephant Calf Drowning · 01 June 2026'),
    SP(8),
    itbl([('Date','01 June 2026'),('Location','Gurda, Kharsia Range, Raigarh Van Mandal'),
          ('GPS','22.0439°N, 83.1313°E  (22°3′16″N 83°8′11″E)'),
          ('Elevation','256.04 ± 9.59 m'),('Water Body','Gurda River / exposed sandbank'),
          ('Species','Asian Elephant (Elephas maximus)'),('Age Class','Calf (0–2 yr)'),
          ('Cause','Suspected Drowning')]),
    SP(6),
    P('Calf found on an exposed sandbank adjacent to the Gurda River. Photographic documentation '
      'at 10:56 hrs (aerial view) and 11:03 hrs (carcass, ground level). Incident is consistent '
      'with the established <b>dry-season drowning pattern</b> — low water levels and steep banks '
      'trap calves that approach the edge to drink.'),
    SP(4),
    P('<i>Field note (original): हाथी निगरानी परिसर गुर्दा — Gurda परिक्षेत्र, खरसिया वनमण्डल रायगढ़।</i>'),
    SP(5),
    hibox('This case exemplifies the 2026-27 cohort: all 5 deaths are calves, all suspected '
          'drowning, all in first 3 months. Gurda is the southernmost recorded drowning '
          'event in Raigarh Division (22.04°N).'),
    PageBreak(),
]

# ─── 15. RECOMMENDATIONS ──────────────────────────────────────────────────────
story += [
    banner('15.  Key Findings, Recommendations &amp; Action Points'),
    SP(8),
    Paragraph('15.1  Summary Statistics', CH2),
    SP(4),
    dtbl(['Metric','Value'],
         [['Study Period','2021-22 to 2026-27 (ongoing)'],
          ['Total Elephant Deaths','49 confirmed'],
          ['Total Human Deaths (HEI)','45 confirmed'],
          ['Leading Cause (Elephant)','Electrocution — 23 deaths (47%)'],
          ['2nd Cause (Elephant)','Suspected Drowning — 13 deaths (27%)'],
          ['Most Vulnerable Age','Calves 0–2 yr — 23 deaths (50%)'],
          ['Record Year','2025-26 — 12 deaths'],
          ['2026-27 Signal','5 deaths in first 3 months — all calves, all drowning'],
          ['CRITICAL Ranges','Chhal (14) + Ghargoda (15) = 59% of all elephant deaths'],
          ['Drowning Season Peak','Jan–May = 62% of drowning deaths'],
          ['Electrocution Season Peak','Oct–Dec = 50% of electrocution deaths'],
          ['Arsenic Finding','Positive — 2 specimens, Tamnar Range, Dec 2025'],
          ['EEHV Status','Negative — all batches tested'],
          ['Toxicology Screen','Negative for nitrates, organophosphates, heavy metals, HCN'],
          ['Workshop Participants','84 — Forest Dept + Veterinary Service Dept, CG']],
         [WC*0.46,WC*0.54]),
    SP(8),
    Paragraph('15.2  Priority Action Matrix', CH2),
    SP(4),
    dtbl(['Priority','Action','Target Area','Timeline'],
         [['IMMEDIATE','Environmental water/sediment sampling','Rabo &amp; Panikshet dams (RG)','This week'],
          ['IMMEDIATE','Install earthen ramps at drowning sites','Chhal ponds + Ghargoda dam edge','Dry season'],
          ['IMMEDIATE','Power-line audit — low-hung lines','All CRITICAL ranges','This month'],
          ['SEASONAL','Enforcement — illegal crop fencing','All ranges','Oct–Dec annually'],
          ['SEASONAL','Dry-season calf monitoring','GPS herd watch near water bodies','Jan–May annually'],
          ['ONGOING','Mandatory PM within 24 hrs + sample dispatch 48 hrs','All ranges','Every event'],
          ['ANNUAL','EEHV surveillance + systematic documentation','All divisions','Annually'],
          ['QUARTERLY','Division mortality review meeting','Dharamjaigarh + Raigarh HQ','Every 3 months']],
         [25*mm,60*mm,50*mm,WC-135*mm]),
    SP(10),
    HR(DG,1.5),
    SP(5),
    Paragraph('<i>Data Sources: Proforma-1 Records, Dharamjaigarh &amp; Raigarh Divisions · '
              'PM Reports: ICAR-IVRI Izatnagar (F.2-19/DI/NRC/2025-26/CWL) · '
              'GIS Data: Bilaspur Forest Division GIS Cell · Generated: June 2026</i>',SM),
    Paragraph('<i>Organised by: Chhattisgarh Forest Department · '
              'Technical Support: WII, Dehradun · Lab: ICAR-IVRI &amp; NDVSU, Jabalpur</i>',SM),
]

# ── Build ──────────────────────────────────────────────────────────────────────
out='/home/user/Workshop-on-Conference/Workshop_GIS_Notes_2026.pdf'
doc=SimpleDocTemplate(out,pagesize=A4,leftMargin=36,rightMargin=36,
                      topMargin=48,bottomMargin=36,
                      title='Chapter 1 — Workshop Notes with GIS Maps — Elephant Mortality Investigation',
                      author='CG Forest Dept / WII')
doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
print(f'PDF saved: {out}')
print(f'Size: {os.path.getsize(out)/1024:.1f} KB')

#!/usr/bin/env python3
"""
Generate Chapter 1: Workshop Overview & Elephant Mortality Analysis in Chhattisgarh
Based on Workshop Illustrated Notes 2026 (15-page source PDF)
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
C_DARK   = HexColor('#1B4332')
C_MED    = HexColor('#2D6A4F')
C_LIGHT  = HexColor('#52B788')
C_TINT   = HexColor('#D8F3DC')
C_TINT2  = HexColor('#EAF7EE')
C_ORANGE = HexColor('#F4A261')
C_ORNG_L = HexColor('#FFF0E6')
C_GOLD   = HexColor('#E9C46A')
C_RED    = HexColor('#C0392B')
C_RED_L  = HexColor('#FADBD8')
C_NAVY   = HexColor('#1A2E4A')
C_BODY   = HexColor('#1A1A1A')
C_MUTED  = HexColor('#555555')
C_WHITE  = colors.white

PW, PH = A4
OUT = '/home/user/Workshop-on-Conference/Workshop_Chapter1_2026.pdf'


# ═══════════════════════════════════════════════════════════════════════════════
# Custom Flowables
# ═══════════════════════════════════════════════════════════════════════════════

class ChapterHeader(Flowable):
    """Full-width chapter title banner."""
    def __init__(self, chapter_num, title, subtitle='', author=''):
        Flowable.__init__(self)
        self.chapter_num = chapter_num
        self.title = title
        self.subtitle = subtitle
        self.author = author

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 120

    def draw(self):
        c = self.canv
        w, h = self.aw, 120
        c.setFillColor(C_DARK)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        # Accent strip
        c.setFillColor(C_LIGHT)
        c.rect(0, h - 6, w, 6, fill=1, stroke=0)
        # Chapter label
        c.setFillColor(C_LIGHT)
        c.setFont('Helvetica', 9)
        c.drawString(14, h - 22, f'CHAPTER {self.chapter_num}')
        # Title
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 16)
        title_y = h - 44
        c.drawString(14, title_y, self.title)
        # Subtitle
        if self.subtitle:
            c.setFillColor(C_TINT)
            c.setFont('Helvetica-Oblique', 10)
            c.drawString(14, title_y - 18, self.subtitle)
        # Author / org
        if self.author:
            c.setFillColor(C_TINT)
            c.setFont('Helvetica', 9)
            c.drawString(14, 14, self.author)


class SectionHeading(Flowable):
    """Green left-bar section heading."""
    def __init__(self, text, level=1):
        Flowable.__init__(self)
        self.text = text
        self.level = level

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 26 if self.level == 1 else 22

    def draw(self):
        c = self.canv
        w = self.aw
        h = 26 if self.level == 1 else 22
        if self.level == 1:
            c.setFillColor(C_MED)
            c.rect(0, 0, w, h, fill=1, stroke=0)
            c.setFillColor(C_WHITE)
            c.setFont('Helvetica-Bold', 11)
            c.drawString(10, 7, self.text)
        else:
            c.setFillColor(C_TINT)
            c.rect(0, 0, w, h, fill=1, stroke=0)
            c.setFillColor(C_DARK)
            c.rect(0, 0, 4, h, fill=1, stroke=0)
            c.setFillColor(C_DARK)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(10, 6, self.text)


class KeyBox(Flowable):
    """Highlighted key-fact box."""
    def __init__(self, text, danger=False, width=None):
        Flowable.__init__(self)
        self.text = text
        self.danger = danger
        self._width = width

    def wrap(self, aw, ah):
        self.aw = self._width or aw
        return self.aw, 36

    def draw(self):
        c = self.canv
        w = self.aw
        bg = C_RED_L if self.danger else C_TINT
        border = C_RED if self.danger else C_LIGHT
        c.setFillColor(bg)
        c.roundRect(0, 0, w, 36, 5, fill=1, stroke=0)
        c.setStrokeColor(border)
        c.setLineWidth(1.5)
        c.roundRect(0, 0, w, 36, 5, fill=0, stroke=1)
        c.setFillColor(C_RED if self.danger else C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(10, 13, self.text)


class StatCard(Flowable):
    """Small stat card with big number and label."""
    def __init__(self, number, label, color=None, width=120, height=60):
        Flowable.__init__(self)
        self.number = number
        self.label = label
        self.color = color or C_MED
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        return self.W, self.H

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.W, self.H, 6, fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 22)
        c.drawCentredString(self.W / 2, self.H - 36, str(self.number))
        c.setFont('Helvetica', 8)
        # wrap label if needed
        words = self.label.split()
        lines = []
        line = ''
        for w in words:
            test = (line + ' ' + w).strip()
            if c.stringWidth(test, 'Helvetica', 8) < self.W - 10:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        y = 22
        for ln in lines[:2]:
            c.drawCentredString(self.W / 2, y, ln)
            y -= 11


# ── Population Trend Bar Chart ─────────────────────────────────────────────────
class PopulationBarChart(Flowable):
    """Bar chart: Elephant population in Chhattisgarh 2001-2026."""
    def __init__(self, width=480, height=160):
        Flowable.__init__(self)
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        self.W = min(self.W, aw)
        return self.W, self.H

    def draw(self):
        c = self.canv
        W, H = self.W, self.H
        # Background
        c.setFillColor(C_TINT2)
        c.roundRect(0, 0, W, H, 5, fill=1, stroke=0)
        # Title
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H - 14, 'Elephant Population Growth in Chhattisgarh (2001–2026)')

        data = [
            ('2001', 24), ('2005', 123), ('2007', 122),
            ('2015', 247), ('2017', 247), ('2021', 279), ('2026', 451)
        ]
        max_val = 480
        n = len(data)
        margin_l, margin_r, margin_b, margin_t = 50, 15, 28, 28
        chart_w = W - margin_l - margin_r
        chart_h = H - margin_b - margin_t
        bar_gap = 8
        bar_w = (chart_w - bar_gap * (n - 1)) / n

        # Y-axis grid lines
        c.setStrokeColor(HexColor('#CCCCCC'))
        c.setLineWidth(0.4)
        for pct in [0.25, 0.5, 0.75, 1.0]:
            y = margin_b + pct * chart_h
            c.line(margin_l, y, W - margin_r, y)
            c.setFillColor(C_MUTED)
            c.setFont('Helvetica', 7)
            c.drawRightString(margin_l - 3, y - 3, str(int(pct * max_val)))

        # Bars
        for i, (year, val) in enumerate(data):
            x = margin_l + i * (bar_w + bar_gap)
            bh = val / max_val * chart_h
            # Gradient effect: lighter bar with darker top
            c.setFillColor(C_LIGHT)
            c.rect(x, margin_b, bar_w, bh, fill=1, stroke=0)
            c.setFillColor(C_MED)
            c.rect(x, margin_b + bh - 4, bar_w, 4, fill=1, stroke=0)
            # Value label
            c.setFillColor(C_DARK)
            c.setFont('Helvetica-Bold', 7)
            c.drawCentredString(x + bar_w / 2, margin_b + bh + 2, str(val))
            # Year label
            c.setFillColor(C_BODY)
            c.setFont('Helvetica', 7)
            c.drawCentredString(x + bar_w / 2, margin_b - 12, year)

        # Y-axis
        c.setStrokeColor(C_DARK)
        c.setLineWidth(1)
        c.line(margin_l, margin_b, margin_l, margin_b + chart_h)
        c.line(margin_l, margin_b, W - margin_r, margin_b)

        # CAGR note
        c.setFillColor(C_MED)
        c.setFont('Helvetica-Oblique', 7.5)
        c.drawRightString(W - margin_r, H - 14, 'CAGR ≈ 13% | Source: CG Forest Dept')


# ── Year-wise Deaths Bar Chart ─────────────────────────────────────────────────
class DeathsBarChart(Flowable):
    """Grouped bar chart: Year-wise elephant deaths by division."""
    def __init__(self, width=480, height=160):
        Flowable.__init__(self)
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        self.W = min(self.W, aw)
        return self.W, self.H

    def draw(self):
        c = self.canv
        W, H = self.W, self.H
        c.setFillColor(C_TINT2)
        c.roundRect(0, 0, W, H, 5, fill=1, stroke=0)
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H - 14, 'Year-wise Elephant Casualties in Chhattisgarh (2021–2027*)')

        # year, DH (Dharamjaigarh), RG (Raigarh), total
        data = [
            ('2021-22', 2, 2, 4),
            ('2022-23', 7, 5, 12),
            ('2023-24', 3, 3, 6),
            ('2024-25', 6, 4, 10),
            ('2025-26', 7, 5, 12),
            ('2026-27*', 2, 3, 5),
        ]
        max_val = 14
        n = len(data)
        margin_l, margin_r, margin_b, margin_t = 45, 80, 28, 28
        chart_w = W - margin_l - margin_r
        chart_h = H - margin_b - margin_t
        group_gap = 10
        inner_gap = 2
        group_w = (chart_w - group_gap * (n - 1)) / n
        bar_w = (group_w - inner_gap) / 2

        C_DH = C_MED
        C_RG = C_ORANGE

        # Grid
        c.setStrokeColor(HexColor('#CCCCCC'))
        c.setLineWidth(0.4)
        for pct in [0.25, 0.5, 0.75, 1.0]:
            y = margin_b + pct * chart_h
            c.line(margin_l, y, W - margin_r, y)
            c.setFillColor(C_MUTED)
            c.setFont('Helvetica', 7)
            c.drawRightString(margin_l - 3, y - 3, str(int(pct * max_val)))

        for i, (yr, dh, rg, tot) in enumerate(data):
            gx = margin_l + i * (group_w + group_gap)
            # DH bar
            bh_dh = dh / max_val * chart_h
            c.setFillColor(C_DH)
            c.rect(gx, margin_b, bar_w, bh_dh, fill=1, stroke=0)
            if dh:
                c.setFillColor(C_WHITE)
                c.setFont('Helvetica-Bold', 6)
                c.drawCentredString(gx + bar_w / 2, margin_b + bh_dh - 9, str(dh))
            # RG bar
            bh_rg = rg / max_val * chart_h
            c.setFillColor(C_RG)
            c.rect(gx + bar_w + inner_gap, margin_b, bar_w, bh_rg, fill=1, stroke=0)
            if rg:
                c.setFillColor(C_WHITE)
                c.setFont('Helvetica-Bold', 6)
                c.drawCentredString(gx + bar_w + inner_gap + bar_w / 2, margin_b + bh_rg - 9, str(rg))
            # Total label above
            c.setFillColor(C_DARK)
            c.setFont('Helvetica-Bold', 7)
            c.drawCentredString(gx + group_w / 2, margin_b + max(bh_dh, bh_rg) + 2, str(tot))
            # Year label
            c.setFillColor(C_BODY)
            c.setFont('Helvetica', 6.5)
            c.drawCentredString(gx + group_w / 2, margin_b - 12, yr)

        # Axes
        c.setStrokeColor(C_DARK)
        c.setLineWidth(1)
        c.line(margin_l, margin_b, margin_l, margin_b + chart_h)
        c.line(margin_l, margin_b, W - margin_r, margin_b)

        # Legend
        lx = W - margin_r + 8
        c.setFillColor(C_DH)
        c.rect(lx, H - 38, 10, 10, fill=1, stroke=0)
        c.setFillColor(C_BODY)
        c.setFont('Helvetica', 7)
        c.drawString(lx + 13, H - 38 + 1, 'DH Division')
        c.setFillColor(C_RG)
        c.rect(lx, H - 52, 10, 10, fill=1, stroke=0)
        c.setFillColor(C_BODY)
        c.drawString(lx + 13, H - 52 + 1, 'RG Division')
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica-Oblique', 6.5)
        c.drawString(lx, margin_b, '* ongoing')


# ── Cause of Death Horizontal Bar Chart ────────────────────────────────────────
class CauseOfDeathChart(Flowable):
    """Horizontal bar chart: Cause of death breakdown."""
    def __init__(self, width=480, height=140):
        Flowable.__init__(self)
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        self.W = min(self.W, aw)
        return self.W, self.H

    def draw(self):
        c = self.canv
        W, H = self.W, self.H
        c.setFillColor(C_TINT2)
        c.roundRect(0, 0, W, H, 5, fill=1, stroke=0)
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H - 14, 'Cause of Death Analysis (2021–2026, n=49)')

        causes = [
            ('Electrocution', 23, 47, C_RED),
            ('Drowning',      13, 27, HexColor('#2980B9')),
            ('Natural / Old Age', 4, 8, C_MED),
            ('Fall / Trauma',     4, 8, C_ORANGE),
            ('Other',             5, 10, C_GOLD),
        ]
        max_pct = 50
        margin_l, margin_r, margin_b, margin_t = 130, 70, 18, 26
        chart_w = W - margin_l - margin_r
        chart_h = H - margin_b - margin_t
        n = len(causes)
        bar_h = chart_h / n - 6

        for i, (label, count, pct, col) in enumerate(causes):
            y = margin_b + (n - 1 - i) * (chart_h / n)
            bw = pct / max_pct * chart_w
            # Bar
            c.setFillColor(col)
            c.roundRect(margin_l, y + 2, bw, bar_h, 3, fill=1, stroke=0)
            # Label
            c.setFillColor(C_DARK)
            c.setFont('Helvetica', 8)
            c.drawRightString(margin_l - 6, y + bar_h / 2 - 3, label)
            # Value
            c.setFillColor(C_DARK)
            c.setFont('Helvetica-Bold', 8)
            c.drawString(margin_l + bw + 4, y + bar_h / 2 - 3, f'{count} ({pct}%)')

        # Note
        c.setFillColor(C_RED)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawCentredString(W / 2, 4, 'Electrocution + Drowning = 74% — PREVENTABLE deaths')


# ── Seasonal Variation Chart ────────────────────────────────────────────────────
class SeasonalChart(Flowable):
    """Grouped bar chart: Seasonal death distribution."""
    def __init__(self, width=480, height=140):
        Flowable.__init__(self)
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        self.W = min(self.W, aw)
        return self.W, self.H

    def draw(self):
        c = self.canv
        W, H = self.W, self.H
        c.setFillColor(C_TINT2)
        c.roundRect(0, 0, W, H, 5, fill=1, stroke=0)
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H - 14, 'Seasonal Variation in Elephant Deaths')

        seasons = [
            ('Jan–May\n(Dry)', 8, 6),
            ('Jun–Sep\n(Monsoon)', 1, 5),
            ('Oct–Dec\n(Harvest)', 4, 10),
        ]
        max_val = 12
        n = len(seasons)
        margin_l, margin_r, margin_b, margin_t = 40, 90, 32, 28
        chart_w = W - margin_l - margin_r
        chart_h = H - margin_b - margin_t
        group_gap = 20
        inner_gap = 4
        group_w = (chart_w - group_gap * (n - 1)) / n
        bar_w = (group_w - inner_gap) / 2

        C_DROWN = HexColor('#2980B9')
        C_ELEC = C_RED

        # Grid
        c.setStrokeColor(HexColor('#CCCCCC'))
        c.setLineWidth(0.4)
        for pct in [0.25, 0.5, 0.75, 1.0]:
            y = margin_b + pct * chart_h
            c.line(margin_l, y, W - margin_r, y)
            c.setFillColor(C_MUTED)
            c.setFont('Helvetica', 7)
            c.drawRightString(margin_l - 3, y - 3, str(int(pct * max_val)))

        for i, (season_lbl, drown, elec) in enumerate(seasons):
            gx = margin_l + i * (group_w + group_gap)
            # Drowning bar
            bh_d = drown / max_val * chart_h
            c.setFillColor(C_DROWN)
            c.rect(gx, margin_b, bar_w, bh_d, fill=1, stroke=0)
            if drown:
                c.setFillColor(C_WHITE)
                c.setFont('Helvetica-Bold', 7)
                c.drawCentredString(gx + bar_w / 2, margin_b + bh_d / 2 - 4, str(drown))
            # Electrocution bar
            bh_e = elec / max_val * chart_h
            c.setFillColor(C_ELEC)
            c.rect(gx + bar_w + inner_gap, margin_b, bar_w, bh_e, fill=1, stroke=0)
            if elec:
                c.setFillColor(C_WHITE)
                c.setFont('Helvetica-Bold', 7)
                c.drawCentredString(gx + bar_w + inner_gap + bar_w / 2, margin_b + bh_e / 2 - 4, str(elec))
            # Season label (2-line)
            lines_s = season_lbl.split('\n')
            c.setFillColor(C_BODY)
            c.setFont('Helvetica', 7)
            for j, ln in enumerate(lines_s):
                c.drawCentredString(gx + group_w / 2, margin_b - 13 - j * 9, ln)

        # Axes
        c.setStrokeColor(C_DARK)
        c.setLineWidth(1)
        c.line(margin_l, margin_b, margin_l, margin_b + chart_h)
        c.line(margin_l, margin_b, W - margin_r, margin_b)

        # Legend
        lx = W - margin_r + 8
        c.setFillColor(C_DROWN)
        c.rect(lx, H - 40, 10, 10, fill=1, stroke=0)
        c.setFillColor(C_BODY)
        c.setFont('Helvetica', 7.5)
        c.drawString(lx + 13, H - 40 + 1, 'Drowning')
        c.setFillColor(C_ELEC)
        c.rect(lx, H - 55, 10, 10, fill=1, stroke=0)
        c.setFillColor(C_BODY)
        c.drawString(lx + 13, H - 55 + 1, 'Electrocution')
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica-Oblique', 6.5)
        c.drawString(lx, H - 70, 'Total = 49')


# ── Age/Sex Demographics Chart ──────────────────────────────────────────────────
class DemographicsChart(Flowable):
    """Side-by-side: Age group + Sex breakdown horizontal bars."""
    def __init__(self, width=480, height=130):
        Flowable.__init__(self)
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        self.W = min(self.W, aw)
        return self.W, self.H

    def draw(self):
        c = self.canv
        W, H = self.W, self.H
        c.setFillColor(C_TINT2)
        c.roundRect(0, 0, W, H, 5, fill=1, stroke=0)

        half = W / 2 - 5
        # Divider
        c.setStrokeColor(C_LIGHT)
        c.setLineWidth(0.8)
        c.line(W / 2, 8, W / 2, H - 8)

        # ── Left: Age groups ──
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawCentredString(half / 2, H - 14, 'Deaths by Age Group (n=46)')

        ages = [
            ('Calf (0-2 yr)', 23, 50, HexColor('#2ECC71')),
            ('Juvenile',       5, 11, HexColor('#27AE60')),
            ('Sub-adult',      2,  4, HexColor('#1ABC9C')),
            ('Adult',         11, 24, HexColor('#16A085')),
            ('Old',            5, 11, HexColor('#0E6655')),
        ]
        max_pct = 55
        ml, mr = 80, 10
        cw_l = half - ml - mr
        ch_l = H - 30 - 18
        n = len(ages)
        bh = ch_l / n - 4

        for i, (label, count, pct, col) in enumerate(ages):
            y = 18 + (n - 1 - i) * (ch_l / n)
            bw = pct / max_pct * cw_l
            c.setFillColor(col)
            c.roundRect(ml, y, bw, bh, 2, fill=1, stroke=0)
            c.setFillColor(C_DARK)
            c.setFont('Helvetica', 7)
            c.drawRightString(ml - 4, y + bh / 2 - 3, label)
            c.setFont('Helvetica-Bold', 7)
            c.drawString(ml + bw + 3, y + bh / 2 - 3, f'{count} ({pct}%)')

        # ── Right: Sex breakdown ──
        rx = W / 2 + 5
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawCentredString(rx + half / 2 - 5, H - 14, 'Deaths by Sex (n=45)')

        sex_data = [
            ('Male',   23, 51, HexColor('#2980B9')),
            ('Female', 22, 49, HexColor('#E74C3C')),
        ]
        ml2 = 60
        cw_r = half - ml2 - 10
        bh2 = 18

        for i, (label, count, pct, col) in enumerate(sex_data):
            y = H - 40 - i * 32
            bw2 = pct / 55 * cw_r
            c.setFillColor(col)
            c.roundRect(rx + ml2, y, bw2, bh2, 3, fill=1, stroke=0)
            c.setFillColor(C_DARK)
            c.setFont('Helvetica', 8)
            c.drawRightString(rx + ml2 - 4, y + bh2 / 2 - 4, label)
            c.setFont('Helvetica-Bold', 8)
            c.drawString(rx + ml2 + bw2 + 4, y + bh2 / 2 - 4, f'{count} ({pct}%)')

        # Note about electrocution sex difference
        c.setFillColor(C_RED)
        c.setFont('Helvetica-Oblique', 7)
        c.drawCentredString(rx + half / 2 - 5, 8,
                            '48% male deaths = electrocution; 33% female')


# ── Monthly Deaths Timeline ─────────────────────────────────────────────────────
class MonthlyDeathsChart(Flowable):
    """Bar chart showing deaths by month with October peak highlighted."""
    def __init__(self, width=480, height=120):
        Flowable.__init__(self)
        self.W = width
        self.H = height

    def wrap(self, aw, ah):
        self.W = min(self.W, aw)
        return self.W, self.H

    def draw(self):
        c = self.canv
        W, H = self.W, self.H
        c.setFillColor(C_TINT2)
        c.roundRect(0, 0, W, H, 5, fill=1, stroke=0)
        c.setFillColor(C_DARK)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, H - 14, 'Monthly Distribution of Elephant Deaths (Oct = Peak Month)')

        # Monthly distribution (approximate from source data)
        months = [
            ('J', 2), ('F', 1), ('M', 1), ('A', 2), ('M', 2),
            ('J', 1), ('J', 2), ('A', 1), ('S', 2),
            ('O', 8), ('N', 5), ('D', 7),
        ]
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        max_val = 10
        margin_l, margin_r, margin_b, margin_t = 30, 15, 22, 24
        chart_w = W - margin_l - margin_r
        chart_h = H - margin_b - margin_t
        bar_gap = 3
        bar_w = (chart_w - bar_gap * 11) / 12

        for i, (lbl, val) in enumerate(months):
            x = margin_l + i * (bar_w + bar_gap)
            bh = val / max_val * chart_h
            col = C_RED if i == 9 else (HexColor('#E67E22') if i in (10, 11) else C_LIGHT)
            c.setFillColor(col)
            c.rect(x, margin_b, bar_w, bh, fill=1, stroke=0)
            if val > 0:
                c.setFillColor(C_DARK)
                c.setFont('Helvetica-Bold', 6.5)
                c.drawCentredString(x + bar_w / 2, margin_b + bh + 1, str(val))
            c.setFillColor(C_BODY)
            c.setFont('Helvetica', 6.5)
            c.drawCentredString(x + bar_w / 2, margin_b - 11, month_names[i][:3])

        c.setStrokeColor(C_DARK)
        c.setLineWidth(1)
        c.line(margin_l, margin_b, margin_l, margin_b + chart_h)
        c.line(margin_l, margin_b, W - margin_r, margin_b)

        c.setFillColor(C_RED)
        c.setFont('Helvetica-Oblique', 7)
        c.drawRightString(W - margin_r, H - 14, 'Oct–Dec = 42% of annual deaths')


# ═══════════════════════════════════════════════════════════════════════════════
# Styles
# ═══════════════════════════════════════════════════════════════════════════════

def make_styles():
    base = getSampleStyleSheet()
    def S(name, **kw):
        return ParagraphStyle(name, parent=base['Normal'], **kw)

    return {
        'body':    S('body',    fontSize=9,  leading=14, textColor=C_BODY, spaceAfter=4,
                     fontName='Helvetica'),
        'bodyJ':   S('bodyJ',   fontSize=9,  leading=14, textColor=C_BODY, spaceAfter=4,
                     fontName='Helvetica', alignment=TA_JUSTIFY),
        'small':   S('small',   fontSize=8,  leading=12, textColor=C_MUTED),
        'bold':    S('bold',    fontSize=9,  leading=14, textColor=C_DARK, fontName='Helvetica-Bold'),
        'caption': S('caption', fontSize=7.5,leading=11, textColor=C_MUTED, alignment=TA_CENTER),
        'bullet':  S('bullet',  fontSize=8.5,leading=13, textColor=C_BODY,
                     fontName='Helvetica', leftIndent=12, bulletIndent=0),
        'th':      S('th',      fontSize=8.5,leading=12, textColor=C_WHITE,
                     fontName='Helvetica-Bold', alignment=TA_CENTER),
        'td':      S('td',      fontSize=8,  leading=12, textColor=C_BODY,
                     fontName='Helvetica'),
        'tdc':     S('tdc',     fontSize=8,  leading=12, textColor=C_BODY,
                     fontName='Helvetica', alignment=TA_CENTER),
        'tdb':     S('tdb',     fontSize=8,  leading=12, textColor=C_DARK,
                     fontName='Helvetica-Bold'),
    }

STYLES = make_styles()

# ── Table helpers ──────────────────────────────────────────────────────────────
def base_ts(col_count):
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_MED),
        ('TEXTCOLOR',  (0, 0), (-1, 0), C_WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, 0), 8.5),
        ('ALIGN',      (0, 0), (-1, 0), 'CENTER'),
        ('GRID',       (0, 0), (-1, -1), 0.4, HexColor('#BBBBBB')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_TINT2]),
        ('FONTNAME',   (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',   (0, 1), (-1, -1), 8),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])


def P(txt, st='body'):
    return Paragraph(txt, STYLES[st])


def SP(h=4):
    return Spacer(1, h)


def HR():
    return HRFlowable(width='100%', thickness=0.5, color=C_LIGHT, spaceAfter=4, spaceBefore=4)


# ── Page template ──────────────────────────────────────────────────────────────
def header_footer(canvas, doc):
    canvas.saveState()
    PW2, PH2 = A4
    # Header bar
    canvas.setFillColor(C_DARK)
    canvas.rect(0, PH2 - 28, PW2, 28, fill=1, stroke=0)
    canvas.setFillColor(C_WHITE)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(20, PH2 - 18,
        'Workshop on Essentials for Mortality Investigation of Asian Elephant | Raigarh, 5–6 June 2026')
    canvas.setFont('Helvetica', 7.5)
    canvas.drawRightString(PW2 - 20, PH2 - 18, f'Chapter 1  |  Page {doc.page}')
    # Footer
    canvas.setFillColor(C_DARK)
    canvas.rect(0, 0, PW2, 18, fill=1, stroke=0)
    canvas.setFillColor(C_TINT)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(20, 5, 'Chhattisgarh Forest Department  ·  Technical Support: WII Dehradun')
    canvas.drawRightString(PW2 - 20, 5, 'ICAR-IVRI  ·  NDVSU Jabalpur')
    canvas.restoreState()


# ═══════════════════════════════════════════════════════════════════════════════
# Content builders
# ═══════════════════════════════════════════════════════════════════════════════

def build_story():
    story = []
    add = story.append

    # ── Chapter header ─────────────────────────────────────────────────────────
    add(ChapterHeader(
        '1',
        'Workshop Overview & Elephant Mortality Analysis',
        'Chhattisgarh 2021–2026: Trends, Causes & Recommendations',
        'Chhattisgarh Forest Department  |  Technical Support: WII Dehradun'
    ))
    add(SP(10))

    # ── Section 1: Workshop Background ────────────────────────────────────────
    add(SectionHeading('1. Workshop Background & Objectives'))
    add(SP(6))

    add(P(
        'The <b>Workshop on Essentials for Mortality Investigation of Asian Elephant</b> was '
        'organised by the Chhattisgarh Forest Department with technical support from the '
        'Wildlife Institute of India (WII), Dehradun, and laboratory partners ICAR-IVRI, '
        'Bareilly and NDVSU, Jabalpur. The two-day programme (5–6 June 2026, Raigarh) '
        'brought together field officers and wildlife veterinarians to build capacity in '
        'systematic elephant necropsy, sample collection, disease diagnosis, and evidence-based '
        'mortality investigations.', 'bodyJ'
    ))
    add(SP(6))

    # Stats row
    stat_data = [
        [StatCard('84', 'Participants', C_MED, 105, 60),
         StatCard('2', 'Days Training', C_MED, 105, 60),
         StatCard('5', 'Expert Resource Persons', C_MED, 105, 60),
         StatCard('3', 'Partner Institutions', C_MED, 105, 60)],
    ]
    stat_tbl = Table(stat_data, colWidths=[110]*4)
    stat_tbl.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1), 4),
        ('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('TOPPADDING',(0,0),(-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1), 0),
    ]))
    add(stat_tbl)
    add(SP(8))

    add(SectionHeading('Workshop Objectives', level=2))
    add(SP(4))
    obj_data = [
        [P('Theme', 'th'), P('Topics Covered', 'th')],
        [P('Biology & Ecology', 'tdb'),
         P('Biology, behaviour, ecology of Asian elephants; population dynamics in CG', 'td')],
        [P('Pathology & Disease', 'tdb'),
         P('Necropsy procedures, biosafety, sample collection, infectious & non-infectious diseases', 'td')],
        [P('Surveillance & Response', 'tdb'),
         P('Elephant surveillance systems, disposal protocols, site remediation, evidence documentation', 'td')],
    ]
    obj_tbl = Table(obj_data, colWidths=[120, 340])
    obj_tbl.setStyle(base_ts(2))
    add(obj_tbl)
    add(SP(6))

    add(SectionHeading('Resource Persons', level=2))
    add(SP(4))
    rp_data = [
        [P('Name', 'th'), P('Institution', 'th'), P('Expertise', 'th')],
        [P('Dr. A. B. Shrivastav', 'tdb'), P('NDVSU, Jabalpur', 'td'),
         P('Wildlife Pathology, Elephant PM Examination', 'td')],
        [P('Dr. Parag Nigam', 'tdb'), P('WII, Dehradun', 'td'),
         P('Elephant Ecology & Population Biology', 'td')],
        [P('Dr. Karikalan Mathesh', 'tdb'), P('ICAR-IVRI, Bareilly', 'td'),
         P('Veterinary Pathology, Sample Diagnostics', 'td')],
        [P('Dr. Tapendra Saini', 'tdb'), P('WII, Dehradun', 'td'),
         P('Wildlife Surveillance & Disease Monitoring', 'td')],
        [P('Dr. Chandra Prakash Sharma', 'tdb'), P('WII, Dehradun', 'td'),
         P('Conservation Biology & Field Investigation', 'td')],
    ]
    rp_tbl = Table(rp_data, colWidths=[145, 145, 170])
    rp_tbl.setStyle(base_ts(3))
    add(rp_tbl)
    add(SP(10))

    # ── Section 2: Population Status ──────────────────────────────────────────
    add(SectionHeading('2. Elephant Population Status in Chhattisgarh'))
    add(SP(6))
    add(P(
        'Chhattisgarh has witnessed a remarkable expansion of its elephant population over the '
        'past two decades. Elephants, originally transient from Odisha and Jharkhand, have '
        'established resident breeding populations across two Forest Divisions: '
        '<b>Dharamjaigarh (DH)</b> and <b>Raigarh (RG)</b>. The population has grown from '
        'just 24 individuals in 2001 to an estimated <b>451 in 2026</b>, representing a '
        'Compound Annual Growth Rate (CAGR) of approximately 13%.', 'bodyJ'
    ))
    add(SP(6))
    add(PopulationBarChart(width=460, height=165))
    add(P('Figure 1: Elephant population growth in Chhattisgarh (2001–2026). '
          'Bilaspur Circle holds the highest concentration.', 'caption'))
    add(SP(6))

    pop_data = [
        [P('Year', 'th'), P('Population Count', 'th'), P('Remarks', 'th')],
        [P('2001', 'tdc'), P('24', 'tdc'), P('First recorded transient elephants from Odisha', 'td')],
        [P('2005', 'tdc'), P('123', 'tdc'), P('Rapid establishment of resident herds', 'td')],
        [P('2007', 'tdc'), P('122', 'tdc'), P('Stable — consolidation phase', 'td')],
        [P('2015', 'tdc'), P('247', 'tdc'), P('Continued range expansion into new areas', 'td')],
        [P('2017', 'tdc'), P('247', 'tdc'), P('Stable count; human-elephant conflict rising', 'td')],
        [P('2021', 'tdc'), P('279', 'tdc'), P('Post-COVID survey — increased mortality recorded', 'td')],
        [P('2026', 'tdc'), P('~451', 'tdc'), P('<b>Estimated</b> — highest ever; detailed census ongoing', 'tdb')],
    ]
    pop_tbl = Table(pop_data, colWidths=[70, 120, 270])
    pop_tbl.setStyle(base_ts(3))
    add(pop_tbl)
    add(SP(10))

    add(PageBreak())

    # ── Section 3: Casualty Analysis ──────────────────────────────────────────
    add(SectionHeading('3. Elephant Casualty Analysis (2021–2026)'))
    add(SP(6))
    add(KeyBox(
        'TOTAL: 49 Elephant Deaths | DH Division: 27 | RG Division: 22  |  '
        '2025-26: 12 deaths (RECORD HIGH) — Immediate intervention required',
        danger=True
    ))
    add(SP(8))
    add(DeathsBarChart(width=460, height=165))
    add(P('Figure 2: Year-wise elephant casualties by division (DH = Dharamjaigarh, RG = Raigarh). '
          '* 2026-27 data as of June 2026 (ongoing year).', 'caption'))
    add(SP(6))

    death_data = [
        [P('Year', 'th'), P('DH Division', 'th'), P('RG Division', 'th'),
         P('Total', 'th'), P('Remarks', 'th')],
        [P('2021-22', 'tdc'), P('2', 'tdc'), P('2', 'tdc'), P('4', 'tdc'),
         P('Baseline year — low mortality', 'td')],
        [P('2022-23', 'tdc'), P('7', 'tdc'), P('5', 'tdc'), P('12', 'tdc'),
         P('Surge in deaths — monsoon related', 'td')],
        [P('2023-24', 'tdc'), P('3', 'tdc'), P('3', 'tdc'), P('6', 'tdc'),
         P('Relatively low year', 'td')],
        [P('2024-25', 'tdc'), P('6', 'tdc'), P('4', 'tdc'), P('10', 'tdc'),
         P('Rising trend resumes', 'td')],
        [P('2025-26', 'tdc'), P('7', 'tdc'), P('5', 'tdc'), P('<b>12</b>', 'tdc'),
         P('<b>Record high — electrocution predominant</b>', 'tdb')],
        [P('2026-27*', 'tdc'), P('2', 'tdc'), P('3', 'tdc'), P('5*', 'tdc'),
         P('Ongoing year (as of June 2026)', 'td')],
        [P('<b>TOTAL</b>', 'tdb'), P('<b>27</b>', 'tdb'), P('<b>22</b>', 'tdb'),
         P('<b>49</b>', 'tdb'), P('<b>Cumulative 2021-2026</b>', 'tdb')],
    ]
    death_tbl = Table(death_data, colWidths=[70, 80, 80, 60, 170])
    ts = base_ts(5)
    ts.add('BACKGROUND', (0, 7), (-1, 7), C_TINT)
    death_tbl.setStyle(ts)
    add(death_tbl)
    add(SP(6))

    # Human deaths note
    add(SectionHeading('Human Casualties in Human-Elephant Conflict', level=2))
    add(SP(4))
    add(P(
        'Alongside elephant deaths, the ongoing human-elephant conflict has resulted in '
        '<b>45 human deaths</b> during 2021–2026 '
        '(DH: 36 deaths | RG: 9 deaths). This underscores the urgency of conflict '
        'mitigation alongside mortality investigation capacity.', 'bodyJ'
    ))
    add(SP(10))

    # ── Section 4: Cause of Death ─────────────────────────────────────────────
    add(SectionHeading('4. Cause of Death Analysis'))
    add(SP(6))
    add(CauseOfDeathChart(width=460, height=145))
    add(P('Figure 3: Cause of death distribution (n=49). Electrocution and drowning account for '
          '74% of all deaths — both are largely preventable with targeted interventions.', 'caption'))
    add(SP(6))

    cod_data = [
        [P('Cause of Death', 'th'), P('Count', 'th'), P('Percentage', 'th'),
         P('Key Mechanism', 'th')],
        [P('<b>Electrocution</b>', 'tdb'), P('23', 'tdc'), P('47%', 'tdc'),
         P('Stray power lines, illegal electric fencing around crops', 'td')],
        [P('<b>Drowning</b>', 'tdb'), P('13', 'tdc'), P('27%', 'tdc'),
         P('Calves unable to exit water bodies; steep banks, dams', 'td')],
        [P('Natural / Old Age', 'td'), P('4', 'tdc'), P('8%', 'tdc'),
         P('Multi-molar loss, senility — natural attrition', 'td')],
        [P('Fall / Trauma', 'td'), P('4', 'tdc'), P('8%', 'tdc'),
         P('Steep terrain, mine shafts, road/rail conflict', 'td')],
        [P('Other / Undetermined', 'td'), P('5', 'tdc'), P('10%', 'tdc'),
         P('Toxicology pending, disease, inter-elephant conflict', 'td')],
    ]
    cod_tbl = Table(cod_data, colWidths=[110, 50, 75, 225])
    ts2 = base_ts(4)
    ts2.add('BACKGROUND', (0, 1), (-1, 2), C_RED_L)
    ts2.add('FONTNAME', (0, 1), (0, 2), 'Helvetica-Bold')
    cod_tbl.setStyle(ts2)
    add(cod_tbl)
    add(SP(10))

    add(PageBreak())

    # ── Section 5: Demographics ───────────────────────────────────────────────
    add(SectionHeading('5. Demographic Analysis of Casualties'))
    add(SP(6))
    add(DemographicsChart(width=460, height=135))
    add(P('Figure 4: Age group (left) and sex (right) distribution of casualties (n=46 and n=45 respectively). '
          'Calves are disproportionately affected — 50% of all deaths.', 'caption'))
    add(SP(6))

    demo_data = [
        [P('Age Category', 'th'), P('Count', 'th'), P('%', 'th'), P('Key Vulnerability', 'th')],
        [P('Calf (0–2 yr)', 'tdb'), P('23', 'tdc'), P('50%', 'tdc'),
         P('Drowning (calves cannot exit steep banks), electrocution', 'td')],
        [P('Juvenile (2–5 yr)', 'td'), P('5', 'tdc'), P('11%', 'tdc'),
         P('Separation from herd, foraging near crop fields', 'td')],
        [P('Sub-adult (5–15 yr)', 'td'), P('2', 'tdc'), P('4%', 'tdc'),
         P('Dispersing males — increased exposure to power lines', 'td')],
        [P('Adult (15–40 yr)', 'td'), P('11', 'tdc'), P('24%', 'tdc'),
         P('Electrocution in bulls; old cow mortality', 'td')],
        [P('Old (>40 yr)', 'td'), P('5', 'tdc'), P('11%', 'tdc'),
         P('Natural senility, molar exhaustion, starvation', 'td')],
    ]
    demo_tbl = Table(demo_data, colWidths=[100, 55, 45, 260])
    demo_tbl.setStyle(base_ts(4))
    add(demo_tbl)
    add(SP(8))

    add(KeyBox(
        'CRITICAL: Calves (0-2 yr) account for 50% of all deaths and 92% of all drowning deaths. '
        'Drowning prevention infrastructure is the single highest-impact intervention.', danger=True
    ))
    add(SP(10))

    # ── Section 6: Seasonal Variation ─────────────────────────────────────────
    add(SectionHeading('6. Seasonal Variation in Mortality'))
    add(SP(6))
    add(SeasonalChart(width=460, height=145))
    add(P('Figure 5: Seasonal distribution of deaths by cause. October is the single deadliest month (8 deaths). '
          'Oct–Dec harvest season accounts for 42% of annual deaths.', 'caption'))
    add(SP(6))

    add(MonthlyDeathsChart(width=460, height=125))
    add(P('Figure 6: Monthly distribution of all elephant deaths (2021–2026 combined). '
          'October–December forms a clear mortality peak driven by illegal electric fencing during harvest.', 'caption'))
    add(SP(6))

    season_data = [
        [P('Season', 'th'), P('Months', 'th'), P('Drowning', 'th'),
         P('Electrocution', 'th'), P('Key Driver', 'th')],
        [P('Dry Season', 'tdb'), P('Jan–May', 'tdc'), P('8', 'tdc'), P('6', 'tdc'),
         P('Low water levels — calves trapped in drying pools / tanks', 'td')],
        [P('Monsoon', 'tdb'), P('Jun–Sep', 'tdc'), P('1', 'tdc'), P('5', 'tdc'),
         P('Flooded rivers, reduced visibility of power lines', 'td')],
        [P('<b>Harvest Season</b>', 'tdb'), P('<b>Oct–Dec</b>', 'tdc'), P('<b>4</b>', 'tdc'),
         P('<b>10</b>', 'tdc'),
         P('<b>PEAK: Illegal electric fencing to protect paddy/maize crops</b>', 'tdb')],
        [P('<b>TOTAL</b>', 'tdb'), P('—', 'tdc'), P('<b>13</b>', 'tdb'),
         P('<b>21*</b>', 'tdb'), P('*excludes 2 unconfirmed electrocution deaths', 'td')],
    ]
    season_tbl = Table(season_data, colWidths=[80, 70, 65, 75, 170])
    ts3 = base_ts(5)
    ts3.add('BACKGROUND', (0, 3), (-1, 3), C_RED_L)
    ts3.add('BACKGROUND', (0, 4), (-1, 4), C_TINT)
    season_tbl.setStyle(ts3)
    add(season_tbl)
    add(SP(10))

    add(PageBreak())

    # ── Section 7: Range-wise Distribution ────────────────────────────────────
    add(SectionHeading('7. Range-wise Distribution of Deaths'))
    add(SP(6))
    add(P(
        'Analysis of death locations reveals distinct spatial hotspots that require '
        'targeted management interventions. Two ranges account for 59% of all deaths '
        'and warrant immediate priority action.', 'bodyJ'
    ))
    add(SP(6))

    range_data = [
        [P('Forest Range', 'th'), P('Division', 'th'), P('Elec.', 'th'),
         P('Drown.', 'th'), P('Other', 'th'), P('Total', 'th'), P('Status', 'th')],
        [P('<b>Ghargoda</b>', 'tdb'), P('RG', 'tdc'), P('8', 'tdc'), P('5', 'tdc'),
         P('2', 'tdc'), P('<b>15</b>', 'tdb'), P('<b>CRITICAL</b>', 'tdb')],
        [P('<b>Chhal</b>', 'tdb'), P('DH', 'tdc'), P('7', 'tdc'), P('5', 'tdc'),
         P('2', 'tdc'), P('<b>14</b>', 'tdb'), P('<b>CRITICAL</b>', 'tdb')],
        [P('Dharamjaigarh', 'td'), P('DH', 'tdc'), P('3', 'tdc'), P('2', 'tdc'),
         P('1', 'tdc'), P('6', 'tdc'), P('HIGH', 'td')],
        [P('Kharsia', 'td'), P('RG', 'tdc'), P('2', 'tdc'), P('1', 'tdc'),
         P('1', 'tdc'), P('4', 'tdc'), P('MODERATE', 'td')],
        [P('Tamnar', 'td'), P('RG', 'tdc'), P('2', 'tdc'), P('1', 'tdc'),
         P('1', 'tdc'), P('4', 'tdc'), P('MODERATE', 'td')],
        [P('Other Ranges', 'td'), P('—', 'tdc'), P('1', 'tdc'), P('—', 'tdc'),
         P('5', 'tdc'), P('6', 'tdc'), P('Monitor', 'td')],
        [P('<b>TOTAL</b>', 'tdb'), P('—', 'tdc'), P('<b>23</b>', 'tdb'),
         P('<b>13</b>', 'tdb'), P('<b>13</b>', 'tdb'), P('<b>49</b>', 'tdb'),
         P('—', 'tdc')],
    ]
    range_tbl = Table(range_data, colWidths=[100, 55, 45, 55, 50, 50, 105])
    ts4 = base_ts(7)
    ts4.add('BACKGROUND', (0, 1), (-1, 2), C_RED_L)
    ts4.add('BACKGROUND', (0, 7), (-1, 7), C_TINT)
    range_tbl.setStyle(ts4)
    add(range_tbl)
    add(SP(6))

    add(SectionHeading('Human Conflict Hotspots', level=2))
    add(SP(4))
    hotspot_data = [
        [P('Range', 'th'), P('Human Deaths', 'th'), P('Priority Status', 'th')],
        [P('Chhal', 'tdb'), P('10', 'tdc'), P('HIGHEST PRIORITY — targeted patrol + power audit', 'td')],
        [P('Borojh', 'tdb'), P('9', 'tdc'), P('HIGH — community early warning system needed', 'td')],
        [P('Lailungaan', 'tdb'), P('8', 'tdc'), P('HIGH — corridor mapping and fencing required', 'td')],
        [P('Total (45 deaths)', 'tdb'), P('45', 'tdc'), P('Comprehensive conflict mitigation plan required', 'td')],
    ]
    hot_tbl = Table(hotspot_data, colWidths=[100, 110, 250])
    hot_tbl.setStyle(base_ts(3))
    add(hot_tbl)
    add(SP(10))

    # ── Section 8: Drowning PM Analysis ───────────────────────────────────────
    add(SectionHeading('8. Suspected Drowning — Post-Mortem Analysis'))
    add(SP(6))

    add(KeyBox(
        'KEY FINDING: Drowning = 13 deaths (27% of total). 92% of drowning victims were calves. '
        'ARSENIC DETECTED in 2 drowning specimens — potential water contamination (Tamnar Range, Dec 2025)',
        danger=True
    ))
    add(SP(8))

    add(P(
        'All 13 suspected drowning deaths underwent systematic post-mortem examination. '
        'Consistent PM findings confirmed asphyxia/drowning as the primary cause. '
        'Critically, diatom testing was positive in all tested cases. Two specimens from '
        'Tamnar Range (Dec 2025) returned positive for arsenic (File No. F.2-19/DI/NRC/2025-26/CWL), '
        'indicating possible water body contamination requiring environmental follow-up.', 'bodyJ'
    ))
    add(SP(6))

    drown_data = [
        [P('PM Finding', 'th'), P('Observation', 'th'), P('Significance', 'th')],
        [P('Frothy discharge', 'tdb'), P('Present in ALL 13 cases', 'tdc'),
         P('Hallmark of antemortem drowning — not seen in post-mortem drowning', 'td')],
        [P('Waterlogged lungs', 'tdb'), P('Present in ALL 13 cases', 'tdc'),
         P('Lung weight 3–5× normal; confirms inhalation of water', 'td')],
        [P('Water in trachea', 'tdb'), P('Present in ALL 13 cases', 'tdc'),
         P('Rules out post-mortem artefact — water aspirated while alive', 'td')],
        [P('GI water content', 'tdb'), P('Large volume — ALL cases', 'tdc'),
         P('Swallowed water while struggling — corroborates active drowning', 'td')],
        [P('Diatom test', 'tdb'), P('<b>POSITIVE — all tested cases</b>', 'tdc'),
         P('Diatoms in bone marrow = systemic dissemination = confirmed antemortem drowning', 'td')],
        [P('Arsenic', 'tdb'), P('<b>DETECTED in 2 specimens</b>', 'tdc'),
         P('Tamnar Range, Dec 2025 — environmental contamination investigation initiated', 'td')],
        [P('EEHV', 'tdb'), P('NEGATIVE all cases', 'tdc'),
         P('Viral haemorrhagic disease ruled out', 'td')],
        [P('Nitrate-Nitrite', 'tdb'), P('NEGATIVE all cases', 'tdc'),
         P('Fertiliser/industrial contamination ruled out', 'td')],
        [P('Heavy metals (Pb/Hg/Cd)', 'tdb'), P('NEGATIVE all cases', 'tdc'),
         P('Common industrial contaminants not implicated', 'td')],
        [P('Organochlorine/phosphate', 'tdb'), P('NEGATIVE all cases', 'tdc'),
         P('Pesticide poisoning excluded', 'td')],
        [P('HCN (Cyanide)', 'tdb'), P('NEGATIVE all cases', 'tdc'),
         P('Plant/industrial cyanide toxicity excluded', 'td')],
    ]
    drown_tbl = Table(drown_data, colWidths=[120, 130, 210])
    ts5 = base_ts(3)
    ts5.add('BACKGROUND', (0, 5), (-1, 5), C_TINT)
    ts5.add('BACKGROUND', (0, 6), (-1, 6), C_RED_L)
    drown_tbl.setStyle(ts5)
    add(drown_tbl)
    add(SP(10))

    add(PageBreak())

    # ── Section 9: Case Study ─────────────────────────────────────────────────
    add(SectionHeading('9. Case Study — Gurda Calf Drowning (01 June 2026)'))
    add(SP(6))

    case_data = [
        [P('Parameter', 'th'), P('Details', 'th')],
        [P('Date', 'tdb'), P('01 June 2026', 'td')],
        [P('Location', 'tdb'), P('Gurda River sandbank, Kharsia Range, Raigarh Van Mandal', 'td')],
        [P('GPS Coordinates', 'tdb'), P('22.0439°N, 83.1313°E', 'td')],
        [P('Victim', 'tdb'), P('Male calf, estimated age 12–18 months', 'td')],
        [P('Discovery', 'tdb'), P('Calf found separated from herd on exposed sandbank after overnight flooding', 'td')],
        [P('Circumstantial evidence', 'tdb'),
         P('River flash flood event; steep eroded banks at GPS location; no other herd members present at recovery', 'td')],
        [P('PM Findings', 'tdb'),
         P('Waterlogged lungs, frothy tracheal discharge, water in stomach (large volume), '
           'no external trauma, no injuries consistent with predation or electrocution', 'td')],
        [P('Diatom Test', 'tdb'), P('POSITIVE — Naviculaceae spp. detected in lung and bone marrow', 'td')],
        [P('Cause of Death', 'tdb'), P('<b>Confirmed drowning (asphyxia due to water inhalation)</b>', 'tdb')],
        [P('Follow-up', 'tdb'),
         P('Water sample collected from Gurda River for arsenic/chemical analysis; '
           'site flagged for earthen ramp installation', 'td')],
    ]
    case_tbl = Table(case_data, colWidths=[130, 330])
    ts6 = base_ts(2)
    ts6.add('BACKGROUND', (0, 9), (-1, 9), C_TINT)
    case_tbl.setStyle(ts6)
    add(case_tbl)
    add(SP(10))

    # ── Section 10: Workshop Programme ────────────────────────────────────────
    add(SectionHeading('10. Two-Day Workshop Programme'))
    add(SP(6))

    prog_data = [
        [P('Day / Time', 'th'), P('Session', 'th'), P('Resource Person', 'th')],
        [P('<b>Day 1</b>\nMorning', 'tdb'),
         P('Inauguration & Overview | CG Elephant Population & Mortality Statistics | '
           'Biological & Anatomical Aspects of Asian Elephants', 'td'),
         P('Forest Officers, CG; Dr. Parag Nigam (WII)', 'td')],
        [P('Day 1\nAfternoon', 'tdb'),
         P('Non-Infectious Diseases in Asian Elephants | '
           'Infectious Diseases & Surveillance | Practical: PM Examination Techniques', 'td'),
         P('Dr. Karikalan Mathesh (ICAR-IVRI); Dr. Tapendra Saini (WII)', 'td')],
        [P('<b>Day 2</b>\nMorning', 'tdb'),
         P('Sample Collection & Chain of Custody | Non-Infectious Pathology | '
           'Drowning & Electrocution Investigation', 'td'),
         P('Dr. A. B. Shrivastav (NDVSU); Dr. C. P. Sharma (WII)', 'td')],
        [P('Day 2\nAfternoon', 'tdb'),
         P('Field Investigation Case Studies | Carcass Disposal & Site Remediation | '
           'Recommendations & Valediction', 'td'),
         P('All resource persons; CG Forest Dept Officers', 'td')],
    ]
    prog_tbl = Table(prog_data, colWidths=[80, 270, 110])
    prog_tbl.setStyle(base_ts(3))
    add(prog_tbl)
    add(SP(10))

    # ── Section 11: Recommendations ───────────────────────────────────────────
    add(SectionHeading('11. Key Recommendations & Priority Action Plan'))
    add(SP(6))
    add(P(
        'Based on the 5-year mortality analysis, the following eight priority actions were '
        'identified by the expert panel as immediate interventions for the Chhattisgarh '
        'Forest Department:', 'bodyJ'
    ))
    add(SP(6))

    rec_data = [
        [P('#', 'th'), P('Priority Action', 'th'), P('Timeline', 'th'), P('Responsible Agency', 'th')],
        [P('1', 'tdc'),
         P('<b>Environmental Water Sampling:</b> Comprehensive toxicology sampling of Rabo and '
           'Panikshet dams and water bodies in Tamnar Range for arsenic and heavy metals', 'td'),
         P('Immediate', 'tdc'), P('CG Forest Dept + ICAR-IVRI', 'td')],
        [P('2', 'tdc'),
         P('<b>Drowning Prevention Infrastructure:</b> Install earthen ramps and exit pathways '
           'at all identified drowning hotspots; priority: Ghargoda and Chhal ranges', 'td'),
         P('1–3 months', 'tdc'), P('CG Forest Dept + PWD', 'td')],
        [P('3', 'tdc'),
         P('<b>Power-Line Audit:</b> Complete audit and rectification of illegal electric '
           'fencing and stray HV lines across all elephant corridors; special focus on Kharsia, '
           'Ghargoda and Dharamjaigarh', 'td'),
         P('1–6 months', 'tdc'), P('CG Forest Dept + CSPDCL', 'td')],
        [P('4', 'tdc'),
         P('<b>Oct–Dec Enforcement Campaign:</b> Deploy anti-poaching/anti-fencing squads '
           'during harvest season with weekly intelligence gathering in conflict-prone villages', 'td'),
         P('Seasonal', 'tdc'), P('Forest Dept + Police', 'td')],
        [P('5', 'tdc'),
         P('<b>Jan–May Calf Monitoring:</b> Intensive calf surveillance during dry season when '
           'calves are most vulnerable to drowning in drying water bodies', 'td'),
         P('Seasonal', 'tdc'), P('WII + CG Forest Dept', 'td')],
        [P('6', 'tdc'),
         P('<b>Mandatory PM within 24 hrs:</b> Standard Operating Procedure mandating complete '
           'post-mortem examination with sample collection within 24 hours of elephant death, '
           'with digital reporting to State WL Office', 'td'),
         P('Policy — immediate', 'tdc'), P('PCCF (WL), CG', 'td')],
        [P('7', 'tdc'),
         P('<b>Annual EEHV Surveillance:</b> Annual serological and PCR surveillance for '
           'Elephant Endotheliotropic Herpesvirus across all elephant herds in DH and RG Divisions', 'td'),
         P('Annual', 'tdc'), P('ICAR-IVRI + WII', 'td')],
        [P('8', 'tdc'),
         P('<b>Quarterly Review Meetings:</b> Quarterly inter-departmental review of mortality '
           'data, action plan implementation, and hotspot management with representation from '
           'Forest Dept, Police, Revenue, and Power Department', 'td'),
         P('Quarterly', 'tdc'), P('PCCF (WL), CG — All Depts', 'td')],
    ]
    rec_tbl = Table(rec_data, colWidths=[22, 270, 80, 88])
    ts7 = base_ts(4)
    for i in range(1, 9):
        if i % 2 == 0:
            ts7.add('BACKGROUND', (0, i), (-1, i), C_TINT2)
    rec_tbl.setStyle(ts7)
    add(rec_tbl)
    add(SP(10))

    # ── Summary Statistics Box ─────────────────────────────────────────────────
    add(SectionHeading('Summary Statistics at a Glance'))
    add(SP(6))

    summ_data = [
        [P('Metric', 'th'), P('Value', 'th'), P('Metric', 'th'), P('Value', 'th')],
        [P('Study Period', 'tdb'), P('2021–2026 (5 yrs)', 'td'),
         P('Total Elephant Deaths', 'tdb'), P('49', 'tdc')],
        [P('DH Division Deaths', 'tdb'), P('27 (55%)', 'td'),
         P('RG Division Deaths', 'tdb'), P('22 (45%)', 'tdc')],
        [P('Electrocution Deaths', 'tdb'), P('23 (47%)', 'td'),
         P('Drowning Deaths', 'tdb'), P('13 (27%)', 'tdc')],
        [P('Calf Deaths (0-2 yr)', 'tdb'), P('23 of 46 (50%)', 'td'),
         P('Male Deaths', 'tdb'), P('23 of 45 (51%)', 'tdc')],
        [P('Peak Death Month', 'tdb'), P('October (8 deaths)', 'td'),
         P('Peak Year', 'tdb'), P('2022-23 & 2025-26 (12 each)', 'tdc')],
        [P('Drowning: Calves', 'tdb'), P('12/13 = 92%', 'td'),
         P('Arsenic Positives', 'tdb'), P('2 specimens (Tamnar, Dec 2025)', 'tdc')],
        [P('Human Deaths (HEC)', 'tdb'), P('45 (DH: 36 | RG: 9)', 'td'),
         P('Pop. Growth (2001-26)', 'tdb'), P('24 → 451 (CAGR ~13%)', 'tdc')],
    ]
    summ_tbl = Table(summ_data, colWidths=[120, 120, 120, 100])
    ts8 = base_ts(4)
    summ_tbl.setStyle(ts8)
    add(summ_tbl)
    add(SP(8))

    add(P(
        '<b>Conclusion:</b> The 5-year mortality analysis clearly demonstrates that elephant '
        'deaths in Chhattisgarh are overwhelmingly anthropogenic and preventable. '
        'Electrocution (47%) and drowning (27%) together account for three-quarters of all '
        'deaths. Calf mortality is disproportionately high at 50%. The record mortality in '
        '2025-26 is a critical signal requiring immediate multi-agency intervention. '
        'This workshop provides the technical foundation for standardised investigation, '
        'evidence-based reporting, and preventive action.', 'bodyJ'
    ))

    return story


# ═══════════════════════════════════════════════════════════════════════════════
# Build PDF
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=2.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=2.4 * cm,
        bottomMargin=1.6 * cm,
        title='Chapter 1 — Workshop Overview & Elephant Mortality Analysis',
        author='Chhattisgarh Forest Department'
    )
    story = build_story()
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    size_kb = os.path.getsize(OUT) // 1024
    print(f'✓  Written: {OUT}  ({size_kb} KB)')


if __name__ == '__main__':
    main()

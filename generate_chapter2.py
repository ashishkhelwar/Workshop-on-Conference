#!/usr/bin/env python3
"""
Generate Chapter 2: Biological & Anatomical Aspects of the Asian Elephant
Schematic diagrams drawn programmatically with ReportLab canvas.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable

C_DARK   = HexColor('#1B4332')
C_MED    = HexColor('#2D6A4F')
C_LIGHT  = HexColor('#52B788')
C_TINT   = HexColor('#D8F3DC')
C_TINT2  = HexColor('#EAF7EE')
C_ORANGE = HexColor('#F4A261')
C_ORNG_L = HexColor('#FFF0E6')
C_BODY   = HexColor('#1A1A1A')
C_MUTED  = HexColor('#555555')
C_WHITE  = colors.white

# Elephant palette
C_SKIN   = HexColor('#C0A882')
C_SKIN_D = HexColor('#8A7055')
C_SKIN_E = HexColor('#A8906A')   # ear / darker areas
C_IVORY  = HexColor('#FFFDE0')
C_IVORY_D= HexColor('#C8B850')
C_EYE    = HexColor('#2A1A0A')

PW, PH = A4
OUT = '/home/user/Workshop-on-Conference/Workshop_Chapter2_Anatomy_2026.pdf'


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAM FLOWABLES
# ═══════════════════════════════════════════════════════════════════════════════

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
        c.rect(0, h-6, w, 6, fill=1, stroke=0)
        c.setFillColor(C_LIGHT)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(14, h-22, f'CHAPTER {self.chapter_num}')
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 18)
        c.drawString(14, h-48, self.title)
        if self.subtitle:
            c.setFillColor(HexColor('#A8D5B5'))
            c.setFont('Helvetica', 10.5)
            c.drawString(14, h-64, self.subtitle)
        if self.author:
            c.setFillColor(HexColor('#88BF9E'))
            c.setFont('Helvetica', 9)
            c.drawString(14, h-80, self.author)
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
            c.rect(0, h-4, self.aw, 4, fill=1, stroke=0)
            c.setFillColor(C_MED)
            c.setFont('Helvetica-Bold', 11)
            c.drawString(0, 0, self.text)


class KeyBox(Flowable):
    def __init__(self, lines, title=None, width=None, warning=False):
        Flowable.__init__(self)
        self.lines = lines if isinstance(lines, list) else [lines]
        self.title = title
        self._width = width
        self.warning = warning

    def wrap(self, aw, ah):
        self.aw = self._width or aw
        self._h = len(self.lines)*13 + (18 if self.title else 0) + 18
        return self.aw, self._h

    def draw(self):
        c = self.canv
        bg = C_ORNG_L if self.warning else C_TINT
        bd = C_ORANGE if self.warning else C_LIGHT
        tc = HexColor('#8B3A00') if self.warning else C_DARK
        c.setFillColor(bg)
        c.roundRect(0, 0, self.aw, self._h, 4, fill=1, stroke=0)
        c.setStrokeColor(bd); c.setLineWidth(1.2)
        c.roundRect(0, 0, self.aw, self._h, 4, fill=0, stroke=1)
        c.setFillColor(bd); c.rect(0, 0, 4, self._h, fill=1, stroke=0)
        y = self._h - 13
        if self.title:
            c.setFont('Helvetica-Bold', 9.5)
            c.setFillColor(tc)
            c.drawString(12, y, self.title)
            y -= 15
        c.setFont('Helvetica', 9)
        c.setFillColor(C_BODY)
        for ln in self.lines:
            c.drawString(12, y, ln)
            y -= 13


# ── Diagram 1: External Anatomy ───────────────────────────────────────────────

class ElephantBodyDiagram(Flowable):
    """Schematic lateral-view labeled anatomy of the Asian Elephant."""

    def __init__(self, width=None):
        Flowable.__init__(self)
        self._w = width

    def wrap(self, aw, ah):
        self.aw = self._w or aw
        self._h = int(self.aw * 250 / 520)
        return self.aw, self._h

    def draw(self):
        c = self.canv
        W, H = self.aw, self._h
        DW, DH = 520, 250   # design canvas size

        def cx(dx): return dx * W / DW
        def cy(dy): return H - dy * H / DH

        def t(dx, dy): return cx(dx), cy(dy)
        def ell(dx1, dy1, dx2, dy2, **kw):
            # dy1=top, dy2=bottom in design space
            c.ellipse(cx(dx1), cy(dy2), cx(dx2), cy(dy1), **kw)

        # Background
        c.setFillColor(HexColor('#F5FAF6'))
        c.setStrokeColor(HexColor('#C8E6C8'))
        c.setLineWidth(0.6)
        c.roundRect(0, 0, W, H, 4, fill=1, stroke=1)

        # ── Draw elephant ──

        # EAR (drawn first so head overlaps it)
        c.saveState()
        c.setFillColor(C_SKIN_E)
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(1.5))
        p = c.beginPath()
        p.moveTo(*t(75, 60))
        p.curveTo(*t(20, 40), *t(5, 10), *t(45, 8))
        p.curveTo(*t(80, 5),  *t(110, 30), *t(112, 60))
        p.curveTo(*t(112, 85), *t(95, 105), *t(75, 112))
        p.curveTo(*t(60, 118), *t(60, 95), *t(75, 60))
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.restoreState()

        # BODY
        c.setFillColor(C_SKIN)
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(1.8))
        ell(135, 55, 415, 168, fill=1, stroke=1)

        # HEAD
        ell(28, 45, 168, 175, fill=1, stroke=1)

        # TRUNK (filled bezier path)
        c.saveState()
        c.setFillColor(C_SKIN)
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(1.5))
        p = c.beginPath()
        p.moveTo(*t(55, 155))
        p.curveTo(*t(35, 165), *t(15, 185), *t(28, 210))
        p.curveTo(*t(34, 222), *t(55, 228), *t(68, 222))
        p.curveTo(*t(80, 215), *t(82, 205), *t(74, 196))
        p.curveTo(*t(66, 205), *t(52, 210), *t(44, 200))
        p.curveTo(*t(30, 182), *t(48, 162), *t(72, 158))
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.restoreState()

        # TUSK (ivory)
        c.saveState()
        c.setFillColor(C_IVORY)
        c.setStrokeColor(C_IVORY_D)
        c.setLineWidth(cx(1.2))
        p = c.beginPath()
        p.moveTo(*t(100, 148))
        p.curveTo(*t(75, 153), *t(42, 162), *t(22, 178))
        p.lineTo(*t(28, 187))
        p.curveTo(*t(50, 172), *t(80, 163), *t(107, 156))
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.restoreState()

        # EYE
        c.saveState()
        c.setFillColor(C_EYE)
        c.circle(*t(125, 92), cx(5), fill=1, stroke=0)
        c.setFillColor(C_WHITE)
        c.circle(cx(127), cy(90), cx(1.5), fill=1, stroke=0)
        c.restoreState()

        # TEMPORAL GLAND (between eye and ear)
        c.saveState()
        c.setFillColor(HexColor('#9A8060'))
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(0.8))
        ell(100, 82, 118, 96, fill=1, stroke=1)
        c.restoreState()

        # LEGS (two pairs, front & back)
        c.setFillColor(C_SKIN)
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(1.5))
        for lx in [148, 183, 288, 322]:
            p = c.beginPath()
            p.moveTo(*t(lx, 163))
            p.lineTo(*t(lx+28, 163))
            p.lineTo(*t(lx+23, 228))
            p.lineTo(*t(lx+5, 228))
            p.close()
            c.drawPath(p, fill=1, stroke=1)

        # FOOT CUSHION PADS
        c.setFillColor(HexColor('#7A6248'))
        for lx in [148, 183, 288, 322]:
            x1, y1 = t(lx+2, 231)
            x2, y2 = t(lx+26, 240)
            c.roundRect(x1, min(y1,y2), abs(x2-x1), abs(y2-y1), cx(3), fill=1, stroke=0)

        # NAILS
        c.setFillColor(HexColor('#EAE0C2'))
        c.setStrokeColor(HexColor('#B0A070'))
        c.setLineWidth(cx(0.4))
        for lx in [148, 183, 288, 322]:
            count = 5 if lx < 200 else 4
            for ni in range(count):
                nx = lx + 3 + ni * (24//count)
                ell(nx, 231, nx+5, 239, fill=1, stroke=1)

        # TAIL
        c.saveState()
        c.setFillColor(C_SKIN)
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(1.2))
        p = c.beginPath()
        p.moveTo(*t(412, 115))
        p.curveTo(*t(430, 120), *t(438, 140), *t(428, 158))
        p.curveTo(*t(420, 148), *t(414, 130), *t(410, 122))
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        # tail tuft hairs
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(1.0))
        for i in range(5):
            c.line(cx(427+i), cy(157), cx(424+i*2), cy(170))
        c.restoreState()

        # SKIN WRINKLES on body (decorative lines)
        c.saveState()
        c.setStrokeColor(HexColor('#A89070'))
        c.setLineWidth(cx(0.5))
        for wx, wy1, wy2 in [(230,85,100),(290,75,95),(350,78,100),(200,82,92)]:
            c.line(*t(wx, wy1), *t(wx+8, wy2))
        c.restoreState()

        # MAMMARY GLANDS (between front legs)
        c.saveState()
        c.setFillColor(HexColor('#B09878'))
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(cx(0.6))
        c.circle(*t(205, 168), cx(7), fill=1, stroke=1)
        c.circle(*t(220, 168), cx(7), fill=1, stroke=1)
        c.restoreState()

        # ── LABELS ──
        lw = cx(0.5)
        c.setStrokeColor(C_MED)
        c.setLineWidth(lw)
        c.setFont('Helvetica-Bold', 6.5)

        def lbl(text, lx, ly, ax, ay, side='R'):
            """Draw label at (lx,ly) with leader to anatomy point (ax,ay)."""
            bx, by = cx(lx), cy(ly)
            apx, apy = cx(ax), cy(ay)
            c.setStrokeColor(C_MED)
            c.setLineWidth(cx(0.5))
            c.line(bx, by, apx, apy)
            c.setFillColor(C_MED)
            c.circle(apx, apy, cx(1.8), fill=1, stroke=0)
            tw = c.stringWidth(text, 'Helvetica-Bold', 6.5)
            pad = 3
            bgh = 10
            c.setFillColor(HexColor('#EAF7EE'))
            if side == 'R':
                c.rect(bx+2, by-3, tw+pad*2, bgh, fill=1, stroke=0)
                c.setFillColor(C_DARK)
                c.drawString(bx+pad+2, by-1, text)
            else:
                c.rect(bx-tw-pad*2, by-3, tw+pad*2, bgh, fill=1, stroke=0)
                c.setFillColor(C_DARK)
                c.drawRightString(bx-pad, by-1, text)

        # Left-side labels (side='L', pointing right toward elephant)
        lbl('Ear (pinna)',         2, 40,  52, 50,  'R')
        lbl('Domed forehead',      2, 68,  98, 68,  'R')
        lbl('Temporal gland',      2, 82, 109, 89,  'R')
        lbl('Eye',                 2, 96, 125, 92,  'R')
        lbl('Tusk',                2,118,  55,165,  'R')
        lbl('Trunk (proboscis)',    2,150,  45,185,  'R')
        lbl('Nail',                2,236, 155,234,  'R')

        # Right-side labels (side='R', pointing left toward elephant)
        lbl('Shoulder hump',    440, 48,  255, 68, 'L')
        lbl('Concave back',     440, 80,  310, 98, 'L')
        lbl('Skin folds',       440,115,  370,125, 'L')
        lbl('Tail with tuft',   440,140,  428,148, 'L')
        lbl('Mammary glands',   440,162,  213,168, 'L')
        lbl('Foot cushion pad', 440,230,  310,234, 'L')

        # Caption
        c.setFont('Helvetica-BoldOblique', 7.5)
        c.setFillColor(C_MED)
        c.drawCentredString(W/2, 6,
            'Fig. 1 — External Anatomy of the Asian Elephant '
            '(Elephas maximus) — Lateral view')


# ── Diagram 2: Molar Progression ──────────────────────────────────────────────

class MolarProgressionDiagram(Flowable):
    """Six molar sets with laminae, size, and age labels."""

    def __init__(self, width=None):
        Flowable.__init__(self)
        self._w = width

    def wrap(self, aw, ah):
        self.aw = self._w or aw
        self._h = int(self.aw * 130 / 480)
        return self.aw, self._h

    def draw(self):
        c = self.canv
        W, H = self.aw, self._h

        # Background
        c.setFillColor(HexColor('#F5FAF6'))
        c.setStrokeColor(HexColor('#C8E6C8'))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, W, H, 4, fill=1, stroke=1)

        molars = [
            ('M1', '~1 yr',  '5',  32),
            ('M2', '~2 yrs', '7',  42),
            ('M3', '~6 yrs', '10', 55),
            ('M4', '~15 yrs','10', 65),
            ('M5', '~28 yrs','12', 80),
            ('M6', '~47 yrs','13', 95),
        ]
        n = len(molars)
        slot_w = W / n
        margin = 8
        max_box_h = H * 0.52
        max_lam = 13

        for i, (name, age, lam_s, lam_n) in enumerate(molars):
            sx = i * slot_w
            cx_slot = sx + slot_w / 2

            # box height proportional to molar size (grows with each set)
            scale = (i + 1) / n
            bw = (slot_w - margin*2) * scale
            bh = max_box_h * scale
            bx = cx_slot - bw/2
            by = H * 0.62 - bh

            # molar box
            c.setFillColor(HexColor('#E0C898'))
            c.setStrokeColor(C_SKIN_D)
            c.setLineWidth(1.0)
            c.rect(bx, by, bw, bh, fill=1, stroke=1)

            # laminae (vertical lines inside box)
            lam_count = int(lam_s)
            if lam_count > 1 and bw > 6:
                c.setStrokeColor(HexColor('#8A7050'))
                c.setLineWidth(0.5)
                step = bw / lam_count
                for li in range(1, lam_count):
                    lx = bx + li * step
                    c.line(lx, by, lx, by + bh)

            # wear surface (slightly darker top)
            c.setFillColor(HexColor('#C0A878'))
            c.rect(bx, by + bh - bh*0.12, bw, bh*0.12, fill=1, stroke=0)

            # molar label
            c.setFont('Helvetica-Bold', 7.5)
            c.setFillColor(C_DARK)
            c.drawCentredString(cx_slot, by - 12, name)

            # age label
            c.setFont('Helvetica', 6.5)
            c.setFillColor(C_MED)
            c.drawCentredString(cx_slot, by - 22, age)

            # laminae count
            c.setFont('Helvetica-Bold', 7)
            c.setFillColor(C_DARK)
            c.drawCentredString(cx_slot, H * 0.62 + 6, f'{lam_s} laminae')

        # arrow showing progressive replacement →
        arr_y = H * 0.62 - max_box_h * 0.5
        c.setStrokeColor(C_MED)
        c.setLineWidth(1.2)
        c.line(slot_w*0.5, arr_y, W - slot_w*0.5, arr_y)
        c.line(W - slot_w*0.5, arr_y, W - slot_w*0.5 - 6, arr_y + 4)
        c.line(W - slot_w*0.5, arr_y, W - slot_w*0.5 - 6, arr_y - 4)
        c.setFont('Helvetica-Oblique', 6.5)
        c.setFillColor(C_MED)
        c.drawCentredString(W/2, arr_y + 5, 'Progressive replacement throughout life →')

        # Caption
        c.setFont('Helvetica-BoldOblique', 7.5)
        c.setFillColor(C_MED)
        c.drawCentredString(W/2, 5,
            'Fig. 2 — Molar Progression in Asian Elephants: Six sequential tooth sets '
            '(M1–M6) with increasing laminae count')


# ── Diagram 3: Foot Cross-Section ─────────────────────────────────────────────

class FootCrossSectionDiagram(Flowable):
    """Simplified cross-section of elephant foot showing internal layers."""

    def __init__(self, width=None):
        Flowable.__init__(self)
        self._w = width

    def wrap(self, aw, ah):
        self.aw = self._w or aw
        self._h = int(self.aw * 180 / 360)
        return self.aw, self._h

    def draw(self):
        c = self.canv
        W, H = self.aw, self._h

        c.setFillColor(HexColor('#F5FAF6'))
        c.setStrokeColor(HexColor('#C8E6C8'))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, W, H, 4, fill=1, stroke=1)

        # foot outline — trapezoid wider at bottom
        FX = W * 0.18
        FW_top = W * 0.42
        FW_bot = W * 0.52
        FY_top = H * 0.10
        FY_bot = H * 0.82
        FH = FY_bot - FY_top
        cx_foot = FX + FW_top / 2

        # layers from top to bottom:
        layers = [
            # (label, fraction of FH, fill-colour, stroke)
            ('Bone (phalanges)',    0.22, HexColor('#E8E0C8'), HexColor('#B0A878')),
            ('Digital cushion pad',0.28, HexColor('#D4B896'), HexColor('#A08060')),
            ('Plantar cushion',    0.30, HexColor('#BEA880'), HexColor('#8A7050')),
            ('Skin / sole',        0.10, HexColor('#8A7050'), HexColor('#6A5030')),
        ]

        y_cur = FY_top
        for label, frac, fill, stroke in layers:
            lh = FH * frac
            # trapezoidal layer — wider at bottom
            prog = (y_cur - FY_top) / FH
            wt = FW_top + (FW_bot - FW_top) * prog
            wb = FW_top + (FW_bot - FW_top) * (prog + frac)
            xt = FX + (FW_bot - wt) / 2
            xb = FX + (FW_bot - wb) / 2

            c.setFillColor(fill)
            c.setStrokeColor(stroke)
            c.setLineWidth(0.8)
            p = c.beginPath()
            p.moveTo(xt, H - y_cur)
            p.lineTo(xt + wt, H - y_cur)
            p.lineTo(xb + wb, H - (y_cur + lh))
            p.lineTo(xb, H - (y_cur + lh))
            p.close()
            c.drawPath(p, fill=1, stroke=1)

            # label inside layer
            c.setFont('Helvetica-Bold', 6.5)
            c.setFillColor(C_DARK)
            mid_y = H - (y_cur + lh / 2)
            c.drawCentredString(cx_foot + (FW_bot - FW_top) * (prog + frac/2) / 2,
                                mid_y - 3, label)
            y_cur += lh

        # Nails across the bottom
        nail_y_top = H - FY_bot
        nail_h = H * 0.09
        n_nails = 5
        nail_w = FW_bot / (n_nails + 1)
        c.setFillColor(HexColor('#EEE4C0'))
        c.setStrokeColor(HexColor('#B0A060'))
        c.setLineWidth(0.8)
        for ni in range(n_nails):
            nx = FX + nail_w * (ni + 0.6)
            c.ellipse(nx, nail_y_top - nail_h, nx + nail_w*0.7, nail_y_top, fill=1, stroke=1)

        # Outer skin (full foot outline)
        c.setFillColor(HexColor('#00000000'))  # transparent
        c.setStrokeColor(C_SKIN_D)
        c.setLineWidth(1.5)
        p = c.beginPath()
        p.moveTo(FX, H - FY_top)
        p.lineTo(FX + FW_top, H - FY_top)
        p.lineTo(FX + (FW_bot - FW_top)/2 + FW_top, H - FY_bot)
        p.lineTo(FX - (FW_bot - FW_top)/2, H - FY_bot)
        p.close()
        c.drawPath(p, fill=0, stroke=1)

        # Arrows + side labels
        c.setStrokeColor(C_MED)
        c.setLineWidth(0.5)
        c.setFont('Helvetica', 7)
        c.setFillColor(C_DARK)

        side_labels = [
            ('Thick skin (2–3 cm)', H * 0.15,  FX + FW_top + 2, 'L'),
            ('Fibrous cushion absorbs\nimpact of 5,000 kg', H * 0.45, FX + FW_top + 2, 'L'),
            ('5 nails (front foot)\n4 nails (hind foot)', H * 0.90, FX + FW_top + 2, 'L'),
        ]
        rlabel_x = FX + FW_bot + 6
        for text, ly, _, __ in side_labels:
            c.setStrokeColor(C_MED)
            c.line(rlabel_x - 2, ly, rlabel_x + 2, ly)
            c.setFont('Helvetica', 6.5)
            c.setFillColor(C_DARK)
            for ti, tline in enumerate(text.split('\n')):
                c.drawString(rlabel_x + 4, ly - 3 + ti*(-9), tline)

        # Caption
        c.setFont('Helvetica-BoldOblique', 7.5)
        c.setFillColor(C_MED)
        c.drawCentredString(W/2, 5,
            'Fig. 3 — Cross-Section of the Asian Elephant Foot '
            '(showing cushion pad layers and nails)')


# ── Diagram 4: Digestive System ───────────────────────────────────────────────

class DigestiveSystemDiagram(Flowable):
    """Schematic flow diagram of the elephant's digestive tract."""

    def __init__(self, width=None):
        Flowable.__init__(self)
        self._w = width

    def wrap(self, aw, ah):
        self.aw = self._w or aw
        self._h = int(self.aw * 175 / 480)
        return self.aw, self._h

    def draw(self):
        c = self.canv
        W, H = self.aw, self._h

        c.setFillColor(HexColor('#F5FAF6'))
        c.setStrokeColor(HexColor('#C8E6C8'))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, W, H, 4, fill=1, stroke=1)

        segments = [
            ('Oral Cavity\n& Teeth',   'Molars grind 100–300 kg\nvegetation/day', HexColor('#C8DFC8')),
            ('Oesophagus',             '~120 cm; muscular tube\nto stomach', HexColor('#D0E8D0')),
            ('Stomach\n(monogastric)', 'Simple; 100–140 cm long\n40 cm diameter', HexColor('#B8D8B8')),
            ('Small\nIntestine',       '~16 m total length;\ndigestion & absorption', HexColor('#A8CCB8')),
            ('Caecum &\nLarge Intestine', 'Hindgut fermentation\n~19 m; microbiome', HexColor('#98C4B0')),
            ('Rectum\n& Anus',         'Dung bolus; ~40%\ndigestion efficiency', HexColor('#88BCA8')),
        ]

        n = len(segments)
        seg_w = (W - 20) / n
        box_h = H * 0.52
        box_y = H * 0.22
        arr_len = 10

        for i, (name, desc, fill) in enumerate(segments):
            bx = 10 + i * seg_w
            bw = seg_w - 4

            # box
            c.setFillColor(fill)
            c.setStrokeColor(C_MED)
            c.setLineWidth(0.8)
            c.roundRect(bx, box_y, bw, box_h, 4, fill=1, stroke=1)

            # name lines
            c.setFont('Helvetica-Bold', 6.8)
            c.setFillColor(C_DARK)
            lines = name.split('\n')
            for li, ln in enumerate(lines):
                cy_txt = box_y + box_h * 0.72 - li * 9
                c.drawCentredString(bx + bw/2, cy_txt, ln)

            # arrow to next
            if i < n - 1:
                ax = bx + bw + 2
                ay = box_y + box_h / 2
                c.setStrokeColor(C_MED)
                c.setLineWidth(1.0)
                c.line(ax, ay, ax + arr_len - 2, ay)
                c.line(ax + arr_len - 2, ay, ax + arr_len - 6, ay + 3)
                c.line(ax + arr_len - 2, ay, ax + arr_len - 6, ay - 3)

            # description below
            c.setFont('Helvetica', 5.8)
            c.setFillColor(C_MUTED)
            desc_lines = desc.split('\n')
            for li, ln in enumerate(desc_lines):
                c.drawCentredString(bx + bw/2, box_y - 10 - li*8, ln)

        # Stats bar at top
        c.setFillColor(C_DARK)
        c.roundRect(10, H-22, W-20, 18, 3, fill=1, stroke=0)
        stats = '100–300 kg food/day   ·   100–200 L water/day   ·   ~40% digestive efficiency   ·   24–48 hr GI transit'
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(C_WHITE)
        c.drawCentredString(W/2, H-14, stats)

        # Caption
        c.setFont('Helvetica-BoldOblique', 7.5)
        c.setFillColor(C_MED)
        c.drawCentredString(W/2, 5,
            'Fig. 4 — Digestive System of the Asian Elephant (Hindgut Fermenter — Monogastric)')


# ── Diagram 5: Asian vs African comparison ────────────────────────────────────

class AsianAfricanCompDiagram(Flowable):
    """Side-by-side schematic heads: Asian vs African elephant differences."""

    def __init__(self, width=None):
        Flowable.__init__(self)
        self._w = width

    def wrap(self, aw, ah):
        self.aw = self._w or aw
        self._h = int(self.aw * 145 / 480)
        return self.aw, self._h

    def draw(self):
        c = self.canv
        W, H = self.aw, self._h

        c.setFillColor(HexColor('#F5FAF6'))
        c.setStrokeColor(HexColor('#C8E6C8'))
        c.setLineWidth(0.5)
        c.roundRect(0, 0, W, H, 4, fill=1, stroke=1)

        half = W / 2 - 2

        def draw_head(ox, label, ear_big, dome_double, skin_col_h):
            """Draw a schematic elephant head."""
            cx_h = ox + half/2
            # Head oval
            hx1, hx2 = ox + half*0.15, ox + half*0.85
            hy1, hy2 = H*0.18, H*0.82
            hw = hx2 - hx1
            hh = hy2 - hy1

            # Ear
            ear_rx = half * (0.38 if ear_big else 0.22)
            ear_ry = H * (0.38 if ear_big else 0.25)
            ear_cx = hx1 - ear_rx * 0.35
            ear_cy = H * 0.50
            c.setFillColor(HexColor('#A88A60') if ear_big else HexColor('#B89868'))
            c.setStrokeColor(C_SKIN_D)
            c.setLineWidth(0.8)
            c.ellipse(ear_cx - ear_rx, ear_cy - ear_ry,
                      ear_cx + ear_rx, ear_cy + ear_ry, fill=1, stroke=1)

            # Head
            c.setFillColor(skin_col_h)
            c.setStrokeColor(C_SKIN_D)
            c.setLineWidth(1.2)
            c.ellipse(hx1, hy1, hx2, hy2, fill=1, stroke=1)

            # Double dome (Asian) or single dome (African)
            if dome_double:
                # Two bumps on top of head
                for bump_x in [cx_h - hw*0.15, cx_h + hw*0.15]:
                    c.setFillColor(skin_col_h)
                    c.setStrokeColor(C_SKIN_D)
                    c.setLineWidth(0.8)
                    c.ellipse(bump_x - hw*0.15, hy2 - H*0.08,
                              bump_x + hw*0.15, hy2 + H*0.06, fill=1, stroke=1)
            else:
                # single rounded dome
                c.setFillColor(skin_col_h)
                c.setStrokeColor(C_SKIN_D)
                c.setLineWidth(0.8)
                c.ellipse(cx_h - hw*0.28, hy2 - H*0.06,
                          cx_h + hw*0.28, hy2 + H*0.08, fill=1, stroke=1)

            # Trunk (simple line)
            c.setStrokeColor(C_SKIN_D)
            c.setLineWidth(half*0.08)
            p = c.beginPath()
            p.moveTo(cx_h, hy1 + H*0.08)
            p.curveTo(cx_h - half*0.08, H*0.30, cx_h - half*0.12, H*0.15, cx_h - half*0.05, H*0.05)
            c.drawPath(p, fill=0, stroke=1)

            # Trunk tip finger(s)
            tip_x = cx_h - half*0.05
            tip_y = H * 0.05
            if dome_double:  # Asian: 1 finger
                c.setFillColor(C_SKIN_D)
                c.circle(tip_x - half*0.05, tip_y + H*0.02, half*0.028, fill=1, stroke=0)
            else:           # African: 2 fingers
                for fi, fx in enumerate([-1, 1]):
                    c.setFillColor(C_SKIN_D)
                    c.circle(tip_x + fx*half*0.04, tip_y + H*0.02, half*0.022, fill=1, stroke=0)

            # Eye
            c.setFillColor(C_EYE)
            c.circle(cx_h + hw*0.22, H*0.54, half*0.03, fill=1, stroke=0)

            # Label at top
            c.setFont('Helvetica-Bold', 8.5)
            c.setFillColor(C_DARK)
            c.drawCentredString(cx_h, H*0.96, label)

        draw_head(4,    'Asian Elephant (Elephas maximus)',
                  ear_big=False, dome_double=True, skin_col_h=C_SKIN)
        draw_head(half+4, 'African Elephant (Loxodonta africana)',
                  ear_big=True,  dome_double=False, skin_col_h=HexColor('#B0986A'))

        # Divider
        c.setStrokeColor(HexColor('#BBBBBB'))
        c.setLineWidth(0.8)
        c.line(W/2, H*0.04, W/2, H*0.94)

        # Caption
        c.setFont('Helvetica-BoldOblique', 7.5)
        c.setFillColor(C_MED)
        c.drawCentredString(W/2, 5,
            'Fig. 5 — Asian vs African Elephant: Key differences in head profile, '
            'ear size, and trunk tip')


# ═══════════════════════════════════════════════════════════════════════════════
# Styles / helpers
# ═══════════════════════════════════════════════════════════════════════════════

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


def make_table(headers, rows, ST, col_widths=None, first_bold=True):
    hdr = [Paragraph(h, ST['cell_hdr']) for h in headers]
    data = [hdr]
    for row in rows:
        data.append([
            Paragraph(str(c), ST['cell_bold'] if (j==0 and first_bold) else ST['cell_body'])
            for j, c in enumerate(row)
        ])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), C_DARK),
        ('TEXTCOLOR',     (0,0), (-1,0), C_WHITE),
        ('ALIGN',         (0,0), (-1,0), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('GRID',          (0,0), (-1,-1), 0.4, HexColor('#BBBBBB')),
        ('LINEBELOW',     (0,0), (-1,0), 1.2, C_LIGHT),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [C_WHITE, C_TINT2]),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t


def sp(n=6):  return Spacer(1, n)
def p(t, ST): return Paragraph(t, ST['body'])
def b(t, ST): return Paragraph(f'• {t}', ST['bullet'])


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
                      'Chapter 2: Biological & Anatomical Aspects of the Asian Elephant')
    canvas.drawRightString(PW - doc.rightMargin, PH - doc.topMargin + 11,
                           'Workshop — Chhattisgarh Forest Department  ·  June 2026')
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


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

def build_story(ST):
    story = []
    W = PW - 3.4 * cm

    # CHAPTER HEADER
    story.append(ChapterHeader(
        '2',
        'Biological & Anatomical Aspects',
        'of the Asian Elephant',
        'Workshop Reference Chapter  ·  '
        'Workshop on Essentials for Mortality Investigation of Asian Elephant  ·  June 2026'
    ))
    story.append(sp(14))

    # ── SECTION 1: TAXONOMY ───────────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('1.  Taxonomy & Classification'),
        sp(6),
        p('The Asian elephant (<i>Elephas maximus</i>) is the largest land animal in Asia '
          'and a keystone species of tropical and subtropical forest ecosystems. It belongs '
          'to Order <b>Proboscidea</b>, the only surviving order of a once-diverse lineage '
          'of trunk-bearing mammals that included mammoths and mastodons.', ST),
        sp(6),
    ]))

    tax_rows = [
        ['Kingdom',  'Animalia'],
        ['Phylum',   'Chordata'],
        ['Class',    'Mammalia'],
        ['Order',    'Proboscidea'],
        ['Family',   'Elephantidae'],
        ['Genus',    'Elephas'],
        ['Species',  'Elephas maximus (Linnaeus, 1758)'],
        ['Subspecies',
         'E. m. maximus (Sri Lanka)  ·  E. m. indicus (Indian mainland)  ·  '
         'E. m. sumatranus (Sumatra)  ·  E. m. borneensis (Borneo)'],
    ]
    story.append(make_table(['Rank', 'Classification'], tax_rows, ST,
                            col_widths=[W*0.22, W*0.78]))
    story.append(sp(12))

    # ── SECTION 2: EXTERNAL ANATOMY DIAGRAM ──────────────────────────────────
    story.append(SectionHeading('2.  External Anatomy'))
    story.append(sp(8))
    story.append(ElephantBodyDiagram(width=W))
    story.append(sp(10))

    # Physical characteristics table
    story.append(SectionHeading('Physical Characteristics', level=2))
    story.append(sp(6))
    phys_rows = [
        ['Shoulder height', 'Male: 2.5–3.5 m   |   Female: 2.0–2.5 m'],
        ['Body weight', 'Male: 3,500–5,000 kg   |   Female: 2,000–3,500 kg'],
        ['Body length (nose to tail)', '5.5–6.5 m (male)'],
        ['Skin thickness', 'Up to 2.5–3 cm on back/head; thinner on ears'],
        ['Lifespan', '60–70 years in the wild'],
        ['Gestation period', '~22 months (longest of any land mammal)'],
        ['Inter-birth interval', '3–5 years'],
        ['Daily food intake', '100–300 kg of vegetation'],
        ['Daily water intake', '100–200 litres'],
    ]
    story.append(make_table(['Parameter', 'Value'], phys_rows, ST,
                            col_widths=[W*0.30, W*0.70]))
    story.append(sp(12))

    # ── SECTION 3: ASIAN vs AFRICAN ───────────────────────────────────────────
    story.append(SectionHeading('3.  Asian vs. African Elephant — Key Differences'))
    story.append(sp(8))
    story.append(AsianAfricanCompDiagram(width=W))
    story.append(sp(8))

    comp_rows = [
        ['Head profile',       'Two-domed (divided forehead)',    'Single rounded dome'],
        ['Ear size',           'Smaller (~1/3 of African)',       'Very large (ear = map of Africa)'],
        ['Back profile',       'Concave / dipped',                'Concave / more arched'],
        ['Highest body point', 'Shoulder',                        'Back / mid-spine'],
        ['Trunk tip fingers',  '1 (upper lip only)',              '2 (upper and lower lip)'],
        ['Tusk presence',      'Males mainly; females often tuskless',
                               'Both sexes commonly tusked'],
        ['Front foot nails',   '5',                               '4–5'],
        ['Hind foot nails',    '4',                               '3–4'],
        ['Skin texture',       'More wrinkled; pinkish depigmented patches common',
                               'Smoother, uniformly dark'],
        ['Ear thermoregulation',
         'Moderate (smaller pinna surface)',
         'Very efficient (large radiator surface)'],
    ]
    story.append(make_table(
        ['Feature', 'Asian Elephant', 'African Elephant'],
        comp_rows, ST, col_widths=[W*0.28, W*0.36, W*0.36],
    ))
    story.append(sp(12))

    # ── SECTION 4: THE TRUNK ─────────────────────────────────────────────────
    story.append(SectionHeading('4.  The Trunk (Proboscis)'))
    story.append(sp(8))

    story.append(p('The trunk is the most anatomically complex and functionally versatile '
                   'organ in the animal kingdom — a <b>muscular hydrostat</b> (like the '
                   'human tongue) containing approximately <b>100,000 individual muscle '
                   'units</b> but no bone whatsoever. It is a fusion of the elongated nose '
                   'and upper lip.', ST))
    story.append(sp(6))

    trunk_rows = [
        ['Breathing',      'Primary airway; can breathe under water by using as a snorkel'],
        ['Drinking',       'Sucks up 8–10 L per draw; transfers to mouth or sprays onto body'],
        ['Bathing & cooling', 'Sprays water or mud over back and sides for evaporative cooling'],
        ['Olfaction',      'Raised to detect scents at height; most important sensory function '
                           '(up to 2,000 olfactory receptor genes)'],
        ['Grasping & foraging', '1 "finger" at tip (Asian) allows precise picking of leaves, '
                                'fruits, and grass; can uproot trees with trunk-and-foot leverage'],
        ['Vocalisation',   'Produces trumpeting calls (alarm, greeting, excitement); '
                           'low-frequency rumbles for infrasound communication'],
        ['Social bonding', 'Touching, intertwining, and exploring other elephants; '
                           'used in greeting and consolation'],
        ['Defence & combat','Striking, throwing, and pushing; males use in musth conflicts'],
        ['Digging',        'Excavates water holes in dry riverbeds; extracts salt licks'],
        ['Disease sampling','Trunk wash: key clinical sample for TB and EEHV diagnosis'],
    ]
    story.append(make_table(
        ['Function', 'Details'],
        trunk_rows, ST, col_widths=[W*0.24, W*0.76],
    ))
    story.append(sp(12))

    # ── SECTION 5: TUSKS & DENTITION ─────────────────────────────────────────
    story.append(SectionHeading('5.  Tusks, Teeth & Dentition'))
    story.append(sp(8))
    story.append(MolarProgressionDiagram(width=W))
    story.append(sp(10))

    story.append(KeepTogether([
        SectionHeading('Tusks', level=2),
        sp(6),
    ]))
    for line in [
        'Tusks are <b>modified second upper incisor teeth</b> — they grow continuously '
        'throughout the elephant\'s life from deep sockets in the premaxillary bone.',
        '<b>Composition:</b> solid dentine (ivory) with a small pulp cavity at the root; '
        'the outer surface has a thin enamel cap that wears off early in life.',
        'In Asian elephants, <b>only adult males</b> normally carry large visible tusks. '
        'Females usually have small <b>tushes</b> (rudimentary tusks) or none at all.',
        'Males of the <b>Sri Lankan subspecies</b> (<i>E. m. maximus</i>) are frequently '
        'tuskless — a genetically and selectively driven trait.',
        'Permanent tusks <b>protrude beyond the lips at ~30 months</b> and are used for '
        'digging, debarking trees, combat, and as resting props for the trunk.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Molar Dentition', level=2),
        sp(6),
        p('Elephants are <b>unique among mammals</b> in producing six successive sets '
          'of molar teeth (M1–M6) that erupt and move forward (mesiodentally) along '
          'the jaw during life. Each molar is larger than the previous and contains '
          'more <b>laminae</b> (transverse enamel ridges that provide grinding surface). '
          'When M6 is exhausted — typically at 55–65 years — the animal can no longer '
          'chew adequately and eventually dies of malnutrition.', ST),
        sp(8),
    ]))

    # ── SECTION 6: EARS & THERMOREGULATION ───────────────────────────────────
    story.append(SectionHeading('6.  Ears & Thermoregulation'))
    story.append(sp(8))

    story.append(p('The elephant ear is a masterpiece of biological engineering — a '
                   '<b>vascularised thermal radiator</b>. A dense network of superficial '
                   'blood vessels runs through the ear\'s thin skin, and rapid flapping '
                   'creates a convective airflow that dissipates heat from the blood before '
                   'it returns to the core.', ST))
    story.append(sp(6))

    ear_rows = [
        ['Vascular network',
         'Dense capillary plexus visible through thin ear skin — blood cooled by 3–9 °C '
         'before returning to core circulation.'],
        ['Ear flapping',
         'Slow rhythmic flapping (1–3 times/min at rest; faster in heat) acts as a '
         'bio-fan, dramatically increasing convective heat loss.'],
        ['Surface area',
         'Asian elephant ear ≈ 0.3–0.5 m² per ear; African ear ≈ 1.5–2.0 m² — '
         'this explains why African elephants tolerate greater heat.'],
        ['Communication',
         'Ear posture signals mood: forward/spread = alert/threatening; '
         'flat against neck = submission or contentment.'],
        ['Infrasound coupling',
         'Ground vibrations from infrasound calls may be sensed through the feet '
         'AND detected via the jaw/skull; ear anatomy plays a secondary role.'],
    ]
    story.append(make_table(
        ['Aspect', 'Details'],
        ear_rows, ST, col_widths=[W*0.24, W*0.76],
    ))
    story.append(sp(12))

    # ── SECTION 7: SKIN ───────────────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('7.  Skin'),
        sp(6),
    ]))
    skin_rows = [
        ['Thickness', 'Up to 2.5–3 cm on the back and head; much thinner (1–2 mm) on the ears'],
        ['Colour', 'Dark grey-brown; depigmented pink-white patches common around ears, '
                   'trunk, and face (especially in Asian elephants)'],
        ['Texture', 'Heavily wrinkled and folded — wrinkles increase surface area for '
                    'evaporative water loss; reduce surface temperature'],
        ['Sweat glands', 'Absent except for small glands between the toes; '
                         'transepidermal water loss through permeable skin is the main mechanism'],
        ['Thermoregulation', 'Skin permeability increases in heat — effective when drinking '
                             'water available; mud and water bathing critical'],
        ['Health indicators', 'Cracked, dry, or peeling skin: dehydration or nutritional deficiency. '
                              'Pox lesions, skin tumours, cutaneous filariasis all externally visible'],
    ]
    story.append(make_table(
        ['Property', 'Detail'],
        skin_rows, ST, col_widths=[W*0.20, W*0.80],
    ))
    story.append(sp(12))

    # ── SECTION 8: FEET ───────────────────────────────────────────────────────
    story.append(SectionHeading('8.  Feet & Locomotion'))
    story.append(sp(8))
    story.append(FootCrossSectionDiagram(width=W))
    story.append(sp(10))

    for line in [
        '<b>Semi-digitigrade posture</b> — elephants walk on the tips of their digits, '
        'with a large fibrous cushion pad (like a built-in heel pad) absorbing impact.',
        'The cushion pad acts as a <b>hydraulic shock absorber</b>, distributing the '
        '3,500–5,000 kg body weight across the foot to reduce pressure per cm².',
        'Despite enormous weight, elephants walk <b>almost silently</b> — the cushion '
        'pad muffles footsteps, essential for stealthy forest movement.',
        '<b>Maximum speed:</b> ~25 km/h (elephants do not truly gallop; all four feet '
        'never leave the ground simultaneously).',
        '<b>Asian elephant nails:</b> 5 on the front foot, 4 on the hind foot. '
        'Overgrown, cracked nails are a common captive management problem.',
        'Footpad health is critical — infections or injuries in foot pads can be '
        'life-threatening for captive elephants.',
    ]:
        story.append(b(line, ST))
    story.append(sp(12))

    # ── SECTION 9: SKELETAL SYSTEM ────────────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('9.  Skeletal System'),
        sp(6),
    ]))
    skel_rows = [
        ['Cervical vertebrae',  '7 (same as all mammals)'],
        ['Rib pairs',           '20 pairs (most land mammals have 12–13)'],
        ['Lumbar vertebrae',    '3–4 (fewer than most mammals; aids weight-bearing)'],
        ['Bone density',        'Pachyosteosclerosis — bones are extremely dense and '
                                'compact, providing structural support for massive weight'],
        ['Femur & humerus',     'Vertically positioned (columnar) — unlike most quadrupeds; '
                                'entire leg acts as a column, not a pendulum'],
        ['Skull',               'Large but surprisingly light — numerous air-filled '
                                'diploe (cancellous bone chambers) reduce skull weight'],
        ['Foot bones',          'All five digits present; digit bones (phalanges) short; '
                                'sesamoid bones within the cushion pad'],
        ['Tusk attachment',     'Deep root in premaxillary bone; periodontal ligament allows '
                                'slight flexibility during use'],
    ]
    story.append(make_table(
        ['Structure', 'Feature'],
        skel_rows, ST, col_widths=[W*0.26, W*0.74],
    ))
    story.append(sp(12))

    # ── SECTION 10: DIGESTIVE SYSTEM ─────────────────────────────────────────
    story.append(SectionHeading('10.  Digestive System'))
    story.append(sp(8))
    story.append(DigestiveSystemDiagram(width=W))
    story.append(sp(10))

    for line in [
        '<b>Monogastric (simple-stomached)</b> — unlike ruminants, elephants have a '
        'single-chambered stomach (~100–140 cm long, ~40 cm diameter).',
        '<b>Hindgut fermentation</b> — microbial breakdown of cellulose occurs primarily '
        'in the enlarged caecum and colon (not in the stomach/small intestine).',
        '<b>Relatively low digestive efficiency (~40%)</b> — compensated by the enormous '
        'volume consumed (100–300 kg/day).',
        '<b>Total intestinal length</b> can reach ~35 metres (stomach + small + large '
        'intestine + caecum + rectum).',
        '<b>GI transit time:</b> 24–48 hours — undigested seeds dispersed over large '
        'distances (elephants are keystone seed dispersers).',
        '<b>Clinical relevance:</b> sudden feed changes → gut microbiome disruption → '
        'colic, diarrhoea, or increased toxin production.',
    ]:
        story.append(b(line, ST))
    story.append(sp(12))

    # ── SECTION 11: REPRODUCTIVE SYSTEM ──────────────────────────────────────
    story.append(KeepTogether([
        SectionHeading('11.  Reproductive System'),
        sp(6),
    ]))
    repro_rows = [
        ['Mammary glands',       'Located between the forelimbs (pectoral position) — '
                                 'unique among large mammals; two glands with one teat each'],
        ['Oestrous cycle',       '~16 weeks; ovulation associated with two LH surges'],
        ['Gestation',            '~22 months (longest of any land mammal)'],
        ['Age at first calving', 'Females: ~14 years; males not usually successful until >20 years'],
        ['Inter-birth interval', '3–5 years (limited by extended lactation)'],
        ['Sexual maturity (male)','~15 years; socially mature at 25–30 years'],
        ['Musth',                'Annual period of heightened testosterone (10–100× normal) '
                                 'in adult males; temporal gland secretion, urine dribbling, '
                                 'aggressive behaviour; lasts days to months'],
        ['Temporal gland',       'Paired exocrine glands between eye and ear; active during '
                                 'musth and in females during oestrus; examined at necropsy'],
        ['Testes',               'Internally located (abdominal); not externally visible'],
        ['Penis',                'S-shaped when erect; males urinate backward'],
        ['Placentation',         'Zonary haemochorial; relatively large placenta'],
    ]
    story.append(make_table(
        ['Feature', 'Detail'],
        repro_rows, ST, col_widths=[W*0.26, W*0.74],
    ))
    story.append(sp(12))

    # ── SECTION 12: BRAIN & SENSES ────────────────────────────────────────────
    story.append(SectionHeading('12.  Brain, Senses & Communication'))
    story.append(sp(8))

    story.append(KeepTogether([
        SectionHeading('Brain', level=2),
        sp(6),
    ]))
    for line in [
        'The Asian elephant brain weighs <b>~4–5 kg</b> — the largest brain of any '
        'land mammal in absolute terms.',
        'Highly convoluted cortex; well-developed <b>hippocampus</b> (memory) and '
        '<b>temporal lobe</b> (social cognition).',
        'Demonstrated capabilities include: <b>mirror self-recognition</b>, '
        '<b>tool use</b>, empathy, altruism, and long-term memory (>20 years).',
        'Encephalisation Quotient (EQ) is lower than primates but higher than most '
        'other large mammals.',
    ]:
        story.append(b(line, ST))
    story.append(sp(8))

    sense_rows = [
        ['Olfaction (smell)',
         'Most dominant sense. >40% of genome dedicated to olfactory receptors — '
         'more than any other animal studied. Trunk raised to sample scent plumes at height.',
         'Exceptional (>2,000 OR genes)'],
        ['Infrasound hearing',
         'Produce and detect calls at 14–35 Hz (below human hearing range). '
         'Seismic vibrations also sensed through feet and jaw.',
         'Communication up to 10 km'],
        ['Tactile sense',
         'Trunk tip is exquisitely sensitive (Meissner\'s corpuscles). '
         'Sensitive skin on feet detects ground vibrations.',
         'Excellent'],
        ['Vision',
         'Relatively poor compared to other senses. Dichromatic colour vision '
         '(blue-yellow; red appears as green). Better in dim light than bright sun.',
         'Limited; poor in bright light'],
        ['Taste',
         'Well-developed; use to select preferred food plants and detect '
         'contaminants or toxic plants.',
         'Good'],
    ]
    story.append(make_table(
        ['Sense', 'Mechanism & Notes', 'Capability'],
        sense_rows, ST, col_widths=[W*0.16, W*0.64, W*0.20],
    ))
    story.append(sp(14))

    # ── KEY TAKEAWAYS ─────────────────────────────────────────────────────────
    story.append(SectionHeading('Key Takeaways'))
    story.append(sp(8))
    story.append(KeyBox([
        '1. Asian elephants (Elephas maximus) are identified by their double-domed head,',
        '   smaller ears, concave back, and single trunk-tip finger — key distinctions',
        '   from the African elephant.',
        '2. The trunk is a boneless, 100,000-muscle organ critical for survival; trunk',
        '   wash is the priority clinical sample for EEHV and TB diagnosis.',
        '3. Six successive molar sets (M1–M6) allow age estimation; exhaustion of M6 at',
        '   55–65 years leads to eventual death from inability to chew.',
        '4. The foot cushion pad silently absorbs enormous weight; nails and pads are',
        '   critical health indicators in captive animals.',
        '5. Hindgut fermentation in the caecum/colon with low (~40%) efficiency is',
        '   compensated by enormous daily food intake (100–300 kg).',
        '6. 22-month gestation, 3–5 year inter-birth interval, and slow sexual maturity',
        '   make the population extremely sensitive to adult mortality.',
        '7. Olfaction (>2,000 olfactory receptor genes) and infrasound communication',
        '   (detectable up to 10 km) are the dominant senses.',
    ], title='Chapter Summary — Biological & Anatomical Aspects of the Asian Elephant'))

    return story


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=1.7*cm, rightMargin=1.7*cm,
        topMargin=1.8*cm, bottomMargin=1.8*cm,
        title='Chapter 2: Biological & Anatomical Aspects of the Asian Elephant',
        author='Workshop on Essentials for Mortality Investigation of Asian Elephant',
    )
    ST = make_styles()
    story = build_story(ST)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate Workshop Overview PDF — styled after the Silviculture Conference Proceeding.
Terracotta page background · white rounded card · dark navy banners · speaker quote cards.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from PIL import Image as PILImage
import io, os, textwrap

PW, PH = A4   # 595.3 × 841.9 pt

# ── Colours ──────────────────────────────────────────────────────────────────
C_BG     = HexColor('#BF4B1A')   # Terracotta page background
C_CARD   = white
C_BANNER = HexColor('#1A2840')   # Dark navy banner
C_GRN    = HexColor('#2D6A4F')   # Forest green (section indicator / Day 1 accent)
C_RED    = HexColor('#C0392B')   # Red (section indicator / bullet alt)
C_GOLD   = HexColor('#C9A84C')   # Gold (Day 2 accent / attribution)
C_DARK   = HexColor('#1A1A1A')   # Body text
C_NAVY   = HexColor('#1A2840')   # Names / sub-heads
C_QBG    = HexColor('#1A2840')   # Pull-quote box bg
C_SPK_A  = HexColor('#1A3B5D')   # Speaker card bg (alternate 1)
C_SPK_B  = HexColor('#0F1E30')   # Speaker card bg (alternate 2)
C_MUTED  = HexColor('#555555')   # Captions / secondary text
C_RULE   = HexColor('#CCCCCC')   # Horizontal rules
C_BULLET = HexColor('#BF4B1A')   # Bullet dot (same as bg for contrast on white)

# ── Card geometry ─────────────────────────────────────────────────────────────
CM   = 22            # page-edge to card margin (pts)
CR   = 12            # card corner radius
CARD_L  = CM
CARD_R  = PW - CM
CARD_B  = 28         # card bottom (space for page number)
CARD_T  = PH - CM - 6
CARD_W  = CARD_R - CARD_L
CARD_H  = CARD_T - CARD_B

PAD     = 26         # inner horizontal padding
INN_L   = CARD_L + PAD
INN_R   = CARD_R - PAD
INN_W   = INN_R - INN_L

IMG_DIR = '/home/user/Workshop-on-Conference/img'
OUT     = '/home/user/Workshop-on-Conference/Workshop_Overview_2026.pdf'


def pil_to_rl(path, max_w=None, max_h=None, rotate_cw=False):
    """Open image with PIL, optionally rotate, return ReportLab ImageReader."""
    im = PILImage.open(path).convert('RGB')
    if rotate_cw:
        im = im.transpose(PILImage.Transpose.ROTATE_270)
    if max_w and max_h:
        im.thumbnail((int(max_w * 3.78), int(max_h * 3.78)))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=88)
    buf.seek(0)
    return ImageReader(buf), im.size


# ═══════════════════════════════════════════════════════════════════════════════
# PageBuilder — tracks y position, draws all primitives
# ═══════════════════════════════════════════════════════════════════════════════
class PB:
    def __init__(self, c):
        self.c = c
        self.y = CARD_T - PAD

    # ── Page shell ────────────────────────────────────────────────────────────
    def new_page(self, pagenum=None):
        self.c.setFillColor(C_BG)
        self.c.rect(0, 0, PW, PH, fill=1, stroke=0)
        self.c.setFillColor(C_CARD)
        self.c.roundRect(CARD_L, CARD_B, CARD_W, CARD_H, CR, fill=1, stroke=0)
        if pagenum is not None:
            self.c.setFillColor(white)
            self.c.setFont('Helvetica', 9)
            self.c.drawCentredString(PW / 2, 10, str(pagenum))
        self.y = CARD_T - PAD

    # ── Dark banner (full card width) ─────────────────────────────────────────
    def banner(self, text, size=13):
        bh = 34
        self.c.setFillColor(C_BANNER)
        self.c.roundRect(CARD_L, self.y - bh, CARD_W, bh, 6, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont('Helvetica-Bold', size)
        self.c.drawCentredString(PW / 2, self.y - bh + 11, f'- : {text} : -')
        self.y -= bh + 10

    # ── Section heading (two squares + title + rule) ──────────────────────────
    def section_heading(self, text, size=16):
        sq = 10
        x = INN_L
        self.c.setFillColor(C_GRN)
        self.c.rect(x, self.y - sq, sq, sq, fill=1, stroke=0)
        self.c.setFillColor(C_RED)
        self.c.rect(x + sq + 2, self.y - sq, sq, sq, fill=1, stroke=0)
        self.c.setFillColor(C_DARK)
        self.c.setFont('Helvetica-Bold', size)
        self.c.drawString(x + sq * 2 + 8, self.y - sq + 1, text)
        self.y -= sq + 4
        self._rule()
        self.y -= 8

    # ── Sub-heading ───────────────────────────────────────────────────────────
    def subhead(self, text, size=11, color=C_NAVY):
        self.c.setFillColor(color)
        self.c.setFont('Helvetica-Bold', size)
        # Simple wrap
        chars_per_line = int(INN_W / (size * 0.54))
        lines = textwrap.wrap(text, chars_per_line)
        for line in lines:
            self.c.drawString(INN_L, self.y, line)
            self.y -= size + 3
        self.y -= 2

    # ── Justified paragraph ───────────────────────────────────────────────────
    def para(self, text, size=10, color=C_DARK, indent=0, leading=None):
        if leading is None:
            leading = size * 1.38
        style = ParagraphStyle(
            'body', fontName='Helvetica', fontSize=size,
            textColor=color, alignment=TA_JUSTIFY, leading=leading,
            leftIndent=indent, rightIndent=0,
        )
        p = Paragraph(text, style)
        w, h = p.wrap(INN_W - indent, 2000)
        p.drawOn(self.c, INN_L + indent, self.y - h)
        self.y -= h + 6

    # ── Bullet point ──────────────────────────────────────────────────────────
    def bullet(self, text, size=10, color=C_BULLET):
        r = 3.5
        bx = INN_L + 7
        by = self.y - size * 0.6
        self.c.setFillColor(color)
        self.c.circle(bx, by, r, fill=1, stroke=0)
        style = ParagraphStyle(
            'bul', fontName='Helvetica', fontSize=size,
            textColor=C_DARK, alignment=TA_JUSTIFY, leading=size * 1.35,
        )
        p = Paragraph(text, style)
        w, h = p.wrap(INN_W - 18, 2000)
        p.drawOn(self.c, INN_L + 18, self.y - h)
        self.y -= h + 5

    # ── Dark pull-quote box ───────────────────────────────────────────────────
    def pull_quote(self, text, attrib=None, size=10.5):
        style = ParagraphStyle(
            'pq', fontName='Helvetica-BoldOblique', fontSize=size,
            textColor=white, alignment=TA_JUSTIFY, leading=size * 1.45,
        )
        p = Paragraph(text, style)
        qw = INN_W - 28
        w, h = p.wrap(qw, 2000)
        bh = h + 22 + (16 if attrib else 0)
        self.c.setFillColor(C_QBG)
        self.c.roundRect(INN_L, self.y - bh, INN_W, bh, 6, fill=1, stroke=0)
        p.drawOn(self.c, INN_L + 14, self.y - h - 12)
        if attrib:
            self.c.setFillColor(C_GOLD)
            self.c.setFont('Helvetica-Bold', 8.5)
            self.c.drawRightString(INN_R - 10, self.y - bh + 7, attrib)
        self.y -= bh + 12

    # ── Speaker quote card ────────────────────────────────────────────────────
    def speaker_card(self, name, quote, dark=True, size=10.5):
        bg = C_SPK_A if dark else C_SPK_B
        photo_r = 26
        txt_x = INN_L + photo_r * 2 + 20

        style = ParagraphStyle(
            'sq', fontName='Helvetica-BoldOblique', fontSize=size,
            textColor=white, alignment=TA_LEFT, leading=size * 1.4,
        )
        p = Paragraph(f'"{quote}"', style)
        qw = INN_R - txt_x - 12
        w, h = p.wrap(qw, 2000)

        bh = max(h + 28, photo_r * 2 + 16)
        cy = self.y - bh / 2
        cx = INN_L + photo_r + 10

        self.c.setFillColor(bg)
        self.c.roundRect(INN_L, self.y - bh, INN_W, bh, 8, fill=1, stroke=0)

        # Photo placeholder circle
        self.c.setFillColor(HexColor('#3A5A7A'))
        self.c.circle(cx, cy, photo_r, fill=1, stroke=0)
        initials = ''.join(w[0] for w in name.split() if w[0].isupper())[:2]
        self.c.setFillColor(HexColor('#8AB8D8'))
        self.c.setFont('Helvetica-Bold', 13)
        self.c.drawCentredString(cx, cy - 5, initials)

        # Quote text
        p.drawOn(self.c, txt_x, self.y - (bh - h) / 2 - h)

        # Attribution
        self.c.setFillColor(C_GOLD)
        self.c.setFont('Helvetica-Bold', 8.5)
        self.c.drawRightString(INN_R - 10, self.y - bh + 8, f'– {name}')

        self.y -= bh + 8

    # ── Stats box row ─────────────────────────────────────────────────────────
    def stats_row(self, items):
        n = len(items)
        bw = (INN_W - (n - 1) * 8) / n
        bh = 52
        x = INN_L
        for val, lbl in items:
            self.c.setFillColor(HexColor('#EDF4F0'))
            self.c.setStrokeColor(HexColor('#B8D4C6'))
            self.c.setLineWidth(0.7)
            self.c.roundRect(x, self.y - bh, bw, bh, 5, fill=1, stroke=1)
            self.c.setFillColor(C_GRN)
            self.c.setFont('Helvetica-Bold', 17)
            self.c.drawCentredString(x + bw / 2, self.y - 23, str(val))
            self.c.setFillColor(C_MUTED)
            self.c.setFont('Helvetica', 8)
            for i, part in enumerate(lbl.split('\n')):
                self.c.drawCentredString(x + bw / 2, self.y - 35 - i * 10, part)
            x += bw + 8
        self.y -= bh + 10

    # ── Schedule day-header ───────────────────────────────────────────────────
    def day_header(self, day, date, trange, gold=False):
        acc = C_GOLD if gold else C_GRN
        bg = HexColor('#FDF7E8') if gold else HexColor('#EBF5EE')
        bh = 26
        self.c.setFillColor(bg)
        self.c.setStrokeColor(acc)
        self.c.setLineWidth(0.9)
        self.c.roundRect(INN_L, self.y - bh, INN_W, bh, 5, fill=1, stroke=1)
        self.c.setFillColor(acc)
        self.c.setFont('Helvetica-Bold', 10.5)
        self.c.drawString(INN_L + 12, self.y - 17, f'{day}  ·  {date}  ·  {trange}')
        self.y -= bh + 2

    # ── Schedule session row ──────────────────────────────────────────────────
    def sched_row(self, time, topic, desc, spk, gold=False):
        acc = C_GOLD if gold else C_GRN
        style = ParagraphStyle(
            'sr', fontName='Helvetica', fontSize=8.5,
            textColor=C_DARK, alignment=TA_LEFT, leading=12,
        )
        html = f'<b>{topic}</b>'
        if desc:
            html += f'<br/><font size="8" color="#666666">{desc}</font>'
        p = Paragraph(html, style)
        desc_w = INN_W - 72 - (70 if spk else 0)
        w, h = p.wrap(desc_w, 2000)
        rh = max(h + 14, 26)

        # Row bg
        self.c.setFillColor(HexColor('#FAFAFA'))
        self.c.rect(INN_L, self.y - rh, INN_W, rh, fill=1, stroke=0)
        self.c.setStrokeColor(HexColor('#E8E8E8'))
        self.c.setLineWidth(0.4)
        self.c.line(INN_L, self.y - rh, INN_R, self.y - rh)

        # Time
        t_parts = time.replace(' – ', '\n').split('\n')
        self.c.setFillColor(acc)
        self.c.setFont('Helvetica-Bold', 7)
        for i, tp in enumerate(t_parts):
            self.c.drawString(INN_L + 5, self.y - 11 - i * 9, tp)

        # Topic + desc
        p.drawOn(self.c, INN_L + 72, self.y - (rh - h) / 2 - h)

        # Speaker label
        if spk:
            self.c.setFillColor(HexColor('#888888'))
            self.c.setFont('Helvetica', 7.5)
            self.c.drawRightString(INN_R - 4, self.y - 11, spk)

        self.y -= rh

    # ── Break row (muted) ─────────────────────────────────────────────────────
    def break_row(self, label):
        self.c.setFillColor(HexColor('#F2F2F2'))
        self.c.rect(INN_L, self.y - 18, INN_W, 18, fill=1, stroke=0)
        self.c.setFillColor(HexColor('#AAAAAA'))
        self.c.setFont('Helvetica-Oblique', 8)
        self.c.drawCentredString(PW / 2, self.y - 12, label)
        self.y -= 18

    # ── Faculty profile card ──────────────────────────────────────────────────
    def faculty_card(self, num, name, title, org, role_label='Resource Person'):
        bh = 62
        # Green left accent bar
        self.c.setFillColor(C_GRN)
        self.c.rect(INN_L, self.y - bh, 4, bh, fill=1, stroke=0)
        # Number badge
        self.c.setFillColor(C_NAVY)
        self.c.roundRect(INN_L + 10, self.y - 22, 20, 20, 3, fill=1, stroke=0)
        self.c.setFillColor(white)
        self.c.setFont('Helvetica-Bold', 8.5)
        self.c.drawCentredString(INN_L + 20, self.y - 14.5, str(num).zfill(2))
        # Role badge
        badge_w = len(role_label) * 5.8 + 10
        self.c.setFillColor(HexColor('#EDF4F0'))
        self.c.roundRect(INN_R - badge_w, self.y - 20, badge_w, 16, 3, fill=1, stroke=0)
        self.c.setFillColor(C_GRN)
        self.c.setFont('Helvetica-Bold', 7.5)
        self.c.drawString(INN_R - badge_w + 5, self.y - 13, role_label)
        # Name
        self.c.setFillColor(C_NAVY)
        self.c.setFont('Helvetica-Bold', 11)
        self.c.drawString(INN_L + 36, self.y - 14, name)
        # Title (wrapped)
        style = ParagraphStyle('ft', fontName='Helvetica', fontSize=9,
                               textColor=C_DARK, leading=12)
        p = Paragraph(title, style)
        pw2, ph2 = p.wrap(INN_W - 40, 100)
        p.drawOn(self.c, INN_L + 36, self.y - 28 - ph2)
        # Org tag
        self.c.setFillColor(HexColor('#E4EFE9'))
        tg_w = min(len(org) * 5.6 + 14, INN_W - 42)
        self.c.roundRect(INN_L + 36, self.y - bh + 6, tg_w, 16, 3, fill=1, stroke=0)
        self.c.setFillColor(C_GRN)
        self.c.setFont('Helvetica-Bold', 7.5)
        self.c.drawString(INN_L + 42, self.y - bh + 10.5, org[:50])
        self.y -= bh + 6

    # ── Highlight session block ───────────────────────────────────────────────
    def highlight(self, title, text, accent=C_GRN):
        # Accent dot + title
        self.c.setFillColor(accent)
        self.c.circle(INN_L + 5, self.y - 7, 4, fill=1, stroke=0)
        self.c.setFillColor(C_DARK)
        self.c.setFont('Helvetica-Bold', 10.5)
        style_t = ParagraphStyle('ht', fontName='Helvetica-Bold', fontSize=10.5,
                                  textColor=C_DARK, leading=14)
        pt = Paragraph(title, style_t)
        tw, th = pt.wrap(INN_W - 16, 100)
        pt.drawOn(self.c, INN_L + 16, self.y - th)
        self.y -= th + 3
        self.para(text, size=9.5, leading=13)
        self._rule(HexColor('#E0E0E0'))
        self.y -= 2

    # ── Recommendation block ──────────────────────────────────────────────────
    def rec_block(self, title, text):
        # Teal title bar
        bh = 18
        self.c.setFillColor(HexColor('#EBF5EE'))
        self.c.roundRect(INN_L, self.y - bh, INN_W, bh, 3, fill=1, stroke=0)
        self.c.setFillColor(C_GRN)
        self.c.setFont('Helvetica-Bold', 9.5)
        self.c.drawString(INN_L + 8, self.y - 12.5, title)
        self.y -= bh + 4
        self.para(text, size=9.5, leading=13, indent=8)
        self.y -= 2

    # ── Image ────────────────────────────────────────────────────────────────
    def image(self, path, height, caption=None):
        try:
            ir, (iw, ih) = pil_to_rl(path)
            ratio = iw / ih
            dh = min(height, ih / 3.78)
            dw = min(INN_W, dh * ratio)
            dh = dw / ratio
            self.c.drawImage(ir, INN_L + (INN_W - dw) / 2, self.y - dh, dw, dh)
            self.y -= dh + 4
            if caption:
                self.c.setFillColor(C_MUTED)
                self.c.setFont('Helvetica-Oblique', 8)
                self.c.drawCentredString(PW / 2, self.y, caption)
                self.y -= 13
        except Exception as e:
            print(f'  [image skip] {path}: {e}')

    # ── Logo inline ───────────────────────────────────────────────────────────
    def logo(self, path, x, y, max_h=50):
        try:
            ir, (iw, ih) = pil_to_rl(path)
            ratio = iw / ih
            dh = min(max_h, ih / 3.78)
            dw = dh * ratio
            self.c.drawImage(ir, x, y, dw, dh, mask='auto')
            return dw
        except Exception as e:
            print(f'  [logo skip] {path}: {e}')
            return 0

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _rule(self, color=C_RULE):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(0.7)
        self.c.line(INN_L, self.y, INN_R, self.y)
        self.y -= 2

    def gap(self, pts=8):
        self.y -= pts

    def hline(self):
        self._rule()
        self.y -= 6


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

def build(c):
    pb = PB(c)

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 1: Workshop at a Glance
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(1)
    pb.banner('WORKSHOP OVERVIEW')
    pb.gap(8)

    pb.c.setFillColor(C_DARK)
    pb.c.setFont('Helvetica-Bold', 19)
    pb.c.drawCentredString(PW / 2, pb.y, 'Workshop on Essentials for Mortality')
    pb.y -= 23
    pb.c.setFont('Helvetica-Bold', 19)
    pb.c.drawCentredString(PW / 2, pb.y, 'Investigation of Asian Elephant')
    pb.y -= 16
    pb.c.setFillColor(C_GRN)
    pb.c.setFont('Helvetica-Bold', 11)
    pb.c.drawCentredString(PW / 2, pb.y, 'Chhattisgarh Forest Department · Bilaspur Circle')
    pb.y -= 14
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica', 9.5)
    pb.c.drawCentredString(PW / 2, pb.y,
        'In Technical Partnership with Wildlife Institute of India & ICAR-IVRI')
    pb.y -= 13
    pb.c.setFillColor(C_DARK)
    pb.c.setFont('Helvetica-Bold', 10)
    pb.c.drawCentredString(PW / 2, pb.y, '30 – 31 May 2026  ·  Bilaspur, Chhattisgarh')
    pb.y -= 20

    pb.stats_row([
        ('2',   'Days'),
        ('18',  'Sessions'),
        ('5',   'National\nExperts'),
        ('30+', 'Participants'),
        ('48',  'Elephant\nDeaths Analyzed'),
    ])

    pb.image(f'{IMG_DIR}/cover-photo-main.jpg', 185,
             'Inaugural session — Workshop on Mortality Investigation of Asian Elephant, Bilaspur, May 2026.')
    pb.gap(4)

    pb.para(
        'The <b>Workshop on Essentials for Mortality Investigation of Asian Elephant</b> was organized '
        'by the Chhattisgarh Forest Department, Bilaspur Circle, in technical partnership with the '
        '<b>Wildlife Institute of India</b>, Dehradun, and <b>ICAR-IVRI</b>, Bareilly. Held on '
        '30–31 May 2026 at Bilaspur, the two-day workshop brought together five nationally eminent '
        'experts in wildlife health, veterinary pathology, and forensic science to equip field officers '
        'from the Dharamjaigarh and Raigarh Van Mandals with systematic, evidence-based skills for '
        'elephant mortality investigation.'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 2: Organizing Team & Technical Partners
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(2)

    # Logos row
    logo_y = pb.y - 4
    dw1 = pb.logo(f'{IMG_DIR}/logo-cg.png', INN_L, logo_y - 52, max_h=52)
    pb.logo(f'{IMG_DIR}/logo-wii.png', INN_L + dw1 + 14, logo_y - 48, max_h=45)
    pb.y -= 62

    pb.banner('Organizing Team')
    pb.gap(4)

    pb.c.setFillColor(C_NAVY)
    pb.c.setFont('Helvetica-Bold', 11)
    pb.c.drawCentredString(PW / 2, pb.y, 'Under the Guidance of')
    pb.y -= 15
    pb.c.setFillColor(C_GRN)
    pb.c.setFont('Helvetica-Bold', 10.5)
    pb.c.drawCentredString(PW / 2, pb.y,
        'Principal Chief Conservator of Forests & Head of Forest Force, Chhattisgarh')
    pb.y -= 14
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica', 9.5)
    pb.c.drawCentredString(PW / 2, pb.y,
        'Chief Conservator of Forests, Bilaspur Circle  ·  Conservator of Forests, Bilaspur')
    pb.y -= 20
    pb.hline()

    pb.section_heading('Technical Partners')
    pb.para(
        '<b>Wildlife Institute of India (WII)</b>, Dehradun — India\'s premier institution for '
        'wildlife research and training, contributing faculty expertise in wildlife health management, '
        'chemical capture of wild animals, and wildlife forensic science.'
    )
    pb.gap(4)
    pb.para(
        '<b>ICAR–Indian Veterinary Research Institute (IVRI)</b>, Bareilly — National centre for '
        'veterinary pathology, disease diagnosis, and wildlife health surveillance, contributing '
        'expertise in field necropsy, molecular diagnostics, comprehensive sampling protocols, '
        'and disease outbreak investigation.'
    )
    pb.gap(4)
    pb.para(
        '<b>Nanaji Deshmukh Veterinary Science University (NDVSU)</b>, Jabalpur — Contributing '
        'expertise in wildlife forensics and health management drawn from three decades of '
        'field experience across Central India\'s forest landscapes.'
    )
    pb.gap(8)
    pb.hline()

    pb.section_heading('Resource Persons')
    pb.faculty_card('01', 'Dr. Parag Nigam',
        'Senior Scientist & Head, Wildlife Health Management',
        'Wildlife Institute of India, Dehradun', 'Session Chair')
    pb.faculty_card('02', 'Dr. A. B. Shrivastav',
        'Former Director, Centre for Wildlife Forensic & Health; Professor & Veterinary Pathologist',
        'NDVSU, Jabalpur', 'Resource Person')
    pb.faculty_card('03', 'Dr. Karikalan Mathesh',
        'Senior Scientist, Centre for Wildlife Conservation, Management & Disease Surveillance',
        'ICAR-IVRI, Bareilly', 'Resource Person')
    pb.faculty_card('04', 'Dr. Chandra Prakash Sharma',
        'Principal Technical Officer & In-charge, Morphology Unit, WFCGC',
        'Wildlife Institute of India, Dehradun', 'Resource Person')
    pb.faculty_card('05', 'Dr. Tapendra Saini',
        'Scientist C, Wildlife Institute of India',
        'Wildlife Institute of India, Dehradun', 'Resource Person')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 3: Speaker Statements
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(3)
    pb.banner('Speaker Statements')
    pb.gap(12)

    quotes = [
        ('Dr. A. B. Shrivastav',
         'Every elephant death is a data point — if we investigate systematically, the forest tells us exactly what we need to know to prevent the next one.',
         True),
        ('Dr. Parag Nigam',
         'Systematic necropsy is not just a scientific procedure; it is an act of accountability to the elephant, to the ecosystem, and to the communities that share this landscape.',
         False),
        ('Dr. Karikalan Mathesh',
         'EEHV is a silent predator. Without PCR diagnostics reaching the ground level, we remain blind to the most lethal infectious threat young elephants face today.',
         True),
        ('Dr. Chandra Prakash Sharma',
         'Evidence collected poorly is evidence lost forever. Forensic discipline at the mortality site determines the outcome of every investigation — and every court proceeding.',
         False),
        ('Dr. Tapendra Saini',
         'Every tissue sample we preserve today is a resource for tomorrow\'s conservation science. The necropsy table is where field work meets molecular genetics.',
         True),
    ]

    for name, quote, dark in quotes:
        pb.speaker_card(name, quote, dark)

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 4: Workshop Background & Context
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(4)
    pb.section_heading('Workshop Background')

    pb.para(
        '<b>Chhattisgarh has emerged as one of India\'s most significant elephant habitats</b>, '
        'with the Bilaspur Circle — encompassing the Dharamjaigarh and Raigarh Van Mandals — '
        'hosting the state\'s highest concentration of wild elephants. The elephant population '
        'has grown remarkably, from an estimated 24 individuals in 2001 to approximately 451 '
        'elephants in 2026, reflecting nearly 10% compound annual growth. This rapid expansion '
        'has intensified the human-elephant interface and, critically, raised the toll of '
        'elephant mortalities to a level demanding systematic institutional response.'
    )
    pb.gap(6)

    pb.pull_quote(
        'Between 2021–22 and 2026–27, a total of 48 elephant deaths were recorded across '
        'Dharamjaigarh (27 deaths) and Raigarh (21 deaths) Van Mandals. Electrocution (51%) '
        'and drowning (22%) account for the majority. The 2025–26 season recorded the highest '
        'single-year toll in the five-year study period, with 2026–27 already showing a '
        'disturbing pattern of calf drowning deaths in the early months.',
        '— Chhattisgarh Forest Department Data, 2021–2026'
    )

    pb.para(
        'Despite this growing urgency, field officers across both divisions faced significant '
        'gaps in standardized procedures for elephant mortality investigation. The absence of '
        'structured training in necropsy protocols, sample collection, forensic documentation, '
        'and legal frameworks meant that critical evidence was often lost in the immediate '
        'aftermath of deaths — limiting the department\'s ability to determine cause of death, '
        'prevent future incidents, and pursue legal action where warranted.'
    )
    pb.gap(6)
    pb.para(
        'Recognizing this critical gap, the Chhattisgarh Forest Department, Bilaspur Circle, '
        'conceptualized and executed this intensive two-day capacity-building workshop. The '
        'initiative drew on the expertise of the Wildlife Institute of India and ICAR-IVRI '
        'to bridge the knowledge gap and build lasting institutional capacity.'
    )
    pb.gap(10)

    pb.section_heading('Workshop Objectives')
    pb.bullet(
        'To train field officers in systematic and scientific investigation of elephant mortalities, '
        'covering veterinary, forensic, and legal dimensions.'
    )
    pb.bullet(
        'To standardize necropsy procedures, sampling protocols, and mortality documentation '
        'practices for the Dharamjaigarh and Raigarh Van Mandals.'
    )
    pb.bullet(
        'To equip officers with the knowledge to identify major causes of elephant death — '
        'electrocution, drowning, infectious diseases, and poisoning — and implement targeted '
        'preventive measures.'
    )
    pb.gap(10)

    pb.section_heading('Expected Outcomes')
    pb.bullet(
        'A trained cadre of field officers capable of conducting scientifically rigorous elephant '
        'mortality investigations across both Van Mandals.'
    )
    pb.bullet(
        'Standardized field protocols and checklists adopted by the Bilaspur Circle for all '
        'future elephant mortality investigations.'
    )
    pb.bullet(
        'Strengthened institutional linkages between the Chhattisgarh Forest Department, WII, '
        'and ICAR-IVRI for ongoing technical support and diagnostic laboratory access.'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 5: Inaugural Session — Part 1
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(5)
    pb.section_heading('Inaugural Session')
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica-Bold', 9.5)
    pb.c.drawString(INN_L, pb.y, '30 May 2026  ·  10:00 – 11:00 hrs  ·  Bilaspur, Chhattisgarh')
    pb.y -= 16

    pb.para(
        'The workshop commenced with a formal inaugural session attended by senior officers of '
        'the Chhattisgarh Forest Department, field staff from both Van Mandals, and all five '
        'national resource persons. The session was presided over by the Chief Conservator of '
        'Forests, Bilaspur Circle, with Dr. Parag Nigam, Senior Scientist & Head of Wildlife '
        'Health Management at WII, serving as Session Chair.'
    )
    pb.gap(8)

    pb.section_heading('Welcome Address', 13)
    pb.para(
        'The welcome address set the context for the two-day programme. The organizing officer '
        'extended a warm welcome to all participants and resource persons, acknowledging the '
        'significance of bringing national expertise directly to the field level in Chhattisgarh. '
        'He highlighted the acute challenge facing the Bilaspur Circle: a growing elephant '
        'population navigating an increasingly fragmented landscape, with mortality records '
        'pointing to preventable causes as the dominant threat. '
    )
    pb.gap(4)
    pb.para(
        'He emphasized that field officers are the first responders at any elephant mortality '
        'site, and that the quality of investigation in those initial hours determines everything '
        'that follows — from legal proceedings to conservation interventions. The workshop, he '
        'noted, was designed not merely as a training exercise but as the foundation for a '
        'permanent, institutionalized protocol that would serve the department for years to come.'
    )
    pb.gap(4)
    pb.pull_quote(
        'Our field officers are not just administrators — they are the first scientists on scene '
        'at every elephant death. This workshop exists to give them the tools, knowledge, and '
        'confidence to do that job with the precision and accountability it demands.',
        '— Welcome Address, Inaugural Session'
    )

    pb.image(f'{IMG_DIR}/cover-photo-sm1.jpg', 155,
             'Inaugural ceremony — Workshop on Mortality Investigation of Asian Elephant, Bilaspur, May 2026.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 6: Inaugural Session — Faculty & Inaugural Address
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(6)
    pb.section_heading('Inaugural Remarks by Resource Persons')

    pb.subhead('Dr. Parag Nigam — Senior Scientist & Head, Wildlife Health Management, WII')
    pb.para(
        'Dr. Nigam, in his inaugural remarks, underscored the urgent need for evidence-based '
        'investigation of wildlife mortalities. Drawing from nearly three decades of field '
        'experience — including India\'s first tiger reintroduction at Sariska and landmark '
        'Indian Gaur reintroductions — he spoke to the critical importance of systematic field '
        'necropsy as the cornerstone of wildlife conservation medicine. He noted that '
        'Chhattisgarh\'s elephant population growth was a conservation success story, but one '
        'that came with new responsibilities for the forest department in managing mortalities '
        'with scientific rigor. Dr. Nigam expressed that the WII–ICAR-IVRI partnership for '
        'this workshop represented a model of institutional collaboration that could be replicated '
        'across other states facing similar challenges.'
    )
    pb.gap(8)

    pb.subhead('Dr. A. B. Shrivastav — Former Director, Centre for Wildlife Forensic & Health, NDVSU')
    pb.para(
        'Prof. Shrivastav addressed the gathering with particular insight into the One Health '
        'dimension of elephant mortalities. He emphasized that diseases transmissible between '
        'elephants, livestock, and humans — particularly tuberculosis and anthrax — make '
        'systematic mortality investigation a public health imperative, not merely a wildlife '
        'conservation concern. He also highlighted that Chhattisgarh\'s forests, with their unique '
        'biodiversity and tribal communities, demand locally adapted investigation protocols. '
        'He called for the workshop\'s outcomes to be converted into a formal State-level Standard '
        'Operating Procedure, backed by departmental order, that would outlast individual officers.'
    )
    pb.gap(10)
    pb.hline()

    pb.section_heading('Inaugural Address')
    pb.para(
        'The inaugural address by the presiding senior officer placed the workshop within '
        'Chhattisgarh\'s broader wildlife governance trajectory. He noted that the state\'s '
        '44.2% forest cover and the remarkable growth of its elephant population reflected '
        'the dedication of field staff across decades of service. However, he acknowledged '
        'that the intensification of human-elephant conflict and the rising mortality figures '
        'demanded a new quality of response from the department — one grounded in science '
        'rather than routine documentation.'
    )
    pb.gap(6)
    pb.para(
        'The address concluded with the formal lighting of the lamp by all resource persons '
        'and senior departmental officers, marking the official commencement of the workshop. '
        'A group photograph of all participants, faculty, and organizing officers was taken '
        'following the inaugural ceremony, and the session set a tone of collaborative learning '
        'and scientific discipline that characterized the two-day programme.'
    )
    pb.gap(6)

    pb.image(f'{IMG_DIR}/cover-photo-sm2.jpg', 145,
             'Resource persons and participants at the inaugural ceremony, Bilaspur, 30 May 2026.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 7: Workshop Programme
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(7)
    pb.section_heading('Workshop Programme')
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica', 9.5)
    pb.c.drawString(INN_L, pb.y,
        'Two-Day Programme  ·  30–31 May 2026  ·  Bilaspur, Chhattisgarh  ·  18 Sessions')
    pb.y -= 16

    # Day 1
    pb.day_header('Day 1', '30 May 2026', '10:00 – 17:30')
    pb.sched_row('10:00\n11:00', 'Inauguration',
        'Official opening, workshop objectives, introduction of experts & participants.',
        '—')
    pb.sched_row('11:00\n11:30', 'Elephant Status & Human-Elephant Interface in Chhattisgarh',
        'Population dynamics, corridor use, conflict and mortality trends.',
        'CG Forest Dept.')
    pb.sched_row('11:30\n12:15', 'Biological & Anatomical Aspects of Elephants',
        'Key anatomical peculiarities relevant to field investigation.',
        'Dr. P. Nigam')
    pb.sched_row('12:15\n13:00', 'Understanding Wildlife Mortalities: The Veterinary Perspective',
        'Carcass condition, natural vs unnatural death; ante/post-mortem changes & time of death.',
        'Dr. P. Nigam')
    pb.break_row('— Lunch Break: 13:00 – 14:00 —')
    pb.sched_row('14:00\n15:30', 'Infectious Causes of Mortality in Elephants',
        'EEHV, EMC, FMD, Rabies, TB, Anthrax, Haemorrhagic Septicaemia.',
        'Dr. K. Mathesh, Dr. Shrivastav')
    pb.sched_row('15:30\n16:30', 'Non-Infectious & Disaster Mortalities',
        'Electrocution, lightning, train hits, infighting, natural disaster deaths.',
        'Dr. Shrivastav, Dr. K. Mathesh')
    pb.sched_row('16:30\n17:30', 'Non-Infectious Diseases in Elephants',
        'Mycotoxicosis, kodo millet poisoning, and environmental bio-toxins.',
        'Dr. K. Mathesh, Dr. P. Nigam')

    pb.gap(12)

    # Day 2
    pb.day_header('Day 2', '31 May 2026', '09:30 – 17:30', gold=True)
    pb.sched_row('09:30\n10:15', 'Biosafety & Biosecurity at Elephant Mortality Sites',
        'Zoonotic risks, PPE requirements, safe carcass disposal, site sanitation.',
        'Dr. K. Mathesh, Dr. Saini, Dr. Nigam', gold=True)
    pb.sched_row('10:15\n11:00', 'Equipment Familiarization & Site Preparation',
        'Chain saws, axes, winches; establishing a secure investigation perimeter.',
        'Dr. Shrivastav, Dr. K. Mathesh, Dr. Saini', gold=True)
    pb.break_row('— Tea Break & Equipment Demonstration: 11:00 – 11:30 —')
    pb.sched_row('11:30\n12:30', 'Comprehensive Sampling Protocols',
        'Collection, packaging, cold chain, transport & documentation for lab analysis.',
        'Dr. K. Mathesh, Dr. Shrivastav, Dr. Saini', gold=True)
    pb.sched_row('12:30\n13:00', 'Recording Information During Necropsy',
        'Report writing and photographic documentation standards.',
        'Dr. K. Mathesh, Dr. Shrivastav', gold=True)
    pb.break_row('— Lunch Break: 13:00 – 14:00 —')
    pb.sched_row('14:00\n14:45', 'Vetro-Legal & Forensic Aspects of Mortality Investigation',
        'Investigation essentials for legal and forensic frameworks.',
        'Dr. C.P. Sharma', gold=True)
    pb.sched_row('14:45\n16:00', 'Practical: Crime Scene Investigation',
        'Chain of custody, evidence collection, legal procedures for ivory/tusk extraction.',
        'Dr. C.P. Sharma, Dr. Nigam, Dr. Saini', gold=True)
    pb.sched_row('16:15\n16:45', 'Panel Discussion',
        'Critical aspects of managing mortalities in elephants.',
        'All Faculty & CG Officers', gold=True)
    pb.sched_row('16:45\n17:30', 'Valedictory',
        'Workshop recap, feedback collection, and closing ceremony.',
        '—', gold=True)

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 8: Session Highlights — Day 1
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(8)
    pb.section_heading('Session Highlights · Day 1 · 30 May 2026')

    pb.highlight(
        'Elephant Status & Human-Elephant Interface in Chhattisgarh',
        'The opening technical session presented a comprehensive overview of elephant population '
        'dynamics in the Bilaspur Circle. Data revealed a remarkable growth trajectory from '
        '24 elephants in 2001 to an estimated 451 by 2026, with the Dharamjaigarh and Raigarh '
        'Van Mandals emerging as the primary habitat zone. Participants were presented with '
        'year-wise mortality data showing 48 deaths over five years, with electrocution (51%) '
        'and drowning (22%) as the dominant causes. The intensification of conflict as '
        'agricultural expansion encroaches on traditional corridors was identified as the '
        'central management challenge for the coming decade.'
    )

    pb.highlight(
        'Biological & Anatomical Aspects of Elephants',
        'Dr. Parag Nigam delivered an engaging session on the unique anatomy and physiology of '
        'Asian elephants, with a focus on features directly relevant to field investigation. '
        'Topics covered included the elephant\'s unusual foot structure, dental formula and tusk '
        'anatomy, the position and size of major organs, and the challenges posed by the animal\'s '
        'great bulk for necropsy procedures. Officers learned to identify key anatomical landmarks '
        'that guide incision sequences during post-mortem examination, and gained an appreciation '
        'for why elephant necropsy requires specialized equipment and a coordinated multi-person team.'
    )

    pb.highlight(
        'Understanding Wildlife Mortalities: The Veterinary Perspective',
        'This session introduced participants to the fundamental framework for classifying wildlife '
        'deaths — natural versus unnatural, acute versus chronic. Dr. Nigam covered ante-mortem '
        'and post-mortem changes in detail, helping officers understand how ambient temperature, '
        'sun exposure, and time since death alter the carcass and what evidence can still be '
        'recovered under various decomposition conditions. The session was particularly valued by '
        'field officers who routinely encounter carcasses in advanced decomposition and have '
        'struggled to determine cause of death under such conditions.'
    )

    pb.highlight(
        'Infectious Causes of Mortality in Elephants',
        'The afternoon\'s most extensive session — co-delivered by Dr. Karikalan Mathesh and '
        'Dr. A.B. Shrivastav — provided a systematic review of infectious diseases known to '
        'cause mortality in Asian elephants. Elephant Endotheliotropic Herpesvirus (EEHV) '
        'received particular attention, with Dr. Karikalan presenting diagnosed case data and '
        'emphasizing the critical role of whole blood PCR in confirming infection. Foot and '
        'Mouth Disease, Rabies, Tuberculosis, Anthrax, and Haemorrhagic Septicaemia were also '
        'covered, with participants equipped to recognize field signs and gross pathological '
        'changes indicative of each disease.'
    )

    pb.highlight(
        'Non-Infectious & Disaster Mortalities',
        'This session addressed the dominant cause of elephant deaths in Chhattisgarh: '
        'electrocution. Dr. Shrivastav presented a systematic framework for distinguishing '
        'electrocution deaths from other causes, including the characteristic lesions — entry '
        'and exit burns, supra-orbital lesions, internal haemorrhages — and the critical role '
        'of the investigative report in triggering action against illegal power line installations. '
        'Lightning strikes, train collision deaths, drowning, and infighting-related fatalities '
        'were also covered, with emphasis on the pathological features that distinguish each.'
    )

    pb.highlight(
        'Non-Infectious Diseases in Elephants',
        'The final Day 1 session addressed toxicological causes of elephant deaths — a critically '
        'under-investigated category in the Indian context. Dr. Karikalan presented detailed '
        'information on mycotoxicosis, with particular attention to kodo millet toxicity (a '
        'documented cause of elephant deaths in central India), and reviewed environmental '
        'bio-toxins. Officers left equipped with a framework for considering toxicological '
        'causes when initial investigation reveals no clear evidence of trauma, infectious '
        'disease, or natural illness.'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 9: Session Highlights — Day 2
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(9)
    pb.section_heading('Session Highlights · Day 2 · 31 May 2026')

    pb.highlight(
        'Biosafety & Biosecurity at Elephant Mortality Sites',
        'Day 2 opened with a critical session on the biosafety risks associated with elephant '
        'carcasses and the systematic measures required to protect field staff. Dr. Karikalan '
        'outlined the spectrum of zoonotic risks — from anthrax and tuberculosis to other '
        'pathogens transmissible through carcass contact — and the standard PPE requirements '
        'for all personnel at a mortality site. The session covered safe carcass disposal, '
        'site decontamination protocols, and the specific biosecurity measures required when '
        'infectious disease is suspected as the cause of death.',
        accent=C_GOLD
    )

    pb.highlight(
        'Equipment Familiarization & Site Preparation',
        'A hands-on session focused on the practical challenges of elephant necropsy under '
        'field conditions. Participants were introduced to the heavy-duty equipment required '
        '— chain saws, large-blade axes, winches, and block-and-tackle systems — and the '
        'sequence for their use during necropsy. The critical importance of establishing a '
        'secure investigation perimeter, controlling access, and documenting the site before '
        'any physical intervention was emphasized. Participants practiced identifying where '
        'to position equipment and personnel at a simulated mortality site.',
        accent=C_GOLD
    )

    pb.highlight(
        'Comprehensive Sampling Protocols',
        'This session addressed one of the most critical gaps in current practice: the '
        'collection, preservation, and transport of biological samples from elephant carcasses. '
        'The full spectrum of sample types was covered — fresh tissue for histopathology, blood '
        'for virology and haematology, swabs for bacteriology, rumen contents for toxicology, '
        'and environmental samples. Participants received detailed instruction on container '
        'types, preservation media, cold chain requirements, and the documentation and labelling '
        'standards required for samples to be accepted by ICAR-IVRI\'s diagnostic laboratory.',
        accent=C_GOLD
    )

    pb.highlight(
        'Recording Information During Necropsy',
        'Dr. Karikalan and Dr. Shrivastav covered the systematic documentation requirements for '
        'a complete necropsy record. Participants learned the standard format for field necropsy '
        'reports — including carcass condition scoring, gross pathological findings by organ '
        'system, preliminary cause-of-death assessment, and a complete sample inventory. '
        'The critical importance of photographic documentation was emphasized, with guidance '
        'on the specific images required at each stage to create a complete visual record '
        'admissible as evidence in legal proceedings.',
        accent=C_GOLD
    )

    pb.highlight(
        'Vetro-Legal & Forensic Aspects of Mortality Investigation',
        'Dr. Chandra Prakash Sharma delivered this pivotal session on the legal and forensic '
        'dimensions of wildlife mortality investigation. Topics included chain-of-custody '
        'protocols for evidence, the legal framework for ivory/tusk extraction and custody '
        'under the Wildlife Protection Act, and the standards for forensic reports that '
        'withstand court scrutiny. Participants gained clarity on their legal obligations '
        'at a mortality site and the precise procedures for coordinating with police '
        'and revenue authorities in multi-agency investigations.',
        accent=C_GOLD
    )

    pb.highlight(
        'Practical: Crime Scene Investigation',
        'The workshop\'s practical session was its highlight for field officers. Dr. Sharma '
        'led participants through a simulated crime scene investigation exercise covering '
        'evidence marking, photography, chain-of-custody documentation, and evidence packaging. '
        'Officers practiced the specific procedures for ivory/tusk extraction — a process with '
        'legal, forensic, and conservation dimensions — and were guided through the documentation '
        'sequence that creates a legally defensible investigation record. The practical was '
        'evaluated by all faculty, with additional guidance provided on forensic sample '
        'collection at the simulated site.',
        accent=C_GOLD
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 10: Key Outcomes & Recommendations
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(10)
    pb.section_heading('Key Outcomes & Recommendations')

    pb.para(
        'The two-day workshop generated concrete outcomes and forward-looking recommendations '
        'reflecting the consensus of national experts and field officers from both Van Mandals.'
    )
    pb.gap(8)

    pb.section_heading('Key Outcomes', 13)
    pb.bullet(
        'Thirty-plus field officers from Dharamjaigarh and Raigarh Van Mandals trained in '
        'systematic elephant mortality investigation across veterinary, forensic, and legal dimensions.'
    )
    pb.bullet(
        'A standardized <b>Field Necropsy Checklist</b> and <b>Sample Collection Protocol</b> '
        'developed and distributed to all participants, adapted for Chhattisgarh\'s field conditions.'
    )
    pb.bullet(
        'Consensus reached on a <b>Minimum Evidence Standard</b> for elephant mortality '
        'investigation reports submitted to the department — covering carcass documentation, '
        'sample inventory, photographic record, and preliminary cause-of-death assessment.'
    )
    pb.bullet(
        'Strengthened institutional relationships established between the Chhattisgarh Forest '
        'Department, WII, and ICAR-IVRI for ongoing technical support and diagnostic laboratory access.'
    )
    pb.bullet(
        'A framework for a <b>dedicated Elephant Mortality Investigation Cell</b> within the '
        'Bilaspur Circle proposed, with defined roles, equipment requirements, and laboratory '
        'referral pathways.'
    )
    pb.gap(10)

    pb.section_heading('Recommendations', 13)
    pb.rec_block('Standard Operating Procedure',
        'The Chhattisgarh Forest Department should develop and circulate a formal departmental '
        'SOP for elephant mortality investigation, drawing on the protocols shared during the '
        'workshop and adapted to the specific terrain, resources, and legal context of the state.')
    pb.gap(4)
    pb.rec_block('Dedicated Mortality Investigation Team',
        'Each Van Mandal should designate a core team of trained officers — including at least '
        'one Range Officer with necropsy training — as the first-response unit for elephant '
        'mortality sites, with a pre-staged equipment kit maintained at division level.')
    pb.gap(4)
    pb.rec_block('Laboratory Linkage with ICAR-IVRI',
        'A formal sample referral arrangement with ICAR-IVRI, Bareilly, should be established '
        'to ensure that biological samples from elephant mortalities receive priority processing '
        'and systematic diagnostic reporting back to the field department.')
    pb.gap(4)
    pb.rec_block('Annual Refresher Training',
        'Given the complexity of elephant mortality investigation and the regular turnover of '
        'field staff, an annual refresher training programme is strongly recommended — '
        'potentially co-facilitated by trained Chhattisgarh Forest Department officers.')
    pb.gap(4)
    pb.rec_block('Electrocution Prevention as Priority',
        'With electrocution accounting for 51% of elephant deaths in the study period, the '
        'workshop strongly endorses prioritizing identification and removal of illegal / '
        'low-hung power lines as the single most impactful conservation intervention '
        'available to the department.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 11: Valedictory
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(11)
    pb.section_heading('Valedictory Session')
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica-Bold', 9.5)
    pb.c.drawString(INN_L, pb.y, '31 May 2026  ·  16:45 – 17:30 hrs')
    pb.y -= 16

    pb.para(
        'The valedictory session brought the two-day workshop to a formal and reflective close. '
        'Presided over by the senior officer of the Bilaspur Circle, the session provided an '
        'opportunity for participants and faculty alike to reflect on the learning journey of '
        'the preceding two days and articulate commitments for applying that learning in the field.'
    )
    pb.gap(8)

    pb.section_heading('Participant Reflections', 13)
    pb.para(
        'Selected field officers from both Van Mandals shared their key learnings. Recurring '
        'themes included: the transformative clarity gained on the necropsy procedure and its '
        'legal significance; new appreciation for the forensic value of initial site documentation; '
        'and the confidence gained from understanding the disease framework — particularly around '
        'EEHV, electrocution lesions, and toxicological causes — that had previously felt '
        'inaccessible without veterinary training. Several officers expressed that the practical '
        'crime scene investigation exercise was among the most valuable sessions of their careers.'
    )
    pb.gap(8)

    pb.section_heading('Closing Remarks by Faculty', 13)
    pb.para(
        'Dr. A. B. Shrivastav, in the closing faculty address, expressed that the quality of '
        'engagement from Chhattisgarh\'s field officers was exceptional and reflected genuine '
        'commitment to conservation excellence. He recommended that future editions include a '
        'practical necropsy demonstration on a wild animal carcass, and called for the workshop '
        'to become an annual fixture in the Bilaspur Circle\'s capacity-building calendar.'
    )
    pb.gap(6)
    pb.para(
        'Dr. Parag Nigam emphasized that the most important next step was institutional — '
        'converting the workshop\'s learning into formal departmental protocols that would '
        'survive officer transfers and administrative changes. He offered WII\'s ongoing '
        'technical support for the development of a Chhattisgarh SOP and for future training.'
    )
    pb.gap(8)

    pb.section_heading('Closing Address', 13)
    pb.para(
        'The closing address by the senior departmental officer highlighted the significance '
        'of the workshop in Chhattisgarh\'s elephant conservation trajectory. He expressed '
        'gratitude to all five resource persons, noting that the calibre of national expertise '
        'assembled was a testament to the importance that institutions attach to Chhattisgarh\'s '
        'growing elephant population.'
    )
    pb.gap(6)
    pb.pull_quote(
        'What we have built in these two days is not just knowledge — it is the foundation of '
        'a system. The 48 elephant deaths we have analyzed here must be the last generation '
        'of deaths that go uninvestigated. From this workshop forward, every death in our '
        'forests will be accounted for.',
        '— Closing Address, Valedictory Session'
    )
    pb.gap(4)
    pb.para(
        'Participation certificates were presented to all field officers by the senior faculty '
        'and departmental officers. A group photograph of all participants, faculty, and '
        'organizing staff was taken in closing. The workshop formally concluded at 17:30 hrs '
        'on 31 May 2026.'
    )

    c.showPage()
    c.save()
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    c = rl_canvas.Canvas(OUT, pagesize=A4)
    build(c)

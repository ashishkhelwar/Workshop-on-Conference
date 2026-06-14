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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import io, os, textwrap

# Register Devanagari font for Hindi text
_DEVA_REG  = '/tmp/NotoSansDevanagari-Regular.ttf'
_DEVA_BOLD = '/tmp/NotoSansDevanagari-Bold.ttf'
if os.path.exists(_DEVA_REG):
    pdfmetrics.registerFont(TTFont('Devanagari',     _DEVA_REG))
    pdfmetrics.registerFont(TTFont('Devanagari-Bold', _DEVA_BOLD))

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

    # ── Hindi text box (Devanagari) ───────────────────────────────────────────
    def hindi_box(self, text, size=10.5, bg=HexColor('#1A2840'), attrib=None):
        """Render Hindi text in a dark box using Devanagari font."""
        lines = text.replace('\n', ' ').split('। ')
        # Draw each sentence as separate para for wrapping
        style = ParagraphStyle(
            'hi', fontName='Devanagari', fontSize=size,
            textColor=white, alignment=TA_JUSTIFY, leading=size * 1.6,
        )
        paras = []
        for i, sent in enumerate(lines):
            s = sent.strip()
            if not s:
                continue
            if i < len(lines) - 1:
                s += '।'
            p = Paragraph(s, style)
            w, h = p.wrap(INN_W - 28, 2000)
            paras.append((p, h))

        total_h = sum(h for _, h in paras) + (len(paras) - 1) * 4
        bh = total_h + 26 + (16 if attrib else 0)

        self.c.setFillColor(bg)
        self.c.roundRect(INN_L, self.y - bh, INN_W, bh, 6, fill=1, stroke=0)

        cy = self.y - 14
        for p, h in paras:
            p.drawOn(self.c, INN_L + 14, cy - h)
            cy -= h + 4

        if attrib:
            self.c.setFillColor(C_GOLD)
            self.c.setFont('Helvetica-Bold', 8.5)
            self.c.drawRightString(INN_R - 10, self.y - bh + 7, attrib)

        self.y -= bh + 10

    # ── Officer address card (Minister / PCCF / CCF) ─────────────────────────
    def officer_heading(self, name, designation, dept=''):
        """Full-width highlighted name block for a speaker."""
        bh = 52 if dept else 38
        self.c.setFillColor(HexColor('#EBF5EE'))
        self.c.roundRect(INN_L, self.y - bh, INN_W, bh, 5, fill=1, stroke=0)
        self.c.setFillColor(C_GRN)
        self.c.setFont('Helvetica-Bold', 12)
        self.c.drawString(INN_L + 12, self.y - 18, name)
        self.c.setFillColor(C_DARK)
        self.c.setFont('Helvetica-Bold', 9.5)
        self.c.drawString(INN_L + 12, self.y - 30, designation)
        if dept:
            self.c.setFillColor(C_MUTED)
            self.c.setFont('Helvetica', 8.5)
            self.c.drawString(INN_L + 12, self.y - 42, dept)
        self.y -= bh + 8


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

def build(c):
    pb = PB(c)

    # ── HINDI SPEECH TEXT ────────────────────────────────────────────────────
    MINISTER_HINDI = (
        'छत्तीसगढ़ में हाथियों की संख्या पिछले 5 वर्षों से लगातार बढ़ रही है और वर्तमान में '
        'राज्य में लगभग 450 हाथी विचरण कर रहे हैं। ये हाथी सरगुजा, बिलासपुर, रायपुर और दुर्ग '
        'संभाग के वन क्षेत्रों में स्थाई रूप से विचरण कर रहे हैं। छत्तीसगढ़ शासन का वन एवं '
        'जलवायु परिवर्तन विभाग इन हाथियों के संरक्षण, संवर्धन और सुरक्षा के साथ-साथ जन समुदाय '
        'की सुरक्षा को भी ध्यान में रखते हुए लगातार कार्य कर रहा है। माननीय वन मंत्री, वन एवं '
        'जलवायु परिवर्तन विभाग, छत्तीसगढ़ शासन के निर्देशानुसार वन एवं जलवायु परिवर्तन विभाग '
        'हाथी-मानव द्वंद्व को शून्य की स्थिति में लाने का प्रयास कर रहा है, जिसमें सकारात्मक '
        'परिणाम भी सामने आए हैं। विगत कुछ दिनों से रायगढ़ जिले के रायगढ़ एवं धरमजयगढ़ '
        'वनमंडल में हाथी शावकों की मृत्यु की घटनाओं को ध्यान में रखते हुए तथा मृत्यु के कारणों '
        'को जानने के लिए माननीय वन मंत्री श्री केदार कश्यप के विशेष प्रयास से एक राष्ट्रीय स्तर '
        'की कार्यशाला का आयोजन दिनांक 05 एवं 06 जून 2026 को रायगढ़ जिले में किया जा रहा है। '
        'इस कार्यशाला में राष्ट्रीय स्तर के पशुचिकित्सक, वैज्ञानिक, हाथी विशेषज्ञ तथा '
        'छत्तीसगढ़ राज्य के पशुचिकित्सक भाग लेंगे। साथ ही राज्य के हाथी प्रभावित जिलों से '
        'वन एवं जलवायु परिवर्तन विभाग एवं पशु संसाधन विभाग के अधिकारी भी इस प्रशिक्षण में '
        'हिस्सा ले रहे हैं। कार्यशाला का उद्देश्य जंगली हाथियों की मृत्यु के कारणों का '
        'वैज्ञानिक अन्वेषण करना और भविष्य में प्रबंधन की रणनीति तैयार करना है। इसके अंतर्गत '
        'प्रतिभागियों को मृत हाथी की जांच, नमूने इकट्ठा करने और उन्हें सुरक्षित ढंग से भेजने '
        'का व्यावहारिक प्रशिक्षण दिया जाएगा। साथ ही शव संभालने में सुरक्षा, शव के उचित '
        'निपटान तथा हाथियों की मौत की घटनाओं और स्वास्थ्य निगरानी के लिए तैयारी को '
        'मज़बूत किया जाएगा।'
    )

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
    pb.c.drawCentredString(PW / 2, pb.y, '05 – 06 June 2026  ·  Raigarh, Chhattisgarh')
    pb.y -= 20

    pb.stats_row([
        ('2',   'Days'),
        ('18',  'Sessions'),
        ('5',   'National\nExperts'),
        ('30+', 'Participants'),
        ('48',  'Elephant\nDeaths Analyzed'),
    ])

    pb.image(f'{IMG_DIR}/cover-photo-main.jpg', 185,
             'Inaugural session — Workshop on Mortality Investigation of Asian Elephant, Raigarh, June 2026.')
    pb.gap(4)

    pb.para(
        'The <b>Workshop on Essentials for Mortality Investigation of Asian Elephant</b> was organized '
        'by the Chhattisgarh Forest Department, Bilaspur Circle, through the special initiative of '
        '<b>Hon\'ble Forest Minister Shri Kedar Kashyap</b>, in technical partnership with the '
        '<b>Wildlife Institute of India</b>, Dehradun, and <b>ICAR-IVRI</b>, Bareilly. Held on '
        '05–06 June 2026 at Raigarh, Chhattisgarh, the two-day workshop brought together five '
        'nationally eminent experts to equip field officers with systematic, evidence-based skills '
        'for elephant mortality investigation.'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 2: Organizing Team
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(2)

    # Logos row
    logo_y = pb.y - 4
    dw1 = pb.logo(f'{IMG_DIR}/logo-cg.png', INN_L, logo_y - 52, max_h=52)
    pb.logo(f'{IMG_DIR}/logo-wii.png', INN_L + dw1 + 14, logo_y - 48, max_h=45)
    pb.y -= 62

    pb.banner('Organizing Team')
    pb.gap(6)

    # Forest Minister
    pb.officer_heading(
        'Shri Kedar Kashyap',
        'Hon\'ble Forest Minister',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )

    # PCCF & HoFF
    pb.officer_heading(
        'Shri Arun Kumar Pandey, IFS',
        'Principal Chief Conservator of Forests & Head of Forest Force',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )

    pb.gap(4)
    pb.hline()

    pb.section_heading('Senior Officers')

    # Three officers in a 3-col layout
    officers = [
        ('Shri Matheshwaran V., IFS', 'APCCF Wildlife', 'CG Forest Dept.'),
        ('Shri Manoj Kumar Pandey, IFS', 'CCF, Bilaspur Circle', 'CG Forest Dept.'),
        ('Smt. Priyanka Pandey, IFS', 'CCF Wildlife Bilaspur\n& Field Director ATR', 'CG Forest Dept.'),
    ]
    n = len(officers)
    bw = (INN_W - (n - 1) * 8) / n
    bh = 64
    x = INN_L
    for name, desg, org in officers:
        pb.c.setFillColor(HexColor('#EBF5EE'))
        pb.c.roundRect(x, pb.y - bh, bw, bh, 5, fill=1, stroke=0)
        pb.c.setFillColor(C_GRN)
        pb.c.rect(x, pb.y - bh, 4, bh, fill=1, stroke=0)
        pb.c.setFillColor(C_NAVY)
        pb.c.setFont('Helvetica-Bold', 9)
        # Wrap name
        max_chars = int(bw / 5.2)
        lines = textwrap.wrap(name, max_chars)
        for i, ln in enumerate(lines[:2]):
            pb.c.drawString(x + 10, pb.y - 14 - i * 12, ln)
        pb.c.setFillColor(C_DARK)
        pb.c.setFont('Helvetica', 8.5)
        for i, dl in enumerate(desg.split('\n')):
            pb.c.drawString(x + 10, pb.y - 38 - i * 11, dl)
        pb.c.setFillColor(HexColor('#888888'))
        pb.c.setFont('Helvetica', 7.5)
        pb.c.drawString(x + 10, pb.y - bh + 9, org)
        x += bw + 8
    pb.y -= bh + 12
    pb.hline()

    pb.section_heading('Technical Partners')
    pb.para(
        '<b>Wildlife Institute of India (WII)</b>, Dehradun — India\'s premier institution for '
        'wildlife research and training, contributing expertise in wildlife health management, '
        'chemical capture, and wildlife forensic science.'
    )
    pb.gap(4)
    pb.para(
        '<b>ICAR–Indian Veterinary Research Institute (IVRI)</b>, Bareilly — National centre for '
        'veterinary pathology, wildlife disease diagnosis, and health surveillance, contributing '
        'expertise in necropsy, molecular diagnostics, and sampling protocols.'
    )
    pb.gap(4)
    pb.para(
        '<b>Nanaji Deshmukh Veterinary Science University (NDVSU)</b>, Jabalpur — Contributing '
        'expertise in wildlife forensics and health management drawn from three decades of '
        'field experience across Central India.'
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
        'has grown remarkably, from an estimated 24 individuals in 2001 to approximately 450 '
        'elephants in 2026, reflecting nearly 10% compound annual growth. These elephants '
        'inhabit forest areas across the Surguja, Bilaspur, Raipur, and Durg divisions. '
        'This rapid expansion has intensified the human-elephant interface and, critically, '
        'raised the toll of elephant mortalities to a level demanding systematic institutional response.'
    )
    pb.gap(6)

    pb.pull_quote(
        'Between 2021–22 and 2026–27, a total of 48 elephant deaths were recorded across '
        'Dharamjaigarh (27 deaths) and Raigarh (21 deaths) Van Mandals. Electrocution (51%) '
        'and drowning (22%) account for the majority. The 2025–26 season recorded the highest '
        'single-year toll, with 2026–27 already showing a disturbing pattern of calf drowning '
        'deaths in the early months of the year.',
        '— Chhattisgarh Forest Department Data, 2021–2026'
    )

    pb.para(
        'In view of the incidents of elephant calf deaths in the Raigarh and Dharamjaigarh '
        'Forest Divisions, and to understand the causes of such deaths, a national-level '
        'workshop was organized on 05–06 June 2026 in Raigarh district through the special '
        'initiative of <b>Hon\'ble Forest Minister Shri Kedar Kashyap</b>. The Department of '
        'Forest & Climate Change is working to bring human-elephant conflict to zero, '
        'with positive results already witnessed in the field.'
    )
    pb.gap(8)

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
    pb.gap(8)

    pb.section_heading('Participants')
    pb.bullet(
        '<b>Chhattisgarh Forest Department:</b> Range Officers, Beat Guards, and Wildlife Wardens '
        'from Dharamjaigarh and Raigarh Van Mandals, and officers from elephant-affected districts.'
    )
    pb.bullet(
        '<b>Animal Resources Department, Chhattisgarh:</b> Veterinary officers from '
        'elephant-affected districts of the state.'
    )
    pb.bullet(
        '<b>National Technical Experts:</b> Veterinarians, scientists, and elephant specialists '
        'from Wildlife Institute of India, ICAR-IVRI, and NDVSU Jabalpur.'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 5: Inaugural Address — Forest Minister Shri Kedar Kashyap
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(5)
    pb.section_heading('Inaugural Session')
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica-Bold', 9.5)
    pb.c.drawString(INN_L, pb.y,
        '05 June 2026  ·  10:00 – 11:00 hrs  ·  Raigarh, Chhattisgarh')
    pb.y -= 18

    pb.officer_heading(
        'Shri Kedar Kashyap',
        'Hon\'ble Forest Minister — Inaugural Address',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )

    pb.para(
        'The workshop was formally inaugurated by <b>Hon\'ble Forest Minister Shri Kedar Kashyap</b>, '
        'whose special initiative drove the organization of this national-level event in response '
        'to the recent incidents of elephant calf deaths in the Raigarh and Dharamjaigarh Forest '
        'Divisions. In his inaugural address, the Hon\'ble Minister spoke directly to the '
        'significance of this workshop — both as a conservation imperative and as a commitment '
        'to the communities living alongside Chhattisgarh\'s growing elephant population.'
    )
    pb.gap(8)

    # Subheading for Hindi text
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica-BoldOblique', 9)
    pb.c.drawString(INN_L, pb.y, 'Address in original Hindi | मूल हिंदी में उद्बोधन')
    pb.y -= 14

    pb.hindi_box(MINISTER_HINDI, size=10, attrib='— माननीय वन मंत्री श्री केदार कश्यप')

    pb.gap(6)
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica-BoldOblique', 9)
    pb.c.drawString(INN_L, pb.y, 'English Summary')
    pb.y -= 14

    pb.para(
        'The Hon\'ble Minister noted that Chhattisgarh\'s elephant population has grown steadily '
        'over the last five years to approximately 450 individuals, inhabiting the forest areas '
        'of Surguja, Bilaspur, Raipur, and Durg divisions. The Department of Forest & Climate '
        'Change is continuously working for their conservation and protection while ensuring '
        'community safety, and is striving to bring human-elephant conflict to zero. The workshop '
        'aims to scientifically investigate causes of wild elephant deaths, provide practical '
        'training in mortality examination, sample collection and safe dispatch, and strengthen '
        'preparedness for future mortality incidents and health surveillance.'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 6: Address by PCCF & HoFF Shri Arun Kumar Pandey
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(6)
    pb.section_heading('Address by PCCF & Head of Forest Force')

    pb.officer_heading(
        'Shri Arun Kumar Pandey, IFS',
        'Principal Chief Conservator of Forests & Head of Forest Force',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )

    pb.para(
        'Shri Arun Kumar Pandey, IFS, Principal Chief Conservator of Forests and Head of '
        'Forest Force, Chhattisgarh, addressed the workshop with a comprehensive overview '
        'of the state\'s elephant conservation efforts and the critical institutional context '
        'that made this workshop necessary and timely.'
    )
    pb.gap(6)
    pb.para(
        'Shri Pandey outlined the remarkable growth of Chhattisgarh\'s elephant population — '
        'from 24 individuals in 2001 to approximately 450 today — as a testament to the '
        'department\'s sustained conservation work over two decades. He acknowledged, however, '
        'that this population growth also brought new and complex challenges: increasing '
        'human-elephant conflict, expanding corridor pressure, and, most urgently, a rising '
        'toll of elephant deaths that demanded systematic investigation.'
    )
    pb.gap(6)
    pb.para(
        'He emphasized that the Chhattisgarh Forest Department, under the direction of '
        'Hon\'ble Forest Minister Shri Kedar Kashyap, is committed to understanding the '
        'precise causes of every elephant death — particularly the recent incidents of calf '
        'mortality in the Raigarh and Dharamjaigarh Van Mandals. He expressed that bringing '
        'national-level expertise from WII, ICAR-IVRI, and NDVSU to the field — rather than '
        'sending samples to distant laboratories without trained local personnel — represented '
        'a fundamental shift in the department\'s approach to wildlife health management.'
    )
    pb.gap(6)
    pb.pull_quote(
        'The strength of our forest department lies in its field officers. This workshop '
        'will give them the scientific tools to do their duty with the precision and '
        'accountability that these magnificent animals — and the communities living with '
        'them — deserve.',
        '— Shri Arun Kumar Pandey, IFS, PCCF & HoFF'
    )
    pb.para(
        'Shri Pandey called upon all participants to engage actively in both the theoretical '
        'and practical sessions, and to carry the learning back to their divisions with the '
        'commitment to establish standardized investigation protocols. He assured the resource '
        'persons of the department\'s full support in implementing the workshop\'s recommendations '
        'and developing a formal SOP for elephant mortality investigation in Chhattisgarh.'
    )
    pb.gap(10)

    pb.image(f'{IMG_DIR}/cover-photo-sm1.jpg', 150,
             'Inaugural ceremony — Workshop on Mortality Investigation of Asian Elephant, Raigarh, June 2026.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 7: Addresses by APCCF & CCF Officers
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(7)
    pb.section_heading('Addresses by Senior Officers')

    # APCCF Wildlife
    pb.officer_heading(
        'Shri Matheshwaran V., IFS',
        'Additional Principal Chief Conservator of Forests (Wildlife)',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )
    pb.para(
        'Shri Matheshwaran V., APCCF Wildlife, addressed the gathering from the perspective '
        'of wildlife management across the state. He highlighted that the elephant mortality '
        'challenge in Chhattisgarh is inseparable from the broader question of wildlife corridor '
        'management and human-wildlife coexistence. He emphasized the critical role of systematic '
        'mortality investigation in building an evidence base that directly informs policy and '
        'management interventions. He expressed the Wildlife Wing\'s commitment to institutionalizing '
        'the protocols developed through this workshop and extending the training to other '
        'elephant-affected divisions across the state.'
    )
    pb.gap(10)

    # CCF Bilaspur Circle
    pb.officer_heading(
        'Shri Manoj Kumar Pandey, IFS',
        'Chief Conservator of Forests, Bilaspur Circle',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )
    pb.para(
        'As the hosting officer for the workshop, Shri Manoj Kumar Pandey, CCF Bilaspur Circle, '
        'welcomed all resource persons, participants, and senior officers. He placed the workshop '
        'in the immediate operational context of the Bilaspur Circle, where the Dharamjaigarh '
        'and Raigarh Van Mandals have recorded 48 elephant deaths over the past five years. '
        'He acknowledged that while the Circle\'s field officers are dedicated and experienced, '
        'the specialized knowledge required for systematic elephant mortality investigation — '
        'particularly in disease diagnosis, forensic documentation, and sample chain-of-custody '
        '— had long been a gap that this workshop was specifically designed to address. '
        'He expressed gratitude to the Hon\'ble Minister and PCCF for their initiative and '
        'support in organizing this event.'
    )
    pb.gap(10)

    # CCF Wildlife & FD ATR
    pb.officer_heading(
        'Smt. Priyanka Pandey, IFS',
        'CCF Wildlife, Bilaspur  &  Field Director, Achanakmar Tiger Reserve',
        'Department of Forest & Climate Change, Government of Chhattisgarh'
    )
    pb.para(
        'Smt. Priyanka Pandey, CCF Wildlife Bilaspur and Field Director of the Achanakmar '
        'Tiger Reserve, brought a unique perspective to the inaugural session, highlighting '
        'the intersection of elephant mortality investigation with tiger reserve management. '
        'She emphasized that the movement of elephants through the ATR landscape made robust '
        'mortality investigation protocols essential not just for elephant conservation, but '
        'also for the integrity of tiger reserve management. She welcomed the national faculty '
        'and expressed confidence that the two-day workshop would lay the foundation for '
        'a new standard of scientific rigour in wildlife mortality investigation '
        'across Chhattisgarh\'s protected area network.'
    )

    pb.image(f'{IMG_DIR}/cover-photo-sm2.jpg', 130,
             'Inaugural session with senior officers and resource persons, Raigarh, 05 June 2026.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 8: Inaugural Remarks by Resource Persons
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(8)
    pb.section_heading('Inaugural Remarks by Resource Persons')

    pb.subhead('Dr. Parag Nigam — Senior Scientist & Head, Wildlife Health Management, WII')
    pb.para(
        'Dr. Nigam, in his inaugural remarks, underscored the urgent need for evidence-based '
        'investigation of wildlife mortalities. Drawing from nearly three decades of field '
        'experience — including India\'s first tiger reintroduction at Sariska and landmark '
        'Indian Gaur reintroductions — he spoke to the critical importance of systematic field '
        'necropsy as the cornerstone of wildlife conservation medicine. He commended the '
        'Chhattisgarh Forest Department for its proactive approach and expressed that the '
        'WII–ICAR-IVRI partnership for this workshop represented a model of institutional '
        'collaboration that could be replicated across other states facing similar challenges.'
    )
    pb.gap(8)

    pb.subhead('Dr. A. B. Shrivastav — Former Director, Centre for Wildlife Forensic & Health, NDVSU')
    pb.para(
        'Prof. Shrivastav addressed the gathering with particular insight into the One Health '
        'dimension of elephant mortalities. He emphasized that diseases transmissible between '
        'elephants, livestock, and humans — particularly tuberculosis and anthrax — make '
        'systematic mortality investigation a public health imperative, not merely a wildlife '
        'conservation concern. He called for the workshop\'s outcomes to be converted into a '
        'formal State-level Standard Operating Procedure, backed by departmental order.'
    )
    pb.gap(8)

    pb.subhead('Dr. Karikalan Mathesh — Senior Scientist, ICAR-IVRI, Bareilly')
    pb.para(
        'Dr. Karikalan spoke on the diagnostic laboratory\'s perspective on field-collected '
        'samples. He emphasized that the quality of samples received from field mortality sites '
        'determines what can and cannot be diagnosed — and that poor sample collection is the '
        'single most common reason why causes of death remain undetermined. He expressed that '
        'equipping Chhattisgarh\'s field officers with proper sampling knowledge would directly '
        'improve the diagnostic yield from every future mortality case referred to ICAR-IVRI.'
    )
    pb.gap(8)

    pb.subhead('Dr. Chandra Prakash Sharma — Principal Technical Officer, WII')
    pb.para(
        'Dr. Sharma brought the forensic scientist\'s perspective to the inaugural session. '
        'He noted that in his decades of work supporting enforcement agencies across India, '
        'the most common weakness in wildlife mortality cases reaching courts was inadequate '
        'field documentation. He expressed confidence that the forensic and legal sessions of '
        'the workshop would address this gap directly, equipping officers to build cases that '
        'could survive legal scrutiny.'
    )
    pb.gap(10)

    pb.pull_quote(
        'This workshop is not just about learning what to do — it is about learning what the '
        'law requires of you. Every forest officer at a mortality site is simultaneously a '
        'scientist, a custodian of evidence, and an officer of the law.',
        '— Dr. Chandra Prakash Sharma, Wildlife Institute of India'
    )

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 9: Workshop Programme
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(9)
    pb.section_heading('Workshop Programme')
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica', 9.5)
    pb.c.drawString(INN_L, pb.y,
        'Two-Day Programme  ·  05–06 June 2026  ·  Raigarh, Chhattisgarh  ·  18 Sessions')
    pb.y -= 16

    pb.day_header('Day 1', '05 June 2026', '10:00 – 17:30')
    pb.sched_row('10:00\n11:00', 'Inauguration',
        'Official opening, address by Forest Minister, PCCF & HoFF, senior officers, and resource persons.',
        'Forest Minister · PCCF · Senior Officers')
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

    pb.day_header('Day 2', '06 June 2026', '09:30 – 17:30', gold=True)
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
    # PAGE 10: Session Highlights — Day 1
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(10)
    pb.section_heading('Session Highlights · Day 1 · 05 June 2026')

    pb.highlight('Elephant Status & Human-Elephant Interface in Chhattisgarh',
        'The opening technical session presented a comprehensive overview of elephant population '
        'dynamics in the Bilaspur Circle. Data revealed a growth trajectory from 24 elephants '
        'in 2001 to approximately 450 by 2026, with the Dharamjaigarh and Raigarh Van Mandals '
        'as the primary habitat zone. Year-wise mortality data showing 48 deaths over five years '
        'was presented, with electrocution (51%) and drowning (22%) as dominant causes. '
        'The intensification of conflict as agricultural expansion encroaches on corridors was '
        'identified as the central management challenge.')

    pb.highlight('Biological & Anatomical Aspects of Elephants',
        'Dr. Parag Nigam delivered an engaging session on the unique anatomy and physiology of '
        'Asian elephants relevant to field investigation — including foot structure, dental formula '
        'and tusk anatomy, organ positions, and why elephant necropsy requires specialized equipment '
        'and a coordinated multi-person team. Officers learned to identify anatomical landmarks '
        'that guide incision sequences during post-mortem examination.')

    pb.highlight('Understanding Wildlife Mortalities: The Veterinary Perspective',
        'This session introduced the fundamental framework for classifying wildlife deaths — '
        'natural versus unnatural, acute versus chronic. Dr. Nigam covered ante-mortem and '
        'post-mortem changes in detail, helping officers understand how ambient temperature, '
        'sun exposure, and time since death alter the carcass. The session was particularly '
        'valued by officers who routinely encounter carcasses in advanced decomposition.')

    pb.highlight('Infectious Causes of Mortality in Elephants',
        'Co-delivered by Dr. Karikalan Mathesh and Dr. A.B. Shrivastav, this session provided '
        'a systematic review of infectious diseases known to cause elephant mortality. EEHV '
        'received particular attention, with the critical role of whole blood PCR emphasized. '
        'FMD, Rabies, Tuberculosis, Anthrax, and Haemorrhagic Septicaemia were also covered, '
        'with participants equipped to recognize field signs and gross pathological changes '
        'indicative of each disease.')

    pb.highlight('Non-Infectious & Disaster Mortalities',
        'Dr. Shrivastav presented a systematic framework for distinguishing electrocution deaths '
        'from other causes — characteristic lesions (entry/exit burns, supra-orbital lesions, '
        'internal haemorrhages) and the investigative report\'s role in triggering action against '
        'illegal power lines. Lightning strikes, train collisions, drowning, and infighting deaths '
        'were also covered with emphasis on distinguishing pathological features.')

    pb.highlight('Non-Infectious Diseases in Elephants',
        'The final Day 1 session addressed toxicological causes — a critically under-investigated '
        'category in the Indian context. Dr. Karikalan presented detailed information on '
        'mycotoxicosis, with particular attention to kodo millet toxicity (a documented cause '
        'of elephant deaths in central India), and reviewed environmental bio-toxins. Officers '
        'received a framework for considering toxicological causes when initial investigation '
        'reveals no clear evidence of trauma, infectious disease, or natural illness.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 11: Session Highlights — Day 2
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(11)
    pb.section_heading('Session Highlights · Day 2 · 06 June 2026')

    pb.highlight('Biosafety & Biosecurity at Elephant Mortality Sites',
        'Day 2 opened with a critical session on the biosafety risks associated with elephant '
        'carcasses. Dr. Karikalan outlined the spectrum of zoonotic risks — from anthrax and '
        'tuberculosis to other pathogens transmissible through carcass contact — and the '
        'standard PPE requirements for all personnel. The session covered safe carcass disposal, '
        'site decontamination protocols, and biosecurity measures required when infectious '
        'disease is suspected.', accent=C_GOLD)

    pb.highlight('Equipment Familiarization & Site Preparation',
        'A hands-on session focused on the practical challenges of elephant necropsy under field '
        'conditions. Participants were introduced to heavy-duty equipment required — chain saws, '
        'axes, winches, block-and-tackle systems — and the sequence for their use. The critical '
        'importance of establishing a secure investigation perimeter and documenting the site '
        'before any physical intervention was emphasized.', accent=C_GOLD)

    pb.highlight('Comprehensive Sampling Protocols',
        'This session addressed one of the most critical gaps in current practice: collection, '
        'preservation, and transport of biological samples from elephant carcasses. The full '
        'spectrum of sample types was covered — fresh tissue for histopathology, blood for '
        'virology, swabs for bacteriology, rumen contents for toxicology. Participants received '
        'detailed instruction on container types, preservation media, cold chain requirements, '
        'and documentation standards required for ICAR-IVRI\'s diagnostic laboratory.', accent=C_GOLD)

    pb.highlight('Recording Information During Necropsy',
        'Dr. Karikalan and Dr. Shrivastav covered systematic documentation requirements for a '
        'complete necropsy record — including carcass condition scoring, gross pathological '
        'findings by organ system, preliminary cause-of-death assessment, and sample inventory. '
        'Guidance was provided on the specific photographs required at each stage to create a '
        'complete visual record admissible as evidence in legal proceedings.', accent=C_GOLD)

    pb.highlight('Vetro-Legal & Forensic Aspects of Mortality Investigation',
        'Dr. Chandra Prakash Sharma delivered this pivotal session on legal and forensic '
        'dimensions of mortality investigation: chain-of-custody protocols, the legal framework '
        'for ivory/tusk custody under the Wildlife Protection Act, and forensic report standards '
        'that withstand court scrutiny. Participants gained clarity on their legal obligations '
        'at a mortality site and procedures for coordinating with police and revenue authorities.',
        accent=C_GOLD)

    pb.highlight('Practical: Crime Scene Investigation & Panel Discussion',
        'Dr. Sharma led participants through a simulated crime scene investigation covering '
        'evidence marking, photography, chain-of-custody documentation, and evidence packaging. '
        'Officers practiced ivory/tusk extraction procedures and the documentation sequence that '
        'creates a legally defensible investigation record. The subsequent Panel Discussion '
        'addressed specific operational challenges raised by field officers — from accessing '
        'remote mortality sites to multi-agency coordination protocols.', accent=C_GOLD)

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 12: Key Outcomes & Recommendations
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(12)
    pb.section_heading('Key Outcomes & Recommendations')

    pb.para(
        'The two-day workshop generated concrete outcomes and forward-looking recommendations '
        'reflecting the consensus of national experts and field officers from both Van Mandals.'
    )
    pb.gap(8)

    pb.section_heading('Key Outcomes', 13)
    pb.bullet(
        'Thirty-plus field officers from Dharamjaigarh and Raigarh Van Mandals and officers '
        'from elephant-affected districts trained in systematic elephant mortality investigation.'
    )
    pb.bullet(
        'A standardized <b>Field Necropsy Checklist</b> and <b>Sample Collection Protocol</b> '
        'developed and distributed to all participants, adapted for Chhattisgarh\'s field conditions.'
    )
    pb.bullet(
        'Consensus reached on a <b>Minimum Evidence Standard</b> for elephant mortality '
        'investigation reports — covering carcass documentation, sample inventory, photographic '
        'record, and preliminary cause-of-death assessment.'
    )
    pb.bullet(
        'Strengthened institutional relationships between the Chhattisgarh Forest Department, '
        'WII, ICAR-IVRI, and NDVSU for ongoing technical support and diagnostic laboratory access.'
    )
    pb.bullet(
        'A framework for a <b>dedicated Elephant Mortality Investigation Cell</b> within the '
        'Bilaspur Circle proposed, with defined roles, equipment requirements, and referral pathways.'
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
        'workshop strongly endorses prioritizing identification and removal of illegal and '
        'low-hung power lines as the single most impactful intervention available.')

    c.showPage()

    # ────────────────────────────────────────────────────────────────────────
    # PAGE 13: Valedictory
    # ────────────────────────────────────────────────────────────────────────
    pb.new_page(13)
    pb.section_heading('Valedictory Session')
    pb.c.setFillColor(C_MUTED)
    pb.c.setFont('Helvetica-Bold', 9.5)
    pb.c.drawString(INN_L, pb.y, '06 June 2026  ·  16:45 – 17:30 hrs  ·  Raigarh, Chhattisgarh')
    pb.y -= 16

    pb.para(
        'The valedictory session brought the two-day workshop to a formal and reflective close. '
        'Presided over by the CCF, Bilaspur Circle, and attended by all senior officers and '
        'resource persons, the session provided an opportunity for participants and faculty to '
        'reflect on the learning journey of the preceding two days.'
    )
    pb.gap(8)

    pb.section_heading('Participant Reflections', 13)
    pb.para(
        'Selected field officers from both Van Mandals shared their key learnings. Recurring '
        'themes included: the transformative clarity gained on the necropsy procedure and its '
        'legal significance; new appreciation for the forensic value of initial site documentation; '
        'and the confidence gained from understanding disease frameworks — particularly around '
        'EEHV, electrocution lesions, and toxicological causes. Several officers expressed '
        'that the practical crime scene investigation exercise was among the most valuable '
        'sessions of their careers.'
    )
    pb.gap(8)

    pb.section_heading('Closing Remarks by Faculty', 13)
    pb.para(
        'Dr. A. B. Shrivastav expressed that the quality of engagement from Chhattisgarh\'s '
        'field officers was exceptional. He recommended that future editions include a live '
        'necropsy demonstration and called for the workshop to become an annual event. '
        'Dr. Parag Nigam emphasized that the most important next step was institutional — '
        'converting the workshop\'s learning into formal departmental protocols. He offered '
        'WII\'s ongoing technical support for the development of a Chhattisgarh SOP and '
        'for future training iterations.'
    )
    pb.gap(8)

    pb.section_heading('Closing Address', 13)
    pb.para(
        'The closing address by Shri Manoj Kumar Pandey, CCF Bilaspur Circle, highlighted the '
        'significance of the workshop in Chhattisgarh\'s elephant conservation trajectory. '
        'He expressed gratitude to Hon\'ble Forest Minister Shri Kedar Kashyap for his vision '
        'in initiating this workshop, to PCCF Shri Arun Kumar Pandey for his leadership, '
        'and to all five resource persons for their dedicated engagement over two intensive days.'
    )
    pb.gap(6)
    pb.pull_quote(
        'What we have built in these two days is not just knowledge — it is the foundation '
        'of a system. The 48 elephant deaths we have analyzed here must be the last generation '
        'that go uninvestigated. From this workshop forward, every death in our forests '
        'will be accounted for.',
        '— Closing Address, Valedictory Session, 06 June 2026'
    )
    pb.gap(6)
    pb.para(
        'Participation certificates were presented to all field officers by the senior faculty '
        'and departmental officers. A group photograph of all participants and faculty was taken '
        'in closing. The workshop formally concluded at 17:30 hrs on 06 June 2026.'
    )

    c.showPage()
    c.save()
    print(f'Saved → {OUT}')


if __name__ == '__main__':
    c = rl_canvas.Canvas(OUT, pagesize=A4)
    build(c)

"""pptkit: small python-pptx kit for clean, editable 16:9 decks.

Everything is drawn on the Blank layout with text boxes, native charts and
native tables, so a team can edit every element in PowerPoint. Positions are
in inches on a 13.333 x 7.5 slide. Colours come from one theme dict (see
assets/themes.json), optionally toned "soft" or "hard"; sizes come from one
format ("video", "live", "read"); alignment is "left" or "center".

new_deck.py pastes this file into a self-contained build script, so keep it
free of imports from the rest of the skill.
"""

import math
import re

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE, XL_TICK_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

SLIDE_W, SLIDE_H = 13.333, 7.5
M = 0.6                      # left and right margin
CW = SLIDE_W - 2 * M         # content width, 12.133
TITLE_Y = 0.45
BODY_Y = 1.65                # first content row under a one-line title
BODY_BOTTOM = 6.75
FOOT_Y = 6.98

# Type scale per delivery format. Each level is clearly bigger than the one
# below it, so the eye finds the title, then the number, then the detail.
# "floor" is the smallest text allowed on a slide that is not a source line.
SIZES = {
    "video": dict(cover=54, title=32, sub=20, h=18, body=14, label=12, small=12, foot=10.5, big=40, hero=56, floor=12),
    "live":  dict(cover=60, title=36, sub=22, h=20, body=18, label=14, small=14, foot=11, big=48, hero=64, floor=14),
    "read":  dict(cover=44, title=28, sub=17, h=15, body=12, label=10, small=10, foot=9, big=32, hero=44, floor=10),
}

NO_STYLE_TABLE = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


# ---------- colour helpers ----------

def rgb(hex6):
    return RGBColor.from_string(hex6.lstrip("#").upper())


def _channels(hex6):
    h = hex6.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    """Blend colour a toward colour b by t (0 = a, 1 = b)."""
    ca, cb = _channels(a), _channels(b)
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


def luminance(hex6):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in _channels(hex6))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def readable_on(bg, *candidates):
    """The first candidate with contrast of at least 4.5 on bg, else the stronger of black and white."""
    for c in candidates:
        if contrast(c, bg) >= 4.5:
            return c
    return "111111" if contrast("111111", bg) >= contrast("FFFFFF", bg) else "FFFFFF"


def toned(theme, tone="regular"):
    """Return the theme in a soft, regular or hard tone.

    soft: covers, cards and fills fade toward the page colour; calm, light decks.
    hard: a dark solid cover, stronger cards and fills; bold, high-contrast decks.
    """
    t = dict(theme)
    t["tone"] = tone
    if tone == "soft":
        t["cover_bg"] = mix(t["card"], t["fill"], 0.12)
        t["card"] = mix(t["card"], t["bg"], 0.4)
        t["card2"] = mix(t["card2"], t["bg"], 0.4)
        t["fill"] = mix(t["fill"], t["bg"], 0.3)
        t["highlight"] = mix(t["highlight"], t["bg"], 0.35)
    elif tone == "hard":
        if "hard_cover" in t:
            t["cover_bg"] = t["hard_cover"]
        elif luminance(t["cover_bg"]) > 0.4:
            t["cover_bg"] = t["ink"] if luminance(t["bg"]) > 0.5 else t["accent"]
        else:
            t["cover_bg"] = mix(t["cover_bg"], "000000", 0.25)
        t["card"] = mix(t["card"], t["cover_bg"], 0.1)
        t["highlight"] = mix(t["fill"], t["bg"], 0.45)
        t["rule"] = t["fill"]
    t["cover_ink"] = readable_on(t["cover_bg"], t["cover_ink"], t["ink"], t["bg"], "FFFFFF")
    t["on_fill"] = readable_on(t["fill"], t["on_fill"], t["ink"], "FFFFFF")
    t["accent"] = readable_on(t["card"], t["accent"], t["ink"])
    return t


def _plain(shp):
    """Remove the default shape style, which adds a shadow and theme colours in some viewers."""
    style = shp._element.find(qn("p:style"))
    if style is not None:
        shp._element.remove(style)


def _set_alpha(shp, opacity):
    """Make a solid fill partly transparent (opacity 0 to 1)."""
    clr = shp.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    alpha = etree.SubElement(clr, qn("a:alpha"))
    alpha.set("val", str(int(opacity * 100000)))


class Deck:
    """One presentation in one theme, one format and one alignment."""

    def __init__(self, theme, fmt="video", align=None, tone="regular", logo=None, corner_logo=False, template=None):
        self.t = toned(theme, tone)
        self.fmt = fmt
        self.s = SIZES[fmt]
        self.align = align or theme.get("align", "left")
        self.logo = logo
        self.corner_logo = corner_logo
        self.prs = Presentation(template) if template else Presentation()
        self.prs.slide_width = Inches(SLIDE_W)
        self.prs.slide_height = Inches(SLIDE_H)
        self.page = 0

    @property
    def ha(self):
        """Horizontal alignment for short text (titles, numbers, labels)."""
        return "center" if self.align == "center" else "left"

    # ---------- basics ----------

    def new_slide(self, bg=None):
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = rgb(bg or self.t["bg"])
        self.page += 1
        return slide

    def font_for(self, head):
        return self.t["head"] if head else self.t["body"]

    def text(self, slide, x, y, w, h, content, size=None, bold=False, color=None,
             align="left", anchor="top", head=False, spacing=1.08, after=4, name=None):
        """Add a text box. content is a string or a list of paragraphs.

        A paragraph is a string; **double stars** mark bold runs inside it.
        A paragraph can also be a dict: {"text", "size", "bold", "color", "after"}.
        """
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        if name:
            box.name = name
        tf = box.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        paras = content if isinstance(content, list) else [content]
        for i, para in enumerate(paras):
            spec = para if isinstance(para, dict) else {"text": para}
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
            p.line_spacing = spacing
            p.space_after = Pt(spec.get("after", after))
            psize = spec.get("size", size or self.s["body"])
            pcolor = spec.get("color", color or self.t["ink"])
            pbold = spec.get("bold", bold)
            for k, chunk in enumerate(re.split(r"\*\*", str(spec["text"]))):
                if not chunk:
                    continue
                r = p.add_run()
                r.text = chunk
                f = r.font
                f.name = self.font_for(head)
                f.size = Pt(psize)
                f.bold = pbold or (k % 2 == 1)
                f.color.rgb = rgb(pcolor)
        return box

    def rect(self, slide, x, y, w, h, fill, rounded=True, line=None, name=None, opacity=None):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
        shp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if rounded:
            shp.adjustments[0] = min(0.12, 0.18 / max(min(w, h), 0.1))
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
        if opacity is not None:
            _set_alpha(shp, opacity)
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(0.75)
        else:
            shp.line.fill.background()
        _plain(shp)
        if name:
            shp.name = name
        return shp

    def oval(self, slide, x, y, d, fill):
        shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
        shp.line.fill.background()
        _plain(shp)
        return shp

    def line(self, slide, x1, y1, x2, y2, color=None, width=1.0, dash=False):
        ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = rgb(color or self.t["muted"])
        ln.line.width = Pt(width)
        if dash:
            ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        return ln

    def picture(self, slide, path, x, y, w, h, align="center"):
        """Insert an image that fits inside the box without stretching (letterboxed)."""
        from PIL import Image
        iw, ih = Image.open(path).size
        scale = min(w / iw, h / ih)
        pw, ph = iw * scale, ih * scale
        px = {"center": x + (w - pw) / 2, "left": x, "right": x + w - pw}[align]
        return slide.shapes.add_picture(path, Inches(px), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))

    def photo_fill(self, slide, path, x, y, w, h, focus=(0.5, 0.5)):
        """Insert a photo that fills the box completely, cropping the overflow (no stretching).

        focus is the point of the photo (0 to 1 across, 0 to 1 down) that stays in view.
        """
        from PIL import Image
        iw, ih = Image.open(path).size
        pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
        box_r, img_r = w / h, iw / ih
        if img_r > box_r:
            keep = box_r / img_r
            left = (1 - keep) * focus[0]
            pic.crop_left, pic.crop_right = left, 1 - keep - left
        else:
            keep = img_r / box_r
            top = (1 - keep) * focus[1]
            pic.crop_top, pic.crop_bottom = top, 1 - keep - top
        return pic

    def logo_mark(self, slide, x, y, h, align="left"):
        """The logo (if the deck has one) at height h, keeping its shape."""
        if not self.logo:
            return None
        from PIL import Image
        iw, ih = Image.open(self.logo).size
        w = h * iw / ih
        px = {"left": x, "center": x - w / 2, "right": x - w}[align]
        return slide.shapes.add_picture(self.logo, Inches(px), Inches(y), Inches(w), Inches(h))

    def notes(self, slide, text, speaker=None, seconds=None):
        """Speaker notes. The header line keeps the speaker and timing that audit.py reads."""
        head = ""
        if speaker:
            head = f"{speaker.upper()} (about {seconds} seconds)\n" if seconds else f"{speaker.upper()}\n"
        slide.notes_slide.notes_text_frame.text = head + text.strip()

    def _text_h(self, text, size, width):
        """Rough height in inches that text needs at this size in a box this wide."""
        cpl = max(1, int(width * 72 / (size * 0.5)))
        lines = sum(max(1, math.ceil(len(part) / cpl)) for part in str(text).split("\n"))
        return lines * size * 1.25 / 72

    def _fit(self, text, size, width, max_lines, min_size, char_w=0.5):
        """Largest size from size down to min_size at which text fits in max_lines (rough estimate).

        char_w is the average glyph width in em: about 0.5 for text, 0.62 for bold numbers.
        """
        while size > min_size and len(text) * size * char_w / 72 > width * max_lines:
            size -= 2
        return size

    # ---------- shared furniture ----------

    def title(self, slide, text, sub=None, lines=None):
        """Slide title, plus an optional takeaway line one level smaller. Returns the y where content can start.

        A title that will not fit on one line gets a two-line box, and the content moves down with it.
        """
        size = self.s["title"]
        if lines is None:
            lines = 1 if len(text) * size * 0.5 / 72 <= CW else 2
        h = size / 72 * 1.2 * lines
        self.text(slide, M, TITLE_Y, CW, h, text, size=size, bold=True, head=True, spacing=1.0,
                  align=self.ha, name="title")
        y = TITLE_Y + h + 0.1
        if sub:
            sh = self.s["sub"] / 72 * 1.35
            self.text(slide, M, y, CW, sh, sub, size=self.s["sub"], color=self.t["muted"], align=self.ha,
                      name="subtitle")
            y += sh + 0.1
        return max(y + 0.15, BODY_Y)

    def footer(self, slide, source=None, speaker=None, page=True):
        """Short source line on the left; page number and a removable speaker tag on the right."""
        sx = M
        if self.corner_logo and self.logo:
            self.logo_mark(slide, M, FOOT_Y - 0.08, 0.36)
            sx = M + 0.45
        if source:
            self.text(slide, sx, FOOT_Y, 9.6, 0.3, source, size=self.s["foot"], color=self.t["muted"], name="source")
        if page:
            self.text(slide, SLIDE_W - M - 0.5, FOOT_Y, 0.5, 0.3, str(self.page), size=self.s["foot"],
                      color=self.t["muted"], align="right", name="page_no")
        if speaker:
            self.text(slide, SLIDE_W - M - 2.7, FOOT_Y, 2.1, 0.3, speaker, size=self.s["foot"],
                      color=self.t["muted"], align="right", name="speaker_tag")

    def stat(self, slide, x, y, w, value, label, color=None, size=None, align=None):
        """Big number with a short label under it. Returns the y below it."""
        size = size or self.s["big"]
        align = align or self.ha
        vh = size / 72 * 1.2
        self.text(slide, x, y, w, vh, value, size=size, bold=True, head=True, color=color or self.t["accent"],
                  spacing=1.0, align=align)
        lh = self.s["label"] / 72 * 1.25 * 2 + 0.06
        self.text(slide, x, y + vh + 0.04, w, lh, label, size=self.s["label"], color=self.t["muted"], align=align)
        return y + vh + lh + 0.12

    def panel_head(self, slide, x, y, w, text, number=None):
        """Small numbered heading with a rule under it, used above a panel."""
        label = f"{number}  {text}" if number else text
        hh = self.s["h"] / 72 * 1.3
        self.text(slide, x, y, w, hh, label, size=self.s["h"], bold=True, head=True, align=self.ha)
        self.line(slide, x, y + hh + 0.06, x + w, y + hh + 0.06, color=self.t["rule"], width=1.5)
        return y + hh + 0.2

    def steps(self, slide, y, items, x=M, w=CW):
        """Numbered process strip: a line with circles, a name and a short note under each."""
        n = len(items)
        gap = w / n
        d = 0.46
        self.line(slide, x + gap / 2, y + d / 2, x + w - gap / 2, y + d / 2, color=self.t["muted"], width=1.0)
        for i, (name, note) in enumerate(items):
            cx = x + gap * i + gap / 2
            self.oval(slide, cx - d / 2, y, d, self.t["fill"])
            self.text(slide, cx - d / 2, y, d, d, str(i + 1), size=self.s["label"] + 1, bold=True,
                      color=self.t["on_fill"], align="center", anchor="middle")
            self.text(slide, cx - gap / 2 + 0.05, y + 0.6, gap - 0.1, 0.34, name, size=self.s["h"] - 2,
                      bold=True, align="center", head=True)
            if note:
                self.text(slide, cx - gap / 2 + 0.05, y + 0.98, gap - 0.1, 0.62, note, size=self.s["small"],
                          color=self.t["muted"], align="center")
        return y + 1.65

    def flow(self, slide, y, boxes, x=M, w=CW, h=1.35, fills=None):
        """Left-to-right flow diagram: rounded boxes (heading, short text) joined by arrows.

        Good for a pipeline, a cause-and-effect chain, or problem, diagnosis, solution.
        """
        n = len(boxes)
        arrow = 0.45
        bw = (w - arrow * (n - 1)) / n
        for i, (head, text) in enumerate(boxes):
            bx = x + i * (bw + arrow)
            fill = (fills or {}).get(i, self.t["card"])
            self.rect(slide, bx, y, bw, h, fill)
            ink = readable_on(fill, self.t["ink"], "FFFFFF")
            self.text(slide, bx + 0.2, y + 0.18, bw - 0.4, 0.36, head, size=self.s["h"], bold=True, color=ink,
                      head=True, align=self.ha)
            if text:
                self.text(slide, bx + 0.2, y + 0.6, bw - 0.4, h - 0.7, text, size=self.s["body"], color=ink, align=self.ha)
            if i < n - 1:
                ax = bx + bw + 0.08
                shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(ax), Inches(y + h / 2 - 0.14),
                                             Inches(arrow - 0.16), Inches(0.28))
                shp.fill.solid()
                shp.fill.fore_color.rgb = rgb(self.t["rule"])
                shp.line.fill.background()
                _plain(shp)
        return y + h

    # ---------- native charts ----------

    def _style_chart(self, chart, legend, number_format):
        chart.has_title = False
        title_off = chart._chartSpace.chart.find(qn("c:autoTitleDeleted"))
        if title_off is not None:
            title_off.set("val", "1")
        chart.font.size = Pt(self.s["label"])
        chart.font.name = self.t["body"]
        chart.font.color.rgb = rgb(self.t["muted"])
        chart.has_legend = bool(legend)
        if legend:
            chart.legend.position = XL_LEGEND_POSITION.TOP
            chart.legend.include_in_layout = False
            chart.legend.font.size = Pt(self.s["label"])
            chart.legend.font.color.rgb = rgb(self.t["ink"])
        va = chart.value_axis
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = rgb(mix(self.t["muted"], self.t["bg"], 0.8))
        va.major_gridlines.format.line.width = Pt(0.75)
        va.format.line.fill.background()
        va.tick_labels.font.size = Pt(self.s["label"])
        va.tick_labels.font.color.rgb = rgb(self.t["muted"])
        if number_format:
            va.tick_labels.number_format = number_format
            va.tick_labels.number_format_is_linked = False
        ca = chart.category_axis
        ca.format.line.color.rgb = rgb(self.t["muted"])
        ca.tick_labels.font.size = Pt(self.s["label"])
        ca.tick_labels.font.color.rgb = rgb(self.t["muted"])
        ca.has_major_gridlines = False

    def _skip_labels(self, chart, every):
        # The schema fixes the order: ... lblOffset, tickLblSkip, tickMarkSkip, noMultiLvlLbl.
        # PowerPoint refuses a chart whose elements are out of order, so insert, never append.
        cat = chart._chartSpace.find(".//" + qn("c:catAx"))
        if cat is None or every <= 1:
            return
        anchor = cat.find(qn("c:noMultiLvlLbl"))
        for tag in ("c:tickLblSkip", "c:tickMarkSkip"):
            el = etree.Element(qn(tag))
            el.set("val", str(every))
            if anchor is not None:
                anchor.addprevious(el)
            else:
                cat.append(el)

    def line_chart(self, slide, x, y, w, h, categories, series, colors=None, dashed=(), legend=True,
                   number_format=None, label_every=1, widths=None):
        """Native line chart. series is {name: values}; None leaves a gap."""
        data = CategoryChartData()
        data.categories = categories
        for name, vals in series.items():
            data.add_series(name, vals)
        gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(x), Inches(y), Inches(w), Inches(h), data)
        chart = gf.chart
        self._style_chart(chart, legend and len(series) > 1, number_format)
        colors = colors or self.t["series"]
        for i, s in enumerate(chart.series):
            s.smooth = False
            s.marker.style = XL_MARKER_STYLE.NONE
            s.format.line.color.rgb = rgb(colors[i % len(colors)])
            s.format.line.width = Pt((widths or {}).get(s.name, 2.5))
            if s.name in dashed:
                s.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        self._skip_labels(chart, label_every)
        return chart

    def bar_chart(self, slide, x, y, w, h, categories, series, colors=None, horizontal=False, legend=True,
                  number_format='0.0', labels=True, point_colors=None, gap=60):
        """Native clustered bar or column chart with value labels."""
        data = CategoryChartData()
        data.categories = categories
        for name, vals in series.items():
            data.add_series(name, vals)
        kind = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
        gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), data)
        chart = gf.chart
        self._style_chart(chart, legend and len(series) > 1, None)
        plot = chart.plots[0]
        plot.gap_width = gap
        plot.overlap = -10 if len(series) > 1 else 0
        colors = colors or self.t["series"]
        for i, s in enumerate(chart.series):
            s.invert_if_negative = False   # otherwise some viewers draw negative bars in white or flipped
            s.format.fill.solid()
            s.format.fill.fore_color.rgb = rgb(colors[i % len(colors)])
        if point_colors:
            for idx, col in point_colors.items():
                pt = chart.series[0].points[idx]
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb = rgb(col)
            # a coloured data point needs its own invertIfNegative, placed right after its idx
            for dpt in chart.series[0]._element.findall(qn("c:dPt")):
                if dpt.find(qn("c:invertIfNegative")) is None:
                    el = etree.Element(qn("c:invertIfNegative"))
                    el.set("val", "0")
                    dpt.find(qn("c:idx")).addnext(el)
        if labels:
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.font.size = Pt(self.s["label"])
            dl.font.color.rgb = rgb(self.t["ink"])
            dl.number_format = number_format
            dl.number_format_is_linked = False
            dl.position = XL_LABEL_POSITION.OUTSIDE_END
        if any(v is not None and v < 0 for vals in series.values() for v in vals):
            chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        if horizontal:
            chart.category_axis.reverse_order = True
        return chart

    # ---------- native table ----------

    def table(self, slide, x, y, w, rows, col_widths=None, row_h=None, highlight=(), bold_rows=(), size=None):
        """Native table: dark header row, light rows, numbers right-aligned.

        rows[0] is the header. highlight is a set of (row, col) cells to tint.
        """
        size = size or self.s["body"]
        row_h = row_h or max(0.4, size / 72 * 2.0)
        nr, nc = len(rows), len(rows[0])
        shape = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
        tbl = shape.table
        tbl_pr = tbl._tbl.tblPr
        style = tbl_pr.find(qn("a:tableStyleId"))
        if style is None:
            style = etree.SubElement(tbl_pr, qn("a:tableStyleId"))
        style.text = NO_STYLE_TABLE
        widths = col_widths or [w / nc] * nc
        for j, cw in enumerate(widths):
            tbl.columns[j].width = Inches(cw)
        numeric = re.compile(r"^[\s+\-−–]?[\d.,]+\s?(%|m|bn|k|pp)?$")
        for i, row in enumerate(rows):
            tbl.rows[i].height = Inches(row_h)
            for j, val in enumerate(row):
                cell = tbl.cell(i, j)
                cell.margin_left = cell.margin_right = Inches(0.1)
                cell.margin_top = cell.margin_bottom = Inches(0.03)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.fill.solid()
                if i == 0:
                    cell.fill.fore_color.rgb = rgb(self.t["ink"])
                elif (i, j) in highlight:
                    cell.fill.fore_color.rgb = rgb(self.t["highlight"])
                else:
                    cell.fill.fore_color.rgb = rgb(self.t["bg"] if i % 2 else self.t["card2"])
                tf = cell.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = ""
                r = p.add_run()
                r.text = str(val)
                r.font.size = Pt(size)
                r.font.name = self.t["body"]
                r.font.bold = i == 0 or i in bold_rows
                r.font.color.rgb = rgb(self.t["bg"] if i == 0 else self.t["ink"])
                if i > 0 and j > 0 and numeric.match(str(val)):
                    p.alignment = PP_ALIGN.RIGHT
        return tbl

    # ---------- slide patterns ----------

    def cover(self, title, course=None, group=None, members=(), image=None, image_focus=(0.5, 0.5),
              notes=None, speaker=None, seconds=None):
        """Title slide: logo and course line, group, title, a rule, members with IDs.

        With image: left alignment puts the photo on the right 42% of the slide;
        center alignment uses it full-bleed under a tinted veil. No slogan, no chart.
        """
        s = self.new_slide(bg=self.t["cover_bg"])
        ink = self.t["cover_ink"]
        x, w = M, CW
        if image and self.align == "center":
            self.photo_fill(s, image, 0, 0, SLIDE_W, SLIDE_H, image_focus)
            self.rect(s, 0, 0, SLIDE_W, SLIDE_H, self.t["cover_bg"], rounded=False, opacity=0.82)
        elif image:
            self.photo_fill(s, image, SLIDE_W * 0.58, 0, SLIDE_W * 0.42, SLIDE_H, image_focus)
            w = SLIDE_W * 0.58 - M - 0.4
        al = self.ha
        cx = x + w / 2
        top = 0.6
        if self.logo:
            if al == "center":
                self.logo_mark(s, cx, top, 1.05, align="center")
                top += 1.2
            else:
                self.logo_mark(s, x, top, 1.05)
        tx = x + (1.05 if self.logo and al == "left" else 0)
        tw = w - (tx - x)
        if course:
            lines = course if isinstance(course, list) else [course]
            self.text(s, tx, top + 0.02, tw, 0.4, lines[0], size=self.s["sub"], bold=True, color=ink, head=True, align=al)
            if len(lines) > 1:
                self.text(s, tx, top + 0.45, tw, 0.4, lines[1], size=self.s["label"] + 2, color=ink, align=al)
        ty = 2.2 if al == "left" else top + 1.1
        if group:
            self.text(s, x, ty, w, 0.4, group, size=self.s["sub"], bold=True, color=ink, head=True, align=al)
            ty += 0.5
        size = self._fit(title, self.s["cover"], w, 2, self.s["title"] + 6)
        lines = min(3, max(1, math.ceil(len(title) * size * 0.5 / 72 / w)))
        th = size / 72 * 1.25 * max(lines, 2)
        self.text(s, x, ty, w, th, title, size=size, bold=True, color=ink, head=True, spacing=1.0, align=al)
        ry = max(ty + th + 0.3, 5.0)
        if al == "center":
            self.line(s, cx - 1.2, ry, cx + 1.2, ry, color=ink, width=1.25)
        else:
            self.line(s, x, ry, x + w, ry, color=ink, width=1.25)
        if members:
            colw = w / max(len(members), 1)
            for i, m in enumerate(members):
                name, sid = (m, None) if isinstance(m, str) else m
                paras = [{"text": name, "bold": True, "size": self.s["sub"]}]
                if sid:
                    paras.append({"text": sid, "size": self.s["label"] + 2})
                self.text(s, x + i * colw, ry + 0.3, colw - 0.1, 0.9, paras, color=ink, head=True,
                          align="center" if al == "center" else "left")
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def section(self, title, items=(), image=None, image_focus=(0.5, 0.5), notes=None, speaker=None, seconds=None):
        """Divider in the cover colour, with up to four short rows of what comes next (optional photo strip)."""
        s = self.new_slide(bg=self.t["cover_bg"])
        ink = self.t["cover_ink"]
        w = CW
        if image:
            self.photo_fill(s, image, SLIDE_W * 0.66, 0, SLIDE_W * 0.34, SLIDE_H, image_focus)
            w = SLIDE_W * 0.66 - M - 0.4
        self.text(s, M, 0.9, w, 1.0, title, size=self.s["title"] + 8, bold=True, color=ink, head=True, align=self.ha)
        row_fill = self.t["card"] if self.t["cover_bg"] == self.t["bg"] else self.t["bg"]
        for i, (label, desc) in enumerate(items):
            y = 2.4 + i * 0.98
            self.rect(s, M, y, w, 0.8, row_fill)
            self.text(s, M + 0.3, y, 2.6, 0.8, label, size=self.s["h"], bold=True, color=self.t["accent"],
                      anchor="middle", head=True)
            self.text(s, M + 3.0, y, w - 3.3, 0.8, desc, size=self.s["body"], anchor="middle")
        if notes:
            self.notes(s, notes, speaker, seconds)
        self.footer(s, speaker=speaker)
        return s

    def questions(self, title, questions, steps=None, steps_title=None, source=None, notes=None, speaker=None, seconds=None):
        """Research questions as cards, with the approach as a numbered strip under them."""
        s = self.new_slide()
        y = self.title(s, title)
        n = len(questions)
        gap = 0.2
        cw = (CW - gap * (n - 1)) / n
        ch = 2.15 if steps else 3.4
        for i, (label, q) in enumerate(questions):
            x = M + i * (cw + gap)
            self.rect(s, x, y, cw, ch, self.t["card"])
            self.text(s, x + 0.22, y + 0.2, cw - 0.44, 0.36, label, size=self.s["h"] - 2, bold=True,
                      color=self.t["accent"], head=True, align=self.ha)
            self.text(s, x + 0.22, y + 0.62, cw - 0.44, ch - 0.75, q, size=self.s["body"] + 1, align=self.ha)
        if steps:
            sy = y + ch + 0.35
            if steps_title:
                self.text(s, M, sy, CW, 0.32, steps_title, size=self.s["h"] - 2, bold=True, head=True, align=self.ha)
                sy += 0.48
            self.steps(s, sy, steps)
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def findings(self, title, tiles, source=None, notes=None, speaker=None, seconds=None):
        """Two to four answer tiles: heading, one big number, one or two sentences.

        Two or four tiles sit in a 2-column grid with the number beside the sentence; three sit in one row,
        and center alignment always stacks the number above the sentence. Long numbers shrink to one line.
        """
        s = self.new_slide()
        y = self.title(s, title)
        n = len(tiles)
        cols = 3 if n == 3 else min(n, 2)
        rows = math.ceil(n / cols)
        stacked = self.align == "center" or cols == 3
        gap = 0.2
        tw = (CW - gap * (cols - 1)) / cols
        bw = tw - 0.56 if stacked else min(2.6, tw * 0.42)
        big = min(self._fit(v, self.s["big"], bw, 1, self.s["big"] - 16, char_w=0.62) for _, v, _ in tiles)
        bh = big / 72 * 1.2
        tx_w = tw - 0.56 if stacked else tw - bw - 0.71
        body = max(self._text_h(t, self.s["body"], tx_w) for _, _, t in tiles)
        need = 0.72 + (bh + 0.1 + body if stacked else max(bh, body)) + 0.3
        th = min((BODY_BOTTOM - y - gap * (rows - 1)) / rows, max(need, 1.7))
        y += max(0, (BODY_BOTTOM - y - (th * rows + gap * (rows - 1))) / 3)
        al = "center" if self.align == "center" else "left"
        for i, (head, value, text) in enumerate(tiles):
            x = M + (i % cols) * (tw + gap)
            ty = y + (i // cols) * (th + gap)
            self.rect(s, x, ty, tw, th, self.t["card"])
            self.text(s, x + 0.28, ty + 0.22, tw - 0.56, 0.36, head, size=self.s["h"], bold=True,
                      color=self.t["accent"], head=True, align=al)
            if stacked:
                self.text(s, x + 0.28, ty + 0.66, tw - 0.56, bh, value, size=big, bold=True, head=True, align=al)
                self.text(s, x + 0.28, ty + 0.76 + bh, tw - 0.56, th - bh - 0.9, text, size=self.s["body"], align=al)
            else:
                self.text(s, x + 0.28, ty + 0.66, bw, bh, value, size=big, bold=True, head=True)
                self.text(s, x + 0.28 + bw + 0.15, ty + 0.72, tx_w, th - 0.9, text, size=self.s["body"])
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def chart_stats(self, title, draw, stats=(), sub=None, aside=None, source=None, notes=None, speaker=None,
                    seconds=None, chart_w=7.7):
        """The workhorse: a chart on the left, two or three stat tiles (or short text) on the right.

        draw(deck, slide, x, y, w, h) adds the chart or picture.
        """
        s = self.new_slide()
        y = self.title(s, title, sub)
        h = BODY_BOTTOM - y
        draw(self, s, M - 0.1, y, chart_w, h)
        rx = M + chart_w + 0.25
        rw = SLIDE_W - M - rx
        ry = y + 0.1
        if aside:
            self.text(s, rx, ry, rw, 1.8, aside, size=self.s["body"])
            ry += 1.9
        for value, label in stats:
            ry = self.stat(s, rx, ry, rw, value, label, align="left") + 0.05
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def photo(self, title, image, text=None, stats=(), side="left", image_focus=(0.5, 0.5), caption=None,
              source=None, notes=None, speaker=None, seconds=None):
        """A photo that fills one half of the slide edge to edge; title, short text and numbers on the other half.

        Use it for the place, product, people or data source the talk is about, never for decoration.
        """
        s = self.new_slide()
        half = SLIDE_W * 0.47
        px = 0 if side == "left" else SLIDE_W - half
        self.photo_fill(s, image, px, 0, half, SLIDE_H, image_focus)
        if caption:
            self.rect(s, px, SLIDE_H - 0.5, half, 0.5, "000000", rounded=False, opacity=0.45)
            self.text(s, px + 0.25, SLIDE_H - 0.42, half - 0.5, 0.3, caption, size=self.s["foot"], color="FFFFFF")
        tx = half + 0.5 if side == "left" else M
        tw = SLIDE_W - half - 0.5 - M
        size = self.s["title"]
        est = len(title) * size * 0.5 / 72
        lines = 1 if est <= tw else (2 if est <= 2 * tw else 3)
        th = size / 72 * 1.2 * lines
        self.text(s, tx, TITLE_Y + 0.3, tw, th, title, size=size, bold=True, head=True, spacing=1.0,
                  align=self.ha, name="title")
        y = TITLE_Y + 0.3 + th + 0.35
        if text:
            self.text(s, tx, y, tw, 2.2, text, size=self.s["body"] + 2, align=self.ha, after=8)
            y += 2.3
        if stats:
            sw = (tw - 0.2 * (len(stats) - 1)) / len(stats)
            for k, (v, l) in enumerate(stats):
                self.stat(s, tx + k * (sw + 0.2), y, sw, v, l)
        if source:
            self.text(s, tx, FOOT_Y, tw - 0.6, 0.3, source, size=self.s["foot"], color=self.t["muted"], name="source")
        self.text(s, SLIDE_W - M - 0.5, FOOT_Y, 0.5, 0.3, str(self.page), size=self.s["foot"],
                  color=self.t["muted"] if side == "left" else "FFFFFF", align="right", name="page_no")
        if speaker:
            self.text(s, tx + tw - 2.8, FOOT_Y, 2.1, 0.3, speaker, size=self.s["foot"], color=self.t["muted"],
                      align="right", name="speaker_tag")
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def full_photo(self, title, image, sub=None, image_focus=(0.5, 0.5), credit=None, notes=None, speaker=None,
                   seconds=None):
        """A full-bleed photo with the title on a tinted band: an opener, a section break or a closing image."""
        s = self.new_slide()
        self.photo_fill(s, image, 0, 0, SLIDE_W, SLIDE_H, image_focus)
        band_h = 2.2 if sub else 1.7
        by = SLIDE_H - band_h - 0.5
        self.rect(s, 0, by, SLIDE_W, band_h, self.t["cover_bg"], rounded=False, opacity=0.88)
        ink = self.t["cover_ink"]
        self.text(s, M, by + 0.35, CW, 0.9, title, size=self.s["title"] + 6, bold=True, color=ink, head=True,
                  align=self.ha)
        if sub:
            self.text(s, M, by + 1.3, CW, 0.5, sub, size=self.s["sub"], color=ink, align=self.ha)
        if credit:
            self.text(s, M, FOOT_Y, CW, 0.3, credit, size=self.s["foot"], color="FFFFFF", name="source")
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def panels(self, title, panels, sub=None, source=None, notes=None, speaker=None, seconds=None):
        """Two or three columns. Each panel: {"head", "draw" or "image", "stats": [(v, l)], "text"}."""
        s = self.new_slide()
        y = self.title(s, title, sub)
        n = len(panels)
        gap = 0.25
        pw = (CW - gap * (n - 1)) / n
        for i, p in enumerate(panels):
            x = M + i * (pw + gap)
            py = self.panel_head(s, x, y, pw, p["head"], i + 1 if n > 1 else None)
            fig_h = 2.3 if (p.get("stats") or p.get("text")) else BODY_BOTTOM - py
            if "draw" in p:
                p["draw"](self, s, x, py, pw, fig_h)
            elif "image" in p:
                self.picture(s, p["image"], x, py, pw, fig_h)
            sy = py + fig_h + 0.1
            stats = p.get("stats", [])
            if stats:
                sw = (pw - 0.15 * (len(stats) - 1)) / len(stats)
                bottoms = [self.stat(s, x + k * (sw + 0.15), sy, sw, v, l, size=self.s["big"] - 10)
                           for k, (v, l) in enumerate(stats)]
                sy = max(bottoms)
            if p.get("text"):
                self.text(s, x, sy, pw, BODY_BOTTOM - sy, p["text"], size=self.s["body"], align=self.ha)
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def table_slide(self, title, rows, col_widths=None, highlight=(), sub=None, below=None, stats=(),
                    source=None, notes=None, speaker=None, seconds=None, table_w=None):
        """A native table with an optional short reading under it and stat tiles on the right."""
        s = self.new_slide()
        y = self.title(s, title, sub)
        tw = table_w or (CW if not stats else 7.6)
        tbl = self.table(s, M, y, tw, rows, col_widths, highlight=highlight)
        ty = y + sum(r.height for r in tbl.rows) / 914400 + 0.25
        if below:
            self.text(s, M, ty, tw, BODY_BOTTOM - ty, below, size=self.s["body"])
        if stats:
            rx = M + tw + 0.35
            ry = y
            for v, l in stats:
                ry = self.stat(s, rx, ry, SLIDE_W - M - rx, v, l, align="left") + 0.05
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def cards(self, title, cards, cols=None, sub=None, source=None, notes=None, speaker=None, seconds=None):
        """A grid of cards: (heading, value or None, text)."""
        s = self.new_slide()
        y = self.title(s, title, sub)
        cols = cols or min(len(cards), 3)
        rows = math.ceil(len(cards) / cols)
        gap = 0.2
        cw = (CW - gap * (cols - 1)) / cols
        vs = self.s["big"] - 6
        need = max(0.66 + (vs / 72 * 1.2 + 0.08 if v else 0) + self._text_h(t, self.s["body"], cw - 0.5) + 0.3
                   for _, v, t in cards)
        ch = min((BODY_BOTTOM - y - gap * (rows - 1)) / rows, max(need, 1.6))
        y += max(0, (BODY_BOTTOM - y - (ch * rows + gap * (rows - 1))) / 3)
        for i, (head, value, text) in enumerate(cards):
            x = M + (i % cols) * (cw + gap)
            cy = y + (i // cols) * (ch + gap)
            self.rect(s, x, cy, cw, ch, self.t["card"])
            self.text(s, x + 0.25, cy + 0.2, cw - 0.5, 0.36, head, size=self.s["h"], bold=True, head=True, align=self.ha)
            ty = cy + 0.66
            if value:
                vh = vs / 72 * 1.2
                self.text(s, x + 0.25, ty, cw - 0.5, vh, value, size=vs, bold=True, color=self.t["accent"],
                          head=True, align=self.ha)
                ty += vh + 0.08
            self.text(s, x + 0.25, ty, cw - 0.5, cy + ch - ty - 0.1, text, size=self.s["body"], align=self.ha)
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def two_lists(self, title, left, right, source=None, notes=None, speaker=None, seconds=None):
        """Two cards with numbered points, e.g. recommendations and limitations. left/right: (heading, [points])."""
        s = self.new_slide()
        y = self.title(s, title)
        gap = 0.25
        cw = (CW - gap) / 2
        need = max(0.9 + sum(self._text_h(f"0.  {p}", self.s["body"], cw - 0.6) + 0.14 for p in pts) + 0.3
                   for _, pts in (left, right))
        ch = min(BODY_BOTTOM - y, max(need, 2.5))
        for i, (head, points) in enumerate((left, right)):
            x = M + i * (cw + gap)
            self.rect(s, x, y, cw, ch, self.t["card"] if i == 0 else self.t["card2"])
            self.text(s, x + 0.3, y + 0.25, cw - 0.6, 0.4, head, size=self.s["h"] + 2, bold=True, head=True)
            paras = [f"**{k + 1}.**  {p}" for k, p in enumerate(points)]
            self.text(s, x + 0.3, y + 0.9, cw - 0.6, ch - 1.05, paras, size=self.s["body"], after=10)
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def conclusion(self, title, rows, hero=None, source=None, notes=None, speaker=None, seconds=None):
        """Label and one-sentence rows on the left, one hero card on the right. hero: (heading, big, text)."""
        s = self.new_slide()
        y = self.title(s, title)
        lw = 8.3 if hero else CW
        rh = (BODY_BOTTOM - y - 0.12 * (len(rows) - 1)) / len(rows)
        for i, (label, text) in enumerate(rows):
            ry = y + i * (rh + 0.12)
            self.rect(s, M, ry, lw, rh, self.t["card"])
            self.text(s, M + 0.25, ry, 2.0, rh, label, size=self.s["h"] - 2, bold=True, color=self.t["accent"],
                      anchor="middle", head=True)
            self.text(s, M + 2.4, ry, lw - 2.6, rh, text, size=self.s["body"], anchor="middle")
        if hero:
            hx = M + lw + 0.25
            hw = SLIDE_W - M - hx
            self.rect(s, hx, y, hw, BODY_BOTTOM - y, self.t["fill"])
            head, big, text = hero
            ink = self.t["on_fill"]
            al = "center" if self.align == "center" else "left"
            hs = self._fit(big, self.s["hero"], hw - 0.6, 1, self.s["big"])
            self.text(s, hx + 0.3, y + 0.3, hw - 0.6, 0.4, head, size=self.s["h"], bold=True, color=ink, head=True, align=al)
            self.text(s, hx + 0.3, y + 0.85, hw - 0.6, hs / 72 * 1.25, big, size=hs, bold=True, color=ink, head=True, align=al)
            self.text(s, hx + 0.3, y + 1.0 + hs / 72 * 1.25, hw - 0.6, 2.5, text, size=self.s["body"], color=ink, align=al)
        self.footer(s, source, speaker)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def thanks(self, line="Thank you", subtitle=None, members_line=None, course=None, image=None,
               image_focus=(0.5, 0.5), notes=None, speaker=None, seconds=None):
        """Closing slide in the cover colour, with the logo; an optional photo as on the cover."""
        s = self.new_slide(bg=self.t["cover_bg"])
        ink = self.t["cover_ink"]
        x, w = M, CW
        if image and self.align == "center":
            self.photo_fill(s, image, 0, 0, SLIDE_W, SLIDE_H, image_focus)
            self.rect(s, 0, 0, SLIDE_W, SLIDE_H, self.t["cover_bg"], rounded=False, opacity=0.82)
        elif image:
            self.photo_fill(s, image, SLIDE_W * 0.58, 0, SLIDE_W * 0.42, SLIDE_H, image_focus)
            w = SLIDE_W * 0.58 - M - 0.4
        al = self.ha
        big = self.s["cover"] + 22
        self.text(s, x, 2.0, w, big / 72 * 1.25, line, size=big, bold=True, color=ink, head=True, align=al)
        y = 2.0 + big / 72 * 1.25 + 0.3
        if subtitle:
            self.text(s, x, y, w, 0.45, subtitle, size=self.s["sub"], color=ink, align=al)
            y += 0.55
        if members_line:
            self.text(s, x, y, w, 0.4, members_line, size=self.s["body"] + 2, bold=True, color=ink, align=al)
        if self.logo or course:
            if al == "center":
                ly = 5.25
                self.logo_mark(s, x + w / 2, ly, 0.9, align="center")
                if course:
                    self.text(s, x, ly + 1.0, w, 0.4, course, size=self.s["body"], color=ink, align="center")
            else:
                cx = x
                if self.logo:
                    self.logo_mark(s, x, 5.45, 0.9)
                    cx = x + 0.9
                if course:
                    self.text(s, cx, 5.6, w - (cx - x), 0.6, course, size=self.s["body"], color=ink)
        if notes:
            self.notes(s, notes, speaker, seconds)
        return s

    def save(self, path):
        self.prs.save(path)
        return path


def clean_copy(src, dst):
    """Copy of a deck without speaker tags, for submission or recording."""
    prs = Presentation(src)
    for slide in prs.slides:
        for shp in list(slide.shapes):
            if shp.name == "speaker_tag":
                shp._element.getparent().remove(shp._element)
    prs.save(dst)
    return dst

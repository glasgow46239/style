"""Build the Britain Elects wordmark and badge lockups as outlined SVGs (text converted to paths).

Usage: python3 make_logos.py <fonts_dir> <out_dir>
fonts_dir holds static Archivo instances: cond800.ttf (wdth 62, wght 800), reg300.ttf (wdth 100, wght 300),
reg800.ttf (wdth 100, wght 800), wide800.ttf (wdth 125, wght 800).
Kerned glyph positions come from Chromium (Playwright); outlines come from fontTools.
"""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from playwright.sync_api import sync_playwright

FONTS_DIR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
FONT_FILES = {k: os.path.join(FONTS_DIR, k + '.ttf') for k in ('cond800', 'reg300', 'reg800', 'wide800')}
FONTS = {k: TTFont(v) for k, v in FONT_FILES.items()}
CAP = FONTS['cond800']['OS/2'].sCapHeight / FONTS['cond800']['head'].unitsPerEm  # 0.686

# Brand colours (tokens.json "logo")
LOGO_LIGHT = ['#05718F', '#D34C4C', '#777777', '#EBB82F']  # top, left, right, bottom
INK_LIGHT, INK_DARK = '#181818', '#F2F2F2'
CROSS = [  # chevrons in a 607-unit square starting at (196, 196)
    '253,196 366,196 500,330 633,196 746,196 500,443',
    '196,253 441,500 196,746 196,633 329,500 196,366',
    '803,253 557,500 803,746 803,633 670,500 803,366',
    '253,803 366,803 500,670 633,803 746,803 500,557',
]

# ---- kerned positions from Chromium -------------------------------------------------------
RUNS = {
    'main': ('cond800', 'BRITAIN ELECTS', 0.01),
    'with': ('reg300', 'WITH', 0.02),
    'ben': ('wide800', 'BEN', 0.0),
    'walker': ('wide800', 'WALKER', 0.0),
    'britain': ('reg800', 'BRITAIN', -0.01),
    'elects': ('reg800', 'ELECTS', -0.01),
}

def measure():
    faces = ''.join("@font-face{font-family:'%s';src:url('file://%s')}" % (k, os.path.abspath(v)) for k, v in FONT_FILES.items())
    divs = ''.join('<div id="%s" style="font-family:\'%s\';letter-spacing:%sem;font-size:1000px;white-space:pre;line-height:1">%s</div>' % (k, f, ls, t) for k, (f, t, ls) in RUNS.items())
    html = '<html><head><style>%s body{margin:0}</style></head><body>%s</body></html>' % (faces, divs)
    path = os.path.join(OUT, '_measure.html')
    open(path, 'w').write(html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto('file://' + os.path.abspath(path))
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(300)
        res = pg.evaluate("""() => { const out = {};
          for (const el of document.querySelectorAll('div')) { const node = el.firstChild, r = document.createRange(), x0 = el.getBoundingClientRect().left, xs = [];
            for (let i = 0; i < node.length; i++) { r.setStart(node, i); r.setEnd(node, i + 1); xs.push(r.getBoundingClientRect().left - x0); }
            out[el.id] = xs; } return out; }""")
        b.close()
    os.remove(path)
    return res

POS = measure()

def run_paths(key, size, x, baseline, fill):
    """Outline a run at font size `size`, its INK left edge at x, baseline at y. Returns (svg, ink_width)."""
    font_key, text, _ = RUNS[key]
    f = FONTS[font_key]
    upm = f['head'].unitsPerEm
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    s = size / upm
    # ink extent at unit scale
    xmin, xmax = None, None
    for ch, px in zip(text, POS[key]):
        if ch == ' ':
            continue
        bp = BoundsPen(gs)
        gs[cmap[ord(ch)]].draw(bp)
        if bp.bounds:
            a, b = px + bp.bounds[0], px + bp.bounds[2]
            xmin = a if xmin is None else min(xmin, a)
            xmax = b if xmax is None else max(xmax, b)
    out = []
    for ch, px in zip(text, POS[key]):
        if ch == ' ':
            continue
        pen = SVGPathPen(gs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
        tp = TransformPen(pen, (s, 0, 0, -s, x + (px - xmin) * s, baseline))
        gs[cmap[ord(ch)]].draw(tp)
        d = pen.getCommands()
        if d:
            out.append(d)
    return '<path fill="%s" d="%s"/>' % (fill, ''.join(out)), (xmax - xmin) * s

def cross(x, y, size, colours):
    k = size / 607.0
    polys = []
    for pts, c in zip(CROSS, colours):
        q = []
        for pair in pts.split():
            px, py = map(float, pair.split(','))
            q.append('%.2f,%.2f' % (x + (px - 196) * k, y + (py - 196) * k))
        polys.append('<polygon fill="%s" points="%s"/>' % (c, ' '.join(q)))
    return ''.join(polys)

def mark(x, y, size, style):
    """style: ('plain', colour) | ('boxed', box_colour, [4 cross colours]). Boxed cross is 70% (wordmark) of the square."""
    if style[0] == 'plain':
        return cross(x, y, size, [style[1]] * 4)
    box, cols, ratio = style[1], style[2], style[3]
    inner = size * ratio
    o = (size - inner) / 2
    return '<rect fill="%s" x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>' % (box, x, y, size, size) + cross(x + o, y + o, inner, cols)

def subline(x, baseline, size, width, fill):
    """'WITH BEN WALKER', words spread so the line spans exactly `width` (ink to ink)."""
    parts, widths = [], []
    for key in ('with', 'ben', 'walker'):
        svg, w = run_paths(key, size, 0, 0, fill)
        widths.append(w)
    gap = (width - sum(widths)) / 2.0
    cx, out = x, []
    for key, w in zip(('with', 'ben', 'walker'), widths):
        svg, _ = run_paths(key, size, cx, baseline, fill)
        out.append(svg)
        cx += w + gap
    return ''.join(out), gap

def doc(w, h, body, title, display_h):
    pad = 0
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f" role="img" aria-label="%s"><title>%s</title>%s</svg>\n'
            % (w, h, display_h * w / h, display_h, title, title, body))

# ---- A: condensed wordmark ----------------------------------------------------------------
F = 1000.0                       # main line font size (units)
CAPH = CAP * F                   # 686
GAP_P = 14 / 72.0 * F            # mark to name, one line
GAP_E = 16 / 72.0 * F            # mark to name, with Ben Walker
SUB_F = 35 / 72.0 * F            # sub-line font size
MARK_E = 87 / 72.0 * F           # mark height on the two-line lockup

def wordmark(style, ink, ben):
    if not ben:
        m = CAPH
        txt, w = run_paths('main', F, m + GAP_P, CAPH, ink)
        return doc(m + GAP_P + w, m, mark(0, 0, m, style) + txt, 'Britain Elects', 48)
    m = MARK_E
    txt, w = run_paths('main', F, m + GAP_E, CAPH, ink)
    sub, _ = subline(m + GAP_E, m, SUB_F, w, ink)
    return doc(m + GAP_E + w, m, mark(0, 0, m, style) + txt + sub, 'Britain Elects with Ben Walker', 72)

# ---- C: badge (stacked) -------------------------------------------------------------------
CF = 1000.0
CCAP = CAP * CF
C_LINEGAP = 11 / 46.0 * CF
C_SQ = CCAP * 2 + C_LINEGAP
C_GAP = 14 / 46.0 * CF
C_SUBF = 19 / 46.0 * CF
C_SUBGAP = 12 / 46.0 * CF

def badge(style, ink, ben):
    t1, w1 = run_paths('britain', CF, C_SQ + C_GAP, CCAP, ink)
    t2, w2 = run_paths('elects', CF, C_SQ + C_GAP, C_SQ, ink)
    W = C_SQ + C_GAP + max(w1, w2)
    body = mark(0, 0, C_SQ, style) + t1 + t2
    if not ben:
        return doc(W, C_SQ, body, 'Britain Elects', 64)
    # size the sub-line so the three words fill the width with ~0.45em between each
    natural = sum(run_paths(k, 1000.0, 0, 0, ink)[1] for k in ('with', 'ben', 'walker')) / 1000.0
    subf = W / (natural + 0.9)
    sub_cap = CAP * subf
    sub, _ = subline(0, C_SQ + C_SUBGAP + sub_cap, subf, W, ink)
    return doc(W, C_SQ + C_SUBGAP + sub_cap, body + sub, 'Britain Elects with Ben Walker', 84)

def icon(style, name):
    return doc(C_SQ, C_SQ, mark(0, 0, C_SQ, style), name, 64)

BOX_LIGHT = ('boxed', INK_LIGHT, ['#FFFFFF'] * 4, 0.70)       # white cross in a black square: light backgrounds
BOX_DARK = ('boxed', '#FFFFFF', LOGO_LIGHT, 0.70)            # colour cross in a white square: dark backgrounds
BADGE_LIGHT = ('boxed', INK_LIGHT, ['#FFFFFF'] * 4, 0.66)
BADGE_DARK = ('boxed', '#FFFFFF', LOGO_LIGHT, 0.66)

FILES = {
    'wordmark.svg': wordmark(BOX_LIGHT, INK_LIGHT, False),
    'wordmark-ben-walker.svg': wordmark(BOX_LIGHT, INK_LIGHT, True),
    'wordmark-dark.svg': wordmark(BOX_DARK, INK_DARK, False),
    'wordmark-dark-ben-walker.svg': wordmark(BOX_DARK, INK_DARK, True),
    'wordmark-mono-black.svg': wordmark(('plain', INK_LIGHT), INK_LIGHT, False),
    'wordmark-mono-black-ben-walker.svg': wordmark(('plain', INK_LIGHT), INK_LIGHT, True),
    'wordmark-mono-white.svg': wordmark(('plain', INK_DARK), INK_DARK, False),
    'wordmark-mono-white-ben-walker.svg': wordmark(('plain', INK_DARK), INK_DARK, True),
    'badge.svg': badge(BADGE_LIGHT, INK_LIGHT, False),
    'badge-ben-walker.svg': badge(BADGE_LIGHT, INK_LIGHT, True),
    'badge-dark.svg': badge(BADGE_DARK, INK_DARK, False),
    'badge-dark-ben-walker.svg': badge(BADGE_DARK, INK_DARK, True),
    'icon.svg': icon(BADGE_LIGHT, 'Britain Elects'),
    'icon-colour.svg': icon(BADGE_DARK, 'Britain Elects'),
}
for name, svg in FILES.items():
    open(os.path.join(OUT, name), 'w').write(svg)
    print(name, len(svg))

#!/usr/bin/env python3
"""
Builds MapLibre glyph files (signed distance fields in protobuf) from a TTF,
so map labels can use the house typeface.

    python tools/make_glyphs.py path/to/IBMPlexSans-Regular.ttf "IBM Plex Sans Regular"

Writes fonts/<fontstack>/<start>-<end>.pbf for the ranges UK maps need:
Basic Latin + Latin-1, Latin Extended-A (Welsh ŵ ŷ, Irish/Polish names) and
General Punctuation (’ – — …). Matches MapLibre's layout: 24px glyphs,
3px buffer, 8px SDF radius, 0.25 cutoff.
"""
import sys
from pathlib import Path

import numpy as np
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import distance_transform_edt

SIZE, BUFFER, RADIUS, CUTOFF, SS = 24, 3, 8, 0.25, 8   # SS = supersampling for the distance field
RANGES = [(0, 255), (256, 511), (8192, 8447)]


def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def zigzag(n):
    return (n << 1) ^ (n >> 31)


def field(num, wire, payload):
    key = varint((num << 3) | wire)
    if wire == 0:
        return key + varint(payload)
    return key + varint(len(payload)) + payload  # wire 2


def glyph_message(cp, bitmap, w, h, left, top, adv):
    m = field(1, 0, cp)
    if bitmap is not None:
        m += field(2, 2, bitmap)
    m += field(3, 0, w) + field(4, 0, h) + field(5, 0, zigzag(left)) + field(6, 0, zigzag(top)) + field(7, 0, adv)
    return m


def build(ttf, stack, outdir):
    tt = TTFont(ttf)
    upm = tt["head"].unitsPerEm
    cmap = tt.getBestCmap()
    gs = tt.getGlyphSet()
    hmtx = tt["hmtx"]
    ascender = round(tt["hhea"].ascent * SIZE / upm)
    big = ImageFont.truetype(str(ttf), SIZE * SS)
    scale = SIZE / upm
    dest = outdir / stack
    dest.mkdir(parents=True, exist_ok=True)

    for start, end in RANGES:
        glyphs = b""
        for cp in range(start, end + 1):
            name = cmap.get(cp)
            if name is None:
                continue
            adv = round(hmtx[name][0] * scale)
            g = tt["glyf"][name] if "glyf" in tt else None
            if g is None or g.numberOfContours == 0 or not hasattr(g, "xMin"):
                glyphs += field(3, 2, glyph_message(cp, None, 0, 0, 0, 0, adv))   # space-like
                continue
            x0, y0 = int(np.floor(g.xMin * scale)), int(np.floor(g.yMin * scale))
            x1, y1 = int(np.ceil(g.xMax * scale)), int(np.ceil(g.yMax * scale))
            w, h = x1 - x0, y1 - y0
            W, H = w + 2 * BUFFER, h + 2 * BUFFER
            img = Image.new("L", (W * SS, H * SS), 0)
            ImageDraw.Draw(img).text(((BUFFER - x0) * SS, (BUFFER + y1) * SS), chr(cp), font=big, fill=255, anchor="ls")
            inside = np.asarray(img) > 127
            d = (distance_transform_edt(~inside) - distance_transform_edt(inside)) / SS
            centres = d[SS // 2::SS, SS // 2::SS][:H, :W]
            val = np.clip(np.round(255 - 255 * (centres / RADIUS + CUTOFF)), 0, 255).astype(np.uint8)
            glyphs += field(3, 2, glyph_message(cp, val.tobytes(), w, h, x0, y1 - ascender, adv))
        stack_msg = field(1, 2, stack.encode()) + field(2, 2, f"{start}-{end}".encode()) + glyphs
        (dest / f"{start}-{end}.pbf").write_bytes(field(1, 2, stack_msg))
        print(f"{stack} {start}-{end}")


if __name__ == "__main__":
    build(Path(sys.argv[1]), sys.argv[2], Path(__file__).resolve().parent.parent / "fonts")

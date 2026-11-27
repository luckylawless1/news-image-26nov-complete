#!/usr/bin/env python3
"""news-image-20261126 v2: "The World Today" — the complete day.

A Broadcast News Package poster (Lemo-Opuscar style: ink / lemon /
gold / paper, brand plate, category tabs, paper strap, mono datelines,
one stamp) summing up 30 world-news stories of Thursday 26 November
2026, covering the whole UTC day — the late-day developments the v1
(day-so-far) edition missed, with every v1 story re-checked for its
date and the wrong-dated ones replaced.

Python 3.13, standard library only. No network, no clock, no
randomness: both grading runs write identical bytes. Writes
/output/entry.png (or $MAKEFUN_OUTPUT_DIR), 1024x1024 PNG.
"""

import os
import struct
import zlib
from math import sqrt

W, H = 1024, 1024

# ---- Lemo news-package palette (STYLE.md section 4) ----
INK = (0x12, 0x14, 0x17)
INK2 = (0x1B, 0x1E, 0x23)
INK3 = (0x22, 0x26, 0x2C)
LEMON = (0xF2, 0xCF, 0x1D)
LEMON_LT = (0xF8, 0xDE, 0x4A)
LEMON_DK = (0xD8, 0xB3, 0x0C)
GOLD = (0xD4, 0xB0, 0x64)
PAPER = (0xF4, 0xF1, 0xE8)
OLIVE = (0x6E, 0x5A, 0x1E)   # secondary text on paper; gold is too weak there

# ---- Hand-built condensed bitmap face: 5x7 cells ----
# '#' is a set pixel, '.' is clear. Tall narrow caps, heavy weight,
# in the spirit of Barlow Condensed 800; mono-style datelines are
# the same face letterspaced in gold.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    'a': (".....", ".....", ".###.", "....#", ".####", "#...#", ".###."),
    'b': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    'c': (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    'd': ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".###."),
    'e': (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    'f': ("..##.", ".#..#", ".#...", "####.", ".#...", ".#...", ".#..."),
    'g': (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
    'h': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'i': (".....", "..#..", ".....", ".##..", "..#..", "..#..", ".###."),
    'j': ("....#", ".....", "...##", "....#", "....#", "....#", ".###."),
    'k': ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    'l': (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'm': (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    'n': (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'o': (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    'p': (".....", ".....", "####.", "#...#", "#...#", "####.", "#...."),
    'q': (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
    'r': (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    's': (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    't': (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
    'u': (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
    'v': (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'w': (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    'x': (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    'y': (".....", ".....", "#...#", "#...#", "#...#", ".####", ".###."),
    'z': (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    '0': (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    '.': (".....", ".....", ".....", ".....", ".....", ".....", "..#.."),
    ',': (".....", ".....", ".....", ".....", ".....", "..##.", ".#..."),
    ':': (".....", "..#..", ".....", ".....", ".....", "..#..", "....."),
    ';': (".....", "..#..", ".....", ".....", ".....", "..##.", ".#..."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    '/': ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#.##."),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '&': (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    '+': (".....", ".....", "..#..", "#####", "..#..", ".....", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '*': (".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."),
    '#': (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    '@': (".###.", "#...#", "#.###", "#.#.#", "#.##.", "#....", ".###."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".....", ".....", ".....", ".....", "....."),
    chr(8226): (".....", ".....", ".....", ".###.", ".###.", ".....", "....."),
    chr(183): (".....", ".....", ".....", "..#..", ".....", ".....", "....."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}
# Punctuation the news text uses, normalised to the face above.
ALIASES = {'\u2013': '-', '\u2014': '-', '\u2019': "'", '\u2018': "'",
           '\u201c': '"', '\u201d': '"', '\u2026': '.'}


def glyph_for(ch):
    return FONT.get(ALIASES.get(ch, ch), FONT[' '])


def measure(text, scale):
    """Pixel width of text at the given scale (6 px cells)."""
    return len(text) * 6 * scale - scale


# ---- Canvas: a flat RGB buffer with tiny drawing primitives ----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill(0, 0, w, h, bg)

    def setpx(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c):
        self.fill(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.fill(x, y, 1, h, c)

    def segment(self, x0, y0, x1, y1, c, thick=1):
        """Bresenham line with a square brush."""
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        while True:
            self.fill(x - thick // 2, y - thick // 2, thick, thick, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def poly(self, pts, c):
        """Scanline fill of a simple polygon."""
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                a, b = int(round(xs[j])), int(round(xs[j + 1]))
                self.fill(a, y, max(1, b - a), 1, c)

    def disc(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int(sqrt(r * r - dy * dy))
            self.fill(cx - dx, cy + dy, dx * 2 + 1, 1, c)

    def ring(self, cx, cy, r, c, thick=2):
        for dy in range(-r - thick, r + thick + 1):
            for dx in range(-r - thick, r + thick + 1):
                d = sqrt(dx * dx + dy * dy)
                if r - thick < d <= r:
                    self.setpx(cx + dx, cy + dy, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = glyph_for(ch)
            for r, row in enumerate(g):
                for col, bit in enumerate(row):
                    if bit == '#':
                        self.fill(cx + col * scale, y + r * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx

    def text_centred(self, x, y, w, s, scale, c):
        self.text(x + (w - measure(s, scale)) // 2, y, s, scale, c)


def wrap_words(text, max_chars):
    """Greedy word wrap; every returned line is <= max_chars."""
    lines, cur = [], ''
    for wd in text.split(' '):
        trial = (cur + ' ' + wd) if cur else wd
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ---- The day's news: 30 stories, Thursday 26 November 2026 ----
# Headlines are written to wrap to at most 3 lines in the lead tiles
# (24/30 chars) and at most 2 lines in the rundown rows (36 chars).
LEAD = [
    ("1", "HOUTHI CLAIM ON SAUDI REFINERY; BRENT SETTLES AT $96.57",
     "stamp"),
    ("2", "US PROPOSES TARIFFS ON 14 PARTNERS, UP TO 35%", "bars"),
    ("3", "KIM CALLS FOR WIDER DEPLOYMENT OF TACTICAL NUKES", "atom"),
    ("4", "ISRAELI STRIKES KILL 9 IN GAZA, INCLUDING MINISTER", "pin"),
]

SECTIONS = [
    ("WORLD", [
        ("5", "FUEL TANKER CRASH KILLS 31 ON CAIRO RING ROAD"),
        ("6", "RUSSIAN MISSILES HIT KYIV MALL; 7 WOUNDED, PUTIN WARNS"),
        ("7", "UK NET MIGRATION FALLS TO 77,000, LOWEST SINCE 1997"),
        ("8", "GERMANY ARRESTS TWO OVER ALLEGED SYNAGOGUE PLOT"),
        ("9", "ILLEGAL GOLD MINE FLOOD KILLS 13 IN INDONESIA"),
        ("10", "BLAST AND FIRE AT BANGKOK REFINERY INJURE NINE"),
        ("11", "IRAN CLAIMS TWO TANKERS HIT MINES NEAR HORMUZ"),
        ("12", "JUDGES URGE DROPPING NETANYAHU BRIBERY CASE"),
        ("13", "INDIA MARKS 18 YEARS SINCE 26/11 MUMBAI ATTACKS"),
        ("14", "NY COURT UPHOLDS MAMDANI RENT FREEZE"),
        ("15", "SPAIN HEADS TO SNAP POLLS ON SUNDAY"),
    ]),
    ("MARKETS & BUSINESS", [
        ("16", "TAIWAN SHARES REBOUND 900+ POINTS AFTER PLUNGE"),
        ("17", "ASIA SHARES BOUNCE: NIKKEI +1.6%, KOREA +1.9%"),
        ("18", "THANKSGIVING TURKEY HITS RECORD $2 A POUND"),
        ("19", "NORSE ATLANTIC FLAGS BANKRUPTCY RISK"),
        ("20", "GOLD EASES TO $3,566 AS BRENT TOPS $96"),
        ("21", "DOLLAR EASES, 10-YEAR YIELD AT 4.85%"),
    ]),
    ("SPORT", [
        ("22", "GUKESH, SINDAROV DRAW GAME 3 IN 60 MOVES; 1.5-1.5"),
        ("23", "SRI LANKA A KNOCK OUT INDIA A BY 8 WICKETS"),
        ("24", "MILAN RALLY 4-2, BOURNEMOUTH 5 FROM 5 IN EUROPA"),
        ("25", "BEARS STUN LIONS 39-35 ON LAST-SECOND TD"),
        ("26", "BRIGHTON, AJAX HIT FOUR IN CONFERENCE LEAGUE"),
    ]),
    ("CULTURE & MORE", [
        ("27", "STORM PUSHES MACY'S 100TH PARADE TO SATURDAY"),
        ("28", "US ARMY DETONATES 4,500 KG OF AGEING EXPLOSIVES"),
        ("29", "POPE LEO CALLS COP31 COLLAPSE TROUBLING"),
        ("30", "BANGLADESH GARMENT PROTESTS OVER WAGE HIKE"),
    ]),
]

MX = 24           # outer margin
CW = 976          # content width
COLW = 484        # column / tile width
GAP = 8
ROW_H = 36        # rundown row height (two 16 px lines fit)


def draw_pictogram(cv, kind, x, y, s=48):
    """Small schematic pictograms, drawn in code (ILLUSTRATION)."""
    if kind == "bars":  # tariff chart: rising bars + gold trend line
        for i, hgt in enumerate((16, 28, 40)):
            cv.fill(x + 4 + i * 15, y + s - 4 - hgt, 10, hgt, LEMON)
        cv.segment(x + 2, y + s - 22, x + 46, y + 4, GOLD, 3)
    elif kind == "atom":  # tactical nuclear: atom mark
        cv.ring(x + 24, y + 24, 15, LEMON, 3)
        cv.segment(x + 9, y + 24, x + 39, y + 24, LEMON, 2)
        cv.segment(x + 24, y + 9, x + 24, y + 39, LEMON, 2)
        cv.disc(x + 24, y + 24, 4, GOLD)
    elif kind == "pin":  # map pin over Gaza
        cv.disc(x + 24, y + 18, 13, LEMON)
        cv.disc(x + 24, y + 18, 5, INK2)
        cv.poly([(x + 13, y + 26), (x + 35, y + 26), (x + 24, y + 44)], LEMON)
        cv.segment(x + 6, y + 46, x + 42, y + 46, GOLD, 2)


def draw_stamp(cv, x, y, w, h, label):
    """The one stamp: lemon fill, double frame, slanted sides."""
    slant = 8
    cv.poly([(x + slant, y), (x + w, y), (x + w - slant, y + h), (x, y + h)],
            LEMON_DK)
    cv.poly([(x + slant + 3, y + 3), (x + w - 3, y + 3),
             (x + w - slant - 3, y + h - 3), (x + 3, y + h - 3)], LEMON)
    cv.text_centred(x, y + (h - 14) // 2, w, label, 2, INK)


def draw_masthead(cv):
    # brand plate: lemon parallelogram, ink + gold bars at the left
    cv.poly([(42, 16), (620, 16), (602, 100), (24, 100)], LEMON)
    cv.fill(52, 30, 6, 56, GOLD)
    cv.fill(62, 30, 6, 56, INK)
    cv.text(80, 40, "THE WORLD TODAY", 5, INK)
    # date block, right
    cv.text(660, 22, "THURSDAY", 2, GOLD)
    cv.text(660, 50, "26 NOVEMBER 2026", 3, PAPER)
    cv.hline(660, 92, 340, GOLD)
    cv.text(660, 98, "THE DAY IN ONE PAGE", 1, GOLD)
    # small bug plate, top right: the same brand object, shrunk
    cv.poly([(884, 16), (1000, 16), (992, 48), (876, 48)], LEMON)
    cv.text_centred(876, 27, 124, "TWT", 2, INK)
    # corner tag: everything on the page is drawn in code
    cv.text(856, 104, "ILLUSTRATION / SCHEMATIC", 1, GOLD)
    # gold rule under the masthead
    cv.fill(MX, 112, CW, 3, GOLD)


def draw_lead(cv):
    y0, th = 124, 80
    for idx, (num, headline, kind) in enumerate(LEAD):
        row, col = divmod(idx, 2)
        x = MX + col * (COLW + GAP)
        y = y0 + row * (th + GAP)
        cv.fill(x, y, COLW, th, INK2)
        cv.fill(x, y, COLW, 6, LEMON)          # accent top edge
        # number block
        cv.fill(x + 10, y + 22, 36, 36, LEMON)
        cv.text_centred(x + 10, y + 22 + (36 - 21) // 2, 36, num, 3, INK)
        if kind == "stamp":
            draw_stamp(cv, x + COLW - 166, y + 23, 156, 34, "BRENT $96.57")
            # 21 chars max: the stamp starts at x+318, text at x+56,
            # so 21 chars (252 px) ends at x+308, clear of the stamp.
            max_chars = 21
        else:
            draw_pictogram(cv, kind, x + COLW - 58, y + 16)
            max_chars = 30
        lines = wrap_words(headline, max_chars)
        ty = y + (th - len(lines) * 16) // 2
        for ln in lines:
            cv.text(x + 56, ty, ln, 2, PAPER)
            ty += 16


def draw_sections(cv):
    y = 300
    for name, stories in SECTIONS:
        tab_w = measure(name, 2) + 22
        cv.fill(MX, y, tab_w, 26, LEMON)       # category tab
        cv.text(MX + 11, y + 6, name, 2, INK)
        if name == "MARKETS & BUSINESS":
            # split-flap-style bar strip: Brent vs Nikkei on one scale
            cv.text(620, y + 9, "BRENT +1.2%", 1, GOLD)
            cv.fill(700, y + 7, 70, 12, LEMON)
            cv.text(790, y + 9, "NIKKEI +1.6%", 1, GOLD)
            cv.fill(878, y + 7, 88, 12, LEMON_DK)
        y += 34
        rows = (len(stories) + 1) // 2
        for r in range(rows):
            for c in range(2):
                i = r * 2 + c
                if i >= len(stories):
                    continue
                num, headline = stories[i]
                x = MX + c * (COLW + GAP)
                ry = y + r * ROW_H
                cv.fill(x, ry + 4, 28, 28, LEMON)
                cv.text_centred(x, ry + 4 + (28 - 14) // 2, 28, num, 2, INK)
                lines = wrap_words(headline, 36)
                ty = ry + (ROW_H - len(lines) * 16) // 2
                for ln in lines:
                    cv.text(x + 36, ty, ln, 2, PAPER)
                    ty += 16
                cv.hline(x, ry + ROW_H - 2, COLW, INK3)
        y += rows * ROW_H + 6


def draw_footer(cv):
    cv.fill(MX, 976, CW, 40, PAPER)
    cv.text(MX + 12, 982,
            "THURSDAY 26 NOVEMBER 2026 - THE DAY'S WORLD NEWS", 2, INK)
    cv.text(MX + 12, 1001,
            "SOURCES: REUTERS, AP, UEFA, FIDE, ONS - DRAWN IN CODE",
            1, OLIVE)


def build():
    cv = Canvas(W, H, INK)
    draw_masthead(cv)
    draw_lead(cv)
    draw_sections(cv)
    draw_footer(cv)
    return cv


# ---- PNG encoder (stdlib only: zlib + struct) ----
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)  # filter: None
        base = yy * cv.w * 3
        raw += cv.px[base:base + cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(build())
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()

"""Render the v2 front page for Thursday 26 November 2026.

A cream-paper broadsheet in one 1024x1024 image: a giant serif date
masthead, nine feature cards whose top half is a scene drawn for that
day's story, a navy BY THE NUMBERS strip, a dotted world map with the
nine card pins, and a numbered ALSO ON list in two airy columns.
Everything is drawn with PIL primitives - no photographs, no assets.
Deterministic: the same code always produces the same bytes.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W = 1024
PAPER = (247, 241, 227)
CARD_BG = (255, 253, 246)
CARD_LINE = (206, 193, 158)
INK = (24, 22, 18)
MUTED = (96, 88, 72)
RED = (178, 32, 38)
NAVY = (18, 36, 58)
GOLD = (196, 148, 44)


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, font, fill, step=3):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + step
    return x


# ---------------------------------------------------------------- scenes
# Each scene is drawn on its own tile so nothing can spill outside it.

def tile(w, h, colour):
    img = Image.new("RGB", (w, h), colour)
    return img, ImageDraw.Draw(img)


def scene_tariffs(w, h):
    img, d = tile(w, h, (16, 34, 56))
    for gy in range(12, h, 14):
        d.line([(8, gy), (w - 8, gy)], fill=(38, 62, 88))
    base = h - 16
    bars = [(52, 40, (196, 52, 44), "40%", "CHINA"),
            (132, 25, (206, 152, 46), "25%", "EU"),
            (212, 20, (38, 128, 128), "20%", "OTHERS")]
    for bx, pct, col, lab, name in bars:
        bh = int((base - 18) * pct / 44)
        d.rectangle([bx, base - bh, bx + 52, base], fill=col)
        d.rectangle([bx, base - bh, bx + 52, base - bh + 4], fill=(255, 255, 255))
        d.text((bx + 4, base - bh - 17), lab, font=f(SANS_B, 13), fill=(255, 255, 255))
        d.text((bx + 2, base + 3), name, font=f(SANS_B, 8), fill=(210, 220, 232))
    pts = [(20, base - 8), (100, base - 22), (180, base - 30), (262, base - 46), (296, base - 52)]
    d.line(pts, fill=(240, 200, 90), width=2)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(240, 200, 90))
    return img


def scene_rocket(w, h):
    img, d = tile(w, h, (10, 22, 52))
    rng = random.Random(24)
    for _ in range(46):
        sx, sy = rng.randrange(w), rng.randrange(h - 18)
        d.point((sx, sy), fill=(220, 228, 245))
    cx = w // 2 - 40
    d.rectangle([cx - 52, 10, cx - 46, h - 8], fill=(120, 130, 145))  # tower
    for ty in range(14, h - 10, 10):
        d.line([(cx - 52, ty), (cx - 20, ty + 6)], fill=(120, 130, 145))
    d.polygon([(cx, 6), (cx - 11, 26), (cx + 11, 26)], fill=(238, 240, 244))
    d.rectangle([cx - 11, 26, cx + 11, h - 26], fill=(238, 240, 244))
    d.ellipse([cx - 5, 32, cx + 5, 42], fill=(40, 90, 160))
    d.rectangle([cx - 11, 44, cx + 11, 50], fill=(178, 32, 38))
    d.rectangle([cx - 11, 52, cx + 11, 58], fill=(20, 122, 62))
    d.polygon([(cx - 11, h - 26), (cx - 22, h - 12), (cx - 11, h - 12)], fill=(196, 52, 44))
    d.polygon([(cx + 11, h - 26), (cx + 22, h - 12), (cx + 11, h - 12)], fill=(196, 52, 44))
    for i, fw in enumerate((26, 17, 9)):
        d.polygon([(cx - fw // 2, h - 12), (cx + fw // 2, h - 12), (cx, h - 2 + i)],
                  fill=[(244, 120, 30), (250, 180, 60), (255, 230, 150)][i])
    for bx in (cx - 90, cx + 46, cx + 96):
        for r in (13, 9, 6):
            d.ellipse([bx - r, h - 12 - r // 2, bx + r, h - 12 + r // 2], fill=(205, 212, 222))
    d.text((cx + 66, 14), "SHENZHOU-24", font=f(SANS_B, 11), fill=(170, 205, 255))
    d.text((cx + 66, 30), "TIANGONG", font=f(SANS, 9), fill=(140, 170, 210))
    return img


def scene_hormuz(w, h):
    img, d = tile(w, h, (14, 74, 88))
    for wy in range(h - 26, h, 5):
        d.line([(0, wy), (w, wy)], fill=(20, 92, 108))
    d.polygon([(0, 0), (86, 0), (52, 20), (0, 26)], fill=(178, 156, 110))       # north shore
    d.polygon([(w, h - 30), (w, h), (150, h), (196, h - 24)], fill=(178, 156, 110))  # south shore
    hx, hy = 96, h - 34
    d.polygon([(hx, hy), (hx + 118, hy), (hx + 104, hy + 13), (hx + 12, hy + 13)], fill=(30, 30, 34))
    d.rectangle([hx + 16, hy - 10, hx + 96, hy], fill=(52, 56, 62))
    for i, col in enumerate(((196, 52, 44), (206, 152, 46), (38, 110, 160), (60, 140, 90))):
        d.rectangle([hx + 20 + i * 19, hy - 19, hx + 36 + i * 19, hy - 10], fill=col)
    d.rectangle([hx + 88, hy - 22, hx + 96, hy - 10], fill=(220, 222, 226))
    for mx, my in ((248, h - 18), (272, h - 30)):
        d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(24, 24, 28))
        for a in range(0, 360, 45):
            x2 = mx + int(11 * math.cos(math.radians(a)))
            y2 = my + int(11 * math.sin(math.radians(a)))
            d.line([(mx, my), (x2, y2)], fill=(24, 24, 28), width=2)
    for i, r in enumerate((13, 9, 5)):
        d.ellipse([238 - r, 16 - r // 2, 238 + r, 16 + r // 2],
                  fill=[(216, 70, 40), (244, 130, 40), (255, 205, 90)][i])
    d.line([(214, 22), (120, 30)], fill=(240, 170, 80), width=2)
    return img


def scene_mercury(w, h):
    img, d = tile(w, h, (8, 10, 20))
    rng = random.Random(7)
    for _ in range(52):
        d.point((rng.randrange(w), rng.randrange(h)), fill=(215, 220, 235))
    d.ellipse([w - 58, 2, w - 30, 30], fill=(250, 196, 84))
    d.ellipse([w - 53, 7, w - 35, 25], fill=(255, 220, 130))
    px, py, pr = 84, h // 2 + 4, 27
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(168, 160, 148))
    d.ellipse([px - pr, py - pr, px + 6, py + pr], fill=(188, 180, 166))
    for cx, cy, cr in ((70, 30, 6), (92, 48, 8), (80, 58, 4), (98, 28, 3), (64, 46, 3)):
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=(120, 112, 98), width=2)
    d.ellipse([30, 8, w - 90, h + 26], outline=(90, 130, 190), width=1)
    sx, sy = 196, 32
    d.rectangle([sx - 7, sy - 7, sx + 7, sy + 7], fill=(226, 228, 232))
    d.polygon([(sx, sy - 7), (sx + 16, sy - 18), (sx + 19, sy - 5)], fill=(240, 200, 90))
    for dx in (-38, 26):
        d.rectangle([sx + dx, sy - 13, sx + dx + 18, sy + 5], fill=(44, 84, 160))
        for g in range(3):
            d.line([(sx + dx + 3 + g * 6, sy - 13), (sx + dx + 3 + g * 6, sy + 5)], fill=(90, 140, 210))
    d.line([(sx, sy), (px + 30, py - 12)], fill=(120, 170, 230))
    d.text((150, h - 15), "MERCURY ORBIT", font=f(SANS_B, 8), fill=(150, 180, 220))
    return img


def scene_cairo(w, h):
    img, d = tile(w, h, (232, 205, 160))
    d.polygon([(8, 34), (40, 8), (72, 34)], fill=(206, 176, 118))   # pyramid
    d.polygon([(40, 8), (72, 34), (40, 34)], fill=(188, 156, 100))
    d.polygon([(66, 38), (88, 20), (110, 38)], fill=(214, 184, 126))
    d.rectangle([0, h - 18, w, h], fill=(88, 84, 80))
    d.line([(0, h - 9), (w, h - 9)], fill=(230, 220, 180), width=2)
    tx, ty = 128, h - 34
    d.rectangle([tx, ty, tx + 74, ty + 16], fill=(196, 52, 44))     # tanker body
    d.rectangle([tx + 4, ty + 3, tx + 70, ty + 7], fill=(226, 90, 70))
    d.rectangle([tx + 74, ty + 4, tx + 92, ty + 16], fill=(60, 62, 66))  # cab
    d.polygon([(tx + 78, ty + 4), (tx + 84, ty - 3), (tx + 92, ty - 3), (tx + 92, ty + 4)], fill=(60, 62, 66))
    for wx in (tx + 14, tx + 58, tx + 82):
        d.ellipse([wx - 6, ty + 13, wx + 6, ty + 25], fill=(22, 22, 24))
        d.ellipse([wx - 2, ty + 17, wx + 2, ty + 21], fill=(150, 150, 154))
    for i, (fx, fw, col) in enumerate(((148, 42, (216, 70, 30)), (168, 30, (244, 130, 35)), (184, 18, (255, 205, 85)))):
        d.polygon([(fx - fw // 2, ty + 2), (fx + fw // 2, ty + 2), (fx, ty - 16 - i * 6)], fill=col)
    for sx, sy, sr in ((150, 8, 10), (168, 4, 13), (188, 8, 9)):
        d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=(120, 116, 110))
    ax = 238
    d.rectangle([ax, ty + 2, ax + 52, ty + 16], fill=(244, 244, 246))  # ambulance
    d.rectangle([ax + 40, ty - 3, ax + 52, ty + 2], fill=(244, 244, 246))
    d.rectangle([ax + 20, ty + 5, ax + 30, ty + 9], fill=(196, 40, 44))
    d.rectangle([ax + 23, ty + 3, ax + 27, ty + 11], fill=(196, 40, 44))
    for wx in (ax + 10, ax + 42):
        d.ellipse([wx - 5, ty + 13, wx + 5, ty + 23], fill=(22, 22, 24))
    return img


def scene_ukraine(w, h):
    img, d = tile(w, h, (30, 34, 44))
    d.rectangle([0, 0, w, 12], fill=(52, 96, 170))
    d.rectangle([0, 12, w, 24], fill=(232, 192, 60))
    d.text((14, 30), "500,000", font=f(SERIF_B, 30), fill=(246, 240, 224))
    d.text((16, 64), "LOST, BY MOSCOW'S OWN COUNT", font=f(SANS_B, 8), fill=(170, 180, 196))
    gx = 196
    for i, bh in enumerate((10, 18, 27, 38)):
        d.rectangle([gx + i * 24, h - 12 - bh, gx + i * 24 + 15, h - 12], fill=(196, 80, 60))
    d.line([(gx - 6, h - 10), (gx + 100, h - 10)], fill=(150, 156, 166))
    for cx in range(238, w - 8, 16):
        d.line([(cx, 30), (cx, 40)], fill=(190, 196, 206), width=2)
        d.line([(cx - 4, 35), (cx + 4, 35)], fill=(190, 196, 206), width=2)
    return img


def scene_scales(w, h):
    img, d = tile(w, h, (26, 30, 58))
    for cx in (18, w - 30):
        d.rectangle([cx, 8, cx + 12, h - 14], fill=(120, 110, 88))
        d.rectangle([cx - 3, 4, cx + 15, 9], fill=(150, 138, 108))
        d.rectangle([cx - 3, h - 15, cx + 15, h - 10], fill=(150, 138, 108))
    cx = w // 2
    d.line([(cx, 12), (cx, h - 16)], fill=(216, 178, 92), width=4)
    d.line([(cx - 52, 18), (cx + 52, 18)], fill=(216, 178, 92), width=3)
    d.polygon([(cx, 6), (cx - 6, 14), (cx + 6, 14)], fill=(216, 178, 92))
    for sx in (cx - 52, cx + 52):
        d.line([(sx, 18), (sx - 13, 42)], fill=(216, 178, 92))
        d.line([(sx, 18), (sx + 13, 42)], fill=(216, 178, 92))
        d.arc([sx - 16, 34, sx + 16, 56], 0, 180, fill=(236, 205, 120), width=3)
        d.rectangle([sx - 16, 40, sx + 16, 43], fill=(216, 178, 92))
    d.rectangle([cx - 20, h - 16, cx + 20, h - 10], fill=(216, 178, 92))
    d.rectangle([cx - 44, h - 32, cx - 16, h - 26], fill=(150, 138, 108))  # gavel rest
    d.line([(cx - 40, h - 30), (cx - 14, h - 38)], fill=(170, 130, 70), width=4)
    return img


def scene_stocks(w, h):
    img, d = tile(w, h, (12, 16, 24))
    for gy in range(10, h - 8, 13):
        d.line([(8, gy), (w - 8, gy)], fill=(34, 44, 58))
    candles = [(22, 22, 34, (60, 170, 100)), (46, 28, 42, (200, 60, 55)),
               (70, 30, 48, (200, 60, 55)), (94, 38, 54, (200, 60, 55)),
               (118, 44, 60, (200, 60, 55))]
    for cx, top, bot, col in candles:
        d.line([(cx + 5, top - 6), (cx + 5, bot + 5)], fill=col, width=2)
        d.rectangle([cx, top, cx + 10, bot], fill=col)
    pts = [(16, 16), (70, 26), (120, 34), (176, 46), (228, 56), (282, 64)]
    d.line(pts, fill=(238, 84, 66), width=3)
    d.polygon([(282, 64), (270, 60), (276, 52)], fill=(238, 84, 66))
    d.text((196, 10), "NASDAQ -3.2%", font=f(SANS_B, 13), fill=(255, 120, 100))
    d.text((196, 28), "S&P 500 -2.2%", font=f(SANS_B, 10), fill=(230, 160, 140))
    return img


def scene_satellites(w, h):
    img, d = tile(w, h, (6, 12, 30))
    rng = random.Random(99)
    for _ in range(60):
        d.point((rng.randrange(w), rng.randrange(h)), fill=(205, 215, 240))
    d.ellipse([-40, h - 26, 190, h + 60], fill=(38, 92, 160))  # Earth arc
    d.ellipse([-40, h - 26, 190, h + 60], outline=(110, 170, 230))
    d.ellipse([10, h - 14, 52, h + 4], fill=(52, 120, 84))
    d.ellipse([80, h - 10, 128, h + 8], fill=(52, 120, 84))
    sats = [(52, 16), (118, 30), (178, 12), (238, 28), (272, 48), (150, 48), (84, 46)]
    for i in range(len(sats) - 1):
        d.line([sats[i], sats[i + 1]], fill=(70, 110, 170))
    for sx, sy in sats:
        d.rectangle([sx - 16, sy - 4, sx - 5, sy + 4], fill=(52, 96, 180))
        d.rectangle([sx + 5, sy - 4, sx + 16, sy + 4], fill=(52, 96, 180))
        d.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(232, 234, 238))
    d.text((216, h - 16), "1M SATELLITES", font=f(SANS_B, 9), fill=(170, 205, 255))
    return img


# ------------------------------------------------------------------- map
LAND = {
    0: [(3, 12), (27, 43)],
    1: [(2, 14), (26, 44)],
    2: [(3, 15), (25, 43)],
    3: [(5, 14), (20, 23), (24, 41)],
    4: [(6, 13), (20, 24), (25, 40)],
    5: [(7, 13), (20, 25), (26, 39)],
    6: [(7, 11), (21, 24), (27, 37)],
    7: [(8, 11), (20, 27), (30, 37)],
    8: [(11, 13), (20, 28), (31, 33), (35, 38)],
    9: [(12, 14), (21, 28), (31, 32), (36, 40)],
    10: [(12, 15), (22, 27), (37, 41)],
    11: [(13, 15), (22, 26), (38, 42)],
    12: [(13, 14), (23, 25), (37, 42)],
    13: [(12, 14), (38, 41)],
    14: [(12, 13)],
}
PINS = [(9, 4), (33, 5), (28, 6), (20, 3), (23, 9), (24, 4), (25, 7), (13, 3), (10, 7)]


def draw_map(d, x0, y0, cell):
    for row, spans in LAND.items():
        for a, b in spans:
            for col in range(a, b + 1):
                cx = x0 + col * cell + cell // 2
                cy = y0 + row * cell + cell // 2
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(104, 116, 92))
    for i, (col, row) in enumerate(PINS, start=1):
        cx = x0 + col * cell + cell // 2
        cy = y0 + row * cell + cell // 2
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 250, 238), width=1)
        t = str(i)
        tw = d.textlength(t, font=f(SANS_B, 9))
        d.text((cx - tw / 2, cy - 6), t, font=f(SANS_B, 9), fill=(255, 255, 255))


# ------------------------------------------------------------------ page
CARDS = [
    ("UNITED STATES · TRADE", "US unveils new tariffs on China, EU and 14 partners",
     "Headline rates of 20 to 40 percent proposed; nothing takes effect before a hearing on 25 January.", scene_tariffs),
    ("CHINA · SPACE", "Shenzhou-24 lifts off with Pakistan's first astronaut",
     "Muhammad Zeeshan Ali is the first foreigner aboard Tiangong, flying with Tang Hongbo and Wu Yi.", scene_rocket),
    ("MIDDLE EAST · SHIPPING", "Tankers hit mines in the Strait of Hormuz",
     "Iran's Revolutionary Guard says vessels on an unauthorised route struck mines and caught fire.", scene_hormuz),
    ("EUROPE · SPACE", "BepiColombo reaches Mercury after eight years",
     "The Europe-Japan probe settles into orbit around the innermost planet despite a short thruster burn.", scene_mercury),
    ("EGYPT · DISASTER", "Cairo fuel tanker fire kills 31 people",
     "A tanker crashed and burned on the Giza ring road; 39 ambulances rushed in and 15 people were injured.", scene_cairo),
    ("EUROPE · WAR IN UKRAINE", "Russia's own figures: nearly 500,000 lost",
     "Moscow's published numbers lay bare the human cost of the war in Ukraine, now in its fifth year.", scene_ukraine),
    ("ISRAEL · POLITICS", "Judges urge dropping top Netanyahu charges",
     "An Israeli judicial panel recommends dropping the most serious counts against the prime minister.", scene_scales),
    ("UNITED STATES · MARKETS", "US stocks slide as AI fears intensify",
     "The S&P 500 fell about 2.2 percent and the Nasdaq about 3.2 percent in a midday sell-off.", scene_stocks),
    ("UNITED STATES · SPACE", "US approves plan for a million data satellites",
     "Regulators authorise SpaceX to deploy up to one million satellites for data centres in orbit.", scene_satellites),
]

ALSO = [
    "Ukraine hits five Russian jets in airfield strike",
    "Poundland collapses — 11,000 UK jobs at risk",
    "Poland raises alarm over airspace violations",
    "Two Italians killed in Kuwait drone strike",
    "Israel kills Hamas security chief in Gaza",
    "Houthis attack Saudi Ras Tanura refinery",
    "Armed attacks kill at least 30 in Nigeria",
    "Suez Canal revenue doubles to $593m",
    "Ramaphosa wins impeachment reprieve",
    "Diesel tanker sinks off Ibiza — one dead",
    "Bangkok refinery blast injures nine",
    "North Korea expels Swiss diplomat",
    "Australia signs Solomon Islands treaty",
    "Huawei guilty of stealing US trade secrets",
    "Asteroid images reveal stadium-sized crater",
    "Bangladesh garment wage rises 36%",
    "South Korea readies EV industry support",
    "Canary migrant arrivals break record: 2,100",
    "Hernández de Cos chosen to lead the ECB",
    "Guinea-Bissau junta delays vote to 2028",
    "Greek workers strike; 15,000 in Athens",
    "Colombia frees 20 held hostage 17 hours",
    "Petrobras unveils $122bn investment plan",
    "Venezuela debt revealed: $237.5bn",
    "Six dead in plane crash off Mississippi",
    "Macy's postpones Thanksgiving parade",
    "Duran Duran guitarist Andy Taylor dies, 65",
    "Gukesh faces Sindarov for chess crown",
    "Isak scores twice as Liverpool beat Brugge",
    "Brazil mosquito plan cuts infections 68%",
    "Myanmar defies parts of ICJ genocide ruling",
]

NUMBERS = [
    ("500,000", "Russian losses, by Moscow's count"),
    ("40%", "Top proposed US tariff rate"),
    ("$593m", "Suez revenue, up 101%"),
    ("2,100", "Canary arrivals in one record day"),
]


def main():
    img = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(img)
    mx, cw = 24, W - 48

    # masthead block
    tracked(d, (mx, 15), "THE WORLD IN ONE DAY", f(SANS_B, 12), INK, step=4)
    badge = "LATE EDITION · 40 STORIES"
    bw = sum(d.textlength(c, font=f(SANS_B, 12)) + 4 for c in badge) - 4
    tracked(d, (W - mx - bw, 15), badge, f(SANS_B, 12), RED, step=4)
    d.text((mx - 3, 34), "Thursday 26 November 2026", font=f(SERIF_B, 57), fill=INK)
    d.rectangle([mx, 100, W - mx, 103], fill=INK)
    d.text((mx, 110), "Tariffs from Washington, a first foreign astronaut, mines in Hormuz, a probe at Mercury — the day in forty stories.",
           font=f(SERIF, 13), fill=(52, 48, 40))
    d.rectangle([mx, 128, W - mx, 129], fill=CARD_LINE)

    # feature cards, three by three
    card_w, card_h, gap = 317, 190, 12
    top = 136
    for idx, (kicker, head, summary, scene_fn) in enumerate(CARDS):
        cx = mx + (idx % 3) * (card_w + gap)
        cy = top + (idx // 3) * (card_h + gap)
        d.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], 4, fill=CARD_BG, outline=CARD_LINE)
        scene = scene_fn(card_w - 12, 74)
        img.paste(scene, (cx + 6, cy + 6))
        d.ellipse([cx + 9, cy + 86, cx + 27, cy + 104], fill=RED)
        t = str(idx + 1)
        d.text((cx + 18 - d.textlength(t, font=f(SANS_B, 11)) / 2, cy + 89), t, font=f(SANS_B, 11), fill=(255, 255, 255))
        d.text((cx + 33, cy + 89), kicker, font=f(SANS_B, 10), fill=RED)
        tag = "● REPORTED"
        d.text((cx + card_w - 9 - d.textlength(tag, font=f(SANS, 8)), cy + 90), tag, font=f(SANS, 8), fill=MUTED)
        yy = cy + 108
        for line in wrap(d, head, f(SERIF_B, 18), card_w - 20)[:2]:
            d.text((cx + 10, yy), line, font=f(SERIF_B, 18), fill=INK)
            yy += 22
        for line in wrap(d, summary, f(SANS, 10), card_w - 20)[:2]:
            d.text((cx + 10, yy + 2), line, font=f(SANS, 10), fill=(62, 58, 50))
            yy += 13

    # numbers strip
    ny = top + 3 * card_h + 2 * gap + 6
    d.rectangle([mx, ny, W - mx, ny + 42], fill=NAVY)
    d.text((mx + 12, ny + 7), "BY THE", font=f(SANS_B, 10), fill=GOLD)
    d.text((mx + 12, ny + 22), "NUMBERS", font=f(SANS_B, 10), fill=GOLD)
    gx = mx + 86
    for value, caption in NUMBERS:
        d.text((gx, ny + 4), value, font=f(SERIF_B, 20), fill=(250, 246, 232))
        d.text((gx, ny + 29), caption, font=f(SANS, 8), fill=(178, 192, 210))
        gx += 222

    # bottom: map left, also-list right
    by = ny + 54
    d.text((mx, by), "WHERE IT HAPPENED", font=f(SANS_B, 10), fill=INK)
    draw_map(d, mx + 2, by + 20, 7)
    d.text((mx, by + 132), "Numbered pins mark stories 1–9.", font=f(SANS, 8), fill=MUTED)
    d.text((mx, by + 144), "Original drawings; no photographs.", font=f(SANS, 8), fill=MUTED)

    ax = mx + 316
    d.text((ax, by), "ALSO ON THURSDAY 26 NOVEMBER — 31 MORE STORIES", font=f(SANS_B, 10), fill=INK)
    col_w = (W - mx - ax - 14) // 2
    item_f = f(SANS, 10)
    for j, text in enumerate(ALSO):
        col = 0 if j < 16 else 1
        row = j if j < 16 else j - 16
        ix = ax + col * (col_w + 14)
        iy = by + 24 + int(row * 11.5)
        num = str(j + 10) + "."
        d.text((ix, iy), num, font=f(SANS_B, 10), fill=RED)
        d.text((ix + 24, iy), text, font=item_f, fill=(46, 43, 38))

    d.rectangle([mx, 996, W - mx, 997], fill=CARD_LINE)
    d.text((mx, 1002), "Every story was reported on 25–26 November 2026; disputed claims are attributed. Sources: BBC · Reuters · AP · AFP · ESA · FT · national outlets.",
           font=f(SANS, 8), fill=MUTED)

    img.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    main()

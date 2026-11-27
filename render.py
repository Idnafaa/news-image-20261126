"""Front page for Thursday 26 November 2026 - third edition.

One 1024x1024 sheet of cream paper. A centred date masthead sits over
a wide hero card (the tariff story, scene on the left, words on the
right), then eight smaller illustrated cards in a four-by-two grid, a
navy strip of the day's key figures, a dotted world map with pins for
the nine illustrated stories, and a numbered index of 38 more briefs.
All artwork is drawn on the spot with PIL shapes; there are no photo
assets. The output is deterministic.
"""

import math
import random

from PIL import Image, ImageDraw, ImageFont

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SIZE = 1024
PAPER = (246, 240, 226)
CARD = (255, 253, 245)
EDGE = (203, 190, 154)
INK = (26, 24, 20)
SOFT = (94, 86, 70)
RED = (176, 34, 40)
NAVY = (16, 34, 56)
GOLD = (198, 150, 46)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, width):
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def spaced(draw, x, y, text, fnt, fill, gap=3):
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + gap
    return x


def canvas(w, h, colour):
    im = Image.new("RGB", (w, h), colour)
    return im, ImageDraw.Draw(im)


# ------------------------------------------------------------- scenes
# Every scene is painted inside its own tile, sized by the caller.

def sc_tariffs(w, h):
    im, d = canvas(w, h, (18, 36, 60))
    # rising steps with flags, biggest step carries the top rate
    steps = [(14, 30, (70, 120, 180)), (86, 58, (52, 150, 130)), (158, 92, (196, 60, 48))]
    base = h - 14
    for sx, sh, col in steps:
        d.rectangle([sx, base - sh, sx + 62, base], fill=col)
        d.rectangle([sx, base - sh, sx + 62, base - sh + 5], fill=(255, 255, 255))
    d.text((226, 26), "40%", font=font(SERIF_B, 44), fill=(246, 200, 84))
    d.text((228, 76), "TOP RATE PROPOSED", font=font(SANS_B, 10), fill=(190, 205, 228))
    d.text((228, 92), "EU 20% - INDIA 25%", font=font(SANS, 9), fill=(150, 170, 200))
    pts = [(10, base - 20), (90, base - 44), (168, base - 74), (238, base - 96), (330, base - 104)]
    d.line(pts, fill=(246, 200, 84), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(246, 200, 84))
    return im


def sc_rocket(w, h):
    im, d = canvas(w, h, (12, 24, 54))
    rng = random.Random(2026)
    for _ in range(34):
        d.point((rng.randrange(w), rng.randrange(h)), fill=(205, 218, 245))
    d.ellipse([w - 40, 6, w - 14, 32], fill=(226, 228, 220))  # moon
    d.ellipse([w - 34, 10, w - 24, 20], fill=(200, 202, 196))
    cx = w // 2 + 30
    base = h - 6
    d.polygon([(cx, 4), (cx - 9, 22), (cx + 9, 22)], fill=(240, 242, 246))
    d.rectangle([cx - 9, 22, cx + 9, base - 14], fill=(240, 242, 246))
    d.ellipse([cx - 4, 28, cx + 4, 36], fill=(36, 84, 150))
    d.rectangle([cx - 9, 40, cx + 9, 45], fill=(20, 122, 62))
    d.rectangle([cx - 9, 46, cx + 9, 51], fill=(178, 32, 38))
    d.polygon([(cx - 9, base - 14), (cx - 19, base - 4), (cx - 9, base - 4)], fill=(200, 60, 46))
    d.polygon([(cx + 9, base - 14), (cx + 19, base - 4), (cx + 9, base - 4)], fill=(200, 60, 46))
    for fw, col in ((20, (246, 128, 34)), (12, (252, 186, 66)), (6, (255, 232, 160))):
        d.polygon([(cx - fw // 2, base - 4), (cx + fw // 2, base - 4), (cx, base + 2)], fill=col)
    d.rectangle([cx - 74, base - 4, cx + 74, base], fill=(96, 104, 118))  # pad
    d.text((10, 8), "SHENZHOU-24", font=font(SANS_B, 10), fill=(168, 204, 255))
    d.text((10, 22), "FIRST FOREIGNER", font=font(SANS, 8), fill=(140, 168, 208))
    d.text((10, 32), "ABOARD TIANGONG", font=font(SANS, 8), fill=(140, 168, 208))
    return im


def sc_hormuz(w, h):
    im, d = canvas(w, h, (196, 110, 52))
    d.rectangle([0, 0, w, h // 2], fill=(214, 128, 58))       # sunset sky
    d.ellipse([w - 52, 4, w - 20, 30], fill=(250, 205, 105))  # low sun
    d.rectangle([0, h // 2, w, h], fill=(24, 70, 88))         # sea
    for wy in range(h // 2 + 5, h - 2, 5):
        d.line([(4, wy), (w - 4, wy)], fill=(34, 92, 110))
    hx, hy = 18, h // 2 + 6
    d.polygon([(hx, hy), (hx + 108, hy), (hx + 96, hy + 10), (hx + 10, hy + 10)], fill=(22, 22, 26))
    d.rectangle([hx + 12, hy - 8, hx + 88, hy], fill=(44, 48, 54))
    for i, col in enumerate(((190, 54, 46), (210, 156, 48), (44, 112, 160))):
        d.rectangle([hx + 16 + i * 22, hy - 16, hx + 34 + i * 22, hy - 8], fill=col)
    for mx in (168, 196):
        d.ellipse([mx - 6, hy + 2, mx + 6, hy + 14], outline=(20, 20, 24), width=2)
        d.line([(mx, hy - 2), (mx, hy + 2)], fill=(20, 20, 24), width=2)
    d.text((8, 6), "STRAIT OF HORMUZ", font=font(SANS_B, 8), fill=(255, 226, 170))
    return im


def sc_mercury(w, h):
    im, d = canvas(w, h, (10, 12, 22))
    rng = random.Random(11)
    for _ in range(30):
        d.point((rng.randrange(w), rng.randrange(h)), fill=(210, 216, 235))
    px, py, pr = 34, h // 2, 20
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(172, 164, 150))
    for cx, cy, cr in ((26, py - 6, 5), (42, py + 4, 7), (34, py + 12, 3)):
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=(124, 116, 102), width=2)
    sx, sy = 148, h // 2 - 4
    d.rectangle([sx - 16, sy - 9, sx - 4, sy + 3], fill=(46, 88, 165))   # panel
    d.rectangle([sx + 8, sy - 9, sx + 20, sy + 3], fill=(46, 88, 165))    # panel
    d.rectangle([sx - 4, sy - 6, sx + 8, sy], fill=(228, 230, 234))      # bus
    d.polygon([(sx + 2, sy - 6), (sx + 14, sy - 16), (sx + 16, sy - 4)], fill=(240, 200, 90))  # dish
    d.line([(sx - 22, sy + 12), (px + 22, py - 8)], fill=(110, 160, 220))
    d.text((176, 6), "MERCURY", font=font(SANS_B, 9), fill=(160, 190, 225))
    d.text((176, 18), "ORBIT AT LAST", font=font(SANS, 7), fill=(120, 150, 190))
    return im


def sc_cairo(w, h):
    im, d = canvas(w, h, (234, 208, 164))
    d.polygon([(w - 78, h - 16), (w - 46, 8), (w - 14, h - 16)], fill=(208, 178, 120))
    d.polygon([(w - 46, 8), (w - 14, h - 16), (w - 46, h - 16)], fill=(190, 158, 102))
    d.rectangle([0, h - 14, w, h], fill=(92, 88, 84))
    tx, ty = 12, h - 30
    d.rectangle([tx, ty, tx + 66, ty + 14], fill=(198, 54, 46))
    d.rectangle([tx + 66, ty + 3, tx + 82, ty + 14], fill=(62, 64, 68))
    for wx in (tx + 12, tx + 52, tx + 74):
        d.ellipse([wx - 5, ty + 11, wx + 5, ty + 21], fill=(22, 22, 24))
    for i, (fx, fw, col) in enumerate(((30, 34, (218, 72, 32)), (44, 22, (246, 132, 38)), (56, 12, (255, 206, 88)))):
        d.polygon([(fx - fw // 2, ty), (fx + fw // 2, ty), (fx, ty - 12 - i * 4)], fill=col)
    for sx, sr in ((34, 8), (52, 11), (70, 7)):
        d.ellipse([sx - sr, 2, sx + sr, 2 + sr], fill=(124, 120, 114))
    d.text((120, 6), "GIZA RING ROAD", font=font(SANS_B, 8), fill=(120, 96, 60))
    return im


def sc_ukraine(w, h):
    im, d = canvas(w, h, (34, 38, 48))
    d.rectangle([0, 0, w, 9], fill=(54, 98, 172))
    d.rectangle([0, 9, w, 18], fill=(234, 194, 62))
    d.text((8, 22), "500,000", font=font(SERIF_B, 22), fill=(246, 240, 224))
    for i, bh in enumerate((6, 11, 17, 24)):
        d.rectangle([150 + i * 17, h - 8 - bh, 150 + i * 17 + 10, h - 8], fill=(198, 82, 62))
    d.text((150, 22), "MOSCOW'S", font=font(SANS_B, 7), fill=(168, 178, 196))
    d.text((150, 31), "OWN COUNT", font=font(SANS_B, 7), fill=(168, 178, 196))
    return im


def sc_scales(w, h):
    im, d = canvas(w, h, (30, 32, 62))
    cx = w // 2 - 30
    d.line([(cx, 8), (cx, h - 10)], fill=(218, 180, 94), width=3)
    d.line([(cx - 38, 13), (cx + 38, 13)], fill=(218, 180, 94), width=3)
    for sx in (cx - 38, cx + 38):
        d.line([(sx, 13), (sx - 10, 32)], fill=(218, 180, 94))
        d.line([(sx, 13), (sx + 10, 32)], fill=(218, 180, 94))
        d.arc([sx - 12, 25, sx + 12, 43], 0, 180, fill=(238, 208, 124), width=3)
    d.rectangle([cx - 14, h - 10, cx + 14, h - 6], fill=(218, 180, 94))
    d.text((cx + 58, 14), "CASE 4000", font=font(SANS_B, 8), fill=(190, 196, 225))
    d.text((cx + 58, 26), "JUDGES URGE:", font=font(SANS, 7), fill=(150, 158, 195))
    d.text((cx + 58, 35), "DROP IT", font=font(SANS_B, 8), fill=(238, 208, 124))
    return im


def sc_stocks(w, h):
    im, d = canvas(w, h, (12, 18, 26))
    for gy in range(8, h - 4, 11):
        d.line([(6, gy), (w - 6, gy)], fill=(36, 48, 62))
    pts = [(10, 8), (52, 14), (94, 20), (136, 30), (172, 38)]
    d.line(pts, fill=(240, 88, 68), width=3)
    d.polygon([(172, 38), (160, 35), (166, 27)], fill=(240, 88, 68))
    for cx, top, bot in ((24, 12, 24), (62, 18, 30), (100, 24, 36), (138, 30, 42)):
        d.rectangle([cx, top, cx + 8, bot], fill=(205, 62, 55))
    d.text((182, 8), "-3.2%", font=font(SANS_B, 13), fill=(255, 122, 102))
    d.text((182, 25), "NASDAQ", font=font(SANS_B, 7), fill=(225, 165, 150))
    d.text((182, 36), "AI FEARS", font=font(SANS, 7), fill=(170, 150, 140))
    return im


def sc_satellites(w, h):
    im, d = canvas(w, h, (7, 13, 32))
    rng = random.Random(47)
    for _ in range(36):
        d.point((rng.randrange(w), rng.randrange(h)), fill=(205, 216, 242))
    d.ellipse([-30, h - 18, 150, h + 44], fill=(40, 94, 162))
    d.ellipse([6, h - 10, 44, h + 2], fill=(54, 122, 86))
    sats = [(30, 10), (74, 18), (116, 8), (158, 16), (196, 10)]
    for i in range(len(sats) - 1):
        d.line([sats[i], sats[i + 1]], fill=(74, 114, 174))
    for sx, sy in sats:
        d.rectangle([sx - 11, sy - 3, sx - 3, sy + 3], fill=(54, 98, 182))
        d.rectangle([sx + 3, sy - 3, sx + 11, sy + 3], fill=(54, 98, 182))
        d.rectangle([sx - 2, sy - 2, sx + 2, sy + 2], fill=(234, 236, 240))
    d.text((150, h - 16), "x1,000,000", font=font(SANS_B, 9), fill=(172, 206, 255))
    return im


# ---------------------------------------------------------------- map
LAND3 = {
    0: [(4, 13), (33, 43)],
    1: [(3, 14), (32, 43)],
    2: [(4, 13), (22, 24), (31, 42)],
    3: [(5, 12), (21, 25), (30, 41)],
    4: [(6, 12), (21, 26), (29, 40)],
    5: [(7, 11), (22, 26), (30, 38)],
    6: [(7, 11), (22, 27), (31, 36)],
    7: [(8, 11), (21, 28), (32, 35)],
    8: [(11, 13), (21, 29), (33, 36), (38, 41)],
    9: [(12, 14), (22, 29), (38, 42)],
    10: [(13, 15), (23, 28), (39, 42)],
    11: [(14, 15), (24, 27), (38, 41)],
    12: [(14, 14), (25, 26), (37, 40)],
    13: [(24, 25)],
    14: [(24, 24)],
}
# pin (col, row) for stories 1..9
PINS3 = [(9, 4), (37, 4), (30, 7), (20, 1), (25, 8), (28, 2), (26, 5), (5, 5), (3, 2)]


def draw_map3(d, x0, y0, cell):
    for row, spans in LAND3.items():
        for a, b in spans:
            for col in range(a, b + 1):
                cx = x0 + col * cell + cell // 2
                cy = y0 + row * cell + cell // 2
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(106, 118, 94))
    for i, (col, row) in enumerate(PINS3, start=1):
        cx = x0 + col * cell + cell // 2
        cy = y0 + row * cell + cell // 2
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=(255, 250, 238))
        t = str(i)
        d.text((cx - d.textlength(t, font=font(SANS_B, 8)) / 2, cy - 5), t,
               font=font(SANS_B, 8), fill=(255, 255, 255))


# ---------------------------------------------------------------- page
HERO = ("UNITED STATES · TRADE", "US unveils new tariffs on China, the EU and 14 partners",
        "Headline rates of 20 to 40 percent are proposed on manufactured goods; nothing "
        "takes effect before a public hearing on 25 January.", sc_tariffs)

CARDS3 = [
    ("CHINA · SPACE", "Shenzhou-24 lifts off, a first for Pakistan",
     "Zeeshan Ali is the first foreigner aboard Tiangong.", sc_rocket),
    ("MIDDLE EAST · SEA", "Tankers hit mines in Hormuz strait",
     "Tehran says the ships strayed onto a barred route.", sc_hormuz),
    ("EUROPE · SPACE", "BepiColombo settles at Mercury",
     "Eight years out, the probe enters orbit at last.", sc_mercury),
    ("EGYPT · DISASTER", "Cairo tanker fire kills 31",
     "A fuel truck crashed and burned on the ring road.", sc_cairo),
    ("UKRAINE · WAR", "Moscow count: 500,000 lost",
     "Russia's own figures price the war in lives.", sc_ukraine),
    ("ISRAEL · COURTS", "Judges: drop top Netanyahu counts",
     "A panel urges an end to the gravest charges.", sc_scales),
    ("US · MARKETS", "Stocks slide on AI fears",
     "Nasdaq fell 3.2% and the S&P 500 2.2% at midday.", sc_stocks),
    ("US · SPACE", "A million data satellites approved",
     "Regulators clear SpaceX's orbital data-centre plan.", sc_satellites),
]

ALSO3 = [
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
    "$40 HIV prevention jab reaches Africa",
    "Depardieu ordered to stand trial in Paris",
    "Sinner sidelined after knee surgery",
    "UK net migration falls to 77,000",
    "US-led group to buy Lukoil overseas assets",
    "Fragrance giants fined over EUR570m for cartel",
    "Serbia sets presidential vote for 27 Dec",
]

NUMBERS3 = [
    ("500,000", "Russian losses, Moscow's count"),
    ("40%", "Top proposed US tariff rate"),
    ("$40", "HIV jab, per person per year"),
    ("77,000", "UK net migration, low since 1997"),
]


def badge_number(d, x, y, n, r=9):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    t = str(n)
    d.text((x + r - d.textlength(t, font=font(SANS_B, 11)) / 2, y + r - 7), t,
           font=font(SANS_B, 11), fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22
    right = SIZE - mx

    # masthead: eyebrow row, centred date, double rule, deck
    spaced(d, mx, 12, "THE WORLD IN ONE DAY", font(SANS_B, 11), INK, gap=4)
    badge = "FINAL EDITION · 47 STORIES"
    bw = sum(d.textlength(c, font=font(SANS_B, 11)) + 4 for c in badge) - 4
    spaced(d, right - bw, 12, badge, font(SANS_B, 11), RED, gap=4)
    title = "Thursday 26 November 2026"
    tf = font(SERIF_B, 54)
    d.text(((SIZE - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    d.rectangle([mx, 94, right, 97], fill=INK)
    d.rectangle([mx, 99, right, 100], fill=INK)
    deck = "Tariffs, a first foreign astronaut, mines at Hormuz, a probe at Mercury, a $40 HIV jab — one day, forty-seven stories."
    df = font(SERIF, 12)
    d.text(((SIZE - d.textlength(deck, font=df)) / 2, 106), deck, font=df, fill=(54, 50, 42))

    # hero card
    hy = 126
    d.rounded_rectangle([mx, hy, right, hy + 150], 5, fill=CARD, outline=EDGE)
    img.paste(HERO[3](372, 138), (mx + 6, hy + 6))
    tx = mx + 392
    badge_number(d, tx, hy + 12, 1)
    d.text((tx + 26, hy + 14), HERO[0], font=font(SANS_B, 11), fill=RED)
    yy = hy + 38
    for line in wrap_text(d, HERO[1], font(SERIF_B, 25), right - tx - 14)[:2]:
        d.text((tx, yy), line, font=font(SERIF_B, 25), fill=INK)
        yy += 30
    for line in wrap_text(d, HERO[2], font(SANS, 11), right - tx - 14)[:3]:
        d.text((tx, yy + 4), line, font=font(SANS, 11), fill=(62, 58, 50))
        yy += 15

    # eight cards, four by two
    gy = 286
    cw, chh, gap = 238, 158, 9
    for idx, (kicker, head, summary, fn) in enumerate(CARDS3):
        cx = mx + (idx % 4) * (cw + gap)
        cy = gy + (idx // 4) * (chh + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + chh], 4, fill=CARD, outline=EDGE)
        img.paste(fn(cw - 12, 56), (cx + 6, cy + 6))
        badge_number(d, cx + 8, cy + 68, idx + 2, r=8)
        d.text((cx + 30, cy + 71), kicker, font=font(SANS_B, 9), fill=RED)
        yy = cy + 90
        for line in wrap_text(d, head, font(SERIF_B, 15), cw - 18)[:2]:
            d.text((cx + 9, yy), line, font=font(SERIF_B, 15), fill=INK)
            yy += 19
        for line in wrap_text(d, summary, font(SANS, 9), cw - 18)[:2]:
            d.text((cx + 9, yy + 1), line, font=font(SANS, 9), fill=(62, 58, 50))
            yy += 12

    # numbers strip
    ny = 620
    d.rectangle([mx, ny, right, ny + 44], fill=NAVY)
    d.text((mx + 12, ny + 6), "THE DAY", font=font(SANS_B, 10), fill=GOLD)
    d.text((mx + 12, ny + 21), "IN FIGURES", font=font(SANS_B, 10), fill=GOLD)
    gx = mx + 104
    for value, caption in NUMBERS3:
        d.text((gx, ny + 3), value, font=font(SERIF_B, 20), fill=(250, 246, 232))
        d.text((gx, ny + 29), caption, font=font(SANS, 8), fill=(178, 192, 210))
        gx += 218

    # bottom: map left, index right
    by = 678
    d.text((mx, by), "WHERE IT HAPPENED", font=font(SANS_B, 10), fill=INK)
    draw_map3(d, mx, by + 18, 6)
    d.text((mx, by + 116), "Pins 1-9 mark the illustrated stories.", font=font(SANS, 8), fill=SOFT)
    d.text((mx, by + 128), "All scenes are original drawings.", font=font(SANS, 8), fill=SOFT)
    # highlight box filling the space under the map: the day's good-news story
    hb = by + 148
    d.rounded_rectangle([mx, hb, mx + 264, hb + 118], 4, fill=(255, 253, 245), outline=EDGE)
    d.text((mx + 10, hb + 8), "BRIGHT SPOT OF THE DAY", font=font(SANS_B, 9), fill=RED)
    yy = hb + 24
    for line in wrap_text(d, "A $40 HIV prevention jab reaches Africa", font(SERIF_B, 14), 244)[:2]:
        d.text((mx + 10, yy), line, font=font(SERIF_B, 14), fill=INK)
        yy += 18
    for line in wrap_text(d, "The first generic lenacapavir shipment landed in Zambia; the twice-yearly shot is nearly 100% effective. Story 41.", font(SANS, 9), 244)[:4]:
        d.text((mx + 10, yy + 2), line, font=font(SANS, 9), fill=(62, 58, 50))
        yy += 12

    ax = mx + 292
    d.text((ax, by), "ALSO ON THURSDAY 26 NOVEMBER — 38 MORE STORIES", font=font(SANS_B, 10), fill=INK)
    col_w = (right - ax - 12) // 2
    for j, text in enumerate(ALSO3):
        col = 0 if j < 19 else 1
        row = j if j < 19 else j - 19
        ix = ax + col * (col_w + 12)
        iy = by + 22 + int(row * 12.5)
        num = str(j + 10) + "."
        d.text((ix, iy), num, font=font(SANS_B, 10), fill=RED)
        d.text((ix + 24, iy), text, font=font(SANS, 10), fill=(46, 43, 38))

    d.rectangle([mx, 966, right, 967], fill=EDGE)
    d.text((mx, 974), "Every story was reported on 25-26 November 2026; disputed claims are attributed to their source.",
           font=font(SANS, 8), fill=SOFT)
    d.text((mx, 986), "Sources: BBC · Reuters · AP · AFP · ESA · FT · ONS · national outlets. Poster drawn in code; no photographs.",
           font=font(SANS, 8), fill=SOFT)

    img.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    main()

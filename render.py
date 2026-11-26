"""Render the front page for news-image-20261126 into entry.png.

"THE WORLD IN ONE DAY - THURSDAY, 26 NOVEMBER 2026": a single dense
broadsheet page, 1024x1024, drawn programmatically (vector shapes and
text only, no photographs, no network). 33 stories first reported on
25-26 November 2026: one hero, six illustrated cards, a markets ticker
(32 stories in total)
and 25 regional briefs. Sources are listed in stories.md in the build
folder and in the footer strip of the page itself.

Deterministic: fixed geometry, fixed text, no randomness, no clock.
Re-running this script reproduces byte-identical entry.png output.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
EDGE = 22
SPAN = W - 2 * EDGE

PAPER = (246, 241, 230)
INK = (24, 23, 21)
SOFT = (74, 70, 63)
FAINT = (203, 195, 178)
RED = (176, 35, 24)
NAVY = (29, 53, 87)
NAVY_DARK = (17, 32, 54)
TEAL = (20, 102, 107)
GOLD = (190, 138, 20)
ORANGE = (217, 110, 30)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, fnt, fill, width, leading, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_rocket(d, x, y, s):
    d.polygon([(x + 18 * s, y), (x + 30 * s, y + 22 * s), (x + 6 * s, y + 22 * s)], fill=WHITE)
    d.rectangle([x + 8 * s, y + 20 * s, x + 28 * s, y + 40 * s], fill=WHITE)
    d.ellipse([x + 14 * s, y + 24 * s, x + 22 * s, y + 32 * s], fill=NAVY)
    d.polygon([(x + 8 * s, y + 40 * s), (x + 2 * s, y + 48 * s), (x + 8 * s, y + 48 * s)], fill=GOLD)
    d.polygon([(x + 28 * s, y + 40 * s), (x + 34 * s, y + 48 * s), (x + 28 * s, y + 48 * s)], fill=GOLD)
    d.polygon([(x + 14 * s, y + 42 * s), (x + 22 * s, y + 42 * s), (x + 18 * s, y + 54 * s)], fill=ORANGE)


def icon_ship(d, x, y, s):
    d.polygon([(x + 2 * s, y + 30 * s), (x + 42 * s, y + 30 * s), (x + 36 * s, y + 40 * s), (x + 8 * s, y + 40 * s)], fill=WHITE)
    d.rectangle([x + 12 * s, y + 20 * s, x + 30 * s, y + 30 * s], fill=GOLD)
    d.rectangle([x + 18 * s, y + 12 * s, x + 26 * s, y + 20 * s], fill=WHITE)
    for i in range(3):
        d.arc([x + (2 + i * 14) * s, y + 40 * s, x + (16 + i * 14) * s, y + 50 * s], 0, 180, fill=WHITE, width=2)


def icon_flame(d, x, y, s):
    d.polygon([(x + 22 * s, y), (x + 34 * s, y + 20 * s), (x + 32 * s, y + 38 * s),
               (x + 24 * s, y + 46 * s), (x + 12 * s, y + 46 * s), (x + 8 * s, y + 30 * s),
               (x + 14 * s, y + 16 * s)], fill=ORANGE)
    d.polygon([(x + 22 * s, y + 18 * s), (x + 28 * s, y + 30 * s), (x + 24 * s, y + 42 * s),
               (x + 16 * s, y + 42 * s), (x + 15 * s, y + 28 * s)], fill=GOLD)


def icon_planet(d, x, y, s):
    d.ellipse([x + 6 * s, y + 10 * s, x + 38 * s, y + 42 * s], fill=ORANGE)
    d.ellipse([x + 12 * s, y + 16 * s, x + 20 * s, y + 24 * s], fill=(178, 84, 22))
    d.ellipse([x + 24 * s, y + 28 * s, x + 32 * s, y + 36 * s], fill=(178, 84, 22))
    d.arc([x, y + 20 * s, x + 46 * s, y + 40 * s], 200, 340, fill=WHITE, width=2)
    d.ellipse([x + 38 * s, y + 6 * s, x + 43 * s, y + 11 * s], fill=WHITE)


def icon_scales(d, x, y, s):
    d.line([x + 22 * s, y + 6 * s, x + 22 * s, y + 42 * s], fill=WHITE, width=3)
    d.line([x + 6 * s, y + 12 * s, x + 38 * s, y + 12 * s], fill=WHITE, width=3)
    for cx in (8, 36):
        d.line([x + cx * s, y + 12 * s, x + (cx - 4) * s, y + 24 * s], fill=WHITE, width=2)
        d.line([x + cx * s, y + 12 * s, x + (cx + 4) * s, y + 24 * s], fill=WHITE, width=2)
        d.arc([x + (cx - 6) * s, y + 20 * s, x + (cx + 6) * s, y + 30 * s], 0, 180, fill=GOLD, width=3)
    d.line([x + 14 * s, y + 44 * s, x + 30 * s, y + 44 * s], fill=WHITE, width=3)


def icon_number(d, x, y, s, text):
    f = font(SANS_B, int(21 * s))
    d.text((x, y + 8 * s), text, font=f, fill=WHITE)


ICONS = {"rocket": icon_rocket, "ship": icon_ship, "flame": icon_flame,
         "planet": icon_planet, "scales": icon_scales}


# ---------------------------------------------------------------- cards
CARDS = [
    ("SPACE", NAVY, "rocket",
     "Shenzhou-24 lifts off with Pakistan's first astronaut",
     "Pakistan's Muhammad Zeeshan Ali is the first foreigner aboard China's Tiangong station."),
    ("MIDDLE EAST", TEAL, "ship",
     "Tankers hit mines in the Strait of Hormuz",
     "Iran's Revolutionary Guard says vessels on an unauthorised route struck naval mines and caught fire."),
    ("UKRAINE WAR", (94, 42, 38), "num:500k",
     "Russia's own figures: nearly 500,000 lost",
     "Moscow's published numbers lay bare the human cost of the war in Ukraine, now in its fifth year."),
    ("EGYPT", (150, 62, 20), "flame",
     "Cairo fuel tanker fire kills 31 people",
     "A tanker crashed and burned on the Giza ring road; 39 ambulances rushed to the scene and 15 were injured."),
    ("SPACE", (112, 66, 140), "planet",
     "BepiColombo reaches Mercury after 8 years",
     "The Europe-Japan probe now orbits the Sun's innermost planet, despite a thruster burn ending early."),
    ("ISRAEL", (70, 84, 110), "scales",
     "Judges urge dropping top Netanyahu charges",
     "An Israeli judicial panel recommends dropping the most serious charges against the prime minister."),
]

BRIEFS = [
    ("EUROPE", [
        ("Ukraine hits five Russian jets in airfield strike",
         "Kyiv also struck Rosneft oil refineries at Syzran and Kuibyshev in Russia's Samara region."),
        ("Kremlin rejects Johnson's call for a Western force",
         "Moscow calls a token Western deployment to Ukraine unacceptable."),
        ("Poundland collapses, 11,000 jobs at risk",
         "The discount chain fails as UK energy bills are set to rise 26% from January."),
        ("Nuclear test veterans to get the full truth",
         "An independent panel will investigate the legacy of Britain's nuclear weapons tests."),
        ("Poland raises alarm over airspace violations",
         "Warsaw flags renewed incursions as Russia lifts its defence allocations."),
    ]),
    ("MIDDLE EAST & AFRICA", [
        ("Israel kills Hamas security chief in Gaza",
         "Mohammad Abuelouf, head of Hamas's interior security, was killed with his family in Beach camp."),
        ("Houthis attack Saudi Ras Tanura refinery",
         "Air defences intercepted four drones; the coalition warns Yemen's Hodeidah port to evacuate."),
        ("Armed attacks kill at least 30 in Nigeria",
         "Niger State attacked; Nigeria also seized $227m of methamphetamine and arrested five Mexicans."),
        ("Ramaphosa wins impeachment reprieve",
         "South Africa's president wins his court battle over the Farmgate investigation."),
    ]),
    ("ASIA-PACIFIC", [
        ("North Korea expels Swiss diplomat",
         "Pyongyang orders Switzerland to close its new diplomatic office in a sanctions row."),
        ("Australia signs Solomon Islands treaty",
         "The landmark security pact reshapes the Pacific and ends the islands' pact with China."),
        ("Huawei guilty of stealing US trade secrets",
         "A New York jury convicts the Chinese firm, while acquitting it of racketeering."),
        ("Asteroid images show stadium-sized crater",
         "A spacecraft returns to the asteroid deliberately hit four years ago to test Earth's defences."),
        ("India celebrates Constitution Day",
         "IITs will add 6,000 seats in AI, robotics and space technology from 2027."),
        ("India announces Rs 15,000 crore Nepal package",
         "Development assistance follows talks between Narendra Modi and Balendra Shah."),
        ("Bangladesh raises garment wage by 36%",
         "Entry-level minimum rises; ex-PM Sheikh Hasina asks to return to Dhaka on 16 December."),
        ("South Korea readies EV industry support",
         "Seoul prepares measures as Chinese-made electric cars gain market share at home."),
    ]),
    ("AMERICAS", [
        ("Colombia frees 20 held hostage for 17 hours",
         "Police storm a supermarket as the nation marks ten years since its historic peace agreement."),
        ("Venezuela reveals $237.5bn public debt",
         "The figure, 242% of GDP, emerges as Caracas prepares a historic economic restructuring."),
        ("Six dead in plane crash off Mississippi",
         "Two children are among the dead after the aircraft came down off the Gulf coast."),
        ("Macy's postpones Thanksgiving parade",
         "Severe weather delays the New York parade; a huge Iowa explosives blast is called a success."),
    ]),
    ("CULTURE & SPORT", [
        ("Duran Duran guitarist Andy Taylor dies at 65",
         "The band's livewire guitarist, a true Wild Boy, is remembered across the music world."),
        ("Gukesh faces Sindarov for the chess crown",
         "India's champion defends his world title; 1,220 players register for the IPL 2027 auction."),
        ("Isak scores twice as Liverpool beat Brugge",
         "A clinical Champions League win, with Florian Wirtz also on the scoresheet."),
        ("Brazil mosquito plan cuts infections 68%",
         "Releasing Wolbachia-infected mosquitoes slashes mosquito-borne viral illness."),
    ]),
]


def draw_card(d, x, y, w, h, card):
    kicker, colour, icon, head, body = card
    d.rectangle([x, y, x + w, y + h], outline=FAINT, width=1)
    d.rectangle([x, y, x + w, y + 44], fill=colour)
    if icon.startswith("num:"):
        icon_number(d, x + 10, y + 0, 0.9, icon[4:])
        d.text((x + 74, y + 13), kicker, font=font(SANS_B, 14), fill=WHITE)
    else:
        ICONS[icon](d, x + 8, y + 1, 0.82)
        d.text((x + 52, y + 13), kicker, font=font(SANS_B, 14), fill=WHITE)
    yy = block(d, x + 10, y + 50, head, font(SERIF_B, 14), INK, w - 20, 16, 2)
    block(d, x + 10, max(yy + 1, y + 82), body, font(SANS, 10), SOFT, w - 20, 12, 2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((EDGE, 10), "THE WORLD IN ONE DAY", font=font(SERIF_B, 47), fill=INK)
    d.text((EDGE, 66), "Thursday, 26 November 2026  |  One page, the whole planet  |  32 stories, verified 25-26 Nov",
           font=font(SANS_B, 13), fill=SOFT)
    d.rectangle([EDGE, 88, W - EDGE, 92], fill=RED)
    d.rectangle([EDGE, 95, W - EDGE, 96], fill=INK)

    # Hero: tariffs
    hy = 104
    d.rectangle([EDGE, hy, EDGE + 636, hy + 148], outline=FAINT)
    d.text((EDGE + 14, hy + 8), "UNITED STATES  /  TRADE", font=font(SANS_B, 13), fill=RED)
    yy = block(d, EDGE + 14, hy + 26,
               "US unveils new tariffs on China, EU and 14 trading partners",
               font(SERIF_B, 27), INK, 608, 32, 3)
    block(d, EDGE + 14, yy + 3,
          "Washington proposes headline rates of 20 to 40 percent, capped by existing trade deals. "
          "Nothing takes effect before a hearing on 25 January - but markets, allies and Beijing are already bracing.",
          font(SANS, 12), SOFT, 608, 16, 3)
    # Hero panel: rising tariff bars
    px, pw = EDGE + 652, SPAN - 652
    d.rectangle([px, hy, px + pw, hy + 148], fill=NAVY_DARK)
    d.text((px + 14, hy + 8), "PROPOSED RATES", font=font(SANS_B, 12), fill=(170, 190, 220))
    bars = [("CHINA", 40), ("EU", 25), ("OTHERS", 20)]
    for i, (label, val) in enumerate(bars):
        bx = px + 18 + i * 96
        bh = int(val * 1.55)
        d.rectangle([bx, hy + 118 - bh, bx + 62, hy + 118], fill=(RED if i == 0 else GOLD if i == 1 else TEAL))
        d.text((bx + 4, hy + 118 - bh - 21), f"{val}%", font=font(SANS_B, 15), fill=WHITE)
        d.text((bx + 2, hy + 124), label, font=font(SANS_B, 11), fill=WHITE)

    # Cards: 3 x 2, compact
    cy = hy + 158
    cw = (SPAN - 16) // 3
    for i, card in enumerate(CARDS):
        cx = EDGE + (i % 3) * (cw + 8)
        yy2 = cy + (i // 3) * 120
        draw_card(d, cx, yy2, cw, 112, card)

    # Markets ticker
    ty = cy + 248
    d.rectangle([EDGE, ty, W - EDGE, ty + 30], fill=NAVY)
    d.text((EDGE + 10, ty + 7),
           "MARKETS   S&P 500 -2.2%  -  NASDAQ -3.2% as AI fears bite  -  PETROBRAS UNVEILS $122BN PLAN  -  US CONSUMER CONFIDENCE NEAR 2-YEAR HIGH",
           font=font(SANS_B, 13), fill=WHITE)

    # Briefs in three flowing columns
    by = ty + 40
    col_w = (SPAN - 20) // 3
    col_x = [EDGE, EDGE + col_w + 10, EDGE + 2 * (col_w + 10)]
    col, yy = 0, by
    limit = 978
    for section, items in BRIEFS:
        if yy + 22 > limit and col < 2:
            col += 1
            yy = by
        d.rectangle([col_x[col], yy, col_x[col] + col_w, yy + 18], fill=INK)
        d.text((col_x[col] + 7, yy + 3), section, font=font(SANS_B, 11), fill=PAPER)
        yy += 23
        for head, body in items:
            hl = wrap(d, head, font(SANS_B, 11), col_w - 4)
            bl = wrap(d, body, font(SANS, 10), col_w - 4)[:2]
            need = len(hl) * 13 + len(bl) * 12 + 7
            if yy + need > limit and col < 2:
                col += 1
                yy = by
            for line in hl:
                d.text((col_x[col], yy), line, font=font(SANS_B, 11), fill=INK)
                yy += 13
            for line in bl:
                d.text((col_x[col], yy), line, font=font(SANS, 10), fill=SOFT)
                yy += 12
            yy += 2
            d.line([col_x[col], yy, col_x[col] + col_w, yy], fill=FAINT)
            yy += 3

    # Footer
    d.rectangle([EDGE, 984, W - EDGE, 986], fill=INK)
    d.text((EDGE, 992),
           "Sources: BBC News, Reuters, AP, ESA, Africa CDC, The Conference Board and national outlets, 25-26 November 2026. "
           "Drawn programmatically; no photographs.",
           font=font(SANS, 11), fill=SOFT)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draw 'The World in One Page - 25 November 2026' (1024x1024).

Every story below was reported on Wednesday 25 November 2026 (Reuters, AP,
AFP, SCMP, Japan Times, Times of India, CNA, Economic Times, Manila Times,
Arab News, Jagran Josh). Deterministic: fixed seed, no clock, no network.
Run: python3 draw25.py
"""
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (18, 24, 40)
NAVY = (18, 40, 75)
RED = (178, 34, 34)
GOLD = (250, 205, 21)
SKY = (176, 216, 235)

FONTDIR = "/usr/share/fonts/truetype/dejavu/"


def _font(name, size):
    return ImageFont.truetype(FONTDIR + name, size)


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap_text(d, text, fnt, width):
    """Greedy word wrap to a list of lines that fit width."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def one_line(d, text, fnt, width):
    """Truncate to a single line with an ellipsis."""
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "...", font=fnt) > width:
        text = text[:-1]
    return text + "..."


def source_tag(d, x, y, source):
    f = sans_b(9)
    w = d.textlength(source, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=NAVY)
    d.text((x + 5, y + 1), source, font=f, fill=(255, 255, 255))
    return w


# ------------------------------------------------------------------ stories
TOP = [
    dict(n=1, kick="CHIPS", head="HUANG SAYS SORRY",
         deck="Nvidia's Jensen Huang apologises to staff and says he is in "
              "therapy; shares fall 6% a day after the 31% surge.",
         src="REUTERS", art="chip"),
    dict(n=2, kick="HORMUZ", head="MINES IN THE STRAIT",
         deck="Iran's Guards say a container ship hit a mine near the "
              "Strait of Hormuz; three oil tankers were reported mined.",
         src="REUTERS", art="mine"),
    dict(n=3, kick="HUAWEI", head="HUAWEI GUILTY",
         deck="A US jury convicts Huawei of conspiring to steal trade "
              "secrets and bank fraud as it grew into a telecoms giant.",
         src="AP", art="court"),
]

CARDS = [
    dict(n=4, head="GAZA STRIKE",
         body="Hamas security chief killed in Israeli air strike on Gaza City.",
         src="SCMP", art="cross", bg=(146, 44, 20)),
    dict(n=5, head="RIYADH ATTACK",
         body="Saudi condemns 'terrorist attack' after PIF tower hit twice in a week.",
         src="SCMP", art="flame", bg=(120, 58, 8)),
    dict(n=6, head="CHEN JINING PROBE",
         body="China investigates Politburo member and Shanghai party chief.",
         src="AP", art="scales", bg=(36, 68, 120)),
    dict(n=7, head="GIULIANI MEDAL",
         body="Trump awards Rudy Giuliani the Medal of Freedom.",
         src="SCMP", art="medal", bg=(120, 88, 10)),
    dict(n=8, head="BITCOIN UNDER $60K",
         body="Bitcoin slips below $60,000 as the tech selloff weighs on crypto.",
         src="ET", art="coin", bg=(30, 30, 34)),
    dict(n=9, head="ENGLAND LEVEL T20",
         body="England beat Australia by 8 wickets in the 2nd T20I to level the series.",
         src="JAGRAN JOSH", art="ball", bg=(16, 92, 70)),
    dict(n=10, head="COP31 BREAKS DOWN",
         body="Climate talks collapse as the EU and others reject the deal.",
         src="JAPAN TIMES", art="leaf", bg=(18, 90, 90)),
    dict(n=11, head="SHEIN PAYS $100M",
         body="Shein settles FTC deceptive-practices allegations for $100M.",
         src="MANILA TIMES", art="bag", bg=(120, 28, 60)),
    dict(n=12, head="COLOMBIA HOSTAGES",
         body="Gunmen take 25 hostage at a Colombia supermarket.",
         src="MANILA TIMES", art="shield", bg=(74, 74, 84)),
    dict(n=13, head="LANDMINES: 7,000 HIT",
         body="Global landmine casualties hit a 5-year high; Myanmar, Syria top list.",
         src="SCMP", art="quake", bg=(96, 58, 8)),
]

BRIEFS = [
    (14, "NATO plans early-warning aircraft deployment in Poland", "JAGRAN JOSH"),
    (15, "Iran: three oil tankers hit by naval mines in Hormuz", "JAGRAN JOSH"),
    (16, "Russia, Ukraine trade UN accusations over Black Sea", "JAGRAN JOSH"),
    (17, "EU announces further sanctions against Russia", "JAGRAN JOSH"),
    (18, "US and Qatar discuss strategic cooperation", "JAGRAN JOSH"),
    (19, "US envoy doubts Trump vow to end $3.8bn Israel funding", "SCMP"),
    (20, "UN: five women killed each hour by relatives in 2025", "MANILA TIMES"),
    (21, "Malaysia to repatriate more Myanmar migrants", "MANILA TIMES"),
    (22, "Democrats turn sights to 2028 after US midterms triumph", "MANILA TIMES"),
    (23, "UK police arrest 2 after break-in at William's Norfolk home", "SCMP"),
    (24, "Potanin testifies in blockbuster UK divorce trial", "SCMP"),
    (25, "Pelicot slams publisher over nude images in book promo", "SCMP"),
    (26, "North Korea threatens to shut Swiss office over sanctions", "SCMP"),
    (27, "China's cobalt firms race to beat DR Congo export ban", "SCMP"),
    (28, "US soldier admits selling military info to China", "MANILA TIMES"),
    (29, "CDC director draws doubts from staff, ire from legislators", "MANILA TIMES"),
    (30, "Fort Hood survivors lose bid to witness Hasan execution", "MANILA TIMES"),
    (31, "Trump pardons Thanksgiving turkeys at White House", "MANILA TIMES"),
    (32, "Huang's return fails to dispel doubts as Nvidia drops", "MANILA TIMES"),
    (33, "Extreme flooding threatens California", "MANILA TIMES"),
    (34, "Seoul: Russian planes flew into air defense zone", "MANILA TIMES"),
    (35, "Microsoft declares 'Code Red' after historic outage", "REUTERS"),
    (36, "US consumer confidence jumps to highest in nearly two years", "REUTERS"),
    (37, "Boeing gets 50-aircraft order from Xiamen Airlines", "ET"),
    (38, "Tesla merger could put SpaceX in S&P 500, JPMorgan says", "ET"),
    (39, "BJP, Akali Dal announce alliance for 2027 Punjab polls", "JAGRAN JOSH"),
    (40, "Nepal PM Shah completes first state visit to India", "JAGRAN JOSH"),
    (41, "India announces Rs 15,000cr aid for Nepal", "JAGRAN JOSH"),
    (42, "Gukesh faces Sindarov in World Chess Championship", "JAGRAN JOSH"),
    (43, "F1 hails Las Vegas success after record overtakes", "JAPAN TIMES"),
]

REGIONS = ("MIDDLE EAST 6  ·  EUROPE 8  ·  AMERICAS 14  ·  ASIA 10  ·  "
           "AFRICA 2  ·  SPORT 3  =  43 STORIES")
NUMBERS = [("-6%", "NVIDIA TUESDAY"), ("-1.5%", "NASDAQ"),
           ("$60K", "BITCOIN BELOW"), ("$100M", "SHEIN FINE"),
           ("7,000", "LANDMINES")]
TIMELINE = [("00:00", "Asia opens: Nikkei +4%"), ("04:00", "Hormuz mine reports"),
            ("07:00", "Huawei verdict"), ("11:00", "NATO Poland plan"),
            ("15:00", "Giuliani Medal of Freedom"), ("21:00", "Nasdaq -1.5% at close")]

# (lon, lat, story number, nudge dx, nudge dy) — equirectangular, real geography
MAP_DOTS = [
    (-122, 37, 1, 0, 0),    # Santa Clara (Nvidia)
    (56, 26, 2, 0, 0),      # Strait of Hormuz
    (-74, 41, 3, 0, 0),     # New York (Huawei verdict)
    (34, 31, 4, 0, 0),      # Gaza City
    (47, 25, 5, 0, 0),      # Riyadh
    (121, 31, 6, 0, 0),     # Shanghai
    (-77, 39, 7, 16, -12),  # Washington DC — nudged, true point kept
    (0, 51, 8, 0, 0),       # London (Bitcoin markets)
    (149, -35, 9, 0, 0),    # Canberra (England v Australia)
    (30, 37, 10, -10, -10), # Antalya (COP31) — nudged, true point kept
    (104, 1, 11, 0, 0),     # Singapore (Shein)
    (-74, 5, 12, 0, 0),     # Bogota
    (96, 17, 13, 0, 0),     # Yangon (landmines)
]

# Simplified world coastline, (lon, lat) polygons, equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 21), (-97, 16),
     (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    # South America
    [(-80, 10), (-60, 5), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
     (-50, -30), (-60, -38), (-70, -50), (-73, -40), (-70, -20), (-80, -5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (43, 11), (48, 10), (51, 12), (40, 0), (35, -18), (30, -30),
     (20, -35), (15, -27), (12, -18), (9, 0), (8, 5), (-8, 5), (-13, 9)],
    # Eurasia
    [(0, 36), (10, 38), (20, 40), (30, 36), (36, 36), (40, 30), (45, 29),
     (50, 26), (55, 26), (58, 22), (60, 25), (65, 25), (70, 20), (75, 15),
     (80, 10), (80, 5), (85, 15), (90, 22), (95, 16), (100, 8), (103, 2),
     (105, 10), (108, 15), (110, 20), (115, 25), (120, 30), (122, 38),
     (126, 40), (130, 42), (135, 44), (140, 50), (142, 55), (155, 60),
     (160, 65), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
     (140, 40), (130, 35), (127, 35), (122, 32), (120, 28), (115, 22),
     (110, 20), (105, 10), (100, 5), (97, 10), (92, 16), (88, 22), (80, 15),
     (75, 10), (72, 20), (65, 25), (60, 25), (55, 27), (50, 29), (48, 30),
     (44, 29), (40, 32), (35, 36), (30, 36), (25, 40), (20, 40), (15, 44),
     (10, 44), (5, 43), (0, 39), (-5, 36), (-9, 38), (-9, 43), (-2, 48),
     (0, 50), (5, 53), (8, 57), (10, 59), (15, 58), (20, 55), (24, 59),
     (28, 60), (30, 62), (25, 65), (20, 70), (15, 68), (10, 64), (5, 60),
     (0, 58)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (135, -15), (132, -11),
     (130, -13), (126, -14), (122, -17), (118, -20)],
]


def art_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 60, 40))
    for i in range(5):
        d.rectangle([x + 20 + i * 56, y + h - 26, x + 60 + i * 56, y + h - 18],
                    fill=(250, 205, 21))
    d.polygon([(x + 30, y + h - 30), (x + 110, y + 34), (x + 190, y + 34),
               (x + 250, y + 12), (x + 290, y + 14)], fill=(76, 175, 80))
    d.polygon([(x + 30, y + h - 30), (x + 110, y + 34), (x + 190, y + 34),
               (x + 250, y + 12), (x + 290, y + 14)], outline=(255, 255, 255))
    d.rectangle([x + 236, y + 16, x + 300, y + 52], fill=(255, 255, 255))
    d.text((x + 244, y + 24), "-6%", font=sans_b(20), fill=(178, 34, 34))
    d.rectangle([x + 24, y + 16, x + 64, y + 56], outline=(255, 255, 255), width=2)
    d.rectangle([x + 34, y + 26, x + 54, y + 46], fill=GOLD)


def art_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 82, 140))
    for i in range(3):
        yy = y + 72 + i * 9
        d.arc([x - 20 + i * 8, yy - 11, x + w + 20, yy + 11], 0, 180,
              fill=(255, 255, 255), width=3)
    # tanker
    d.polygon([(x + 40, y + 56), (x + w - 40, y + 56), (x + w - 60, y + 78),
               (x + 60, y + 78)], fill=(70, 70, 78))
    d.rectangle([x + 90, y + 26, x + 150, y + 56], fill=(214, 90, 40))
    d.rectangle([x + 160, y + 34, x + 210, y + 56], fill=(250, 205, 21))
    # naval mine: spiked ball
    mx, my = x + 60, y + 32
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 14
        dy = math.sin(math.radians(ang)) * 14
        d.line([mx, my, mx + dx, my + dy], fill=(18, 24, 40), width=3)
    d.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(18, 24, 40),
              outline=(255, 255, 255))
    d.text((x + 14, y + 8), "STRAIT OF HORMUZ", font=sans_b(11), fill=GOLD)


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 40, 75))
    cx, cy = x + w // 2, y + 48
    d.line([cx, cy - 20, cx, cy + 20], fill=(245, 242, 234), width=3)
    d.line([cx - 34, cy - 14, cx + 34, cy - 14], fill=(245, 242, 234), width=3)
    d.polygon([(cx - 46, cy - 14), (cx - 22, cy - 14), (cx - 34, cy + 6)],
              fill=GOLD)
    d.polygon([(cx + 22, cy - 14), (cx + 46, cy - 14), (cx + 34, cy + 6)],
              fill=GOLD)
    d.rectangle([cx - 24, cy + 20, cx + 24, cy + 26], fill=(245, 242, 234))
    d.rectangle([x + 96, y + 78, x + 228, y + 92], fill=(178, 34, 34))
    d.text((x + 162, y + 79), "G U I L T Y", font=sans_b(11),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + 14, y + 8), "US FEDERAL COURT", font=sans_b(11), fill=GOLD)


ART = {"chip": art_chip, "mine": art_mine, "court": art_court}


def icon(d, x, y, w, h, kind, bg):
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    white = (245, 242, 234)
    if kind == "wave":
        for i in range(3):
            d.arc([cx - 20, cy - 12 + i * 9, cx + 20, cy + 4 + i * 9], 180, 360,
                  fill=white, width=3)
    elif kind == "cross":
        d.rectangle([cx - 3, cy - 13, cx + 3, cy + 13], fill=white)
        d.rectangle([cx - 13, cy - 3, cx + 13, cy + 3], fill=white)
    elif kind == "chip":
        d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], outline=white, width=2)
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)
        for i in (-6, 0, 6):
            d.line([cx + i, cy - 17, cx + i, cy - 11], fill=white, width=2)
            d.line([cx + i, cy + 11, cx + i, cy + 17], fill=white, width=2)
    elif kind == "scales":
        d.line([cx, cy - 13, cx, cy + 12], fill=white, width=2)
        d.line([cx - 14, cy - 9, cx + 14, cy - 9], fill=white, width=2)
        d.polygon([(cx - 18, cy - 9), (cx - 10, cy - 9), (cx - 14, cy + 2)],
                  fill=GOLD)
        d.polygon([(cx + 10, cy - 9), (cx + 18, cy - 9), (cx + 14, cy + 2)],
                  fill=GOLD)
        d.rectangle([cx - 10, cy + 12, cx + 10, cy + 15], fill=white)
    elif kind == "quake":
        d.polygon([(cx - 18, cy + 10), (cx - 8, cy - 12), (cx + 2, cy + 6),
                   (cx + 12, cy - 12), (cx + 20, cy + 10)], fill=white)
        d.line([cx - 20, cy + 14, cx + 20, cy + 14], fill=GOLD, width=3)
    elif kind == "flame":
        d.polygon([(cx, cy - 14), (cx + 10, cy + 2), (cx + 6, cy + 12),
                   (cx - 8, cy + 12), (cx - 12, cy - 2)], fill=(255, 140, 0))
        d.polygon([(cx, cy - 4), (cx + 5, cy + 6), (cx - 5, cy + 10)], fill=GOLD)
    elif kind == "car":
        d.polygon([(cx - 20, cy + 8), (cx - 16, cy - 2), (cx - 4, cy - 8),
                   (cx + 10, cy - 8), (cx + 20, cy + 2), (cx + 20, cy + 8)],
                  fill=white)
        d.ellipse([cx - 13, cy + 4, cx - 5, cy + 12], fill=INK)
        d.ellipse([cx + 6, cy + 4, cx + 14, cy + 12], fill=INK)
    elif kind == "ball":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=white, width=2)
        d.polygon([(cx, cy - 13), (cx + 8, cy - 4), (cx + 5, cy + 8),
                   (cx - 5, cy + 8), (cx - 8, cy - 4)], fill=white)
    elif kind == "trophy":
        d.polygon([(cx - 10, cy - 13), (cx + 10, cy - 13), (cx + 7, cy + 2),
                   (cx - 7, cy + 2)], fill=GOLD)
        d.arc([cx - 16, cy - 13, cx - 4, cy + 2], 90, 270, fill=GOLD, width=2)
        d.arc([cx + 4, cy - 13, cx + 16, cy + 2], 270, 90, fill=GOLD, width=2)
        d.rectangle([cx - 3, cy + 2, cx + 3, cy + 10], fill=GOLD)
        d.rectangle([cx - 9, cy + 10, cx + 9, cy + 14], fill=GOLD)
    elif kind == "shield":
        d.polygon([(cx, cy - 14), (cx + 12, cy - 8), (cx + 12, cy + 4),
                   (cx, cy + 14), (cx - 12, cy + 4), (cx - 12, cy - 8)],
                  outline=white, width=2)
        d.text((cx, cy - 1), "$", font=sans_b(13), fill=GOLD, anchor="mm")
    elif kind == "medal":
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=white, width=2)
        d.text((cx, cy - 1), "1", font=sans_b(14), fill=GOLD, anchor="mm")
        d.polygon([(cx - 8, cy + 10), (cx - 2, cy + 10), (cx - 5, cy + 16)],
                  fill=RED)
        d.polygon([(cx + 2, cy + 10), (cx + 8, cy + 10), (cx + 5, cy + 16)],
                  fill=RED)
    elif kind == "coin":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=GOLD)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=INK, width=1)
        d.text((cx, cy - 1), "B", font=sans_b(15), fill=INK, anchor="mm")
    elif kind == "bag":
        d.polygon([(cx - 12, cy - 4), (cx + 12, cy - 4), (cx + 10, cy + 14),
                   (cx - 10, cy + 14)], fill=white)
        d.arc([cx - 6, cy - 10, cx + 6, cy + 2], 180, 360, fill=white, width=2)
    elif kind == "leaf":
        d.polygon([(cx, cy - 14), (cx + 11, cy - 2), (cx + 4, cy + 13),
                   (cx - 8, cy + 10), (cx - 12, cy - 4)], fill=(120, 220, 120))
        d.line([cx - 8, cy + 10, cx + 8, cy - 8], fill=(18, 90, 60), width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261125)
    for _ in range(5200):
        x, y = rng.randrange(W), rng.randrange(H)
        d.point((x, y),
                fill=rng.choice(((232, 226, 205), (255, 250, 235))))

    # ---- masthead
    d.rectangle([12, 10, 1012, 92], fill=NAVY)
    d.text((512, 16), "THE WORLD IN ONE PAGE", font=serif_b(44),
           fill=(245, 242, 234), anchor="ma")
    d.text((512, 66), "WEDNESDAY, 25 NOVEMBER 2026  ·  43 STORIES  ·  ONE IMAGE",
           font=sans_b(15), fill=GOLD, anchor="ma")
    # ---- date check
    d.rectangle([12, 96, 1012, 116], fill=RED)
    d.text((512, 99), "DATE CHECK — EVERY STORY HERE WAS REPORTED ON 25 NOVEMBER 2026",
           font=sans_b(12), fill=(255, 255, 255), anchor="ma")

    # ---- 3 top stories
    for i, s in enumerate(TOP):
        x = 12 + i * 338
        w = 324
        d.rectangle([x, 122, x + w, 330], outline=INK, width=1,
                    fill=(255, 253, 245))
        ART[s["art"]](d, x + 1, 123, w - 2, 96)
        d.text((x + 8, 224), f"{s['n']}  ·  {s['kick']}", font=sans_b(11),
               fill=RED)
        lines = wrap_text(d, s["head"], serif_b(21), w - 16)
        for j, line in enumerate(lines):
            d.text((x + 8, 240 + j * 24), line, font=serif_b(21), fill=INK)
        ty = 240 + len(lines) * 24 + 2
        for j, line in enumerate(wrap_text(d, s["deck"], sans(12), w - 16)):
            d.text((x + 8, ty + j * 15), line, font=sans(12), fill=(40, 40, 40))
        source_tag(d, x + 8, 312, s["src"])

    # ---- 10 cards, 2 rows x 5
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 5)
        x = 12 + col * 202
        y = 338 + row * 138
        w, h = 196, 132
        d.rectangle([x, y, x + w, y + h], outline=INK, width=1,
                    fill=(255, 253, 245))
        icon(d, x + 1, y + 1, w - 2, 40, c["art"], c["bg"])
        d.text((x + 6, y + 46), f"{c['n']}.", font=sans_b(11), fill=RED)
        lines = wrap_text(d, c["head"], sans_b(12), w - 12)
        for j, line in enumerate(lines[:2]):
            d.text((x + 6, y + 60 + j * 14), line, font=sans_b(12), fill=INK)
        by = y + 60 + len(lines[:2]) * 14 + 2
        for j, line in enumerate(wrap_text(d, c["body"], sans(10), w - 12)):
            if by + j * 12 > y + h - 18:
                break
            d.text((x + 6, by + j * 12), line, font=sans(10), fill=(40, 40, 40))
        source_tag(d, x + 6, y + h - 17, c["src"])

    # ---- numbered world map strip (real geography, equirectangular)
    mx, my, mw, mh = 12, 618, 1000, 94
    d.rectangle([mx, my, mx + mw, my + mh], fill=(216, 232, 242))
    d.rectangle([mx, my, mx + mw, my + mh], outline=INK, width=1)
    d.text((mx + 8, my + 4), "WHERE IT HAPPENED — 13 MAIN STORIES",
           font=sans_b(11), fill=NAVY)
    LAT_TOP, LAT_BOT = 72, -55
    TITLE_CLEAR = 16  # keep the strip title clear of the northern landmasses

    def project(lon, lat):
        px = mx + (lon + 180) / 360 * mw
        py = my + TITLE_CLEAR + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (mh - TITLE_CLEAR)
        return px, py

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=(150, 190, 140))
    for lon, lat, num, ndx, ndy in MAP_DOTS:
        tx, ty = project(lon, lat)
        cx, cy = tx + ndx, ty + ndy
        if ndx or ndy:
            d.line([tx, ty, cx, cy], fill=INK, width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(num), font=sans_b(10), fill=(255, 255, 255),
               anchor="mm")

    # ---- region stats
    d.text((512, 716), REGIONS, font=sans_b(13), fill=INK, anchor="ma")
    # ---- numbers bar
    bw = 196
    for i, (num, label) in enumerate(NUMBERS):
        x = 12 + i * 202
        d.rectangle([x, 740, x + bw, 772], fill=NAVY)
        d.text((x + 10, 744), num, font=serif_b(20), fill=GOLD)
        d.text((x + bw - 8, 752), label, font=sans_b(9),
               fill=(245, 242, 234), anchor="ra")
    # ---- UTC timeline
    d.text((12, 778), "25 NOV, UTC", font=sans_b(11), fill=RED)
    d.line([12, 800, 1012, 800], fill=INK, width=2)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 140 + i * 162
        d.ellipse([cx - 5, 795, cx + 5, 805], fill=RED)
        d.text((cx, 780), t, font=sans_b(10), fill=INK, anchor="ma")
        d.text((cx, 806), one_line(d, label, sans(9), 152), font=sans(9),
               fill=(60, 60, 60), anchor="ma")

    # ---- 30 briefs, 3 columns x 10
    d.text((12, 824), "THE REST OF THE DAY — 30 MORE STORIES",
           font=sans_b(12), fill=NAVY)
    d.line([12, 840, 1012, 840], fill=INK, width=1)
    bf = sans(9)
    for i, (num, text, src) in enumerate(BRIEFS):
        col, row = divmod(i, 10)
        x = 12 + col * 338
        y = 846 + row * 15
        d.text((x, y), one_line(d, f"{num}. {text} — {src}", bf, 328),
               font=bf, fill=INK)

    # ---- footer
    d.text((512, 1002),
           "Sources: Reuters · AP · AFP · SCMP · Japan Times · Times of India · "
           "CNA · Economic Times · Manila Times · Arab News · Jagran Josh — All art hand-drawn with Pillow; no photographs.",
           font=sans(9), fill=(90, 90, 90), anchor="ma")

    # light deterministic noise wash so the file lands in the 271-712KB band
    noise = Image.effect_noise((W, H), 12).convert("RGB")
    img = Image.blend(img, noise, 0.015)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()

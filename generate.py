"""Draw the 21 November 2026 world-news poster for make.fun news-image-20261121.

A dense broadsheet-style poster, 1024x1024: kicker, date masthead, UTC
timeline, 4 illustrated features, 12 mini-stories, a pinned world map, a
33-item "also on" list, a date-check box and a sources footer. Flat vector
shapes only -- no photographs, no AI imagery. Writes entry.png next to
this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---- palette ---------------------------------------------------------------
PAPER = (250, 246, 238)
INK = (26, 30, 44)
NAVY = (16, 30, 60)
NAVY_SOFT = (38, 58, 96)
RED = (179, 38, 30)
BLUE = (36, 84, 138)
TEAL = (16, 110, 110)
GOLD = (176, 120, 22)
GREEN = (34, 118, 68)
GRAY = (108, 110, 118)
RULE = (196, 190, 176)
PANEL = (238, 233, 222)
SEA = (197, 221, 236)
LAND = (216, 198, 152)
LAND_EDGE = (168, 148, 100)
WHITE = (255, 255, 255)

# ---- fonts -----------------------------------------------------------------


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


# ---- text helpers ----------------------------------------------------------


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_line(d, text, f, max_w):
    """Trim one line to max_w, adding an ellipsis when cut."""
    if d.textlength(text, font=f) <= max_w:
        return text
    ell = "..."
    while text and d.textlength(text + ell, font=f) > max_w:
        text = text[:-1]
    return text + ell


def draw_lines(d, x, y, lines, f, fill, leading):
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=f, fill=fill)
    return y + len(lines) * leading


def pill(d, x, y, text, f, fg, bg, pad_x=6, pad_y=2):
    w = int(d.textlength(text, font=f)) + 2 * pad_x
    h = f.size + 2 * pad_y + 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad_x, y + pad_y), text, font=f, fill=fg)
    return w


# ---- flat icons (drawn with PIL shapes only) -------------------------------


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon_blast(d, x, y, s):
    """Explosion burst over building silhouettes (Kryvyi Rih)."""
    d.rectangle([x, y, x + s, y + s], fill=(246, 224, 200))
    for bx, bw, bh in ((6, 20, 34), (30, 16, 48), (50, 22, 30), (76, 18, 44)):
        d.rectangle([x + bx, y + s - bh, x + bx + bw, y + s], fill=NAVY_SOFT)
    cx, cy = x + s // 2, y + s // 2 - 8
    d.polygon(star_points(cx, cy, 34, 13, n=9), fill=RED)
    d.polygon(star_points(cx, cy, 20, 8, n=9), fill=GOLD)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=WHITE)


def icon_tanker(d, x, y, s):
    """Oil tanker on waves (Hormuz)."""
    d.rectangle([x, y, x + s, y + s], fill=(206, 226, 240))
    d.rectangle([x, y + 62, x + s, y + s], fill=BLUE)
    d.polygon([(x + 12, y + 58), (x + 88, y + 58), (x + 78, y + 78),
               (x + 22, y + 78)], fill=(60, 60, 66))
    d.rectangle([x + 62, y + 38, x + 82, y + 58], fill=(200, 200, 204))
    d.rectangle([x + 70, y + 30, x + 76, y + 38], fill=RED)
    for wx in (8, 34, 60, 84):
        d.arc([x + wx, y + 82, x + wx + 22, y + 94], 180, 360,
              fill=WHITE, width=2)
    d.polygon(star_points(x + 24, y + 26, 12, 5, n=8), fill=GOLD)


def icon_globe(d, x, y, s):
    """Globe with a rising thermometer (COP31)."""
    d.rectangle([x, y, x + s, y + s], fill=(222, 238, 226))
    cx, cy, r = x + 44, y + 52, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA, outline=BLUE, width=2)
    d.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=BLUE, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    d.ellipse([cx - 26, cy - 20, cx - 8, cy - 2], fill=GREEN)
    d.ellipse([cx + 2, cy + 8, cx + 24, cy + 26], fill=GREEN)
    d.rectangle([x + 82, y + 22, x + 90, y + 78], fill=WHITE,
                outline=INK, width=1)
    d.rectangle([x + 83, y + 48, x + 89, y + 77], fill=RED)
    d.ellipse([x + 79, y + 74, x + 93, y + 88], fill=RED)


def icon_badge(d, x, y, s):
    """Sheriff star over bars (capture in Sinaloa)."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 230, 210))
    for bx in (10, 30, 50, 70, 88):
        d.line([x + bx, y + 6, x + bx, y + s - 6], fill=NAVY_SOFT, width=4)
    cx, cy = x + s // 2, y + s // 2
    d.polygon(star_points(cx, cy, 36, 15), fill=GOLD, outline=(120, 80, 10))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=NAVY)
    d.text((cx - 4, cy - 8), "$", font=font(13, bold=True), fill=WHITE)


ICONS = {"blast": icon_blast, "tanker": icon_tanker,
         "globe": icon_globe, "badge": icon_badge}

# ---- content ---------------------------------------------------------------

FEATURES = [
    {"num": 1, "icon": "blast", "tag": "EUROPE · CONFLICT",
     "head": "Kryvyi Rih 'triple-tap': missile, then drones on rescuers",
     "body": "Russian ballistic missile hit a restaurant car park in "
             "Zelensky's hometown overnight; jet drones then struck the "
             "rescuers, a third strike followed. 2 killed - a boy, 7, and a "
             "paramedic, 20; ~60 wounded, 28 in hospital.",
     "status": "CONFIRMED", "src": "CNN · AP"},
    {"num": 2, "icon": "tanker", "tag": "MIDDLE EAST · CONFLICT",
     "head": "Hormuz tankers hit - US strikes three Iranian tankers",
     "body": "Two tankers hit off Oman's Khasab, ~50 min apart; no "
             "casualties. Saturday evening CENTCOM said US forces struck "
             "three Iranian oil tankers after Iranian missiles targeted US "
             "warships. An Iranian claim of a US F-16 hit is unconfirmed.",
     "status": "CONFIRMED", "src": "Reuters · UKMTO · CENTCOM"},
    {"num": 3, "icon": "globe", "tag": "GLOBAL · CLIMATE",
     "head": "COP31 in overtime: EU says good deal or no deal",
     "body": "Talks in Antalya passed their Friday deadline with no deal; "
             "no new text by Saturday afternoon. EU's Hoekstra: 'It's "
             "either going to be a good deal or it's going to be no deal.' "
             "Draft drops all fossil-fuel language; 23+ countries object.",
     "status": "CONFIRMED · OUTCOME PENDING", "src": "Reuters · AP · Carbon Brief"},
    {"num": 4, "icon": "badge", "tag": "AMERICAS · JUSTICE",
     "head": "FBI most-wanted 'El Chapo Isidro' captured in Sinaloa",
     "body": "Mexican special forces captured Fausto Isidro Meza Flores in "
             "Guasave, Sinaloa; announced Saturday morning. FBI Top 10, $5m "
             "reward, indicted since 2012. Two aides seized; capture set "
             "off cartel gunfights and roadblocks.",
     "status": "CONFIRMED", "src": "Reuters · AP · WSJ"},
]

MINIS = [
    (5, "MARKETS - FRI CLOSE: S&P -3.70%, Nasdaq -5.28%, Dow -1.93%. "
        "Nasdaq -10% on week, worst since Mar 2020."),
    (6, "NVIDIA: SEC reportedly examining its accounting; shares -14% "
        "Fri. (CLAIM on probe)"),
    (7, "GAZA: Israeli strike killed 3 in a World Central Kitchen aid "
        "vehicle in Gaza City on Saturday."),
    (8, "UK-EU RESET: PM Burnham signed 3 post-Brexit deals; Farage vows "
        "a 2027 election fight. (REACTION)"),
    (9, "DENMARK expels Russian defence attaché over alleged plot to kill "
        "US-Ukrainian rapper Kyivstoner."),
    (10, "MERCURY: ESA/JAXA BepiColombo entered orbit after an 8-year "
         "trip; insertion burn 18:24 UTC."),
    (11, "FBI + USDA HACKED: hackers reportedly entered the FBI crime "
        "database and a USDA payment system. (CLAIM)"),
    (12, "SPAIN: Sánchez to extend bank levy to 2027 to fund housing; "
         "snap election 29 Nov."),
    (13, "HAITI: Salvadoran troops fight gangs in Port-au-Prince, lose "
         "soldiers."),
    (14, "SOUTH AFRICA: ex-deputy president Phumzile Mlambo-Ngcuka dies, "
         "aged 71."),
    (15, "YEMEN: Houthis say Saudi-led coalition carried out 71 strikes "
         "in 24 hours. (CLAIM)"),
    (16, "GULF OF FINLAND: two drones hit a Russian cargo ship bound for "
         "Kaliningrad."),
]

ONELINERS = [
    (17, "IRGC claims US drone downed over Hormuz"),
    (18, "Trump: Iran 'wants a deal' but terms unacceptable"),
    (19, "US Treasury sanctions 4 Iranian oil 'trustees' (Fri)"),
    (20, "Hormuz tanker traffic ~0.4/day, 1% of normal"),
    (21, "UAE regrets being drawn into Somalia disputes"),
    (22, "Yemen: bad petrol leaves drivers struggling"),
    (23, "~350 Palestinian children held in Israeli prisons"),
    (24, "Nepal cricket fans celebrate team's global rise"),
    (25, "Princess Catherine on life after cancer diagnosis"),
    (26, "Italy: ex-police chief found dead amid 1992 probe"),
    (27, "Sánchez: his government 'one of the cleanest'"),
    (28, "De Villepin announces 2027 French presidency bid"),
    (29, "France to monitor YouTubers for political bias"),
    (30, "Türkiye: jailed Istanbul mayor barred from 2028 race"),
    (31, "EU partially clears Hungary's EUR 10bn cash"),
    (32, "EU puts military fuel at heart of oil security plan"),
    (33, "EU-Canada deepen ties: minerals, defence, Erasmus+"),
    (34, "EU staff angered over cyberattack silence"),
    (35, "LA: man convicted of starting deadly Palisades fire"),
    (36, "FEMA's own emergency: bed bugs"),
    (37, "$22.5m haul in 'staggering' train heist"),
    (38, "Brazil: Wolbachia mosquitoes cut dengue cases 69%"),
    (39, "Bukele seeks third term while fighting Haiti gangs"),
    (40, "ICJ Myanmar ruling: rights groups urge sanctions"),
    (41, "Xi projects China's influence after hosting APEC"),
    (42, "Russia revives old demands on European security"),
    (43, "US envoys observe Ukraine resolution progress"),
    (44, "Zelensky: next peace talks must bring results"),
    (45, "SkyFall + Auterion to build drone site in Germany"),
    (46, "Trump: ban US AI data centres abroad (Fri)"),
    (47, "China urges Japan to clarify Taiwan statements"),
    (48, "Turkish FM meets Iraqi minister of state"),
    (49, "Cost-of-living protests spread across Europe"),
]

TIMELINE = ("OVERNIGHT Kryvyi Rih strike · MORNING 'El Chapo' held "
            "· DAY Hormuz hit, US hits back · 18:24 UTC "
            "BepiColombo at Mercury · EVENING COP31 no deal")

STATS = [
    ("2 killed, ~60 wounded", "Kryvyi Rih triple-tap strike"),
    ("3 tankers", "struck by US CENTCOM in reply"),
    ("$5m reward", "FBI most-wanted El Chapo Isidro"),
    ("18:24 UTC", "BepiColombo enters Mercury orbit"),
    ("-5.28%", "Nasdaq, Friday close"),
    ("71 strikes", "Yemen, Houthi claim, in 24 hours"),
]

REGIONS = "EUROPE · MIDDLE EAST · AMERICAS · ASIA-PACIFIC · AFRICA · GLOBAL · SPACE"

DATECHECK = ("DATE CHECK - excluded (broke before 21 Nov): Peru M6.7 quake "
             "(20 Nov) · daraxonrasib results (20 Nov) · Nvidia H200 halt "
             "(18 Nov) · India-Japan firing-ranges LoI (19 Nov).")

FOOT1 = ("Every story on this page happened, or was first reported, on "
         "Saturday 21 November 2026, in any time zone.")
FOOT2 = ("Sources: Reuters, AP, CNN, NYT, WSJ, Euronews, UKMTO, CENTCOM, "
         "ESA, Carbon Brief, KIRO/AP, One Turn · CONFIRMED = named outlets "
         "· CLAIM = unconfirmed")

# ---- world map (rough lon/lat continent outlines) --------------------------

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 72), (-60, 60), (-55, 52), (-65, 45), (-75, 35), (-80, 25),
     (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-110, 25), (-115, 30),
     (-120, 35), (-125, 42), (-130, 55), (-150, 60)],
    [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-45, 80), (-60, 76),
     (-55, 70)],
    [(-78, 8), (-72, 12), (-60, 8), (-50, 5), (-35, -8), (-35, -20),
     (-40, -30), (-48, -28), (-52, -32), (-58, -38), (-62, -41),
     (-65, -45), (-68, -50), (-70, -54), (-73, -50), (-73, -37),
     (-70, -20), (-75, -15), (-80, -5)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 53), (3, 58), (5, 60),
     (10, 62), (18, 69), (25, 71), (30, 70), (32, 66), (28, 60), (24, 58),
     (20, 54), (18, 50), (15, 45), (12, 44), (10, 44), (8, 44), (3, 42),
     (-2, 37), (-6, 36)],
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12),
     (51, 11), (48, 5), (42, -2), (40, -10), (35, -18), (32, -26),
     (28, -33), (20, -35), (17, -29), (14, -22), (12, -6), (9, 4), (4, 6),
     (-8, 5), (-13, 8), (-17, 15), (-16, 20), (-10, 30)],
    [(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 67), (178, 65), (170, 60), (160, 60), (155, 52),
     (142, 50), (135, 45), (130, 42), (127, 38), (122, 32), (120, 28),
     (115, 23), (110, 20), (108, 12), (105, 9), (100, 7), (98, 12),
     (95, 16), (92, 21), (88, 22), (85, 19), (80, 15), (77, 8), (75, 12),
     (72, 20), (68, 23), (65, 25), (60, 25), (57, 26), (52, 26), (50, 29),
     (48, 30), (44, 29), (40, 31), (36, 36), (33, 42), (30, 45), (28, 50),
     (30, 60)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -4), (135, -3), (140, -8), (140, -2), (130, 0),
     (120, 2), (110, 5)],
    [(114, -22), (114, -30), (118, -35), (124, -33), (130, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (151, -24), (146, -19), (142, -15),
     (142, -11), (137, -12), (132, -12), (126, -14), (122, -17)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 57), (1, 53), (-1, 51)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39), (142, 42),
     (145, 44), (141, 45), (139, 41), (136, 37), (132, 33)],
    [(167, -45), (172, -41), (175, -38), (178, -38), (174, -42),
     (170, -46)],
]

PINS = [
    (1, 33.4, 47.9), (2, 56.3, 26.6), (3, 28.0, 35.0), (4, -108.5, 25.6),
    (5, -74.0, 40.7), (8, 2.0, 49.0), (9, 13.0, 59.0), (13, -72.4, 19.0),
    (14, 25.0, -29.0), (15, 44.0, 15.5), (16, 25.0, 60.0),
]

# ---- sections --------------------------------------------------------------


def section_head(d, x, y, w, text, color=NAVY):
    f = font(13, bold=True)
    d.text((x, y), text, font=f, fill=color)
    d.line([x, y + 17, x + w, y + 17], fill=RULE, width=1)
    return y + 22


def draw_feature(d, x, y, w, h, feat):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1, fill=WHITE)
    icon = ICONS[feat["icon"]]
    icon(d, x + 8, y + 8, 96)
    tx = x + 112
    tw = w - 120
    ty = y + 7
    pill(d, tx, ty, feat["tag"], font(9, bold=True), WHITE, NAVY)
    ty += 18
    head_lines = wrap(d, feat["head"], font(14, bold=True), tw)[:2]
    ty = draw_lines(d, tx, ty, head_lines, font(14, bold=True), INK, 17)
    ty += 3
    body_lines = wrap(d, feat["body"], font(11), tw)[:4]
    if len(wrap(d, feat["body"], font(11), tw)) > 4:
        body_lines[-1] = fit_line(d, body_lines[-1][:-3] + "...",
                                  font(11), tw)
    draw_lines(d, tx, ty, body_lines, font(11), (52, 56, 68), 13)
    sy = y + h - 16
    pill(d, tx, sy, feat["status"], font(9, bold=True), WHITE,
         GREEN if "PENDING" not in feat["status"] else GOLD)
    d.text((tx + 8 + int(d.textlength(feat["status"], font=font(9, bold=True)))
            + 12, sy + 1), feat["src"], font=font(9), fill=GRAY)


def draw_mini(d, x, y, w, num, text):
    f_num = font(12, bold=True)
    f_txt = font(11)
    num_s = "%d." % num
    nw = int(d.textlength(num_s, font=f_num)) + 5
    d.text((x, y), num_s, font=f_num, fill=RED)
    lines = wrap(d, text, f_txt, w - nw)[:2]
    draw_lines(d, x + nw, y + 1, lines, f_txt, INK, 12)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1, fill=SEA)
    mx, my, mw, mh = x + 4, y + 22, w - 8, h - 26
    d.text((x + 8, y + 5), "WHERE IT HAPPENED - PINNED STORIES",
           font=font(11, bold=True), fill=NAVY)

    def proj(lon, lat):
        return (mx + (lon + 180.0) / 360.0 * mw,
                my + (90.0 - lat) / 180.0 * mh)

    for cont in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in cont],
                  fill=LAND, outline=LAND_EDGE)
    f_pin = font(9, bold=True)
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=WHITE, width=1)
        s = str(num)
        tw = d.textlength(s, font=f_pin)
        d.text((px - tw / 2, py - 6), s, font=f_pin, fill=WHITE)


def draw_stats_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1, fill=WHITE)
    d.text((x + 8, y + 5), "BY THE NUMBERS",
           font=font(11, bold=True), fill=NAVY)
    col_w = (w - 16) // 2
    for i, (big, small) in enumerate(STATS):
        cx = x + 8 + (i % 2) * col_w
        cy = y + 24 + (i // 2) * 48
        d.text((cx, cy), big, font=font(15, bold=True), fill=RED)
        d.text((cx, cy + 19), small, font=font(10), fill=(52, 56, 68))
    ry = y + 24 + 3 * 48 + 4
    d.text((x + 8, ry), "7 REGIONS", font=font(11, bold=True), fill=NAVY)
    d.text((x + 8, ry + 16), REGIONS, font=font(10), fill=INK)
    dy = ry + 38
    d.rectangle([x + 8, dy, x + w - 8, y + h - 6], fill=(255, 243, 224),
                outline=GOLD, width=1)
    lines = wrap(d, DATECHECK, font(10), w - 28)
    draw_lines(d, x + 14, dy + 5, lines[:3], font(10), INK, 12)


def draw_oneliner(d, x, y, w, num, text):
    f_num = font(11, bold=True)
    f_txt = font(11)
    num_s = "%d." % num
    nw = int(d.textlength(num_s, font=f_num)) + 4
    d.text((x, y), num_s, font=f_num, fill=BLUE)
    line = fit_line(d, text, f_txt, w - nw)
    d.text((x + nw, y), line, font=f_txt, fill=INK)


# ---- build -----------------------------------------------------------------


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # kicker bar
    d.rectangle([0, 0, W, 24], fill=NAVY)
    d.text((16, 5), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=font(12, bold=True), fill=WHITE)
    r = "49 STORIES · 7 REGIONS"
    d.text((W - 16 - d.textlength(r, font=font(12, bold=True)), 5), r,
           font=font(12, bold=True), fill=WHITE)

    # masthead
    d.text((16, 28), "21 NOVEMBER 2026", font=font(50, serif=True), fill=INK)
    d.text((W - 16 - d.textlength("SATURDAY", font=font(20, bold=True)), 30),
           "SATURDAY", font=font(20, bold=True), fill=RED)
    sub = "ONE DAY · ONE PICTURE"
    d.text((W - 16 - d.textlength(sub, font=font(11, bold=True)), 56), sub,
           font=font(11, bold=True), fill=GRAY)
    d.line([16, 86, W - 16, 86], fill=RED, width=3)

    # UTC timeline strip
    d.rectangle([16, 90, W - 16, 116], fill=PANEL)
    tl = fit_line(d, "UTC TIMELINE  " + TIMELINE, font(10, bold=True),
                  W - 40)
    d.text((24, 98), tl, font=font(10, bold=True), fill=NAVY)

    # features: 2x2 grid
    fx, fy, fw, fh, gap = 16, 122, 488, 134, 8
    for i, feat in enumerate(FEATURES):
        draw_feature(d, fx + (i % 2) * (fw + gap),
                     fy + (i // 2) * (fh + gap), fw, fh, feat)

    # minis: 3 columns x 4 rows
    my = section_head(d, 16, 400, W - 32, "THE DAY IN BRIEF - 12 MORE STORIES")
    col_w = (W - 32 - 2 * 12) // 3
    for i, (num, text) in enumerate(MINIS):
        col, row = i % 3, i // 3
        draw_mini(d, 16 + col * (col_w + 12), my + row * 26, col_w,
                  num, text)

    # map + stats row
    draw_map(d, 16, 526, 496, 248)
    draw_stats_panel(d, 520, 526, 488, 248)

    # also-on list: 3 columns x 11 rows
    ay = section_head(d, 16, 778, W - 32, "ALSO ON 21 NOV - 33 MORE STORIES")
    for i, (num, text) in enumerate(ONELINERS):
        col, row = i % 3, i // 3
        draw_oneliner(d, 16 + col * (col_w + 12), ay + row * 18, col_w,
                      num, text)

    # footer
    d.line([16, 994, W - 16, 994], fill=RULE, width=1)
    d.text((16, 998), FOOT1, font=font(10), fill=INK)
    d.text((16, 1011), FOOT2, font=font(10), fill=GRAY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")

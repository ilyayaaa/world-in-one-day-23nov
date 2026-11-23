"""Draw 'The World in One Day: Monday 23 November 2026' as one 1024 x 1024 PNG.

All art (scenes, map, type) is drawn here with Pillow at 2x and scaled
down.  Facts come from wire and RSS items dated 23 November 2026 in at
least one time zone; every card names the outlet it came from.

    python3 tools/build.py            -> assets/entry.png
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "entry.png")
K = 2                      # supersampling
W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FACES = {
    "serif": "DejaVuSerif-Bold.ttf", "serifr": "DejaVuSerif.ttf",
    "serifi": "DejaVuSerif-Italic.ttf", "sans": "DejaVuSans.ttf",
    "sansb": "DejaVuSans-Bold.ttf", "cond": "DejaVuSansCondensed.ttf",
    "condb": "DejaVuSansCondensed-Bold.ttf",
}
_cache = {}


def F(face, px):
    key = (face, px)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_DIR + FACES[face], int(px * K))
    return _cache[key]


PAPER = (248, 243, 233)
INK = (20, 24, 38)
NAVY = (22, 34, 64)
RED = (176, 26, 34)
GREY = (98, 98, 102)
RULE = (202, 194, 180)
WHITE = (255, 255, 255)
CHIP = (18, 20, 30)

DAY = "Monday 23 November 2026"

# ------------------------------------------------------------------ data
LEADS = [
    dict(region="Europe", place="DYMER, KYIV REGION", topic="WAR",
         tag="UKRAINE: 11 DEAD", fig="Boy, 7, saved", chip="Rescuers",
         head="Russian strike brings down a block of flats near Kyiv",
         body="Eleven people are dead; a boy of seven was pulled out alive "
              "after 14 hours under the rubble.",
         outlet="BBC, Reuters", lat=50.8, lon=30.3, scene="rubble"),
    dict(region="Europe", place="ANTALYA, TURKEY", topic="CLIMATE",
         tag="COP31: NO DEAL", fig="+2 days", chip="Summit outcome",
         head="COP31 climate talks collapse with no deal",
         body="A row over naming fossil fuels sank the longest summit in "
              "COP history.",
         outlet="BBC, AP", lat=36.9, lon=30.7, scene="nodeal"),
    dict(region="Asia-Pacific", place="SEOUL, SOUTH KOREA", topic="MARKETS",
         tag="KOSPI: -5%", fig="AI sell-off", chip="Exchange data",
         head="AI bubble fears sink Asian stocks",
         body="Seoul vows to steady its market as Taiwan, China and Hong "
              "Kong fall too.",
         outlet="CNA, Al Jazeera", lat=37.6, lon=127.0, scene="kospi"),
]

CARDS = [
    dict(region="Asia-Pacific", place="CIKANDE, INDONESIA", tag="34 MISSING",
         chip="Police", head="24 killed in Indonesian candy factory fire",
         body="Search for workers resumes.", outlet="Al Jazeera, AP",
         lat=-6.2, lon=106.3, scene="factory"),
    dict(region="Africa", place="BENGHAZI, LIBYA", tag="WARSHIP SUNK",
         chip="Zelenskyy confirms", head="Ukraine says it sank a Russian warship",
         body="Sea drones hit it in Benghazi port.", outlet="AP, Reuters",
         lat=32.1, lon=20.1, scene="warship"),
    dict(region="Middle East", place="STRAIT OF HORMUZ", tag="TANKERS ABLAZE",
         chip="Iran navy claim", head="Iran says it set tankers on fire",
         body="IRGC warns of plots to stir unrest.", outlet="Al Jazeera",
         lat=26.6, lon=56.3, scene="tankers"),
    dict(region="Americas", place="WASHINGTON, US", tag="258 SEATS",
         chip="Race called", head="Democrats' biggest House win since 1992",
         body="A North Carolina recount decides it.", outlet="AP, BBC",
         lat=38.9, lon=-77.0, scene="capitol"),
    dict(region="Africa", place="KHARTOUM, SUDAN", tag="4 KILLED",
         chip="Local reports", head="Drones hit Khartoum and a UN building",
         body="At least nine more are hurt.", outlet="ABC",
         lat=15.6, lon=32.5, scene="drone"),
    dict(region="Africa", place="EASTERN DR CONGO", tag="EBOLA AT RISK",
         chip="WHO chief", head="Fighting near hospital disrupts Ebola effort",
         body="Outbreak still out of control.", outlet="Al Jazeera, Reuters",
         lat=0.5, lon=29.4, scene="ebola"),
    dict(region="Europe", place="BRUSSELS, BELGIUM", tag="AIRPORTS SHUT",
         chip="Air traffic body", head="National strike grounds Belgian flights",
         body="Unions march against austerity.", outlet="Al Jazeera",
         lat=50.85, lon=4.35, scene="airport"),
    dict(region="Middle East", place="JERUSALEM", tag="NO COALITION",
         chip="Party statement", head="Likud and Eisenkot end talks with no deal",
         body="Split over Ben-Gvir and the top job.", outlet="Al Jazeera, ST",
         lat=31.8, lon=35.2, scene="lecterns"),
    dict(region="Americas", place="IOWA, US", tag="4 TONNES",
         chip="US Army", head="Army to blow up lead azide despite court stay",
         body="It invokes emergency powers.", outlet="AP, Guardian",
         lat=40.8, lon=-91.2, scene="blast"),
    dict(region="World", place="MERCURY ORBIT", tag="IN ORBIT",
         chip="Space agencies", head="BepiColombo begins orbit of Mercury",
         body="A glitch is reported on arrival.", outlet="Reuters, ST",
         lat=None, lon=None, scene="mercury"),
]

ALSO = [
    ("Americas", "US", "ICE arrests at Seattle airport spark protests", "Guardian"),
    ("Americas", "US", "Spy chief backs Trump calling Putin 'friend'", "AP"),
    ("Americas", "US", "Delta system glitch delays Thanksgiving flights", "AP"),
    ("Americas", "US", "Trump hosts top holders of his meme coin", "Reuters"),
    ("Asia-Pacific", "Australia", "Molly Meldrum, Countdown host, dies at 83", "ABC"),
    ("Asia-Pacific", "Australia", "PBS medicines capped at $25 to 2030", "ABC"),
    ("Asia-Pacific", "Australia", "Jobless rate to top 5%, treasurer says", "Reuters"),
    ("Asia-Pacific", "India", "Tata Steel buys 26.4% of APL Apollo", "Reuters"),
    ("Americas", "US", "California sues OpenAI over model safety", "Reuters"),
    ("Europe", "Armenia", "New constitution offered for peace", "Reuters"),
    ("Europe", "UK", "Co-op Live arena evacuated after tear gas", "BBC"),
    ("Europe", "UK", "NHS starts world's largest AI breast-scan trial", "BBC"),
    ("Europe", "UK", "Burnham to sell 'landmark' EU deal to MPs", "BBC"),
    ("Middle East", "Gaza", "Study finds a 'toxic wasteland'", "Guardian"),
    ("Europe", "Poland", "Russia twice tried to kill a Ukrainian rapper", "AP"),
    ("Europe", "Italy", "Jeweller Paolo Bulgari dies aged 89", "BBC"),
    ("Middle East", "Iran", "Unveils a twin-missile launcher", "ST"),
    ("Middle East", "Lebanon", "Israeli forces keep demolishing homes", "Al Jazeera"),
    ("Middle East", "West Bank", "Eisenkot condemns settler arson", "Reuters"),
    ("Africa", "Zanzibar", "Fire tears through six hotels in Nungwi", "Al Jazeera"),
    ("World", "Markets", "Dollar near 19-month high; oil slips", "Reuters"),
    ("World", "AI", "OpenAI scientist proposes industry limits", "Reuters"),
]

NUMBERS = [
    ("11", "dead in the Dymer strike"),
    ("14", "hours a boy, 7, lay trapped"),
    ("+2", "days COP31 ran past its end"),
    ("-5%", "KOSPI fall in Seoul"),
    ("34", "workers missing in Indonesia"),
    ("258", "House seats for Democrats"),
]

REGIONS = ["Europe", "Middle East", "Africa", "Asia-Pacific", "Americas", "World"]
REGION_COL = {
    "Europe": (38, 68, 140), "Middle East": (176, 26, 34),
    "Africa": (124, 74, 38), "Asia-Pacific": (198, 118, 18),
    "Americas": (28, 118, 88), "World": (92, 60, 132),
}


# ------------------------------------------------------------ primitives
def p(v):
    return int(round(v * K))


def rect(b):
    return [p(b[0]), p(b[1]), p(b[2]), p(b[3])]


def put(d, xy, s, f, fill=INK, anchor="la"):
    d.text((p(xy[0]), p(xy[1])), s, font=f, fill=fill, anchor=anchor)


def width(s, f):
    return f.getlength(s) / K


def lines_for(s, f, w, n):
    out, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if width(trial, f) <= w:
            cur = trial
        else:
            out.append(cur)
            cur = word
    out.append(cur)
    if len(out) > n:
        raise ValueError("does not fit in %d lines: %r" % (n, s))
    return out


def block(d, x, y, s, f, w, n, lh, fill=INK):
    rows = lines_for(s, f, w, n)
    for i, r in enumerate(rows):
        put(d, (x, y + i * lh), r, f, fill)
    return y + len(rows) * lh


def tag(d, x, y, s, f, bg, fg=WHITE, pad=4):
    w = width(s, f)
    d.rectangle(rect([x, y, x + w + 2 * pad, y + f.size / K + 2 * pad - 1]), fill=bg)
    put(d, (x + pad, y + pad - 1), s, f, fg)
    return x + w + 2 * pad


# ---------------------------------------------------------- scene kit
def sky(img, top, bottom):
    w, h = img.size
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))


def halo(img, cx, cy, r, col, alpha=150):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (alpha,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r / 2)))


def fire(d, x, base, w, h, rnd):
    n = max(3, int(w / (h * 0.42)))
    for i in range(n):
        cx = x + w * (i + 0.5) / n
        hh = h * rnd.uniform(0.55, 1.0)
        hw = w / n * 0.78
        d.polygon([(cx - hw, base), (cx + rnd.uniform(-0.2, 0.2) * hw, base - hh), (cx + hw, base)],
                  fill=(232, 104, 28))
        d.polygon([(cx - hw * 0.5, base), (cx, base - hh * 0.58), (cx + hw * 0.5, base)],
                  fill=(252, 204, 64))


def plume(d, x, y, h, rnd, col=(74, 72, 80)):
    for i in range(8):
        r = h * (0.1 + 0.045 * i)
        cx = x + i * h * 0.1 + rnd.uniform(-2, 2) * K
        cy = y - i * h * 0.12
        d.ellipse([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], fill=col)


def figure(d, x, feet, s, body, head=(212, 168, 128), helmet=None):
    d.rounded_rectangle([x - s * 0.44, feet - s * 1.4, x + s * 0.44, feet], radius=s * 0.28, fill=body)
    d.ellipse([x - s * 0.31, feet - s * 2.02, x + s * 0.31, feet - s * 1.42], fill=head)
    if helmet:
        d.chord([x - s * 0.36, feet - s * 2.1, x + s * 0.36, feet - s * 1.6], 180, 360, fill=helmet)


def towers(d, w, base, rnd, col=(18, 22, 40), lit=(250, 208, 108), hmax=0.55, density=0.35):
    x = 0
    while x < w:
        bw = rnd.randint(int(w * 0.045), int(w * 0.095))
        bh = rnd.randint(int(base * 0.22), int(base * hmax))
        d.rectangle([x, base - bh, x + bw - 2 * K, base], fill=col)
        for wy in range(int(base - bh + 5 * K), int(base - 4 * K), int(6 * K)):
            for wx in range(int(x + 3 * K), int(x + bw - 5 * K), int(6 * K)):
                if rnd.random() < density:
                    d.rectangle([wx, wy, wx + 2 * K, wy + 2 * K], fill=lit)
        x += bw


def hull(d, x0, x1, waterline, h, col):
    d.polygon([(x0, waterline - h), (x1, waterline - h), (x1 - h * 0.6, waterline + h * 0.5),
               (x0 + h * 0.6, waterline + h * 0.5)], fill=col)


# ----------------------------------------------------------------- scenes
def sc_rubble(img, rnd):
    w, h = img.size
    sky(img, (40, 46, 72), (196, 150, 120))
    d = ImageDraw.Draw(img)
    base = h * 0.88
    towers(d, w, base, rnd, col=(60, 62, 80), lit=(220, 190, 120), hmax=0.42, density=0.2)
    # standing half of the block, one side sheared off
    d.polygon([(w * 0.08, base), (w * 0.08, h * 0.18), (w * 0.3, h * 0.18), (w * 0.33, h * 0.32),
               (w * 0.29, h * 0.45), (w * 0.34, h * 0.6), (w * 0.34, base)], fill=(176, 166, 150))
    for wy in range(int(h * 0.24), int(base - 8 * K), int(12 * K)):
        for wx in range(int(w * 0.1), int(w * 0.27), int(12 * K)):
            d.rectangle([wx, wy, wx + 6 * K, wy + 6 * K], fill=(52, 52, 64))
    # floor slabs hanging and the debris heap
    for i in range(4):
        y = h * (0.3 + i * 0.13)
        d.polygon([(w * 0.33, y), (w * 0.5, y + h * 0.1), (w * 0.49, y + h * 0.13), (w * 0.33, y + h * 0.03)],
                  fill=(150, 142, 130))
    heap = [(w * 0.3, base)]
    for i in range(14):
        heap.append((w * (0.32 + i * 0.045), base - h * rnd.uniform(0.12, 0.32)))
    heap.append((w * 0.98, base))
    d.polygon(heap, fill=(128, 118, 106))
    for _ in range(26):
        x, y = rnd.uniform(w * 0.33, w * 0.95), rnd.uniform(base - h * 0.25, base)
        d.rectangle([x, y, x + rnd.uniform(4, 10) * K, y + 3 * K], fill=(96, 88, 80))
    plume(d, w * 0.55, h * 0.45, h * 0.5, rnd, col=(118, 112, 116))
    d.rectangle([0, base, w, h], fill=(86, 76, 66))
    # rescuers, one lifting the child
    for i, x in enumerate((0.5, 0.62, 0.86)):
        figure(d, w * x, base - h * 0.2 + i * 2 * K, h * 0.13, (220, 120, 30), helmet=(250, 220, 40))
    figure(d, w * 0.74, base - h * 0.24, h * 0.13, (220, 120, 30), helmet=(250, 220, 40))
    figure(d, w * 0.74, base - h * 0.5, h * 0.07, (80, 130, 200))
    # torch beam
    d.polygon([(w * 0.62, base - h * 0.42), (w * 0.95, h * 0.22), (w * 0.98, h * 0.36)], fill=(250, 236, 180))


def sc_nodeal(img, rnd):
    w, h = img.size
    sky(img, (104, 170, 180), (220, 234, 224))
    d = ImageDraw.Draw(img)
    # hall back wall with the summit logo ring
    d.rectangle([0, h * 0.08, w, h * 0.62], fill=(70, 120, 120))
    cx, cy, r = w * 0.2, h * 0.34, h * 0.2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=4 * K)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=(60, 140, 90))
    # oil barrel with a crossed-out sign: the sticking point
    bx = w * 0.42
    d.rounded_rectangle([bx - 14 * K, h * 0.16, bx + 14 * K, h * 0.52], radius=4 * K, fill=(30, 30, 34))
    for yy in (0.26, 0.42):
        d.line([(bx - 14 * K, h * yy), (bx + 14 * K, h * yy)], fill=(120, 120, 130), width=2 * K)
    d.line([(bx - 22 * K, h * 0.12), (bx + 22 * K, h * 0.56)], fill=RED, width=5 * K)
    # long table, chairs left empty, papers scattered
    d.rectangle([w * 0.04, h * 0.62, w * 0.96, h * 0.72], fill=(126, 84, 52))
    d.rectangle([0, h * 0.84, w, h], fill=(150, 120, 90))
    for i in range(10):
        x = w * (0.08 + i * 0.09)
        d.rectangle([x, h * 0.48, x + 18 * K, h * 0.62], fill=(40, 52, 90) if i % 3 else (160, 50, 50))
        d.rectangle([x + 2 * K, h * 0.72, x + 5 * K, h * 0.84], fill=(80, 56, 36))
    for _ in range(9):
        x, y = rnd.uniform(w * 0.05, w * 0.95), rnd.uniform(h * 0.74, h * 0.95)
        a = rnd.uniform(-0.5, 0.5)
        pw, ph = 12 * K, 8 * K
        pts = [(x + math.cos(a) * dx - math.sin(a) * dy, y + math.sin(a) * dx + math.cos(a) * dy)
               for dx, dy in ((-pw, -ph), (pw, -ph), (pw, ph), (-pw, ph))]
        d.polygon(pts, fill=WHITE)
    # one delegate walking out on the right
    figure(d, w * 0.9, h * 0.84, h * 0.22, (40, 40, 50))
    d.rectangle([w * 0.93, h * 0.68, w * 0.97, h * 0.76], fill=(90, 60, 40))


def sc_kospi(img, rnd):
    w, h = img.size
    sky(img, (12, 16, 28), (28, 34, 52))
    d = ImageDraw.Draw(img)
    # ticker board
    d.rectangle([w * 0.03, h * 0.08, w * 0.97, h * 0.66], fill=(6, 8, 14))
    for r in range(4):
        for c in range(6):
            x = w * (0.05 + c * 0.155)
            y = h * (0.12 + r * 0.13)
            d.rectangle([x, y, x + w * 0.13, y + h * 0.1], fill=(40, 8, 12))
            bars = rnd.randint(2, 5)
            for b in range(bars):
                d.rectangle([x + 4 * K + b * 7 * K, y + 5 * K, x + 8 * K + b * 7 * K, y + h * 0.08],
                            fill=(236, 60, 60))
    # falling index line over the board
    pts = []
    v = h * 0.16
    for i in range(16):
        v += h * rnd.uniform(-0.01, 0.045)
        pts.append((w * (0.04 + i * 0.06), v))
    d.line(pts, fill=(255, 90, 80), width=4 * K)
    ex, ey = pts[-1]
    d.polygon([(ex + 6 * K, ey + 12 * K), (ex - 10 * K, ey + 2 * K), (ex + 4 * K, ey - 8 * K)], fill=(255, 90, 80))
    # traders with heads in hands
    d.rectangle([0, h * 0.8, w, h], fill=(36, 40, 56))
    for i in range(6):
        x = w * (0.1 + i * 0.16)
        figure(d, x, h * 0.92, h * 0.15, (30, 50, 90) if i % 2 else (60, 64, 76))
        d.rectangle([x - 18 * K, h * 0.8, x + 18 * K, h * 0.84], fill=(80, 84, 96))
        d.rectangle([x - 10 * K, h * 0.71, x + 10 * K, h * 0.8], fill=(90, 150, 220))


def sc_factory(img, rnd):
    w, h = img.size
    sky(img, (40, 24, 30), (200, 110, 60))
    d = ImageDraw.Draw(img)
    base = h * 0.84
    halo(img, w * 0.5, base - h * 0.2, h * 0.5, (255, 120, 40))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.1, h * 0.42, w * 0.9, base], fill=(70, 62, 60))
    for i in range(5):                          # saw-tooth roof
        x = w * (0.1 + i * 0.16)
        d.polygon([(x, h * 0.42), (x + w * 0.16, h * 0.42), (x + w * 0.16, h * 0.28)], fill=(90, 80, 76))
    d.rectangle([w * 0.78, h * 0.1, w * 0.84, h * 0.42], fill=(80, 70, 66))
    plume(d, w * 0.6, h * 0.3, h * 0.6, rnd, col=(50, 46, 50))
    fire(d, w * 0.14, h * 0.44, w * 0.6, h * 0.34, rnd)
    for i in range(6):
        d.rectangle([w * (0.14 + i * 0.12), h * 0.55, w * (0.2 + i * 0.12), h * 0.66], fill=(255, 170, 60))
    d.rectangle([0, base, w, h], fill=(60, 50, 44))
    for i in range(3):
        x = w * (0.08 + i * 0.05)
        figure(d, x, h * 0.96, h * 0.12, (230, 200, 40), helmet=(230, 60, 30))


def sc_warship(img, rnd):
    w, h = img.size
    sky(img, (26, 32, 54), (110, 104, 120))
    d = ImageDraw.Draw(img)
    sea = h * 0.66
    d.rectangle([0, sea, w, h], fill=(24, 50, 80))
    d.rectangle([w * 0.72, sea - 10 * K, w, sea + 4 * K], fill=(120, 116, 110))      # quay
    for i in range(3):
        d.rectangle([w * (0.8 + i * 0.06), sea - 40 * K, w * (0.82 + i * 0.06), sea - 10 * K], fill=(70, 70, 80))
    # tilted grey warship going down by the bow
    ship = Image.new("RGBA", (int(w * 0.72), int(h * 0.5)), (0, 0, 0, 0))
    sd = ImageDraw.Draw(ship)
    sw, sh = ship.size
    sd.polygon([(0, sh * 0.55), (sw, sh * 0.55), (sw * 0.92, sh * 0.9), (sw * 0.05, sh * 0.9)], fill=(110, 116, 124))
    sd.rectangle([sw * 0.35, sh * 0.3, sw * 0.62, sh * 0.55], fill=(130, 136, 144))
    sd.rectangle([sw * 0.47, sh * 0.08, sw * 0.5, sh * 0.3], fill=(90, 96, 104))
    sd.rectangle([sw * 0.12, sh * 0.47, sw * 0.24, sh * 0.55], fill=(96, 100, 108))
    ship = ship.rotate(-12, resample=Image.BICUBIC, expand=False)
    img.alpha_composite(ship, (int(w * 0.02), int(sea - sh * 0.72)))
    d = ImageDraw.Draw(img)
    d.rectangle([0, sea + 4 * K, w * 0.72, h], fill=(24, 50, 80))             # water over the bow
    for i in range(7):
        y = sea + 7 * K + i * 4 * K
        d.line([(rnd.uniform(0, w * 0.3), y), (rnd.uniform(w * 0.4, w * 0.7), y)], fill=(70, 100, 140), width=K)
    plume(d, w * 0.3, sea - 30 * K, h * 0.7, rnd)
    fire(d, w * 0.18, sea - 2 * K, w * 0.22, h * 0.2, rnd)


def sc_tankers(img, rnd):
    w, h = img.size
    sky(img, (40, 26, 50), (220, 120, 70))
    d = ImageDraw.Draw(img)
    sea = h * 0.7
    d.rectangle([0, sea, w, h], fill=(30, 46, 76))
    for x0, x1, s in ((0.04, 0.5, 9), (0.52, 0.97, 7)):
        hull(d, w * x0, w * x1, sea, s * K, (140, 34, 36))
        d.rectangle([w * (x1 - 0.1), sea - (s + 13) * K, w * (x1 - 0.04), sea - s * K], fill=(230, 230, 230))
        plume(d, w * (x0 + 0.1), sea - (s + 8) * K, h * 0.55, rnd, col=(40, 36, 40))
        fire(d, w * (x0 + 0.05), sea - s * K, w * 0.22, h * 0.24, rnd)
    for i in range(6):
        y = sea + 8 * K + i * 4 * K
        d.line([(rnd.uniform(0, w * 0.4), y), (rnd.uniform(w * 0.6, w), y)], fill=(230, 130, 60), width=K)


def sc_capitol(img, rnd):
    w, h = img.size
    sky(img, (120, 160, 210), (226, 232, 240))
    d = ImageDraw.Draw(img)
    cx, base = w * 0.5, h * 0.86
    d.rectangle([w * 0.12, h * 0.6, w * 0.88, base], fill=(238, 234, 224))
    for i in range(13):
        x = w * (0.15 + i * 0.056)
        d.rectangle([x, h * 0.64, x + 3 * K, base], fill=(206, 200, 188))
    d.rectangle([w * 0.34, h * 0.48, w * 0.66, h * 0.6], fill=(232, 228, 218))
    d.chord([w * 0.36, h * 0.2, w * 0.64, h * 0.76], 180, 360, fill=(244, 240, 232))
    d.rectangle([cx - 6 * K, h * 0.12, cx + 6 * K, h * 0.22], fill=(236, 232, 222))
    d.ellipse([cx - 3 * K, h * 0.07, cx + 3 * K, h * 0.13], fill=(236, 232, 222))
    d.rectangle([0, base, w, h], fill=(80, 130, 80))
    # seat bar: blue majority
    bx0, bx1, by = w * 0.06, w * 0.94, h * 0.92
    split = bx0 + (bx1 - bx0) * 258 / 435
    d.rectangle([bx0, by, split, by + 5 * K], fill=(40, 80, 180))
    d.rectangle([split, by, bx1, by + 5 * K], fill=(196, 40, 40))


def sc_drone(img, rnd):
    w, h = img.size
    sky(img, (200, 170, 120), (236, 214, 170))
    d = ImageDraw.Draw(img)
    base = h * 0.88
    towers(d, w, base, rnd, col=(150, 120, 90), lit=(110, 90, 70), hmax=0.4, density=0.25)
    d.rectangle([w * 0.56, h * 0.42, w * 0.8, base], fill=(74, 140, 210))         # UN-blue building
    put(d, (w * 0.68 / K, h * 0.55 / K), "UN", F("sansb", 13), WHITE, anchor="mm")
    plume(d, w * 0.6, h * 0.42, h * 0.5, rnd, col=(90, 84, 80))
    fire(d, w * 0.58, h * 0.44, w * 0.12, h * 0.16, rnd)
    # drone with four rotors
    dx, dy = w * 0.25, h * 0.24
    d.rectangle([dx - 14 * K, dy - 3 * K, dx + 14 * K, dy + 3 * K], fill=(30, 30, 30))
    for ox in (-16, 16):
        d.line([(dx + ox * K - 7 * K, dy - 5 * K), (dx + ox * K + 7 * K, dy - 5 * K)], fill=(30, 30, 30), width=2 * K)
    d.line([(dx, dy + 3 * K), (w * 0.6, h * 0.42)], fill=(250, 240, 220), width=K)
    d.rectangle([0, base, w, h], fill=(170, 140, 100))


def sc_ebola(img, rnd):
    w, h = img.size
    sky(img, (150, 190, 160), (220, 230, 200))
    d = ImageDraw.Draw(img)
    for i in range(5):                                   # forest edge
        x = w * (0.02 + i * 0.1)
        d.ellipse([x - 10 * K, h * 0.12, x + 26 * K, h * 0.6], fill=(40, 100, 50))
    d.polygon([(w * 0.4, h * 0.8), (w * 0.6, h * 0.3), (w * 0.95, h * 0.3), (w * 0.98, h * 0.8)], fill=WHITE)
    cx, cy = w * 0.76, h * 0.5
    d.rectangle([cx - 4 * K, cy - 11 * K, cx + 4 * K, cy + 11 * K], fill=RED)
    d.rectangle([cx - 11 * K, cy - 4 * K, cx + 11 * K, cy + 4 * K], fill=RED)
    d.rectangle([0, h * 0.8, w, h], fill=(130, 100, 70))
    for x in (0.12, 0.24, 0.36):
        figure(d, w * x, h * 0.94, h * 0.16, (236, 240, 244), head=(250, 250, 250))
        d.rectangle([w * x - 5 * K, h * 0.94 - h * 0.31, w * x + 5 * K, h * 0.94 - h * 0.28], fill=(60, 140, 200))
    plume(d, w * 0.08, h * 0.3, h * 0.35, rnd, col=(110, 110, 110))


def sc_airport(img, rnd):
    w, h = img.size
    sky(img, (170, 190, 210), (226, 230, 236))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.72, w, h], fill=(110, 112, 116))
    d.rectangle([w * 0.06, h * 0.25, w * 0.12, h * 0.72], fill=(200, 200, 205))      # control tower
    d.rectangle([w * 0.02, h * 0.15, w * 0.16, h * 0.27], fill=(60, 100, 140))
    d.line([(w * 0.03, h * 0.16), (w * 0.15, h * 0.26)], fill=RED, width=3 * K)
    d.line([(w * 0.15, h * 0.16), (w * 0.03, h * 0.26)], fill=RED, width=3 * K)
    for i in range(3):                                   # parked jets, nose to the gate
        x, y = w * (0.28 + i * 0.24), h * 0.66
        d.rounded_rectangle([x, y - 6 * K, x + w * 0.2, y + 4 * K], radius=5 * K, fill=WHITE)
        d.polygon([(x + w * 0.08, y), (x + w * 0.13, y), (x + w * 0.09, y + 14 * K)], fill=(220, 224, 230))
        d.polygon([(x + w * 0.17, y - 6 * K), (x + w * 0.2, y - 18 * K), (x + w * 0.2, y - 6 * K)], fill=(40, 70, 150))
    # pickets with banners
    for i in range(4):
        x = w * (0.3 + i * 0.17)
        figure(d, x, h * 0.95, h * 0.12, (200, 40, 40))
        d.rectangle([x - 8 * K, h * 0.68, x + 8 * K, h * 0.75], fill=(250, 220, 60))


def sc_lecterns(img, rnd):
    w, h = img.size
    sky(img, (206, 214, 232), (240, 236, 228))
    d = ImageDraw.Draw(img)
    d.rectangle([w * 0.04, h * 0.28, w * 0.96, h * 0.84], fill=(224, 212, 184))
    for i in range(9):
        d.rectangle([w * (0.08 + i * 0.1), h * 0.34, w * (0.08 + i * 0.1) + 6 * K, h * 0.84], fill=(204, 188, 154))
    d.rectangle([0, h * 0.84, w, h], fill=(150, 140, 120))
    for x, col in ((0.34, (30, 40, 70)), (0.66, (60, 60, 72))):
        figure(d, w * x, h * 0.84, h * 0.24, col)
        d.rectangle([w * (x - 0.07), h * 0.62, w * (x + 0.07), h * 0.84], fill=(108, 78, 48))
    d.line([(w * 0.5, h * 0.5), (w * 0.5, h * 0.84)], fill=RED, width=2 * K)          # the split
    d.line([(w * 0.87, h * 0.84), (w * 0.87, h * 0.18)], fill=INK, width=K)
    d.rectangle([w * 0.87, h * 0.18, w * 0.98, h * 0.4], fill=WHITE)
    d.rectangle([w * 0.87, h * 0.21, w * 0.98, h * 0.24], fill=(30, 70, 170))
    d.rectangle([w * 0.87, h * 0.34, w * 0.98, h * 0.37], fill=(30, 70, 170))


def sc_blast(img, rnd):
    w, h = img.size
    sky(img, (150, 170, 190), (220, 224, 210))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h * 0.7, w, h], fill=(150, 140, 90))
    for i in range(3):                                   # earth-covered bunkers
        x = w * (0.08 + i * 0.22)
        d.chord([x, h * 0.48, x + w * 0.2, h * 0.92], 180, 360, fill=(100, 120, 70))
        d.rectangle([x + w * 0.08, h * 0.6, x + w * 0.12, h * 0.7], fill=(60, 60, 64))
    # warning sign
    sx, sy = w * 0.84, h * 0.3
    d.polygon([(sx, sy - 16 * K), (sx + 16 * K, sy + 12 * K), (sx - 16 * K, sy + 12 * K)], fill=(250, 200, 30),
              outline=INK)
    d.rectangle([sx - 1.5 * K, sy - 6 * K, sx + 1.5 * K, sy + 4 * K], fill=INK)
    d.ellipse([sx - 1.5 * K, sy + 6 * K, sx + 1.5 * K, sy + 9 * K], fill=INK)
    d.line([(sx, sy + 12 * K), (sx, h * 0.7)], fill=(80, 80, 80), width=2 * K)
    # gavel over a court order sheet
    d.rectangle([w * 0.7, h * 0.76, w * 0.84, h * 0.94], fill=WHITE)
    for k in range(4):
        d.line([(w * 0.71, h * (0.8 + k * 0.035)), (w * 0.83, h * (0.8 + k * 0.035))], fill=GREY, width=K)
    d.line([(w * 0.86, h * 0.7), (w * 0.95, h * 0.88)], fill=(110, 70, 40), width=3 * K)
    d.rounded_rectangle([w * 0.82, h * 0.64, w * 0.92, h * 0.74], radius=3 * K, fill=(110, 70, 40))


def sc_mercury(img, rnd):
    w, h = img.size
    sky(img, (4, 6, 16), (18, 20, 40))
    d = ImageDraw.Draw(img)
    for _ in range(70):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        d.ellipse([x, y, x + 1.4 * K, y + 1.4 * K], fill=(220, 220, 240))
    halo(img, w * 0.02, h * 0.1, h * 0.5, (255, 230, 160), alpha=120)        # the near Sun
    d = ImageDraw.Draw(img)
    cx, cy, r = w * 0.32, h * 0.62, h * 0.5
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 140, 132))
    for _ in range(14):
        a, rr = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, r * 0.8)
        x, y, s = cx + math.cos(a) * rr, cy + math.sin(a) * rr, rnd.uniform(4, 12) * K
        d.ellipse([x - s, y - s * 0.8, x + s, y + s * 0.8], fill=(118, 110, 104))
    d.chord([cx - r, cy - r, cx + r, cy + r], 300, 120, fill=(90, 84, 80))
    d.arc([w * 0.1, h * 0.2, w * 0.95, h * 0.95], 200, 340, fill=(140, 180, 240), width=K)
    sx, sy = w * 0.78, h * 0.3                            # spacecraft with panels
    d.rectangle([sx - 6 * K, sy - 6 * K, sx + 6 * K, sy + 6 * K], fill=(220, 190, 90))
    d.rectangle([sx - 26 * K, sy - 3 * K, sx - 7 * K, sy + 3 * K], fill=(50, 80, 170))
    d.rectangle([sx + 7 * K, sy - 3 * K, sx + 26 * K, sy + 3 * K], fill=(50, 80, 170))


SCENES = {n[3:]: f for n, f in globals().items() if n.startswith("sc_")}


def paint(canvas, b, name, seed):
    x0, y0, x1, y1 = rect(b)
    tile = Image.new("RGBA", (x1 - x0, y1 - y0), PAPER + (255,))
    SCENES[name](tile, random.Random(seed))
    canvas.alpha_composite(tile, (x0, y0))


# -------------------------------------------------------------------- map
LAND = [
    [(-168, 66), (-140, 70), (-95, 72), (-80, 64), (-60, 58), (-55, 48), (-70, 42), (-80, 30), (-82, 25),
     (-97, 18), (-88, 15), (-80, 8), (-92, 14), (-105, 20), (-117, 32), (-124, 42), (-124, 49), (-135, 58),
     (-152, 58), (-165, 60)],
    [(-78, 9), (-60, 10), (-50, 0), (-35, -6), (-39, -15), (-48, -26), (-58, -36), (-65, -42), (-70, -54),
     (-74, -42), (-71, -20), (-81, -5), (-78, 2)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (5, 51), (8, 55), (12, 57), (5, 61), (14, 68), (25, 71),
     (40, 68), (60, 70), (80, 73), (110, 76), (140, 72), (170, 68), (178, 64), (160, 60), (142, 52),
     (135, 43), (128, 35), (121, 30), (120, 22), (108, 20), (106, 10), (100, 5), (98, 15), (92, 22),
     (80, 13), (77, 8), (72, 20), (66, 25), (57, 25), (56, 18), (44, 12), (35, 28), (34, 32), (28, 37),
     (24, 38), (20, 40), (16, 38), (12, 44), (6, 43), (0, 39)],
    [(-17, 15), (-16, 22), (-9, 31), (-5, 36), (10, 37), (20, 32), (32, 31), (34, 28), (43, 12), (51, 12),
     (40, -2), (40, -15), (35, -25), (20, -35), (17, -29), (12, -17), (13, -5), (9, 4), (-8, 4), (-15, 10)],
    [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37),
     (141, -38), (131, -31), (115, -34)],
    [(95, 5), (105, -6), (120, -8), (141, -3), (150, -6), (140, -9), (125, -10), (108, -8)],
    [(130, 31), (135, 34), (140, 36), (142, 42), (140, 45), (137, 37)],
    [(-5, 50), (2, 52), (0, 58), (-6, 58)],
]


def world_map(canvas, b, pins):
    x0, y0, x1, y1 = b
    d = ImageDraw.Draw(canvas)
    d.rectangle(rect(b), fill=(230, 237, 240))
    lon0, lon1, lat0, lat1 = -170, 180, 78, -48

    def xy(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0), y0 + (lat - lat0) / (lat1 - lat0) * (y1 - y0))

    mask = Image.new("L", canvas.size, 0)
    md = ImageDraw.Draw(mask)
    for poly in LAND:
        md.polygon([tuple(p(v) for v in xy(*q)) for q in poly], fill=255)
    yy = y0 + 2
    while yy < y1:
        xx = x0 + 2
        while xx < x1:
            if mask.getpixel((p(xx), p(yy))):
                d.ellipse(rect([xx - 1.4, yy - 1.4, xx + 1.4, yy + 1.4]), fill=(178, 162, 132))
            xx += 5
        yy += 5
    f = F("condb", 9)
    used = []
    for n, lat, lon in pins:
        px, py = xy(lon, lat)
        for qx, qy in used:
            if abs(qx - px) < 11 and abs(qy - py) < 11:
                py += 11
        used.append((px, py))
        d.ellipse(rect([px - 6.5, py - 6.5, px + 6.5, py + 6.5]), fill=RED, outline=WHITE, width=K)
        put(d, (px, py + 0.5), str(n), f, WHITE, anchor="mm")


# ------------------------------------------------------------------- page
def build():
    img = Image.new("RGBA", (W * K, H * K), PAPER + (255,))
    d = ImageDraw.Draw(img)
    M = 12
    all_regions = [s["region"] for s in LEADS + CARDS] + [a[0] for a in ALSO]
    counts = {r: all_regions.count(r) for r in REGIONS}
    total = len(all_regions)
    active = [r for r in REGIONS if counts[r]]

    d.rectangle(rect([0, 0, W, 20]), fill=NAVY)
    put(d, (M, 4), "THE WORLD IN ONE DAY", F("sansb", 10.5), WHITE)
    put(d, (W - M, 4), "%d STORIES  ·  %d REGIONS  ·  EVERY ONE DATED %s" % (total, len(active), DAY.upper()),
        F("sansb", 10.5), WHITE, anchor="ra")

    put(d, (W / 2, 24), DAY, F("serif", 60), INK, anchor="ma")
    put(d, (W / 2, 96), "Russian strike kills 11 near Kyiv  ·  COP31 collapses with no deal  ·  "
        "AI fears sink Asian stocks", F("serifi", 14.5), RED, anchor="ma")
    d.line(rect([M, 118, W - M, 118]), fill=INK, width=K)

    cw = (W - 2 * M) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = M + i * cw
        if i:
            d.line(rect([x, 124, x, 158]), fill=RULE, width=K)
        put(d, (x + 8, 121), num, F("serif", 24), RED)
        if width(lab, F("cond", 10)) > cw - 12:
            raise ValueError("number label too long: " + lab)
        put(d, (x + 8, 150), lab, F("cond", 10), GREY)
    d.line(rect([M, 164, W - M, 164]), fill=RULE, width=K)

    x = M
    min_w = 70
    spare = (W - 2 * M) - min_w * len(active)
    for r in active:
        ww = min_w + spare * counts[r] / total
        d.rectangle(rect([x, 168, x + ww - 2, 184]), fill=REGION_COL[r])
        put(d, (x + ww / 2, 176), "%s %d" % (r.upper(), counts[r]), F("condb", 10), WHITE, anchor="mm")
        x += ww

    widths = [384, 300, 300]
    x, top, ph = M, 192, 124
    for i, s in enumerate(LEADS):
        wv = widths[i]
        paint(img, [x, top, x + wv, top + ph], s["scene"], 300 + i)
        d = ImageDraw.Draw(img)
        tag(d, x + 6, top + 6, s["tag"], F("condb", 12 if i == 0 else 11), RED)
        if i == 0:
            tag(d, x + 6, top + 27, "TOP STORY", F("condb", 9), INK)
        fw = width(s["fig"], F("serif", 13)) + 10
        d.rectangle(rect([x + wv - fw - 6, top + 6, x + wv - 6, top + 26]), fill=WHITE, outline=INK, width=K)
        put(d, (x + wv - 6 - fw / 2, top + 16), s["fig"], F("serif", 13), INK, anchor="mm")
        tag(d, x + 6, top + ph - 21, s["chip"], F("cond", 9.5), CHIP)
        y = top + ph + 6
        put(d, (x, y), "%d  %s · %s" % (i + 1, s["place"], s["topic"]), F("condb", 10), RED)
        y += 14
        y = block(d, x, y, s["head"], F("serif", 19 if i == 0 else 17), wv, 2, 22 if i == 0 else 20)
        y += 2
        if y + 27 > 410:
            raise ValueError("lead %d runs into the cards" % (i + 1))
        block(d, x, y, s["body"] + " (" + s["outlet"] + ")", F("sans", 10.5), wv, 2, 13.5, (50, 50, 56))
        x += wv + 8

    cw = (W - 2 * M - 4 * 8) / 5
    for k, s in enumerate(CARDS):
        row, col = divmod(k, 5)
        x, y = M + col * (cw + 8), 412 + row * 142
        d = ImageDraw.Draw(img)
        d.rectangle(rect([x, y, x + cw, y + 136]), fill=(252, 249, 242), outline=RULE, width=K)
        paint(img, [x + 1, y + 1, x + cw - 1, y + 62], s["scene"], 400 + k)
        d = ImageDraw.Draw(img)
        tag(d, x + 5, y + 5, s["tag"], F("condb", 9.5), RED, pad=3)
        tag(d, x + 5, y + 44, s["chip"], F("cond", 8.5), CHIP, pad=3)
        d.ellipse(rect([x + cw - 20, y + 4, x + cw - 4, y + 20]), fill=WHITE, outline=INK, width=K)
        put(d, (x + cw - 12, y + 12.5), str(k + 4), F("condb", 9), INK, anchor="mm")
        put(d, (x + 6, y + 67), s["place"], F("condb", 8.5), RED)
        block(d, x + 6, y + 79, s["head"], F("serif", 12.5), cw - 12, 2, 15)
        block(d, x + 6, y + 110, s["body"] + " (" + s["outlet"] + ")", F("cond", 9.5), cw - 12, 2, 11.5,
              (50, 50, 56))

    top = 702
    d = ImageDraw.Draw(img)
    put(d, (M, top), "WHERE IT HAPPENED", F("sansb", 11), INK)
    put(d, (M + 140, top + 1.5), "pins match story numbers", F("cond", 9), GREY)
    pins = [(i + 1, s["lat"], s["lon"]) for i, s in enumerate(LEADS + CARDS) if s["lat"] is not None]
    world_map(img, [M, top + 16, M + 372, top + 200], pins)

    d = ImageDraw.Draw(img)
    lx = M + 384
    put(d, (lx, top), "ALSO ON MONDAY 23 NOVEMBER — %d MORE STORIES" % len(ALSO), F("sansb", 11), INK)
    d.line(rect([lx, top + 15, W - M, top + 15]), fill=INK, width=K)
    colw = (W - M - lx) / 2
    for i, (_, where, what, src) in enumerate(ALSO):
        c, r = divmod(i, 11)
        x, y = lx + c * (colw + 6), top + 21 + r * 16.4
        put(d, (x, y), str(i + 14), F("condb", 10), RED)
        put(d, (x + 18, y), where + ":", F("condb", 10), INK)
        x3 = x + 18 + width(where + ": ", F("condb", 10))
        line = what + " (" + src + ")"
        if x3 + width(line, F("cond", 10)) > x + colw - 4:
            raise ValueError("also item too long: " + line)
        put(d, (x3, y), line, F("cond", 10), (40, 40, 46))

    top = 908
    d.rectangle(rect([M, top, W - M, top + 54]), outline=RED, width=2 * K, fill=(252, 240, 236))
    put(d, (M + 8, top + 6), "DATE CHECK", F("sansb", 10.5), RED)
    dc = ("Wires read up to 08:05 UTC, Monday 23 November 2026; every story here was reported or still developing "
          "on 23 November in at least one time zone. Left out as other days' news: the Strathmore, California "
          "concert shooting (21 Nov), the UK-EU deal itself (agreed Friday 20 Nov) and weekend sport results.")
    block(d, M + 8, top + 20, dc, F("cond", 10), W - 2 * M - 16, 3, 11.5, INK)

    foot = ("Sources: Reuters, AP, BBC, Al Jazeera, The Guardian, The Straits Times, CNA, ABC Australia. "
            "Every story names its outlet. Pictures and map: original, drawn in code.")
    block(d, M, 970, foot, F("cond", 9.5), W - 2 * M, 2, 12, GREY)
    d.line(rect([M, 1004, W - M, 1004]), fill=RULE, width=K)
    put(d, (M, 1008), "THE WORLD IN ONE DAY", F("condb", 9), INK)
    put(d, (W - M, 1008), "MONDAY 23 NOVEMBER 2026  ·  ONE PAGE", F("condb", 9), INK, anchor="ra")

    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.save(OUT, optimize=True)
    return OUT


if __name__ == "__main__":
    print(build())

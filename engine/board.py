#!/usr/bin/env python3
"""2350: the core board library (projection, glow fields, text), first written for season 1's boards.

  python3 board.py <base_global.jpg> <out_dir> [era ...|summary]

Geography: base_global_v1.jpg fitted to real lon/lat (calib.json), plus a
thin-plate-spline correction (warp_src/dst.npy) so places land on the coastlines
as drawn. Everything shown comes from playtest 1's record (23 Oct 2026).
"""
import json, math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import gaussian_filter

HERE = Path(__file__).resolve().parent
FONTS = HERE / 'fonts'
GEO = HERE / 'data'

cal = json.loads((HERE / 'calib.json').read_text())
_src, _dst = np.load(HERE / 'warp_src.npy'), np.load(HERE / 'warp_dst.npy')
_rbf = RBFInterpolator(_src, _dst - _src, kernel='thin_plate_spline', smoothing=200.0)
WX0, WY0, WF = 4300, 1050, 2

OUT_W, OUT_H = 2560, 1440
BX0 = cal['a'] * 80 + cal['b']
BX1 = cal['a'] * 183 + cal['b']
BY0 = cal['c'] * 10.5 + cal['d']
SC = OUT_W / (BX1 - BX0)
BY1 = BY0 + OUT_H / SC


def geo_out(pts):
    a = np.atleast_2d(np.asarray(pts, float))
    x = cal['a'] * a[:, 0] + cal['b']
    y = cal['c'] * a[:, 1] + cal['d']
    q = np.stack([(x - WX0) / WF, (y - WY0) / WF], 1)
    d = _rbf(q) * WF
    return np.stack([(x + d[:, 0] - BX0) * SC, (y + d[:, 1] - BY0) * SC], 1)


def P(lon, lat):
    x, y = geo_out([(lon, lat)])[0]
    return float(x), float(y)


# ---------------------------------------------------------------- colours
OC = np.array([255, 186, 64])      # Oceania: gold
AS = np.array([196, 104, 255])     # Asia: violet
GREY = np.array([150, 165, 180])
WHITE = np.array([235, 246, 255])
HEAT = np.array([255, 92, 40])
CYAN = (70, 205, 235)
INK = (215, 240, 250)
DIM = (120, 170, 190)

def font(name, size):
    return ImageFont.truetype(str(FONTS / f'{name}.ttf'), size)

F_TITLE = font('Rajdhani-700', 50)
F_H2 = font('Rajdhani-700', 30)
F_H3 = font('Rajdhani-600', 22)
F_LAB = font('Rajdhani-700', 24)
F_SM = font('Rajdhani-600', 18)
F_MONO = font('ShareTechMono', 17)
F_MONO_L = font('ShareTechMono', 22)

# ---------------------------------------------------------------- the season
ERAS = [
    ('I', '2120–2150', 'THE GATE', "Asia's ore must come through Darwin", None),
    ('II', '2150–2180', 'CONTACT', 'A firewalled link, and the Unfinished', None),
    ('III', '2210–2240', 'THE TORRES LINE', 'Strait closed; Sydney cools itself', None),
    ('IV', '2240–2270', 'COOLING FOR MEMBRANES', 'A deal made in the drought', 'LONG EL NIÑO'),
    ('V', '2270–2300', 'THE REEF IS TAKEN', 'Boarded without a shot', 'CORAL SEA COLLAPSE'),
    ('VI', '2300–2330', 'THE REEF GATE', "Asia's traffic pays at the gate", 'HEAT SPIKE'),
    ('VII', '2330–2350', 'THE ATOLLS COME TO THE CAPE', 'Every byte through the gate, read', 'ANTARCTIC PULSE'),
]
# what the rival depends on you for, counted from the record
HOOKS_OC = [2, 2, 3, 4, 4, 4, 3]
HOOKS_AS = [0, 1, 0, 1, 1, 1, 1]
# influence (game master's reading of the story), (Oceania %, Asia %) or None = unheld
CONTEST = {
    'STRAIT': [None, None, (100, 0), (100, 0), (100, 0), (85, 15), (90, 10)],
    'DARWIN': [(85, 15), (75, 25), (80, 20), (80, 20), (80, 20), (80, 20), (80, 20)],
    'NG SOUTH': [None, (0, 100), (0, 100), (25, 75), (25, 75), (35, 65), (30, 70)],
}
THROUGH_OC = [
    ['ORE TO ASIA · DARWIN', 'ASIA CABLE LANDING', 'ISLANDS NETWORK'],
    ['ORE · DOWN A THIRD', 'DARWIN LINK · FIREWALLED', 'ISLANDS NETWORK'],
    ['ORE TO ASIA', 'DARWIN LINK', 'TORRES STRAIT · CLOSED', 'ISLANDS NETWORK'],
    ['NICKEL · LITHIUM ENDS 2255', 'COOLING TO ASIA', 'DARWIN LINK', 'TORRES STRAIT', 'ISLANDS NETWORK'],
    ['NICKEL', 'COOLING TO ASIA', 'DARWIN LINK', 'THE REEF · TAKEN', 'ISLANDS · FED'],
    ['NICKEL', 'COOLING TO ASIA', 'DARWIN LINK', 'REEF GATE · TOLL', 'ISLANDS NETWORK'],
    ['NICKEL', 'REEF GATE · TAPPED', 'DARWIN LINK', 'ISLANDS NETWORK', 'ATOLL PEOPLES · CAPE'],
]
THROUGH_AS = [
    ['NOTHING YET'],
    ['COOLING PLANT · UNFINISHED', 'NEW GUINEA GRID'],
    ['NEW GUINEA GRID', 'PAPUA COPPER', 'COOLING PARTS · CUT'],
    ['MEMBRANES', 'NEW GUINEA GRID', 'OWN LITHIUM · 2255'],
    ['MEMBRANES', 'NEW GUINEA GRID'],
    ['MEMBRANES', 'NEW GUINEA GRID', 'COOLING · COPIED'],
    ['MEMBRANES', 'NEW GUINEA · SELF-RULE 2345', 'OWN COOLING · 2340'],
]

PL = dict(
    sydney=(151.21, -33.87), highlands=(150.41, -34.48), darwin=(130.84, -12.46),
    hedland=(118.60, -20.31), reef=(142.35, -9.95), capetip=(142.53, -10.69),
    cape=(142.9, -13.6), moresby=(147.18, -9.44), copper=(137.11, -4.06),
    java=(110.4, -7.0), honiara=(159.95, -9.43), vila=(168.32, -17.73),
    noumea=(166.45, -22.27), suva=(178.44, -18.14), funafuti=(179.19, -8.52),
    tarawa=(173.0, 1.45), majuro=(171.38, 7.09), coral=(152.0, -15.5),
)
RAIL = [(118.6, -20.31), (122.2, -17.96), (125.6, -18.2), (128.74, -15.77), (132.26, -14.47), (130.84, -12.46)]
DESAL = [(145.78, -16.92), (146.82, -19.26), (149.18, -21.14), (150.5, -23.38), (152.35, -24.87), (153.1, -27.47),
         (153.11, -30.3), (152.91, -31.43), (151.78, -32.93), (150.89, -34.42), (149.91, -37.07)]
ATOLL_TOWNS = [(143.35, -12.79), (144.1, -14.3), (145.25, -15.47)]

# ---------------------------------------------------------------- geometry
def load_groups():
    g = json.loads((GEO / 'countries-50m.geojson').read_text())
    oce = {'Australia', 'Solomon Is.', 'Vanuatu', 'New Caledonia', 'Fiji'}
    asia = {'Indonesia', 'Malaysia', 'Philippines', 'Timor-Leste', 'Brunei', 'Singapore', 'Thailand', 'Vietnam',
            'Cambodia', 'Laos', 'Myanmar', 'Sri Lanka', 'India', 'Bangladesh', 'China', 'Taiwan'}
    groups = {'oce': [], 'asia': [], 'ng': [], 'aus': []}
    for f in g['features']:
        name = f['properties']['name']
        gm = f['geometry']
        polys = gm['coordinates'] if gm['type'] == 'MultiPolygon' else [gm['coordinates']]
        for p in polys:
            ring = [(lo, la) for lo, la in p[0] if lo > 60]
            if len(ring) < 3:
                continue
            clon = sum(lo for lo, _ in ring) / len(ring)
            if name == 'Papua New Guinea' or (name == 'Indonesia' and clon > 134):
                groups['ng'].append(ring)
            elif name in oce:
                groups['oce'].append(ring)
                if name == 'Australia':
                    groups['aus'].append(ring)
            elif name in asia:
                groups['asia'].append(ring)
    return groups


def poly_mask(rings, blur=0):
    m = Image.new('L', (OUT_W, OUT_H), 0)
    d = ImageDraw.Draw(m)
    for r in rings:
        pts = geo_out(r)
        if (pts[:, 0].max() < -50 or pts[:, 0].min() > OUT_W + 50 or pts[:, 1].max() < -50 or pts[:, 1].min() > OUT_H + 50):
            continue
        d.polygon([tuple(p) for p in pts], fill=255)
    a = np.asarray(m).astype(np.float32) / 255
    return gaussian_filter(a, blur) if blur else a


def lonlat_grid():
    ys, xs = np.mgrid[0:OUT_H, 0:OUT_W].astype(np.float32)
    lon = (xs / SC + BX0 - cal['b']) / cal['a']
    lat = (ys / SC + BY0 - cal['d']) / cal['c']
    return lon, lat


def bezier(p0, p1, bend=0.2, n=90):
    p0, p1 = np.array(p0), np.array(p1)
    mid = (p0 + p1) / 2
    v = p1 - p0
    perp = np.array([-v[1], v[0]])
    c = mid + perp * bend
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1


def polyline_len(pts):
    return np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]


def resample(pts, step):
    L = polyline_len(pts)
    s = np.arange(0, L[-1], step)
    return np.stack([np.interp(s, L, pts[:, 0]), np.interp(s, L, pts[:, 1])], 1)


# ---------------------------------------------------------------- layers
class Board:
    def __init__(self, base):
        self.base = base
        self.light = Image.new('RGB', (OUT_W, OUT_H))   # additive, gets glow
        self.ld = ImageDraw.Draw(self.light)
        self.ui = Image.new('RGBA', (OUT_W, OUT_H), (0, 0, 0, 0))  # panels and text, no glow
        self.ud = ImageDraw.Draw(self.ui)
        self.fields = np.zeros((OUT_H, OUT_W, 3), np.float32)

    # map light
    def line(self, pts, col, w=3, dash=None, chevrons=False):
        pts = np.asarray(pts, float)
        col = tuple(int(c) for c in col)
        if dash:
            seg = resample(pts, 2)
            on, off = dash
            L = polyline_len(seg)
            cyc = on + off
            for i in range(len(seg) - 1):
                if (L[i] % cyc) < on:
                    self.ld.line([tuple(seg[i]), tuple(seg[i + 1])], fill=col, width=w)
        else:
            self.ld.line([tuple(p) for p in pts], fill=col, width=w, joint='curve')
        if chevrons:
            seg = resample(pts, 4)
            L = polyline_len(seg)
            for s0 in np.arange(40, L[-1] - 20, 70):
                i = int(np.searchsorted(L, s0))
                if i < 2 or i >= len(seg) - 2:
                    continue
                d = seg[i + 1] - seg[i - 1]
                d /= (np.hypot(*d) + 1e-6)
                nrm = np.array([-d[1], d[0]])
                tip = seg[i] + d * 7
                a = tip - d * 11 + nrm * 7
                b = tip - d * 11 - nrm * 7
                self.ld.line([tuple(a), tuple(tip), tuple(b)], fill=col, width=max(2, w - 1))

    def ring(self, xy, r, col, w=2):
        x, y = xy
        self.ld.ellipse([x - r, y - r, x + r, y + r], outline=tuple(int(c) for c in col), width=w)

    def dot(self, xy, r, col):
        x, y = xy
        self.ld.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(c) for c in col))

    def hexagon(self, xy, r, col, w=3, fill=None):
        x, y = xy
        pts = [(x + r * math.cos(math.pi / 6 + k * math.pi / 3), y + r * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
        if fill is not None:
            self.ld.polygon(pts, fill=tuple(int(c) for c in fill))
        self.ld.polygon(pts, outline=tuple(int(c) for c in col), width=w)

    def square(self, xy, r, col):
        x, y = xy
        self.ld.rectangle([x - r, y - r, x + r, y + r], outline=tuple(int(c) for c in col), width=2)
        self.ld.rectangle([x - 2, y - 2, x + 2, y + 2], fill=tuple(int(c) for c in col))

    def field(self, mask, col, strength=1.0, glow=30):
        g = gaussian_filter(mask, glow)
        sm = gaussian_filter(mask, 1.6)
        gy, gx = np.gradient(sm)
        edge = np.clip(np.hypot(gx, gy) * 5.0, 0, 1)
        self.fields += (mask[..., None] * 0.05 + g[..., None] * 0.07 + edge[..., None] * 0.55) * (col / 255.0) * strength

    # text
    def text(self, xy, s, f, col=INK, anchor='la', stroke=3):
        col = tuple(int(c) for c in col)
        if len(col) == 3:
            col = col + (255,)
        self.ud.text((float(xy[0]), float(xy[1])), s, font=f, fill=col, anchor=anchor,
                     stroke_width=stroke, stroke_fill=(4, 10, 18, 235))

    def tag(self, node, s, offset, col, sub=None, new=False):
        x, y = node
        tx, ty = x + offset[0], y + offset[1]
        colt = tuple(int(c) for c in col)
        self.ud.line([(x, y), (tx, ty)], fill=colt + (200,), width=2)
        anchor = 'ld' if offset[0] >= 0 else 'rd'
        self.text((tx + (6 if offset[0] >= 0 else -6), ty - 2), s, F_LAB, colt, anchor=anchor)
        if sub:
            self.text((tx + (6 if offset[0] >= 0 else -6), ty + 2), sub, F_SM, INK, anchor='la' if offset[0] >= 0 else 'ra')
        if new:
            w = self.ud.textlength(s, font=F_LAB)
            nx = tx + 6 + w + 10 if offset[0] >= 0 else tx - 6 - w - 10 - 46
            self.ud.rectangle([nx, ty - 24, nx + 46, ty - 4], fill=(255, 255, 255, 230))
            self.ud.text((nx + 23, ty - 14), 'NEW', font=F_SM, fill=(10, 16, 26, 255), anchor='mm')

    def panel(self, box, title=None):
        x0, y0, x1, y1 = box
        c = 14
        poly = [(x0 + c, y0), (x1, y0), (x1, y1 - c), (x1 - c, y1), (x0, y1), (x0, y0 + c)]
        self.ud.polygon(poly, fill=(6, 14, 24, 205))
        self.ud.line(poly + [poly[0]], fill=CYAN + (230,), width=2)
        self.ud.line([(x0 + c + 6, y0 + 4), (x0 + c + 70, y0 + 4)], fill=(255, 140, 40, 230), width=3)
        if title:
            self.text((x0 + 18, y0 + 14), title, F_H3, DIM, stroke=0)

    def compose(self):
        b = np.asarray(self.base).astype(np.float32) / 255
        L = np.asarray(self.light).astype(np.float32) / 255
        glow = np.stack([gaussian_filter(L[..., k], 5) for k in range(3)], -1) * 1.1
        glow2 = np.stack([gaussian_filter(L[..., k], 18) for k in range(3)], -1) * 0.9
        out = b + self.fields + L + glow + glow2
        out = 1 - (1 - np.clip(b, 0, 1)) * (1 - np.clip(out - b, 0, 1))  # screen
        img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
        img = img.convert('RGBA')
        img.alpha_composite(self.ui)
        return img.convert('RGB')


# ---------------------------------------------------------------- one board
def render(base_img, era, summary=False):
    e = era - 1
    on = lambda since, until=99: since <= era <= until
    new = lambda since: (since == era) and not summary
    B = Board(base_img)
    G = GROUPS

    # --- influence fields
    B.field(M['oce'], OC, 1.0)
    B.field(M['asia'], AS, 0.9)
    if era >= 2:
        B.field(M['ng'], AS, 0.9)
    else:
        B.field(M['ng'], GREY, 0.5)
    # the Great Dry: heat over the emptied north and interior
    heat = M['aus'] * np.clip(1 - np.hypot(LON - 127, (LAT + 21) * 1.2) / 16, 0, 1) ** 1.3
    B.fields += heat[..., None] * (HEAT / 255.0) * 0.10
    # contested hatching on New Guinea's south coast
    if era >= 4:
        band = M['ng'] * np.clip((-LAT - 7.4) / 1.2, 0, 1) * (LON > 140.9) * (LON < 147.6)
        stripes = ((XS + YS) // 8 % 3 == 0)
        B.fields += (band * stripes)[..., None] * (OC / 255.0) * 0.40
    # Green Cape
    if era >= 5:
        cape = M['aus'] * np.clip(1 - np.hypot((LON - 142.7) * 1.3, LAT + 13.2) / 3.2, 0, 1)
        B.fields += cape[..., None] * (np.array([170, 255, 140]) / 255.0) * 0.30

    p = {k: P(*v) for k, v in PL.items()}

    # --- islands and cables (era I on)
    for k in ['honiara', 'vila', 'noumea', 'suva'] + ([] if era >= 7 else ['funafuti', 'tarawa', 'majuro']):
        B.line(bezier(p['sydney'], p[k], 0.10), OC * 0.55, w=2)
        B.ring(p[k], 7, OC, 2); B.dot(p[k], 3, OC)
    if era >= 7:
        for k in ['funafuti', 'tarawa', 'majuro']:
            B.line(bezier(p[k], p['cape'], -0.18), WHITE * 0.8, w=2, dash=(10, 8), chevrons=True)
            for r in (8, 13):
                B.ring(p[k], r, GREY, 1)
        B.tag(p['tarawa'], 'ATOLLS DROWNED', (-30, -40), WHITE, 'ANTARCTIC PULSE · VII', new=new(7))

    # --- Darwin gate, the rail and the ore
    rail = geo_out(RAIL)
    B.line(rail, OC * 0.9, w=3, dash=(14, 6))
    B.square(p['hedland'], 7, OC)
    ore_w = {1: 8, 2: 6, 3: 6, 4: 4}.get(era, 3)
    ore = bezier(p['darwin'], p['java'], 0.22)
    B.line(ore, OC, w=ore_w, chevrons=True)
    lab = 'ORE' if era <= 3 else ('ORE · LITHIUM ENDS 2255' if era == 4 else 'NICKEL')
    mid = ore[len(ore) // 2]
    B.text((mid[0] - 10, mid[1] - 14), lab, F_LAB, tuple(OC), anchor='rd')
    B.hexagon(p['darwin'], 16, OC, w=3, fill=OC * 0.35)
    B.tag(p['darwin'], 'DARWIN GATE', (-60, 52), OC, 'the only port for Asia’s ore', new=new(1))
    B.tag(p['hedland'], 'PILBARA', (-40, 40), OC, 'machine-run mines', )

    # --- Asia's cable from Java
    cable = bezier(p['java'], p['darwin'], 0.12)
    if era == 1:
        cut = cable[: int(len(cable) * 0.93)]
        B.line(cut, AS, w=3)
        B.text(tuple(cable[int(len(cable) * 0.6)] + np.array([0, 14])), 'ASIA CABLE · UNPLUGGED', F_SM, tuple(AS), anchor='la')
    else:
        B.line(cable, AS, w=3)
        q0, q1 = cable[-14], cable[-10]
        d = (q1 - q0) / (np.hypot(*(q1 - q0)) + 1e-6); nrm = np.array([-d[1], d[0]])
        B.ld.line([tuple(q1 + nrm * 13), tuple(q1 - nrm * 13)], fill=tuple(int(c) for c in WHITE), width=5)
        B.text(tuple(cable[int(len(cable) * 0.6)] + np.array([0, 14])), 'FIREWALLED LINK', F_SM, tuple(AS), anchor='la')

    # --- Sydney, the Unfinished, the Highlands
    B.hexagon(p['sydney'], 13, OC, w=3, fill=OC * 0.5)
    for r in (22, 32):
        B.ring(p['sydney'], r, OC * 0.8, 2)
    B.ring(p['highlands'], 10, OC, 3); B.dot(p['highlands'], 4, OC)
    hl = 'HIGHLANDS TOWN' if era < 3 else ('COOLING WORKS' if era < 6 else ('TWIN CITY' if era < 7 else 'SEA WORKS'))
    hl_new = new(1) or new(3) or new(6) or new(7)
    B.tag(p['highlands'], hl, (-150, 70), OC, 'the Highlands', new=hl_new)
    if era >= 2:
        B.tag(p['sydney'], 'SYDNEY', (70, 30), OC, 'THE UNFINISHED below', new=new(2))
    else:
        B.tag(p['sydney'], 'SYDNEY', (70, 30), OC, 'the dig begins')

    # --- cooling parts from Asia (II, cut in III)
    if era in (2, 3):
        cp = bezier(p['java'], p['sydney'], -0.25)
        if era == 2:
            B.line(cp, AS, w=3, chevrons=True)
            m = cp[int(len(cp) * 0.55)]
            B.text((m[0], m[1] + 10), 'COOLING PARTS', F_SM, tuple(AS))
        else:
            a, b = cp[: int(len(cp) * 0.5)], cp[int(len(cp) * 0.58):]
            B.line(a, AS * 0.7, w=3, dash=(8, 8)); B.line(b, AS * 0.7, w=3, dash=(8, 8))
            m = cp[int(len(cp) * 0.54)]
            B.text((m[0], m[1] + 10), 'COOLING PARTS · CUT', F_SM, tuple(AS))

    # --- cooling machines to Asia (IV on, ended 2340)
    if era >= 4:
        cm = bezier(p['highlands'], p['java'], -0.30)
        if era < 7:
            B.line(cm, OC, w=3, chevrons=True)
            m = cm[int(len(cm) * 0.36)]
            B.text((m[0], m[1] + 10), 'COOLING TO ASIA', F_SM, tuple(OC))
        else:
            B.line(cm, OC * 0.5, w=2, dash=(6, 10))
            m = cm[int(len(cm) * 0.36)]
            B.text((m[0], m[1] + 10), 'COOLING · ENDED 2340', F_SM, tuple(OC))

    # --- desal coast and membranes (IV on)
    if era >= 4:
        dpts = geo_out(DESAL)
        B.line(dpts, OC * 0.5, w=2)
        for q in dpts:
            B.square(tuple(q), 6, OC)
        mem = bezier(p['java'], tuple(dpts[4]), -0.22)
        B.line(mem, AS, w=3, chevrons=True)
        m = mem[int(len(mem) * 0.58)]
        B.text((m[0] - 8, m[1] + 8), 'MEMBRANES', F_SM, tuple(AS), anchor='ra')
        B.tag(tuple(dpts[2]), 'DESAL COAST', (95, -10), OC, 'built in the drought · IV', new=new(4))

    # --- New Guinea
    B.hexagon(p['copper'], 10, AS if era >= 2 else GREY, w=2)
    if era >= 2:
        B.tag(p['copper'], 'PAPUA COPPER', (-40, -46), AS, 'on Asia’s network', new=new(2))
    ngs = 'NEW GUINEA'
    ngsub = {1: 'unclaimed', 2: 'joins Asia’s network', 3: 'Asia’s grid', 4: 'remembers who brought water',
             5: 'Asia’s grid, your goodwill', 6: 'Asia’s grid, your water', 7: 'south: self-rule 2345'}[era]
    B.ring(p['moresby'], 8, AS if era >= 2 else GREY, 2)
    B.tag(p['moresby'], ngs, (60, -46), AS if era >= 2 else GREY, ngsub, new=new(2) or new(7))
    if era in (4, 6):
        aid = bezier(p['capetip'], p['moresby'], 0.35)
        B.line(aid, OC, w=2, dash=(8, 6), chevrons=True)
        m = aid[len(aid) // 2]
        B.text((m[0] + 8, m[1] + 4), 'AID' if era == 4 else 'WATER + FOOD', F_SM, tuple(OC))

    # --- Torres Strait, the reef, the gate
    if era >= 3:
        line = geo_out([(141.0, -9.72), (143.9, -9.72)])
        B.line(line, OC, w=4, dash=(16, 6))
    if era == 2:
        B.tag(p['reef'], 'TORRES STRAIT', (70, 70), GREY, 'networks touch')
    if era == 3 or era == 4:
        B.tag(p['reef'], 'TORRES LINE', (70, 70), OC, 'strait closed · III', new=new(3))
    if era >= 5:
        B.hexagon(p['reef'], 15, WHITE, w=3, fill=OC * 0.6)
        for r in (24, 34):
            B.ring(p['reef'], r, WHITE * 0.7, 2)
        sub = {5: 'boarded, no shot fired', 6: 'Asia’s relay · your toll', 7: 'tapped'}[era]
        B.tag(p['reef'], 'REEF GATE', (95, 120), WHITE, sub, new=new(5))
    if era >= 6:
        st = bezier(p['moresby'], p['reef'], 0.25)
        st2 = bezier(p['reef'], p['coral'], -0.25)
        B.line(np.r_[st, st2], AS, w=6, chevrons=True)
        m = st2[-1]
        B.text((m[0] + 14, m[1] + 6), 'ASIA CORAL SEA TRAFFIC', F_SM, tuple(AS))
    if era >= 7:
        tp = bezier(p['reef'], p['sydney'], -0.18)
        B.line(tp, OC, w=2, dash=(4, 5))
        m = tp[int(len(tp) * 0.55)]
        B.text((m[0] + 10, m[1]), 'TAPPED', F_LAB, tuple(OC))
    if era == 5:
        rice = bezier(p['copper'], p['honiara'], -0.25)
        rice = rice[: int(len(rice) * 0.7)]
        B.line(rice, AS * 0.8, w=2, dash=(8, 8))
        end = rice[-1]
        B.ld.line([tuple(end - 9), tuple(end + 9)], fill=tuple(AS), width=3)
        B.ld.line([(end[0] - 9, end[1] + 9), (end[0] + 9, end[1] - 9)], fill=tuple(AS), width=3)
        B.text((end[0] + 14, end[1] - 6), 'ASIA’S RICE · TURNED BACK', F_SM, tuple(AS))
        B.tag(p['honiara'], 'ISLANDS', (40, 70), OC, 'fed by Oceania · V')

    # --- Green Cape
    if era >= 5:
        sub = 'irrigated from the desal coast · V' if era < 7 else 'atoll towns settle · VII'
        B.tag(p['cape'], 'GREEN CAPE', (-150, 92), (170, 255, 140), sub, new=new(5) or new(7))
        if era >= 7:
            for q in geo_out(ATOLL_TOWNS):
                B.dot(tuple(q), 5, WHITE)

    # --- Tibet lithium, off the board
    tx, ty = 960, 40
    if era >= 3:
        colt = AS if era >= 4 else AS * 0.6
        B.line([(tx + 60, ty + 70), (tx + 6, ty + 16)], colt, w=3)
        B.ld.polygon([(tx, ty), (tx + 22, ty + 6), (tx + 6, ty + 22)], fill=tuple(int(c) for c in colt))

    # --- region labels
    ox, oy = P(125.5, -24.0)
    B.text((ox, oy), 'OCEANIA', F_H2, tuple(OC), anchor='mm', stroke=4)
    ax, ay = P(114.5, 1.5)
    B.text((ax, ay), 'ASIA', F_H2, tuple(AS), anchor='mm', stroke=4)
    if era >= 3:
        B.text((tx + 70, ty + 70), 'TIBET LITHIUM' + (' · ONLINE 2255' if era >= 4 else ' · SURVEY'), F_SM, tuple(AS), anchor='lm')

    # ------------------------------------------------------------ UI
    num, years, head, line, event = ERAS[e]
    # title block
    B.panel((60, 28, 900, 214))
    B.text((84, 44), '2350 · SEASON 1', F_MONO_L, DIM, stroke=0)
    if summary:
        B.text((84, 72), 'THE CONTINENT EVERYTHING RAN THROUGH', F_TITLE, INK, stroke=0)
        B.text((86, 132), 'Final state · 2350 · Oceania (Mike) against Asia (Claude)', F_H3, DIM, stroke=0)
    else:
        B.text((84, 72), f'ERA {num} · {head}', F_TITLE, INK, stroke=0)
        B.text((86, 132), f'{years} · {line}', F_H3, DIM, stroke=0)
    # legend
    lx, ly = 86, 172
    for lab_, col in (('OCEANIA', OC), ('ASIA', AS), ('UNCLAIMED', GREY), ('THE GREAT DRY', HEAT)):
        B.ud.rectangle([lx, ly, lx + 16, ly + 16], fill=tuple(int(c) for c in col) + (255,))
        B.text((lx + 24, ly + 8), lab_, F_SM, INK, anchor='lm', stroke=0)
        lx += 24 + B.ud.textlength(lab_, font=F_SM) + 30
    if event and not summary:
        B.text((880, 44), 'WORLD EVENT · ' + event, F_MONO_L, (255, 150, 70), anchor='ra', stroke=0)

    # left column panels
    X0, X1 = 30, 600
    # hooks chart
    y0 = 530
    B.panel((X0, y0, X1, y0 + 250), 'HOOKS HELD · what the rival depends on you for')
    cx0, cx1, cy0, cy1 = X0 + 50, X1 - 30, y0 + 62, y0 + 210
    for v in range(0, 6):
        yy = cy1 - (cy1 - cy0) * v / 5
        B.ud.line([(cx0, yy), (cx1, yy)], fill=(60, 120, 140, 110), width=1)
        B.text((cx0 - 12, yy), str(v), F_MONO, DIM, anchor='rm', stroke=0)
    upto = 7 if summary else era
    xs = [cx0 + (cx1 - cx0) * i / 6 for i in range(7)]
    for i in range(7):
        B.text((xs[i], cy1 + 18), ERAS[i][0], F_MONO, INK if i < upto else DIM, anchor='mm', stroke=0)
    for vals, col in ((HOOKS_AS, AS), (HOOKS_OC, OC)):
        pts = [(xs[i], cy1 - (cy1 - cy0) * vals[i] / 5) for i in range(upto)]
        if len(pts) > 1:
            B.ud.line(pts, fill=tuple(int(c) for c in col) + (255,), width=4, joint='curve')
        for q in pts:
            B.ud.ellipse([q[0] - 5, q[1] - 5, q[0] + 5, q[1] + 5], fill=tuple(int(c) for c in col) + (255,))
    # contested
    y0 = 800
    B.panel((X0, y0, X1, y0 + 230), 'INFLUENCE OVER CONTESTED PLACES')
    rows = [('REEF GATE' if era >= 5 else 'TORRES STRAIT', 'STRAIT'), ('DARWIN', 'DARWIN'), ('NEW GUINEA SOUTH', 'NG SOUTH')]
    for i, (lab_, key) in enumerate(rows):
        yy = y0 + 66 + i * 54
        B.text((X0 + 22, yy), lab_, F_H3, INK, anchor='lm', stroke=0)
        bx0, bx1 = X0 + 270, X1 - 30
        v = CONTEST[key][e]
        B.ud.rectangle([bx0, yy - 10, bx1, yy + 10], outline=(70, 130, 150, 255), width=1)
        if v is None:
            B.text(((bx0 + bx1) / 2, yy), 'UNHELD', F_MONO, DIM, anchor='mm', stroke=0)
        else:
            mid_ = bx0 + (bx1 - bx0) * v[0] / 100
            if v[0]:
                B.ud.rectangle([bx0 + 1, yy - 9, mid_, yy + 9], fill=tuple(int(c) for c in OC) + (255,))
            if v[1]:
                B.ud.rectangle([mid_, yy - 9, bx1 - 1, yy + 9], fill=tuple(int(c) for c in AS) + (255,))
    # runs through
    y0 = 1050
    B.panel((X0, y0, X1, y0 + 330), 'WHAT RUNS THROUGH YOU')
    for j, (lab_, items, col) in enumerate((('OCEANIA', THROUGH_OC[e], OC), ('ASIA', THROUGH_AS[e], AS))):
        cx = X0 + 22 + j * 285
        B.text((cx, y0 + 62), lab_, F_H3, tuple(int(c) for c in col), stroke=0)
        for k, it in enumerate(items):
            B.text((cx, y0 + 98 + k * 40), it, F_SM, INK, stroke=0)
    # timeline
    tx0, tx1, tyy = 640, 1540, 1398
    B.ud.line([(tx0, tyy), (tx1, tyy)], fill=CYAN + (200,), width=2)
    for i, (n_, yrs, _, _, ev) in enumerate(ERAS):
        xx = tx0 + (tx1 - tx0) * i / 6
        cur = (i == e) and not summary
        done = i < (7 if summary else era)
        r = 11 if cur else 7
        fillc = (255, 255, 255, 255) if cur else ((90, 210, 235, 255) if done else (40, 70, 85, 255))
        B.ud.ellipse([xx - r, tyy - r, xx + r, tyy + r], fill=fillc)
        B.text((xx, tyy - 22), n_, F_MONO, INK if done else DIM, anchor='mm', stroke=2)
        if ev and done:
            B.ud.polygon([(xx, tyy + 14), (xx - 7, tyy + 26), (xx + 7, tyy + 26)], fill=(255, 150, 70, 255))

    return B.compose()


def main():
    global GROUPS, M, LON, LAT, XS, YS
    base_path, out_dir = sys.argv[1], Path(sys.argv[2])
    which = sys.argv[3:] or ['1', '2', '3', '4', '5', '6', '7', 'summary']
    out_dir.mkdir(parents=True, exist_ok=True)
    im = Image.open(base_path).convert('RGB')
    base = im.crop((int(BX0), int(BY0), int(BX1), int(BY1))).resize((OUT_W, OUT_H), Image.LANCZOS)
    base = Image.fromarray((np.asarray(base).astype(np.float32) * 0.5).astype(np.uint8))
    GROUPS = load_groups()
    M = {k: poly_mask(v) for k, v in GROUPS.items()}
    LON, LAT = lonlat_grid()
    YS, XS = np.mgrid[0:OUT_H, 0:OUT_W]
    for w in which:
        if w == 'summary':
            img = render(base, 7, summary=True); name = 'season1_board_final.jpg'
        else:
            n = int(w); img = render(base, n); name = f'season1_board_era{n}.jpg'
        img.save(out_dir / name, quality=92)
        print('saved', name)


if __name__ == '__main__':
    main()

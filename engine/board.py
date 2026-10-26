#!/usr/bin/env python3
"""2350: the core board library.

Projection from longitude and latitude onto a stylised base map (a linear fit plus a
thin-plate-spline correction), glow fields, lines, rings, labels and panels. The world
renderer (world_board.py) loads this module and sets its own calibration and canvas size.
"""
import json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import gaussian_filter

HERE = Path(__file__).resolve().parent
FONTS = HERE / 'fonts'

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

# ---------------------------------------------------------------- geometry
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

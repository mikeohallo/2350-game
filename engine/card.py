#!/usr/bin/env python3
"""2350: a power's 2350 card. The ring is everything its people wanted (100): each value is a slice
sized by its weight, split into delivered / out of reach (the world: events and the century draft) / let down.

  python3 card.py base/card_bg_asia.jpg out/season6_card_asia.jpg
"""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from board import font  # noqa: E402

PORT = (255, 105, 95)
GREY = (120, 130, 145)
LET = (58, 20, 26)
INK = (230, 240, 248)
DIM = (150, 175, 190)

CARD = dict(
    power='ASIA', who='How Asia\u2019s people judged the century', colour=PORT, season='SEASON 6',
    values=[  # name, weight, delivered, out of reach, let down, reason
        ('By need', 25, 18, 0, 7, 'Green levels, Thaw places, cool halls by need. Fifty years of cooling by the bill.'),
        ('Surviving the heat', 25, 20, 2, 3, 'The move north, coolcells, cool streets, the Sunshade. The hot levels waited.'),
        ('Water', 15, 10, 3, 2, 'Equal shares and water from the air after the ice went. The plains went hungry first.'),
        ('A network you trust', 15, 13, 0, 2, 'The mirror, the gates, the open watch, one world. The decoy cost trust for a time.'),
        ('Food', 10, 8, 0, 2, 'Machine farms and sky farms. Four continents fed from the Thaw, and a hungry 2279.'),
        ('Family in the north', 10, 5, 2, 3, 'Your wells saved most of the Thaw. When the ground went, you sent a treaty.'),
    ],
    others=[('EUROPE', (190, 125, 255), 58, 14), ('OCEANIA', (70, 225, 205), 60, 8), ('S. AMERICA', (150, 235, 90), 50, 20),
            ('AFRICA', (255, 190, 70), 52, 10), ('THE THAW', (255, 150, 215), 44, 18), ('N. AMERICA', (150, 215, 255), 45, 10)],
    words='You cooled them, watered them and kept the network honest. You let the bill decide for fifty years.',
)


def sector(cx, cy, r0, r1, a0, a1, n=80):
    a = np.radians(np.linspace(a0, a1, n))
    outer = [(cx + r1 * math.cos(t), cy + r1 * math.sin(t)) for t in a]
    inner = [(cx + r0 * math.cos(t), cy + r0 * math.sin(t)) for t in a[::-1]]
    return outer + inner


def ring(img, cx, cy, r0, r1, parts, colour, glow=True, hatch_px=10):
    """parts: list of (weight, delivered, out_of_reach, let_down). Angles start at the top, clockwise."""
    W, H = img.size
    fill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fill)
    lit = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lit)
    hatch = Image.new('L', (W, H), 0); dh = ImageDraw.Draw(hatch)
    gap = 1.6; a = -90.0; mids = []
    for wgt, dv, oor, ld in parts:
        span = wgt * 3.6
        s0, s1 = a + gap / 2, a + span - gap / 2
        tot = dv + oor + ld
        b0 = s0; b1 = s0 + (s1 - s0) * dv / tot; b2 = b1 + (s1 - s0) * oor / tot
        d.polygon(sector(cx, cy, r0, r1, b0, b1), fill=colour + (255,))
        dl.polygon(sector(cx, cy, r0, r1, b0, b1), fill=colour + (255,))
        if oor:
            d.polygon(sector(cx, cy, r0, r1, b1, b2), fill=GREY + (255,))
            dh.polygon(sector(cx, cy, r0, r1, b1, b2), fill=255)
        if ld:
            d.polygon(sector(cx, cy, r0, r1, b2, s1), fill=LET + (255,))
            d.line(sector(cx, cy, r0, r1, b2, s1) + [sector(cx, cy, r0, r1, b2, s1)[0]], fill=colour + (150,), width=2)
        mids.append((a + span / 2, s0, s1))
        a += span
    if glow:
        g = lit.filter(ImageFilter.GaussianBlur(22))
        img.alpha_composite(Image.eval(g, lambda v: int(v * 0.9)))
    # stripes over out-of-reach
    ys, xs = np.mgrid[0:H, 0:W]
    stripes = ((xs + ys) // hatch_px % 2 == 0)
    hm = (np.asarray(hatch) > 0) & stripes
    sh = np.zeros((H, W, 4), np.uint8); sh[hm] = (70, 78, 92, 255)
    img.alpha_composite(fill)
    img.alpha_composite(Image.fromarray(sh, 'RGBA'))
    return mids


def main():
    bg_path, out = sys.argv[1], sys.argv[2]
    C = CARD
    bg = Image.open(bg_path).convert('RGB')
    W, H = bg.size
    arr = np.asarray(bg).astype(np.float32) * 0.42
    # darken more under the panel and around the ring for legibility
    xs = np.arange(W)[None, :, None]
    arr *= np.clip(1.0 - (xs - W * 0.55) / (W * 0.45) * 0.55, 0.45, 1.0)
    img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(img)
    F_BIG = font('Rajdhani-700', 230); F_T = font('Rajdhani-700', 74); F_S = font('Rajdhani-600', 34)
    F_K = font('Rajdhani-700', 38); F_L = font('Rajdhani-600', 30); F_M = font('ShareTechMono', 28); F_V = font('Rajdhani-700', 34)

    cx, cy, r0, r1 = 840, 790, 335, 525
    parts = [(w, dv, o, l) for _, w, dv, o, l, _ in C['values']]
    mids = ring(img, cx, cy, r0, r1, parts, C['colour'])
    d = ImageDraw.Draw(img)
    deliv = sum(p[1] for p in parts); oor = sum(p[2] for p in parts); let = sum(p[3] for p in parts)
    pct = round(100 * deliv / (100 - oor))
    d.text((cx, cy - 40), f'{pct}%', font=F_BIG, fill=INK + (255,), anchor='mm')
    d.text((cx, cy + 92), 'OF WHAT WAS POSSIBLE', font=F_K, fill=DIM + (255,), anchor='mm')
    d.text((cx, cy + 142), f'{deliv} delivered · {oor} out of reach · {let} let down', font=F_L, fill=INK + (255,), anchor='mm')
    # slice labels
    for (name, w, dv, o, l, why), (am, s0, s1) in zip(C['values'], mids):
        t = math.radians(am); rx, ry = cx + (r1 + 46) * math.cos(t), cy + (r1 + 46) * math.sin(t)
        anc = 'lm' if math.cos(t) > 0.15 else ('rm' if math.cos(t) < -0.15 else 'mm')
        nm = name.upper(); parts = [nm]
        if len(nm) > 14:
            ws = nm.split(); h = len(ws) // 2 + len(ws) % 2; parts = [' '.join(ws[:h]), ' '.join(ws[h:])]
        top = ry - 18 - 18 * (len(parts) - 1)
        for j, pt in enumerate(parts):
            d.text((rx, top + 36 * j), pt, font=F_V, fill=C['colour'] + (255,), anchor=anc, stroke_width=4, stroke_fill=(5, 8, 14, 230))
        d.text((rx, top + 36 * len(parts)), f'{dv} of {w}', font=F_L, fill=INK + (255,), anchor=anc, stroke_width=4, stroke_fill=(5, 8, 14, 230))

    # right panel
    px = 1560; pw = W - px - 70
    panel = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(panel).rectangle([px - 40, 0, W, H], fill=(4, 8, 14, 175))
    img.alpha_composite(panel); d = ImageDraw.Draw(img)
    d.text((px, 60), f"2350 · {C.get('season', 'SEASON 5')} · 2350 CARD", font=F_M, fill=DIM + (255,))
    d.text((px, 98), C['power'], font=F_T, fill=C['colour'] + (255,))
    d.text((px, 182), C['who'], font=F_S, fill=INK + (255,))
    y = 246
    for lab, col, hatch in (('Delivered', C['colour'], False), ('Out of reach: the world made it impossible', GREY, True), ('Let down: possible, not done', LET, False)):
        d.rectangle([px, y + 4, px + 30, y + 30], fill=col + (255,), outline=C['colour'] + (180,) if col == LET else None, width=2)
        if hatch:
            for k in range(-30, 30, 9):
                d.line([(px + max(0, k), y + 4 + max(0, -k)), (px + min(30, 30 + k), y + 30 - max(0, k))], fill=(70, 78, 92, 255), width=3)
        d.text((px + 44, y + 17), lab, font=F_L, fill=INK + (255,), anchor='lm'); y += 44
    y += 14; d.line([(px, y), (W - 70, y)], fill=(70, 130, 150, 200), width=2); y += 22

    def wrap(s, f, width):
        out, cur = [], ''
        for wd in s.split():
            t = (cur + ' ' + wd).strip()
            if d.textlength(t, font=f) > width and cur:
                out.append(cur); cur = wd
            else:
                cur = t
        out.append(cur); return out

    for name, w, dv, o, l, why in C['values']:
        d.text((px, y), f'{name}', font=F_K, fill=INK + (255,))
        d.text((W - 70, y + 4), f'{dv} / {w}', font=F_K, fill=C['colour'] + (255,), anchor='ra')
        # mini bar
        bx0, bx1 = px, W - 70; by = y + 50
        tot = w; seg = [(dv, C['colour']), (o, GREY), (l, LET)]; cxp = bx0
        for v, col in seg:
            if v:
                d.rectangle([cxp, by, cxp + (bx1 - bx0) * v / tot, by + 10], fill=col + (255,)); cxp += (bx1 - bx0) * v / tot
        lines = wrap(why, F_L, W - 70 - px)
        for j, part in enumerate(lines):
            d.text((px, by + 22 + j * 34), part, font=F_L, fill=DIM + (255,))
        y = by + 22 + len(lines) * 34 + 18
    d.line([(px, y), (W - 70, y)], fill=(70, 130, 150, 200), width=2); y += 22
    d.text((px, y), 'THE OTHER POWERS', font=F_K, fill=INK + (255,)); y += 58
    n_o = len(C['others']); ox = px + (50 if n_o > 3 else 70); ro0, ro1 = (26, 44) if n_o > 3 else (34, 58)
    for name, col, dv, oo in C['others']:
        ring(img, ox, y + 60, ro0, ro1, [(100, dv, oo, 100 - dv - oo)], col, glow=False, hatch_px=6)
        d = ImageDraw.Draw(img)
        p = round(100 * dv / (100 - oo))
        d.text((ox, y + 60), f'{p}%', font=F_L if n_o > 3 else F_V, fill=INK + (255,), anchor='mm')
        d.text((ox, y + (122 if n_o > 3 else 140)), name if n_o > 3 else name.replace('THE ', ''), font=F_L, fill=col + (255,), anchor='mm')
        ox += (W - 70 - px - (100 if n_o > 3 else 140)) / (n_o - 1)
    # verdict in words, bottom-left under the ring
    d.text((cx, H - 70), C['words'], font=F_S, fill=INK + (255,), anchor='mm', stroke_width=4, stroke_fill=(5, 8, 14, 230))
    img.convert('RGB').save(out, quality=93)
    print('card', pct, deliv, oor, let)


if __name__ == '__main__':
    main()

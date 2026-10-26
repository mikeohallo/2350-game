#!/usr/bin/env python3
"""2350, season 6: GLOBAL scale. Six continental blocs on the world board, plus unclaimed ground
(Siberia's thaw, the Arctic, Antarctica, the Moon link). The key runs underneath the map.

  python3 world_board.py base/base_global_v1.jpg out setup 1 2 ... 10
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import RBFInterpolator
from scipy.ndimage import gaussian_filter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import board as bd                                   # noqa: E402
from board import font, INK, DIM, CYAN                # noqa: E402

cal = json.loads((HERE / 'calib_world.json').read_text())
bd.cal = cal
src, dst = np.load(HERE / 'warp_src_world.npy'), np.load(HERE / 'warp_dst_world.npy')
bd._rbf = RBFInterpolator(src, dst - src, kernel='thin_plate_spline', smoothing=400.0)
bd.WX0, bd.WY0, bd.WF = int(cal['WX0']), int(cal['WY0']), int(cal['WF'])

LON0, LON1, LAT_TOP, LAT_BOT = -172, 190, 82, -58
MAP_W = 3000
bd.BX0 = cal['a'] * LON0 + cal['b']; bd.BX1 = cal['a'] * LON1 + cal['b']
bd.BY0 = cal['c'] * LAT_TOP + cal['d']
bd.SC = MAP_W / (bd.BX1 - bd.BX0)
MAP_H = int(round((cal['c'] * LAT_BOT + cal['d'] - bd.BY0) * bd.SC))
bd.BY1 = bd.BY0 + MAP_H / bd.SC
KEY_H = 860
bd.OUT_W, bd.OUT_H = MAP_W, MAP_H + KEY_H
P, geo_out = bd.P, bd.geo_out

NAM = np.array([150, 215, 255]); SAM = np.array([150, 235, 90]); EUR = np.array([190, 125, 255])
AFR = np.array([255, 190, 70]); ASI = np.array([255, 105, 95]); OCE = np.array([70, 225, 205])
THW = np.array([255, 150, 215])
CENTRE = np.array([205, 218, 232])
AREA = {'nam': NAM, 'sam': SAM, 'eur': EUR, 'afr': AFR, 'asi': ASI, 'oce': OCE, 'thw': THW}
NAMEOF = {'nam': 'NORTH AMERICA', 'sam': 'SOUTH AMERICA', 'eur': 'EUROPE', 'afr': 'AFRICA', 'asi': 'ASIA', 'oce': 'OCEANIA',
          'thw': 'THE THAW', 'centre': 'UNCLAIMED'}
COL = {'WATER': np.array([70, 140, 255]), 'POWER': np.array([255, 225, 70]), 'PEOPLE': np.array([255, 245, 190]),
       'FOOD': np.array([150, 235, 90]), 'DATA': np.array([235, 240, 255]), 'HEAT': np.array([255, 95, 45]),
       'SUN': np.array([255, 210, 90]), 'ICE': np.array([225, 245, 255]), 'STORM': np.array([185, 120, 255]),
       'MINERALS': np.array([255, 140, 30]), 'CONTACT': np.array([190, 205, 220]), 'STAR': np.array([240, 240, 255]),
       'centre': CENTRE, 'key': np.array([210, 230, 240])}
COL.update(AREA)

F_TITLE = font('Rajdhani-700', 58); F_SUBT = font('Rajdhani-600', 28); F_REG = font('Rajdhani-700', 30)
F_KT = font('Rajdhani-700', 32); F_KL = font('Rajdhani-600', 26); F_BADGE = font('Rajdhani-700', 28)
F_MONO = font('ShareTechMono', 24); F_EVT = font('Rajdhani-600', 22); F_REF = font('Rajdhani-600', 22)
LH = 31

PL = dict(
    canada_north=(-100.0, 62.0), southwest=(-110.0, 33.0), gulfcoast=(-90.0, 30.0), newyork=(-74.0, 40.7),
    amazon=(-62.0, -5.0), andes=(-68.0, -20.0), pampas=(-62.0, -35.0),
    northsea=(2.0, 56.0), med=(18.0, 39.0), alps=(10.0, 46.5),
    sahara=(10.0, 23.0), congo=(22.0, -2.0), lagos=(3.4, 6.5), kinshasa=(15.3, -4.3),
    himalaya=(84.0, 29.5), india=(78.0, 22.0), eastchina=(116.0, 31.0), gulf=(51.0, 26.0), jakarta=(106.8, -6.2),
    australia=(134.0, -25.0), aotearoa=(172.5, -41.5), pacific=(-170.0, -14.0), pacificw=(165.0, -8.0),
    siberia=(105.0, 64.0), arctic=(45.0, 76.0), antarctica=(0.0, -56.0), moonlink=(-30.0, 0.0),
)


def blocs():
    g = json.loads((HERE / 'data' / 'ne_50m_admin_0_countries.geojson').read_text())
    key = {'North America': 'nam', 'South America': 'sam', 'Europe': 'eur', 'Africa': 'afr', 'Asia': 'asi', 'Oceania': 'oce'}
    out = {k: [] for k in list(key.values()) + ['thaw']}
    for f in g['features']:
        pr = f['properties']; k = key.get(pr['CONTINENT'])
        gm = f['geometry']
        polys = gm['coordinates'] if gm['type'] == 'MultiPolygon' else [gm['coordinates']]
        for p in polys:
            ring = p[0]
            clon = sum(a for a, _ in ring) / len(ring)
            if pr['ADMIN'] == 'Russia':
                out['eur' if -100 < clon < 60 else 'thaw'].append(ring); continue
            if pr['ADMIN'] == 'France' and clon < -30:
                out['sam'].append(ring); continue
            if k:
                out[k].append(ring)
    return out


def setup(base_path):
    im = Image.open(base_path).convert('RGB')
    mp = im.crop((int(bd.BX0), int(bd.BY0), int(bd.BX1), int(bd.BY1))).resize((MAP_W, MAP_H), Image.LANCZOS)
    mp = Image.fromarray((np.asarray(mp).astype(np.float32) * 0.5).astype(np.uint8))
    base = Image.new('RGB', (bd.OUT_W, bd.OUT_H), (5, 10, 18)); base.paste(mp, (0, 0))
    bd.YS, bd.XS = np.mgrid[0:bd.OUT_H, 0:bd.OUT_W]
    R = blocs()
    A = {k: bd.poly_mask(v) > 0.4 for k, v in R.items()}
    A['centre'] = A.pop('thaw')
    A['thw'] = np.zeros_like(A['centre'])
    for k in A:
        A[k][MAP_H:, :] = False
    return base, A


def edge_of(m, sigma=1.2, k=5.0):
    sm = gaussian_filter(m.astype(np.float32), sigma); gy, gx = np.gradient(sm)
    return np.clip(np.hypot(gx, gy) * k, 0, 1)


def blob(xy, r_deg):
    x, y = xy; sig = r_deg * cal['a'] * bd.SC
    return np.exp(-((bd.XS - x) ** 2 + (bd.YS - y) ** 2) / (2 * sig * sig)).astype(np.float32)


def where(w):
    return P(*PL[w]) if isinstance(w, str) else P(*w)


def territory(B, A, strength=None):
    strength = strength or {}
    for k in AREA:
        col = AREA[k]; s = strength.get(k, 1.0)
        B.fields += A[k][..., None] * (col / 255.0) * 0.09 * s
        B.fields += edge_of(A[k])[..., None] * (col / 255.0) * 0.75 * s
    hatch = ((bd.XS + bd.YS) // 8 % 4 == 0)
    B.fields += (A['centre'] & hatch)[..., None] * (CENTRE / 255.0) * 0.10


def heat(B, items):
    acc = {}
    for w, who, s, r in items:
        acc.setdefault(who, np.zeros((bd.OUT_H, bd.OUT_W), np.float32))
        acc[who] += s * blob(where(w), r)
    for who, h in acc.items():
        col = COL[who]; h = np.clip(h, 0, 1.3)
        c = (col / 255.0)[None, None, :] * np.clip(h, 0, 1)[..., None] ** 0.8 * 0.7
        c += np.clip(h - 0.85, 0, 1)[..., None] * 0.4
        B.fields += c.astype(np.float32)


def badge(B, xy, n, col):
    x, y = xy; r = 21; c = tuple(int(v) for v in col)
    B.ud.ellipse([x - r, y - r, x + r, y + r], fill=c + (255,), outline=(8, 14, 22, 255), width=3)
    dark = (10, 16, 26, 255) if sum(col) > 360 else (245, 250, 255, 255)
    B.ud.text((x, y + 1), str(n), font=F_BADGE, fill=dark, anchor='mm')


def wrap(d, s, f, width):
    words, out, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > width and cur:
            out.append(cur); cur = w
        else:
            cur = t
    out.append(cur); return out


def smooth(pts, n=200):
    from scipy.interpolate import splprep, splev
    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=0, k=min(3, len(pts) - 1))
    x, y = splev(np.linspace(0, 1, n), tck)
    return np.stack([x, y], 1)


def flow(B, f):
    col = COL[f['what']]
    pts = geo_out(f['pts'])
    if len(pts) > 3:
        pts = smooth(pts)
    dep = f.get('dep', 2); w = {1: 4, 2: 8, 3: 13}[dep]
    if f.get('style') == 'contact':
        B.line(pts, col * 0.85, w=4, dash=(14, 12))
    else:
        B.line(pts, col * {1: 0.9, 2: 0.75, 3: 0.62}[dep], w=w, chevrons=f.get('arrows', False))
    B.fields += blob(tuple(pts[len(pts) // 2]), 3.0)[..., None] * (col / 255.0) * 0.3
    return tuple(pts[len(pts) // 2])


LABEL_AT = {'nam': (-100, 47), 'sam': (-60, -14), 'eur': (15, 51), 'afr': (20, 8), 'asi': (95, 37), 'oce': (134, -27),
            'centre': (110, 67), 'thw': (108, 66)}


def names(B, A=None):
    for k, ll in LABEL_AT.items():
        if A is not None and (k not in A or not A[k].any()):
            continue
        name = 'SIBERIA · THE THAW' if k == 'centre' else NAMEOF[k]
        x, y = P(*ll); col = COL[k]
        B.text((x, y), name, F_REG, tuple(int(c) for c in col), anchor='mm', stroke=5)
    for name, ll in (('THE ARCTIC', (-20, 77.5)), ('ANTARCTICA (SOUTH)', (20, -47))):
        x, y = P(*ll); B.text((x, y), name, F_REG, tuple(int(c) for c in CENTRE), anchor='mm', stroke=5)


def key_area(img):
    bg = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(bg).rectangle([0, MAP_H, img.width, img.height], fill=(4, 9, 16, 255))
    ImageDraw.Draw(bg).line([(0, MAP_H), (img.width, MAP_H)], fill=CYAN + (220,), width=3)
    img.alpha_composite(bg)


def item(B2, d, x0, x1, y, n, c, t, l):
    col = COL[c]; badge(B2, (x0 + 22, y + 22), n, col)
    B2.text((x0 + 56, y + 2), t, F_KT, tuple(int(v) for v in col), stroke=0)
    lines = wrap(d, l, F_KL, x1 - x0 - 60)
    for j, part in enumerate(lines):
        B2.text((x0 + 56, y + 44 + j * LH), part, F_KL, INK, stroke=0)
    return y + 50 + len(lines) * LH + 16


def render_setup(base, A, D):
    S = D.SETUP; B = bd.Board(base)
    territory(B, A, {})
    heat(B, S['hot'])
    badges = []
    for key, head, sub, items in S['sections']:
        for n, c, at, t, l in items:
            badges.append((where(at), n, COL[c]))
    names(B)
    img = B.compose().convert('RGBA')
    key_area(img)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    B2 = bd.Board(base); B2.ui = ov; B2.ud = d
    y0 = MAP_H + 28
    B2.text((40, y0), '2350 · SEASON 6 · THE WORLD', F_MONO, DIM, stroke=0)
    B2.text((40, y0 + 30), S['title'], F_TITLE, INK, stroke=0)
    B2.text((40, y0 + 100), S['sub'], F_SUBT, DIM, stroke=0)
    cols = [(40, 980), (1020, 1960), (2000, 2960)]
    ys = [y0 + 160, y0 + 28, y0 + 28]
    for i, (key, head, sub, items) in enumerate(S['sections']):
        ci = S['column'][i]; x0, x1 = cols[ci]; y = ys[ci]
        col = tuple(int(c) for c in COL[key])
        d.rectangle([x0, y + 6, x0 + 14, y + 32], fill=col + (255,))
        B2.text((x0 + 26, y), head, F_KT, col, stroke=0)
        B2.text((x0 + 26, y + 36), sub, F_REF, DIM, stroke=0); y += 70
        for n, c, at, t, l in items:
            y = item(B2, d, x0, x1, y, n, c, t, l)
        ys[ci] = y + 10
    for xy, n, col in badges:
        badge(B2, xy, n, col)
    img.alpha_composite(ov); return img.convert('RGB')


def zone(name):
    lon_lat = {
        'thaw_east': [(84, 49), (100, 50), (120, 48), (135, 46), (142, 52), (139, 58), (122, 61), (100, 59), (86, 56)],
        'thaw_west': [(58, 52), (70, 54), (84, 53), (87, 58), (81, 63), (70, 66), (60, 64)],
        'yenisei_towns': [(86, 58), (100, 58), (108, 62), (104, 69), (90, 70), (84, 64)],
        'west_towns_back': [(84, 57), (88, 58), (89, 63), (86, 66), (83, 62)],
        'thaw_north': [[(88, 66), (110, 63), (140, 60), (160, 62), (180, 62), (180, 72), (140, 74), (110, 78), (88, 76)],
                       [(-182, 62), (-166, 62), (-166, 72), (-182, 72)]],
    }[name]
    rings = lon_lat if isinstance(lon_lat[0], list) else [lon_lat]
    return gaussian_filter(bd.poly_mask(rings), 12) > 0.5


def apply_transfers(A, D, n):
    A2 = {k: v.copy() for k, v in A.items()}; fresh = []
    for i, era in enumerate(D.ERAS[:n]):
        for z, frm, to in era.get('transfers', []):
            zm = A['centre'] if z == 'thaw_all' else zone(z)
            m = zm & A2[frm]; A2[frm] &= ~m; A2[to] |= m
            if i == n - 1:
                fresh.append((m, frm))
    return A2, fresh


REF = []   # filled per era: [(name, (lon, lat), side)]


def ref_labels(B2, refs, avoid=()):
    for name, ll, side in refs:
        x, y = P(*ll)
        near = any((x - ax) ** 2 + (y - ay) ** 2 < 40 ** 2 for ax, ay in avoid)
        if near:
            B2.text((x, y + 38), name, F_REF, (225, 238, 248), anchor='mm', stroke=4); continue
        B2.ud.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(235, 245, 255, 235), outline=(8, 14, 22, 255), width=2)
        dx = 10 if side == 'r' else -10
        B2.text((x + dx, y), name, F_REF, (225, 238, 248), anchor='lm' if side == 'r' else 'rm', stroke=4)


def standing(B2, d, x0, x1, y, e, n, D):
    """Rival cards in brief: each bloc's standing now, with a bar and its change since last era."""
    B2.text((x0, y), 'WHERE EVERYONE STANDS', F_KT, tuple(int(c) for c in COL['key']), stroke=0); y += 44
    prev = D.ERAS[n - 2]['strength'] if n > 1 else {}
    for k in AREA:
        if k not in e['strength']:
            continue
        col = tuple(int(c) for c in AREA[k]); s = e['strength'].get(k, 1.0)
        B2.text((x0, y + 12), NAMEOF[k] + (' (YOU)' if k == D.PLAYER else ''), F_KL, col, anchor='lm', stroke=0)
        bx0, bx1 = x0 + 300, x1 - 70
        d.rectangle([bx0, y + 2, bx1, y + 22], outline=(70, 130, 150, 255), width=1)
        d.rectangle([bx0 + 1, y + 3, bx0 + (bx1 - bx0) * min(s / 1.8, 1), y + 21], fill=col + (255,))
        if k in prev:
            ch = s - prev[k]; tx, ty = bx1 + 26, y + 12
            if ch > 0.02:
                d.polygon([(tx - 9, ty + 7), (tx + 9, ty + 7), (tx, ty - 8)], fill=(120, 235, 150, 255))
            elif ch < -0.02:
                d.polygon([(tx - 9, ty - 7), (tx + 9, ty - 7), (tx, ty + 8)], fill=(255, 110, 95, 255))
            else:
                d.rectangle([tx - 8, ty - 2, tx + 8, ty + 2], fill=(150, 165, 180, 255))
        y += 36
    return y


def render_era(base, A, D, n):
    e = D.ERAS[n - 1]; B = bd.Board(base)
    A, fresh = apply_transfers(A, D, n)
    territory(B, A, e.get('strength'))
    for m, frm in fresh:
        hatch = ((bd.XS - bd.YS) // 8 % 3 == 0)
        B.fields += (m & hatch)[..., None] * (COL[frm] / 255.0) * 0.16
    for g in e.get('ghost', []):
        pts = geo_out(g['pts']); pts = smooth(pts) if len(pts) > 3 else pts
        B.line(pts, COL[g['what']] * 0.38, w=4)
    heat(B, e['hot'])
    for b in e['beats']:
        if 'flow' in b:
            b['_b'] = flow(B, b['flow'])
        else:
            xy = where(b['at']); col = COL[b['c']]
            h = np.clip(blob(xy, b.get('r', 4)) * b.get('s', 1.0), 0, 1.3)
            c = (col / 255.0)[None, None, :] * np.clip(h, 0, 1)[..., None] ** 0.8 * 0.75 + np.clip(h - 0.8, 0, 1)[..., None] * 0.45
            B.fields += c.astype(np.float32); b['_b'] = xy
    names(B, A)
    img = B.compose().convert('RGBA')
    key_area(img)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    B2 = bd.Board(base); B2.ui = ov; B2.ud = d
    y0 = MAP_H + 28
    B2.text((40, y0), '2350 · SEASON 6 · THE WORLD', F_MONO, DIM, stroke=0)
    B2.text((40, y0 + 30), f"ERA {e['n']} · {e['head']}", F_TITLE, INK, stroke=0)
    sub = wrap(d, f"{e['years']} · {e['line']}", F_SUBT, 940)
    for j, part in enumerate(sub):
        B2.text((40, y0 + 100 + j * 34), part, F_SUBT, DIM, stroke=0)
    y = y0 + 100 + len(sub) * 34 + 6
    if e.get('event'):
        B2.text((40, y), 'WORLD EVENT · ' + e['event'], F_SUBT, (255, 150, 70), stroke=0); y += 40
    y += 16
    standing(B2, d, 40, 980, y, e, n, D)
    cols = [(1020, 1960), (2000, 2960)]; ys = [y0 + 28, y0 + 28]
    half = (len(e['beats']) + 1) // 2
    for i, b in enumerate(e['beats']):
        ci = 0 if i < half else 1; x0, x1 = cols[ci]
        ys[ci] = item(B2, d, x0, x1, ys[ci], b['id'], b['c'], b['title'], b['line'])
    ref_labels(B2, e.get('refs', []), [b['_b'] for b in e['beats']])
    for b in e['beats']:
        badge(B2, b['_b'], b['id'], COL[b['c']])
    # timeline along the map's bottom edge
    tx0, tx1, tyy = 120, MAP_W - 120, MAP_H - 34
    d.line([(tx0, tyy), (tx1, tyy)], fill=CYAN + (200,), width=2)
    for i, era in enumerate(D.ERAS):
        xx = tx0 + (tx1 - tx0) * i / (len(D.ERAS) - 1); done = i < n; cur = i == n - 1
        r = 11 if cur else 7
        d.ellipse([xx - r, tyy - r, xx + r, tyy + r], fill=(255, 255, 255, 255) if cur else ((90, 210, 235, 255) if done else (40, 70, 85, 255)))
        B2.text((xx, tyy - 24), era['n'], F_MONO, INK if done else DIM, anchor='mm', stroke=3)
        if era.get('event') and done:
            B2.text((xx, tyy + 20), era['event'], F_EVT, (255, 150, 70), anchor='mm', stroke=3)
    img.alpha_composite(ov); return img.convert('RGB')


def main():
    base_path, out_dir = sys.argv[1], Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)
    base, A = setup(base_path)
    import season6 as D
    for w in sys.argv[3:]:
        if w == 'setup':
            render_setup(base, A, D).save(out_dir / 'season6_setup.jpg', quality=92); print('saved setup'); continue
        render_era(base, A, D, int(w)).save(out_dir / f'season6_era{int(w)}.jpg', quality=92); print('saved', w)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""2350, season 6 finale: the world in 2350, each bloc's verdict ring on the map, standing by era, the verdict and the arcs.
  python3 finale.py base/base_global_v1.jpg out/season6_finale.jpg
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
import world_board as SB
import season6 as D
from card import ring, GREY, LET

bd = SB.bd


def main():
    base_path, out = sys.argv[1], sys.argv[2]
    base, A = SB.setup(base_path)
    F = D.FINALE; last = D.ERAS[9]
    A, _ = SB.apply_transfers(A, D, 10)
    B = bd.Board(base)
    SB.territory(B, A, last['strength'])
    for g in F['networks']:
        pts = SB.geo_out(g['pts']); pts = SB.smooth(pts) if len(pts) > 3 else pts
        B.line(pts, SB.COL[g['what']] * 0.7, w=7)
    SB.heat(B, [((60, 8), 'STAR', 0.35, 16), ('india', 'ICE', 0.35, 7), ('siberia', 'thw', 0.3, 12), ('eastchina', 'asi', 0.3, 6)])
    for name, ll in (('THE ARCTIC', (-20, 77.5)), ('ANTARCTICA (SOUTH)', (20, -47))):
        x, y = SB.P(*ll); B.text((x, y), name, SB.F_REG, tuple(int(c) for c in SB.CENTRE), anchor='mm', stroke=5)
    img = B.compose().convert('RGBA')
    SB.key_area(img)
    ring_at = {'nam': (-102, 50), 'sam': (-60, -12), 'eur': (12, 50), 'afr': (20, 6), 'asi': (92, 34), 'oce': (134, -26), 'thw': (110, 64)}
    for k, (dv, oo, ld) in F['verdict'].items():
        x, y = SB.P(*ring_at[k]); col = tuple(int(c) for c in SB.AREA[k])
        big = k == D.PLAYER
        r0, r1 = (52, 84) if big else (38, 62)
        ring(img, x, y, r0, r1, [(100, dv, oo, ld)], col, glow=big, hatch_px=6)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    B2 = bd.Board(base); B2.ui = ov; B2.ud = d
    F_PCT = SB.font('Rajdhani-700', 40); F_PCTB = SB.font('Rajdhani-700', 54)
    for k, (dv, oo, ld) in F['verdict'].items():
        x, y = SB.P(*ring_at[k]); col = tuple(int(c) for c in SB.AREA[k]); big = k == D.PLAYER
        p = round(100 * dv / (100 - oo))
        B2.text((x, y + 2), f'{p}%', F_PCTB if big else F_PCT, SB.INK, anchor='mm', stroke=4)
        B2.text((x, y + (112 if big else 88)), SB.NAMEOF[k] + (' (YOU)' if big else ''), SB.F_REG, col, anchor='mm', stroke=5)

    y0 = SB.MAP_H + 28
    B2.text((40, y0), '2350 · SEASON 6 · THE WORLD · 2350', SB.F_MONO, SB.DIM, stroke=0)
    B2.text((40, y0 + 30), F['title'], SB.F_TITLE, SB.INK, stroke=0)
    B2.text((40, y0 + 100), F['sub'], SB.F_SUBT, SB.DIM, stroke=0)
    # standing by era
    cx0, cx1, cy0, cy1 = 90, 960, y0 + 200, y0 + 690
    B2.text((40, y0 + 150), 'STANDING BY ERA', SB.F_KT, tuple(int(c) for c in SB.COL['key']), stroke=0)
    d.rectangle([cx0, cy0, cx1, cy1], outline=(50, 90, 110, 255), width=1)
    smax = 1.7
    for i, e in enumerate(D.ERAS):
        xx = cx0 + (cx1 - cx0) * i / 9
        d.line([(xx, cy0), (xx, cy1)], fill=(30, 55, 70, 255), width=1)
        B2.text((xx, cy1 + 22), e['n'], SB.F_MONO, SB.DIM, anchor='mm', stroke=0)
        if e.get('event'):
            d.polygon([(xx - 8, cy0 - 4), (xx + 8, cy0 - 4), (xx, cy0 + 9)], fill=(255, 150, 70, 255))
    for k in SB.AREA:
        pts = [(cx0 + (cx1 - cx0) * i / 9, cy1 - (cy1 - cy0) * (e['strength'][k] - 0.5) / (smax - 0.5))
               for i, e in enumerate(D.ERAS) if k in e['strength']]
        col = tuple(int(c) for c in SB.AREA[k])
        d.line(pts, fill=col + (255,), width=6 if k == D.PLAYER else 3, joint='curve')
        d.ellipse([pts[-1][0] - 6, pts[-1][1] - 6, pts[-1][0] + 6, pts[-1][1] + 6], fill=col + (255,))
    B2.text((cx0, cy1 + 52), '▲ marks an era a world event fired', SB.F_REF, SB.DIM, stroke=0) if False else None
    B2.text((cx0, cy1 + 52), 'Orange marks: a draft card fired that era (III, V, X).', SB.F_REF, SB.DIM, stroke=0)
    # verdict bars
    vx0, vx1 = 1040, 1940; y = y0 + 28
    B2.text((vx0, y), 'THE VERDICT', SB.F_KT, tuple(int(c) for c in SB.COL['key']), stroke=0); y += 46
    B2.text((vx0, y), 'Each people’s 100: delivered · out of reach (the world) · let down', SB.F_REF, SB.DIM, stroke=0); y += 46
    order = sorted(F['verdict'], key=lambda k: -F['verdict'][k][0] / (100 - F['verdict'][k][1]))
    for k in order:
        dv, oo, ld = F['verdict'][k]; col = tuple(int(c) for c in SB.AREA[k]); p = round(100 * dv / (100 - oo))
        B2.text((vx0, y), SB.NAMEOF[k] + (' (YOU)' if k == D.PLAYER else ''), SB.F_KL, col, stroke=0)
        B2.text((vx1, y), f'{p}%', SB.F_KT, SB.INK, anchor='ra', stroke=0)
        bx0, bx1, by = vx0, vx1, y + 38; cxp = bx0
        for v, c in ((dv, col), (oo, GREY), (ld, LET)):
            if v:
                w = (bx1 - bx0) * v / 100
                d.rectangle([cxp, by, cxp + w, by + 18], fill=c + (255,))
                if c == GREY:
                    for hx in range(int(cxp), int(cxp + w), 8):
                        d.line([(hx, by + 18), (min(hx + 8, cxp + w), by)], fill=(70, 78, 92, 255), width=2)
                cxp += w
        y += 86
    # arcs
    ax0, ax1 = 2020, 2960; y = y0 + 28
    B2.text((ax0, y), 'THE CENTURY', SB.F_KT, tuple(int(c) for c in SB.COL['key']), stroke=0); y += 52
    for k in order:
        col = tuple(int(c) for c in SB.AREA[k])
        d.rectangle([ax0, y + 6, ax0 + 10, y + 26], fill=col + (255,))
        lines = SB.wrap(d, F['arcs'][k], SB.F_KL, ax1 - ax0 - 26)
        for j, part in enumerate(lines):
            B2.text((ax0 + 24, y + j * SB.LH), part, SB.F_KL, SB.INK, stroke=0)
        y += len(lines) * SB.LH + 16
    B2.text((40, SB.bd.OUT_H - 44), F['draft'], SB.F_REF, (255, 170, 110), stroke=0)
    img.alpha_composite(ov); img.convert('RGB').save(out, quality=92); print('saved finale')


if __name__ == '__main__':
    main()

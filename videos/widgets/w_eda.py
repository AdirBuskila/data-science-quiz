# -*- coding: utf-8 -*-
"""Statistics / chart widgets for the eda-course videos (E01..E08). Every class is prefixed ed- so other courses'
widgets are untouched. Every number a widget draws is computed here from the data it is given (numpy, and the
course checker's conventions from tools/verify/needhelp/common.py: quartiles = medians of the halves, the median
left out when n is odd; fences Q1 - k*IQR, Q3 + k*IQR).

Ids (hidden elements start with class h; show()/hide() fade them):
  strip(pfx, vals)          a row of value boxes.  {pfx}-c{i} cell, {pfx}-k{i} ring on cell i, {pfx}-d{i} dimmed cell,
                            {pfx}-br-{name} a bracket under cells i0..i1 with a label (brackets=[(name, i0, i1, html)])
  NumLine(pfx, lo, hi, ...) a number line with stacked dots.  .dots(id, vals, kind) .mark(id, x, label, kind)
                            .band(id, a, b, kind) .svg()
  hist(pfx, data, edges)    a histogram from np.histogram.  {pfx}-b{i} bar i, {pfx}-n{i} its count
  boxplot(pfx, data, ...)   a horizontal box plot over a dot strip of the data.  {pfx}-pts {pfx}-lq1 {pfx}-lmd {pfx}-lq3 (value labels)
                            {pfx}-box {pfx}-med {pfx}-fl {pfx}-fh {pfx}-wl {pfx}-wr {pfx}-out
  scatter(pfx, xs, ys, ...) a scatter plot.  {pfx}-pts {pfx}-mx {pfx}-my (mean guides) {pfx}-qp / {pfx}-qn (quadrants
                            where the product of deviations is positive / negative) {pfx}-fit (least-squares line)
  table(pfx, head, rows)    an LTR table; cell (i, j) of the body has id {pfx}-r{i}c{j}; hide=set of column indexes
                            that start hidden; hrow=True hides whole body rows ({pfx}-r{i})
  icon(kind)                a small chart pictogram (hist, bar, scatter, box, pie, line, heat)
"""
import html as _html
import math

import numpy as np

from common import quartiles, median as cmedian   # course checker (SIM_PATHS)

CELL, GAP = 78, 10


def esc(s):
    return _html.escape(str(s), quote=True)


def _h(hidden):
    return " h" if hidden else ""


def fmt(v):
    """3 -> '3', 2.5 -> '2.5', 13.8333 -> '13.83'"""
    v = float(v)
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- course statistics (asserted against numpy)
def stats(vals):
    a = np.asarray(vals, float)
    q1, q2, q3 = quartiles(list(vals))
    assert q2 == np.median(a) == cmedian(list(vals))
    return {"n": len(a), "mean": float(a.mean()), "median": float(q2), "q1": float(q1), "q3": float(q3),
            "iqr": float(q3 - q1), "s": float(a.std(ddof=1)) if len(a) > 1 else 0.0, "sp": float(a.std(ddof=0))}


def fences(vals, k=1.5):
    S = stats(vals)
    return S["q1"] - k * S["iqr"], S["q3"] + k * S["iqr"]


def outliers(vals, k=1.5):
    lo, hi = fences(vals, k)
    return [v for v in vals if v < lo or v > hi]


# ---------------------------------------------------------------- a strip of value boxes
def strip(pfx, vals, hidden=False, brackets=(), cell=CELL, gap=GAP, size=40, label=None):
    n = len(vals)
    W = n * cell + (n - 1) * gap
    cells = []
    for i, v in enumerate(vals):
        x = i * (cell + gap)
        cells.append(f'<div id="{pfx}-c{i}" class="ed-cell{_h(hidden)}" style="left:{x}px;width:{cell}px;font-size:{size}px">'
                     f'<i id="{pfx}-d{i}" class="ed-dim h"></i><b>{esc(fmt(v) if not isinstance(v, str) else v)}</b>'
                     f'<i id="{pfx}-k{i}" class="ed-ring h"></i></div>')
    brs = []
    for name, i0, i1, lab in brackets:
        x = i0 * (cell + gap)
        w = (i1 - i0 + 1) * cell + (i1 - i0) * gap
        brs.append(f'<div id="{pfx}-br-{name}" class="ed-br h" style="left:{x}px;width:{w}px"><span>{lab}</span></div>')
    hb = 64 if brackets else 0
    lab = f'<div class="ed-slab">{label}</div>' if label else ""
    return (f'<div class="ed-strip" id="{pfx}" dir="ltr">{lab}<div class="ed-row" style="width:{W}px;height:{cell + 8 + hb}px">'
            f'{"".join(cells)}{"".join(brs)}</div></div>')


# ---------------------------------------------------------------- number line with stacked dots
class NumLine:
    def __init__(self, pfx, lo, hi, ticks, w=940, h=230, pad=40, dot=13, base=None):
        self.pfx, self.lo, self.hi, self.w, self.h, self.pad, self.r = pfx, lo, hi, w, h, pad, dot
        self.base = base if base is not None else h - 58
        self.ticks = ticks
        self.parts = {"band": [], "mark": [], "dot": []}

    def X(self, v):
        return self.pad + (v - self.lo) * (self.w - 2 * self.pad) / (self.hi - self.lo)

    def dots(self, id_, vals, kind="ink", hidden=False, each=False):
        """stacked dots (duplicates pile up). each=True: every dot also gets its own id {id_}-{i} (order of vals)"""
        seen, out = {}, []
        for i, v in enumerate(vals):
            k = seen.get(v, 0)
            seen[v] = k + 1
            cx, cy = self.X(v), self.base - self.r - 2 - k * (2 * self.r + 4)
            idt = f' id="{id_}-{i}"' if each else ""
            out.append(f'<circle{idt} class="ed-dot k-{kind}" cx="{cx:.1f}" cy="{cy:.1f}" r="{self.r}"/>')
        self.parts["dot"].append(f'<g id="{id_}" class="{_h(hidden).strip()}">{"".join(out)}</g>')
        return id_

    def mark(self, id_, v, label, kind="a", hidden=True, top=18, lift=0):
        x = self.X(v)
        self.parts["mark"].append(
            f'<g id="{id_}" class="{_h(hidden).strip()}"><line class="ed-mk k-{kind}" x1="{x:.1f}" x2="{x:.1f}" '
            f'y1="{top + 30 + lift:.1f}" y2="{self.base + 6:.1f}"/><text class="ed-mkl k-{kind}" x="{x:.1f}" y="{top + 22 + lift:.1f}">'
            f'{esc(label)}</text></g>')
        return id_

    def band(self, id_, a, b, kind="a", hidden=True, label=None):
        x0, x1 = self.X(a), self.X(b)
        lab = (f'<text class="ed-bl k-{kind}" x="{(x0 + x1) / 2:.1f}" y="44">{esc(label)}</text>'
               if label else "")
        self.parts["band"].append(f'<g id="{id_}" class="{_h(hidden).strip()}"><rect class="ed-band k-{kind}" x="{x0:.1f}" y="10" '
                                  f'width="{x1 - x0:.1f}" height="{self.base - 10:.1f}"/>{lab}</g>')
        return id_

    def svg(self):
        ax = [f'<line class="ed-ax" x1="{self.pad - 14}" x2="{self.w - self.pad + 14}" y1="{self.base}" y2="{self.base}"/>']
        for v in self.ticks:
            x = self.X(v)
            ax.append(f'<line class="ed-tk" x1="{x:.1f}" x2="{x:.1f}" y1="{self.base}" y2="{self.base + 10}"/>'
                      f'<text class="ed-tl" x="{x:.1f}" y="{self.base + 38}">{esc(fmt(v))}</text>')
        body = self.parts["band"] + ax + self.parts["mark"] + self.parts["dot"]
        return (f'<svg class="ed-svg" id="{self.pfx}" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'direction="ltr">{"".join(body)}</svg>')


# ---------------------------------------------------------------- histogram
def hist(pfx, data, edges, w=880, h=430, ymax=None, yticks=None, hidden=False, kind="a", xlabel=None):
    counts, e = np.histogram(np.asarray(data, float), bins=np.asarray(edges, float))
    assert counts.sum() == len(data), "every value must fall in a bin"
    counts = [int(c) for c in counts]
    ymax = ymax or max(counts) + 1
    pl, pr, pt, pb = 70, 30, 24, 64
    X = lambda v: pl + (v - edges[0]) * (w - pl - pr) / (edges[-1] - edges[0])
    Y = lambda v: pt + (ymax - v) * (h - pt - pb) / ymax
    out = []
    for t in (yticks or range(0, ymax + 1, max(1, ymax // 5))):
        out.append(f'<line class="ed-grid" x1="{pl}" x2="{w - pr}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/>'
                   f'<text class="ed-tl" x="{pl - 14}" y="{Y(t) + 9:.1f}" text-anchor="end">{t}</text>')
    for i, c in enumerate(counts):
        x0, x1 = X(edges[i]), X(edges[i + 1])
        out.append(f'<g id="{pfx}-b{i}" class="{_h(hidden).strip()}"><rect class="ed-bar k-{kind}" x="{x0 + 2:.1f}" y="{Y(c):.1f}" '
                   f'width="{x1 - x0 - 4:.1f}" height="{Y(0) - Y(c):.1f}"/>'
                   f'<text id="{pfx}-n{i}" class="ed-cnt" x="{(x0 + x1) / 2:.1f}" y="{Y(c) - 10:.1f}">{c}</text></g>')
    out.append(f'<line class="ed-ax" x1="{pl - 6}" x2="{w - pr + 6}" y1="{Y(0):.1f}" y2="{Y(0):.1f}"/>')
    for v in edges:
        out.append(f'<line class="ed-tk" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{Y(0):.1f}" y2="{Y(0) + 10:.1f}"/>'
                   f'<text class="ed-tl" x="{X(v):.1f}" y="{Y(0) + 38:.1f}">{fmt(v)}</text>')
    if xlabel:
        out.append(f'<text class="ed-tl" x="{w - pr}" y="{h - 2}" text-anchor="end">{esc(xlabel)}</text>')
    svg = (f'<svg class="ed-svg" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">'
           f'{"".join(out)}</svg>')
    return svg, counts


# ---------------------------------------------------------------- box plot
def boxplot(pfx, data, lo, hi, ticks, whis=1.5, w=940, h=330, show_pts=True):
    S = stats(data)
    flo, fhi = S["q1"] - whis * S["iqr"], S["q3"] + whis * S["iqr"]
    inside = [v for v in data if flo <= v <= fhi]
    out = [v for v in data if v < flo or v > fhi]
    wl, wr = min(inside), max(inside)          # whiskers: to the farthest data point inside the fences (matplotlib)
    NL = NumLine(pfx, lo, hi, ticks, w=w, h=h, base=h - 58, dot=11)
    X = NL.X
    by, bh = 130, 80                          # box top / height
    cy = by + bh / 2
    g = []
    if show_pts:
        seen = {}
        dots = []
        for v in data:
            k = seen.get(v, 0)
            seen[v] = k + 1
            dots.append(f'<circle class="ed-dot k-ink" cx="{X(v):.1f}" cy="{60 - k * 22:.1f}" r="10"/>')
        g.append(f'<g id="{pfx}-pts">{"".join(dots)}</g>')

    g.append(f'<rect id="{pfx}-box" class="ed-box h" x="{X(S["q1"]):.1f}" y="{by}" width="{X(S["q3"]) - X(S["q1"]):.1f}" height="{bh}"/>')
    g.append(f'<line id="{pfx}-med" class="ed-medl h" x1="{X(S["median"]):.1f}" x2="{X(S["median"]):.1f}" y1="{by}" y2="{by + bh}"/>')
    for id_, v in ((f"{pfx}-lq1", S["q1"]), (f"{pfx}-lmd", S["median"]), (f"{pfx}-lq3", S["q3"])):
        g.append(f'<text id="{id_}" class="ed-mkl k-{"b" if id_.endswith("md") else "a"} h" x="{X(v):.1f}" '
                 f'y="{by + bh + 30}">{fmt(v)}</text>')
    g.append(f'<g id="{pfx}-wl" class="h"><line class="ed-wh" x1="{X(wl):.1f}" x2="{X(S["q1"]):.1f}" y1="{cy}" y2="{cy}"/>'
             f'<line class="ed-wh" x1="{X(wl):.1f}" x2="{X(wl):.1f}" y1="{cy - 24}" y2="{cy + 24}"/></g>')
    g.append(f'<g id="{pfx}-wr" class="h"><line class="ed-wh" x1="{X(S["q3"]):.1f}" x2="{X(wr):.1f}" y1="{cy}" y2="{cy}"/>'
             f'<line class="ed-wh" x1="{X(wr):.1f}" x2="{X(wr):.1f}" y1="{cy - 24}" y2="{cy + 24}"/></g>')
    g.append(f'<g id="{pfx}-out" class="h">' + "".join(
        f'<circle class="ed-odot" cx="{X(v):.1f}" cy="{cy}" r="13"/>' for v in out) + "</g>")
    for id_, v, lab, kind in ((f"{pfx}-fl", flo, f"{fmt(flo)}", "b"), (f"{pfx}-fh", fhi, f"{fmt(fhi)}", "b")):
        if lo <= v <= hi:
            g.append(f'<g id="{id_}" class="h"><line class="ed-fence" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{by - 8}" y2="{NL.base}"/>'
                     f'<text class="ed-mkl k-b" x="{X(v):.1f}" y="{by - 14}">{esc(lab)}</text></g>')
        else:
            g.append(f'<g id="{id_}" class="h"></g>')
    NL.parts["dot"] = g
    S.update(flo=flo, fhi=fhi, wl=wl, wr=wr, out=out)
    return NL.svg(), S


# ---------------------------------------------------------------- scatter plot
def scatter(pfx, xs, ys, xr, yr, w=620, h=480, xticks=(), yticks=(), r=11, hidden=False, labels=False, kind="ink",
            xname="x", yname="y"):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    pl, pr, pt, pb = 64, 26, 24, 60
    X = lambda v: pl + (v - xr[0]) * (w - pl - pr) / (xr[1] - xr[0])
    Y = lambda v: pt + (yr[1] - v) * (h - pt - pb) / (yr[1] - yr[0])
    mx, my = xs.mean(), ys.mean()
    o = []
    # quadrants around the means: (+,+) and (-,-) give positive products of deviations
    qp = (f'<rect class="ed-q k-ok" x="{X(mx):.1f}" y="{pt}" width="{w - pr - X(mx):.1f}" height="{Y(my) - pt:.1f}"/>'
          f'<rect class="ed-q k-ok" x="{pl}" y="{Y(my):.1f}" width="{X(mx) - pl:.1f}" height="{Y(yr[0]) - Y(my):.1f}"/>')
    qn = (f'<rect class="ed-q k-bad" x="{pl}" y="{pt}" width="{X(mx) - pl:.1f}" height="{Y(my) - pt:.1f}"/>'
          f'<rect class="ed-q k-bad" x="{X(mx):.1f}" y="{Y(my):.1f}" width="{w - pr - X(mx):.1f}" height="{Y(yr[0]) - Y(my):.1f}"/>')
    o.append(f'<g id="{pfx}-qp" class="h">{qp}</g><g id="{pfx}-qn" class="h">{qn}</g>')
    for t in yticks:
        o.append(f'<line class="ed-grid" x1="{pl}" x2="{w - pr}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/>'
                 f'<text class="ed-tl" x="{pl - 12}" y="{Y(t) + 9:.1f}" text-anchor="end">{fmt(t)}</text>')
    for t in xticks:
        o.append(f'<text class="ed-tl" x="{X(t):.1f}" y="{Y(yr[0]) + 38:.1f}">{fmt(t)}</text>'
                 f'<line class="ed-tk" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{Y(yr[0]):.1f}" y2="{Y(yr[0]) + 10:.1f}"/>')
    o.append(f'<line class="ed-ax" x1="{pl}" x2="{w - pr}" y1="{Y(yr[0]):.1f}" y2="{Y(yr[0]):.1f}"/>'
             f'<line class="ed-ax" x1="{pl}" x2="{pl}" y1="{pt}" y2="{Y(yr[0]):.1f}"/>'
             f'<text class="ed-an" x="{w - pr}" y="{Y(yr[0]) - 12:.1f}" text-anchor="end">{esc(xname)}</text>'
             f'<text class="ed-an" x="{pl + 12}" y="{pt + 26}">{esc(yname)}</text>')
    o.append(f'<g id="{pfx}-mx" class="h"><line class="ed-mk k-a" x1="{X(mx):.1f}" x2="{X(mx):.1f}" y1="{pt}" y2="{Y(yr[0]):.1f}"/>'
             f'<text class="ed-mkl k-a" x="{X(mx) + 10:.1f}" y="{pt + 26}" text-anchor="start">x̄ = {fmt(mx)}</text></g>')
    o.append(f'<g id="{pfx}-my" class="h"><line class="ed-mk k-a" x1="{pl}" x2="{w - pr}" y1="{Y(my):.1f}" y2="{Y(my):.1f}"/>'
             f'<text class="ed-mkl k-a" x="{w - pr - 4}" y="{Y(my) - 12:.1f}" text-anchor="end">ȳ = {fmt(my)}</text></g>')
    if len(xs) > 1 and xs.std() > 0:
        b, a = np.polyfit(xs, ys, 1)
        x0, x1 = xr[0], xr[1]
        o.append(f'<line id="{pfx}-fit" class="ed-fit h" x1="{X(x0):.1f}" x2="{X(x1):.1f}" y1="{Y(a + b * x0):.1f}" y2="{Y(a + b * x1):.1f}"/>')
    pts = []
    for i, (u, v) in enumerate(zip(xs, ys)):
        lab = (f'<text class="ed-pl" x="{X(u) + 16:.1f}" y="{Y(v) - 14:.1f}">({fmt(u)}, {fmt(v)})</text>' if labels else "")
        pts.append(f'<g id="{pfx}-p{i}"><circle class="ed-dot k-{kind}" cx="{X(u):.1f}" cy="{Y(v):.1f}" r="{r}"/>{lab}</g>')
    o.append(f'<g id="{pfx}-pts" class="{_h(hidden).strip()}">{"".join(pts)}</g>')
    return (f'<svg class="ed-svg" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">'
            f'{"".join(o)}</svg>')


def pearson_parts(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    dx, dy = xs - xs.mean(), ys - ys.mean()
    sxy, sxx, syy = float((dx * dy).sum()), float((dx * dx).sum()), float((dy * dy).sum())
    r = sxy / math.sqrt(sxx * syy)
    assert abs(r - np.corrcoef(xs, ys)[0, 1]) < 1e-12
    return dx, dy, sxy, sxx, syy, r


# ---------------------------------------------------------------- table
def table(pfx, head, rows, hide=(), hrow=False, size=32, cls=""):
    hide = set(hide)
    th = "".join(f"<th>{h}</th>" for h in head)
    body = []
    for i, row in enumerate(rows):
        tds = "".join(f'<td><span id="{pfx}-r{i}c{j}" class="{"h" if j in hide else ""}">{c}</span></td>'
                      for j, c in enumerate(row))
        body.append(f'<tr id="{pfx}-r{i}" class="{"h" if hrow else ""}">{tds}</tr>')
    return (f'<table class="ed-tab {cls}" id="{pfx}" dir="ltr" style="font-size:{size}px"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>')


# ---------------------------------------------------------------- chart pictograms (E07)
def icon(kind, w=200, h=140):
    o = []
    base = h - 18
    if kind == "hist":
        hs = [20, 48, 80, 100, 70, 38, 16]
        bw = (w - 20) / len(hs)
        for i, v in enumerate(hs):
            o.append(f'<rect class="ed-ib" x="{10 + i * bw:.1f}" y="{base - v}" width="{bw:.1f}" height="{v}"/>')
    elif kind == "bar":
        hs = [60, 96, 40, 76]
        for i, v in enumerate(hs):
            o.append(f'<rect class="ed-ib" x="{22 + i * 44}" y="{base - v}" width="30" height="{v}"/>')
    elif kind == "scatter":
        rng = np.random.default_rng(3)
        for _ in range(18):
            u = rng.uniform(0, 1)
            v = 0.8 * u + rng.normal(0, 0.1)
            o.append(f'<circle class="ed-id" cx="{18 + u * (w - 36):.1f}" cy="{base - 6 - max(0, min(1, v)) * (h - 40):.1f}" r="6"/>')
    elif kind == "box":
        for i, (a, q1, m, q3, b) in enumerate([(20, 50, 70, 95, 130), (40, 70, 90, 110, 160)]):
            y = 34 + i * 54
            o.append(f'<line class="ed-iw" x1="{a}" x2="{b}" y1="{y}" y2="{y}"/><rect class="ed-ibx" x="{q1}" y="{y - 16}" '
                     f'width="{q3 - q1}" height="32"/><line class="ed-iw" x1="{m}" x2="{m}" y1="{y - 16}" y2="{y + 16}"/>')
        o.append(f'<circle class="ed-id" cx="186" cy="34" r="6"/>')
    elif kind == "pie":
        cx, cy, R = w / 2, h / 2 - 2, 56
        fr = [0.45, 0.3, 0.25]
        a0 = -math.pi / 2
        for i, f in enumerate(fr):
            a1 = a0 + 2 * math.pi * f
            x0, y0, x1, y1 = cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1)
            o.append(f'<path class="ed-ip k{i}" d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 {1 if f > .5 else 0},1 {x1:.1f},{y1:.1f} Z"/>')
            a0 = a1
    elif kind == "line":
        ys = [30, 44, 40, 62, 58, 80, 92, 88]
        pts = " ".join(f"{14 + i * 25},{base - v}" for i, v in enumerate(ys))
        o.append(f'<polyline class="ed-il" points="{pts}"/>')
    elif kind == "heat":
        vals = [[1, .6, -.2, .1], [.6, 1, .3, -.5], [-.2, .3, 1, .7], [.1, -.5, .7, 1]]
        for i, row in enumerate(vals):
            for j, v in enumerate(row):
                col = f"rgba(45,212,191,{abs(v):.2f})" if v >= 0 else f"rgba(251,113,133,{abs(v):.2f})"
                o.append(f'<rect x="{40 + j * 30}" y="{8 + i * 30}" width="28" height="28" fill="{col}" rx="3"/>')
    if kind not in ("pie", "heat"):
        o.append(f'<line class="ed-iax" x1="8" x2="{w - 6}" y1="{base}" y2="{base}"/>')
    return f'<svg class="ed-icon" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{"".join(o)}</svg>'


def chart_card(id_, kind, name, hidden=True):
    return f'<div id="{id_}" class="ed-chart{_h(hidden)}">{icon(kind)}<div class="ed-cname">{name}</div></div>'


# ---------------------------------------------------------------- misc
def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="ed-chip {kind}{_h(hidden)}">{html_}</div>'


def eq(id_, tex, size=40, hidden=True):
    return f'<div id="{id_}" class="ed-eq{_h(hidden)}" style="font-size:{size}px">{tex}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


# ---------------------------------------------------------------- reading an exam scatter raster
def raster_corr(path, color, splits, min_px=15):
    """Pearson r of the dot centroids in each vertical slice of an exam figure (the dots found by color).
    color(r, g, b) -> bool mask. Returns [(number of dots, r)] per slice."""
    from PIL import Image
    from scipy import ndimage
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    m = color(a[..., 0], a[..., 1], a[..., 2])
    lab, n = ndimage.label(m)
    idx = range(1, n + 1)
    cs, sz = ndimage.center_of_mass(m, lab, idx), ndimage.sum(m, lab, idx)
    pts = [(c[1], -c[0]) for c, s in zip(cs, sz) if s > min_px]
    res = []
    for lo, hi in splits:
        P = np.array([(x, y) for x, y in pts if lo <= x < hi])
        res.append((len(P), float(np.corrcoef(P[:, 0], P[:, 1])[0, 1])))
    return res


# ---------------------------------------------------------------- pie and bar charts from data (E07)
PIE_COLORS = ["#38bdf8", "#fbbf24", "#f472b6", "#a78bfa", "#34d399", "#fb7185", "#c9cdf0", "#2dd4bf", "#f97316",
              "#818cf8", "#facc15", "#e879f9"]


def pie(pfx, vals, R=150, labels=None, pct=True):
    """slices in the given order, clockwise from 12 o'clock. Returns (svg, angles in degrees)."""
    tot = float(sum(vals))
    cx = cy = R + 60
    a0 = -math.pi / 2
    o, angles = [], []
    for i, v in enumerate(vals):
        f = v / tot
        a1 = a0 + 2 * math.pi * f
        angles.append(360 * f)
        x0, y0, x1, y1 = cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1)
        col = PIE_COLORS[i % len(PIE_COLORS)]
        o.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 {1 if f > .5 else 0},1 {x1:.1f},{y1:.1f} Z" '
                 f'fill="{col}" stroke="#0a0c18" stroke-width="2"/>')
        if pct:
            am = (a0 + a1) / 2
            lx, ly = cx + (R + 34) * math.cos(am), cy + (R + 34) * math.sin(am) + 9
            lab = labels[i] if labels else f"{round(100 * f)}%"
            o.append(f'<text class="ed-pl" x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" style="font-size:24px">{esc(lab)}</text>')
        a0 = a1
    S = 2 * (R + 60)
    return (f'<svg class="ed-svg" id="{pfx}" viewBox="0 0 {S} {S}" width="{S}" height="{S}" direction="ltr">'
            f'{"".join(o)}</svg>'), angles


def bars(pfx, names, vals, w=520, h=300, ymax=None):
    ymax = ymax or max(vals)
    pl, pb, pt = 20, 44, 20
    bw = (w - 2 * pl) / len(vals)
    o = []
    for i, (n, v) in enumerate(zip(names, vals)):
        bh = (h - pb - pt) * v / ymax
        x = pl + i * bw
        o.append(f'<rect x="{x + 3:.1f}" y="{h - pb - bh:.1f}" width="{bw - 6:.1f}" height="{bh:.1f}" '
                 f'fill="{PIE_COLORS[i % len(PIE_COLORS)]}"/>'
                 f'<text class="ed-tl" x="{x + bw / 2:.1f}" y="{h - pb + 30}" style="font-size:20px">{esc(n)}</text>')
    o.append(f'<line class="ed-ax" x1="{pl}" x2="{w - pl}" y1="{h - pb}" y2="{h - pb}"/>')
    return (f'<svg class="ed-svg" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">'
            f'{"".join(o)}</svg>')

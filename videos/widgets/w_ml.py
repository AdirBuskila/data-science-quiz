# -*- coding: utf-8 -*-
"""Model / evaluation widgets for the ml-course videos (M01..M07). Every class is prefixed ml- so other courses'
widgets are untouched. A widget only draws what it is given; every number (centroids, distances, votes, merge
heights, metrics) is computed and asserted in the video script or in the helpers below.

  Plot(pfx, xr, yr, ...)     2-D axes in data units (element ids are "<pfx>-<id>").  .pts(id, P, kinds) .centroid(id, x, y, kind) .links(id, P, C, assign)
                             .circle(id, x, y, rad) .fline(id, a, b) .segs(id, [(p, q)]) .text(id, x, y, s) .svg()
                             Every element is a group with the given id (hidden by default where it says so).
  dendro(pfx, vals, ...)     a dendrogram of 1-D values (scipy single/complete linkage).  {pfx}-m{i} = merge i (in
                             merge order), {pfx}-cut = a dashed cut line; returns (svg, Z)
  cmatrix(pfx, tp, fn, fp, tn) a 2x2 confusion matrix (Hebrew headers).  {pfx}-h-tp/fn/fp/tn cell highlights
  folds(pfx, k, n)           K-fold bars: round r = {pfx}-r{r}; the validation block of round r is {pfx}-v{r}
  tree(p, shown)             the "which kind of problem" decision tree (M01), ids <p>-q1 … (see the function)
  eq / chip / stem / code / note    small text helpers (as in the other courses)
"""
import html as _html
import math

import numpy as np

KINDS = ("a", "b", "c", "d", "ink", "bad", "ok", "mut")


def esc(s):
    return _html.escape(str(s), quote=True)


def _h(hidden):
    return "h" if hidden else ""


def fmt(v, nd=2):
    v = float(v)
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.{nd}f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- metrics (asserted against sklearn in the scripts)
def metrics(tp, fn, fp, tn):
    n = tp + fn + fp + tn
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return {"n": n, "acc": (tp + tn) / n, "prec": p, "rec": r, "f1": 2 * p * r / (p + r) if p + r else 0.0,
            "spec": tn / (tn + fp) if tn + fp else 0.0}


def round_half_up(v, nd=2):
    """the exams' "עיגול מתמטי": 0.875 -> 0.88 (Python's round() would give 0.88 or 0.87 depending on the float)"""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(v)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def kmeans_run(P, C0, iters=10):
    """Lloyd iterations by hand: [(centroids, assignment)] until the assignment stops changing.
    Each entry i holds the centroids used for assignment i and that assignment."""
    P = np.asarray(P, float)
    C = np.asarray(C0, float)
    out, prev = [], None
    for _ in range(iters):
        d = np.linalg.norm(P[:, None, :] - C[None, :, :], axis=2)
        srt = np.sort(d, axis=1)
        assert (srt[:, 1] - srt[:, 0] > 1e-9).all(), "a tie in the assignment step"
        a = d.argmin(axis=1)
        out.append((C.copy(), a.copy()))
        if prev is not None and (a == prev).all():
            break
        prev = a
        C = np.array([P[a == k].mean(axis=0) for k in range(len(C))])
    return out


def sse(P, C, a):
    P, C = np.asarray(P, float), np.asarray(C, float)
    return float(((P - C[a]) ** 2).sum())


def knn_vote(train, labels, q, k):
    """distances sorted (no ties allowed at the k-th place), the k nearest, and the majority label"""
    d = [(dist(p, q), i) for i, p in enumerate(train)]
    d.sort()
    if k < len(d):
        assert d[k][0] - d[k - 1][0] > 1e-9, "tie at the k-th neighbour"
    near = [i for _, i in d[:k]]
    votes = {}
    for i in near:
        votes[labels[i]] = votes.get(labels[i], 0) + 1
    best = sorted(votes.items(), key=lambda kv: -kv[1])
    assert len(best) == 1 or best[0][1] > best[1][1], "tied vote"
    return d, near, best[0][0], votes


# ---------------------------------------------------------------- 2-D plot
class Plot:
    def __init__(self, pfx, xr, yr, w=640, h=520, xticks=(), yticks=(), xname="x", yname="y", grid=True, pad=None):
        self.pfx, self.xr, self.yr, self.w, self.h = pfx, xr, yr, w, h
        self.pl, self.pr, self.pt, self.pb = pad or (64, 26, 24, 60)
        self.xticks, self.yticks, self.xname, self.yname, self.grid = xticks, yticks, xname, yname, grid
        self.layers = {"under": [], "mid": [], "pts": [], "top": []}

    def X(self, v):
        return self.pl + (v - self.xr[0]) * (self.w - self.pl - self.pr) / (self.xr[1] - self.xr[0])

    def Y(self, v):
        return self.pt + (self.yr[1] - v) * (self.h - self.pt - self.pb) / (self.yr[1] - self.yr[0])

    def _g(self, layer, id_, body, hidden):
        """every element id is prefixed with the plot's pfx: Plot("pa").pts("p0") -> id "pa-p0" """
        self.layers[layer].append(f'<g id="{self.pfx}-{id_}" class="{_h(hidden)}">{body}</g>')
        return f"{self.pfx}-{id_}"

    def pts(self, id_, P, kinds="ink", hidden=False, r=13, each=False, shapes=None, labels=None, lab_top=False):
        """kinds: one kind or one per point; shapes: 'o' circle / 's' square / 't' triangle per point;
        labels: text per point (or None) drawn above-right; each=True gives every point the id {id_}-{i}"""
        out = []
        for i, (x, y) in enumerate(P):
            k = kinds if isinstance(kinds, str) else kinds[i]
            sh = (shapes or "o" * len(P))[i]
            cx, cy = self.X(x), self.Y(y)
            if sh == "s":
                m = f'<rect class="ml-dot k-{k}" x="{cx - r:.1f}" y="{cy - r:.1f}" width="{2 * r}" height="{2 * r}" rx="3"/>'
            elif sh == "t":
                m = (f'<path class="ml-dot k-{k}" d="M{cx:.1f},{cy - r * 1.25:.1f} L{cx + r * 1.15:.1f},{cy + r * .8:.1f} '
                     f'L{cx - r * 1.15:.1f},{cy + r * .8:.1f} Z"/>')
            else:
                m = f'<circle class="ml-dot k-{k}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"/>'
            if labels and labels[i] and lab_top:
                m += f'<text class="ml-pl" x="{cx:.1f}" y="{cy - r - 10:.1f}" text-anchor="middle">{esc(labels[i])}</text>'
            elif labels and labels[i]:
                m += f'<text class="ml-pl" x="{cx + r + 4:.1f}" y="{cy - r - 2:.1f}">{esc(labels[i])}</text>'
            out.append(f'<g id="{self.pfx}-{id_}-{i}">{m}</g>' if each else m)
        return self._g("pts", id_, "".join(out), hidden)

    def centroid(self, id_, x, y, kind="a", hidden=True, label=None, size=17, lx=0, ly=0):
        cx, cy = self.X(x), self.Y(y)
        s = size
        body = (f'<path class="ml-cen k-{kind}" d="M{cx - s:.1f},{cy - s:.1f} L{cx + s:.1f},{cy + s:.1f} '
                f'M{cx + s:.1f},{cy - s:.1f} L{cx - s:.1f},{cy + s:.1f}"/>')
        if label:
            body += f'<text class="ml-cl k-{kind}" x="{cx + s + 6 + lx:.1f}" y="{cy + 9 + ly:.1f}">{esc(label)}</text>'
        return self._g("top", id_, body, hidden)

    def links(self, id_, P, C, assign, hidden=True, kinds=None):
        out = []
        for i, (x, y) in enumerate(P):
            c = C[assign[i]]
            k = (kinds or KINDS)[assign[i]]
            out.append(f'<line class="ml-link k-{k}" x1="{self.X(x):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(c[0]):.1f}" '
                       f'y2="{self.Y(c[1]):.1f}"/>')
        return self._g("under", id_, "".join(out), hidden)

    def circle(self, id_, x, y, rad, kind="a", hidden=True):
        rx = abs(self.X(x + rad) - self.X(x))
        ry = abs(self.Y(y + rad) - self.Y(y))
        return self._g("under", id_, f'<ellipse class="ml-circ k-{kind}" cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" '
                                     f'rx="{rx:.1f}" ry="{ry:.1f}"/>', hidden)

    def fline(self, id_, a, b, kind="b", hidden=True, x0=None, x1=None):
        """the line y = a + b·x across the plot"""
        x0 = self.xr[0] if x0 is None else x0
        x1 = self.xr[1] if x1 is None else x1
        return self._g("mid", id_, f'<line class="ml-fit k-{kind}" x1="{self.X(x0):.1f}" y1="{self.Y(a + b * x0):.1f}" '
                                   f'x2="{self.X(x1):.1f}" y2="{self.Y(a + b * x1):.1f}"/>', hidden)

    def segs(self, id_, S, kind="bad", hidden=True, cls="ml-res"):
        body = "".join(f'<line class="{cls} k-{kind}" x1="{self.X(p[0]):.1f}" y1="{self.Y(p[1]):.1f}" '
                       f'x2="{self.X(q[0]):.1f}" y2="{self.Y(q[1]):.1f}"/>' for p, q in S)
        return self._g("under", id_, body, hidden)

    def text(self, id_, x, y, s, kind="ink", hidden=True, anchor="middle", dx=0, dy=0, size=26):
        return self._g("top", id_, f'<text class="ml-tx k-{kind}" x="{self.X(x) + dx:.1f}" y="{self.Y(y) + dy:.1f}" '
                                   f'text-anchor="{anchor}" font-size="{size}">{esc(s)}</text>', hidden)

    def svg(self, hidden=False):
        o = []
        x0, x1 = self.X(self.xr[0]), self.X(self.xr[1])
        y0, y1 = self.Y(self.yr[0]), self.Y(self.yr[1])
        for t in self.yticks:
            if self.grid:
                o.append(f'<line class="ml-grid" x1="{x0:.1f}" x2="{x1:.1f}" y1="{self.Y(t):.1f}" y2="{self.Y(t):.1f}"/>')
            o.append(f'<text class="ml-tl" x="{x0 - 12:.1f}" y="{self.Y(t) + 9:.1f}" text-anchor="end">{fmt(t)}</text>')
        for t in self.xticks:
            if self.grid:
                o.append(f'<line class="ml-grid" x1="{self.X(t):.1f}" x2="{self.X(t):.1f}" y1="{y1:.1f}" y2="{y0:.1f}"/>')
            o.append(f'<text class="ml-tl" x="{self.X(t):.1f}" y="{y0 + 38:.1f}">{fmt(t)}</text>')
        o.append(f'<line class="ml-ax" x1="{x0:.1f}" x2="{x1:.1f}" y1="{y0:.1f}" y2="{y0:.1f}"/>')
        if self.yr[1] > self.yr[0] and self.yticks:
            o.append(f'<line class="ml-ax" x1="{x0:.1f}" x2="{x0:.1f}" y1="{y1:.1f}" y2="{y0:.1f}"/>')
        if self.xname:
            o.append(f'<text class="ml-an" x="{x1:.1f}" y="{y0 - 12:.1f}" text-anchor="end">{esc(self.xname)}</text>')
        if self.yname and self.yticks:
            o.append(f'<text class="ml-an" x="{x0 + 12:.1f}" y="{y1 + 26:.1f}">{esc(self.yname)}</text>')
        body = self.layers["under"] + self.layers["mid"] + self.layers["pts"] + self.layers["top"]
        return (f'<svg class="ml-svg {_h(hidden)}" id="{self.pfx}" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" direction="ltr">{"".join(o)}{"".join(body)}</svg>')


# ---------------------------------------------------------------- dendrogram
def dendro(pfx, vals, method="single", w=760, h=440, hmax=None, hticks=None, cut=None, hidden=False):
    """dendrogram of 1-D values. Merge i (row i of scipy's Z) has id {pfx}-m{i}; its height label {pfx}-l{i}."""
    from scipy.cluster.hierarchy import linkage, dendrogram
    X = np.asarray(vals, float).reshape(-1, 1)
    Z = linkage(X, method=method)
    hs = Z[:, 2]
    assert len(set(np.round(hs, 9))) == len(hs), "merge heights must be distinct (they map drawing -> merge)"
    D = dendrogram(Z, no_plot=True, labels=[fmt(v) for v in vals])
    hmax = hmax or float(hs.max()) * 1.1
    pl, pr, pt, pb = 70, 30, 26, 60
    xs = [x for ic in D["icoord"] for x in ic]
    lo, hi = min(xs), max(xs)
    X_ = lambda u: pl + 30 + (u - lo) * (w - pl - pr - 60) / (hi - lo)
    Y_ = lambda v: pt + (hmax - v) * (h - pt - pb) / hmax
    o = []
    for t in (hticks or []):
        o.append(f'<line class="ml-grid" x1="{pl}" x2="{w - pr}" y1="{Y_(t):.1f}" y2="{Y_(t):.1f}"/>'
                 f'<text class="ml-tl" x="{pl - 12}" y="{Y_(t) + 9:.1f}" text-anchor="end">{fmt(t)}</text>')
    o.append(f'<line class="ml-ax" x1="{pl}" x2="{pl}" y1="{pt}" y2="{Y_(0):.1f}"/>')
    merges = []
    for ic, dc in zip(D["icoord"], D["dcoord"]):
        i = int(np.argmin(np.abs(hs - dc[1])))
        d = " ".join(f"{'M' if j == 0 else 'L'}{X_(x):.1f},{Y_(y):.1f}" for j, (x, y) in enumerate(zip(ic, dc)))
        merges.append((i, f'<g id="{pfx}-m{i}" class="h"><path class="ml-den" d="{d}"/>'
                          f'<text id="{pfx}-l{i}" class="ml-dl" x="{X_((ic[1] + ic[2]) / 2) + 12:.1f}" y="{Y_(dc[1]) - 12:.1f}" '
                          f'text-anchor="start">'
                          f'{fmt(dc[1])}</text></g>'))
    o += [m for _, m in sorted(merges)]
    for j, lab in enumerate(D["ivl"]):
        x = X_(5 + 10 * j)
        o.append(f'<circle class="ml-dot k-ink" cx="{x:.1f}" cy="{Y_(0):.1f}" r="9"/>'
                 f'<text class="ml-leaf" x="{x:.1f}" y="{Y_(0) + 42:.1f}">{esc(lab)}</text>')
    if cut is not None:
        o.append(f'<g id="{pfx}-cut" class="h"><line class="ml-cut" x1="{pl}" x2="{w - pr}" y1="{Y_(cut):.1f}" '
                 f'y2="{Y_(cut):.1f}"/></g>')
    svg = (f'<svg class="ml-svg {_h(hidden)}" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">'
           f'{"".join(o)}</svg>')
    return svg, Z, D["ivl"]


# ---------------------------------------------------------------- confusion matrix
def cmatrix(pfx, tp, fn, fp, tn, pos="חיובי", neg="שלילי", size=34, hidden=False, values=True):
    def cell(tag, v, cls):
        val = f'<b>{v}</b>' if values else ""
        return (f'<td class="ml-cm {cls}"><i id="{pfx}-h-{tag}" class="ml-cmh h"></i>'
                f'<span class="ml-cmt">{tag.upper()}</span>{val}</td>')
    return (f'<table class="ml-cmx {_h(hidden)}" id="{pfx}" style="font-size:{size}px"><thead><tr><th></th>'
            f'<th>חזוי {pos}</th><th>חזוי {neg}</th></tr></thead><tbody>'
            f'<tr><th>באמת {pos}</th>{cell("tp", tp, "ok")}{cell("fn", fn, "bad")}</tr>'
            f'<tr><th>באמת {neg}</th>{cell("fp", fp, "bad")}{cell("tn", tn, "ok")}</tr></tbody></table>')


# ---------------------------------------------------------------- K-fold bars
def folds(pfx, k, n, w=820, hidden_rows=True):
    size = n // k
    assert size * k == n
    rows = []
    bw = w / k
    for r in range(k):
        cells = []
        for j in range(k):
            cls = "val" if j == r else "trn"
            idt = f' id="{pfx}-v{r}"' if j == r else ""
            cells.append(f'<div{idt} class="ml-fold {cls}" style="width:{bw - 8:.0f}px">'
                         f'{"תיקוף" if j == r else "אימון"} · {size}</div>')
        rows.append(f'<div id="{pfx}-r{r}" class="ml-frow {"h" if hidden_rows else ""}">'
                    f'<span class="ml-fr">סבב {r + 1}</span>{"".join(cells)}</div>')
    return f'<div class="ml-folds" id="{pfx}">{"".join(rows)}</div>'


# ---------------------------------------------------------------- M01 decision tree
def tree(p="t", shown=False):
    """ids <p>-q1 <p>-yes <p>-no <p>-q2 <p>-q3 <p>-cls <p>-reg <p>-clu <p>-dim; all but q1 start hidden unless shown;
    <p>-hl-<name> is a highlight ring on box <name>"""
    def box(name, html_, cls="", hidden=False):
        return (f'<div id="{p}-{name}" class="ml-tb {cls} {_h(hidden and not shown)}">'
                f'<i id="{p}-hl-{name}" class="ml-thl h"></i>{html_}</div>')
    return ('<div class="ml-tree">'
            + box("q1", "יש <b>תווית</b>?", "q")
            + '<div class="ml-tr2">'
            + '<div class="ml-tcol">' + box("yes", "כן ← <b>מונחית</b>", "y", True)
            + box("q2", "התווית: קטגוריה או מספר?", "q", True)
            + '<div class="ml-tr3">' + box("cls", "קטגוריה<br><b>סיווג</b>", "leaf", True)
            + box("reg", "מספר<br><b>רגרסיה</b>", "leaf", True) + "</div></div>"
            + '<div class="ml-tcol">' + box("no", "לא ← <b>לא מונחית</b>", "n", True)
            + box("q3", "קבוצות, או פחות עמודות?", "q", True)
            + '<div class="ml-tr3">' + box("clu", "קבוצות<br><b>אשכול</b>", "leaf", True)
            + box("dim", "פחות עמודות<br><b>הורדת ממדים</b>", "leaf", True) + "</div></div>"
            + "</div></div>")


# ---------------------------------------------------------------- misc
def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="ml-chip {kind} {_h(hidden)}">{html_}</div>'


def eq(id_, tex, size=40, hidden=True):
    return f'<div id="{id_}" class="ml-eq {_h(hidden)}" style="font-size:{size}px">{tex}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def code(id_, html_, hidden=False, size=30):
    return f'<div id="{id_}" class="ml-code {_h(hidden)}" style="font-size:{size}px">{html_}</div>'


def note(html_, id_=None, hidden=False):
    i = f' id="{id_}"' if id_ else ""
    return f'<div{i} class="ml-note {_h(hidden)}">{html_}</div>'


def table(pfx, head, rows, hide_rows=True, size=30):
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "".join(f'<tr id="{pfx}-r{i}" class="{"h" if hide_rows else ""}">' + "".join(f"<td>{c}</td>" for c in row)
                   + "</tr>" for i, row in enumerate(rows))
    return (f'<table class="ml-tab" id="{pfx}" style="font-size:{size}px"><thead><tr>{th}</tr></thead>'
            f'<tbody>{body}</tbody></table>')

# -*- coding: utf-8 -*-
"""Widgets for the cleaning-course videos (C01..C07): a DataFrame table whose cells highlight / change / get struck,
pandas code blocks that are really executed, an output box, the measurement-scale ladder, and a number line for
outlier fences. Every class is prefixed cl- (all widget css files load into every video of the app).

Ids:
  frame(pfx, df, after=None, extra=())
      {pfx}-v-{i}-{j}   the value of cell (row position i, column position j)
      {pfx}-n-{i}-{j}   the new value drawn over it (only where `after` differs from df), hidden
      {pfx}-h-{i}-{j}   highlight of the cell, hidden          {pfx}-hh-{j}  highlight of the column header
      {pfx}-s-{i}-{j}   strike over the cell (j = "i" for the index cell), hidden: a dropped row
      {pfx}-e{k}h / {pfx}-e{k}-{i}   extra column k (header / cell i), hidden: isnull flags, duplicated() output …
  code(pfx, src)    {pfx}-l{k} line k (hidden when hidden=True)
  out(pfx, text)    the printed output of a block
  ladder(pfx)       {pfx}-r{k} rung k (0 nominal … 3 ratio), {pfx}-x{k} its example
  numline(pfx, …)   {pfx}-p{k} point k, {pfx}-o{k} ring on point k, {pfx}-f0 / {pfx}-f1 fences, {pfx}-box Q1..Q3
"""
import contextlib
import html as _html
import io
import math
import re

import numpy as np
import pandas as pd

LATIN = re.compile(r"[A-Za-z]")


def esc(s):
    return _html.escape(str(s), quote=True)


def _h(hidden):
    return " h" if hidden else ""


def fmt(v):
    """cell text: NaN -> 'NaN', 3.0 -> '3', 6.6667 -> '6.67', strings as they are"""
    if isinstance(v, str):
        return v
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "NaN"
    if isinstance(v, (bool, np.bool_)):
        return str(bool(v))
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    v = float(v)
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _isnan(v):
    return v is None or (isinstance(v, float) and math.isnan(v))


# ---------------------------------------------------------------- running the code that is shown
def run(src, env=None):
    """exec the code exactly as it is shown; returns (env, printed text)"""
    env = {"pd": pd, "np": np} if env is None else env
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(src, env)
    return env, buf.getvalue().rstrip("\n")


# ---------------------------------------------------------------- DataFrame table
def frame(pfx, df, after=None, extra=(), hidden=False, size=32, cw=118, index=True, cls=""):
    """df as a table. after: a DataFrame of the same shape; cells that differ get a hidden new value on top.
    extra: [(header_html, [cell_html per row])] extra columns at the right, all hidden."""
    cols = list(df.columns)
    head = ('<th class="cl-ix"></th>' if index else "") + "".join(
        f'<th style="width:{cw}px"><i id="{pfx}-hh-{j}" class="cl-hi h"></i><span>{esc(c)}</span></th>'
        for j, c in enumerate(cols))
    head += "".join(f'<th class="cl-ex"><span id="{pfx}-e{k}h" class="h">{h}</span></th>' for k, (h, _) in enumerate(extra))
    body = []
    for i in range(len(df)):
        tds = []
        if index:
            tds.append(f'<th class="cl-ix"><span>{esc(df.index[i])}</span><i id="{pfx}-s-{i}-i" class="cl-strike h"></i></th>')
        for j, c in enumerate(cols):
            v = df.iat[i, j]
            nan = " cl-nan" if _isnan(v) else ""
            new = ""
            if after is not None:
                a = after.iat[i, j]
                same = (_isnan(a) and _isnan(v)) or (not _isnan(a) and not _isnan(v) and fmt(a) == fmt(v))
                if not same:
                    new = f'<b id="{pfx}-n-{i}-{j}" class="cl-new h">{esc(fmt(a))}</b>'
            tds.append(f'<td><i id="{pfx}-h-{i}-{j}" class="cl-hi h"></i>'
                       f'<span id="{pfx}-v-{i}-{j}" class="cl-val{nan}">{esc(fmt(v))}</span>{new}'
                       f'<i id="{pfx}-s-{i}-{j}" class="cl-strike h"></i></td>')
        for k, (_, cells) in enumerate(extra):
            tds.append(f'<td class="cl-ex"><span id="{pfx}-e{k}-{i}" class="h">{cells[i]}</span></td>')
        body.append(f'<tr>{"".join(tds)}</tr>')
    return (f'<table class="cl-df {cls}{_h(hidden)}" id="{pfx}" dir="ltr" style="font-size:{size}px">'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>')


def ids(pfx, kind, cells):
    """[(i, j)] -> ['{pfx}-{kind}-{i}-{j}', …]"""
    return [f"{pfx}-{kind}-{i}-{j}" for i, j in cells]


def row_strike(pfx, df, i, index=True):
    return ([f"{pfx}-s-{i}-i"] if index else []) + [f"{pfx}-s-{i}-{j}" for j in range(df.shape[1])]


def nan_cells(df):
    return [(i, j) for i in range(df.shape[0]) for j in range(df.shape[1]) if _isnan(df.iat[i, j])]


def changed(df, after):
    return [(i, j) for i in range(df.shape[0]) for j in range(df.shape[1])
            if not ((_isnan(after.iat[i, j]) and _isnan(df.iat[i, j])) or
                    (not _isnan(after.iat[i, j]) and not _isnan(df.iat[i, j]) and fmt(after.iat[i, j]) == fmt(df.iat[i, j])))]


def flag(v):
    return f'<b class="cl-t">True</b>' if v else '<b class="cl-f">False</b>'


# ---------------------------------------------------------------- code and output
KW = r"\b(import|as|from|for|in|if|else|True|False|None|lambda|print)\b"


def _hl(line):
    out, pos = [], 0
    for m in re.finditer(r"('[^']*'|\"[^\"]*\"|#.*$)", line):
        out.append(_hl_plain(line[pos:m.start()]))
        cls = "cl-cm" if m.group(0).startswith("#") else "cl-str"
        out.append(f'<span class="{cls}">{esc(m.group(0))}</span>')
        pos = m.end()
    out.append(_hl_plain(line[pos:]))
    return "".join(out)


def _hl_plain(s):
    s = esc(s)
    s = re.sub(KW, r'<span class="cl-kw">\1</span>', s)
    s = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)", r'<span class="cl-num">\1</span>', s)
    return s


def code(pfx, src, hidden=False, size=30, lines_hidden=False):
    lines = src.split("\n")
    body = "".join(f'<div id="{pfx}-l{k}" class="cl-ln{_h(lines_hidden)}">{_hl(l) or "&nbsp;"}</div>'
                   for k, l in enumerate(lines))
    return f'<div class="cl-code{_h(hidden)}" id="{pfx}" dir="ltr" style="font-size:{size}px">{body}</div>'


def out(pfx, text, hidden=True, size=28, label="פלט"):
    """label: Hebrew text, or code (no Hebrew letters: drawn LTR)"""
    if not re.search(r"[֐-׿]", label):
        label = f'<bdi dir="ltr" class="cl-mono">{label}</bdi>'
    body = "".join(f'<div>{esc(l) or "&nbsp;"}</div>' for l in text.split("\n"))
    return (f'<div class="cl-out{_h(hidden)}" id="{pfx}" style="font-size:{size}px"><span class="cl-olab">{label}</span>'
            f'<div class="cl-obody" dir="ltr">{body}</div></div>')


# ---------------------------------------------------------------- the scale ladder
SCALES = ["nominal", "ordinal", "interval", "ratio"]
SCALE_HE = {"nominal": "שמי", "ordinal": "סדר", "interval": "רווח", "ratio": "מנה"}
OPS = {"nominal": ["שכיח"], "ordinal": ["שכיח", "חציון"], "interval": ["שכיח", "חציון", "ממוצע", "הפרשים"],
       "ratio": ["שכיח", "חציון", "ממוצע", "הפרשים", "יחסים"]}
PROPS = {"nominal": "שמות בלבד", "ordinal": "יש סדר", "interval": "מרווחים שווים", "ratio": "אפס אמיתי"}
for _k in range(1, 4):            # each scale keeps every operation of the one below and adds new ones
    assert set(OPS[SCALES[_k - 1]]) < set(OPS[SCALES[_k]])


def new_ops(scale):
    k = SCALES.index(scale)
    return OPS[scale] if k == 0 else [o for o in OPS[scale] if o not in OPS[SCALES[k - 1]]]


def ladder(pfx, examples=None, hidden=True):
    """four rungs, ratio on top; each rung: name, defining property, the operations it adds; examples: {scale: html}"""
    examples = examples or {}
    rungs = []
    for k in reversed(range(4)):
        s = SCALES[k]
        ops = "".join(f'<span class="cl-op">{"+ " if k else ""}{o}</span>' for o in new_ops(s))
        ex = f'<span id="{pfx}-x{k}" class="cl-rex h">{examples[s]}</span>' if s in examples else ""
        rungs.append(f'<div id="{pfx}-r{k}" class="cl-rung k{k}{_h(hidden)}" style="margin-left:{200 + k * 30}px">'
                     f'<span class="cl-rname">{SCALE_HE[s]}</span><span class="cl-ren">{s}</span>'
                     f'<span class="cl-rprop">{PROPS[s]}</span><span class="cl-rops">{ops}</span>{ex}</div>')
    return f'<div class="cl-ladder" id="{pfx}">{"".join(rungs)}</div>'


# ---------------------------------------------------------------- number line
def numline(pfx, vals, lo, hi, ticks, w=940, h=230, fences=None, box=None, hidden=False, labels=None):
    """points of vals on [lo, hi]; equal values stack. fences=(f0, f1) dashed lines; box=(q1, q3) a band."""
    pad = 40
    X = lambda v: pad + (v - lo) / (hi - lo) * (w - 2 * pad)
    base = h - 70
    o = [f'<line class="cl-ax" x1="{pad - 20}" x2="{w - pad + 20}" y1="{base}" y2="{base}"/>']
    for t in ticks:
        o.append(f'<line class="cl-tk" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{base}" y2="{base + 12}"/>'
                 f'<text class="cl-tl" x="{X(t):.1f}" y="{base + 42}">{fmt(t)}</text>')
    if box:
        o.append(f'<rect id="{pfx}-box" class="cl-band h" x="{X(box[0]):.1f}" y="{base - 120}" '
                 f'width="{X(box[1]) - X(box[0]):.1f}" height="120"/>')
    if fences:
        for k, f in enumerate(fences):
            lab = (labels or {}).get(k, fmt(f))
            o.append(f'<g id="{pfx}-f{k}" class="h"><line class="cl-fence" x1="{X(f):.1f}" x2="{X(f):.1f}" '
                     f'y1="{base - 150}" y2="{base + 8}"/><text class="cl-fl" x="{X(f):.1f}" y="{base - 160}">{esc(lab)}</text></g>')
    seen = {}
    for k, v in enumerate(vals):
        n = seen.get(v, 0)
        seen[v] = n + 1
        y = base - 22 - n * 34
        o.append(f'<circle id="{pfx}-p{k}" class="cl-pt" cx="{X(v):.1f}" cy="{y}" r="14"/>'
                 f'<circle id="{pfx}-o{k}" class="cl-ring h" cx="{X(v):.1f}" cy="{y}" r="24"/>')
    return (f'<svg class="cl-svg{_h(hidden)}" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'direction="ltr">{"".join(o)}</svg>')


# ---------------------------------------------------------------- layout helpers
def stack(*items, gap=24, cls=""):
    return f'<div class="cl-stack {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def row(*items, gap=30, cls=""):
    return f'<div class="cl-rowf {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def big(id_, html_, hidden=True, size=44):
    return f'<div id="{id_}" class="cl-big{_h(hidden)}" style="font-size:{size}px">{html_}</div>'


def chip(id_, html_, kind="ok", hidden=True):
    return f'<div id="{id_}" class="cl-chip {kind}{_h(hidden)}">{html_}</div>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def mono(s):
    return f'<span class="cl-mono">{esc(s)}</span>'


# ---------------------------------------------------------------- script checks
def no_latin(scenes):
    """the voice misreads Latin letters: every spoken phrase must be Hebrew (and digits) only"""
    bad = [(S.key, p.say) for S in scenes for p in S.phrases if LATIN.search(p.say)]
    assert not bad, "Latin letters in spoken text:\n" + "\n".join(f"  [{k}] {s}" for k, s in bad)


def swap(h, *layers):
    """several elements sharing one spot (show one, hide the previous): stage.css .swap"""
    return f'<div class="swap" style="--swap-h:{h}px">' + "".join(f"<div>{x}</div>" for x in layers) + "</div>"

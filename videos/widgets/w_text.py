# -*- coding: utf-8 -*-
"""Regex / text widgets for the text-course videos (T01..T08). Every class is prefixed tx- so other courses'
widgets are untouched. Every highlight a widget draws comes from a real `re` run (finditer / search / split) done
here on the exact string shown; every Bag-of-Words number from sklearn's CountVectorizer (the course checker,
tools/verify/needhelp/text/check.py, uses the same).

Regex and code are Latin/LTR: they sit in <span class="tx" dir="ltr"> (Consolas) and `$` is written &#36; so the
video builder never mistakes a regex anchor for TeX.

Ids (hidden elements start with class h; show()/hide() fade them):
  strip(pfx, text, layers)    the text as a row of monospace cells; layers = [(id, start, end, kind, label)] are
                              hidden overlays over cells start..end-1 (kind: m match, g1/g2 group, cur scan cursor,
                              no failed try, cut split cut, stop struck word, nil empty match at `start`)
  hits(pfx, pattern, text)    layers {pfx}-m{k} for the k-th match of re.finditer, plus the strings found
  parts(pfx, pieces)          a regex cut into labelled pieces: {pfx}-p{i} piece i (hidden)
  tests(pfx, pattern, rows)   one strip per string + its verdict ({pfx}-v{i}); verdict = bool(re.search)
  code(id, text) / out(id, text)  a code line / a result line (hidden)
  bow(pfx, docs)              CountVectorizer matrix: {pfx}-v{i}-{j} value (hidden), {pfx}-row{i} row ring,
                              {pfx}-col{j} column ring
  chips(pfx, words)           word chips {pfx}-w{i} (hidden) with a strike {pfx}-s{i} (hidden)
"""
import html as _html
import re

from vid import P, show, hide

DUAL = re.compile(r"\[\[([^|\]]*)\|([^\]]*)\]\]")


def L(text, **kw):
    """a phrase whose subtitle shows Latin and whose voice says Hebrew: "[[a|אֵיי]]" -> sub 'a', say 'אֵיי'"""
    sub = DUAL.sub(lambda m: m.group(1), text)
    say = DUAL.sub(lambda m: m.group(2), text).replace("**", "")
    return P(sub, say=say, **kw)


def esc(s):
    """HTML-escape a Latin string and hide `$` from the TeX scanner"""
    return _html.escape(str(s), quote=False).replace("$", "&#36;")


def rx(s, cls=""):
    """inline regex / code, LTR monospace"""
    return f'<span class="tx{(" " + cls) if cls else ""}" dir="ltr">{esc(s)}</span>'


def nw(h):
    """a short option note that never wraps"""
    return f'<span class="tx-nw">{h}</span>'


def pyrepr(v):
    """Python's own repr of a result (a list, a string, None), escaped"""
    return esc(repr(v))


# ------------------------------------------------------------------------------------------------ text strip
def _cw(n, maxw):
    return max(24, min(54, maxw // max(1, n)))


def strip(pfx, text, layers=(), cw=None, maxw=1000, idx=False, hidden=False):
    n = len(text)
    cw = cw or _cw(n, maxw)
    fs = min(50, round(cw * 1.0))
    cells = "".join(f'<b class="tx-ch{" sp" if c == " " else ""}" style="width:{cw}px">{"·" if c == " " else esc(c)}</b>'
                    for c in text)
    ov = []
    for ly in layers:
        lid, s, e, kind = ly[:4]
        label = ly[4] if len(ly) > 4 else ""
        assert 0 <= s <= e <= n, (lid, s, e, n)
        lab = f'<em class="tx-lb">{label}</em>' if label else ""
        if kind == "nil" or e == s:
            ov.append(f'<i id="{lid}" class="tx-ly nil h" style="left:{s * cw - 4}px;width:8px">{lab}</i>')
        else:
            ov.append(f'<i id="{lid}" class="tx-ly {kind} h" style="left:{s * cw}px;width:{(e - s) * cw}px">{lab}</i>')
    ix = ""
    if idx:
        ix = "".join(f'<span class="tx-ix" style="left:{i * cw}px;width:{cw}px">{i}</span>' for i in range(n))
    has_lab = any(len(ly) > 4 and ly[4] for ly in layers)
    cls = "tx-strip" + (" lab" if has_lab else "") + (" ix" if idx else "") + (" h" if hidden else "")
    return (f'<div class="{cls}" id="{pfx}" dir="ltr" style="font-size:{fs}px;height:{round(cw * 1.45)}px">'
            f'{"".join(ov)}{ix}{cells}</div>')


def hits(pfx, pattern, text, flags=0, kind="m", label=None):
    """layers for every match of re.finditer (id {pfx}-m{k}); returns (layers, [group(0) strings])"""
    ms = list(re.finditer(pattern, text, flags))
    found = [m.group(0) for m in ms]
    if re.compile(pattern).groups == 0:
        assert found == re.findall(pattern, text, flags)
    layers = [(f"{pfx}-m{k}", m.start(), m.end(), kind, label(m) if label else "") for k, m in enumerate(ms)]
    return layers, found


def show_hits(pfx, k_from, k_to):
    return show(*[f"{pfx}-m{k}" for k in range(k_from, k_to)])


# ------------------------------------------------------------------------------------------------ regex in parts
def parts(pfx, pieces, pattern=None, hidden=True, small=False):
    """pieces = [(regex piece, Hebrew label)]; asserts the pieces spell `pattern`"""
    if pattern is not None:
        assert "".join(p for p, _ in pieces) == pattern, ("".join(p for p, _ in pieces), pattern)
    boxes = "".join(f'<div id="{pfx}-p{i}" class="tx-pc{" h" if hidden else ""}"><span class="tx" dir="ltr">{"␣" if p == " " else esc(p)}</span>'
                    f'<small>{lab}</small></div>' for i, (p, lab) in enumerate(pieces))
    return f'<div class="tx-parts{" sm" if small else ""}" id="{pfx}" dir="ltr">{boxes}</div>'


def big(id_, s, hidden=False, size=None):
    st = f' style="font-size:{size}px"' if size else ""
    return f'<div id="{id_}" class="tx-big{" h" if hidden else ""}" dir="ltr"{st}>{esc(s)}</div>'


def code(id_, s, hidden=True, size=None):
    st = f' style="font-size:{size}px"' if size else ""
    return f'<div id="{id_}" class="tx-code{" h" if hidden else ""}" dir="ltr"{st}>{esc(s)}</div>'


def out(id_, s, hidden=True, bad=False, size=None):
    st = f' style="font-size:{size}px"' if size else ""
    return (f'<div id="{id_}" class="tx-out{" bad" if bad else ""}{" h" if hidden else ""}" dir="ltr"{st}>'
            f'<span class="ar">→</span> {esc(s)}</div>')


# ------------------------------------------------------------------------------------------------ test strings
def tests(pfx, pattern, rows, func="search", maxw=620, layers=None, row_hidden=True):
    """rows = [string]; one strip per string with a verdict ✓/✗ computed by re.<func>(pattern, s).
    layers: {i: [(id, s, e, kind, label)]} extra overlays on strip i. Returns (html, [bool])."""
    f = getattr(re, func)
    res = [f(pattern, s) is not None for s in rows]
    layers = layers or {}
    cw = min(_cw(max(len(s) for s in rows), maxw), 40)
    out_ = []
    for i, s in enumerate(rows):
        v = ('<b id="{p}-v{i}" class="tx-v ok h">✓</b>' if res[i] else '<b id="{p}-v{i}" class="tx-v bad h">✗</b>')
        out_.append(f'<div id="{pfx}-r{i}" class="tx-trow{" h" if row_hidden else ""}">'
                    f'{strip(f"{pfx}-s{i}", s, layers.get(i, ()), cw=cw)}{v.format(p=pfx, i=i)}</div>')
    return f'<div class="tx-tests" id="{pfx}">{"".join(out_)}</div>', res


# ------------------------------------------------------------------------------------------------ bag of words
def vectorize(docs, **kw):
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(**kw)
    X = cv.fit_transform(docs).toarray()
    return list(cv.get_feature_names_out()), X.tolist()


def bow(pfx, docs, vocab, X, hide_vals=True, labels=None):
    head = "".join(f'<th><i id="{pfx}-col{j}" class="tx-ring h"></i><span class="tx" dir="ltr">{esc(w)}</span></th>'
                   for j, w in enumerate(vocab))
    rows = []
    for i, d in enumerate(docs):
        lab = labels[i] if labels else f'<span class="tx" dir="ltr">{esc(d)}</span>'
        cells = "".join(f'<td><b id="{pfx}-v{i}-{j}" class="tx-n{" h" if hide_vals else ""}">{X[i][j]}</b></td>'
                        for j in range(len(vocab)))
        rows.append(f'<tr><th class="doc"><i id="{pfx}-row{i}" class="tx-ring h"></i>{lab}</th>{cells}</tr>')
    return (f'<table class="tx-bow" id="{pfx}" dir="ltr"><thead><tr><th></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def row_do(pfx, i, n):
    return show(*[f"{pfx}-v{i}-{j}" for j in range(n)])


def chips(pfx, words, hidden=True, cls=""):
    return (f'<div class="tx-chips {cls}" id="{pfx}" dir="ltr">'
            + "".join(f'<span id="{pfx}-w{i}" class="tx-chip{" h" if hidden else ""}">{esc(w)}'
                      f'<i id="{pfx}-s{i}" class="tx-strike h"></i></span>' for i, w in enumerate(words))
            + "</div>")


# ------------------------------------------------------------------------------------------------ checks
LATIN = re.compile(r"[A-Za-z]")


def no_latin(video):
    """the voice misreads Latin letters: every spoken phrase must be Hebrew (digits are fine)"""
    bad = [(S.key, p.say) for S in video.scenes for p in S.phrases if LATIN.search(p.say)]
    assert not bad, "Latin in spoken text:\n" + "\n".join(f"[{k}] {s}" for k, s in bad)
    return video


# ------------------------------------------------------------------------------------------------ call -> result grid
def calls(pfx, rows, size=32, shown=()):
    """rows = [(code, result)] in a two-column LTR grid; {pfx}-c{i} the call, {pfx}-r{i} its result (hidden unless
    i in shown)"""
    h = lambda i: "" if i in shown else " h"
    cells = "".join(f'<div id="{pfx}-c{i}" class="tx-cl{h(i)}">{esc(c)}</div>'
                    f'<div id="{pfx}-r{i}" class="tx-cr{h(i)}"><span class="ar">→</span> {esc(r)}</div>'
                    for i, (c, r) in enumerate(rows))
    return f'<div class="tx-calls" id="{pfx}" dir="ltr" style="font-size:{size}px">{cells}</div>'

"""Shared helpers for the per-course machine checks (tools/verify/needhelp/<course>/check.py).

A check recomputes a question's answer with Python (math / numpy / pandas / sklearn / re) and compares it
with the keyed option of the real course file. For every question it asserts:
  * the keyed option satisfies the computed predicate, and
  * NO other option satisfies it   (one defensible answer),
and at the end that every question of the course has exactly one check.

usage (from the repo root):  python tools/verify/needhelp/<course>/check.py
"""
import json
import math
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_course(cid):
    """Dump the course (refs resolved from the bank) through course_check.js and read it back."""
    subprocess.run(["node", os.path.join("tools", "course_check.js"), "--json", cid], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    path = os.path.join(ROOT, "tools", "verify", "needhelp", cid, "course.json")
    with open(path, encoding="utf-8") as f:
        levels = json.load(f)
    qs = {}
    for L in levels:
        for q in L["questions"]:
            qs[q["id"]] = q
    return levels, qs


NUM = re.compile(r"-?\d+(?:[.,]\d+)?")


def numbers(text):
    """All numbers inside an option text, as floats."""
    return [float(m.replace(",", ".")) for m in NUM.findall(text.replace("−", "-"))]


class Checker:
    def __init__(self, cid):
        self.cid = cid
        self.levels, self.qs = load_course(cid)
        self.done = {}      # qid -> kind
        self.failed = []

    # ---- core: a predicate over option text, evaluated on all options -------------------------------------
    def pred(self, qid, fn, kind="computed"):
        q = self.qs[qid]
        if qid in self.done:
            self.failed.append(f"{qid}: checked twice")
        self.done[qid] = kind
        hits = [i for i, o in enumerate(q["options"]) if fn(o)]
        if hits != [q["answer"]]:
            self.failed.append(f"{qid}: predicate holds for options {hits}, keyed {q['answer']}  ({q['question'][:50]!r})")

    # ---- numeric answer: the option whose first number equals `value` -------------------------------------
    def num(self, qid, value, tol=0.006, idx=0):
        self.pred(qid, lambda o: bool(numbers(o)) and len(numbers(o)) > idx and abs(numbers(o)[idx] - value) <= tol)

    def has_nums(self, qid, *values, tol=0.006):
        """option mentions every given number (in any position)."""
        def fn(o):
            ns = numbers(o)
            return all(any(abs(n - v) <= tol for n in ns) for v in values)
        self.pred(qid, fn)

    def exact(self, qid, text):
        self.pred(qid, lambda o: o.strip() == text.strip())

    def contains(self, qid, text):
        self.pred(qid, lambda o: text in o)

    def boolean_claim(self, qid, truth_by_index):
        """truth_by_index: list of bools computed for each option; the keyed one must be the only True
        (or the only False, for 'which is NOT true')."""
        q = self.qs[qid]
        self.pred(qid, lambda o: truth_by_index[q["options"].index(o)])

    def concept(self, qid, why):
        """Not computable. Recorded, checked only by the blind self-review."""
        self.done[qid] = "concept"
        self.concept_notes = getattr(self, "concept_notes", {})
        self.concept_notes[qid] = why

    def finish(self):
        missing = [q for q in self.qs if q not in self.done]
        extra = [q for q in self.done if q not in self.qs]
        for m in missing:
            self.failed.append(f"{m}: no check")
        for e in extra:
            self.failed.append(f"{e}: check for an unknown question")
        kinds = {}
        for k in self.done.values():
            kinds[k] = kinds.get(k, 0) + 1
        print(f"[{self.cid}] {len(self.qs)} questions; checks: {kinds}")
        if self.failed:
            print("FAILED:")
            for f in self.failed:
                print("  -", f)
            sys.exit(1)
        print(f"[{self.cid}] ALL CHECKS PASSED")


# ---------------- reference statistics, with the course's conventions ----------------------------------------
def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def quartiles(xs):
    """Course method: Q2 = median, Q1/Q3 = medians of the lower/upper half (the median itself is left out
    when n is odd). Matches the keys of 24A-A-Q8 and 25A-A-Q2."""
    s = sorted(xs)
    n = len(s)
    lower = s[: n // 2]
    upper = s[(n + 1) // 2:]
    return median(lower), median(s), median(upper)


def iqr(xs):
    q1, _, q3 = quartiles(xs)
    return q3 - q1


def fences(xs, k=1.5):
    q1, _, q3 = quartiles(xs)
    i = q3 - q1
    return q1 - k * i, q3 + k * i


def pstdev(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def sstdev(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def pearson(xs, ys):
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)

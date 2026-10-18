"""Machine check for the EDA course (E01..E08). Run from the repo root:  python tools/verify/needhelp/eda/check.py"""
import math
import os
import statistics
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import Checker, iqr, quartiles, fences, pstdev, sstdev, pearson, median  # noqa: E402

c = Checker("eda")

# ---- sanity of the reference helpers against numpy / independent code -------------------------------------
for data in ([16, 19, 23, 36, 39, 81, 85, 90], [8, 2, 4, 4, 6, 12, 17, 6, 6], [3, 5, 7, 8, 10, 12, 15, 18, 20]):
    s = np.sort(data)
    n = len(s)
    lo, hi = s[: n // 2], s[(n + 1) // 2:]
    assert quartiles(data) == (np.median(lo), np.median(s), np.median(hi))
assert iqr([16, 19, 23, 36, 39, 81, 85, 90]) == 62 and iqr([8, 2, 4, 4, 6, 12, 17, 6, 6]) == 6   # bank keys
assert abs(sstdev([4, 8, 6, 5, 3]) - np.std([4, 8, 6, 5, 3], ddof=1)) < 1e-12
assert abs(pstdev([1, 3, 5, 7]) - np.std([1, 3, 5, 7])) < 1e-12
assert abs(pearson([1, 2, 3, 4, 5], [2, 4, 5, 4, 5]) - np.corrcoef([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])[0, 1]) < 1e-12

# ---- E01 ---------------------------------------------------------------------------------------------
c.num("E01-Q1", np.median([12, 7, 9, 7, 15, 10]))
c.num("E01-Q2", np.mean([3, 9, 6, 12, 10]))
sal = [8, 9, 9, 10, 11, 12, 70]
sal2 = [8, 9, 9, 10, 11, 12, 13]
assert round(np.mean(sal), 1) == 18.4 and round(np.mean(sal2), 1) == 10.3
assert np.median(sal) == np.median(sal2) == 10
c.contains("E01-Q3", "הממוצע יורד מ-18.4 לכ-10.3, והחציון נשאר 10")
d = [1, 2, 2, 3, 3, 3, 4, 20]
assert np.mean(d) == 4.75 and np.median(d) == 3 and stats.skew(d) > 0 and len(statistics.multimode(d)) == 1
c.contains("E01-Q4", "זנב ארוך ימינה (הטיה חיובית)")
c.num("E01-Q5", statistics.multimode([4, 6, 6, 9, 4, 6, 9, 3])[0]) if len(statistics.multimode([4, 6, 6, 9, 4, 6, 9, 3])) == 1 else sys.exit("mode not unique")

# ---- E02 ---------------------------------------------------------------------------------------------
c.num("E02-Q1", np.std([2, 6, 10], ddof=1))
c.num("E02-Q2", np.std([1, 3, 5, 7]))
a, b = [48, 50, 52], [40, 50, 60]
assert np.mean(a) == np.mean(b) and round(np.std(b, ddof=1) / np.std(a, ddof=1)) == 5
c.contains("E02-Q3", "גדול פי 5 בערך")
c.num("E02-Q4", np.std([5, 5, 9, 9], ddof=1))
x = np.array([3.0, 9, 4, 11, 20])
assert abs(np.std(2 * (x + 100), ddof=1) - 2 * np.std(x, ddof=1)) < 1e-9 and abs(np.std(x + 100, ddof=1) - np.std(x, ddof=1)) < 1e-9
c.exact("E02-Q5", "2s")

# ---- E03 ---------------------------------------------------------------------------------------------
assert math.ceil(0.30 * 45) == 14
c.contains("E03-Q1", "המדידה ה-14")
c.num("E03-Q2", iqr([5, 7, 8, 12, 13, 14, 18, 21, 23, 27]))
dd = [4, 6, 9, 10, 12, 15, 20, 22, 25]
assert quartiles(dd) == (7.5, 12, 21)
c.num("E03-Q3", iqr(dd))
assert 40 - 22 == 18
c.pred("E03-Q4", lambda o: "IQR = 18" in o and "50%" in o)
assert math.ceil(0.75 * 20) == 15
c.contains("E03-Q5", "האחוזון ה-75")

# ---- E04 ---------------------------------------------------------------------------------------------
e4 = [10, 12, 12, 13, 14, 15, 16, 18, 45]
lo, hi = fences(e4)
assert quartiles(e4) == (12, 14, 17) and (lo, hi) == (4.5, 24.5)
assert [v for v in e4 if v < lo or v > hi] == [45]
c.exact("E04-Q1", "רק 45")
lo, hi = 30 - 1.5 * 20, 50 + 1.5 * 20
assert (lo, hi) == (0, 80)
c.contains("E04-Q2", "בין 0 ל-80")
c.num("E04-Q3", (58 - 70) / 8)
vals = [30, 41, 62, 69, 66]
out = [v for v in vals if abs(v - 50) > 3 * 6]
assert out == [30, 69]
c.exact("E04-Q4", "30 ו-69")
e5 = [2, 4, 5, 5, 6, 6, 7, 8, 9, 14, 25]
q1, _, q3 = quartiles(e5)
assert (q1, q3) == (5, 9)
assert [v for v in e5 if v < q1 - 1.5 * 4 or v > q3 + 1.5 * 4] == [25]
assert [v for v in e5 if v < q1 - 1 * 4 or v > q3 + 1 * 4] == [14, 25]
c.exact("E04-Q5", "14 ו-25")

# ---- E05 ---------------------------------------------------------------------------------------------
rng = np.random.default_rng(0)
for _ in range(200):
    data = rng.normal(size=100) * rng.uniform(1, 5)
    h4, _e = np.histogram(data, bins=4)
    h20, _e = np.histogram(data, bins=20, range=(data.min(), data.max()))
    assert h20.max() <= h4.max() and h20.sum() == h4.sum() == 100
c.contains("E05-Q1", "אף עמודה לא תעלה על 40, וסכום כל העמודות יישאר 100")
d2 = [3, 7, 12, 14, 15, 18, 22, 25, 29, 33, 38, 41]
h, _e = np.histogram(d2, bins=[0, 10, 20, 30, 40, 50])
c.num("E05-Q2", h[1])
fl, fh = 8 - 1.5 * 6, 14 + 1.5 * 6
assert [v for v in (5, 22, 24) if v < fl or v > fh] == [24]
c.exact("E05-Q3", "רק 24")
n15 = len([v for v in (5, 22, 24, 40) if v < 8 - 9 or v > 14 + 9])
n5 = len([v for v in (5, 22, 24, 40) if v < 8 - 30 or v > 14 + 30])
assert (n15, n5) == (2, 0)
c.contains("E05-Q4", "2 עם 1.5, ו-0 עם 5")
hh, _e = np.histogram(rng.normal(size=120), bins=8)
c.num("E05-Q5", hh.sum())

# ---- E06 ---------------------------------------------------------------------------------------------
c.num("E06-Q1", np.corrcoef([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])[0, 1], tol=0.006)
xs = np.arange(-3, 4)
r = np.corrcoef(xs, xs ** 2)[0, 1]
assert abs(r) < 1e-12
c.num("E06-Q2", 0)
xs = np.arange(1, 6)
assert abs(np.corrcoef(xs, -2 * xs + 10)[0, 1] + 1) < 1e-12
c.num("E06-Q3", -1)
xx = rng.normal(size=500)
yy = 0.6 * xx + rng.normal(size=500)
assert abs(np.corrcoef(xx, -2 * yy + 5)[0, 1] + np.corrcoef(xx, yy)[0, 1]) < 1e-12
c.num("E06-Q4", -0.6)
rs = {"A": -0.92, "B": 0.55, "C": 0.05, "D": -0.3}
c.exact("E06-Q5", max(rs, key=lambda k: abs(rs[k])))

# ---- E07 ---------------------------------------------------------------------------------------------
q = c.qs["E07-Q1"]["table"]
df = pd.DataFrame(q["rows"], columns=q["head"])
ct = pd.crosstab(df["sex"], df["passed"], normalize="index")
assert (ct.sum(axis=1) == 1).all()
c.num("E07-Q1", ct.loc["F", "yes"])
# chart choice: rule table taken from the lesson (task -> chart); the keyed option must be the chart the table names
CHART = {"E07-Q2": "היסטוגרמה", "E07-Q3": "box plot מקביל", "E07-Q4": "scatter plot עם A ו-B", "E07-Q5": "heatmap"}
for qid, key in CHART.items():
    c.pred(qid, lambda o, key=key: o.startswith(key), kind="rule")

# ---- E08 boss (real bank questions: recomputed) ---------------------------------------------------------
c.num("E08:25-S-Q8", sstdev([4, 8, 6, 5, 3]), tol=0.006)
assert math.ceil(0.2 * 49) == 10
c.contains("E08:24A-B-Q19", "העשירית")
c.num("E08:25A-A-Q2", iqr([8, 2, 4, 4, 6, 12, 17, 6, 6]))
c.has_nums("E08:26B-A-Q7", -5, 35)
xs = np.arange(-5, 6)
assert abs(np.corrcoef(xs, xs ** 2)[0, 1]) < 1e-12   # zero correlation with perfect dependence
c.contains("E08:26B-A-Q6", "בהכרח מעיד שאין כל תלות")   # the false claim, keyed as "not true"
ln = rng.lognormal(size=2000)
assert ln.mean() > np.median(ln)
c.contains("E08:25A-A-Q22", "הממוצע יהיה גדול מהחציון")

c.finish()

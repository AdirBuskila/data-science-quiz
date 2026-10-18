"""Machine check for the cleaning course (C01..C07). Run from the repo root:  python tools/verify/needhelp/clean/check.py"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import Checker, quartiles, fences  # noqa: E402

c = Checker("clean")


def df_of(qid):
    t = c.qs[qid]["table"]
    d = pd.DataFrame(t["rows"], columns=t["head"]).replace("NaN", np.nan)
    return d


def numdf(qid):
    d = df_of(qid)
    for col in d.columns:
        try:
            d[col] = pd.to_numeric(d[col])
        except (ValueError, TypeError):
            pass
    return d


# ---- C01: scales. Rule table: each scale inherits the previous scale's operations and adds one --------
SCALES = ["nominal", "ordinal", "interval", "ratio"]
OPS = {"nominal": {"mode"}, "ordinal": {"mode", "median"}, "interval": {"mode", "median", "mean", "difference"},
       "ratio": {"mode", "median", "mean", "difference", "ratio"}}
for i in range(1, 4):
    assert OPS[SCALES[i - 1]] < OPS[SCALES[i]]
VAR = {"טמפרטורה בצלזיוס": "interval", "דירוג סרט בכוכבים": "ordinal", "קבוצת דם": "nominal", "גובה בס״מ": "ratio"}
HE = {"nominal": "שמי", "ordinal": "סדר", "interval": "רווח", "ratio": "מנה"}
c.pred("C01-Q1", lambda o: ("שכיח וחציון" in o and "לא ממוצע" in o) == (OPS["ordinal"] == {"mode", "median"}), kind="rule")
good = " · ".join(f"{k}: {HE[v]}" for k, v in VAR.items())
c.pred("C01-Q2", lambda o: o == good, kind="rule")
k10, k20 = 10 + 273.15, 20 + 273.15
assert abs(k20 / k10 - 1.0353) < 0.001 and k20 / k10 != 2
c.contains("C01-Q3", "אינו \"פי שניים חם\"")
c.pred("C01-Q4", lambda o: o == "שכיח בלבד", kind="rule")
t = [10.0, 10.1, 15.0]
assert round(t[1] - t[0], 1) == 0.1 and round(t[2] - t[1], 1) == 4.9
c.contains("C01-Q5", "סולם סדר")

# ---- C02 ---------------------------------------------------------------------------------------------
d = numdf("C02-Q1")
c.num("C02-Q1", d.isnull().sum()["B"])
d = numdf("C02-Q2")
c.num("C02-Q2", len(d.dropna()))
d = numdf("C02-Q3")
c.num("C02-Q3", d.dropna(axis=1).shape[1])
c.contains("C02-Q4", "MNAR")
big = pd.DataFrame({"x": range(1000)}).astype(float)
big.loc[800, "x"] = np.nan
assert big.head().isnull().sum().sum() == 0 and big.isnull().sum().sum() == 1
assert big.info.__name__ == "info" and big.describe().loc["count", "x"] == 999
c.exact("C02-Q5", "df.head()")

# ---- C03 ---------------------------------------------------------------------------------------------
d = numdf("C03-Q1")
c.num("C03-Q1", d["x"].fillna(d["x"].median()).iloc[-1])
d = df_of("C03-Q2")
c.exact("C03-Q2", d["city"].fillna(d["city"].mode()[0]).iloc[-1])
s = pd.Series([4, np.nan, 8, np.nan, 6])
c.num("C03-Q3", s.fillna(s.mean()).sum())
d = numdf("C03-Q4")
d.loc[d["A"] > 5, "B"] = 0
c.num("C03-Q4", d["B"].sum())
s = pd.Series([20, np.nan, np.nan, 23])
c.num("C03-Q5", s.ffill().iloc[2])

# ---- C04 ---------------------------------------------------------------------------------------------
d = numdf("C04-Q1")
c.num("C04-Q1", d.duplicated().sum())
c.num("C04-Q2", len(d.drop_duplicates()))
c.pred("C04-Q3", lambda o: o == ", ".join(map(str, list(d.drop_duplicates(keep="last").index[:-1]))) + " ו-" + str(d.drop_duplicates(keep="last").index[-1]))
s = pd.Series([5, 3, 5, 8, 3, 1, 5, 9, 2, 7])
assert s.nunique() + s.duplicated().sum() == len(s) == 10
c.num("C04-Q4", s.duplicated().sum())
d = df_of("C04-Q5")
assert len(d.drop_duplicates()) == 4
c.num("C04-Q5", len(d.drop_duplicates(subset=["name"])))

# ---- C05 ---------------------------------------------------------------------------------------------
d = pd.DataFrame({"id": [1, 2, 3], "color": ["red", "green", "blue"]})
c.num("C05-Q1", pd.get_dummies(d, columns=["color"]).shape[1])
st = pd.DataFrame({"Status": ["Active", "Inactive", "Pending"]})
row = pd.get_dummies(st["Status"]).astype(int).loc[2]
want = f"Active = {row['Active']}, Inactive = {row['Inactive']}, Pending = {row['Pending']}"
c.exact("C05-Q2", want)
ages = pd.Series([5, 12, 19, 21, 29, 40])
cut = pd.cut(ages, bins=[0, 12, 19, 34, 120])
c.exact("C05-Q3", str(cut[2]).replace("Interval", ""))
assert cut[3] == cut[4]   # 21 and 29 land in the same bin
c.contains("C05-Q4", "21 ו-29")
xs = np.arange(1, 6)
y = np.exp(xs)
res = {"log": np.corrcoef(xs, np.log(y))[0, 1], "sqrt": np.corrcoef(xs, np.sqrt(y))[0, 1],
       "square": np.corrcoef(xs, y ** 2)[0, 1], "inverse": np.corrcoef(xs, 1 / y)[0, 1]}
assert abs(res["log"] - 1) < 1e-12 and all(abs(v - 1) > 1e-3 for k, v in res.items() if k != "log")
c.contains("C05-Q5", "לוגריתם טבעי")

# ---- C06: the options are real code, evaluated -----------------------------------------------------
s = pd.Series([10, 12, 12, 13, 14, 15, 16, 18, 45])
q1, q3 = s.quantile(0.25), s.quantile(0.75)
iqr = q3 - q1
assert (q1, q3, iqr) == (12, 16, 4)
env = {"s": s, "q1": q1, "q3": q3, "iqr": iqr, "np": np, "pd": pd}
c.pred("C06-Q1", lambda o: abs(eval(o, env) - iqr) < 1e-9)
expected = list(s[(s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)])
assert expected == [45]
c.pred("C06-Q2", lambda o: list(eval(o, env)) == expected)
r = np.random.default_rng(1)
data = pd.Series(list(np.array([50, 52, 48, 51, 49, 50, 53, 47, 50, 51, 49, 52, 48, 50, 51, 49, 50, 52, 48])) + [120], dtype=float)
assert data.between(47, 120).all() and len(data) == 20
z = (data - data.mean()) / data.std()
assert round(abs(z.iloc[-1]), 1) == 4.2 and round(data.mean(), 1) == 53.5
c.num("C06-Q3", len(data[z.abs() > 3]))
c.num("C06-Q4", s[s != 45].mean())
assert round(s.mean(), 2) == 17.22
c.pred("C06-Q5", lambda o: o == "גרף עוגה", kind="rule")

# ---- C07 boss (bank questions, recomputed) ---------------------------------------------------------
c.pred("C07:24A-A-Q3", lambda o: "בסולם סודר ובסולם רווח אפשר לחשב שכיח" in o and "ובסולם רווח אפשר לחשב גם ממוצע" in o
       and "mode" in OPS["ordinal"] and "mean" not in OPS["ordinal"] and "mean" in OPS["interval"], kind="rule")
a = pd.DataFrame({"A": [1, 2, None, 4]})
filled = {n: a["A"].fillna(getattr(a["A"], n)()) for n in ("median", "max")}
assert filled["median"].tolist() == [1, 2, 2, 4]
assert a["A"].fillna(a["A"].dropna()).isnull().sum() == 1          # dropna() as a fill value fills nothing
assert filled["max"].tolist() == [1, 2, 4, 4]                       # max is distorted upward, median is the representative fill
c.exact("C07:24A-A-Q18", "median")
t = pd.DataFrame({"A": [1, 2, np.nan, 4, 5], "B": [3, np.nan, np.nan, 8, 9]})
b2 = t.copy()
b2.loc[t["A"].isnull(), "B"] = t["B"].mean()
assert b2["B"].iloc[2] == t["B"].mean() and b2["B"].iloc[1] != b2["B"].iloc[2]   # only the row where A is NaN was filled
assert b2["A"].equals(t["A"]) and len(b2) == len(t)
c.contains("C07:25-S-Q24", "רק עבור השורות שבהן הערך ב-A הוא NaN")
em = pd.get_dummies(pd.DataFrame({"Embarked": list("CSQCSQ")}), columns=["Embarked"])
assert em.shape[1] == 3 and "Embarked" not in em.columns and set(em.astype(int).values.ravel()) == {0, 1}
c.contains("C07:26A-B-Q24", "3 עמודות חדשות")
vals = pd.Series([10, 11, 12, 13, 14, 15, 500, 600])
assert vals.mean() > 100 and vals.median() == 13.5   # the mean is dragged by outliers
c.contains("C07:P-20", "כדאי להשתמש בממוצע")
rng = np.random.default_rng(3)
for _ in range(100):
    v = rng.standard_t(2, size=60)
    q1_, _m, q3_ = quartiles(v)
    i_ = q3_ - q1_
    n15 = ((v < q1_ - 1.5 * i_) | (v > q3_ + 1.5 * i_)).sum()
    n2 = ((v < q1_ - 2 * i_) | (v > q3_ + 2 * i_)).sum()
    assert n15 >= n2
c.contains("C07:26A-B-Q21", "1.5IQR יתן לנו פחות חריגים מ-2IQR")

c.finish()

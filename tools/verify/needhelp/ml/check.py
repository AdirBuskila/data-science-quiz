"""Machine check for the models & evaluation course (M01..M07). Run from the repo root:  python tools/verify/needhelp/ml/check.py"""
import math
import os
import sys

import numpy as np
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, f1_score, precision_score, r2_score, recall_score, accuracy_score
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import Checker  # noqa: E402

c = Checker("ml")

# ---- M01: rule engine: (has label?, label type / goal) -> (learning kind, problem type) ---------------
def classify(has_label, label_kind=None, goal=None):
    if has_label:
        return ("מונחית", "סיווג" if label_kind == "categorical" else "רגרסיה")
    return ("לא מונחית", "אשכול" if goal == "groups" else "הורדת ממדים")


SUP = {"KNN", "SVM", "רגרסיה לוגיסטית"}
UNSUP = {"K-Means", "PCA", "DBSCAN"}


def verdict(qid, kind, prob):
    want = f"למידה {kind}, והבעיה היא {prob}"
    c.pred(qid, lambda o: o == want, kind="rule")


verdict("M01-Q1", *classify(False, goal="groups"))
verdict("M01-Q2", *classify(True, "numeric"))
verdict("M01-Q3", *classify(True, "categorical"))
verdict("M01-Q4", *classify(False, goal="reduce"))
c.pred("M01-Q5", lambda o: all(a.strip() in UNSUP for a in o.split(" ו-")), kind="rule")

# ---- M02: K-Means -------------------------------------------------------------------------------------
X = np.array([[1], [2], [3], [10], [11], [12]], dtype=float)
km = KMeans(n_clusters=2, init=np.array([[1.0], [12.0]]), n_init=1, max_iter=1).fit(X)
assert sorted(km.cluster_centers_.ravel().tolist()) == [2.0, 11.0]
c.pred("M02-Q1", lambda o: sorted(float(x) for x in o.replace(" ו-", " ").split()) == [2.0, 11.0])
cd = np.array([[8, 8], [9, 9]]).mean(axis=0)
c.exact("M02-Q2", f"({cd[0]:g}, {cd[1]:g})")
cent = np.array([[0, 0], [6, 0]])
assert np.argmin(np.linalg.norm(cent - np.array([4, 0]), axis=1)) == 1
c.exact("M02-Q3", "המרכז (6, 0)")
sse2 = sum(((X[:3] - 2) ** 2).sum() for _ in [0]) + ((X[3:] - 11) ** 2).sum()
assert abs(KMeans(n_clusters=2, n_init=10, random_state=0).fit(X).inertia_ - sse2) < 1e-9
c.num("M02-Q4", sse2)
sse1 = ((X - X.mean()) ** 2).sum()
assert abs(KMeans(n_clusters=1, n_init=1).fit(X).inertia_ - sse1) < 1e-9 and X.mean() == 6.5
c.num("M02-Q5", sse1)

# ---- M03: DBSCAN / hierarchical ---------------------------------------------------------------------------
M, y = make_moons(400, noise=0.05, random_state=0)
ari_db = adjusted_rand_score(y, DBSCAN(eps=0.2, min_samples=5).fit_predict(M))
ari_km = adjusted_rand_score(y, KMeans(2, n_init=10, random_state=0).fit_predict(M))
assert ari_db > 0.95 and ari_km < 0.5
c.exact("M03-Q1", "DBSCAN")
P = np.array([[1], [2], [3], [10], [11], [12], [50]], dtype=float)


def summary(eps, ms):
    lab = DBSCAN(eps=eps, min_samples=ms).fit_predict(P)
    return len(set(lab) - {-1}), int((lab == -1).sum())


assert summary(2, 2) == (2, 1) and summary(10, 2) == (1, 1) and summary(2, 4) == (0, 7)
c.exact("M03-Q2", "2 אשכולות ונקודת רעש אחת")
c.exact("M03-Q3", "שני האשכולות מתמזגים לאחד, והנקודה 50 נשארת רעש")
c.exact("M03-Q4", "אף אשכול: כל הנקודות הן רעש")
Z = linkage(np.array([[1], [2], [6]], dtype=float), method="single")
assert Z[0, 2] == 1 and Z[1, 2] == 4
c.num("M03-Q5", Z[-1, 2])

# ---- M04: PCA ---------------------------------------------------------------------------------------------
line = np.array([[1, 1], [2, 2], [3, 3], [4, 4]], dtype=float)
r = PCA().fit(line).explained_variance_ratio_
assert abs(r[0] - 1) < 1e-12
c.exact("M04-Q1", "100%")
shape = PCA(n_components=2).fit_transform(np.random.default_rng(0).normal(size=(100, 5))).shape
c.exact("M04-Q2", str(shape))
# x var : y var = 4 : 1, uncorrelated (constructed exactly: columns mean 0, zero covariance)
D = np.array([[2, 0], [-2, 0], [0, 1], [0, -1]], dtype=float)
assert abs(np.cov(D.T)[0, 1]) < 1e-12 and abs(np.cov(D.T)[0, 0] / np.cov(D.T)[1, 1] - 4) < 1e-12
rr = PCA().fit(D).explained_variance_ratio_
assert abs(rr[0] - 0.8) < 1e-12
c.exact("M04-Q3", str([round(float(v), 1) for v in rr]))
all4 = PCA().fit(np.random.default_rng(1).normal(size=(50, 4))).explained_variance_ratio_
assert abs(all4.sum() - 1) < 1e-12
c.contains("M04-Q4", "1.0 (100%)")
for seed in range(20):
    rat = PCA().fit(np.random.default_rng(seed).normal(size=(60, 5)) * [5, 3, 2, 1, 1]).explained_variance_ratio_
    assert all(rat[i] >= rat[i + 1] for i in range(len(rat) - 1))
c.contains("M04-Q5", "הם ממוינים מהגדול לקטן")

# ---- M05 --------------------------------------------------------------------------------------------------
Xtr = np.array([[1], [2], [3], [10], [11]], dtype=float)
ytr = np.array(list("AAABB"))
assert KNeighborsClassifier(3).fit(Xtr, ytr).predict([[7]])[0] == "B"
c.exact("M05-Q1", KNeighborsClassifier(3).fit(Xtr, ytr).predict([[7]])[0])
c.exact("M05-Q2", KNeighborsClassifier(5).fit(Xtr, ytr).predict([[7]])[0])
yt, yp = np.array([3, 5, 7.0]), np.array([2, 5, 9.0])
c.num("M05-Q3", ((yt - yp) ** 2).sum())
yt, yp = np.array([1, 2, 3, 4.0]), np.array([1.5, 1.5, 3.5, 3.5])
c.num("M05-Q4", r2_score(yt, yp))
c.contains("M05-Q5", "לבדוק את ביצועי המודל על נתונים שלא השתתפו באימון")

# ---- M06 --------------------------------------------------------------------------------------------------
TP, FN, FP, TN = 40, 10, 20, 30
yt = np.array([1] * (TP + FN) + [0] * (FP + TN))
yp = np.array([1] * TP + [0] * FN + [1] * FP + [0] * TN)
assert abs(precision_score(yt, yp) - TP / (TP + FP)) < 1e-12 and abs(recall_score(yt, yp) - TP / (TP + FN)) < 1e-12
c.num("M06-Q1", precision_score(yt, yp))
c.num("M06-Q2", recall_score(yt, yp))
c.num("M06-Q3", accuracy_score(yt, yp))
p_, r_ = 0.5, 0.75
c.num("M06-Q4", 2 * p_ * r_ / (p_ + r_))
folds = list(KFold(5).split(np.arange(120)))
assert all(len(v) == 24 for _, v in folds) and all(len(t) == 96 for t, _ in folds)
assert sorted(i for _, v in folds for i in v) == list(range(120))   # each sample validated exactly once
c.num("M06-Q5", len(folds[0][0]))

# ---- M07 boss (bank questions, recomputed / rule) ------------------------------------------------------
c.pred("M07:24A-A-Q17", lambda o: "לא מונחית" in o and "אשכול" in o and "מונחית (supervised)" not in o and "(clustering)" in o, kind="rule")
c.pred("M07:26B-A-Q14", lambda o: "למידה מונחית (supervised) ומוגדרת כבעיית סיווג" in o, kind="rule")
c.contains("M07:25A-B-Q21", "בהתבסס על קלט מהמשתמש")
assert KMeans(n_clusters=3).n_clusters == 3                           # k is a constructor argument, never inferred
c.contains("M07:26A-A-Q5", "החלוקה נועדה לשפר את הדיוק של המודל בזמן האימון")   # the false statement (see M05)
c.num("M07:25A-B-Q18", 2 * 0.8 * 0.6 / (0.8 + 0.6), tol=0.006)
tp, fn, fp, tn = 90, 10, 200, 100
rec, prec, acc = tp / (tp + fn), tp / (tp + fp), (tp + tn) / (tp + fn + fp + tn)
assert rec > prec and rec > acc                                       # many false positives: recall is the high one
c.contains("M07:26A-B-Q16", "Recall")

c.finish()

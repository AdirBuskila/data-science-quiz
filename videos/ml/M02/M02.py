# -*- coding: utf-8 -*-
"""M02 · K-Means צעד אחר צעד — video script (build: tools/video/vid.py M02).

Source: courses/ml/M02.js (lesson + goal: one K-Means round by hand: assign every point to the nearest centroid,
recompute the centroids as means, compute SSE). Exam anchor: 24A-B-Q1 (which algorithm clusters the pictured data
best: KMeans K=4), which no guided quiz uses.
Not used on purpose: every M02 quiz item (1,2,3,10,11,12 with centroids 1 and 12; the centroid of (8,8),(9,9); the
point (4,0) between (0,0) and (6,0); SSE 4 and 125.5), and the boss item 25A-B-Q21 (who sets k) and its twin
26A-A-Q21: the video never asks or answers "how is k chosen".
Worked example: six new points, initial centroids (1,1) and (2,4); three rounds, computed by w_ml.kmeans_run and
asserted against sklearn's KMeans with the same initial centroids.
Exam figure: the dots of images/exams/24A-B-Q1.png are digitized (green markers -> one centre per connected component)
and the claims made in the video are asserted on them: KMeans(4) finds the four groups, KMeans(5) splits one of
them, DBSCAN with eps 4 or 5 chains everything into one cluster.
"""
import math

import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN, KMeans

from vid import P, Scene, Video, show, hide, BANK, ROOT
import stage as st
import w_ml as w

# ---------------------------------------------------------------- worked example (verified)
PTS = [(1, 1), (3, 1), (2, 4), (6, 5), (8, 5), (7, 8)]
C0 = [(1, 1), (2, 4)]
RUN = w.kmeans_run(PTS, C0)
assert len(RUN) == 3
(CA, A1), (CB, A2), (CC, A3) = RUN
assert CA.tolist() == [[1, 1], [2, 4]] and A1.tolist() == [0, 0, 1, 1, 1, 1]
assert CB.tolist() == [[2, 1], [5.75, 5.5]] and A2.tolist() == [0, 0, 0, 1, 1, 1]
assert CC.tolist() == [[2, 2], [7, 6]] and (A3 == A2).all()               # nothing moves: stop
# the distances that are narrated
assert w.dist((3, 1), (1, 1)) == 2 and abs(w.dist((3, 1), (2, 4)) - math.sqrt(10)) < 1e-12 and round(math.sqrt(10), 2) == 3.16
assert w.dist((2, 4), (2, 1)) == 3 and round(w.dist((2, 4), (5.75, 5.5)), 2) == 4.04
assert (2 + 6 + 8 + 7) / 4 == 5.75 and (4 + 5 + 5 + 8) / 4 == 5.5
assert w.sse(PTS, CA, A1) == 99 and w.sse(PTS, CC, A3) == 16
assert [((x - 2) ** 2 + (y - 2) ** 2) for x, y in PTS[:3]] == [2, 2, 4]
assert [((x - 7) ** 2 + (y - 6) ** 2) for x, y in PTS[3:]] == [2, 2, 4]
km = KMeans(2, init=np.array(C0, float), n_init=1).fit(np.array(PTS, float))
assert np.allclose(km.cluster_centers_, CC) and km.inertia_ == 16


# ---------------------------------------------------------------- exam figure, digitized
def figure_points():
    """the exam figure's markers in data units: green pixels -> connected components (8-neighbour) -> one centre
    per component (grid: x=0 at px 116, x=20 at px 507; y=0 at px 401, y=20 at px 5). Inside the dense groups
    several markers touch and become one centre, so the groups are, if anything, sparser than in the original."""
    from scipy import ndimage
    a = np.asarray(Image.open(ROOT / "images/exams/24A-B-Q1.png").convert("RGB")).astype(int)
    green = (a[..., 1] > 120) & (a[..., 1] - a[..., 0] > 50)
    lab, n = ndimage.label(green, structure=np.ones((3, 3)))
    cm = ndimage.center_of_mass(green, lab, range(1, n + 1))
    return np.array([((c[1] - 116) / (391 / 20), (401 - c[0]) / (396 / 20)) for c in cm])


FIG = figure_points()
assert len(FIG) > 200
K4 = KMeans(4, n_init=10, random_state=0).fit(FIG).cluster_centers_
BLOBS = [(5, 15), (15, 15), (5, 5), (15, 5)]
assert all(min(w.dist(c, b) for c in K4) < 1.0 for b in BLOBS)              # K=4: one centroid per group
K5 = KMeans(5, n_init=10, random_state=0).fit(FIG).cluster_centers_
near = [min(range(4), key=lambda j: w.dist(c, BLOBS[j])) for c in K5]
assert len(set(near)) == 4 and len(near) - len(set(near)) == 1              # K=5: one group gets two centroids
for eps in (3.5, 4, 5):                                                      # eps 4 and 5 (and below): one cluster
    lab = DBSCAN(eps=eps, min_samples=5).fit_predict(FIG)                    # min_samples 5 = sklearn's default
    assert len(set(lab) - {-1}) == 1, eps

Q = BANK["24A-B-Q1"]
assert Q["correctIndex"] == 0 and Q["options"][0] == "אלגוריתם KMeans עם K=4" and Q["options"][3].endswith("K=5")
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
NAMES = ["A", "B", "C", "D", "E", "F"]


def plot(pfx):
    """the six points; ids <pfx>-p0 (white, labelled), -p1 / -p2 (colours after assignment 1 / 2, drawn on top),
    -ca0..2 / -cb0..2 (blue / yellow centroid after 0, 1, 2 updates), -ln1..3 (assignment links), distance segments"""
    pl = w.Plot(pfx, (0, 10), (0, 10), w=600, h=560, xticks=range(0, 11, 2), yticks=range(0, 11, 2))
    pl.links("ln1", PTS, CA, A1, kinds=("a", "b"))
    pl.links("ln2", PTS, CB, A2, kinds=("a", "b"))
    pl.links("ln3", PTS, CC, A3, kinds=("a", "b"))
    pl.segs("d-b1", [((3, 1), (1, 1))], kind="a")
    pl.segs("d-b2", [((3, 1), (2, 4))], kind="b")
    pl.segs("d-c1", [((2, 4), (2, 1))], kind="a")
    pl.segs("d-c2", [((2, 4), (5.75, 5.5))], kind="b")
    pl.pts("p0", PTS, "ink", labels=NAMES)
    pl.pts("p1", PTS, ["a" if k == 0 else "b" for k in A1], hidden=True)
    pl.pts("p2", PTS, ["a" if k == 0 else "b" for k in A2], hidden=True)
    for tag, C in (("0", CA), ("1", CB), ("2", CC)):
        pl.centroid(f"ca{tag}", *C[0], kind="a")
        pl.centroid(f"cb{tag}", *C[1], kind="b")
    pl.text("t-b1", 2, 1, "2", kind="a", dy=-12)
    pl.text("t-b2", 2.5, 2.5, "3.16", kind="b", dx=-36)
    pl.text("t-c1", 2, 2.5, "3", kind="a", dx=-22)
    pl.text("t-c2", 3.9, 4.75, "4.04", kind="b", dy=-16)
    return pl.svg()


RAST = st.raster("xr", "images/exams/24A-B-Q1.png", 620, (616, 455),
                 rings=[("tl", 214, 104, 62), ("tr", 409, 104, 66), ("bl", 214, 302, 50), ("br", 409, 302, 56)])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נריץ K-Means ביד, צעד אחר צעד."),
    P("נשייך נקודות למרכז הקרוב, נזיז את המרכזים, ונחשב את ה-SSE."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">M02 · מודלים והערכה</div><h1>K-Means צעד אחר צעד</h1>'
         '<p>לבצע סבב של K-Means ביד: לשייך נקודות למרכז הקרוב, לחשב מרכזים חדשים ולחשב SSE.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("K-Means מחלק נקודות ל-k אשכולות. לכל אשכול יש **מרכז**, והמרכזים מתחילים במקום כלשהו.",
      say="קֵיי מִינְס מחלק נקודות לקֵיי אשכולות. לכל אשכול יש מרכז, והמרכזים מתחילים במקום כלשהו."),
    P("ואז חוזרים על שני צעדים.", hold=0.2),
    P("צעד ראשון, **שיוך**: כל נקודה הולכת למרכז הקרוב אליה.", do=show("i-1")),
    P("צעד שני, **עדכון**: כל מרכז זז לממוצע של הנקודות ששויכו אליו.", do=show("i-2")),
    P("עוצרים כשהשיוך כבר לא משתנה.", do=show("i-3"), hold=0.3),
    P("המרחק הוא מרחק רגיל במישור: שורש של סכום ריבועי ההפרשים.", do=show("i-d")),
    P("וממוצע של נקודות מחשבים בכל ציר לחוד: ממוצע האִקְסים, וממוצע הוַואים.", do=show("i-m"), hold=0.4),
], stage='<div class="ml-col">'
         + w.eq("i-d", "$d = \\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$", 46)
         + w.eq("i-m", "$\\text{center} = (\\bar{x},\\ \\bar{y})$", 46) + "</div>",
   panel=st.card("i-1", "rule", "1️⃣ <b>שיוך</b>: כל נקודה למרכז הקרוב")
         + st.card("i-2", "rule", "2️⃣ <b>עדכון</b>: מרכז = ממוצע הנקודות שלו")
         + st.card("i-3", "ex", "עוצרים כשהשיוך לא משתנה"))

round1 = Scene("round1", "סבב ראשון", [
    P("שש נקודות, ו-k שווה שתיים. המרכזים ההתחלתיים: הנקודה A והנקודה C.", do=show("pa-ca0", "pa-cb0"),
      say="שש נקודות, וקֵיי שווה שתיים. המרכזים ההתחלתיים: הנקודה אֵיי, והנקודה סִי."),
    P("נתחיל בנקודה B. המרחק שלה למרכז הכחול הוא 2.", do=show("pa-d-b1", "pa-t-b1"),
      say="נתחיל בנקודה בִּי. המרחק שלה למרכז הכחול הוא שתיים."),
    P("ולמרכז הצהוב: שורש של אחת ועוד תשע, כלומר שורש עשר, בערך 3.16. B הולכת לכחול.", do=show("pa-d-b2", "pa-t-b2", "r1-b"),
      say="ולמרכז הצהוב: שורש של אחת ועוד תשע, כלומר שורש עשר, בערך שלוש נקודה אחת שש. בִּי הולכת לכחול."),
    P("כך עושים לכל נקודה. שלוש הנקודות מימין קרובות יותר לצהוב, שיושב גבוה יותר.",
      do=hide("pa-d-b1", "pa-d-b2", "pa-t-b1", "pa-t-b2") + show("pa-p1", "pa-ln1")),
    P("שימו לב: C עצמה צהובה, כי היא המרכז הצהוב.", hold=0.3,
      say="שימו לב: סִי עצמה צהובה, כי היא המרכז הצהוב."),
    P("עכשיו עדכון. הכחול זז לממוצע של A ו-B: הנקודה שתיים, אחת.", do=hide("pa-ca0", "pa-ln1") + show("pa-ca1", "r1-a"),
      say="עכשיו עדכון. הכחול זז לממוצע של אֵיי ובִּי: הנקודה שתיים, אחת."),
    P("הצהוב זז לממוצע של ארבע נקודות: 23 חלקי 4 זה 5.75, ו-22 חלקי 4 זה 5.5.", do=hide("pa-cb0") + show("pa-cb1", "r1-c"),
      say="הצהוב זז לממוצע של ארבע נקודות: עשרים ושלוש חלקי ארבע זה חמש נקודה שבעים וחמש, ועשרים ושתיים חלקי ארבע זה חמש וחצי.",
      hold=0.4),
], stage=f'<div class="ml-rowc">{plot("pa")}</div>',
   panel=st.card("r1-b", "ex", "$B$: מרחק $2$ לכחול, $\\sqrt{10} \\approx 3.16$ לצהוב ← כחול")
         + st.card("r1-a", "ex", "כחול: $\\left(\\frac{1+3}{2},\\ \\frac{1+1}{2}\\right) = (2,\\ 1)$")
         + st.card("r1-c", "ex", "צהוב: $\\left(\\frac{23}{4},\\ \\frac{22}{4}\\right) = (5.75,\\ 5.5)$"))

round2 = Scene("round2", "סבב שני", [
    P("סבב שני: משייכים מחדש לפי המרכזים החדשים.", do=show("pb-ca1", "pb-cb1", "pb-p1")),
    P("הנקודה המעניינת היא C. המרחק שלה לכחול, שזז לשתיים, אחת, הוא בדיוק 3.", do=show("pb-d-c1", "pb-t-c1"),
      say="הנקודה המעניינת היא סִי. המרחק שלה לכחול, שזז לשתיים, אחת, הוא בדיוק שלוש."),
    P("והמרחק לצהוב, שזז ימינה, הוא בערך 4.04. לכן C **עוברת** לכחול.", do=show("pb-d-c2", "pb-t-c2", "r2-c"),
      say="והמרחק לצהוב, שזז ימינה, הוא בערך ארבע נקודה אפס ארבע. לכן סִי עוברת לכחול."),
    P("כל השאר נשארות במקומן.", do=hide("pb-d-c1", "pb-d-c2", "pb-t-c1", "pb-t-c2") + show("pb-p2", "pb-ln2"), hold=0.3),
    P("ועדכון: הכחול הוא עכשיו הממוצע של A, B ו-C, הנקודה שתיים, שתיים.", do=hide("pb-ca1", "pb-ln2") + show("pb-ca2", "r2-a"),
      say="ועדכון: הכחול הוא עכשיו הממוצע של אֵיי, בִּי וסִי, הנקודה שתיים, שתיים."),
    P("והצהוב הוא הממוצע של D, E ו-F: הנקודה שבע, שש.", do=hide("pb-cb1") + show("pb-cb2"),
      say="והצהוב הוא הממוצע של דִּי, אִי ואֶף: הנקודה שבע, שש."),
    P("סבב שלישי: משייכים שוב, ואף נקודה לא מחליפה צבע. השיוך התייצב, ועוצרים.", do=show("pb-ln3", "r2-s"), hold=0.4),
], stage=f'<div class="ml-rowc">{plot("pb")}</div>',
   panel=st.card("r2-c", "ex", "$C$: $3$ לכחול, $4.04$ לצהוב ← עוברת לכחול")
         + st.card("r2-a", "ex", "כחול: $(2,\\ 2)$ · צהוב: $(7,\\ 6)$")
         + st.card("r2-s", "rule", "🔑 השיוך לא השתנה ← העצירה"))

sse = Scene("sse", "SSE", [
    P("כמה טובה החלוקה? מודדים את **SSE**: סכום ריבועי המרחקים של כל נקודה מהמרכז שלה.", do=show("s-def")),
    P("באשכול הכחול: A ו-B במרחק בריבוע 2 כל אחת, ו-C במרחק בריבוע 4. יחד 8.", do=show("s-a"),
      say="באשכול הכחול: אֵיי ובִּי במרחק בריבוע שתיים כל אחת, וסִי במרחק בריבוע ארבע. יחד שמונה."),
    P("באשכול הצהוב יוצא בדיוק אותו דבר: עוד 8. סך הכול SSE שווה 16.", do=show("s-b", "s-t")),
    P("להשוואה: עם המרכזים ההתחלתיים, ה-SSE היה 99.", do=show("s-0")),
    P("כל סבב של שיוך ועדכון רק מקטין את ה-SSE, או משאיר אותו. לכן האלגוריתם תמיד עוצר.", do=show("s-k"), hold=0.4),
], stage='<div class="ml-col">'
         + w.eq("s-def", "$\\text{SSE} = \\sum_i \\lVert p_i - c(p_i) \\rVert^2$", 44)
         + w.eq("s-a", "$2 + 2 + 4 = 8$", 40)
         + w.eq("s-b", "$2 + 2 + 4 = 8$", 40)
         + w.chip("s-t", "SSE = 8 + 8 = 16", "ok")
         + w.chip("s-0", "בהתחלה: SSE = 99", "warn") + "</div>",
   panel=st.card("s-k", "rule", "🔑 שיוך ועדכון רק מקטינים את ה-SSE"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: איזה אלגוריתם יאשכל הכי טוב את הנתונים שבאיור?"),
    P("מסתכלים על הצורה: ארבע קבוצות עגולות, מופרדות, וכל אחת סביב מרכז אחד.", do=show("xr-ring-tl", "xr-ring-tr", "xr-ring-bl", "xr-ring-br")),
    P("זה בדיוק המקרה ש-K-Means טוב בו: אשכולות עגולים, שכל אחד מתואר היטב על ידי מרכז.", do=show("x-1")),
    P("ומספר האשכולות שנותנים לו צריך להתאים לנתונים: ארבע.", do=show("q-ok-0"), hold=0.3),
    P("עם k שווה חמש, יש מרכז אחד יותר מקבוצות. אחת הקבוצות תיחתך לשניים, וזה בדקנו על הנקודות שבאיור.", do=show("q-x-3", "q-n-3"),
      say="עם קֵיי שווה חמש, יש מרכז אחד יותר מקבוצות. אחת הקבוצות תיחתך לשניים, וזה בדקנו על הנקודות שבאיור."),
    P("ו-DBSCAN? רדיוס של 4 או 5 גדול כמעט כמו הרווחים בין הקבוצות.", do=show("x-2"),
      say="ודִּי בִּי סְקָאן? רדיוס של ארבע או חמש גדול כמעט כמו הרווחים בין הקבוצות."),
    P("עם רדיוס כזה, הקבוצות והנקודות הפזורות ביניהן מתחברות, וכל הנתונים הופכים לאשכול **אחד**.", do=show("q-x-1", "q-n-1", "q-x-2", "q-n-2")),
    P("המלכודת: DBSCAN מתאים לצורות מוזרות. כאן הצורות פשוטות, ו-K-Means עם k נכון מנצח.", do=show("x-t"), hold=0.6,
      say="המלכודת: דִּי בִּי סְקָאן מתאים לצורות מוזרות. כאן הצורות פשוטות, וקֵיי מִינְס עם קֵיי נכון מנצח."),
], stage=f'<div class="ml-col">{RAST}'
         + st.card("x-1", "rule", "🔑 קבוצות עגולות ונפרדות ← K-Means, עם k = מספר הקבוצות")
         + "</div>",
   panel=w.stem(Q["id"], "איזה אלגוריתם יאשכל את הנתונים שבאיור בצורה הטובה ביותר?")
         + f'<div class="ml-opts">{st.options("q", OPTS, notes={1: "הכול מתחבר", 2: "הכול מתחבר", 3: "חותך קבוצה"})}</div>'
         + st.card("x-2", "ex", "רדיוס של 4 או 5: בערך הרווח בין הקבוצות")
         + st.card("x-t", "trap", "⚠️ צורות עגולות ונפרדות: K-Means, לא DBSCAN"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: K-Means חוזר על שני צעדים. שיוך כל נקודה למרכז הקרוב.", do=show("r-1"),
      say="לסיכום: קֵיי מִינְס חוזר על שני צעדים. שיוך כל נקודה למרכז הקרוב."),
    P("ועדכון כל מרכז לממוצע של הנקודות שלו, בכל ציר לחוד.", do=show("r-2")),
    P("עוצרים כשהשיוך לא משתנה. ה-SSE הוא סכום ריבועי המרחקים למרכז.", do=show("r-3")),
    P("ו-K-Means מתאים לאשכולות עגולים, כשמספר האשכולות נכון. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ml-col">' + w.eq("r-eq", "$d = \\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$", 46, hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 שיוך: למרכז <b>הקרוב</b>")
         + st.card("r-2", "rule", "🔑 עדכון: מרכז = <b>ממוצע</b> בכל ציר")
         + st.card("r-3", "rule", "🔑 SSE = סכום ריבועי המרחקים")
         + st.card("r-4", "trap", "⚠️ K-Means: אשכולות עגולים, k נכון"))

VIDEO = Video("M02", "ml", "K-Means צעד אחר צעד", [title, idea, round1, round2, sse, exam, recap],
              bank={"24A-B-Q1": 0})

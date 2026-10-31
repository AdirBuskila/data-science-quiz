# -*- coding: utf-8 -*-
"""M03 · DBSCAN ואשכול היררכי — video script (build: tools/video/vid.py M03).

Source: courses/ml/M03.js (lesson + goal: when DBSCAN beats K-Means, what eps and min_samples decide, what the
height of a dendrogram link means). Exam anchor: 26A-B-Q13 (DBSCAN's clear advantage: no preset number of clusters,
and it handles outliers), which no guided quiz uses.
Not used on purpose: the M03 quiz data (1,2,3,10,11,12,50 with eps 2 / 10 and min_samples 2 / 4; the two moons;
single linkage on 1, 2, 6) and the lesson's examples. 25A-B-Q19 (fewer clusters: "raise eps AND lower min_samples")
is avoided: its claim 2 pulls min_samples the opposite way from the lesson's rule (see the report).
Worked examples (new): DBSCAN on 4,5,6,7,15,16,17,30 with eps 1.5 and min_samples 3 (core / border / noise);
three groups of different density, 2,3,4,5 / 10..13 / 30,36,42,48, where no single eps finds all three; single
linkage on 2, 4, 9, 10, 20. Every label, core set and merge height is asserted against sklearn / scipy.
"""
import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.cluster import DBSCAN

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_ml as w

# ---------------------------------------------------------------- DBSCAN, core / border / noise (verified)
V1 = [4, 5, 6, 7, 15, 16, 17, 30]
D1 = DBSCAN(eps=1.5, min_samples=3).fit(np.array(V1, float).reshape(-1, 1))
assert D1.labels_.tolist() == [0, 0, 0, 0, 1, 1, 1, -1]
assert [V1[i] for i in D1.core_sample_indices_] == [5, 6, 16]


def neigh(v, vals, eps):
    return [u for u in vals if abs(u - v) <= eps]


assert neigh(4, V1, 1.5) == [4, 5] and neigh(5, V1, 1.5) == [4, 5, 6] and neigh(30, V1, 1.5) == [30]
ROLE = {}
for i, v in enumerate(V1):
    ROLE[v] = "core" if i in D1.core_sample_indices_ else ("noise" if D1.labels_[i] == -1 else "border")
assert [v for v in V1 if ROLE[v] == "border"] == [4, 7, 15, 17]

# ---------------------------------------------------------------- different densities (verified)
V2 = [2, 3, 4, 5, 10, 11, 12, 13, 30, 36, 42, 48]
X2 = np.array(V2, float).reshape(-1, 1)
counts = {}
for eps in np.arange(0.25, 40.01, 0.25):
    lab = DBSCAN(eps=eps, min_samples=3).fit_predict(X2)
    counts[float(eps)] = len(set(lab) - {-1})
assert max(counts.values()) == 2 and 3 not in counts.values()          # no eps gives the three groups
L15 = DBSCAN(eps=1.5, min_samples=3).fit_predict(X2)
assert L15.tolist() == [0] * 4 + [1] * 4 + [-1] * 4                     # small eps: the sparse group is noise
L6 = DBSCAN(eps=6, min_samples=3).fit_predict(X2)
assert L6.tolist() == [0] * 8 + [1] * 4                                 # eps 6: sparse found, dense pair merged
assert 10 - 5 == 5 and 36 - 30 == 6                                     # the two gaps that clash

# ---------------------------------------------------------------- dendrogram (verified)
V3 = [2, 4, 9, 10, 20]
Z = linkage(np.array(V3, float).reshape(-1, 1), method="single")
assert Z[:, 2].tolist() == [1, 2, 5, 10]
assert fcluster(Z, t=7, criterion="distance").tolist() == [1, 1, 1, 1, 2]   # cut at 7: two clusters
assert 9 - 4 == 5 and 20 - 10 == 10                                          # single linkage = closest pair

# exam 26A-B-Q13
Q = BANK["26A-B-Q13"]
assert Q["correctIndex"] == 0 and "Outliers" in Q["options"][0] and "סנטרואידים" in Q["options"][3]
assert "צפיפות" in Q["options"][2] and "מהיר" in Q["options"][1]
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
KIND = {"core": "a", "border": "d", "noise": "bad"}
A = w.Plot("da", (0, 32), (0, 1), w=960, h=250, xticks=range(0, 33, 4), yticks=(), xname="", pad=(30, 30, 20, 60))
A.segs("e4", [((4 - 1.5, 0.62), (4 + 1.5, 0.62)), ((2.5, 0.52), (2.5, 0.72)), ((5.5, 0.52), (5.5, 0.72))], kind="d", cls="ml-fit")
A.segs("e5", [((5 - 1.5, 0.82), (5 + 1.5, 0.82)), ((3.5, 0.72), (3.5, 0.92)), ((6.5, 0.72), (6.5, 0.92))], kind="a", cls="ml-fit")
A.segs("e30", [((28.5, 0.62), (31.5, 0.62)), ((28.5, 0.52), (28.5, 0.72)), ((31.5, 0.52), (31.5, 0.72))], kind="bad", cls="ml-fit")
A.pts("p0", [(v, 0.25) for v in V1], "ink", labels=[str(v) for v in V1], lab_top=True, r=10)
A.pts("p1", [(v, 0.25) for v in V1], [KIND[ROLE[v]] for v in V1], hidden=True, r=10)
A.text("c1", 5.5, 0.25, "אשכול 1", kind="a", dy=-72, hidden=True)
A.text("c2", 16, 0.25, "אשכול 2", kind="a", dy=-72, hidden=True)
A.text("cn", 30, 0.25, "רעש", kind="bad", dy=-72, hidden=True)
PA = A.svg()

B = w.Plot("db", (0, 50), (0, 1), w=960, h=230, xticks=range(0, 51, 5), yticks=(), xname="", pad=(30, 30, 20, 60))
B.pts("p0", [(v, 0.3) for v in V2], "ink")
B.pts("p1", [(v, 0.3) for v in V2], ["a"] * 4 + ["b"] * 4 + ["bad"] * 4, hidden=True)
B.pts("p2", [(v, 0.3) for v in V2], ["a"] * 8 + ["c"] * 4, hidden=True)
PB = B.svg()

DEN, _, _ = w.dendro("dn", V3, "single", w=760, h=430, hmax=12, hticks=[0, 2, 4, 6, 8, 10, 12], cut=7)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר שני אלגוריתמי אשכול נוספים: DBSCAN, ואשכול היררכי."),
    P("נראה מה הפרמטרים של DBSCAN קובעים, ומה אומר הגובה בדנדרוגרם."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">M03 · מודלים והערכה</div><h1>DBSCAN ואשכול היררכי</h1>'
         '<p>להבין מתי DBSCAN עדיף על K-Means, מה eps ו-min_samples קובעים, ומה גובה הקו בדנדרוגרם.</p>', layout="title")

dbscan = Scene("dbscan", "DBSCAN", [
    P("DBSCAN לא מחפש מרכזים. הוא מחפש אזורים **צפופים**."),
    P("יש לו שני פרמטרים. הראשון הוא אֶפְּס: רדיוס השכונה סביב כל נקודה.", do=show("b-eps"),
      say="יש לו שני פרמטרים. הראשון הוא אֶפְּס: רדיוס השכונה סביב כל נקודה."),
    P("השני, min_samples: כמה נקודות צריך בשכונה, כולל הנקודה עצמה, כדי שהיא תהיה **ליבה**.", do=show("b-ms")),
    P("נריץ עם רדיוס אחד וחצי, ושלוש נקודות לפחות.", do=show("b-run")),
    P("הנקודה 5: בשכונה שלה יש 4, 5 ו-6. שלוש נקודות, ולכן היא ליבה.", do=show("da-e5"),
      say="הנקודה חמש: בשכונה שלה יש ארבע, חמש ושש. שלוש נקודות, ולכן היא ליבה."),
    P("הנקודה 4: בשכונה שלה רק 4 ו-5. היא לא ליבה, אבל היא בשכונה של ליבה, ולכן היא נקודת **גבול** באשכול.",
      do=show("da-e4"), say="הנקודה ארבע: בשכונה שלה רק ארבע וחמש. היא לא ליבה, אבל היא בשכונה של ליבה, ולכן היא נקודת גבול באשכול."),
    P("והנקודה 30: לבד לגמרי. היא לא ליבה ולא ליד ליבה, ולכן היא **רעש**.", do=show("da-e30"),
      say="והנקודה שלושים: לבד לגמרי. היא לא ליבה ולא ליד ליבה, ולכן היא רעש."),
    P("התוצאה: שני אשכולות, ונקודת רעש אחת. ליבות בכחול, גבול בירוק, רעש באדום.",
      do=hide("da-e4", "da-e5", "da-e30") + show("da-p1", "da-c1", "da-c2", "da-cn"), hold=0.3),
    P("שימו לב: לא אמרנו לאלגוריתם כמה אשכולות יש. הוא מצא אותם לבד.", do=show("b-k1")),
    P("והחריג לא נדחס לאף אשכול: הוא קיבל תווית נפרדת, מינוס אחת.", do=show("b-k2"), hold=0.4),
], stage=f'<div class="ml-col">{PA}'
         + w.chip("b-run", "eps = 1.5 · min_samples = 3", "info") + "</div>",
   panel=st.card("b-eps", "ex", "<b>eps</b>: רדיוס השכונה")
         + st.card("b-ms", "ex", "<b>min_samples</b>: כמה נקודות בשכונה כדי להיות ליבה")
         + st.card("b-k1", "rule", "🔑 אין צורך לקבוע מראש כמה אשכולות")
         + st.card("b-k2", "rule", "🔑 חריג ← רעש, תווית $-1$"))

density = Scene("density", "צפיפויות שונות", [
    P("אבל ל-DBSCAN יש חולשה. יש לו רדיוס **אחד** לכל הנתונים."),
    P("כאן שלוש קבוצות: שתיים צפופות מאוד משמאל, ואחת דלילה מימין.", do=show("db-wrap")),
    P("רדיוס קטן, אחד וחצי: שתי הקבוצות הצפופות נמצאות, אבל הדלילה כולה הופכת לרעש.", do=show("db-p1", "d-1")),
    P("כדי למצוא את הדלילה צריך רדיוס של לפחות 6, כי זה הרווח בין הנקודות שלה.", do=hide("db-p1") + show("db-p2", "d-2"),
      say="כדי למצוא את הדלילה צריך רדיוס של לפחות שש, כי זה הרווח בין הנקודות שלה."),
    P("אבל אז הפער של 5 בין שתי הקבוצות הצפופות נבלע, והן מתמזגות לאשכול אחד.",
      say="אבל אז הפער של חמש בין שתי הקבוצות הצפופות נבלע, והן מתמזגות לאשכול אחד."),
    P("בדקנו כל רדיוס: אף אחד לא נותן שלושה אשכולות.", do=show("d-k"), hold=0.4),
], stage=f'<div class="ml-col"><div id="db-wrap" class="h">{PB}</div>'
         + w.chip("d-1", "eps = 1.5: שני אשכולות + 4 רעש", "warn")
         + w.chip("d-2", "eps = 6: הצפופות מתמזגות", "warn") + "</div>",
   panel=st.card("d-k", "trap", "⚠️ צפיפויות שונות מאוד: אין eps אחד שמתאים לכולן"))

hier = Scene("hier", "אשכול היררכי", [
    P("ועכשיו אשכול היררכי. מתחילים כשכל נקודה היא אשכול בפני עצמה."),
    P("בכל צעד ממזגים את שני האשכולות הקרובים ביותר, ומציירים את המיזוג בעץ שנקרא **דנדרוגרם**."),
    P("נשתמש בקישור יחיד: המרחק בין אשכולות הוא המרחק בין שתי הנקודות **הקרובות** ביותר שלהם.", do=show("h-1")),
    P("הכי קרובות הן 9 ו-10, במרחק 1. הן מתמזגות בגובה 1.", do=show("dn-m0"),
      say="הכי קרובות הן תשע ועשר, במרחק אחת. הן מתמזגות בגובה אחת."),
    P("אחר כך 2 ו-4, במרחק 2.", do=show("dn-m1"), say="אחר כך שתיים וארבע, במרחק שתיים."),
    P("אחר כך שני הזוגות. הנקודות הקרובות שלהם הן 4 ו-9, ולכן הגובה 5.", do=show("dn-m2"),
      say="אחר כך שני הזוגות. הנקודות הקרובות שלהם הן ארבע ותשע, ולכן הגובה חמש."),
    P("ולבסוף 20 מצטרפת, במרחק 10 מהנקודה 10.", do=show("dn-m3"),
      say="ולבסוף עשרים מצטרפת, במרחק עשר מהנקודה עשר."),
    P("אז גובה הקו הוא **המרחק** בין שני האשכולות שמוזגו. קו ארוך פירושו קבוצות רחוקות.", do=show("h-k"), hold=0.3),
    P("ואת מספר האשכולות בוחרים בסוף, בחיתוך. חותכים בגובה 7, ומקבלים שני אשכולות.", do=show("dn-cut", "h-2"),
      say="ואת מספר האשכולות בוחרים בסוף, בחיתוך. חותכים בגובה שבע, ומקבלים שני אשכולות.", hold=0.4),
], stage=f'<div class="ml-col">{DEN}</div>',
   panel=st.card("h-1", "ex", "קישור יחיד: המרחק בין הנקודות <b>הקרובות</b>")
         + st.card("h-k", "rule", "🔑 גובה הקו = <b>המרחק</b> שבו מוזגו שני האשכולות")
         + st.card("h-2", "ex", "חיתוך בגובה 7: $\\{2, 4, 9, 10\\}$ ו-$\\{20\\}$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מהו היתרון המובהק של DBSCAN על פני K-Means ואשכול היררכי?"),
    P("ראינו את זה בהרצה הראשונה: לא אמרנו לו כמה אשכולות יש, והחריג סומן כרעש.", do=show("q-ok-0"), hold=0.3),
    P("ב-K-Means, לעומת זאת, כל נקודה, גם חריגה, נדחסת לאשכול כלשהו.", do=show("x-1"),
      say="בקֵיי מִינְס, לעומת זאת, כל נקודה, גם חריגה, נדחסת לאשכול כלשהו."),
    P("״עובד מצוין כשהצפיפויות שונות מאוד״: בדיוק ההפך. ראינו שרדיוס אחד לא מתאים לכולן.", do=show("q-x-2", "q-n-2")),
    P("״מבוסס על מציאת מרכזים״: זה K-Means. ב-DBSCAN אין מרכזים, יש שכונות וצפיפות.", do=show("q-x-3", "q-n-3")),
    P("ומהירות על נתונים קטנים מאוד איננה היתרון שלו. על נתונים קטנים כל האלגוריתמים מהירים.", do=show("q-x-1", "q-n-1")),
    P("המלכודת: DBSCAN מתמודד עם צורות מוזרות ועם רעש, אבל לא עם צפיפויות שונות.", do=show("x-t"), hold=0.6,
      say="המלכודת: דִּי בִּי סְקָאן מתמודד עם צורות מוזרות ועם רעש, אבל לא עם צפיפויות שונות."),
], stage=w.stem(Q["id"], "מהו היתרון המובהק של DBSCAN על פני K-Means או אשכול היררכי?")
         + f'<div class="ml-opts">{st.options("q", OPTS, notes={1: "לא היתרון", 2: "ההפך", 3: "זה K-Means"})}</div>',
   panel=st.card("x-1", "ex", "ב-K-Means כל נקודה, גם חריג, נדחסת לאשכול")
         + st.card("x-t", "trap", "⚠️ DBSCAN: לא צריך k, ומסמן רעש. אבל eps אחד לכל הצפיפויות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ב-DBSCAN, נקודה עם מספיק שכנים בתוך הרדיוס היא ליבה.", do=show("r-1"),
      say="לסיכום: בדִּי בִּי סְקָאן, נקודה עם מספיק שכנים בתוך הרדיוס היא ליבה."),
    P("ליבות קרובות יוצרות אשכול, ומה שלא מגיע לאף ליבה הוא רעש. אין צורך לקבוע מראש כמה אשכולות.", do=show("r-2")),
    P("אבל רדיוס אחד לא מתאים לקבוצות בצפיפויות שונות מאוד.", do=show("r-3")),
    P("ובדנדרוגרם, גובה הקו הוא המרחק שבו מוזגו שני אשכולות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="ml-col">{w.dendro("dr", V3, "single", w=700, h=400, hmax=12, hticks=[0, 4, 8, 12])[0].replace(chr(34) + "h" + chr(34), chr(34) + chr(34))}</div>',
   panel=st.card("r-1", "rule", "🔑 ליבה = לפחות min_samples נקודות בתוך eps")
         + st.card("r-2", "rule", "🔑 בלי k מראש, וחריג ← רעש")
         + st.card("r-3", "trap", "⚠️ צפיפויות שונות מאוד: eps אחד לא מספיק")
         + st.card("r-4", "rule", "🔑 גובה בדנדרוגרם = מרחק המיזוג"))

VIDEO = Video("M03", "ml", "DBSCAN ואשכול היררכי", [title, dbscan, density, hier, exam, recap],
              bank={"26A-B-Q13": 0})

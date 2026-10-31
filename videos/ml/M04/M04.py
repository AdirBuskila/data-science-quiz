# -*- coding: utf-8 -*-
"""M04 · PCA: הורדת ממדים — video script (build: tools/video/vid.py M04).

Source: courses/ml/M04.js (lesson + goal: what PCA does, what n_components and explained_variance_ratio_ say, and
the variance share of a component). Exam anchor: P-37 (the meaning of explained_variance_ratio_; key = index 1),
which no guided quiz uses.
Not used on purpose: the M04 quiz data (the collinear points (1,1)..(4,4), the (100,5) table, variances 4:1,
4 features kept, the order of the ratios as a question) and the lesson's 9:1 example. 24B-B-Q12 / 25A-B-Q12 / P-32 /
P-44 are also free, but one exam item is enough.
Worked example (new): six points (2,2),(4,2),(3,5),(5,7),(8,6),(8,8) around (5,5); the squared distances from the
centre add up to 64, of which 56 lie along the diagonal (PC1) and 8 across it (PC2), so the ratios are 0.875 / 0.125.
Asserted against sklearn's PCA and numpy's eigen-decomposition.
"""
import numpy as np
from sklearn.decomposition import PCA

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_ml as w

# ---------------------------------------------------------------- data (verified)
PTS = [(2, 2), (4, 2), (3, 5), (5, 7), (8, 6), (8, 8)]
X = np.array(PTS, float)
assert X.mean(axis=0).tolist() == [5, 5]
D = X - 5
TOT = float((D ** 2).sum())
U = np.array([1, 1]) / np.sqrt(2)
V = np.array([1, -1]) / np.sqrt(2)
ALONG, ACROSS = float(((D @ U) ** 2).sum()), float(((D @ V) ** 2).sum())
assert TOT == 64 and round(ALONG, 9) == 56 and round(ACROSS, 9) == 8
assert [((x - 5) ** 2 + (y - 5) ** 2) for x, y in PTS] == [18, 10, 4, 4, 10, 18]
pca = PCA(2).fit(X)
assert np.allclose(pca.explained_variance_ratio_, [0.875, 0.125])
assert np.allclose(np.abs(pca.components_[0]), U)                          # PC1 is the diagonal direction
ev = np.sort(np.linalg.eigvalsh(np.cov(X.T)))[::-1]
assert np.allclose(ev / ev.sum(), [0.875, 0.125])
P1 = PCA(n_components=1)
Z1 = P1.fit_transform(X)
assert Z1.shape == (6, 1) and np.allclose(P1.explained_variance_ratio_, [0.875])
PROJ = [tuple(5 + (D[i] @ U) * U) for i in range(6)]                       # foot of each point on PC1
assert np.allclose(PROJ, [(2, 2), (3, 3), (4, 4), (6, 6), (7, 7), (8, 8)])

# exam P-37
Q = BANK["P-37"]
assert Q["correctIndex"] == 1 and "אחוז השונות" in Q["options"][1] and "outliers" in Q["options"][0]
assert Q["options"][2] == "אף תשובה אינה נכונה"
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figure
PL = w.Plot("pc", (0, 10), (0, 10), w=560, h=540, xticks=range(0, 11, 2), yticks=range(0, 11, 2), xname="x₁", yname="x₂")
PL.fline("l1", 0, 1, kind="b", x0=0.5, x1=9.5)
PL.fline("l2", 10, -1, kind="c", x0=3, x1=7)
PL.segs("proj", [(p, q) for p, q in zip(PTS, PROJ)], kind="c")
PL.pts("p", PTS, "ink")
PL.pts("z", PROJ, "b", r=9, hidden=True)
PL.text("t1", 9.3, 9.3, "PC1", kind="b", dx=-6, dy=-18)
PL.text("t2", 7, 3, "PC2", kind="c", dx=24, dy=22)
PL.centroid("m", 5, 5, kind="ink", size=10, label=None)
PLOT = PL.svg()

CODE = w.code("cd", "pca = PCA(<b>n_components=1</b>)\nZ = pca.fit_transform(X)\n<i># (6, 2) → (6, 1)</i>\n"
                    "pca.explained_variance_ratio_\n<i>→ [0.875]</i>", hidden=True, size=24)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד מה PCA עושה, ואיך הוא מוריד ממדים."),
    P("נבין מה אומר n_components, ונחשב את <bdi>explained_variance_ratio_</bdi> על דוגמה."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">M04 · מודלים והערכה</div><h1>PCA: הורדת ממדים</h1>'
         '<p>להבין מה PCA עושה, מה n_components ו-<bdi>explained_variance_ratio_</bdi> אומרים, ולחשב אחוז שונות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("לפעמים יש לנו הרבה עמודות, ורוצים פחות. אבל בלי לאבד הרבה מידע."),
    P("PCA הוא אלגוריתם **לא מונחה**: הוא לא צריך תוויות, רק את הנתונים.", do=show("i-1")),
    P("הוא מוצא צירים חדשים, שנקראים **רכיבים ראשיים**.", do=show("i-2")),
    P("הרכיב הראשון הוא הכיוון שבו הנתונים **מתפזרים הכי הרבה**. כלומר, שבו השונות הכי גדולה.", hold=0.2),
    P("הרכיב השני מאונך לו, ותופס את מה שנשאר.", hold=0.3),
    P("ואז שומרים רק את הרכיבים הראשונים, וזורקים את השאר.", do=show("i-3")),
    P("שימו לב: PCA מצמצם **עמודות**. מספר השורות, הדוגמאות, לא משתנה.", do=show("i-4"), hold=0.4),
], stage='<div class="ml-col">' + w.eq("i-eq", "$(n \\times d) \\;\\to\\; (n \\times k), \\quad k &lt; d$", 50, hidden=False)
         + '<div class="ml-note">n שורות נשארות · d עמודות הופכות ל-k</div></div>',
   panel=st.card("i-1", "rule", "🔑 PCA: <b>לא מונחה</b>, הורדת ממדים")
         + st.card("i-2", "ex", "רכיב ראשי = ציר חדש. הראשון: כיוון הפיזור הגדול ביותר")
         + st.card("i-3", "ex", "שומרים $k$ רכיבים ראשונים")
         + st.card("i-4", "trap", "⚠️ מצמצם <b>עמודות</b>, לא שורות"))

worked = Scene("worked", "דוגמה", [
    P("שש נקודות עם שתי עמודות. המרכז שלהן הוא הנקודה חמש, חמש.", do=show("pc-m")),
    P("רואים שהן מתפזרות בעיקר לאורך האלכסון. זה הרכיב הראשון.", do=show("pc-l1", "pc-t1")),
    P("והרכיב השני מאונך לו.", do=show("pc-l2", "pc-t2"), hold=0.3),
    P("כמה פיזור יש בסך הכול? נסכום את ריבועי המרחקים של כל הנקודות מהמרכז: יוצא 64.", do=show("w-1"),
      say="כמה פיזור יש בסך הכול? נסכום את ריבועי המרחקים של כל הנקודות מהמרכז: יוצא שישים וארבע."),
    P("כל ריבוע כזה מתפרק לחלק לאורך האלכסון ולחלק שמאונך לו, כמו בפיתגורס.", hold=0.2),
    P("לאורך הרכיב הראשון מצטבר 56, ובניצב אליו רק 8.", do=show("pc-proj", "w-2"),
      say="לאורך הרכיב הראשון מצטבר חמישים ושש, ובניצב אליו רק שמונה."),
    P("לכן הרכיב הראשון מסביר 56 חלקי 64, כלומר 0.875. והשני 8 חלקי 64, כלומר 0.125.", do=show("w-3"),
      say="לכן הרכיב הראשון מסביר חמישים ושש חלקי שישים וארבע, כלומר אפס נקודה שמונה מאות שבעים וחמש. והשני שמונה חלקי שישים וארבע, כלומר אפס נקודה מאה עשרים וחמש.",
      hold=0.3),
    P("זה בדיוק מה ש-<bdi>explained_variance_ratio_</bdi> מחזיר: לכל רכיב, איזה חלק מהשונות הוא מסביר.", do=show("w-k")),
], stage=f'<div class="ml-rowc">{PLOT}<div class="ml-col" style="width:400px">'
         + w.chip("w-1", "סך הכול: 64", "info")
         + w.chip("w-2", "PC1: 56 · PC2: 8", "warn")
         + w.eq("w-3", "$\\dfrac{56}{64} = 0.875, \\quad \\dfrac{8}{64} = 0.125$", 34) + "</div></div>",
   panel=st.card("w-k", "rule", "🔑 <b>חלק השונות</b> שכל רכיב מסביר:<br><bdi>explained_variance_ratio_</bdi>"))

reduce = Scene("reduce", "שומרים רכיב אחד", [
    P("עכשיו נוריד ממד. בקוד, n_components אומר כמה רכיבים לשמור. כאן אחד.", do=show("cd", "pc2-l1", "pc2-t1")),
    P("כל נקודה יורדת אל הרכיב הראשון, ונשאר לה מספר אחד: המיקום שלה על הקו.", do=show("pc2-z", "pc2-proj")),
    P("הטבלה עוברת משש שורות ושתי עמודות, לשש שורות ועמודה אחת.", hold=0.2),
    P("מה איבדנו? רק את מה שהיה בניצב לקו: 0.125 מהשונות.", do=show("r-1"),
      say="מה איבדנו? רק את מה שהיה בניצב לקו: אפס נקודה מאה עשרים וחמש מהשונות."),
    P("ושמרנו 0.875 ממנה: 87.5 אחוז, עם חצי מהעמודות.", do=show("r-2"),
      say="ושמרנו אפס נקודה שמונה מאות שבעים וחמש ממנה: שמונים ושבעה וחצי אחוז, עם חצי מהעמודות.", hold=0.4),
    P("איך בוחרים כמה רכיבים לשמור? מוסיפים רכיבים לפי הסדר, עד שהחלקים שלהם מצטברים למה שמספיק לנו."),
    P("למשל, אם מספיק לנו שמונים אחוז מהשונות, כאן רכיב אחד כבר עובר את הסף.", hold=0.2),
    P("ובנתונים עם עשרות עמודות, לרוב כמה רכיבים ראשונים תופסים את רוב השונות. זה כל הכוח של PCA.", hold=0.4),
], stage=f'<div class="ml-rowc">{PLOT.replace(chr(34) + "pc", chr(34) + "pc2")}<div class="ml-col" style="width:470px">{CODE}</div></div>',
   panel=st.card("r-1", "ex", "נאבד: $0.125$ מהשונות")
         + st.card("r-2", "rule", "🔑 נשמר: $0.875$, עם עמודה אחת במקום שתיים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אחרי הרצת PCA, מה המשמעות של <bdi>explained_variance_ratio_</bdi>?"),
    P("ראינו: זה וקטור עם מספר לכל רכיב ראשי. המספר הוא החלק מהשונות שהרכיב מסביר.", do=show("q-ok-1"), hold=0.3),
    P("האפשרות שמדברת על כמות הנתונים בעמודה, ועל השאר כחריגים, שגויה פעמיים.", do=show("q-x-0", "q-n-0")),
    P("היא מדברת על **עמודה** של הטבלה, בעוד שהיחס שייך לרכיב ראשי, שהוא ציר חדש.", do=show("x-1")),
    P("והחלק הלא מוסבר הוא לא חריגים. בדוגמה שלנו, 0.125 הוא פשוט הפיזור בניצב לקו.", do=show("x-2"),
      say="והחלק הלא מוסבר הוא לא חריגים. בדוגמה שלנו, אפס נקודה מאה עשרים וחמש הוא פשוט הפיזור בניצב לקו."),
    P("ומכיוון שיש תשובה נכונה, ״אף תשובה אינה נכונה״ נופלת.", do=show("q-x-2", "q-n-2"), hold=0.6),
], stage=w.stem(Q["id"], "לאחר ריצת PCA, מה המשמעות של התכונה <bdi>explained_variance_ratio_</bdi>?")
         + f'<div class="ml-opts">{st.options("q", OPTS, notes={0: "עמודה, חריגים", 2: "יש נכונה"})}</div>',
   panel=st.card("x-1", "trap", "⚠️ היחס שייך ל<b>רכיב ראשי</b>, לא לעמודה של הטבלה")
         + st.card("x-2", "ex", "החלק הלא מוסבר ≠ חריגים: זה פיזור בכיוונים שנזרקו"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: PCA הוא אלגוריתם לא מונחה להורדת ממדים.", do=show("r-a")),
    P("הוא מוצא רכיבים ראשיים: צירים חדשים, והראשון הוא כיוון הפיזור הגדול ביותר.", do=show("r-b")),
    P("n_components אומר כמה רכיבים לשמור, ו-<bdi>explained_variance_ratio_</bdi> אומר איזה חלק מהשונות כל רכיב מסביר.", do=show("r-c")),
    P("והוא מצמצם עמודות, לא שורות. נתראה ברמה הבאה.", do=show("r-d"), hold=0.6),
], stage=f'<div class="ml-col">{w.code("rc", "pca = PCA(<b>n_components=k</b>)" + chr(10) + "pca.<b>explained_variance_ratio_</b>", size=30)}</div>',
   panel=st.card("r-a", "rule", "🔑 PCA: לא מונחה, הורדת ממדים")
         + st.card("r-b", "rule", "🔑 רכיב ראשון = כיוון הפיזור הגדול ביותר")
         + st.card("r-c", "rule", "🔑 ratio = חלק השונות של כל רכיב")
         + st.card("r-d", "trap", "⚠️ פחות <b>עמודות</b>, אותן שורות"))

VIDEO = Video("M04", "ml", "PCA: הורדת ממדים", [title, idea, worked, reduce, exam, recap],
              bank={"P-37": 1})

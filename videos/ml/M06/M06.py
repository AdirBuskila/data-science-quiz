# -*- coding: utf-8 -*-
"""M06 · מטריצת בלבול, Precision, Recall ו-F1 — video script (build: tools/video/vid.py M06).

Source: courses/ml/M06.js (lesson + goal: compute accuracy, Precision, Recall and F1 from a confusion matrix, and the
fold sizes of K-Fold). Exam anchor: 25A-A-Q14 (Recall from a pictured matrix TP=85, FN=15, FP=10, TN=90), which no
guided quiz uses. Its twin 26A-A-Q22 (same matrix) is not a quiz item either.
Not used on purpose: the M06 quiz matrix (TP=40, FN=10, FP=20, TN=30), P=0.5/R=0.75, 120 samples in 5 folds, the
lesson's 30/10/10/50, and the boss items 25A-B-Q18 (F1 from P=0.8, R=0.6) and 26A-B-Q16 (90 of 100 sick found).
Worked examples use a new spam filter (TP=36, FN=4, FP=12, TN=148) and 200 samples in 4 folds.
Every metric is computed here and asserted against sklearn.
"""
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import KFold

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_ml as w


def sk(tp, fn, fp, tn):
    """the same matrix as label vectors, scored by sklearn"""
    y = np.r_[np.ones(tp + fn), np.zeros(fp + tn)]
    p = np.r_[np.ones(tp), np.zeros(fn), np.ones(fp), np.zeros(tn)]
    return {"acc": accuracy_score(y, p), "prec": precision_score(y, p, zero_division=0),
            "rec": recall_score(y, p), "f1": f1_score(y, p, zero_division=0)}


def same(a, b):
    for k in b:
        assert abs(a[k] - b[k]) < 1e-12, k


# ---------------------------------------------------------------- spam filter (verified)
M = w.metrics(36, 4, 12, 148)
same(M, sk(36, 4, 12, 148))
assert M["n"] == 200 and 36 + 4 == 40
assert M["prec"] == 0.75 and M["rec"] == 0.9 and M["acc"] == 0.92
assert round(M["f1"], 4) == 0.8182 and w.round_half_up(M["f1"]) == 0.82
assert (M["prec"] + M["rec"]) / 2 == 0.825 and M["f1"] < 0.825       # harmonic mean below the arithmetic one

Z = w.metrics(0, 40, 0, 160)                                           # "never spam"
same(Z, sk(0, 40, 0, 160))
assert Z["acc"] == 0.8 and Z["rec"] == 0 and Z["prec"] == 0

# K-Fold: 200 samples, K = 4
KF = list(KFold(n_splits=4).split(np.zeros(200)))
assert all(len(v) == 50 and len(t) == 150 for t, v in KF)
assert sorted(np.concatenate([v for _, v in KF]).tolist()) == list(range(200))   # each sample validated once

# exam 25A-A-Q14
Q = BANK["25A-A-Q14"]
assert Q["correctIndex"] == 0 and Q["options"] == ["0.85", "0.88", "0.89", "0.9"]
E = w.metrics(85, 15, 10, 90)
same(E, sk(85, 15, 10, 90))
assert E["rec"] == 0.85
assert E["acc"] == 0.875 and w.round_half_up(E["acc"]) == 0.88
assert round(E["prec"], 4) == 0.8947 and w.round_half_up(E["prec"]) == 0.89
assert E["spec"] == 0.9
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
CM = w.cmatrix("cm", 36, 4, 12, 148, pos="ספאם", neg="תקין", hidden=True)
CMH = w.cmatrix("cz", 36, 4, 12, 148, pos="ספאם", neg="תקין", size=26)
FOLDS = w.folds("kf", 4, 200)
RAST = st.raster("xr", "images/exams/25A-A-Q14.png", 900, (596, 143),
                 rings=[("tp", 273, 77, 24), ("fn", 478, 77, 24), ("fp", 273, 108, 24), ("tn", 478, 108, 24)])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד למדוד כמה טוב מודל סיווג."),
    P("נבנה מטריצת בלבול, ונחשב ממנה ארבעה מדדים: דיוק, Precision, Recall ו-F1."),
    P("נראה איך מחלקים נתונים ב-K-Fold, ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">M06 · מודלים והערכה</div><h1>מטריצת בלבול, Precision, Recall ו-F1</h1>'
         '<p>לחשב דיוק, Precision, Recall ו-F1 ממטריצת בלבול, ולחשב גדלי fold ב-K-Fold.</p>', layout="title")

matrix = Scene("matrix", "מטריצת הבלבול", [
    P("מסנן ספאם בדק מאתיים הודעות. ארבעים מהן באמת ספאם."),
    P("במודל בינארי בוחרים מחלקה אחת כ**חיובית**. כאן החיובי הוא ספאם.", do=show("cm")),
    P("המטריצה סופרת ארבעה מצבים: השורה היא האמת, והעמודה היא מה שהמודל חזה."),
    P("36 הודעות ספאם נתפסו כספאם. זו פגיעה: חיובי אמיתי.", do=show("cm-h-tp", "c-tp"),
      say="שלושים ושש הודעות ספאם נתפסו כספאם. זו פגיעה: חיובי אמיתי."),
    P("4 הודעות ספאם עברו כאילו הן תקינות. זו החמצה: שלילי כוזב.", do=hide("cm-h-tp") + show("cm-h-fn", "c-fn"),
      say="ארבע הודעות ספאם עברו כאילו הן תקינות. זו החמצה: שלילי כוזב."),
    P("12 הודעות תקינות סומנו כספאם. זו אזעקת שווא: חיובי כוזב.", do=hide("cm-h-fn") + show("cm-h-fp", "c-fp"),
      say="שתים עשרה הודעות תקינות סומנו כספאם. זו אזעקת שווא: חיובי כוזב."),
    P("ו-148 הודעות תקינות עברו כתקינות: שלילי אמיתי.", do=hide("cm-h-fp") + show("cm-h-tn"),
      say="ומאה ארבעים ושמונה הודעות תקינות עברו כתקינות: שלילי אמיתי.", hold=0.3),
    P("באותיות האנגליות: האות השנייה אומרת מה המודל חזה, והאות הראשונה אומרת אם הוא צדק.", do=hide("cm-h-tn") + show("c-rule"), hold=0.4),
], stage=f'<div class="ml-col">{CM}'
         '<div class="ml-note">200 הודעות · 40 מהן ספאם</div></div>',
   panel=st.card("c-tp", "ex", "$TP$: ספאם שנתפס, פגיעה")
         + st.card("c-fn", "ex", "$FN$: ספאם שהוחמץ")
         + st.card("c-fp", "ex", "$FP$: תקינה שסומנה כספאם")
         + st.card("c-rule", "rule", "🔑 $P$ / $N$ = מה המודל <b>חזה</b>. $T$ / $F$ = האם הוא <b>צדק</b>"))

metrics = Scene("metrics", "ארבעה מדדים", [
    P("עכשיו המדדים. **Precision** שואל: מכל מה שהמודל סימן כספאם, כמה באמת ספאם?", do=show("cz-h-tp", "cz-h-fp")),
    P("המודל סימן 48 הודעות, ו-36 מהן ספאם. 36 חלקי 48 זה 0.75.", do=show("e-p"),
      say="המודל סימן ארבעים ושמונה הודעות, ושלושים ושש מהן ספאם. שלושים ושש חלקי ארבעים ושמונה זה אפס נקודה שבעים וחמש."),
    P("**Recall** שואל: מכל הספאם שיש באמת, כמה המודל מצא?", do=hide("cz-h-fp") + show("cz-h-fn")),
    P("יש 40 הודעות ספאם, והמודל מצא 36. 36 חלקי 40 זה 0.9.", do=show("e-r"),
      say="יש ארבעים הודעות ספאם, והמודל מצא שלושים ושש. שלושים ושש חלקי ארבעים זה אפס נקודה תשע.", hold=0.3),
    P("שימו לב: המונה זהה, אבל המכנה שונה. ב-Precision מוסיפים את אזעקות השווא, וב-Recall את ההחמצות.",
      do=hide("cz-h-tp", "cz-h-fn") + show("m-k1")),
    P("**דיוק**, Accuracy: כמה חיזויים נכונים מתוך הכול. 36 ועוד 148 זה 184, מתוך 200: 0.92.",
      do=show("cz-h-tp", "cz-h-tn", "e-a"),
      say="דיוק, אַקְיוּרַסִי: כמה חיזויים נכונים מתוך הכול. שלושים ושש ועוד מאה ארבעים ושמונה זה מאה שמונים וארבע, מתוך מאתיים: אפס נקודה תשעים ושתיים."),
    P("ו-**F1** משלב את Precision ו-Recall: פעמיים המכפלה שלהם, חלקי הסכום שלהם.", do=hide("cz-h-tp", "cz-h-tn") + show("e-f")),
    P("פעמיים 0.75 כפול 0.9 זה 1.35. חלקי 1.65 יוצא בערך 0.82.",
      say="פעמיים אפס נקודה שבעים וחמש כפול אפס נקודה תשע זה אחת נקודה שלושים וחמש. חלקי אחת נקודה שישים וחמש יוצא בערך אפס נקודה שמונים ושתיים.", hold=0.3),
    P("זה ממוצע **הרמוני**: הוא קצת מתחת לממוצע הרגיל, 0.825, ונמשך אל המדד החלש.", do=show("m-k2"),
      say="זה ממוצע הרמוני: הוא קצת מתחת לממוצע הרגיל, אפס נקודה שמונה מאות עשרים וחמש, ונמשך אל המדד החלש.", hold=0.4),
], stage=f'<div class="ml-col">{CMH}'
         + w.eq("e-p", "$\\text{Precision} = \\dfrac{TP}{TP+FP} = \\dfrac{36}{48} = 0.75$", 34)
         + w.eq("e-r", "$\\text{Recall} = \\dfrac{TP}{TP+FN} = \\dfrac{36}{40} = 0.9$", 34)
         + w.eq("e-a", "$\\text{Accuracy} = \\dfrac{36+148}{200} = 0.92$", 34) + "</div>",
   panel=st.card("e-f", "ex", "$F_1 = \\dfrac{2 \\cdot 0.75 \\cdot 0.9}{0.75 + 0.9} = \\dfrac{1.35}{1.65} \\approx 0.82$")
         + st.card("m-k1", "rule", "🔑 Precision: חלקי <b>כל מה שסומן</b> חיובי. Recall: חלקי <b>כל החיוביים האמיתיים</b>")
         + st.card("m-k2", "rule", "🔑 $F_1 = \\dfrac{2PR}{P+R}$: ממוצע הרמוני, לא חשבוני"))

trap = Scene("trap", "מלכודת הדיוק", [
    P("למה צריך יותר ממדד אחד? נסתכל על מודל עצלן, שאומר על כל הודעה ״תקינה״.", do=show("cl")),
    P("הוא צודק על כל 160 ההודעות התקינות, ולכן הדיוק שלו 0.8. נשמע לא רע.", do=show("cl-h-tn", "t-a"),
      say="הוא צודק על כל מאה שישים ההודעות התקינות, ולכן הדיוק שלו אפס נקודה שמונה. נשמע לא רע."),
    P("אבל הוא לא תפס אף ספאם: ה-Recall שלו אפס.", do=hide("cl-h-tn") + show("cl-h-fn", "t-r")),
    P("כשמחלקה אחת נדירה, דיוק גבוה יכול להסתיר מודל חסר תועלת.", do=show("t-k"), hold=0.3),
    P("ואיזה מדד לבדוק? אם אזעקת שווא יקרה, כמו מייל חשוב שנזרק, מסתכלים על Precision.", do=show("t-1")),
    P("אם החמצה יקרה, כמו הודעת התחזות שהגיעה למשתמש, מסתכלים על Recall.", do=show("t-2"), hold=0.4),
], stage='<div class="ml-col">' + w.cmatrix("cl", 0, 40, 0, 160, pos="ספאם", neg="תקין", size=30, hidden=True)
         + w.chip("t-a", "Accuracy = 160 ÷ 200 = 0.8", "warn") + w.chip("t-r", "Recall = 0 ÷ 40 = 0", "bad") + "</div>",
   panel=st.card("t-k", "trap", "⚠️ מחלקה נדירה: דיוק גבוה לא אומר שהמודל טוב")
         + st.card("t-1", "ex", "אזעקת שווא ($FP$) יקרה ← <b>Precision</b>")
         + st.card("t-2", "ex", "החמצה ($FN$) יקרה ← <b>Recall</b>"))

kfold = Scene("kfold", "K-Fold", [
    P("ועכשיו, על מה מודדים? אם בודקים על חלק אחד בלבד של הנתונים, התוצאה תלויה במזל."),
    P("ב-K-Fold מחלקים את הנתונים ל-K חלקים שווים, שנקראים folds.", do=show("kf-r0"),
      say="בקֵיי פוֹלְד מחלקים את הנתונים לקֵיי חלקים שווים, שנקראים פוֹלְדְס."),
    P("נניח מאתיים דוגמאות ו-K שווה ארבע. כל חלק מכיל חמישים דוגמאות.", do=show("k-1"),
      say="נניח מאתיים דוגמאות, וקֵיי שווה ארבע. כל חלק מכיל חמישים דוגמאות."),
    P("בכל סבב חלק אחד משמש לתיקוף, ושלושת האחרים לאימון: מאה חמישים דוגמאות.", do=show("k-2")),
    P("בסבב הבא, חלק אחר עובר לתיקוף.", do=show("kf-r1")),
    P("וכך ארבעה סבבים, עד שכל דוגמה שימשה לתיקוף בדיוק פעם אחת.", do=show("kf-r2", "kf-r3", "k-3")),
    P("הציון הסופי הוא הממוצע של ארבעת הסבבים.", hold=0.4),
], stage=f'<div class="ml-col">{FOLDS}<div class="ml-note">200 דוגמאות · K = 4</div></div>',
   panel=st.card("k-1", "ex", "גודל fold: $200 \\div 4 = 50$")
         + st.card("k-2", "ex", "אימון בכל סבב: $3 \\cdot 50 = 150$")
         + st.card("k-3", "rule", "🔑 תיקוף = fold אחד. אימון = $K-1$ folds"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: נתונה מטריצת הבלבול הזו. מהו ה-Recall, בעיגול לשתי ספרות?"),
    P("קודם מזהים את התאים. בשורת החיוביים האמיתיים: 85 נתפסו ו-15 הוחמצו.", do=show("xr-ring-tp", "xr-ring-fn"),
      say="קודם מזהים את התאים. בשורת החיוביים האמיתיים: שמונים וחמש נתפסו, וחמש עשרה הוחמצו."),
    P("Recall הוא 85 חלקי (85 ועוד 15). כלומר 85 חלקי 100: 0.85.", do=show("x-r", "q-ok-0"),
      say="רִיקוֹל הוא שמונים וחמש חלקי, בסוגריים, שמונים וחמש ועוד חמש עשרה. כלומר שמונים וחמש חלקי מאה: אפס נקודה שמונים וחמש.", hold=0.3),
    P("ושאר התשובות? כל אחת מהן היא מדד אחר של אותה מטריצה.", do=hide("xr-ring-fn") + show("xr-ring-fp")),
    P("0.89 הוא ה-Precision: 85 חלקי 95, כי מוסיפים את 10 אזעקות השווא.", do=show("q-x-2", "q-n-2"),
      say="אפס נקודה שמונים ותשע הוא הפְּרֶסִיזְ'ן: שמונים וחמש חלקי תשעים וחמש, כי מוסיפים את עשר אזעקות השווא."),
    P("0.88 הוא הדיוק: 175 נכונים מתוך 200 זה 0.875, ובעיגול 0.88.", do=hide("xr-ring-fp") + show("xr-ring-tn", "q-x-1", "q-n-1"),
      say="אפס נקודה שמונים ושמונה הוא הדיוק: מאה שבעים וחמישה נכונים מתוך מאתיים זה אפס נקודה שמונה מאות שבעים וחמש, ובעיגול אפס נקודה שמונים ושמונה."),
    P("ו-0.9 הוא 90 חלקי 100: ה-Recall של המחלקה **השלילית**, לא של החיובית.", do=show("q-x-3", "q-n-3"),
      say="ואפס נקודה תשע הוא תשעים חלקי מאה: הרִיקוֹל של המחלקה השלילית, לא של החיובית."),
    P("המלכודת: כל המספרים נראים סבירים. הכלל: Recall הולך לפי **השורה** של החיוביים האמיתיים.", do=show("x-t"), hold=0.6),
], stage=f'<div class="ml-col">{RAST}'
         + w.eq("x-r", "$\\text{Recall} = \\dfrac{85}{85+15} = 0.85$", 38)
         + st.card("x-t", "trap", "⚠️ Recall = השורה של החיוביים <b>האמיתיים</b>, לא העמודה") + "</div>",
   panel=w.stem(Q["id"], "בהינתן מטריצת הבלבול, מהו ערך ה-Recall (עיגול לשתי ספרות)?")
         + st.options("q", OPTS, notes={1: "Accuracy", 2: "Precision", 3: "Recall של השליליים"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: השורה היא האמת, העמודה היא החיזוי.", do=show("r-1")),
    P("Precision: מכל מה שסומן חיובי, כמה נכון. Recall: מכל החיוביים האמיתיים, כמה נמצאו.", do=show("r-2")),
    P("דיוק הוא הנכונים מתוך הכול, ו-F1 הוא הממוצע ההרמוני של Precision ו-Recall.", do=show("r-3")),
    P("וב-K-Fold, חלק אחד לתיקוף והשאר לאימון, בכל סבב. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ml-col">' + w.cmatrix("cr", "TP", "FN", "FP", "TN", values=False)
         + w.eq("r-eq", "$F_1 = \\dfrac{2PR}{P+R}$", 44, hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 שורה = אמת, עמודה = חיזוי")
         + st.card("r-2", "rule", "🔑 $P = \\dfrac{TP}{TP+FP}$ · $R = \\dfrac{TP}{TP+FN}$")
         + st.card("r-3", "rule", "🔑 $\\text{Acc} = \\dfrac{TP+TN}{n}$")
         + st.card("r-4", "trap", "⚠️ K-Fold: תיקוף = fold אחד, אימון = $K-1$"))

VIDEO = Video("M06", "ml", "מטריצת בלבול, Precision, Recall ו-F1", [title, matrix, metrics, trap, kfold, exam, recap],
              bank={"25A-A-Q14": 0})

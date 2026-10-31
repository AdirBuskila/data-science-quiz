# -*- coding: utf-8 -*-
"""E05 · היסטוגרמה ו-box plot — video script (build: tools/video/vid.py E05).

Source: courses/eda/E05.js (lesson + goal: read a histogram (what a bar's height is, what changing the number of bins
does) and a box plot (box, whiskers, outlier points)).
Exam anchor: 26B-A-Q13 (fewer bins -> larger bin values). No guided quiz uses it. Not used on purpose: every E05 quiz
item (100 values 4 -> 20 bins, the 12 values 3..41 in bins of 10, Q1 = 8 / Q3 = 14 with 5, 22, 24, 40 and whis 5,
120 students in 8 bins), the boss item 25A-A-Q2, and the bank twins of the anchor (24A-A-Q15, 24B-B-Q15: more bins
-> smaller values; the worked example shows that direction on its own data, the exam scene the other one).
Worked examples: 24 waiting times in 6 bins of 10 minutes, then 12 bins of 5 (np.histogram); a box plot of 15 values
(Q1 = 18, median 23, Q3 = 28, fences 3 / 43, whiskers to 12 and 31, outlier 52). Exam scene: the same 24 values in 3
bins of 20. Every count and every box-plot number is computed (np.histogram, the checker's quartiles()) and asserted.
"""
import numpy as np

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_eda as w

# ---------------------------------------------------------------- data (verified)
T = [4, 8, 11, 13, 15, 17, 19, 21, 22, 23, 24, 25, 26, 27, 29, 31, 33, 35, 36, 38, 42, 45, 48, 55]
assert len(T) == 24
E6, E12, E3 = list(range(0, 61, 10)), list(range(0, 61, 5)), list(range(0, 61, 20))
H6, c6 = w.hist("h6", T, E6, w=860, h=420, ymax=10, yticks=[0, 2, 4, 6, 8, 10])
H12, c12 = w.hist("h12", T, E12, w=860, h=420, ymax=10, yticks=[0, 2, 4, 6, 8, 10], kind="b")
H3, c3 = w.hist("h3", T, E3, w=860, h=420, ymax=14, yticks=[0, 2, 4, 6, 8, 10, 12, 14], kind="b")
assert c6 == [2, 5, 8, 5, 3, 1] and c12 == [1, 1, 2, 3, 4, 4, 2, 3, 1, 2, 0, 1] and c3 == [7, 13, 4]
assert sum(c6) == sum(c12) == sum(c3) == 24
assert all(c6[i] == c12[2 * i] + c12[2 * i + 1] for i in range(6))          # each wide bar = two narrow bars
assert all(c3[i] == c6[2 * i] + c6[2 * i + 1] for i in range(3))
assert max(c12) == 4 < max(c6) == 8 < max(c3) == 13

B = [24, 15, 31, 18, 52, 22, 27, 12, 25, 20, 30, 17, 23, 28, 21]
BX, S = w.boxplot("bx", B, 0, 60, [0, 10, 20, 30, 40, 50, 60], w=900, h=330)
assert (S["q1"], S["median"], S["q3"], S["iqr"]) == (18, 23, 28, 10)
assert (S["flo"], S["fhi"]) == (3, 43) and (S["wl"], S["wr"]) == (12, 31) and S["out"] == [52]
assert sorted(B)[:7] == [12, 15, 17, 18, 20, 21, 22] and sorted(B)[8:] == [24, 25, 27, 28, 30, 31, 52]

# exam 26B-A-Q13
Q = BANK["26B-A-Q13"]
assert Q["correctIndex"] == 0 and "הקטנת מספר התאים" in Q["question"]
assert "גדולים יותר" in Q["options"][0] and "קטנים יותר" in Q["options"][3]
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נקרא שני גרפים חשובים: היסטוגרמה ו-box plot."),
    P("נבין מה גובה של עמודה, מה קורה כשמשנים את מספר התאים, ואיך בונים קופסה ושפמים."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">E05 · סטטיסטיקה וגרפים</div><h1>היסטוגרמה ו-box plot</h1>'
         '<p>לקרוא היסטוגרמה (מה גובה העמודה ומה קורה כשמשנים את מספר התאים) ו-box plot (קופסה, שפמים ונקודות חריגות).</p>',
   layout="title")

hist = Scene("hist", "היסטוגרמה", [
    P("היסטוגרמה מציגה התפלגות של משתנה **רציף**. כאן: זמן המתנה בדקות, של 24 לקוחות.", do=show("g-c0")),
    P("מחלקים את הציר לטווחים שווים, שנקראים **תאים**. כאן שישה תאים, כל אחד ברוחב עשר דקות.", do=show("g-h6")),
    P("גובה כל עמודה הוא **כמה נתונים נפלו בתא**. למשל, בין 20 ל-30 דקות יש 8 לקוחות.", do=show("g-c1")),
    P("ואם נחבר את כל העמודות: 2, 5, 8, 5, 3 ו-1. יוצא 24, כל הנתונים.", do=show("g-c2")),
    P("וזה תמיד נכון: כל נתון נופל בדיוק בתא אחד, ולכן סכום העמודות שווה למספר הנתונים.", hold=0.3),
    P("עכשיו נכפיל את מספר התאים לשנים עשר, כל אחד ברוחב חמש דקות.", do=hide("g-h6") + show("g-h12")),
    P("כל תא ישן התפצל לשניים, והנתונים שלו התחלקו ביניהם. למשל, ה-8 התפצל ל-4 ו-4.", do=show("g-c3")),
    P("לכן העמודות **נמוכות** יותר: הגבוהה ביותר ירדה מ-8 ל-4. והסכום? עדיין 24.", do=show("g-c4"), hold=0.4),
], stage=f'<div class="swap" style="--swap-h:440px"><div id="g-h6" class="h">{H6}</div><div id="g-h12" class="h">{H12}</div></div>'
         + '<div class="ed-note">זמן המתנה (דקות), 24 לקוחות</div>',
   panel=st.card("g-c0", "plain", "ציר $x$: טווחי ערכים · ציר $y$: כמה נתונים בכל תא")
         + st.card("g-c1", "rule", "🔑 גובה עמודה = <b>מספר הנתונים בתא</b>")
         + st.card("g-c2", "ex", "$2+5+8+5+3+1 = 24 = n$")
         + st.card("g-c3", "ex", "6 תאים ← 12 תאים: $8 = 4 + 4$")
         + st.card("g-c4", "rule", "🔑 יותר תאים ← עמודות <b>נמוכות</b> יותר, הסכום תמיד $n$"))

box = Scene("box", "box plot", [
    P("עכשיו box plot. הנה חמישה עשר ערכים על ציר.", do=show("b-pl")),
    P("מחשבים רבעונים בשיטת הקורס: החציון הוא 23, הרבעון הראשון 18 והשלישי 28.", do=show("bx-lq1", "bx-lmd", "bx-lq3")),
    P("**הקופסה** נמתחת מהרבעון הראשון עד השלישי, והקו שבתוכה הוא החציון.", do=show("bx-box", "bx-med")),
    P("בתוך הקופסה נמצא חצי מהנתונים, ורוחבה הוא הטווח הבין רבעוני: 10.", do=show("b-c1")),
    P("עכשיו הגדרות, כמו ברמה הקודמת: 18 פחות 15 זה 3, ו-28 ועוד 15 זה 43.", do=show("bx-fl", "bx-fh", "b-c2")),
    P("**השפמים** יוצאים מהקופסה עד הערך הרחוק ביותר שעדיין בתוך הגדרות: 12 משמאל, ו-31 מימין.",
      do=show("bx-wl", "bx-wr")),
    P("והערך 52? הוא מעבר לגדר העליונה, ולכן הוא מצויר כ**נקודה** נפרדת: ערך חריג.", do=show("bx-out", "b-c3")),
    P("כך box plot מראה בתמונה אחת את המרכז, את הפיזור, ואת החריגים.", hold=0.3),
    P("ומלכודת: היסטוגרמה מתאימה למשתנה רציף. משתנה בדיד עם מעט ערכים, כמו יחידות בגרות, מציגים בגרף עמודות.",
      do=show("b-trap"), hold=0.4),
], stage=f'<div class="ed-col"><div id="b-pl" class="h">{BX}</div></div>',
   panel=st.card("b-c1", "ex", "קופסה: $Q_1 = 18$ עד $Q_3 = 28$, חציון 23")
         + st.card("b-c2", "ex", "גדרות: $18 - 15 = 3$, $\\ 28 + 15 = 43$")
         + st.card("b-c3", "rule", "🔑 שפם עד הנתון האחרון <b>בתוך</b> הגדר; מעבר לה: נקודה חריגה")
         + st.card("b-trap", "trap", "⚠️ רציף: היסטוגרמה · בדיד עם מעט ערכים: גרף עמודות"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: ״ערך תא״ הוא כמות הדגימות בתא. איך עלולה להשפיע **הקטנת** מספר התאים על ערכי התאים?"),
    P("ראינו את הכיוון ההפוך. עכשיו נחזור לשישה התאים שלנו, ונקטין לשלושה, ברוחב עשרים דקות.", do=show("x-h6")),
    P("כל תא רחב הוא איחוד של שני תאים צרים, ולכן הערך שלו הוא הסכום שלהם.", do=hide("x-h6") + show("x-h3")),
    P("2 ועוד 5 זה 7. 8 ועוד 5 זה 13. ו-3 ועוד 1 זה 4. העמודה הגבוהה עלתה מ-8 ל-13.", do=show("x-eq")),
    P("לכן ערכי התאים גדלים, וזו התשובה.", do=show("q-ok-0")),
    P("והתשובה ההפוכה, שהם קטנים, היא בדיוק הכיוון של **הגדלת** מספר התאים.", do=show("q-x-3", "q-n-3")),
    P("השונות של הערכים בתוך כל תא לא נשאלה: ״ערך תא״ הוגדר כאן כמספר הדגימות.", do=show("q-x-1", "q-n-1")),
    P("ו״בלתי תלויים יותר״ לא אומר כלום על ספירה: מספר התאים לא משנה את התלות בין הנתונים.", do=show("q-x-2", "q-n-2"),
      hold=0.6),
], stage=f'<div class="swap" style="--swap-h:440px"><div id="x-h6" class="h">{H6.replace(chr(34) + "h6", chr(34) + "xh6")}</div>'
         f'<div id="x-h3" class="h">{H3}</div></div>'
         + w.eq("x-eq", "$2+5 = 7,\\quad 8+5 = 13,\\quad 3+1 = 4$", 36),
   panel='<div class="ed-small">' + w.stem(Q["id"], "״ערך תא״ (bin) = כמות הדגימות בו. איך עלולה להשפיע הקטנת מספר התאים על ״ערך התא״?")
         + st.options("q", OPTS, notes={1: "לא נשאל", 2: "לא קשור", 3: "הפוך"}) + "</div>")

recap = Scene("recap", "סיכום", [
    P("לסיכום: בהיסטוגרמה, גובה עמודה הוא מספר הנתונים בתא, וסכום העמודות הוא מספר הנתונים.",
      do=show("r-1", "rb-box", "rb-med", "rb-wl", "rb-wr", "rb-out", "rb-lq1", "rb-lmd", "rb-lq3")),
    P("יותר תאים: עמודות נמוכות יותר. פחות תאים: עמודות גבוהות יותר.", do=show("r-2")),
    P("ב-box plot, הקופסה היא מהרבעון הראשון עד השלישי, עם החציון באמצע.", do=show("r-3")),
    P("השפמים עד הנתון האחרון בתוך הגדרות, ומעבר להן נקודות חריגות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="ed-col">{w.boxplot("rb", B, 0, 60, [0, 10, 20, 30, 40, 50, 60], w=900, h=330)[0]}</div>',
   panel=st.card("r-1", "rule", "🔑 גובה = ספירה, סכום = $n$")
         + st.card("r-2", "rule", "🔑 יותר תאים ← נמוכות · פחות תאים ← גבוהות")
         + st.card("r-3", "rule", "🔑 קופסה: $Q_1$ עד $Q_3$, קו = חציון")
         + st.card("r-4", "trap", "⚠️ שפם עד נתון <b>בתוך</b> הגדר"))

VIDEO = Video("E05", "eda", "היסטוגרמה ו-box plot", [title, hist, box, exam, recap], bank={"26B-A-Q13": 0})

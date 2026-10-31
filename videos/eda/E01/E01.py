# -*- coding: utf-8 -*-
"""E01 · ממוצע, חציון ושכיח — video script (build: tools/video/vid.py E01).

Source: courses/eda/E01.js (lesson + goal: compute the three measures of center, and pick one when there is an
extreme value or a skewed distribution).
Exam anchor: 24A-B-Q15 (which measure of center for a highly skewed variable such as monthly salary: the median).
No guided quiz uses it (the lesson only cites it). Not used on purpose: every E01 quiz item (12,7,9,7,15,10 /
3,9,6,12,10 / the salaries 8..70 -> 13 / 1,2,2,3,3,3,4,20 / 4,6,6,9,4,6,9,3), the lesson's 3,5,5,7,100 and 9,1,5,
and the boss items 25A-A-Q22 (skew -> mean > median, asked there) and its twins. The worked examples use new data:
commute times 14,9,22,9,17,12,50 (then without 50), exam scores with a low tail, and salaries for the exam scene.
Every mean / median / mode below is computed with numpy / statistics and asserted.
"""
import statistics

import numpy as np

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_eda as w

# ---------------------------------------------------------------- data (verified)
D = [14, 9, 22, 9, 17, 12, 50]                      # minutes to work, 7 people
S = sorted(D)
assert S == [9, 9, 12, 14, 17, 22, 50]
assert sum(D) == 133 and np.mean(D) == 19
assert np.median(D) == 14 and S[3] == 14 and D[3] == 9
assert statistics.multimode(D) == [9]

D6 = [v for v in D if v != 50]                       # the extreme value removed
S6 = sorted(D6)
assert S6 == [9, 9, 12, 14, 17, 22] and np.median(D6) == 13 == (12 + 14) / 2
assert sum(D6) == 83 and round(np.mean(D6), 2) == 13.83
assert round(np.mean(D) - np.mean(D6), 1) == 5.2 and np.median(D) - np.median(D6) == 1

L = [95, 88, 91, 40, 85, 93, 90]                     # exam scores with one very low score: tail to the left
assert sorted(L) == [40, 85, 88, 90, 91, 93, 95]
assert np.median(L) == 90 and sum(L) == 582 and round(np.mean(L), 1) == 83.1
assert np.mean(L) < np.median(L) and np.mean(D) > np.median(D)
from scipy import stats as sps
assert sps.skew(D) > 0 and sps.skew(L) < 0

SAL = [7, 8, 8, 9, 9, 10, 11, 12, 14, 35]            # monthly salaries (thousands), exam scene illustration
assert np.median(SAL) == 9.5 and np.mean(SAL) == 12.3 and sps.skew(SAL) > 0
assert sum(v > 12.3 for v in SAL) == 2               # only 2 of 10 earn more than the mean
assert statistics.multimode(SAL) == [8, 9]           # two modes: the mode does not even give one number here

# exam 24A-B-Q15
Q = BANK["24A-B-Q15"]
assert Q["correctIndex"] == 0 and Q["options"] == ["median", "mean", "mode", "quartile"]
OPTS = [(i, o) for i, o in enumerate(Q["options"])]

# ---------------------------------------------------------------- figures
ST1 = w.strip("s1", D)
ST2 = w.strip("s2", S, hidden=True)
ST3 = w.strip("s3", S6, brackets=[("mid", 2, 3, "שני האמצעיים")])

N1 = w.NumLine("n1", 0, 55, [0, 10, 20, 30, 40, 50], w=920, h=250)
N1.dots("n1-d", D, kind="a", hidden=False)
N1.mark("n1-md", 14, "חציון 14", kind="b", lift=30)
N1.mark("n1-mn", 19, "ממוצע 19", kind="a")
N1.band("n1-tail", 25, 53, kind="b", label="זנב ימינה →")

N2 = w.NumLine("n2", 35, 100, [40, 50, 60, 70, 80, 90, 100], w=920, h=250, dot=9)
N2.dots("n2-d", L, kind="b", hidden=False)
N2.mark("n2-md", 90, "חציון 90", kind="b", lift=30)
N2.mark("n2-mn", float(np.mean(L)), "ממוצע 83.1", kind="a")
N2.band("n2-tail", 37, 80, kind="b", label="← זנב שמאלה")

N3 = w.NumLine("n3", 5, 37, [5, 10, 15, 20, 25, 30, 35], w=920, h=250)
N3.dots("n3-d", SAL, kind="a", hidden=False)
N3.mark("n3-md", 9.5, "חציון 9.5", kind="b", lift=30)
N3.mark("n3-mn", 12.3, "ממוצע 12.3", kind="a")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לתאר עמודה שלמה של נתונים במספר אחד."),
    P("נחשב ממוצע, חציון ושכיח, ונראה מה קורה להם כשיש ערך קיצוני."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">E01 · סטטיסטיקה וגרפים</div><h1>ממוצע, חציון ושכיח</h1>'
         '<p>לחשב את שלושת מדדי המרכז, ולדעת איזה מהם לבחור כשיש ערך קיצוני או התפלגות מוטה.</p>', layout="title")

idea = Scene("idea", "שלושה מדדי מרכז", [
    P("מדד מרכז הוא מספר אחד שאומר איפה הנתונים נמצאים בערך."),
    P("יש שלושה מדדים כאלה, וכל אחד עונה על שאלה אחרת.", hold=0.2),
    P("**ממוצע**: סכום כל הערכים, חלקי מספר הערכים.", do=show("c-mean")),
    P("**חציון**: ממיינים מהקטן לגדול, ולוקחים את הערך שבאמצע.", do=show("c-med")),
    P("**שכיח**: הערך שמופיע הכי הרבה פעמים.", do=show("c-mode"), hold=0.3),
    P("נחשב את שלושתם על דוגמה אחת: כמה דקות לוקח לשבעה אנשים להגיע לעבודה.", do=show("s1")),
], stage=f'<div class="ed-col"><div id="s1" class="h">{ST1}</div>'
         '<div class="ed-note">דקות נסיעה לעבודה, 7 אנשים</div></div>',
   panel=st.card("c-mean", "rule", "🔑 <b>ממוצע</b> = סכום ÷ מספר הערכים")
         + st.card("c-med", "rule", "🔑 <b>חציון</b> = הערך האמצעי <b>אחרי מיון</b>")
         + st.card("c-mode", "rule", "🔑 <b>שכיח</b> = הערך שחוזר הכי הרבה"))

mean = Scene("mean", "ממוצע, חציון ושכיח", [
    P("נתחיל בממוצע. מחברים את כל שבעת הערכים, ומקבלים 133.", do=show("m-sum")),
    P("מחלקים בשבע, ומקבלים ממוצע 19.", do=show("m-mean")),
    P("עכשיו החציון. הצעד הראשון הוא תמיד **מיון**.", hold=0.2),
    P("הכי קטנים: 9, 9, ואחר כך 12.", do=show("s2-c0", "s2-c1", "s2-c2")),
    P("אחריהם 14, 17, 22, ובסוף 50.", do=show("s2-c3", "s2-c4", "s2-c5", "s2-c6")),
    P("יש שבעה ערכים, מספר אי זוגי, ולכן יש ערך אמצעי אחד: הרביעי.", do=show("s2-k3")),
    P("שלושה ערכים משמאלו ושלושה מימינו. החציון הוא 14.", do=show("m-med")),
    P("שימו לב: בסדר המקורי, הערך הרביעי הוא 9. בלי מיון היינו טועים.", do=show("s1-k3", "m-trap")),
    P("ולבסוף השכיח: 9 מופיע פעמיים, וכל השאר פעם אחת. השכיח הוא 9.", do=hide("s1-k3") + show("s2-k0", "s2-k1", "m-mode"),
      hold=0.4),
    P("שלושה מדדים, שלוש תשובות שונות: 19, 14 ו-9.", do=hide("s2-k3")),
], stage=f'<div class="ed-col">{ST1}<div class="ed-note">אחרי מיון:</div>{ST2}'
         + w.eq("m-sum", "$14+9+22+9+17+12+50=133$", 38)
         + w.eq("m-mean", "$133 \\div 7 = 19$", 40) + "</div>",
   panel=st.card("m-med", "ex", "חציון = <b>14</b> (הערך הרביעי מתוך 7)")
         + st.card("m-trap", "trap", "⚠️ קודם ממיינים! הרביעי <b>בסדר המקורי</b> הוא 9")
         + st.card("m-mode", "ex", "שכיח = <b>9</b> (מופיע פעמיים)"))

even = Scene("even", "מספר זוגי וערך קיצוני", [
    P("ומה קורה כשמספר הערכים זוגי? נוציא את הנוסע של 50 הדקות.", do=show("e-st")),
    P("נשארו שישה ערכים ממוינים. אין ערך אמצעי אחד, יש **שניים**: השלישי והרביעי.", do=show("s3-k2", "s3-k3", "s3-br-mid")),
    P("החציון הוא הממוצע שלהם: 12 ועוד 14, חלקי שתיים. כלומר 13.", do=show("e-med")),
    P("והממוצע? הסכום ירד ל-83, ו-83 חלקי שש זה בערך 13.8.", do=show("e-mean"),
      say="והממוצע? הסכום ירד לשמונים ושלוש, ושמונים ושלוש חלקי שש זה בערך שלוש עשרה נקודה שמונה."),
    P("עכשיו נשווה. הוצאנו ערך אחד, והממוצע צנח מ-19 לכ-13.8.", do=show("e-c1"),
      say="עכשיו נשווה. הוצאנו ערך אחד, והממוצע צנח מתשע עשרה לכשלוש עשרה נקודה שמונה."),
    P("החציון כמעט לא זז: מ-14 ל-13.", do=show("e-c2"), hold=0.3),
    P("זה הכלל החשוב: הממוצע **רגיש** לערכים קיצוניים, והחציון **עמיד** להם.", do=show("e-rule")),
    P("למה? הממוצע משתמש בגודל של כל ערך. החציון רק בסדר שלהם, ולא משנה כמה רחוק הקיצוני.", hold=0.4),
], stage=f'<div class="ed-col"><div id="e-st" class="h">{ST3}</div>'
         + w.eq("e-med", "$\\text{median} = (12+14) \\div 2 = 13$", 38)
         + w.eq("e-mean", "$\\text{mean} = 83 \\div 6 \\approx 13.83$", 38) + "</div>",
   panel=st.card("e-c1", "ex", "ממוצע: 19 ← 13.83 (ירידה של יותר מ-5)")
         + st.card("e-c2", "ex", "חציון: 14 ← 13 (ירידה של 1)")
         + st.card("e-rule", "rule", "🔑 ממוצע <b>רגיש</b> לקיצוניים, חציון <b>עמיד</b> להם"))

skew = Scene("skew", "הטיה", [
    P("נחזור לשבעת הנוסעים, הפעם על ציר. רוב הערכים צפופים משמאל.", do=show("k-n1")),
    P("והערך 50 יושב לבד, רחוק ימינה. זה **זנב ארוך ימינה**: הטיה חיובית.", do=show("n1-tail")),
    P("החציון 14 נמצא בלב הקבוצה.", do=show("n1-md")),
    P("הממוצע 19 נמשך אחרי הזנב, ימינה. בזנב ימינה, הממוצע גדול מהחציון.", do=show("n1-mn", "k-r1"), hold=0.3),
    P("עכשיו ציונים במבחן: רוב הכיתה בין 85 ל-95, ותלמיד אחד קיבל 40.", do=show("k-n2")),
    P("כאן הזנב הארוך **שמאלה**: הטיה שלילית.", do=show("n2-tail")),
    P("החציון 90. הממוצע בערך 83, כי הציון 40 מושך אותו שמאלה.", do=show("n2-md", "n2-mn"),
      say="החציון תשעים. הממוצע בערך שמונים ושלוש, כי הציון ארבעים מושך אותו שמאלה."),
    P("בזנב שמאלה הממוצע קטן מהחציון. ובהתפלגות סימטרית, הם בערך שווים.", do=show("k-r2"), hold=0.4),
], stage=f'<div class="ed-col"><div id="k-n1" class="h">{N1.svg()}</div><div id="k-n2" class="h">{N2.svg()}</div></div>',
   panel=st.card("k-r1", "rule", "🔑 זנב ימינה (הטיה חיובית): <b>ממוצע &gt; חציון</b>")
         + st.card("k-r2", "rule", "🔑 זנב שמאלה (הטיה שלילית): <b>ממוצע &lt; חציון</b>"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: באיזה מדד מודדים את המרכז של התפלגות עם הטיה גבוהה, כמו שכר חודשי?"),
    P("שכר הוא הדוגמה הקלאסית: רוב האנשים מרוויחים סכום דומה, ומעטים מרוויחים הרבה מאוד.", do=show("x-n3")),
    P("כאן עשרה שכרים, באלפי שקלים. החציון 9.5, באמצע הקבוצה.", do=show("n3-md"),
      say="כאן עשרה שכרים, באלפי שקלים. החציון תשע וחצי, באמצע הקבוצה."),
    P("הממוצע 12.3: רק שני אנשים מתוך עשרה מרוויחים יותר ממנו. הוא לא מייצג את המרכז.", do=show("n3-mn", "q-x-1", "q-n-1"),
      say="הממוצע שתים עשרה נקודה שלוש: רק שני אנשים מתוך עשרה מרוויחים יותר ממנו. הוא לא מייצג את המרכז."),
    P("לכן הממוצע נופל: הוא בדיוק המדד שהזנב מושך.", hold=0.3),
    P("השכיח מראה רק את הערך הנפוץ. כאן יש אפילו שניים, 8 ו-9, והוא מתעלם מכל השאר.", do=show("q-x-2", "q-n-2")),
    P("ורבעון הוא לא מדד מרכז בכלל: הרבעון הראשון מסמן רבע מהנתונים, לא את האמצע.", do=show("q-x-3", "q-n-3")),
    P("נשאר החציון: הוא עמיד לזנב, ולכן הוא התשובה.", do=show("q-ok-0"), hold=0.6),
], stage=f'<div class="ed-col"><div id="x-n3" class="h">{N3.svg()}</div>'
         '<div class="ed-note">שכר חודשי של 10 עובדים (אלפי ₪)</div></div>',
   panel=w.stem(Q["id"], "באיזה מדד מודדים את המרכז של התפלגות עם צידוד (skew) גבוה, כמו שכר חודשי?")
         + st.options("q", OPTS, notes={1: "נמשך אחרי הזנב", 2: "רק הנפוץ", 3: "לא מרכז"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ממוצע הוא סכום חלקי כמות. חציון הוא האמצעי אחרי מיון.", do=show("r-1")),
    P("ובמספר זוגי של ערכים, החציון הוא הממוצע של שני האמצעיים.", do=show("r-2")),
    P("שכיח הוא הערך שחוזר הכי הרבה.", do=show("r-3")),
    P("ממוצע רגיש לערכים קיצוניים, חציון עמיד. זנב ימינה: ממוצע גדול מהחציון. נתראה ברמה הבאה.",
      do=show("r-4"), hold=0.6),
], stage='<div class="ed-col">' + w.eq("r-eq", "$\\bar{x} = \\dfrac{x_1 + x_2 + \\dots + x_n}{n}$", 48, hidden=False)
         + "</div>",
   panel=st.card("r-1", "rule", "🔑 חציון: <b>קודם ממיינים</b>")
         + st.card("r-2", "rule", "🔑 n זוגי: ממוצע שני האמצעיים")
         + st.card("r-3", "rule", "🔑 שכיח: הערך הנפוץ ביותר")
         + st.card("r-4", "trap", "⚠️ ערך קיצוני / הטיה: <b>חציון</b>, לא ממוצע"))

VIDEO = Video("E01", "eda", "ממוצע, חציון ושכיח", [title, idea, mean, even, skew, exam, recap],
              bank={"24A-B-Q15": 0})

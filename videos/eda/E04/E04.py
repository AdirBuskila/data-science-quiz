# -*- coding: utf-8 -*-
"""E04 · ערכים חריגים — video script (build: tools/video/vid.py E04).

Source: courses/eda/E04.js (lesson + goal: outliers by the two course methods, the IQR fences and the z-score, and
what happens when the threshold changes).
Exam anchor: 26B-A-Q24 (the distance-from-the-mean method: an outlier is at least 3 standard deviations away, since
~99.7% of a normal variable lies within +-3 sd). No guided quiz uses it. Not used on purpose: every E04 quiz item
(10,12,12,13,14,15,16,18,45 / Q1 = 30, Q3 = 50 / mean 70 sd 8 x = 58 / mean 50 sd 6 / 2..25 with multiplier 1), the
lesson's Q1 = 12, Q3 = 17, the boss item 26B-A-Q7 (Q1 = 10, Q3 = 20 -> -5..35), and the cleaning-course items on
outliers in pandas code (25-S-Q25, 26A-A-Q9, 25-S-Q6, 26A-B-Q21).
Worked examples: 41,20,47,36,78,38,45,35,43,40 (Q1 = 36, Q3 = 45, fences 22.5 / 58.5 -> 20 and 78; with multiplier 3
the fences are 9 / 72 -> only 78); heights with mean 170 and sd 7 (193 -> z = 3.29, 156 -> z = -2).
Quartiles from the course checker's quartiles(); the 68/95/99.7 shares from scipy's normal cdf.
"""
import numpy as np
from scipy.stats import norm

from vid import P, Scene, Video, show, hide, BANK
from common import quartiles
import stage as st
import w_eda as w

# ---------------------------------------------------------------- data (verified)
D = [41, 20, 47, 36, 78, 38, 45, 35, 43, 40]
S = sorted(D)
assert S == [20, 35, 36, 38, 40, 41, 43, 45, 47, 78]
q1, q2, q3 = quartiles(D)
assert (q1, q2, q3) == (36, 40.5, 45) and q3 - q1 == 9
assert w.fences(D) == (22.5, 58.5) and w.outliers(D) == [20, 78]
assert w.fences(D, 3) == (9, 72) and w.outliers(D, 3) == [78]

MU, SD = 170, 7
z_hi, z_lo = (193 - MU) / SD, (156 - MU) / SD
assert round(z_hi, 2) == 3.29 and z_lo == -2
assert (MU - 3 * SD, MU + 3 * SD) == (149, 191)
share = lambda k: norm.cdf(k) - norm.cdf(-k)
assert round(share(1), 2) == 0.68 and round(share(2), 2) == 0.95 and round(share(3), 3) == 0.997
assert round(1 - share(1), 2) == 0.32 and round(1 - share(3), 4) == 0.0027

# exam 26B-A-Q24
Q = BANK["26B-A-Q24"]
assert Q["correctIndex"] == 0 and Q["options"][0].startswith("3 סטיות תקן")
assert Q["options"][1:] == ["סטיית תקן אחת", "חציון אחד", "טווח בין-רבעוני אחד (IQR)"]
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
ST0 = w.strip("s0", D, cell=74)
ST1 = w.strip("s1", S, cell=74, brackets=[("lo", 0, 4, "Q1 = 36"), ("hi", 5, 9, "Q3 = 45")])

NL = w.NumLine("nl", 0, 90, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90], w=940, h=230, dot=9)
NL.band("nl-ok", 22.5, 58.5, kind="a", label="טווח תקין")
NL.dots("nl-d", S, kind="ink", hidden=False)
NL.dots("nl-oa", [20], kind="bad", hidden=True)
NL.dots("nl-ob", [78], kind="bad", hidden=True)
NL.mark("nl-f1", 22.5, "22.5", kind="b")
NL.mark("nl-f2", 58.5, "58.5", kind="b")
NL.mark("nl-g1", 9, "9", kind="c")
NL.mark("nl-g2", 72, "72", kind="c")

NZ = w.NumLine("nz", 140, 200, [142, 149, 156, 163, 170, 177, 184, 191, 198], w=940, h=230, dot=13)
NZ.band("nz-b", 149, 191, kind="a", label="ממוצע ± 3 סטיות תקן")
NZ.mark("nz-m", 170, "170", kind="a")
NZ.dots("nz-p1", [193], kind="bad", hidden=True)
NZ.dots("nz-p2", [156], kind="ok", hidden=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לזהות **ערכים חריגים**."),
    P("נכיר את שתי השיטות של הקורס, גדר ה-IQR וציון z, ונראה מה קורה כשמשנים את הסף."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">E04 · סטטיסטיקה וגרפים</div><h1>ערכים חריגים</h1>'
         '<p>לזהות חריגים בשתי השיטות של הקורס, גדר ה-IQR וציון z, ולדעת מה קורה כשמשנים את הסף.</p>', layout="title")

fence = Scene("fence", "שיטת ה-IQR", [
    P("ערך חריג הוא ערך שרחוק מאוד משאר הנתונים. אבל כמה רחוק זה ״מאוד״? צריך כלל.", hold=0.2),
    P("השיטה הראשונה בונה **גדרות** מהרבעונים. הנה עשרה ערכים.", do=show("f-s0")),
    P("ממיינים, ומחשבים רבעונים בשיטת הקורס: חצי תחתון של חמישה, וחצי עליון של חמישה.", do=show("f-s1")),
    P("הרבעון הראשון 36, השלישי 45, ולכן הטווח הבין רבעוני הוא 9.", do=show("s1-br-lo", "s1-br-hi", "f-1")),
    P("מכפילים באחת וחצי: 13.5. זה המרחק של הגדרות מהקופסה.", do=show("f-2"),
      say="מכפילים באחת וחצי: שלוש עשרה וחצי. זה המרחק של הגדרות מהקופסה."),
    P("גדר תחתונה: 36 פחות 13.5, כלומר 22.5.", do=show("f-3"),
      say="גדר תחתונה: שלושים ושש פחות שלוש עשרה וחצי, כלומר עשרים ושתיים וחצי."),
    P("גדר עליונה: 45 ועוד 13.5, כלומר 58.5.", do=show("f-4"),
      say="גדר עליונה: ארבעים וחמש ועוד שלוש עשרה וחצי, כלומר חמישים ושמונה וחצי."),
    P("כל ערך מחוץ לגדרות הוא חריג.", do=show("f-rule"), hold=0.3),
], stage=f'<div class="ed-col"><div id="f-s0" class="h">{ST0}</div><div id="f-s1" class="h">{ST1}</div>'
         + w.eq("f-1", "$\\mathrm{IQR} = 45 - 36 = 9$", 38)
         + w.eq("f-2", "$1.5 \\times 9 = 13.5$", 38)
         + w.eq("f-3", "$36 - 13.5 = 22.5$", 38)
         + w.eq("f-4", "$45 + 13.5 = 58.5$", 38) + "</div>",
   panel=st.card("f-rule", "rule", "🔑 חריג: מתחת ל-$Q_1 - 1.5\\cdot\\mathrm{IQR}$ או מעל $Q_3 + 1.5\\cdot\\mathrm{IQR}$"))

line = Scene("line", "על הציר", [
    P("נשים את הנתונים על ציר, ונסמן את הגדרות.", do=show("l-nl", "nl-f1", "nl-f2", "nl-ok")),
    P("הערך 78 מעל הגדר העליונה, 58.5. הוא חריג.", do=show("nl-ob"),
      say="הערך שבעים ושמונה מעל הגדר העליונה, חמישים ושמונה וחצי. הוא חריג."),
    P("והערך 20 מתחת לגדר התחתונה, 22.5. גם הוא חריג, מהצד השני.", do=show("nl-oa"),
      say="והערך עשרים מתחת לגדר התחתונה, עשרים ושתיים וחצי. גם הוא חריג, מהצד השני."),
    P("שימו לב שבודקים את שני הצדדים. חריג יכול להיות גם קטן מדי.", do=show("l-c1"), hold=0.3),
    P("ועכשיו נשנה את הסף: במקום אחת וחצי, נכפיל בשלוש.", do=hide("nl-f1", "nl-f2", "nl-ok")),
    P("הגדרות מתרחקות: 36 פחות 27 זה 9, ו-45 ועוד 27 זה 72.", do=show("nl-g1", "nl-g2", "l-eq")),
    P("עכשיו 20 בתוך הגדרות, ורק 78 נשאר חריג.", do=hide("nl-oa") + show("l-r1")),
    P("מכפיל גדול יותר, גדרות רחבות יותר, ולכן **פחות** חריגים. ומכפיל קטן מסמן יותר.", hold=0.4),
], stage=f'<div class="ed-col"><div id="l-nl" class="h">{NL.svg()}</div>'
         + w.eq("l-eq", "$3 \\times 9 = 27:\\quad [\\,9,\\ 72\\,]$", 38) + "</div>",
   panel=st.card("l-c1", "ex", "מכפיל 1.5: הגדרות 22.5 ו-58.5 ← <b>20 ו-78</b> חריגים")
         + st.card("l-r1", "rule", "🔑 מכפיל 3: הגדרות 9 ו-72 ← רק <b>78</b>. סף גבוה = פחות חריגים"))

zsc = Scene("zsc", "ציון z", [
    P("השיטה השנייה מודדת מרחק מהממוצע, ביחידות של סטיית תקן. זה **ציון z**.", do=show("z-def")),
    P("מחסרים את הממוצע, ומחלקים בסטיית התקן.", hold=0.2),
    P("דוגמה: גובה של אנשים, עם ממוצע 170 סנטימטר, וסטיית תקן 7.", do=show("z-nl")),
    P("אדם בגובה 193: ההפרש הוא 23, וחלקי 7 זה בערך 3.3.", do=show("nz-p1", "z-1"),
      say="אדם בגובה מאה תשעים ושלוש: ההפרש הוא עשרים ושלוש, וחלקי שבע זה בערך שלוש נקודה שלוש."),
    P("הכלל: ערך שרחוק **יותר משלוש סטיות תקן** מהממוצע הוא חריג. ולכן 193 חריג.", do=show("nz-b", "z-rule"),
      say="הכלל: ערך שרחוק יותר משלוש סטיות תקן מהממוצע הוא חריג. ולכן מאה תשעים ושלוש חריג."),
    P("אדם בגובה 156: ההפרש מינוס 14, וחלקי 7 זה מינוס 2. רק שתי סטיות תקן מתחת. לא חריג.", do=show("nz-p2", "z-2"),
      say="אדם בגובה מאה חמישים ושש: ההפרש מינוס ארבע עשרה, וחלקי שבע זה מינוס שתיים. רק שתי סטיות תקן מתחת. לא חריג."),
    P("ולמה שלוש? בהתפלגות נורמלית, כ-99.7 אחוז מהנתונים נמצאים בטווח של שלוש סטיות תקן מהממוצע.", do=show("z-why"),
      say="ולמה שלוש? בהתפלגות נורמלית, כתשעים ותשע נקודה שבע אחוז מהנתונים נמצאים בטווח של שלוש סטיות תקן מהממוצע."),
    P("ושימו לב: חריג הוא לא בהכרח טעות. אדם בגובה 193 קיים באמת. חריג הוא רק ״נדיר״.", do=show("z-trap"),
      hold=0.4, say="ושימו לב: חריג הוא לא בהכרח טעות. אדם בגובה מאה תשעים ושלוש קיים באמת. חריג הוא רק נדיר."),
], stage=f'<div class="ed-col"><div id="z-nl" class="h">{NZ.svg()}</div>'
         + w.eq("z-1", "$z = \\dfrac{193 - 170}{7} \\approx 3.29$", 40)
         + w.eq("z-2", "$z = \\dfrac{156 - 170}{7} = -2$", 40) + "</div>",
   panel=st.card("z-def", "plain", "$z = \\dfrac{x - \\bar{x}}{s}$")
         + st.card("z-rule", "rule", "🔑 חריג אם $|z| > 3$")
         + st.card("z-why", "ex", "נורמלית:<br>$\\pm 1 \\to 68\\%,\\ \\ \\pm 2 \\to 95\\%,\\ \\ \\pm 3 \\to 99.7\\%$")
         + st.card("z-trap", "trap", "⚠️ חריג ≠ שגוי: ייתכן ערך אמיתי ונדיר"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: לפי שיטת המרחק בסטיות תקן מהממוצע, ערך נחשב חריג אם הוא מרוחק מהממוצע לפחות כמה?"),
    P("זו בדיוק השיטה השנייה שלנו. והתשובה: שלוש סטיות תקן, בגלל כלל ה-99.7 אחוז.", do=show("q-ok-0"),
      say="זו בדיוק השיטה השנייה שלנו. והתשובה: שלוש סטיות תקן, בגלל כלל התשעים ותשע נקודה שבע אחוז."),
    P("סטיית תקן אחת קרובה מדי: בהתפלגות נורמלית, כשליש מהנתונים רחוקים יותר מזה.", do=show("q-x-1", "q-n-1")),
    P("כמעט אחד מכל שלושה ערכים היה ״חריג״. זה כבר לא נדיר.", hold=0.2),
    P("חציון הוא מדד מרכז, נקודה בנתונים. הוא לא יחידה של מרחק.", do=show("q-x-2", "q-n-2")),
    P("וטווח בין רבעוני שייך לשיטה האחרת: שם מודדים אחת וחצי כפול IQR מהרבעונים, ולא מהממוצע.",
      do=show("q-x-3", "q-n-3"), hold=0.6),
], stage='<div class="ed-col">' + w.eq("x-eq", "$|z| = \\dfrac{|x - \\bar{x}|}{s} \\ge 3$", 52, hidden=False)
         + '<div class="ed-note">כ-0.3% בלבד מהנתונים הנורמליים מחוץ לטווח</div></div>',
   panel=w.stem(Q["id"], "לפי שיטת המרחק בסטיות תקן מהממוצע (למשתנה נורמלי), ערך חריג אם הוא מרוחק מהממוצע לפחות:")
         + st.options("q", OPTS, notes={1: "כ-32% מחוץ", 2: "לא מרחק", 3: "שיטה אחרת"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום, שתי שיטות. שיטת ה-IQR: גדרות במרחק אחת וחצי כפול IQR מהרבעונים.", do=show("r-1")),
    P("ושיטת ציון z: חריג אם הוא רחוק יותר משלוש סטיות תקן מהממוצע.", do=show("r-2")),
    P("מכפיל גדול יותר נותן פחות חריגים.", do=show("r-3")),
    P("וחריג הוא לא בהכרח שגוי. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ed-col">' + w.eq("r-eq1", "$[\\,Q_1 - 1.5\\,\\mathrm{IQR},\\ \\ Q_3 + 1.5\\,\\mathrm{IQR}\\,]$", 44, hidden=False)
         + w.eq("r-eq2", "$|z| > 3$", 52, hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 גדרות IQR מהרבעונים")
         + st.card("r-2", "rule", "🔑 $|z| > 3$ מהממוצע")
         + st.card("r-3", "rule", "🔑 סף גבוה ← פחות חריגים")
         + st.card("r-4", "trap", "⚠️ חריג ≠ טעות"))

VIDEO = Video("E04", "eda", "ערכים חריגים", [title, fence, line, zsc, exam, recap], bank={"26B-A-Q24": 0})

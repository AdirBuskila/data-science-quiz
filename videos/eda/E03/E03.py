# -*- coding: utf-8 -*-
"""E03 · אחוזונים, רבעונים ו-IQR — video script (build: tools/video/vid.py E03).

Source: courses/eda/E03.js (lesson + goal: the position of a percentile (p% of n, rounded up), Q1 and Q3 by the
course method (medians of the halves, the median left out when n is odd), IQR = Q3 - Q1).
Exam anchor: 24A-A-Q8 (IQR of 16,19,23,36,39,81,85,90 -> 62; even n). No guided quiz uses it (the E03 lesson cites
it; its key is the reference the checker's quartiles() was built on). Not used on purpose: every E03 quiz item
(45 values / 30th percentile, the IQRs of 5..27 and 4..25, Q1 = 22 / Q3 = 40, 20 scores / 15th), the lesson's
3..20 example, and the boss items 24A-B-Q19 (49 values, 20th percentile) and 25A-A-Q2 (8,2,4,4,6,12,17,6,6).
Worked examples: the 90th percentile of 36 values; quartiles of 14,2,21,9,30,6,11,18,5,13,8 (n = 11), and the
wrong result when the median is kept in both halves.
Every quartile below comes from the course checker's quartiles() (tools/verify/needhelp/common.py) and is asserted.
"""
import math

import numpy as np

from vid import P, Scene, Video, show, hide, BANK
from common import quartiles, iqr
import stage as st
import w_eda as w

# ---------------------------------------------------------------- data (verified)
assert 0.9 * 36 == 32.4 and math.ceil(0.9 * 36) == 33

D = [14, 2, 21, 9, 30, 6, 11, 18, 5, 13, 8]
S = sorted(D)
assert S == [2, 5, 6, 8, 9, 11, 13, 14, 18, 21, 30] and len(S) == 11
assert quartiles(D) == (6, 11, 18) and iqr(D) == 12
assert np.median(S[:5]) == 6 and np.median(S[6:]) == 18
# the trap: keep the median in both halves
lo_bad, hi_bad = S[:6], S[5:]
assert np.median(lo_bad) == 7 and np.median(hi_bad) == 16 and 16 - 7 == 9

# exam 24A-A-Q8
Q = BANK["24A-A-Q8"]
X = [16, 19, 23, 36, 39, 81, 85, 90]
assert "[16,19,23,36,39,81,85,90]" in Q["question"].replace(" ", "")
assert Q["correctIndex"] == 0 and Q["options"] == ["62", "37.5", "49", "83"]
assert quartiles(X) == (21, 37.5, 83) and iqr(X) == 62
assert round(np.mean(X), 3) == 48.625                    # 49 is about the mean, a measure of center
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
CELL = 74
ST0 = w.strip("s0", D, cell=CELL)
ST1 = w.strip("s1", S, cell=CELL, brackets=[("lo", 0, 4, "חצי תחתון: Q1 = 6"), ("md", 5, 5, "חציון"),
                                            ("hi", 6, 10, "חצי עליון: Q3 = 18")])
ST2 = w.strip("s2", S, cell=CELL, brackets=[("lo", 0, 5, "Q1 = 7 ✗")])
ST3 = w.strip("s3", S, cell=CELL, brackets=[("hi", 5, 10, "Q3 = 16 ✗")])
SX = w.strip("sx", X, brackets=[("lo", 0, 3, "Q1 = (19+23)÷2 = 21"), ("hi", 4, 7, "Q3 = (81+85)÷2 = 83")])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נחתוך נתונים ממוינים לחלקים."),
    P("נמצא איפה נמצא אחוזון, נחשב רבעונים בשיטה של הקורס, ומהם את הטווח הבין רבעוני."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">E03 · סטטיסטיקה וגרפים</div><h1>אחוזונים, רבעונים ו-IQR</h1>'
         '<p>למצוא את מיקום האחוזון, לחשב Q1 ו-Q3 בשיטת הקורס, ולהחסיר ביניהם כדי לקבל IQR.</p>', layout="title")

idea = Scene("idea", "אחוזון", [
    P("אחרי שממיינים את הנתונים, **אחוזון** הוא ערך שחלק ידוע מהנתונים נמצא מתחתיו."),
    P("למשל, האחוזון התשעים הוא ערך שתשעים אחוז מהנתונים קטנים ממנו או שווים לו.", do=show("a-def")),
    P("איך מוצאים אותו? כופלים את האחוז במספר הנתונים, ומעגלים **למעלה**.", do=show("a-rule")),
    P("נניח שיש 36 נתונים, ורוצים את האחוזון התשעים.", do=show("a-0")),
    P("תשעים אחוז כפול 36 זה 32.4.", do=show("a-1"),
      say="תשעים אחוז כפול שלושים ושש זה שלושים ושתיים נקודה ארבע."),
    P("מעגלים למעלה ל-33. האחוזון התשעים הוא המדידה ה-33, בסדר העולה.", do=show("a-2", "a-2c"),
      say="מעגלים למעלה לשלושים ושלוש. האחוזון התשעים הוא המדידה השלושים ושלוש, בסדר העולה."),
    P("לא המדידה ה-32: שם עדיין פחות מתשעים אחוז מהנתונים.", do=show("a-trap"),
      say="לא המדידה השלושים ושתיים: שם עדיין פחות מתשעים אחוז מהנתונים."),
    P("ולא המדידה התשעים: האחוז הוא חלק מ-n, לא מקום ברשימה.", hold=0.4,
      say="ולא המדידה התשעים: האחוז הוא חלק מאֶן, לא מקום ברשימה."),
], stage='<div class="ed-col">'
         + w.eq("a-0", "$n = 36,\\quad p = 90\\%$", 44)
         + w.eq("a-1", "$0.90 \\times 36 = 32.4$", 48)
         + w.eq("a-2", "$32.4 \\;\\xrightarrow{\\text{ round up }}\\; 33$", 52)
         + w.chip("a-2c", "המדידה ה-33 אחרי מיון", "ok") + "</div>",
   panel=st.card("a-def", "plain", "אחוזון $p$: $p\\%$ מהנתונים קטנים ממנו או שווים לו")
         + st.card("a-rule", "rule", "🔑 מיקום = $p\\% \\times n$, מעוגל <b>למעלה</b>")
         + st.card("a-trap", "trap", "⚠️ 32 נותן רק $32/36 \\approx 89\\%$"))

quart = Scene("quart", "רבעונים", [
    P("**רבעונים** הם שלוש נקודות חיתוך, שמחלקות את הנתונים הממוינים לארבעה חלקים שווים.", do=show("q-def")),
    P("הרבעון השני הוא בדיוק החציון. ואת הראשון והשלישי מחשבים בשיטת הקורס, בחצאים.", do=show("q-m")),
    P("הנה אחד עשר ערכים. קודם, כמו תמיד, ממיינים.", do=show("q-s0")),
    P("אחרי מיון: מ-2 ועד 30.", do=show("q-s1")),
    P("יש אחד עשר ערכים, מספר אי זוגי, ולכן החציון הוא השישי: 11.", do=show("s1-k5", "s1-br-md")),
    P("עכשיו מפצלים לחצי תחתון וחצי עליון, **בלי** החציון עצמו.", do=show("s1-d5")),
    P("החצי התחתון: 2, 5, 6, 8, 9. החציון שלו הוא 6. זה הרבעון הראשון.", do=show("s1-br-lo")),
    P("החצי העליון: 13, 14, 18, 21, 30. החציון שלו, 18, הוא הרבעון השלישי.", do=show("s1-br-hi")),
    P("והטווח הבין רבעוני הוא ההפרש ביניהם: 18 פחות 6, כלומר 12.", do=show("q-iqr")),
    P("הוא מודד את הרוחב של חצי הנתונים האמצעי, ולכן הוא מדד פיזור.", hold=0.4),
], stage=f'<div class="ed-col"><div id="q-s0" class="h">{ST0}</div><div id="q-s1" class="h">{ST1}</div>'
         + w.eq("q-iqr", "$\\mathrm{IQR} = Q_3 - Q_1 = 18 - 6 = 12$", 42) + "</div>",
   panel=st.card("q-def", "plain", "$Q_1$ · $Q_2$ = חציון · $Q_3$")
         + st.card("q-m", "rule", "🔑 $Q_1$ = חציון החצי התחתון, $Q_3$ = חציון החצי העליון. n אי-זוגי: <b>מוציאים</b> את החציון"))

trap = Scene("trap", "המלכודת", [
    P("ומה אם משאירים את החציון בתוך החצאים? נראה מה יוצא.", hold=0.2),
    P("החצי התחתון יהיה שישה ערכים, מ-2 עד 11. החציון שלו: 6 ועוד 8, חלקי שתיים. כלומר 7.", do=show("t-s2")),
    P("והחצי העליון, מ-11 עד 30: 14 ועוד 18, חלקי שתיים. כלומר 16.", do=show("t-s3")),
    P("ואז הטווח הבין רבעוני יוצא 9, במקום 12.", do=show("t-bad")),
    P("שתי השיטות קיימות בעולם, ולכן כדאי לדעת בדיוק מה הקורס מצפה.", hold=0.2),
    P("בשיטת הקורס, כשמספר הנתונים אי זוגי, החציון **לא** נכנס לאף חצי.", do=show("t-rule"), hold=0.4),
], stage=f'<div class="ed-col"><div id="t-s2" class="h">{ST2}</div><div id="t-s3" class="h">{ST3}</div>'
         + w.eq("t-bad", "$16 - 7 = 9 \\;\\ne\\; 12$", 44) + "</div>",
   panel=st.card("t-rule", "trap", "⚠️ n אי-זוגי: החציון <b>מחוץ</b> לשני החצאים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: חשבו את הטווח הבין רבעוני של שמונה נתונים: מ-16 ועד 90."),
    P("הנתונים כבר ממוינים. יש שמונה, מספר זוגי, ולכן הם מתחלקים לשני חצאים של ארבעה.", do=show("x-s")),
    P("החצי התחתון: 16, 19, 23, 36. יש שני אמצעיים, 19 ו-23, והממוצע שלהם 21. זה הרבעון הראשון.",
      do=show("sx-br-lo")),
    P("החצי העליון: 39, 81, 85, 90. הממוצע של 81 ו-85 הוא 83. זה הרבעון השלישי.", do=show("sx-br-hi")),
    P("ההפרש: 83 פחות 21, כלומר 62. זו התשובה.", do=show("x-eq", "q-ok-0")),
    P("והמלכודות: 83 הוא הרבעון השלישי לבדו, ושכחו להחסיר.", do=show("q-x-3", "q-n-3")),
    P("37.5 הוא החציון: הממוצע של 36 ו-39. זה מדד מרכז, לא פיזור.", do=show("q-x-1", "q-n-1"),
      say="שלושים ושבע וחצי הוא החציון: הממוצע של שלושים ושש ושלושים ותשע. זה מדד מרכז, לא פיזור."),
    P("ו-49 בכלל לא יוצא מהרבעונים. הוא קרוב לממוצע, 48.6, שגם הוא מדד מרכז.", do=show("q-x-2", "q-n-2"),
      say="וארבעים ותשע בכלל לא יוצא מהרבעונים. הוא קרוב לממוצע, ארבעים ושמונה נקודה שש, שגם הוא מדד מרכז.",
      hold=0.6),
], stage=f'<div class="ed-col"><div id="x-s" class="h">{SX}</div>'
         + w.eq("x-eq", "$\\mathrm{IQR} = 83 - 21 = 62$", 46) + "</div>",
   panel=w.stem(Q["id"], "חשבו את ה-IQR של הנתונים: 16, 19, 23, 36, 39, 81, 85, 90")
         + st.options("q", OPTS, notes={1: "החציון", 2: "≈ הממוצע", 3: "רק Q3"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מיקום אחוזון הוא האחוז כפול מספר הנתונים, מעוגל למעלה.", do=show("r-1")),
    P("הרבעון הראשון והשלישי הם החציונים של החצי התחתון והחצי העליון.", do=show("r-2")),
    P("כשמספר הנתונים אי זוגי, החציון יוצא משני החצאים.", do=show("r-3")),
    P("והטווח הבין רבעוני הוא תמיד הפרש: השלישי פחות הראשון. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ed-col">' + w.eq("r-eq", "$\\mathrm{IQR} = Q_3 - Q_1$", 60, hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 אחוזון: $p\\% \\times n$, מעגלים למעלה")
         + st.card("r-2", "rule", "🔑 $Q_1$, $Q_3$: חציוני החצאים")
         + st.card("r-3", "trap", "⚠️ n אי-זוגי: בלי החציון")
         + st.card("r-4", "rule", "🔑 IQR = <b>הפרש</b>, לא $Q_3$ לבד"))

VIDEO = Video("E03", "eda", "אחוזונים, רבעונים ו-IQR", [title, idea, quart, trap, exam, recap],
              bank={"24A-A-Q8": 0})

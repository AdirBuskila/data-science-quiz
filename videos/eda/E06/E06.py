# -*- coding: utf-8 -*-
"""E06 · מתאם פירסון — video script (build: tools/video/vid.py E06).

Source: courses/eda/E06.js (lesson + goal: compute and read a correlation coefficient: sign, strength, and the limit
that it measures only a linear relation).
Exam anchor: 25-S-Q9 (three scatter plots: right ~0, middle negative, left positive). No guided quiz uses it. The
original figure is shown as is; its reading is asserted by locating the red dots in each third of the image
(w_eda.raster_corr) and computing Pearson's r of their centroids: left +0.99, middle -0.88, right +0.08.
Not used on purpose: every E06 quiz item (x = 1..5 / y = 2,4,5,4,5; y = x^2 on -3..3; y = -2x + 10; Z = -2Y + 5 from
0.6; the A..D list), the lesson's x = 1,2,3 / y = 1,3,2 and y = x^2 on -2..2, the boss item 26B-A-Q6, and 24A-A-Q9
(kept for the E08 walkthrough). Worked examples: x = 2,4,6,8 with y = 3,7,5,9 (r = 16/20 = 0.8), its mirror
y' = 12 - y (r = -0.8), and the V shape x = -3,-1,1,3 / y = 3,1,1,3 (r = 0 with y = |x|).
Every r below is computed with numpy (w_eda.pearson_parts asserts it equals np.corrcoef).
"""
import os

import numpy as np

from vid import P, Scene, Video, show, hide, BANK, ROOT
import stage as st
import w_eda as w

# ---------------------------------------------------------------- data (verified)
X, Y = [2, 4, 6, 8], [3, 7, 5, 9]
dx, dy, sxy, sxx, syy, r = w.pearson_parts(X, Y)
assert np.mean(X) == 5 and np.mean(Y) == 6
assert list(dx) == [-3, -1, 1, 3] and list(dy) == [-3, 1, -1, 3]
assert list(dx * dy) == [9, -1, -1, 9] and sxy == 16 and sxx == 20 and syy == 20 and r == 0.8

Y2 = [12 - v for v in Y]
assert Y2 == [9, 5, 7, 3] and abs(w.pearson_parts(X, Y2)[-1] + 0.8) < 1e-12

XV, YV = [-3, -1, 1, 3], [3, 1, 1, 3]
assert YV == [abs(v) for v in XV] and abs(w.pearson_parts(XV, YV)[-1]) < 1e-12
assert list(np.array(XV) * (np.array(YV) - 2)) == [-3, 1, -1, 3]           # products cancel: -3 + 1 - 1 + 3 = 0

# exam 25-S-Q9 (the figure, read by machine)
Q = BANK["25-S-Q9"]
assert Q["correctIndex"] == 0 and Q["image"] == "images/exams/25-S-Q9.png"
assert Q["options"][0] == "בגרף הימני יש מתאם קרוב לאפס, בגרף האמצעי שלילי ובגרף השמאלי חיובי"
red = lambda R, G, B: (R > 200) & (G < 130) & (B < 110)
(nl, rl), (nm, rm), (nr, rr) = w.raster_corr(os.path.join(ROOT, Q["image"]), red, [(0, 280), (280, 560), (560, 830)])
assert rl > 0.95 and rm < -0.8 and abs(rr) < 0.15 and nm >= 12 and nr >= 14
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
SC1 = w.scatter("p1", X, Y, (0, 10), (0, 10), w=500, h=440, xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8, 10],
                labels=True, kind="a")
SC2 = w.scatter("p2", X, Y2, (0, 10), (0, 10), w=420, h=380, xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8, 10],
                kind="b")
SC3 = w.scatter("p3", XV, YV, (-4, 4), (0, 4), w=420, h=380, xticks=[-4, -2, 0, 2, 4], yticks=[0, 1, 2, 3, 4],
                kind="ok")
ROWS = [[w.fmt(a), w.fmt(b), w.fmt(c).replace("-", "−"), w.fmt(d).replace("-", "−"), w.fmt(c * d).replace("-", "−")]
        for a, b, c, d in zip(X, Y, dx, dy)]
TAB = w.table("t", ["$x$", "$y$", "$x-\\bar{x}$", "$y-\\bar{y}$", "מכפלה"], ROWS + [["", "", "", "", "<b>16</b>"]],
              hide={2, 3, 4}, size=30, cls="tight")
FIG = st.raster("fig", Q["image"], 1000, (830, 239),
                tags=[("שמאלי", 140, 0), ("אמצעי", 420, 0), ("ימני", 700, 0)])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נמדוד קשר בין שני משתנים, במספר אחד: מקדם המתאם של פירסון."),
    P("נחשב אותו ביד, נבין מה אומרים הסימן והגודל, ונראה מה הוא לא רואה."),
    P("ובסוף נקרא גרפים משאלת מבחן.", hold=0.4),
], stage='<div class="kicker">E06 · סטטיסטיקה וגרפים</div><h1>מתאם פירסון</h1>'
         '<p>לחשב ולפרש מקדם מתאם: סימן, עוצמה, והמגבלה שהוא מודד רק קשר לינארי.</p>', layout="title")

calc = Scene("calc", "חישוב ביד", [
    P("הנה ארבע נקודות. כש-$x$ גדל, $y$ גדל בדרך כלל. כמה חזק הקשר?", do=show("c-sc", "c-f")),
    P("צעד ראשון: הממוצעים. הממוצע של $x$ הוא 5, ושל $y$ הוא 6.", do=show("p1-mx", "p1-my")),
    P("הקווים האלה מחלקים את הגרף לארבעה רבעים.", hold=0.2),
    P("צעד שני: הסטיות מהממוצע. ל-$x$: מינוס 3, מינוס 1, 1, ו-3.", do=show("t-r0c2", "t-r1c2", "t-r2c2", "t-r3c2")),
    P("ל-$y$: מינוס 3, 1, מינוס 1, ו-3.", do=show("t-r0c3", "t-r1c3", "t-r2c3", "t-r3c3")),
    P("צעד שלישי: כופלים את שתי הסטיות של כל נקודה. 9, מינוס 1, מינוס 1, ו-9. הסכום: 16.",
      do=show("t-r0c4", "t-r1c4", "t-r2c4", "t-r3c4", "t-r4c4")),
    P("נקודה ברבע הירוק, שבה שניהם מעל הממוצע או שניהם מתחתיו, נותנת מכפלה **חיובית**.", do=show("p1-qp")),
    P("וברבע האדום, כשאחד מעל ואחד מתחת, המכפלה **שלילית**. כאן רוב המשקל בירוק.", do=show("p1-qn")),
    P("צעד רביעי: מחלקים בשורש של מכפלת סכומי הריבועים. כאן כל סכום הוא 20.", do=show("c-eq1")),
    P("16 חלקי שורש של 400, כלומר 16 חלקי 20: המתאם הוא 0.8. קשר חיובי חזק.", do=show("c-eq2", "c-ok"),
      say="שש עשרה חלקי שורש של ארבע מאות, כלומר שש עשרה חלקי עשרים: המתאם הוא אפס נקודה שמונה. קשר חיובי חזק.",
      hold=0.4),
], stage=f'<div class="ed-rowc"><div id="c-sc" class="h">{SC1}</div><div class="ed-col" style="width:auto">{TAB}'
         + w.eq("c-eq1", "$r = \\dfrac{16}{\\sqrt{20 \\cdot 20}}$", 38)
         + w.eq("c-eq2", "$= \\dfrac{16}{20} = 0.8$", 38) + "</div></div>",
   panel=st.card("c-f", "plain", "$r = \\dfrac{\\sum (x-\\bar{x})(y-\\bar{y})}{\\sqrt{\\sum (x-\\bar{x})^2 \\cdot \\sum (y-\\bar{y})^2}}$")
         + st.card("c-ok", "rule", "🔑 רוב הנקודות ברבעים הירוקים ← $r > 0$"))

sign = Scene("sign", "סימן ועוצמה", [
    P("המתאם תמיד בין מינוס 1 ל-1. הסימן אומר את **הכיוון**.", do=show("s-c1")),
    P("עכשיו נהפוך את הנקודות: במקום $y$ ניקח 12 פחות $y$. כש-$x$ עולה, הערך יורד.", do=show("s-sc2")),
    P("כל המכפלות מחליפות סימן, והמתאם יוצא מינוס 0.8.", do=show("s-r2"),
      say="כל המכפלות מחליפות סימן, והמתאם יוצא מינוס אפס נקודה שמונה."),
    P("האם הקשר נחלש? לא. הנקודות קרובות לקו בדיוק באותה מידה, רק בכיוון ההפוך.", hold=0.2),
    P("**העוצמה** היא הערך המוחלט. מינוס 0.8 חזק בדיוק כמו 0.8, וחזק יותר מ-0.5.", do=show("s-c2"),
      say="העוצמה היא הערך המוחלט. מינוס אפס נקודה שמונה חזק בדיוק כמו אפס נקודה שמונה, וחזק יותר מאפס נקודה חמש."),
    P("קרוב ל-1 או למינוס 1: קשר לינארי חזק. קרוב לאפס: אין קשר **לינארי**.", do=show("s-c3"), hold=0.4),
], stage=f'<div class="ed-rowc"><div id="s-sc2" class="h">{SC2}</div>'
         + '<div class="ed-col" style="width:auto">' + w.eq("s-r2", "$r = -0.8$", 50) + "</div></div>",
   panel=st.card("s-c1", "plain", "$-1 \\le r \\le 1$ · סימן = כיוון")
         + st.card("s-c2", "rule", "🔑 עוצמה = $|r|$: $\\ |-0.8| = |0.8| > |0.5|$")
         + st.card("s-c3", "ex", "$|r| \\approx 1$: חזק · $r \\approx 0$: אין קשר <b>לינארי</b>"))

lin = Scene("lin", "רק לינארי", [
    P("ולמה ההדגשה על לינארי? הנה ארבע נקודות בצורת וי: $y$ הוא הערך המוחלט של $x$.", do=show("l-sc3")),
    P("$y$ נקבע לגמרי על ידי $x$. יש כאן תלות מושלמת.", hold=0.2),
    P("אבל בצד שמאל הנקודות יורדות, ובצד ימין הן עולות. המכפלות מתקזזות: מינוס 3, 1, מינוס 1 ו-3.",
      do=show("p3-mx", "p3-my", "l-eq")),
    P("הסכום אפס, ולכן המתאם הוא **אפס**.", do=show("l-r")),
    P("כלומר: מתאם אפס אומר שאין קשר לינארי, ולא שאין קשר בכלל.", do=show("l-trap")),
    P("ועוד דבר: מתאם הוא לא סיבתיות. הוא מודד חוזק של קשר, לא מי גרם למי.", do=show("l-c2"), hold=0.4),
], stage=f'<div class="ed-rowc"><div id="l-sc3" class="h">{SC3}</div><div class="ed-col" style="width:auto">'
         + w.eq("l-eq", "$\\sum = -3+1-1+3 = 0$", 38) + w.eq("l-r", "$r = 0$", 50) + "</div></div>",
   panel=st.card("l-trap", "trap", "⚠️ $r = 0$: אין קשר <b>לינארי</b>, לא ״אין תלות״")
         + st.card("l-c2", "trap", "⚠️ מתאם ≠ סיבתיות"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה ניתן לומר על המתאם בכל אחד משלושת הגרפים?", do=show("x-fig")),
    P("בגרף השמאלי הנקודות עולות, צמודות לקו: מתאם חיובי חזק.", do=show("x-l")),
    P("בגרף האמצעי הן יורדות לאורך הקו: מתאם שלילי.", do=show("x-m")),
    P("ובגרף הימני, ענן בלי כיוון: מתאם קרוב לאפס.", do=show("x-r")),
    P("לכן התשובה: ימני קרוב לאפס, אמצעי שלילי, שמאלי חיובי.", do=show("q-ok-0")),
    P("המלכודת: בשאלה בעברית, ״הימני״ הוא הגרף הימני בתמונה, ולא הראשון שקוראים משמאל.", do=show("x-trap")),
    P("התשובה שבה הימני חיובי והשמאלי אפס, פשוט החליפה בין ימין לשמאל.", do=show("q-x-2", "q-n-2")),
    P("זו שבה האמצעי חיובי טועה בכיוון: הנקודות שם יורדות.", do=show("q-x-1", "q-n-1")),
    P("ו״רק בשמאלי יש מתאם״ שוכחת שגם מתאם שלילי הוא מתאם, וחזק.", do=show("q-x-3", "q-n-3"), hold=0.6),
], stage=f'<div class="ed-col"><div id="x-fig" class="h">{FIG}</div>'
         '<div class="ed-rowc" style="font-size:32px">'
         + w.chip("x-l", "שמאלי: חיובי", "ok") + w.chip("x-m", "אמצעי: שלילי", "bad")
         + w.chip("x-r", "ימני: ≈ 0", "warn") + "</div>"
         + st.card("x-trap", "trap", "⚠️ ״ימני״ = הגרף הימני בתמונה") + "</div>",
   panel='<div class="ed-small">' + w.stem(Q["id"], "מה ניתן לומר על המתאם בין X1 ו-X2 בכל אחד מהתרשימים?")
         + st.options("q", OPTS, notes={1: "כיוון הפוך", 2: "ימין↔שמאל", 3: "שוכחת שלילי"}) + "</div>")

recap = Scene("recap", "סיכום", [
    P("לסיכום: המתאם בין מינוס 1 ל-1. מכפלות הסטיות קובעות את הסימן.", do=show("r-1")),
    P("הסימן הוא הכיוון, והעוצמה היא הערך המוחלט.", do=show("r-2")),
    P("מתאם אפס אומר שאין קשר לינארי, אבל ייתכן קשר אחר.", do=show("r-3")),
    P("ומתאם הוא לא סיבתיות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="ed-col">'
         + w.eq("r-eq", "$r = \\dfrac{\\sum (x-\\bar{x})(y-\\bar{y})}{\\sqrt{\\sum (x-\\bar{x})^2 \\cdot \\sum (y-\\bar{y})^2}}$", 46,
                hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 $-1 \\le r \\le 1$")
         + st.card("r-2", "rule", "🔑 סימן = כיוון · עוצמה = $|r|$")
         + st.card("r-3", "trap", "⚠️ $r = 0$ ≠ אין תלות")
         + st.card("r-4", "trap", "⚠️ מתאם ≠ סיבתיות"))

VIDEO = Video("E06", "eda", "מתאם פירסון", [title, calc, sign, lin, exam, recap], bank={"25-S-Q9": 0})

# -*- coding: utf-8 -*-
"""E02 · פיזור וסטיית תקן — video script (build: tools/video/vid.py E02).

Source: courses/eda/E02.js (lesson + goal: compute the standard deviation, unbiased (n-1) and population (n), step by
step; what it measures; how it reacts to a shift and to a scaling).
Exam anchor: 24A-A-Q20 (which of standard deviation / median / mean / quartile measures spread). No guided quiz uses
it. Not used on purpose: every E02 quiz item (2,6,10 / 1,3,5,7 / 48,50,52 vs 40,50,60 / 5,5,9,9 / "+100 then x2"),
the lesson's 3,5,7 and 20,50,80, and the boss item 25-S-Q8 (the s of 4,8,6,5,3 is never computed here).
Worked example: 12, 4, 14, 8, 12 (mean 10, sum of squared deviations 64, s = 4, population 3.58), against
9, 10, 11, 10, 10 (same mean, s = 0.71); a shift by +5 and a scaling by 3 shown separately.
Every number below is computed with numpy and asserted.
"""
import math

import numpy as np

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_eda as w

# ---------------------------------------------------------------- data (verified)
A = [12, 4, 14, 8, 12]
a = np.array(A, float)
assert a.mean() == 10
dev = a - a.mean()
assert list(dev) == [2, -6, 4, -2, 2] and dev.sum() == 0          # deviations always sum to 0
sq = dev ** 2
assert list(sq) == [4, 36, 16, 4, 4] and sq.sum() == 64
assert sq.sum() / 4 == 16 and np.var(a, ddof=1) == 16 and np.std(a, ddof=1) == 4
assert sq.sum() / 5 == 12.8 and round(np.std(a), 2) == 3.58 and abs(np.std(a) - math.sqrt(12.8)) < 1e-12

B = [9, 10, 11, 10, 10]
b = np.array(B, float)
assert b.mean() == 10 and ((b - 10) ** 2).sum() == 2 and round(np.std(b, ddof=1), 2) == 0.71

assert np.std(a + 5, ddof=1) == 4 and (a + 5).mean() == 15             # shift: spread unchanged
assert abs(np.std(3 * a, ddof=1) - 12) < 1e-12 and (3 * a).mean() == 30  # scale by 3: s times 3
assert abs(np.std(-3 * a, ddof=1) - 12) < 1e-12                          # |c|

# exam 24A-A-Q20
Q = BANK["24A-A-Q20"]
assert Q["correctIndex"] == 0 and Q["options"] == ["סטיית תקן", "חציון", "ממוצע", "רבעון"]
OPTS = list(enumerate(Q["options"]))
Sb = w.stats(B + [7, 13])                       # exam scene: two sets with the same mean/median, different spread
Sa = w.stats([4, 10, 16, 10, 10, -2, 22])
assert Sa["mean"] == Sb["mean"] == 10 and Sa["median"] == Sb["median"] == 10
assert round(Sb["s"], 2) == 1.83 and round(Sa["s"], 2) == 7.75

# ---------------------------------------------------------------- figures
NA = w.NumLine("na", 0, 16, [0, 2, 4, 6, 8, 10, 12, 14, 16], w=900, h=210, dot=13)
NA.dots("na-d", A, kind="a", hidden=False)
NA.mark("na-m", 10, "ממוצע 10", kind="b")
NB = w.NumLine("nb", 0, 16, [0, 2, 4, 6, 8, 10, 12, 14, 16], w=900, h=210, dot=13)
NB.dots("nb-d", B, kind="ok", hidden=False)
NB.mark("nb-m", 10, "ממוצע 10", kind="b")

ROWS = [[w.fmt(x), w.fmt(d), w.fmt(s)] for x, d, s in zip(a, dev, sq)]
ROWS = [[r[0], r[1].replace("-", "−"), r[2]] for r in ROWS]
TAB = w.table("t", ["$x$", "$x-\\bar{x}$", "$(x-\\bar{x})^2$"], ROWS + [["", "<b>0</b>", "<b>64</b>"]],
              hide={1, 2}, size=34)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נמדוד כמה הנתונים מפוזרים."),
    P("נחשב סטיית תקן צעד אחר צעד, בשתי הגרסאות שלה, ונראה איך היא מגיבה להזזה ולהכפלה."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">E02 · סטטיסטיקה וגרפים</div><h1>פיזור וסטיית תקן</h1>'
         '<p>לחשב סטיית תקן (מוטה ולא מוטה) צעד אחר צעד, ולדעת מה היא מודדת ואיך היא מגיבה להזזה ולהכפלה.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("הנה שתי קבוצות של חמישה ערכים. לשתיהן אותו ממוצע: 10.", do=show("i-a", "i-b")),
    P("אבל הכחולה מפוזרת על כל הציר, והירוקה צפופה סביב 10."),
    P("מדד מרכז לבדו לא מבחין ביניהן. צריך מדד **פיזור**.", do=show("i-c1"), hold=0.3),
    P("הרעיון של סטיית התקן: למדוד כמה רחוק, בממוצע, כל ערך נמצא מהממוצע.", do=show("i-c2")),
    P("נחשב אותה לקבוצה הכחולה, בארבעה צעדים.", hold=0.3),
], stage=f'<div class="ed-col"><div id="i-a" class="h">{NA.svg()}</div><div id="i-b" class="h">{NB.svg()}</div></div>',
   panel=st.card("i-c1", "plain", "כחולה: 12, 4, 14, 8, 12<br>ירוקה: 9, 10, 11, 10, 10")
         + st.card("i-c2", "rule", "🔑 סטיית תקן = מרחק טיפוסי של ערך <b>מהממוצע</b>"))

recipe = Scene("recipe", "המתכון", [
    P("צעד ראשון: הממוצע. הסכום הוא 50, וחלקי חמש זה 10.", do=show("p-1")),
    P("צעד שני: מחסרים את הממוצע מכל ערך. 12 פחות 10 זה 2.", do=show("t-r0c1")),
    P("4 פחות 10 זה מינוס 6. וכך הלאה: 4, מינוס 2, ו-2.", do=show("t-r1c1", "t-r2c1", "t-r3c1", "t-r4c1")),
    P("שימו לב: סכום הסטיות יוצא אפס. תמיד, בכל נתונים.", do=show("t-r5c1", "p-0")),
    P("החיוביות והשליליות מתקזזות, ולכן מעלים כל סטייה **בריבוע**.", hold=0.2),
    P("4, 36, 16, 4 ו-4. הסטייה של מינוס 6 תורמת הכי הרבה.", do=show("t-r0c2", "t-r1c2", "t-r2c2", "t-r3c2", "t-r4c2")),
    P("צעד שלישי: מסכמים את הריבועים, ומקבלים 64.", do=show("t-r5c2", "p-3")),
    P("ומחלקים. בסטיית תקן **לא מוטה** מחלקים ב-n פחות אחת: 64 חלקי 4 זה 16.", do=show("p-4"),
      say="ומחלקים. בסטיית תקן לא מוטה מחלקים באֶן פחות אחת: שישים וארבע חלקי ארבע זה שש עשרה."),
    P("ה-16 הזה נקרא **שונות**. אבל עוד לא סיימנו.", hold=0.2),
    P("צעד רביעי: שורש. שורש של 16 הוא 4. סטיית התקן היא 4.", do=show("p-5", "p-ok")),
], stage=f'<div class="ed-col">{TAB}'
         + w.eq("p-1", "$\\bar{x} = 50 \\div 5 = 10$", 36)
         + w.eq("p-4", "$s^2 = 64 \\div (5-1) = 16$", 36)
         + w.eq("p-5", "$s = \\sqrt{16} = 4$", 40) + "</div>",
   panel=st.card("p-0", "ex", "סכום הסטיות תמיד <b>0</b>, ולכן מעלים בריבוע")
         + st.card("p-3", "rule", "🔑 ① ממוצע ② סטיות בריבוע ③ סכום ÷ (n−1) ④ שורש")
         + w.chip("p-ok", "s = 4", "ok"))

two = Scene("two", "שתי גרסאות", [
    P("למה n פחות אחת? זו הגרסה שמתקנת הטיה, כשהנתונים הם מדגם. במבחן, ״לא מוטה״ פירושו לחלק ב-n פחות אחת.",
      do=show("v-1", "v-c1"),
      say="למה אֶן פחות אחת? זו הגרסה שמתקנת הטיה, כשהנתונים הם מדגם. במבחן, לא מוטה פירושו לחלק באֶן פחות אחת."),
    P("הגרסה השנייה, של אוכלוסייה, מחלקת ב-n: 64 חלקי 5 זה 12.8.", do=show("v-2", "v-c2"),
      say="הגרסה השנייה, של אוכלוסייה, מחלקת באֶן: שישים וארבע חלקי חמש זה שתים עשרה נקודה שמונה."),
    P("ושורש של 12.8 הוא בערך 3.58. קצת פחות מ-4, כי חילקנו במספר גדול יותר.", do=show("v-3"),
      say="ושורש של שתים עשרה נקודה שמונה הוא בערך שלוש נקודה חמש שמונה. קצת פחות מארבע, כי חילקנו במספר גדול יותר."),
    P("ועכשיו הקבוצה הירוקה. כאן סכום ריבועי הסטיות הוא רק 2.", do=show("v-4"),
      say="ועכשיו הקבוצה הירוקה. כאן סכום ריבועי הסטיות הוא רק שתיים."),
    P("שתיים חלקי ארבע, ושורש: סטיית תקן של בערך 0.71. קטנה בערך פי חמש וחצי מזו של הכחולה.", do=show("v-5"),
      say="שתיים חלקי ארבע, ושורש: סטיית תקן של בערך אפס נקודה שבעים ואחת. קטנה בערך פי חמש וחצי מזו של הכחולה."),
    P("וזו בדיוק התמונה שראינו: אותו ממוצע, פיזור שונה לגמרי.", hold=0.3),
    P("ומלכודת חשובה: שונות היא סטיית התקן **בריבוע**. בשאלה על סטיית תקן, אל תעצרו לפני השורש.",
      do=show("v-trap"), hold=0.4),
], stage='<div class="ed-col">'
         + w.eq("v-1", "$s = \\sqrt{\\dfrac{\\sum (x-\\bar{x})^2}{n-1}} = \\sqrt{\\dfrac{64}{4}} = 4$", 40)
         + w.eq("v-2", "$\\sigma^2 = \\dfrac{64}{5} = 12.8$", 40)
         + w.eq("v-3", "$\\sigma = \\sqrt{12.8} \\approx 3.58$", 40)
         + w.eq("v-4", "$\\text{green: } \\sum (x-10)^2 = 1+0+1+0+0 = 2$", 36)
         + w.eq("v-5", "$s = \\sqrt{2 \\div 4} \\approx 0.71$", 40) + "</div>",
   panel=st.card("v-c1", "ex", "מדגם, ״לא מוטה״: חלקי $n-1$")
         + st.card("v-c2", "ex", "אוכלוסייה: חלקי $n$")
         + st.card("v-trap", "trap", "⚠️ שונות = $s^2$ (16), סטיית תקן = $s$ (4)"))

props = Scene("props", "הזזה והכפלה", [
    P("מה קורה לסטיית התקן אם מוסיפים 5 לכל הערכים?", do=show("h-1")),
    P("כל הנקודות זזות יחד חמש יחידות ימינה. הממוצע עולה ל-15, אבל המרחקים ביניהן לא משתנים.", do=show("h-2")),
    P("לכן סטיית התקן נשארת 4.", do=show("h-3", "h-r1"), hold=0.3),
    P("ואם מכפילים כל ערך בשלוש? עכשיו כל המרחקים נמתחים פי שלושה.", do=show("h-4")),
    P("ולכן גם סטיית התקן גדלה פי שלושה, ל-12.", do=show("h-5")),
    P("ובהכפלה במספר שלילי, היא מוכפלת בערך המוחלט שלו: סטיית תקן לעולם לא שלילית.", do=show("h-r2"), hold=0.4),
], stage='<div class="ed-col">'
         + w.eq("h-1", "$12,\\ 4,\\ 14,\\ 8,\\ 12 \\;\\xrightarrow{+5}\\; 17,\\ 9,\\ 19,\\ 13,\\ 17$", 38)
         + w.eq("h-2", "$\\bar{x}:\\ 10 \\to 15$", 38)
         + w.eq("h-3", "$s:\\ 4 \\to 4$", 42)
         + w.eq("h-4", "$12,\\ 4,\\ 14,\\ 8,\\ 12 \\;\\xrightarrow{\\times 3}\\; 36,\\ 12,\\ 42,\\ 24,\\ 36$", 38)
         + w.eq("h-5", "$s:\\ 4 \\to 12$", 42) + "</div>",
   panel=st.card("h-r1", "rule", "🔑 הוספת קבוע: הפיזור <b>לא</b> משתנה")
         + st.card("h-r2", "rule", "🔑 הכפלה ב-$c$: סטיית התקן גדלה פי $|c|$"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: איזה מבין המדדים הבאים משמש למדידת פיזור הנתונים?"),
    P("הנה שתי קבוצות של שבעה ערכים, עם אותו ממוצע ואותו חציון: 10.", do=show("x-a", "x-b")),
    P("ובכל זאת אחת צפופה והשנייה מפוזרת. לכן החציון והממוצע לא מודדים פיזור.", do=show("q-x-1", "q-n-1", "q-x-2", "q-n-2")),
    P("הם מדדי **מרכז**: הם אומרים איפה הנתונים, לא כמה הם מתפרשים.", hold=0.3),
    P("ורבעון? רבעון בודד הוא **מיקום**, נקודה אחת בנתונים.", do=show("q-x-3", "q-n-3")),
    P("פיזור מודדים ב**הפרש** בין הרבעונים, וזה מדד אחר, שנפגוש ברמה הבאה.", hold=0.3),
    P("סטיית התקן כן מבחינה בין הקבוצות: בערך 1.8 לצפופה, ובערך 7.7 למפוזרת.", do=show("x-s"),
      say="סטיית התקן כן מבחינה בין הקבוצות: בערך אחת נקודה שמונה לצפופה, ובערך שבע נקודה שבע למפוזרת."),
    P("לכן התשובה: סטיית תקן.", do=show("q-ok-0"), hold=0.6),
], stage=f'<div class="ed-col">'
         + f'<div id="x-a" class="h">{w.strip("xa", sorted(B + [7, 13]), label="צפופה")}</div>'
         + f'<div id="x-b" class="h">{w.strip("xb", sorted([4, 10, 16, 10, 10, -2, 22]), label="מפוזרת")}</div>'
         + w.eq("x-s", "$s \\approx 1.83 \\qquad s \\approx 7.75$", 40) + "</div>",
   panel=w.stem(Q["id"], "מבין המדדים הבאים, מהו מדד המשמש למדידת פיזור נתונים?")
         + st.options("q", OPTS, notes={1: "מדד מרכז", 2: "מדד מרכז", 3: "מיקום בודד"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: סטיית תקן מודדת כמה הערכים רחוקים מהממוצע.", do=show("r-1")),
    P("המתכון: ממוצע, סטיות בריבוע, סכום חלקי n פחות אחת, ושורש.", do=show("r-2"),
      say="המתכון: ממוצע, סטיות בריבוע, סכום חלקי אֶן פחות אחת, ושורש."),
    P("שונות היא לפני השורש. ובאוכלוסייה מחלקים ב-n.", do=show("r-3"),
      say="שונות היא לפני השורש. ובאוכלוסייה מחלקים באֶן."),
    P("הוספת קבוע לא משנה אותה, והכפלה ב-c מכפילה אותה בערך המוחלט של c. נתראה ברמה הבאה.", do=show("r-4"),
      say="הוספת קבוע לא משנה אותה, והכפלה בקבוע מכפילה אותה בערך המוחלט שלו. נתראה ברמה הבאה.", hold=0.6),
], stage='<div class="ed-col">'
         + w.eq("r-eq", "$s = \\sqrt{\\dfrac{\\sum (x_i-\\bar{x})^2}{n-1}}$", 52, hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 פיזור סביב הממוצע")
         + st.card("r-2", "rule", "🔑 לא מוטה: חלקי $n-1$, ואז שורש")
         + st.card("r-3", "trap", "⚠️ שונות = בלי שורש · אוכלוסייה: חלקי $n$")
         + st.card("r-4", "rule", "🔑 $+c$: ללא שינוי · $\\times c$: פי $|c|$"))

VIDEO = Video("E02", "eda", "פיזור וסטיית תקן", [title, idea, recipe, two, props, exam, recap],
              bank={"24A-A-Q20": 0})

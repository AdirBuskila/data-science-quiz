# -*- coding: utf-8 -*-
"""E08 · מבחן גמר: סטטיסטיקה וגרפים — boss walkthrough (build: tools/video/vid.py E08).

Source: courses/eda/E08.js (boss level). A walkthrough of three exam questions that no guided quiz uses (the boss
quiz uses 25-S-Q8, 24A-B-Q19, 25A-A-Q2, 26B-A-Q7, 26B-A-Q6, 25A-A-Q22; none of them, nor their numbers, appear here):
  24A-B-Q14  whis=5 in a box plot -> fewer outliers. Shown on new data (the E05 worked example: Q1 = 18, Q3 = 28,
             fences 3 / 43 with whis 1.5 -> 52 is an outlier; -32 / 78 with whis 5 -> none). Not the E05-Q4 numbers.
  24A-A-Q9   three scatter plots (blob, arch, U): every linear correlation is near zero. The original figure is shown;
             its reading is asserted by locating the green dots in each third (w_eda.raster_corr): r = 0.03, -0.11, 0.18.
  26A-B-Q8   df.describe (count, mean, std with n-1, min, 25%, 50%, 75%, max), computed with pandas on the E02 data
             12,4,14,8,12; pandas' 25% / 75% (8, 12) are interpolated and differ from the course quartiles (6, 13).
"""
import os

import numpy as np
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK, ROOT
from common import quartiles
import stage as st
import w_eda as w

# ---------------------------------------------------------------- 24A-B-Q14 (whis)
Q1 = BANK["24A-B-Q14"]
assert Q1["correctIndex"] == 0 and Q1["options"][0] == "נראה פחות נתונים חריגים בתרשים"
B = [24, 15, 31, 18, 52, 22, 27, 12, 25, 20, 30, 17, 23, 28, 21]
BX15, S15 = w.boxplot("ba", B, 0, 60, [0, 10, 20, 30, 40, 50, 60], whis=1.5, w=900, h=300)
BX5, S5 = w.boxplot("bb", B, 0, 60, [0, 10, 20, 30, 40, 50, 60], whis=5, w=900, h=300)
assert (S15["q1"], S15["q3"], S15["iqr"]) == (18, 28, 10) and (S15["flo"], S15["fhi"]) == (3, 43) and S15["out"] == [52]
assert (S5["flo"], S5["fhi"]) == (-32, 78) and S5["out"] == [] and (S5["wl"], S5["wr"]) == (12, 52)
assert (S5["q1"], S5["q3"]) == (S15["q1"], S15["q3"])                  # whis never moves the box
O1 = list(enumerate(Q1["options"]))

# ---------------------------------------------------------------- 24A-A-Q9 (the figure, read by machine)
Q2 = BANK["24A-A-Q9"]
assert Q2["correctIndex"] == 0 and Q2["image"] == "images/exams/24A-A-Q9.png"
assert Q2["options"][0] == "בכל הגרפים יש מתאם לינארי קרוב לאפס"
green = lambda R, G, Bc: (G > R + 30) & (G > Bc + 30)
(n1, r1), (n2, r2), (n3, r3) = w.raster_corr(os.path.join(ROOT, Q2["image"]), green, [(0, 290), (290, 580), (580, 829)])
assert max(abs(r1), abs(r2), abs(r3)) < 0.25 and min(n1, n2, n3) >= 15
assert (round(r1, 2), round(r2, 2), round(r3, 2)) == (0.03, -0.11, 0.18)
O2 = list(enumerate(Q2["options"]))
FIG = st.raster("fig", Q2["image"], 1000, (829, 199), tags=[("שמאלי", 150, 0), ("אמצעי", 440, 0), ("ימני", 720, 0)])

# ---------------------------------------------------------------- 26A-B-Q8 (describe)
Q3 = BANK["26A-B-Q8"]
assert Q3["correctIndex"] == 0 and Q3["options"] == ["df.describe", "df.summary", "df.stats", "df.info"]
ser = pd.Series([12, 4, 14, 8, 12])
d = ser.describe()
assert list(d.index) == ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
assert list(d.values) == [5, 10, 4, 4, 8, 12, 12, 14]
assert d["std"] == np.std(ser, ddof=1) == 4                                # pandas std divides by n - 1
assert quartiles(list(ser)) == (6, 12, 13)                                 # the course method gives other Q1 / Q3
assert not hasattr(pd.DataFrame, "summary") and not hasattr(pd.DataFrame, "stats") and hasattr(pd.DataFrame, "info")
O3 = list(enumerate(Q3["options"]))
DESC = w.table("ds", ["", "value"], [[k, w.fmt(v)] for k, v in d.items()], hide={1}, size=30, cls="tight")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הסיכום של הקורס: נפתור יחד שלוש שאלות אמיתיות ממבחנים."),
    P("שפמים של box plot, קריאת גרפי פיזור, ופקודה אחת של pandas שמחברת את כל המדדים.",
      say="שפמים של בּוֹקְס פְּלוֹט, קריאת גרפי פיזור, ופקודה אחת של פַּנְדָס שמחברת את כל המדדים."),
    P("בכל שאלה: קודם חושבים, ואחר כך פוסלים כל תשובה שגויה עם סיבה.", hold=0.4),
], stage='<div class="kicker">E08 · סטטיסטיקה וגרפים</div><h1>מבחן גמר: סטטיסטיקה וגרפים</h1>'
         '<p>שלוש שאלות ממבחנים קודמים: box plot, מתאם מגרפים, ו-describe.</p>', layout="title")

whis = Scene("whis", "שאלה 1: whis", [
    P("שאלה ראשונה: בקוד שמצייר box plot כתוב whis שווה 5. מה ההשפעה?", do=show("w-code"),
      say="שאלה ראשונה: בקוד שמצייר בּוֹקְס פְּלוֹט כתוב וִויס שווה חמש. מה ההשפעה?"),
    P("נזכור: הגדרות נמצאות במרחק של המכפיל כפול IQR מהקופסה, והפרמטר הזה הוא המכפיל. ברירת המחדל: אחת וחצי.", do=show("w-a")),
    P("נבדוק על חמישה עשר ערכים. הרבעונים 18 ו-28, ולכן IQR של 10. הגדרות: 3 ו-43, והערך 52 חריג.",
      do=show("ba-box", "ba-med", "ba-wl", "ba-wr", "ba-fl", "ba-fh", "ba-out")),
    P("עכשיו מכפיל 5: חמש כפול 10 זה 50. הגדרות: מינוס 32 ו-78.", do=hide("w-a") + show("w-b", "w-eq")),
    P("52 כבר בתוך הגדר. השפם הימני נמתח עד אליו, ואין אף נקודה חריגה.",
      do=show("bb-box", "bb-med", "bb-wl", "bb-wr")),
    P("לכן: נראה **פחות** נתונים חריגים. זו התשובה.", do=show("a-ok-0")),
    P("יותר חריגים? הפוך: מכפיל גדול מרחיק את הגדרות.", do=show("a-x-1", "a-n-1")),
    P("והקופסה לא זזה בכלל: היא תמיד מהרבעון הראשון עד השלישי. אין כאן חמישונים.", do=show("a-x-2", "a-n-2")),
    P("ורוחב הקופסה בציור נקבע בפרמטר אחר, לא במכפיל של השפמים.", do=show("a-x-3", "a-n-3"), hold=0.6),
], stage=('<div class="ed-col"><div id="w-code" class="ed-code h">sns.boxplot(x=data, <b>whis=5</b>)</div>'
          f'<div class="swap" style="--swap-h:300px"><div id="w-a" class="h">{BX15}</div><div id="w-b" class="h">{BX5}</div></div>'
          + w.eq("w-eq", "$[\\,18 - 5\\cdot 10,\\ \\ 28 + 5\\cdot 10\\,] = [-32,\\ 78]$", 36) + "</div>"),
   panel='<div class="ed-small">' + w.stem(Q1["id"], "מה ההשפעה של <b>whis=5</b> בקוד שמצייר box plot?")
         + st.options("a", O1, notes={1: "הפוך", 2: "הקופסה לא משתנה", 3: "פרמטר אחר"}) + "</div>")

corr = Scene("corr", "שאלה 2: מתאם", [
    P("שאלה שנייה: מה ניתן לומר על המתאם בכל אחד משלושת הגרפים?", do=show("c-fig")),
    P("בגרף השמאלי, ענן בלי כיוון: מתאם קרוב לאפס.", do=show("c-l")),
    P("בגרף האמצעי, קשת: הנקודות עולות ואחר כך יורדות. בגרף הימני, צורת יו: יורדות ואחר כך עולות.", do=show("c-m")),
    P("בשני המקרים, החצי שעולה והחצי שיורד מתקזזים. מתאם פירסון מודד רק קו ישר.", do=show("c-why")),
    P("מדדנו את הנקודות בתמונה עצמה: המתאם בערך אפס, מינוס 0.11 ו-0.18. כולם קרובים לאפס.", do=show("c-eq"),
      say="מדדנו את הנקודות בתמונה עצמה: המתאם בערך אפס, מינוס אפס נקודה אחת אחת, ואפס נקודה אחת שמונה. כולם קרובים לאפס."),
    P("לכן: בכל הגרפים יש מתאם לינארי קרוב לאפס, למרות שבשניים יש תבנית ברורה.", do=show("b-ok-0")),
    P("שתי התשובות שמייחסות לגרף הימני ולאמצעי מתאם חיובי או שלילי, טועות: אין שם מגמה של קו.",
      do=show("b-x-1", "b-n-1", "b-x-2", "b-n-2")),
    P("והאחרונה מדברת על מתאם ״פרבולי״ ו״רדיאלי״. אבל פירסון מודד רק קשר לינארי, ובשלושתם הוא קרוב לאפס.", do=show("b-x-3", "b-n-3"), hold=0.6),
], stage=(f'<div class="ed-col"><div id="c-fig" class="h">{FIG}</div><div class="ed-rowc" style="font-size:30px">'
          + w.chip("c-l", "שמאלי: ענן", "warn") + w.chip("c-m", "אמצעי: קשת · ימני: יו", "info") + "</div>"
          + w.eq("c-eq", "$r \\approx 0.03,\\quad -0.11,\\quad 0.18$", 36)
          + st.card("c-why", "trap", "⚠️ תבנית לא ישרה יכולה לתת $r \\approx 0$") + "</div>"),
   panel='<div class="ed-small">' + w.stem(Q2["id"], "מה ניתן לומר על המתאם בין X1 ו-X2 בכל אחד מהתרשימים?")
         + st.options("b", O2, notes={1: "אין מגמה", 2: "אין מגמה", 3: "r רק לינארי"}) + "</div>")

desc = Scene("desc", "שאלה 3: describe", [
    P("שאלה שלישית: איזו מתודה ב-pandas מחשבת סטטיסטיקות תיאוריות לכל העמודות הנומריות?",
      say="שאלה שלישית: איזו מתודה בפַּנְדָס מחשבת סטטיסטיקות תיאוריות לכל העמודות הנומריות?"),
    P("התשובה: describe. נריץ אותה על הנתונים 12, 4, 14, 8, 12.", do=show("d-code", "c-ok-0"),
      say="התשובה: דִּיסְקְרַייבּ. נריץ אותה על הנתונים שתים עשרה, ארבע, ארבע עשרה, שמונה, שתים עשרה."),
    P("היא מחזירה כמות וממוצע: 5 ערכים, ממוצע 10.", do=show("ds-r0c1", "ds-r1c1")),
    P("ואז סטיית תקן: 4. שימו לב, היא מחולקת ב-n פחות אחת, כמו שחישבנו ביד.", do=show("ds-r2c1", "d-c1"),
      say="ואז סטיית תקן: ארבע. שימו לב, היא מחולקת באֶן פחות אחת, כמו שחישבנו ביד."),
    P("ואחריה מינימום, שלושה אחוזונים, ומקסימום. האחוזון החמישים הוא החציון: 12.",
      do=show("ds-r3c1", "ds-r4c1", "ds-r5c1", "ds-r6c1", "ds-r7c1")),
    P("ושימו לב: הרבעונים של pandas, 8 ו-12, מחושבים באינטרפולציה. בשיטת הקורס יוצא 6 ו-13.", do=show("d-trap"),
      say="ושימו לב: הרבעונים של פַּנְדָס, שמונה ושתים עשרה, מחושבים באינטרפולציה. בשיטת הקורס יוצא שש ושלוש עשרה."),
    P("ושאר התשובות? info מציגה סוגי עמודות וכמה ערכים לא חסרים, בלי ממוצע ובלי סטיית תקן.", do=show("c-x-3", "c-n-3"),
      say="ושאר התשובות? אִינְפוֹ מציגה סוגי עמודות וכמה ערכים לא חסרים, בלי ממוצע ובלי סטיית תקן."),
    P("ו-summary ו-stats בכלל לא קיימות כמתודות של טבלה ב-pandas.", do=show("c-x-1", "c-n-1", "c-x-2", "c-n-2"),
      say="וסַאמֶרִי וסְטַאטְס בכלל לא קיימות כמתודות של טבלה בפַּנְדָס.", hold=0.6),
], stage=('<div class="ed-rowc"><div class="ed-col" style="width:auto">'
          '<div id="d-code" class="ed-code h">pd.Series([12, 4, 14, 8, 12]).<b>describe()</b></div>'
          f'{DESC}</div></div>'),
   panel='<div class="ed-small">' + w.stem(Q3["id"], "איזו מתודה ב-Pandas מחשבת סטטיסטיקות תיאוריות (ממוצע, סטיית תקן, חציונים) לכל העמודות הנומריות?")
         + st.options("c", O3, notes={1: "לא קיימת", 2: "לא קיימת", 3: "בלי סטטיסטיקות"})
         + st.card("d-c1", "ex", "std של pandas: חלקי $n-1$")
         + st.card("d-trap", "trap", "⚠️ 25%/75% של pandas ≠ $Q_1$/$Q_3$ של הקורס") + "</div>")

recap = Scene("recap", "סיכום", [
    P("לסיכום השאלות: מכפיל שפמים גדול מרחיק את הגדרות, ולכן פחות חריגים. הקופסה לא זזה.", do=show("r-1")),
    P("מתאם קרוב לאפס לא אומר שאין תבנית: קשת וצורת יו נותנות אפס.", do=show("r-2")),
    P("ו-describe נותנת את כל המדדים בבת אחת, עם סטיית תקן לא מוטה.", do=show("r-3"),
      say="ודִּיסְקְרַייבּ נותנת את כל המדדים בבת אחת, עם סטיית תקן לא מוטה."),
    P("עכשיו תורכם: שש שאלות מבחן מחכות לכם ברמה הזו. בהצלחה!", do=show("r-4"), hold=0.6),
], stage='<div class="ed-col">' + w.eq("r-eq", "$\\text{fences} = [\\,Q_1 - k\\cdot\\mathrm{IQR},\\ \\ Q_3 + k\\cdot\\mathrm{IQR}\\,]$", 40,
                                         hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 whis גדול ← פחות חריגים")
         + st.card("r-2", "trap", "⚠️ $r \\approx 0$ ≠ אין קשר")
         + st.card("r-3", "rule", "🔑 describe: count, mean, std, min, 25%, 50%, 75%, max")
         + st.card("r-4", "plain", "🏆 ועכשיו, שש שאלות מבחן"))

VIDEO = Video("E08", "eda", "מבחן גמר: סטטיסטיקה וגרפים", [title, whis, corr, desc, recap],
              bank={"24A-B-Q14": 0, "24A-A-Q9": 0, "26A-B-Q8": 0})

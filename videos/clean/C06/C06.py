# -*- coding: utf-8 -*-
"""C06 · חריגים בקוד pandas — video script (build: tools/video/vid.py C06).

Source: courses/clean/C06.js (lesson + goal: read and write code that computes the IQR, filters outliers by the
fences or by z-score, and decide what to do with them). Exam anchor: 26A-A-Q9 (which statement about outliers is
NOT true: "an outlier is an erroneous value that requires treatment"), which no guided quiz uses.
Avoided on purpose: the C06 quiz data (10, 12, 12, 13, 14, 15, 16, 18, 45 and the 20 measurements around 50 with
120), the pie-chart question (C06-Q5, P-24), 25-S-Q25 (the IQR code itself: a content twin of C06-Q2), its relatives
P-25 / 26A-B-Q21 (1.5 vs 2 IQR, the C07 boss item) and P-26 (a twin of the anchor). The series of items per order
2, 6, 6, 7, 8, 9, 11, 11, 25 is mine; pandas' interpolated quartiles agree here with the course's quartile rule
(common.quartiles), and every printed line on screen comes from running the code that is shown. The fences come
from describe() (not the quantile / iqr lines of C06-Q1), the filter is ~s.between(low, high) and the or-vs-and point
is made in words only (C06-Q2), and the decide scene shows the effect on the std, not the new mean (C06-Q4).
"""
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
from common import quartiles                       # course checker (SIM_PATHS)
import stage as st
import w_clean as w

# ---------------------------------------------------------------- IQR in code (run)
IQR_SRC = ("s = pd.Series([2, 6, 6, 7, 8, 9, 11, 11, 25])\n"
           "d = s.describe()\n"
           "low = d['25%'] - 1.5 * (d['75%'] - d['25%'])\n"
           "high = d['75%'] + 1.5 * (d['75%'] - d['25%'])\n"
           "print(d['25%'], d['75%'], low, high)")
env, IQR_OUT = w.run(IQR_SRC)
s = env["s"]
assert IQR_OUT == "6.0 11.0 -1.5 18.5"
cq1, _, cq3 = quartiles(list(s))
assert (cq1, cq3) == (env["d"]["25%"], env["d"]["75%"]) == (6, 11)     # same quartiles by the course's rule
OUT_SRC = "print(s[~s.between(low, high)].tolist())"
_, OUT_OUT = w.run(OUT_SRC, env)
assert OUT_OUT == "[25]"
assert ((s < env["low"]) | (s > env["high"])).equals(~s.between(env["low"], env["high"]))   # outside = below OR above
assert not ((s < env["low"]) & (s > env["high"])).any()                                     # below AND above: impossible

# z-score: the same 25 is only 2.41 standard deviations above the mean, so |z| > 3 flags nothing.
# With n values and the sample std, |z| <= (n - 1) / sqrt(n): for n = 9 that is 8/3 ≈ 2.67 < 3.
Z_SRC = "z = (s - s.mean()) / s.std()\nprint(round(z.iloc[-1], 2))\nprint(s[z.abs() > 3].tolist())"
env, Z_OUT = w.run(Z_SRC, env)
assert Z_OUT == "2.41\n[]"
n = len(s)
BOUND = (n - 1) / n ** 0.5
assert n == 9 and round(BOUND, 2) == 2.67 and env["z"].abs().max() <= BOUND
import numpy as np
rng = np.random.default_rng(0)
for _ in range(2000):                                  # the bound holds for any 9 numbers
    v = pd.Series(rng.standard_cauchy(9))
    assert ((v - v.mean()) / v.std()).abs().max() <= BOUND + 1e-9
STD_SRC = "print(round(s.std(), 2), round(s[s != 25].std(), 2))"
_, STD_OUT = w.run(STD_SRC, env)
assert STD_OUT == "6.46 2.98"

# ---------------------------------------------------------------- exam 26A-A-Q9
Q = BANK["26A-A-Q9"]
assert Q["correctIndex"] == 0 and Q["options"][0] == "ערך חריג הינו ערך שגוי ודורש טיפול"
OPTS = list(enumerate(Q["options"]))

VALS = s.tolist()
NL = w.numline("nl", VALS, -5, 27, [0, 5, 10, 15, 20, 25], fences=(-1.5, 18.5), box=(6, 11), w=940, h=270, hidden=True)
NLF = w.numline("nf", VALS, -5, 27, [0, 5, 10, 15, 20, 25], fences=(-1.5, 18.5), w=900, h=250).replace(
    'id="nf-f0" class="h"', 'id="nf-f0"').replace('id="nf-f1" class="h"', 'id="nf-f1"')
NLX = w.numline("nx", VALS, -5, 27, [0, 5, 10, 15, 20, 25], fences=(-1.5, 18.5), box=(6, 11), w=900, h=250, hidden=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכתוב בקוד את שיטת ה-IQR לאיתור חריגים, ונקרא כל שורה."),
    P("נשווה אותה לשיטת ציון z, ונחליט מה עושים עם חריג אחרי שמצאנו אותו."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">C06 · ניקוי נתונים וסולמות</div><h1>חריגים בקוד pandas</h1>'
         '<p>לכתוב ולקרוא קוד שמחשב IQR, מסנן חריגים לפי גדרות או z-score, ולהחליט מה לעשות איתם.</p>', layout="title")

iqr = Scene("iqr", "IQR בקוד", [
    P("לפנינו מספר הפריטים בתשע הזמנות בחנות.", do=show("iq-l0", "nl")),
    P("שורה שתיים: describe מחזיר סיכום, ובו גם הרבעונים: עשרים וחמישה אחוז, ושבעים וחמישה אחוז.",
      do=show("iq-l1", "nl-box"),
      say="שורה שתיים: דִיסְקְרַייבּ מחזיר סיכום, ובו גם הרבעונים: עשרים וחמישה אחוז, ושבעים וחמישה אחוז."),
    P("הרבעון הראשון שש, והשלישי אחת עשרה. ההפרש ביניהם, חמש, הוא ה-IQR: רוחב הקופסה."),
    P("שורות שלוש וארבע: הגדרות. אחת וחצי IQR מתחת לרבעון הראשון, ואחת וחצי IQR מעל השלישי.", do=show("iq-l2", "iq-l3"),
      say="שורות שלוש וארבע: הגדרות. אחת וחצי אַיי קְיוּ אָר מתחת לרבעון הראשון, ואחת וחצי אַיי קְיוּ אָר מעל השלישי."),
    P("שש פחות שבע וחצי זה מינוס אחת וחצי. ואחת עשרה ועוד שבע וחצי זה שמונה עשרה וחצי.",
      do=show("iq-l4", "iq-out", "nl-f0", "nl-f1")),
    P("כל ערך מחוץ לגדרות הוא חריג. כאן רק אחד: עשרים וחמש.", do=show("nl-o8")),
    P("ובנתונים האלה, pandas והשיטה של הקורס נותנות את אותם רבעונים. זה לא תמיד כך.", do=show("iq-c1"),
      say="ובנתונים האלה, פַּנְדָס והשיטה של הקורס נותנות את אותם רבעונים. זה לא תמיד כך.", hold=0.3),
], stage=w.stack(w.code("iq", IQR_SRC, size=26, lines_hidden=True), w.out("iq-out", IQR_OUT, size=28), NL, gap=18),
   panel=st.card("iq-c1", "trap", "⚠️ pandas מחשב רבעונים באינטרפולציה. בחישוב ידני: לפי שיטת הקורס"))

filt = Scene("filter", "הסינון", [
    P("עכשיו מסננים. בתוך הסוגריים המרובעים שמים תנאי, ומקבלים רק את הערכים שמקיימים אותו.", do=show("f-code")),
    P("between בודק אם ערך נמצא **בין** הגדרות, כולל הגדרות עצמן.", do=show("f-c1"),
      say="בִּיטְוִוין בודק אם ערך נמצא בין הגדרות, כולל הגדרות עצמן."),
    P("והגל שלפניו הופך את התנאי: לא בין הגדרות. כלומר מחוץ להן.", do=show("f-c2")),
    P("התוצאה: רשימה עם ערך אחד, עשרים וחמש.", do=show("f-out")),
    P("ובמילים: חריג הוא ערך שקטן מהגדר התחתונה, **או** גדול מהעליונה. אחד משני הצדדים מספיק."),
    P("״וגם״ לא יכול להתקיים: אף מספר אינו גם קטן ממינוס אחת וחצי וגם גדול משמונה עשרה וחצי.", do=show("f-c3"),
      hold=0.3),
], stage=w.stack(w.code("f-code", OUT_SRC, hidden=True, size=30), w.out("f-out", OUT_OUT, size=30), NLF, gap=26),
   panel=st.card("f-c1", "rule", "🔑 " + w.mono("s.between(low, high)") + " ← בין הגדרות")
         + st.card("f-c2", "rule", "🔑 " + w.mono("~") + " ← ״לא״: מחוץ לגדרות")
         + st.card("f-c3", "trap", "⚠️ חריג: מתחת <b>או</b> מעל. לא ״וגם״"))

zsc = Scene("zscore", "ציון z", [
    P("שיטה שנייה: ציון z. כמה סטיות תקן הערך רחוק מהממוצע.", do=show("z-code")),
    P("את הממוצע מחסרים, ובסטיית התקן מחלקים. חריג הוא מי שהערך המוחלט של ה-z שלו גדול משלוש.", do=show("z-c1"),
      say="את הממוצע מחסרים, ובסטיית התקן מחלקים. חריג הוא מי שהערך המוחלט של הזֶד שלו גדול משלוש."),
    P("ומה יוצא לעשרים וחמש? בערך 2.41. פחות משלוש. לפי השיטה הזו, אין כאן חריג בכלל.", do=show("z-out"),
      say="ומה יוצא לעשרים וחמש? בערך שתיים נקודה ארבעים ואחת. פחות משלוש. לפי השיטה הזו, אין כאן חריג בכלל."),
    P("אותו ערך, שתי שיטות, ושתי תשובות שונות. אין הגדרה אחת ויחידה לחריג.", do=show("z-c2")),
    P("ולמה? החריג עצמו מנפח את סטיית התקן. ובתשעה ערכים, z לא יכול לעבור 2.67 בכלל.", do=show("z-c3"), hold=0.3,
      say="ולמה? החריג עצמו מנפח את סטיית התקן. ובתשעה ערכים, זֶד לא יכול לעבור שתיים נקודה שישים ושבע בכלל."),
], stage=w.stack(w.code("z-code", Z_SRC, hidden=True, size=28), w.out("z-out", Z_OUT, size=30), gap=26),
   panel=st.card("z-c1", "rule", "🔑 " + w.mono("|z| > 3") + " (גדול משלוש) ← חריג לפי ציון z")
         + st.card("z-c2", "trap", "⚠️ IQR: 25 חריג · ציון z: אף אחד")
         + st.card("z-c3", "ex", "9 ערכים ← " + w.mono("|z| ≤ 8/√9 ≈ 2.67")))

decide = Scene("decide", "ומה עושים איתו", [
    P("מצאנו חריג. האם מוחקים אותו? קודם בודקים מה הוא."),
    P("אם זו שגיאת הקלדה, למשל שתיים וחמש שהפכו לעשרים וחמש, מתקנים או מוחקים.", do=show("d-c1")),
    P("אבל אולי זו באמת הזמנה גדולה של לקוח עסקי. אז זה ערך **אמיתי**, ומחיקה שלו מעוותת את התמונה.", do=show("d-c2")),
    P("וכדאי לדעת כמה הוא משפיע: סטיית התקן עם עשרים וחמש היא 6.46, ובלעדיו 2.98. יותר מפי שניים.",
      do=show("d-code", "d-out"),
      say="וכדאי לדעת כמה הוא משפיע: סטיית התקן עם עשרים וחמש היא שש נקודה ארבעים ושש, ובלעדיו שתיים נקודה תשעים ושמונה. יותר מפי שניים."),
    P("ערך אחד מתוך תשעה משנה את תמונת הפיזור כולה. לכן מחליטים עליו בזהירות.", do=show("d-c3"), hold=0.3),
], stage=w.stack(w.code("d-code", STD_SRC, hidden=True, size=28), w.out("d-out", STD_OUT, size=30), gap=26),
   panel=st.card("d-c1", "ex", "שגיאה ← מתקנים או מוחקים")
         + st.card("d-c2", "ex", "ערך אמיתי ← משאירים, אולי מטפלים בנפרד")
         + st.card("d-c3", "rule", "🔑 חריג ≠ שגוי. קודם בודקים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: איזו טענה על ערכים חריגים **אינה** נכונה?"),
    P("בשאלת ״מה לא נכון״ עוברים על כל הטענות, ומחפשים את השגויה."),
    P("שיטת ה-IQR מזהה חריגים? כן, בדיוק עשינו את זה. הטענה נכונה, ולכן היא לא התשובה.", do=show("q-x-3", "q-n-3", "nx")),
    P("ויזואליזציה? כן: על ציר המספרים רואים את עשרים וחמש רחוק מכולם.", do=show("q-x-2", "q-n-2", "nx-o8")),
    P("ההגדרה אינה חד משמעית? נכון: IQR סימן חריג, וציון z לא סימן אף אחד.", do=show("q-x-1", "q-n-1")),
    P("ונשארה הטענה ״ערך חריג הוא ערך שגוי ודורש טיפול״. היא **לא נכונה**: חריג יכול להיות אמיתי.", do=show("q-ok-0")),
    P("וזו המלכודת: בשאלה הפוכה, התשובה היא הטענה השגויה, לא הנכונה.", do=show("x-t"), hold=0.5),
], stage=w.stack(NLX, st.card("x-t", "trap", "⚠️ ״מה לא נכון״: בוחרים את הטענה <b>השגויה</b>"), gap=40),
   panel=w.stem(Q["id"], "מה <b>לא</b> נכון מבין הטענות הבאות לגבי ערכים חריגים (Outliers)?")
         + st.options("q", OPTS, notes={1: "נכון", 2: "נכון", 3: "נכון"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: describe נותן רבעונים, ה-IQR הוא ההפרש, והגדרות במרחק אחת וחצי IQR מהקופסה.", do=show("r-1"),
      say="לסיכום: דִיסְקְרַייבּ נותן רבעונים, האַיי קְיוּ אָר הוא ההפרש, והגדרות במרחק אחת וחצי אַיי קְיוּ אָר מהקופסה."),
    P("חריג הוא מה שמחוץ לגדרות: מתחת לתחתונה, או מעל העליונה.", do=show("r-2")),
    P("ציון z יכול לתת תשובה אחרת, וחריג הוא לא בהכרח שגיאה. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.code("rc", OUT_SRC, size=30),
   panel=st.card("r-1", "rule", "🔑 IQR = רבעון שלישי פחות ראשון · גדרות ± 1.5·IQR")
         + st.card("r-2", "rule", "🔑 " + w.mono("~s.between(low, high)") + " ← מחוץ לגדרות")
         + st.card("r-3", "trap", "⚠️ חריג ≠ שגוי"))

SCENES = [title, iqr, filt, zsc, decide, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("C06", "clean", "חריגים בקוד pandas", SCENES, bank={"26A-A-Q9": 0})

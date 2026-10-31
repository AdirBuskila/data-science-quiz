# -*- coding: utf-8 -*-
"""C03 · מילוי ערכים חסרים — video script (build: tools/video/vid.py C03).

Source: courses/clean/C03.js (lesson + goal: choose what to fill with — median, mean, mode or a neighbouring value —
by the kind of column, and compute what comes out). Exam anchor: 25-S-Q19 (complete the code that fills a
DataFrame's NaN with the column means), which no guided quiz uses.
Avoided on purpose: every C03 quiz series (10/12/11/13/200, TLV/HFA/JLM, 4/NaN/8/NaN/6, the loc table, 20/NaN/NaN/23)
and the boss items 24A-A-Q18 (fill with median), its twin 24A-B-Q11 (mode), 25-S-Q24 (loc) and P-20. Worked
series are mine: rents 4, 5, 5, 6, 40 (median vs mean), colours (mode()[0], and a tie to show why [0]), daily
temperatures 30, 31, NaN, 29 (ffill / bfill). Every value and printed output on screen comes from running the code
that is shown; the four exam options are run too (one fills the cells with a method object, two raise).
"""
import warnings

import numpy as np
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_clean as w

# ---------------------------------------------------------------- worked examples (run)
RENT_SRC = "rent = pd.Series([4, 5, 5, 6, 40, np.nan])\nprint(rent.mean(), rent.median())"
env, RENT_OUT = w.run(RENT_SRC)
rent = env["rent"]
assert RENT_OUT == "12.0 5.0" and rent.dropna().sum() == 60 and rent.count() == 5
RENT_FILL = "rent = rent.fillna(rent.median())"
env2, _ = w.run(RENT_FILL, dict(env))
assert env2["rent"].tolist() == [4, 5, 5, 6, 40, 5]
assert (rent.dropna() < rent.mean()).sum() == 4          # four of the five known rents are below the mean

COL_SRC = "color = pd.Series(['red', 'blue', 'red', np.nan, 'green'])\nprint(color.mode()[0])"
envc, COL_OUT = w.run(COL_SRC)
assert COL_OUT == "red"
COL_FILL = "color = color.fillna(color.mode()[0])"
envc2, _ = w.run(COL_FILL, dict(envc))
assert envc2["color"].tolist() == ["red", "blue", "red", "red", "green"]
NOIDX_SRC = "print(color.fillna(color.mode()).tolist())"       # without [0]: fillna aligns on the index
_, NOIDX_OUT = w.run(NOIDX_SRC, dict(envc))
assert NOIDX_OUT == "['red', 'blue', 'red', nan, 'green']"           # index 3 stays NaN, silently, no error
TIE_SRC = "print(pd.Series(['tea', 'coffee', 'tea', 'coffee']).mode())"
_, TIE_OUT = w.run(TIE_SRC)
assert TIE_OUT.split() == ["0", "coffee", "1", "tea", "dtype:", "object"]

TEMP_SRC = "temp = pd.Series([30, 31, np.nan, 29])\nprint(temp.ffill().tolist())\nprint(temp.bfill().tolist())"
envt, TEMP_OUT = w.run(TEMP_SRC)
assert TEMP_OUT == "[30.0, 31.0, 31.0, 29.0]\n[30.0, 31.0, 29.0, 29.0]"

# ---------------------------------------------------------------- exam 25-S-Q19: run all four options
Q = BANK["25-S-Q19"]
assert Q["correctIndex"] == 2
MAKE = ("df = pd.DataFrame({\n    'A': [1, 2, np.nan, 4, 5],\n    'B': [3, np.nan, np.nan, 8, 9],\n"
        "    'C': [10, 11, 12, np.nan, 14]\n })")
assert MAKE in Q["question"]
RESULT = {}
for k, opt in enumerate(Q["options"]):
    e, _ = w.run(MAKE)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(opt, e)
        RESULT[k] = ("ok", e["df"])
    except Exception as ex:                              # noqa: BLE001
        RESULT[k] = (type(ex).__name__, str(ex))
e0, _ = w.run(MAKE)
DF = e0["df"]
MEANS = DF.mean()
assert MEANS["A"] == 3 and abs(MEANS["B"] - 20 / 3) < 1e-12 and MEANS["C"] == 11.75
good = RESULT[2][1]
assert RESULT[2][0] == "ok" and not good.isnull().any().any()
assert good.loc[2, "A"] == 3 and abs(good.loc[1, "B"] - 20 / 3) < 1e-12 and good.loc[3, "C"] == 11.75
bad0 = RESULT[0][1]
assert RESULT[0][0] == "ok" and callable(bad0.loc[2, "A"])           # to_dict without (): the method object itself
assert RESULT[1][0] == "ValueError" and "inplace" in RESULT[1][1]
assert str(bad0.loc[2, "A"]).startswith("<bound method Series.to_dict")
assert RESULT[3] == ("TypeError", "DataFrame.dropna() takes 1 positional argument but 2 positional arguments "
                                  "(and 1 keyword-only argument) were given")
BAD0_LINE = str(bad0.loc[2, "A"]).split("\n")[0]
assert BAD0_LINE == "<bound method Series.to_dict of A     3.000000"
OPTS = [(k, f'<span class="cl-mono" style="font-size:24px">{w.esc(o)}</span>') for k, o in enumerate(Q["options"])]

TR = w.frame("tr", rent.to_frame("rent"), after=env2["rent"].to_frame("rent"), size=30, cw=150)
TC = w.frame("tc", envc["color"].to_frame("color"), after=envc2["color"].to_frame("color"), size=30, cw=170)
TT = w.frame("tt", envt["temp"].to_frame("temp"), after=envt["temp"].ffill().to_frame("temp"), size=30, cw=150)
XNAN_ = None
XNAN = w.nan_cells(DF)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד למלא ערכים חסרים במקום למחוק אותם."),
    P("נבחר במה למלא לפי סוג העמודה: חציון, ממוצע, שכיח או ערך סמוך."),
    P("ובסוף נשלים קוד אמיתי ממבחן.", hold=0.4),
], stage='<div class="kicker">C03 · ניקוי נתונים וסולמות</div><h1>מילוי ערכים חסרים</h1>'
         '<p>לבחור במה למלא (חציון, ממוצע, שכיח או ערך סמוך) לפי סוג העמודה, ולחשב מה יתקבל.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("מחיקה של כל שורה עם חסר יכולה לזרוק חלק גדול מהנתונים."),
    P("האלטרנטיבה: fillna. היא **ממלאת** כל NaN בערך שאנחנו בוחרים.", do=show("i-0")),
    P("והשאלה היא רק במה למלא. התשובה תלויה בסוג העמודה.", do=show("i-1")),
    P("עמודה מספרית בלי חריגים: ממוצע. עמודה מספרית עם חריגים: חציון.", do=show("i-2", "i-3")),
    P("עמודה קטגורית, כמו צבע: שכיח. וסדרת זמן: הערך הסמוך.", do=show("i-4", "i-5"), hold=0.3),
    P("ולמה לא פשוט אפס? כי אפס הוא ערך אמיתי, ובעמודה של מספרים חיוביים הוא ימשוך את הממוצע למטה.", do=show("i-c")),
], stage=w.stack(
    w.big("i-0", "s.fillna(value)", size=46),
    f'<table class="cl-df h" id="i-1" dir="rtl" style="font-size:30px;font-family:\'Segoe UI\'">'
    '<thead><tr><th>סוג העמודה</th><th>ממלאים ב…</th></tr></thead><tbody>'
    '<tr id="i-2" class="h"><td>מספרית, בלי חריגים</td><td>ממוצע · <span class="cl-mono">mean()</span></td></tr>'
    '<tr id="i-3" class="h"><td>מספרית <b>עם חריגים</b></td><td>חציון · <span class="cl-mono">median()</span></td></tr>'
    '<tr id="i-4" class="h"><td>קטגורית</td><td>שכיח · <span class="cl-mono">mode()[0]</span></td></tr>'
    '<tr id="i-5" class="h"><td>סדרת זמן</td><td>ערך סמוך · <span class="cl-mono">ffill()</span></td></tr>'
    '</tbody></table>', gap=34),
   panel=st.card("i-c", "trap", "⚠️ 0 הוא לא ״אין מידע״. הוא ערך, והוא מעוות את הממוצע"))

median = Scene("median", "חציון מול ממוצע", [
    P("נתחיל בשכר דירה, באלפי שקלים: ארבע, חמש, חמש, שש, ארבעים, ועוד ערך חסר.", do=show("tr", "m-code")),
    P("ממוצע או חציון? נחשב את שניהם. pandas מחשבת אותם **רק מהערכים הקיימים**.", do=show("m-out"),
      say="ממוצע או חציון? נחשב את שניהם. פַּנְדָס מחשבת אותם רק מהערכים הקיימים."),
    P("הממוצע: שישים חלקי חמש, כלומר 12. החציון: הערך האמצעי אחרי מיון, חמש.", do=show("m-c1"),
      say="הממוצע: שישים חלקי חמש, כלומר שתים עשרה. החציון: הערך האמצעי אחרי מיון, חמש."),
    P("הממוצע גבוה מארבע מתוך חמש הדירות. הדירה של ארבעים, החריגה, משכה אותו למעלה.", do=show("tr-h-4-0")),
    P("החציון לא זז בגלל ערך קיצוני אחד. לכן כשיש חריגים, ממלאים בחציון.", do=show("m-c2")),
    P("וזו השורה שממלאת: fillna עם החציון. ה-NaN הופך לחמש.", do=show("m-fill", "tr-n-5-0"),
      say="וזו השורה שממלאת: פִיל אֶן אֵיי עם החציון. הנָאן הופך לחמש."),
    P("בלי חריגים, הממוצע והחציון קרובים, ושניהם בסדר. ממוצע הוא הבחירה הרגילה.", hold=0.3),
], stage=w.row(TR, w.stack(w.code("m-code", RENT_SRC, hidden=True, size=24), w.out("m-out", RENT_OUT, size=28),
                           w.code("m-fill", RENT_FILL, hidden=True, size=24), gap=22), gap=40),
   panel=st.card("m-c1", "ex", "ממוצע 12 · חציון 5")
         + st.card("m-c2", "rule", "🔑 יש חריגים? ממלאים ב<b>חציון</b>: הוא עמיד לערכים קיצוניים"))

mode = Scene("mode", "שכיח", [
    P("עכשיו עמודה של צבעים. אין ממוצע של אדום וכחול, ולכן ממלאים בשכיח.", do=show("tc", "c-code")),
    P("השכיח הוא אדום: הוא מופיע פעמיים, וכל צבע אחר פעם אחת.", do=show("c-out", "tc-h-0-0", "tc-h-2-0")),
    P("ולמה כתוב mode, ואחריו אפס בסוגריים מרובעים?", do=show("c-q"),
      say="ולמה כתוב מוֹד, ואחריו אפס בסוגריים מרובעים?"),
    P("כי mode מחזירה Series, ולא ערך אחד. כשיש תיקו, יש בה יותר מערך אחד.", do=show("c-tie", "c-tout"),
      say="כי מוֹד מחזירה סִירִיז, ולא ערך אחד. כשיש תיקו, יש בה יותר מערך אחד."),
    P("תה וקפה מופיעים פעמיים כל אחד, ומקבלים שניהם. אפס בסוגריים לוקח את הראשון.", do=show("c-c1")),
    P("בלי [0], fillna מיישרת לפי אינדקס, והחסר באינדקס 3 נשאר NaN בשקט, בלי שגיאה.", do=show("c-c2"),
      say="בלי האפס בסוגריים, פִיל אֶן אֵיי מיישרת לפי אינדקס, והחסר באינדקס שלוש נשאר נָאן בשקט, בלי שגיאה."),
    P("עם האפס בסוגריים, החסר הופך לאדום.", do=show("c-fill", "tc-n-3-0"), hold=0.3),
], stage=w.row(TC, w.stack(w.code("c-code", COL_SRC, hidden=True, size=22), w.out("c-out", COL_OUT, size=28),
                           w.code("c-tie", TIE_SRC, hidden=True, size=20), w.out("c-tout", TIE_OUT, size=24),
                           w.code("c-fill", COL_FILL, hidden=True, size=22), gap=16), gap=30),
   panel=st.card("c-q", "plain", "למה " + w.mono("mode()[0]") + "?")
         + st.card("c-c1", "rule", "🔑 " + w.mono("mode()") + " מחזירה Series. " + w.mono("[0]") + " = הערך הראשון")
         + w.out("c-c2", NOIDX_OUT, size=22, label=w.esc(NOIDX_SRC)))

ffill = Scene("ffill", "סדרת זמן", [
    P("והמקרה האחרון: סדרת זמן. טמפרטורה בכל יום: שלושים, שלושים ואחת, חסר, עשרים ותשע.", do=show("tt", "t-code")),
    P("ביום החסר, הניחוש הטוב ביותר הוא כנראה הערך של היום הסמוך, ולא ממוצע של כל החודש."),
    P("ffill, מילוי קדימה, מעתיק את הערך האחרון הידוע: שלושים ואחת.", do=show("t-out", "tt-n-2-0"),
      say="אֶף פִיל, מילוי קדימה, מעתיק את הערך האחרון הידוע: שלושים ואחת."),
    P("ו-bfill, מילוי אחורה, לוקח את הערך הבא: עשרים ותשע.", do=show("t-c1"),
      say="ובִּי פִיל, מילוי אחורה, לוקח את הערך הבא: עשרים ותשע."),
    P("זה עובד רק כשהסדר בטבלה הוא סדר בזמן. בטבלה רגילה, השורה הקודמת היא סתם שורה אחרת.", do=show("t-c2"), hold=0.3),
], stage=w.row(TT, w.stack(w.code("t-code", TEMP_SRC, hidden=True, size=24), w.out("t-out", TEMP_OUT, size=26), gap=22), gap=40),
   panel=st.card("t-c1", "ex", w.mono("ffill") + " ← 31 · " + w.mono("bfill") + " ← 29")
         + st.card("t-c2", "trap", "⚠️ ערך סמוך: רק כשהשורות מסודרות לפי זמן"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: השלימו את הקוד, כך שהחסרים בטבלה ימולאו.", do=show("tx")),
    P("האפשרות הנכונה: replace, שמחליף כל NaN בממוצע של העמודה שלו.", do=show("q-ok-2"),
      say="האפשרות הנכונה: רִיפְּלֵייס, שמחליף כל נָאן בממוצע של העמודה שלו."),
    P("df.mean() מחשב ממוצע לכל עמודה בנפרד, רק מהערכים הקיימים.", do=show("x-m"),
      say="דִי אֶף מִין מחשב ממוצע לכל עמודה בנפרד, רק מהערכים הקיימים."),
    P("בעמודה A: שלוש. בעמודה B: עשרים חלקי שלוש, בערך 6.67. ובעמודה C: 11.75.",
      do=show(*w.ids("tx", "n", XNAN)),
      say="בעמודה אֵיי: שלוש. בעמודה בִּי: עשרים חלקי שלוש, בערך שש נקודה שש שבע. ובעמודה סִי: אחת עשרה נקודה שבעים וחמש."),
    P("שאר האפשרויות? הרצנו את כולן. בראשונה חסרים סוגריים אחרי to_dict.", do=show("q-x-0", "q-n-0", "x-e0"),
      say="שאר האפשרויות? הרצנו את כולן. בראשונה חסרים סוגריים אחרי טוּ דִיקְט."),
    P("אין שגיאה, אבל התאים מתמלאים בפונקציה עצמה, לא במספרים. זו המלכודת הכי מסוכנת."),
    P("בשנייה inplace מקבל מחרוזת במקום ערך בוליאני, ו-pandas זורקת שגיאה.",
      do=show("q-x-1", "q-n-1", "x-e1") + hide("x-e0"),
      say="בשנייה, אִינְפְּלֵייס מקבל מחרוזת במקום ערך בוליאני, ופַּנְדָס זורקת שגיאה."),
    P("והאחרונה משתמשת ב-dropna, שמוחקת ולא ממלאת. וגם היא נכשלת בהרצה.",
      do=show("q-x-3", "q-n-3", "x-e3") + hide("x-e1"),
      say="והאחרונה משתמשת בדְרוֹפּ אֶן אֵיי, שמוחקת ולא ממלאת. וגם היא נכשלת בהרצה."),
    P("ושימו לב: בשתיים מהן השגיאה בזמן ריצה, ולא שגיאת תחביר. הקוד נראה תקין, ונופל רק כשמריצים.", hold=0.5),
], stage=w.stack(w.frame("tx", DF, after=good, size=26, cw=130, hidden=True),
                 w.code("x-m", "df.mean()  # A: 3,  B: 6.67,  C: 11.75", hidden=True, size=24),
                 w.swap(170,
                        w.out("x-e0", BAD0_LINE + "\n…", size=22, label="print(df.loc[2, 'A'])"),
                        w.out("x-e1", f"{RESULT[1][0]}: {RESULT[1][1]}".replace(", received", ",\nreceived"), size=22,
                              label="df.fillna(df.median(), inplace='True')"),
                        w.out("x-e3", f"{RESULT[3][0]}: {RESULT[3][1]}".replace(" but ", "\nbut ").replace(" (and", "\n(and"),
                              size=20, label="df.dropna(df.sum()/3, inplace = 'False')")),
                 gap=18),
   panel=w.stem(Q["id"], "השלימו את הקוד כך שהערכים החסרים ב-df ימולאו:")
         + st.options("q", OPTS, notes={0: "לא מספרים", 1: "שגיאה", 3: "שגיאה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: fillna ממלא, ובמה למלא תלוי בעמודה.", do=show("r-1")),
    P("מספרית: ממוצע, ועם חריגים חציון. קטגורית: שכיח, עם אפס בסוגריים מרובעים.", do=show("r-2"),
      say="מספרית: ממוצע, ועם חריגים חציון. קטגורית: שכיח, עם אפס בסוגריים מרובעים."),
    P("סדרת זמן: הערך הסמוך. וממוצע וחציון מחושבים תמיד רק מהערכים הקיימים. נתראה ברמה הבאה.", do=show("r-3"),
      hold=0.6),
], stage=w.stack(w.big("r-0", "s.fillna(s.median())", hidden=False, size=44), gap=20),
   panel=st.card("r-1", "rule", "🔑 " + w.mono("fillna") + " ממלא, " + w.mono("dropna") + " מוחק")
         + st.card("r-2", "rule", "🔑 חריגים ← חציון · קטגורי ← " + w.mono("mode()[0]"))
         + st.card("r-3", "rule", "🔑 סדרת זמן ← " + w.mono("ffill()")))

SCENES = [title, idea, median, mode, ffill, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("C03", "clean", "מילוי ערכים חסרים", SCENES, bank={"25-S-Q19": 2})

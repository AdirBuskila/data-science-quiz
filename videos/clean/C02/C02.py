# -*- coding: utf-8 -*-
"""C02 · איתור ערכים חסרים — video script (build: tools/video/vid.py C02).

Source: courses/clean/C02.js (lesson + goal: find and count missing values, what dropna does, the kind of
missingness). Exam anchor: 26B-A-Q11 (which command counts the missing values of every column), which no guided
quiz uses.
Avoided on purpose: the C02 quiz table (A, B, C with 4 rows) and its answers, the head() question (C02-Q5 and its
twin P-21), the income example of C02-Q4, and P-19 (the C07 video solves it). The worked DataFrame (id, age, city,
score) is my own; every table, count and printed output on screen is produced below by running the code that is
shown (w_clean.run), and the elimination of each exam option is run too (count_null raises, describe drops the
text column, info prints non-null counts).
"""
import io

import numpy as np
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_clean as w

# ---------------------------------------------------------------- data + code (verified by running it)
MAKE = ("df = pd.DataFrame({'id': [1, 2, 3, 4, 5],\n"
        "                   'age': [23, np.nan, 31, 27, np.nan],\n"
        "                   'city': ['Haifa', 'Eilat', np.nan, 'Eilat', 'Acre'],\n"
        "                   'score': [88, 92, 75, np.nan, 81]})")
env, _ = w.run(MAKE)
df = env["df"]
NANS = w.nan_cells(df)
assert NANS == [(1, 1), (2, 2), (3, 3), (4, 1)]

ISN = df.isnull()
assert ISN.values.sum() == 4

SUM_SRC = "print(df.isnull().sum())"
_, SUM_OUT = w.run(SUM_SRC, env)
assert df.isnull().sum().to_dict() == {"id": 0, "age": 2, "city": 1, "score": 1}
assert SUM_OUT.splitlines()[1].split() == ["age", "2"]

buf = io.StringIO()
df.info(buf=buf)
INFO_LINES = [l.rstrip() for l in buf.getvalue().splitlines() if l.strip()[:1].isdigit() and "non-null" in l]
assert len(INFO_LINES) == 4 and "3 non-null" in INFO_LINES[1] and "4 non-null" in INFO_LINES[2]
INFO_OUT = "\n".join(INFO_LINES)
assert len(df) - df["age"].count() == 2

DROP_SRC = "print(len(df.dropna()))"
_, DROP_OUT = w.run(DROP_SRC, env)
assert DROP_OUT == "1" and list(df.dropna().index) == [0]
DROPC_SRC = "print(list(df.dropna(axis=1).columns))"
_, DROPC_OUT = w.run(DROPC_SRC, env)
assert DROPC_OUT == "['id']"

# exam 26B-A-Q11: run every option
Q = BANK["26B-A-Q11"]
assert Q["correctIndex"] == 0 and Q["options"] == ["df.isnull().sum()", "df.count_null()", "df.describe()", "df.info()"]
try:
    df.count_null()
    raise AssertionError("count_null exists?")
except AttributeError as e:
    ERR = f"AttributeError: {e}"
assert ERR == "AttributeError: 'DataFrame' object has no attribute 'count_null'"
DESC = df.describe()
assert "city" not in DESC.columns and DESC.loc["count", "age"] == 3     # describe: non-null counts, numeric columns only
DESC_SRC = "print(df.describe().loc['count'])"
_, DESC_OUT = w.run(DESC_SRC, env)
assert DESC_OUT.splitlines()[:3] == ["id       5.0", "age      3.0", "score    4.0"] and "city" not in DESC_OUT
OPTS = [(i, w.mono(o)) for i, o in enumerate(Q["options"])]

# kinds of missingness (definitions of the lesson; examples are mine)
KINDS = [("MCAR", "אקראי לגמרי"), ("MAR", "תלוי במשתנה אחר שנמדד"), ("MNAR", "תלוי בערך החסר עצמו")]

T = w.frame("t", df, size=30, cw=120)
TI = w.frame("ti", ISN, size=26, cw=120, hidden=True)
TD = w.frame("td", df, size=30, cw=120)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד למצוא ערכים חסרים בטבלה, ולספור אותם."),
    P("נראה מה dropna מוחק, ונכיר שלושה סוגים של חוסר."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">C02 · ניקוי נתונים וסולמות</div><h1>איתור ערכים חסרים</h1>'
         '<p>למצוא ולספור ערכים חסרים ב-DataFrame, להבין מה dropna עושה, ולסווג את סוג החוסר.</p>', layout="title")

idea = Scene("idea", "NaN", [
    P("לפנינו טבלה קטנה של חמישה סטודנטים: מספר, גיל, עיר וציון.", do=show("t")),
    P("בחלק מהתאים כתוב NaN. זה הסימון של pandas לערך **חסר**.", do=show(*w.ids("t", "h", NANS))),
    P("ערך חסר הוא לא אפס ולא מחרוזת ריקה. פשוט אין שם מידע.", do=show("i-c1")),
    P("בטבלה של חמש שורות רואים אותם בעין. בטבלה של מאה אלף שורות, צריך פקודה.", do=show("i-c2"), hold=0.3),
], stage=T,
   panel=st.card("i-c1", "rule", "🔑 <span class=\"cl-mono\">NaN</span> = אין מידע. לא 0 ולא ריק")
         + st.card("i-c2", "ex", "בטבלה גדולה סופרים חסרים בקוד"))

isnull = Scene("isnull", "isnull ו-sum", [
    P("הפקודה הראשונה היא isnull(). היא מחזירה טבלה באותו גודל בדיוק.", do=show("s-c1", "ti")),
    P("בכל תא כתוב True אם הוא חסר, ו-False אם לא.", do=show(*w.ids("ti", "h", NANS))),
    P("עכשיו מוסיפים sum. פייתון סופר True כאחת ו-False כאפס.", do=show("s-c2"),
      say="עכשיו מוסיפים סָאם. פייתון סופר טְרוּ כאחת, ופוֹלְס כאפס."),
    P("והסכום נעשה לכל **עמודה** בנפרד: כמה חסרים יש בה.", do=show("s-out")),
    P("בעמודת הגיל שני חסרים, בעיר ובציון אחד, ובמספר הסטודנט אף אחד.", do=show("ti-hh-1")),
    P("שימו לב: isnull() לבד נותן טבלה. רק עם sum מקבלים מספרים.", hold=0.3,
      say="שימו לב: אִיז נָאל לבד נותן טבלה. רק עם סָאם מקבלים מספרים."),
    P("גם info עוזרת: היא מראה כמה ערכים **לא** חסרים יש בכל עמודה.", do=show("s-info"),
      say="גם אִינְפוֹ עוזרת: היא מראה כמה ערכים לא חסרים יש בכל עמודה."),
    P("בגיל שלושה ערכים מתוך חמש שורות, כלומר שניים חסרים. אבל את החיסור עושים לבד.", do=show("s-c3")),
], stage=w.stack(w.frame("t2", df, size=26, cw=120), TI, gap=22),
   panel=st.card("s-c1", "plain", w.mono("df.isnull()") + " ← טבלת True / False")
         + st.card("s-c2", "plain", w.mono("df.isnull().sum()") + " ← מספר לכל עמודה")
         + w.out("s-out", SUM_OUT, size=23)
         + w.out("s-info", INFO_OUT, size=22, label='<bdi dir="ltr" class="cl-mono">df.info()</bdi> · חלק מהפלט')
         + st.card("s-c3", "trap", "⚠️ info סופרת <b>קיימים</b>, לא חסרים"))

drop = Scene("dropna", "dropna", [
    P("מצאנו את החסרים. הפקודה dropna() **מוחקת** כל שורה שיש בה לפחות NaN אחד.", do=show("d-c1")),
    P("שורה 1: חסר גיל. נמחקת.", do=show(*w.row_strike("td", df, 1))),
    P("שורה 2: חסרה עיר. נמחקת.", do=show(*w.row_strike("td", df, 2))),
    P("שורה 3: חסר ציון. ושורה 4: שוב חסר גיל. שתיהן נמחקות.", do=show(*w.row_strike("td", df, 3), *w.row_strike("td", df, 4))),
    P("נשארה שורה אחת מתוך חמש. ארבעה ערכים חסרים מחקו שמונים אחוז מהנתונים.", do=show("d-out")),
    P("ועם axis שווה אחת, הפקודה מוחקת **עמודות** במקום שורות.", do=show("d-c2"),
      say="ועם אַקְסִיס שווה אחת, הפקודה מוחקת עמודות במקום שורות."),
    P("כל עמודה שיש בה חסר נעלמת. נשארת רק עמודת המספר, שהיא מלאה.", do=show("d-out2"), hold=0.3),
    P("לכן dropna היא כלי חד: לפני שמוחקים, בודקים כמה זה עולה.", do=show("d-c3")),
], stage=TD,
   panel=st.card("d-c1", "plain", w.mono("df.dropna()") + " ← מוחק <b>שורות</b> עם NaN")
         + w.out("d-out", DROP_OUT, size=26, label=w.esc(DROP_SRC))
         + st.card("d-c2", "plain", w.mono("df.dropna(axis=1)") + " ← מוחק <b>עמודות</b>")
         + w.out("d-out2", DROPC_OUT, size=26, label=w.esc(DROPC_SRC))
         + st.card("d-c3", "trap", "⚠️ 4 חסרים ← נשארה שורה אחת מתוך 5"))

kinds = Scene("kinds", "סוגי חוסר", [
    P("ולמה הערך חסר? יש שלושה סוגים, ולכל אחד שם."),
    P("MCAR: החוסר אקראי לגמרי. מבחנה נפלה במעבדה ונשברה, בלי קשר לשום דבר.", do=show("k-0"),
      say="אֶם סִי אֵיי אָר: החוסר אקראי לגמרי. מבחנה נפלה במעבדה ונשברה, בלי קשר לשום דבר."),
    P("MAR: החוסר תלוי במשתנה **אחר** שמדדנו. למשל, ציונים חסרים רק מכיתה אחת, שהמורה שלה שכחה לשלוח.",
      do=show("k-1"), say="אֶם אֵיי אָר: החוסר תלוי במשתנה אחר שמדדנו. למשל, ציונים חסרים רק מכיתה אחת, שהמורה שלה שכחה לשלוח."),
    P("את הכיתה אנחנו רואים בטבלה, ולכן אפשר להסביר את החוסר בעזרתה."),
    P("MNAR: החוסר תלוי **בערך החסר עצמו**. למשל, מי שנכשל במבחן לא מדווח על הציון שלו.", do=show("k-2"),
      say="אֶם אֶן אֵיי אָר: החוסר תלוי בערך החסר עצמו. למשל, מי שנכשל במבחן לא מדווח על הציון שלו."),
    P("וזה הסוג הקשה: מה שגורם לחוסר הוא בדיוק מה שלא רואים.", do=show("k-c"), hold=0.3),
], stage=w.stack(*[st.card(f"k-{i}", "ex", f'<b class="cl-mono">{a}</b> · {b}') for i, (a, b) in enumerate(KINDS)], gap=26),
   panel=st.card("k-c", "trap", "⚠️ MNAR: הסיבה לחוסר היא הערך שחסר"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: איזו פקודה תיתן את מספר הערכים החסרים בכל עמודה, בצורה המדויקת ביותר?"),
    P("זו בדיוק הפקודה שהרצנו: isnull ואחריה sum. מספר חסרים לכל עמודה.", do=show("q-ok-0", "x-o1"),
      say="זו בדיוק הפקודה שהרצנו: אִיז נָאל ואחריה סָאם. מספר חסרים לכל עמודה."),
    P("count_null נשמעת מתאימה, אבל אין פקודה כזו. pandas זורקת שגיאה.", do=show("q-x-1", "q-n-1", "x-o2"),
      say="קָאוּנְט נָאל נשמעת מתאימה, אבל אין פקודה כזו. פַּנְדָס זורקת שגיאה."),
    P("describe מראה count, כלומר ערכים **קיימים**. וגם מדלגת על עמודת העיר, כי היא טקסט.",
      do=show("q-x-2", "q-n-2", "x-o3"),
      say="דִיסְקְרַייבּ מראה קָאוּנְט, כלומר ערכים קיימים. וגם מדלגת על עמודת העיר, כי היא טקסט."),
    P("ו-info מראה ערכים לא חסרים. אפשר להסיק ממנה, אבל צריך לחסר לבד.", do=show("q-x-3", "q-n-3"),
      say="ואִינְפוֹ מראה ערכים לא חסרים. אפשר להסיק ממנה, אבל צריך לחסר לבד."),
    P("המלכודת: count סופר את מה שיש, לא את מה שחסר.", do=show("x-t"), hold=0.5,
      say="המלכודת: קָאוּנְט סופר את מה שיש, לא את מה שחסר."),
], stage=w.stack(
    w.out("x-o1", SUM_OUT, size=26, label="df.isnull().sum()"),
    w.out("x-o2", ERR.replace(" has no ", " has no\n"), size=24, label="df.count_null()"),
    w.out("x-o3", DESC_OUT, size=24, label=w.esc(DESC_SRC)),
    st.card("x-t", "trap", "⚠️ count = כמה ערכים <b>קיימים</b>"), gap=30),
   panel=w.stem(Q["id"], "איזו פקודה תיתן את מספר הערכים החסרים בכל עמודה בצורה המדויקת ביותר?")
         + st.options("q", OPTS, notes={1: "לא קיימת", 2: "סופרת קיימים", 3: "צריך לחסר"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: isnull() נותן טבלת True ו-False, ואיתה sum נותן מספר חסרים לכל עמודה.", do=show("r-1"),
      say="לסיכום: אִיז נָאל נותן טבלת טְרוּ ופוֹלְס, ואיתה סָאם נותן מספר חסרים לכל עמודה."),
    P("dropna() מוחק כל שורה עם חסר, ועם axis שווה אחת, כל עמודה.", do=show("r-2"),
      say="דְרוֹפּ אֶן אֵיי מוחק כל שורה עם חסר, ועם אַקְסִיס שווה אחת, כל עמודה."),
    P("ושלושה סוגי חוסר: אקראי לגמרי, תלוי במשתנה אחר, או תלוי בערך עצמו. נתראה ברמה הבאה.", do=show("r-3"),
      hold=0.6),
], stage=w.stack(w.frame("tr", df, size=30, cw=120), gap=20),
   panel=st.card("r-1", "rule", "🔑 " + w.mono("isnull().sum()") + " ← חסרים לכל עמודה")
         + st.card("r-2", "rule", "🔑 " + w.mono("dropna()") + " ← שורות · " + w.mono("axis=1") + " ← עמודות")
         + st.card("r-3", "rule", "🔑 MCAR · MAR · MNAR"))

SCENES = [title, idea, isnull, drop, kinds, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("C02", "clean", "איתור ערכים חסרים", SCENES, bank={"26B-A-Q11": 0})

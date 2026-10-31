# -*- coding: utf-8 -*-
"""C04 · שורות כפולות — video script (build: tools/video/vid.py C04).

Source: courses/clean/C04.js (lesson + goal: what duplicated returns, counting duplicates, drop_duplicates with
keep and subset). Exam anchor: 26A-B-Q7 (the meaning of a True in the 4th place of duplicated()), which no guided
quiz uses. The exam prints no table, so the video builds its own 4-row table whose output is False, False, False,
True and uses it to test each option.
Avoided on purpose: the C04 quiz tables (Dan / Eli / Noa, the 10-value series, the name/city subset table) and their
answers, and the unique + duplicates = rows rule (C04-Q4, P-22). P-43 (duplicated() is a vector as long as the rows)
is solved in the C07 video. The shop table (product, price) is mine; every flag, count and kept index on screen
comes from running the code that is shown.
"""
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_clean as w

# ---------------------------------------------------------------- the shop table (run)
MAKE = ("df = pd.DataFrame({'product': ['pen', 'cup', 'pen', 'hat', 'cup', 'pen'],\n"
        "                   'price':   [5, 12, 5, 30, 15, 7]})")
env, _ = w.run(MAKE)
df = env["df"]
DUP = df.duplicated().tolist()
assert DUP == [False, False, True, False, False, False]
_, SUM_OUT = w.run("print(df.duplicated().sum())", env)
assert SUM_OUT == "1"
_, DROP_OUT = w.run("print(len(df.drop_duplicates()))", env)
assert DROP_OUT == "5"
_, LAST_OUT = w.run("print(list(df.drop_duplicates(keep='last').index))", env)
assert LAST_OUT == "[1, 2, 3, 4, 5]"
_, SUB_OUT = w.run("print(list(df.drop_duplicates(subset=['product']).index))", env)
assert SUB_OUT == "[0, 1, 3]"
assert df.iloc[4].tolist() == ["cup", 15] and df.iloc[1].tolist() == ["cup", 12]   # same product, other price
assert df.iloc[5].tolist() == ["pen", 7]

# ---------------------------------------------------------------- exam 26A-B-Q7 on a 4-row table of mine
Q = BANK["26A-B-Q7"]
assert Q["correctIndex"] == 0
MAKE4 = "d = pd.DataFrame({'name': ['Ron', 'Gal', 'Ron', 'Ron'],\n                  'age':  [30, 41, 25, 30]})"
e4, _ = w.run(MAKE4)
d = e4["d"]
D4 = d.duplicated().tolist()
assert D4 == [False, False, False, True]
assert d.iloc[3].tolist() == d.iloc[0].tolist()                 # row 4 equals an earlier row (the first)
assert d.iloc[3].tolist() != d.iloc[2].tolist()                 # but not the row right before it
assert d.iloc[2]["name"] == d.iloc[0]["name"] and D4[2] is False   # sharing one column value is not a duplicate
OPTS = [(k, f'<span style="font-size:27px;line-height:1.3">{o}</span>') for k, o in enumerate(Q["options"])]

T1 = w.frame("a", df, extra=[("duplicated()", [w.flag(v) for v in DUP])], size=30, cw=150)
T2 = w.frame("b", df, size=24, cw=140)
T3 = w.frame("c", df, size=24, cw=140)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד למצוא שורות כפולות בטבלה, ולמחוק אותן."),
    P("נראה מה duplicated מחזיר, ואיך keep ו-subset משנים את מה שנמחק.",
      say="נראה מה דּוּפְּלִיקֵייטֵד מחזיר, ואיך קִיפּ וסַאבְּסֶט משנים את מה שנמחק."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">C04 · ניקוי נתונים וסולמות</div><h1>שורות כפולות</h1>'
         '<p>להבין מה duplicated מחזיר, לספור כפילויות, ולהשתמש ב-drop_duplicates עם keep ו-subset.</p>', layout="title")

idea = Scene("idea", "duplicated", [
    P("לפנינו טבלת מכירות של חנות: מוצר ומחיר, שש שורות.", do=show("a")),
    P("שורה כפולה היא שורה **זהה לגמרי** לשורה שכבר הופיעה קודם. בכל העמודות."),
    P("למה זה מפריע? כי מכירה שנרשמה פעמיים תיספר פעמיים, בכל סכום ובכל ממוצע.", do=show("i-c0")),
    P("הפקודה duplicated() עוברת על השורות לפי הסדר, ולכל שורה עונה True או False.", do=show("a-e0h")),
    P("שורה 0, עט בחמישה שקלים: מופיעה בפעם הראשונה. False.", do=show("a-e0-0", "a-h-0-0", "a-h-0-1")),
    P("שורה 1, כוס, גם היא חדשה. אבל שורה 2: עט בחמישה שקלים, בדיוק כמו שורה 0. True.",
      do=show("a-e0-1", "a-e0-2", "a-h-2-0", "a-h-2-1")),
    P("שורה 3, כובע: חדשה. ושורה 4: כוס, כמו בשורה 1. אבל המחיר שונה, 15 ולא 12. לכן False.",
      do=show("a-e0-3", "a-e0-4", "a-h-4-1", "a-h-1-1") + hide("a-h-0-0", "a-h-0-1", "a-h-2-0", "a-h-2-1"),
      say="שורה שלוש, כובע: חדשה. ושורה ארבע: כוס, כמו בשורה אחת. אבל המחיר שונה, חמש עשרה ולא שתים עשרה. לכן פוֹלְס."),
    P("גם שורה 5 היא עט, אבל בשבעה שקלים. False. ערך אחד משותף לא הופך שורה לכפולה.",
      do=show("a-e0-5", "i-c1") + hide("a-h-4-1", "a-h-1-1")),
    P("והתוצאה היא **וקטור**: ערך אחד לכל שורה, באורך מספר השורות. כדי לקבל מספר, מוסיפים sum.",
      do=show("i-out"), say="והתוצאה היא וקטור: ערך אחד לכל שורה, באורך מספר השורות. כדי לקבל מספר, מוסיפים סָאם."),
], stage=T1,
   panel=st.card("i-c0", "ex", "כפילות נספרת פעמיים בכל סכום וממוצע")
         + st.card("i-c1", "rule", "🔑 True רק כשהשורה זהה <b>בכל העמודות</b> לשורה קודמת")
         + w.out("i-out", SUM_OUT, size=28, label="print(df.duplicated().sum())"))

drop = Scene("drop", "drop_duplicates", [
    P("עכשיו מוחקים. drop_duplicates() מוחק כל שורה שהיא כפילות.", do=show("b")),
    P("ברירת המחדל היא keep שווה first: משאירים את ההופעה **הראשונה**, ומוחקים את מה שבא אחריה.",
      do=show(*w.row_strike("b", df, 2), "d-c1"),
      say="ברירת המחדל היא קִיפּ שווה פֶרְסְט: משאירים את ההופעה הראשונה, ומוחקים את מה שבא אחריה."),
    P("שורה 2 נמחקת, ונשארות חמש שורות.", do=show("d-out")),
    P("עם keep שווה last, ההפך: משאירים את ההופעה **האחרונה**.", do=show("c", "d-c2"),
      say="עם קִיפּ שווה לַאסְט, ההפך: משאירים את ההופעה האחרונה."),
    P("עכשיו שורה 0 נמחקת, ושורה 2 נשארת. אותו מספר שורות, אינדקסים אחרים.",
      do=show(*w.row_strike("c", df, 0), "d-out2")),
], stage=w.stack(T2, T3, gap=24),
   panel=st.card("d-c1", "plain", w.mono("keep='first'") + " (ברירת מחדל) ← נשארת הראשונה")
         + w.out("d-out", DROP_OUT, size=26, label="print(len(df.drop_duplicates()))")
         + st.card("d-c2", "plain", w.mono("keep='last'") + " ← נשארת האחרונה")
         + w.out("d-out2", LAST_OUT, size=26, label="drop_duplicates(keep='last').index"))

subset = Scene("subset", "subset", [
    P("ומה אם אנחנו רוצים מוצר אחד בלבד מכל סוג, בלי קשר למחיר?", do=show("s")),
    P("בשביל זה יש subset: משווים רק לפי העמודות שבוחרים.", do=show("s-c1", "s-hh-0"),
      say="בשביל זה יש סַאבְּסֶט: משווים רק לפי העמודות שבוחרים."),
    P("לפי המוצר בלבד, שורות 2 ו-5 הן עט שכבר הופיע, ושורה 4 היא כוס שכבר הופיעה.",
      do=show(*w.row_strike("s", df, 2), *w.row_strike("s", df, 4), *w.row_strike("s", df, 5))),
    P("נשארות שלוש שורות: 0, 1 ו-3.", do=show("s-out")),
    P("אבל שימו לב מה הלך לאיבוד: עט בשבעה שקלים וכוס בחמישה עשר. אלה לא היו כפילויות אמיתיות.", do=show("s-c2"),
      hold=0.3),
], stage=w.frame("s", df, size=30, cw=150, hidden=True),
   panel=st.card("s-c1", "plain", w.mono("subset=['product']") + " ← משווים רק לפי product")
         + w.out("s-out", SUB_OUT, size=26, label="drop_duplicates(subset=['product']).index")
         + st.card("s-c2", "trap", "⚠️ subset יכול למחוק שורות ששונות בעמודות האחרות"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: duplicated על טבלה של ארבע שורות החזיר שלושה False ואז True. מה המשמעות של ה-True?",
      say="ועכשיו שאלה ממבחן: דּוּפְּלִיקֵייטֵד על טבלה של ארבע שורות החזיר שלושה פוֹלְס ואז טְרוּ. מה המשמעות של הטְרוּ?"),
    P("נבנה טבלה כזו ונבדוק: רון בן 30, גל בן 41, רון בן 25, ושוב רון בן 30.", do=show("x"),
      say="נבנה טבלה כזו ונבדוק: רון בן שלושים, גל בן ארבעים ואחת, רון בן עשרים וחמש, ושוב רון בן שלושים."),
    P("הפלט באמת שלושה False ואז True.", do=show(*[f"x-e0-{i}" for i in range(4)], "x-e0h"),
      say="הפלט באמת שלושה פוֹלְס ואז טְרוּ."),
    P("השורה הרביעית זהה לשורה הראשונה. כלומר היא כפילות של **אחת** מהשורות הקודמות.",
      do=show("x-h-3-0", "x-h-3-1", "x-h-0-0", "x-h-0-1", "q-ok-0")),
    P("לא של השורה שלפניה: השורה השלישית היא רון בן 25, והיא שונה.", do=show("q-x-2", "q-n-2"),
      say="לא של השורה שלפניה: השורה השלישית היא רון בן עשרים וחמש, והיא שונה."),
    P("והשורה השלישית חולקת עם הראשונה את השם רון, ובכל זאת קיבלה False. ערך משותף בעמודה אחת לא מספיק.",
      do=show("q-x-3", "q-n-3", "x-h-2-0"), say="והשורה השלישית חולקת עם הראשונה את השם רון, ובכל זאת קיבלה פוֹלְס. ערך משותף בעמודה אחת לא מספיק."),
    P("ו״ייחודית״ היא ההפך הגמור: ייחודית מקבלת False.", do=show("q-x-1", "q-n-1"),
      say="וייחודית היא ההפך הגמור: שורה ייחודית מקבלת פוֹלְס."),
    P("המלכודת: True לא אומר ״דומה״ ולא ״זהה לשכנה״. הוא אומר זהה לגמרי לשורה שכבר הופיעה.", do=show("x-t"),
      hold=0.5, say="המלכודת: טְרוּ לא אומר דומה, ולא זהה לשכנה. הוא אומר זהה לגמרי לשורה שכבר הופיעה."),
], stage=w.stack(w.stem(Q["id"], "duplicated על דטה בן 4 שורות החזיר False, False, False, True. מה משמעות ה-True הרביעי?"),
                 w.frame("x", d, extra=[("duplicated()", [w.flag(v) for v in D4])], size=30, cw=130, hidden=True),
                 st.card("x-t", "trap", "⚠️ True = זהה בכל העמודות לשורה <b>קודמת כלשהי</b>"), gap=30),
   panel=st.options("q", OPTS, notes={1: "הפוך", 2: "לא השכנה", 3: "לא מספיק"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: duplicated() מחזיר וקטור של True ו-False, אחד לכל שורה.", do=show("r-1"),
      say="לסיכום: דּוּפְּלִיקֵייטֵד מחזיר וקטור של טְרוּ ופוֹלְס, אחד לכל שורה."),
    P("True רק כשהשורה זהה בכל העמודות לשורה קודמת. עם sum סופרים כפילויות.", do=show("r-2"),
      say="טְרוּ רק כשהשורה זהה בכל העמודות לשורה קודמת. עם סָאם סופרים כפילויות."),
    P("drop_duplicates מוחק. keep קובע איזו הופעה נשארת, ו-subset קובע לפי אילו עמודות משווים. נתראה ברמה הבאה.",
      do=show("r-3"), hold=0.6,
      say="דְרוֹפּ דּוּפְּלִיקֵייטְס מוחק. קִיפּ קובע איזו הופעה נשארת, וסַאבְּסֶט קובע לפי אילו עמודות משווים. נתראה ברמה הבאה."),
], stage=w.frame("r", df, extra=[("duplicated()", [w.flag(v) for v in DUP])], size=30, cw=150).replace(
    'class="h">', 'class="">'),
   panel=st.card("r-1", "rule", "🔑 " + w.mono("duplicated()") + " ← וקטור באורך מספר השורות")
         + st.card("r-2", "rule", "🔑 True = זהה בכל העמודות לשורה קודמת")
         + st.card("r-3", "rule", "🔑 " + w.mono("keep") + " ← איזו נשארת · " + w.mono("subset") + " ← לפי מה משווים"))

SCENES = [title, idea, drop, subset, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("C04", "clean", "שורות כפולות", SCENES, bank={"26A-B-Q7": 0})

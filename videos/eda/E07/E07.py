# -*- coding: utf-8 -*-
"""E07 · איזה גרף למה? — video script (build: tools/video/vid.py E07).

Source: courses/eda/E07.js (lesson + goal: choose the chart by the variable type and the goal; read a crosstab with
normalize='index').
Exam anchor: 24A-B-Q6 (pie charts: the composition of a whole, for few categories). No guided quiz uses it.
Not used on purpose: every E07 quiz item (the sex/passed crosstab, height of 500 people, three classes + outliers,
A/B numeric + C categorical, the 12 x 12 correlation matrix) and their bank twins (25A-B-Q13 parallel box plots,
25A-A-Q18 / 26A-A-Q10 / 25A-B-Q14 / 25A-B-Q15 scatter with color, 26A-B-Q17 heatmap); 26A-B-Q18 (pairplot) and
P-35 / P-51 (crosstab) are left for other uses. Worked examples: six new chart-choice scenarios, and a crosstab of 12
employees (shift day/night x late yes/no) computed with pandas.crosstab and asserted.
"""
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_eda as w

# ---------------------------------------------------------------- crosstab (verified)
df = pd.DataFrame({"shift": ["day"] * 8 + ["night"] * 4,
                   "late": ["yes", "no", "no", "no", "yes", "no", "no", "no", "yes", "yes", "no", "yes"]})
ct = pd.crosstab(df["shift"], df["late"])
assert ct.loc["day", "yes"] == 2 and ct.loc["day", "no"] == 6 and ct.loc["night", "yes"] == 3 and ct.loc["night", "no"] == 1
cn = pd.crosstab(df["shift"], df["late"], normalize="index")
assert cn.loc["day", "yes"] == 0.25 and cn.loc["day", "no"] == 0.75
assert cn.loc["night", "yes"] == 0.75 and cn.loc["night", "no"] == 0.25
assert (cn.sum(axis=1) == 1).all()
ca = pd.crosstab(df["shift"], df["late"], normalize="all")
assert round(ca.loc["night", "yes"], 2) == 0.25 and ca.values.sum() == 1          # 3 of all 12: a different question
assert list(ct.columns) == ["no", "yes"]

# exam 24A-B-Q6
Q = BANK["24A-B-Q6"]
assert Q["correctIndex"] == 0 and "הרכב השלם" in Q["options"][0] and "מועטות" in Q["options"][0]
OPTS = list(enumerate(Q["options"]))

# pie vs bars (verified)
PA = [45, 30, 15, 10]
PIE_A, ang = w.pie("pa", PA, R=140)
assert sum(PA) == 100 and [round(a) for a in ang] == [162, 108, 54, 36]
PB = [11, 10, 9, 9, 8, 8, 8, 8, 8, 7, 7, 7]
PIE_B, angb = w.pie("pb", PB, R=140, pct=False)
assert sum(PB) == 100 and len(PB) == 12 and round(angb[2] - angb[4], 1) == 3.6
BARS_B = w.bars("bb", [str(i + 1) for i in range(12)], PB, w=520, h=300, ymax=12)

# ---------------------------------------------------------------- figures
CHARTS = [("hist", "hist", "היסטוגרמה"), ("bar", "bar", "גרף עמודות"), ("sc", "scatter", "scatter plot"),
          ("pie", "pie", "גרף עוגה"), ("line", "line", "גרף קו (line)"), ("box", "box", "box plot מקביל")]
GRID = '<div class="ed-grid3">' + "".join(w.chart_card(f"g-{k}", kind, name) for k, kind, name in CHARTS) + "</div>"

T1 = w.table("t1", ["shift \\ late", "no", "yes", "סה״כ"], [["day", "6", "2", "8"], ["night", "1", "3", "4"]], size=34)
T2 = w.table("t2", ["shift \\ late", "no", "yes"], [["day", "0.75", "0.25"], ["night", "0.25", "0.75"]], hide={1, 2}, size=34)
CODE = ('<div id="c-code" class="ed-code h">pd.crosstab(df[\'shift\'], df[\'late\'],\n'
        '            <b>normalize=\'index\'</b>)</div>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לבחור את הגרף הנכון לנתונים."),
    P("נבנה כלל החלטה לפי סוג המשתנה והמטרה, ונקרא טבלת שכיחויות משולבת."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">E07 · סטטיסטיקה וגרפים</div><h1>איזה גרף למה?</h1>'
         '<p>לבחור את הגרף הנכון לפי סוג המשתנים והמטרה, ולקרוא טבלת crosstab מנורמלת.</p>', layout="title")

pick = Scene("pick", "כלל ההחלטה", [
    P("לפני שבוחרים גרף, שואלים שתי שאלות: איזה סוג משתנה יש לי, ומה אני רוצה לראות.", do=show("k-q")),
    P("משך שיחות במוקד, בדקות. משתנה **רציף**, ורוצים לדעת באיזה טווח נמצאות רוב השיחות: היסטוגרמה.", do=show("g-hist")),
    P("מספר הילדים במשפחה, מאפס עד חמש. משתנה **בדיד**, עם מעט ערכים: גרף עמודות, עמודה לכל ערך.", do=show("g-bar")),
    P("תקציב פרסום מול מכירות: הקשר בין **שני** משתנים רציפים. כל נקודה היא חנות: גרף פיזור.", do=show("g-sc")),
    P("נתח השוק של ארבעה מותגים. **חלקים מתוך שלם**, ומעט קטגוריות: גרף עוגה.", do=show("g-pie")),
    P("טמפרטורה יומית לאורך שנה. מגמה לאורך **זמן**: גרף קו.", do=show("g-line")),
    P("ואם רוצים להשוות את החציון והרבעונים של זמני משלוח בין ארבע ערים: box plot, אחד ליד השני.", do=show("g-box")),
    P("ועוד שניים: מפת חום, למשל מכירות לפי יום בשבוע ושעה ביום, ו-pairplot לכל זוגות המשתנים.", do=show("k-more"),
      say="ועוד שניים: מפת חום, למשל מכירות לפי יום בשבוע ושעה ביום, ופֵּייר פְּלוֹט לכל זוגות המשתנים.", hold=0.4),
], stage=GRID,
   panel=st.card("k-q", "rule", "🔑 שתי שאלות: מה <b>סוג המשתנה</b>? ומה <b>רוצים לראות</b>?")
         + st.card("k-more", "ex", "heatmap: מכירות לפי יום × שעה · pairplot: כל זוג משתנים + התפלגות כל אחד"))

cross = Scene("cross", "crosstab", [
    P("עכשיו שני משתנים **קטגוריאליים**. שנים עשר עובדים: משמרת יום או לילה, והאם איחרו.", hold=0.2),
    P("הפקודה crosstab סופרת כל צירוף. ביום: 6 לא איחרו ו-2 איחרו. בלילה: 1 ו-3.", do=show("c-t1"),
      say="הפקודה קְרוֹס טַאבּ סופרת כל צירוף. ביום: שישה לא איחרו ושניים איחרו. בלילה: אחד ושלושה."),
    P("אבל ביום יש שמונה עובדים ובלילה רק ארבעה. איך משווים?", do=show("c-q")),
    P("מוסיפים נרמול לפי שורה. עכשיו כל תא מחולק **בסכום השורה שלו**.", do=show("c-code", "c-t2")),
    P("ביום: 2 מתוך 8, כלומר 0.25 איחרו, ו-0.75 לא.", do=show("t2-r0c1", "t2-r0c2"),
      say="ביום: שניים מתוך שמונה, כלומר אפס נקודה עשרים וחמש איחרו, ואפס נקודה שבעים וחמש לא."),
    P("בלילה: 3 מתוך 4, כלומר 0.75 איחרו. שיעור האיחורים בלילה גבוה פי שלושה.", do=show("t2-r1c1", "t2-r1c2"),
      say="בלילה: שלושה מתוך ארבעה, כלומר אפס נקודה שבעים וחמש איחרו. שיעור האיחורים בלילה גבוה פי שלושה."),
    P("ובדיקה מהירה: אחרי נרמול לפי שורה, הסכום של כל שורה הוא בדיוק אחת.", do=show("c-r1")),
    P("והמלכודת: 3 מתוך כל 12 העובדים זה 0.25. זה נרמול לפי הסכום הכללי, שאלה אחרת.", do=show("c-trap"),
      say="והמלכודת: שלושה מתוך כל שנים עשר העובדים זה אפס נקודה עשרים וחמש. זה נרמול לפי הסכום הכללי, שאלה אחרת.",
      hold=0.4),
], stage=f'<div class="ed-col"><div id="c-t1" class="h">{T1}</div>{CODE}<div id="c-t2" class="h">{T2}</div></div>',
   panel=st.card("c-q", "plain", "יום: 8 עובדים · לילה: 4 עובדים")
         + st.card("c-r1", "rule", "🔑 <code>normalize='index'</code>: כל תא ÷ סכום השורה, כל שורה = 1")
         + st.card("c-trap", "trap", "⚠️ $3 \\div 12 = 0.25$ הוא נרמול כללי, לא לפי שורה"))

pies = Scene("pies", "מתי עוגה", [
    P("נתעכב על גרף העוגה. ארבעה מותגים, עם 45, 30, 15 ו-10 אחוזים מהמכירות.", do=show("p-a")),
    P("כל פרוסה מקבלת זווית לפי החלק שלה: 45 אחוז מתוך 360 מעלות זה 162 מעלות.", do=show("p-eq")),
    P("עם ארבע פרוסות רואים מיד מי גדול ומי קטן, ושכולן יחד הן שלם אחד.", do=show("p-c1"), hold=0.3),
    P("ועכשיו שתים עשרה קטגוריות, עם ערכים קרובים: בין 7 ל-11 אחוז.", do=hide("p-a", "p-eq") + show("p-b")),
    P("איזו פרוסה גדולה יותר, של 9 אחוז או של 8 אחוז? ההבדל ביניהן הוא פחות מארבע מעלות.", do=show("p-eq2")),
    P("באותם נתונים בגרף עמודות, ההשוואה קלה: כל העמודות עומדות על אותו ציר.", do=show("p-bars", "p-c2"), hold=0.4),
], stage=f'<div class="ed-rowc"><div class="swap" style="--swap-h:420px;width:420px"><div id="p-a" class="h">{PIE_A}</div>'
         f'<div id="p-b" class="h">{PIE_B}</div></div><div class="ed-col" style="width:auto">'
         + w.eq("p-eq", "$0.45 \\times 360^\\circ = 162^\\circ$", 38)
         + w.eq("p-eq2", "$9\\% \\to 32.4^\\circ,\\quad 8\\% \\to 28.8^\\circ$", 34)
         + f'<div id="p-bars" class="h">{BARS_B}</div></div></div>',
   panel=st.card("p-c1", "rule", "🔑 עוגה: חלקים מתוך <b>שלם</b>, ומעט קטגוריות")
         + st.card("p-c2", "trap", "⚠️ הרבה קטגוריות קרובות ← גרף עמודות"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה נכון לגבי תרשים עוגה?"),
    P("עוגה מראה איך שלם אחד מתחלק לחלקים, והעין משווה זוויות. זה עובד כשיש מעט פרוסות.", do=show("x-pie")),
    P("לכן התשובה: הרכב של השלם, עבור מספר קטן של קטגוריות.", do=show("q-ok-0")),
    P("עם יותר מעשר קטגוריות, הפרוסות נהיות דקות, וכמעט אי אפשר להשוות ביניהן. לזה מתאים גרף עמודות.",
      do=show("q-x-1", "q-n-1")),
    P("נתונים לאורך הרבה תקופות זמן? זו מגמה, ולה מתאים גרף קו, לא עוגה.", do=show("q-x-2", "q-n-2")),
    P("ונתונים רציפים מציגים בהיסטוגרמה: לעוגה צריך קטגוריות שמרכיבות שלם.", do=show("q-x-3", "q-n-3"), hold=0.6),
], stage=f'<div class="ed-col">{w.chart_card("x-pie", "pie", "חלקים מתוך שלם, מעט קטגוריות")}</div>',
   panel='<div class="ed-small">' + w.stem(Q["id"], "מה מהטענות הבאות נכון לגבי תרשים עוגה?")
         + st.options("q", OPTS, notes={1: "פרוסות דקות", 2: "גרף קו", 3: "היסטוגרמה"}) + "</div>")

recap = Scene("recap", "סיכום", [
    P("לסיכום: רציף, היסטוגרמה. בדיד עם מעט ערכים, גרף עמודות.", do=show("r-1")),
    P("קשר בין שני רציפים, גרף פיזור. השוואת חציונים ורבעונים בין קבוצות, box plot מקביל.", do=show("r-2")),
    P("חלקים מתוך שלם עם מעט קטגוריות, עוגה. ומגמה בזמן, גרף קו.", do=show("r-3")),
    P("ובטבלה משולבת עם נרמול לפי שורה, כל שורה מסתכמת לאחת. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=GRID.replace('id="g-', 'id="rg-').replace(' h"', '"'),
   panel=st.card("r-1", "rule", "🔑 רציף ← היסטוגרמה · בדיד ← עמודות")
         + st.card("r-2", "rule", "🔑 שני רציפים ← scatter · קבוצות ← box plot")
         + st.card("r-3", "rule", "🔑 שלם, מעט קטגוריות ← עוגה · זמן ← קו")
         + st.card("r-4", "rule", "🔑 <code>normalize='index'</code>: כל שורה = 1"))

VIDEO = Video("E07", "eda", "איזה גרף למה?", [title, pick, cross, pies, exam, recap], bank={"24A-B-Q6": 0})

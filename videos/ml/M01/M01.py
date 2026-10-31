# -*- coding: utf-8 -*-
"""M01 · איזה סוג בעיה זו? — video script (build: tools/video/vid.py M01).

Source: courses/ml/M01.js (lesson + goal: supervised vs unsupervised, and classification / regression / clustering /
dimension reduction). Exam anchor: 25-S-Q2 (the difference between classification and regression: the label is
nominal/ordinal vs a number; key = option index 1), which no guided quiz uses.
Not used on purpose: the M01 quiz scenarios (50 customer features into 5 groups, apartment prices, spam e-mails,
50 features shown in 2-D, the "unsupervised pair" of algorithms), the boss items 24A-A-Q17 (Netflix customers into
5 groups) and 26B-A-Q14 (songs: hit / good / no potential) and their twin 24A-B-Q12 (Netflix, visualize). The worked
scenarios are new: chest X-rays, tomorrow's temperature, news articles, a 40-sensor machine, student grades.
The verdicts come from the course checker's rule (tools/verify/needhelp/ml/check.py: classify), re-implemented and
asserted below on every scenario shown.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_ml as w


def classify(has_label, label_kind=None, goal=None):
    """the checker's rule engine (ml/check.py): (label?, label kind / goal) -> (learning kind, problem type)"""
    if has_label:
        return ("מונחית", "סיווג" if label_kind == "categorical" else "רגרסיה")
    return ("לא מונחית", "אשכול" if goal == "groups" else "הורדת ממדים")


# ---------------------------------------------------------------- scenarios (verified)
SCEN = [
    ("צילומי רנטגן, כל אחד מסומן ״דלקת ריאות״ או ״תקין״", (True, "categorical", None), ("מונחית", "סיווג")),
    ("עשר שנות מדידות, ולכל יום הטמפרטורה של מחרת", (True, "numeric", None), ("מונחית", "רגרסיה")),
    ("אלפי כתבות חדשות בלי שום סימון, לקבץ כתבות דומות", (False, None, "groups"), ("לא מונחית", "אשכול")),
    ("מכונה עם 40 חיישנים, לתאר כל רגע ב-3 מספרים", (False, None, "reduce"), ("לא מונחית", "הורדת ממדים")),
]
for _, args, want in SCEN:
    assert classify(*args) == want
# the trap scene: the LABEL decides, whatever the features are
assert classify(True, "numeric") == ("מונחית", "רגרסיה")              # grade 0-100 from categorical features
assert classify(True, "categorical") == ("מונחית", "סיווג")           # pass / fail from numeric features
assert classify(True, "categorical") == ("מונחית", "סיווג")           # ordinal label low / medium / high

# exam 25-S-Q2
Q = BANK["25-S-Q2"]
assert Q["correctIndex"] == 1 and "שמית או סודרת" in Q["options"][1] and "הנתונים הינם קטגוריאליים" in Q["options"][2]
assert Q["options"][3] == "בסיווג יש תויות ובנסיגה אין."
OPTS = list(enumerate(Q["options"]))

ROWS = [(t, "כן" if a[0] else "לא", f"{k}, <b>{p}</b>") for t, a, (k, p) in SCEN]
TAB = w.table("sc", ["המצב", "תווית?", "הסוג"], ROWS, size=32)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לזהות איזה סוג בעיה עומד מולנו."),
    P("מונחית או לא מונחית, ואחר כך: סיווג, רגרסיה, אשכול או הורדת ממדים."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">M01 · מודלים והערכה</div><h1>איזה סוג בעיה זו?</h1>'
         '<p>לסווג בעיה ללמידה מונחית או לא מונחית, ולהגדיר אותה כסיווג, רגרסיה, אשכול או הורדת ממדים.</p>', layout="title")

idea = Scene("idea", "שאלה אחת מכריעה", [
    P("השאלה הראשונה תמיד: האם בנתוני האימון יש **תווית**?", do=show("t-hl-q1")),
    P("תווית היא התשובה הנכונה, שמוכנה מראש לכל דוגמה. למשל: ״הצילום הזה תקין״.", do=show("i-1")),
    P("אם יש תווית, זו **למידה מונחית**: המודל לומד מהתשובות.", do=hide("t-hl-q1") + show("t-yes")),
    P("עכשיו שואלים איזו תווית. אם היא קטגוריה, הבעיה היא **סיווג**.", do=show("t-q2", "t-cls")),
    P("ואם היא מספר, הבעיה היא **רגרסיה**.", do=show("t-reg"), hold=0.3),
    P("אם אין תווית, זו **למידה לא מונחית**: אין תשובות, רק הנתונים עצמם.", do=show("t-no")),
    P("רוצים לחלק את הדוגמאות לקבוצות דומות? זה **אשכול**.", do=show("t-q3", "t-clu")),
    P("רוצים לצמצם את מספר העמודות, ולשמור על רוב המידע? זו **הורדת ממדים**.", do=show("t-dim"), hold=0.4),
], stage=f'<div class="ml-col">{w.tree()}</div>',
   panel=st.card("i-1", "rule", "🔑 <b>תווית</b> = התשובה הנכונה, מוכנה מראש לכל דוגמה באימון"))

examples = Scene("examples", "ארבעה מצבים", [
    P("נתרגל על ארבעה מצבים חדשים."),
    P("בית חולים: צילומי רנטגן, וכל צילום מסומן ״דלקת ריאות״ או ״תקין״.", do=show("sc-r0")),
    P("יש תווית, והיא קטגוריה. לכן: מונחית, סיווג.", hold=0.2),
    P("תחנת מזג אוויר: עשר שנות מדידות, ולכל יום רשומה הטמפרטורה של מחרת.", do=show("sc-r1")),
    P("התווית היא מספר, מעלות. לכן: מונחית, רגרסיה.", hold=0.2),
    P("אתר חדשות: אלפי כתבות בלי שום סימון, ורוצים לקבץ כתבות דומות.", do=show("sc-r2")),
    P("אין תווית, והמטרה היא קבוצות. לכן: לא מונחית, אשכול.", hold=0.2),
    P("ומכונה עם 40 חיישנים: רוצים לתאר כל רגע בשלושה מספרים בלבד.", do=show("sc-r3"),
      say="ומכונה עם ארבעים חיישנים: רוצים לתאר כל רגע בשלושה מספרים בלבד."),
    P("אין תווית, והמטרה היא פחות עמודות. לכן: לא מונחית, הורדת ממדים.", hold=0.4),
], stage=f'<div class="ml-col">{TAB}</div>', layout="full")

trap = Scene("trap", "התווית מכריעה", [
    P("ועכשיו המלכודת הגדולה: מה קובע אם זה סיווג או רגרסיה?"),
    P("לא סוג העמודות שנכנסות למודל, אלא רק סוג **התווית**.", do=show("k-rule")),
    P("דוגמה: חוזים ציון בבחינה, מאפס עד מאה, לפי מגמת הלימוד ולפי משמרת בוקר או ערב.", do=show("k-1")),
    P("כל העמודות קטגוריות, אבל התווית היא מספר. לכן זו רגרסיה.", do=show("k-1v"), hold=0.2),
    P("ובכיוון ההפוך: חוזים ״עבר״ או ״נכשל״, לפי שעות למידה ואחוז נוכחות.", do=show("k-2")),
    P("העמודות מספריות, אבל התווית קטגוריה. לכן זה סיווג.", do=show("k-2v"), hold=0.3),
    P("ותווית **סודרת**, כמו נמוך, בינוני וגבוה? יש בה סדר, אבל היא עדיין קטגוריה: סיווג.", do=show("k-3")),
    P("ועוד שם מטעה: **רגרסיה לוגיסטית** היא, למרות השם, אלגוריתם סיווג.", do=show("k-4"), hold=0.4),
], stage='<div class="ml-col">'
         + st.card("k-1", "ex", "ציון 0–100 ← מגמה, בוקר/ערב (קטגוריות)")
         + w.chip("k-1v", "תווית מספרית ← <b>רגרסיה</b>", "info")
         + st.card("k-2", "ex", "עבר / נכשל ← שעות למידה, נוכחות (מספרים)")
         + w.chip("k-2v", "תווית קטגוריה ← <b>סיווג</b>", "info") + "</div>",
   panel=st.card("k-rule", "rule", "🔑 <b>התווית</b> מכריעה, לא העמודות שנכנסות")
         + st.card("k-3", "ex", "תווית סודרת (נמוך / בינוני / גבוה) ← עדיין <b>סיווג</b>")
         + st.card("k-4", "trap", "⚠️ רגרסיה לוגיסטית = אלגוריתם <b>סיווג</b>"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה ההבדל בין סיווג לבין נסיגה, כלומר רגרסיה?"),
    P("לפי מה שראינו, ההבדל הוא בסוג התווית: קטגוריה מול מספר."),
    P("קטגוריה יכולה להיות שמית, כמו צבע, או סודרת, כמו נמוך ובינוני. ובנסיגה התווית היא מספר.", do=show("q-ok-1"), hold=0.3),
    P("המלכודת היא האפשרות שמדברת על **הנתונים**: נתונים קטגוריאליים מול מספריים.", do=show("x-t")),
    P("אבל ראינו רגרסיה עם עמודות קטגוריות, וסיווג עם עמודות מספריות. העמודות לא קובעות.", do=show("q-x-2", "q-n-2")),
    P("״בסיווג יש תוויות ובנסיגה אין״: לא נכון. שתיהן מונחות, ובשתיהן יש תווית.", do=show("q-x-3", "q-n-3")),
    P("והאפשרות הארוכה מתארת בעצם בחירה של נתוני אימון, ולא את ההבדל בין סוגי הבעיות.", do=show("q-x-0", "q-n-0"), hold=0.6),
], stage=w.stem(Q["id"], "מה ההבדל בין סיווג ונסיגה (רגרסיה)?")
         + f'<div class="ml-opts">{st.options("q", OPTS, notes={0: "לא קשור", 2: "העמודות", 3: "שתיהן מונחות"})}</div>',
   panel=st.card("x-t", "trap", "⚠️ <b>הנתונים</b> (העמודות) לא קובעים. רק <b>התווית</b>"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: קודם שואלים אם יש תווית. יש: מונחית. אין: לא מונחית.", do=show("r-1")),
    P("במונחית, תווית קטגוריה היא סיווג, ותווית מספרית היא רגרסיה.", do=show("r-2")),
    P("בלא מונחית: קבוצות הן אשכול, ופחות עמודות הן הורדת ממדים.", do=show("r-3")),
    P("והתווית מכריעה, לא העמודות. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=f'<div class="ml-col">{w.tree("u", shown=True)}</div>',
   panel=st.card("r-1", "rule", "🔑 יש תווית? כן ← מונחית · לא ← לא מונחית")
         + st.card("r-2", "rule", "🔑 קטגוריה ← סיווג · מספר ← רגרסיה")
         + st.card("r-3", "rule", "🔑 קבוצות ← אשכול · פחות עמודות ← הורדת ממדים")
         + st.card("r-4", "trap", "⚠️ <b>התווית</b> קובעת, לא העמודות"))

VIDEO = Video("M01", "ml", "איזה סוג בעיה זו?", [title, idea, examples, trap, exam, recap],
              bank={"25-S-Q2": 1})

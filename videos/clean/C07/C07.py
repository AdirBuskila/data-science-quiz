# -*- coding: utf-8 -*-
"""C07 · מבחן גמר: ניקוי נתונים — boss walkthrough (build: tools/video/vid.py C07).

Source: courses/clean/C07.js (boss: real exam questions on scales, missing values, encoding and outliers). The boss
quiz itself (24A-A-Q3, 24A-A-Q18, 25-S-Q24, 26A-B-Q24, P-20, 26A-B-Q21) is never solved here (vid.py refuses those
ids), nor their twins (24A-B-Q11, 26B-A-Q15, P-25, 25A-B-Q7). The walkthrough solves three other bank questions, one
per theme of the course: P-15 (the scale of "prior knowledge in statistics"), P-19 (MCAR vs MAR) and P-43 (what
df.duplicated() returns). Not used: 24B-B-Q10 ("every option is right under conditions", including filling a
numeric feature with the mode, which P-20 calls unsuitable) and P-50 (an option cites its siblings by letter).
The P-43 demonstration runs on a table of mine (5 rows x 3 columns), and its output is produced by running it.
"""
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_clean as w

# ---------------------------------------------------------------- P-15
Q1 = BANK["P-15"]
assert Q1["options"] == ["שמי", "סדר", "מנה"] and Q1["correctIndex"] == 1
LEVELS = ["אין", "בסיסי", "טוב", "מצוין"]
CLASS = [1, 2, 4, 3, 3]                     # five students coded 1..4: the "mean" 2.6 has no meaning
assert sum(CLASS) / len(CLASS) == 2.6
assert w.OPS["ordinal"] == ["שכיח", "חציון"]
O1 = list(enumerate(Q1["options"]))

# ---------------------------------------------------------------- P-19
Q2 = BANK["P-19"]
assert Q2["correctIndex"] == 2 and "(MCAR)" in Q2["options"][2] and "(MAR)" in Q2["options"][2]
SHORT = []
for o in Q2["options"]:
    tags = [t for t in ("MCAR", "MNAR", "MAR") if f"({t})" in o]
    SHORT.append(" ו-".join(f'<bdi class="cl-mono">{t}</bdi>' for t in sorted(tags, key=o.index)))
assert len(SHORT) == 3 and "MCAR" in SHORT[2] and "MAR</bdi>" in SHORT[2]
O2 = list(enumerate(SHORT))

# ---------------------------------------------------------------- P-43 (run)
Q3 = BANK["P-43"]
assert Q3["correctIndex"] == 1
MAKE = ("df = pd.DataFrame({'a': [1, 2, 1, 3, 1],\n                   'b': ['x', 'y', 'x', 'z', 'y'],\n"
        "                   'c': [0, 0, 0, 1, 0]})\nd = df.duplicated()\nprint(type(d).__name__, len(d), df.shape)")
env, OUT3 = w.run(MAKE)
assert OUT3 == "Series 5 (5, 3)"
D = env["d"].tolist()
assert D == [False, False, True, False, False]
r = env["df"].values.tolist()
assert r[2] == r[0] and sum(x == y for x, y in zip(r[4], r[0])) == 2   # row 5 shares two of three values with row 1
assert len(D) == env["df"].shape[0] != env["df"].shape[1]               # one value per row, not per column
O3 = [(k, f'<span style="font-size:28px;line-height:1.3">{o}</span>') for k, o in enumerate(Q3["options"])]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של מסלול ניקוי הנתונים."),
    P("נפתור יחד שלוש שאלות אמיתיות מהתרגול: סולם, סוג חוסר, וכפילויות."),
    P("בכל שאלה נפסול כל אפשרות שגויה, עם הסיבה שלה.", hold=0.4),
], stage='<div class="kicker">C07 · ניקוי נתונים וסולמות</div><h1>מבחן גמר: ניקוי נתונים</h1>'
         '<p>שלוש שאלות אמיתיות: סולם מדידה, סוג החוסר, ומה duplicated מחזיר.</p>', layout="title")

plan = Scene("plan", "איך ניגשים", [
    P("לפני שמתחילים, שיטת עבודה אחת לכל שלוש השאלות.", do=show("p-1")),
    P("קודם מזהים על מה שואלים: סולם, חוסר, או פקודה של pandas.", do=show("p-2"),
      say="קודם מזהים על מה שואלים: סולם, חוסר, או פקודה של פַּנְדָס."),
    P("אחר כך בודקים כל אפשרות לחוד, ונותנים סיבה לפסילה. ובשאלת קוד, הכי בטוח להריץ דוגמה קטנה.", do=show("p-3"),
      hold=0.3),
], stage=w.stack(st.card("p-1", "plain", "שלוש שאלות · שלושה נושאים"),
                 st.card("p-2", "ex", "1 · מזהים את הנושא"),
                 st.card("p-3", "ex", "2 · פוסלים כל אפשרות עם סיבה · 3 · בקוד: מריצים דוגמה"), gap=24),
   panel=st.card("p-c", "rule", "🔑 תשובה בלי סיבה היא ניחוש"))
plan.phrases[-1].do += show("p-c")

q1 = Scene("q1", "שאלה 1: סולם", [
    P("שאלה ראשונה: מהו הסולם המתאים ביותר למשתנה ״ידע קודם בסטטיסטיקה״?"),
    P("איך נראים הערכים? משהו כמו: אין ידע, בסיסי, טוב, מצוין.", do=show("a-v")),
    P("יש ביניהם סדר ברור: מצוין יותר מטוב, וטוב יותר מבסיסי. לכן זה לא סולם שמי.", do=show("al-r0", "al-r1", "q1-x-0", "q1-n-0")),
    P("האם המרווחים שווים? האם הפער בין בסיסי לטוב שווה לפער בין טוב למצוין? אין שום דרך לדעת.", do=show("al-r2")),
    P("ואין אפס אמיתי: ״אין ידע״ הוא קצה של דירוג, ולא כמות שאפשר להכפיל. לכן זה לא סולם מנה.",
      do=show("al-r3", "q1-x-2", "q1-n-2")),
    P("יש סדר, ואין מרווחים שווים: סולם **סדר**. ומה מותר לחשב עליו? שכיח וחציון.", do=show("q1-ok-1", "a-c")),
    P("למשל, בכיתה של חמישה סטודנטים אפשר למיין את רמות הידע ולמצוא את האמצעית. זה החציון."),
    P("אבל ״ממוצע הידע הוא 2.6״ לא אומר כלום, בדיוק כמו הממוצע של מידות חולצה.", hold=0.4,
      say="אבל ממוצע הידע הוא שתיים נקודה שש, לא אומר כלום, בדיוק כמו הממוצע של מידות חולצה."),
], stage=w.stack(w.big("a-v", " · ".join(LEVELS), size=46).replace('class="cl-big', 'dir="rtl" class="cl-big'),
                 w.ladder("al", hidden=True), gap=30),
   panel=w.stem(Q1["id"], "מהו הסולם המתאים ביותר למשתנה ״ידע קודם בסטטיסטיקה״?")
         + st.options("q1", O1, notes={0: "יש סדר", 2: "אין אפס אמיתי"})
         + st.card("a-c", "rule", "🔑 סדר ← שכיח וחציון"))

q2 = Scene("q2", "שאלה 2: סוג החוסר", [
    P("שאלה שנייה: ״נתוני גיל חסרים באופן אקראי״, מול ״נתוני גיל חסרים עבור אנשים שנולדו לפני 1980״.",
      say="שאלה שנייה: נתוני גיל חסרים באופן אקראי, מול נתוני גיל חסרים עבור אנשים שנולדו לפני אלף תשע מאות ושמונים."),
    P("איזה הבדל בין סוגי חוסר הם ממחישים? נבדוק כל משפט בנפרד."),
    P("המשפט הראשון: החוסר אקראי, לא תלוי בשום דבר. זה MCAR.", do=show("b-0"),
      say="המשפט הראשון: החוסר אקראי, לא תלוי בשום דבר. זה אֶם סִי אֵיי אָר."),
    P("המשפט השני: החוסר תלוי בשנת הלידה. שנת הלידה היא משתנה **אחר**, ואנחנו יודעים אותו.", do=show("b-1")),
    P("חוסר שתלוי במשתנה אחר שנמדד הוא MAR.", do=show("b-2"), say="חוסר שתלוי במשתנה אחר שנמדד הוא אֶם אֵיי אָר."),
    P("כאן שנת הלידה נרשמה בטבלה, ולכן זה MAR. אילו לא נרשמה, זה היה MNAR.",
      say="כאן שנת הלידה נרשמה בטבלה, ולכן זה אֶם אֵיי אָר. אילו לא נרשמה, זה היה אֶם אֶן אֵיי אָר."),
    P("זה לא MNAR: שם החוסר תלוי בערך החסר עצמו, למשל אנשים שמסתירים את הגיל **בגלל** הגיל שלהם.",
      do=show("b-3", "q2-x-0", "q2-n-0", "q2-x-1", "q2-n-1"),
      say="זה לא אֶם אֶן אֵיי אָר: שם החוסר תלוי בערך החסר עצמו, למשל אנשים שמסתירים את הגיל בגלל הגיל שלהם."),
    P("לכן התשובה: MCAR מול MAR.", do=show("q2-ok-2"), say="לכן התשובה: אֶם סִי אֵיי אָר מול אֶם אֵיי אָר."),
    P("ולמה זה חשוב? כי ב-MAR המשתנה האחר מסביר את החוסר: אפשר לראות בטבלה מי חסר ולמה.",
      say="ולמה זה חשוב? כי באֶם אֵיי אָר המשתנה האחר מסביר את החוסר: אפשר לראות בטבלה מי חסר ולמה."),
    P("אם נמחק את השורות החסרות, נאבד דווקא את המבוגרים, והנתונים שנשארו כבר לא מייצגים את כולם.", hold=0.4),
], stage=w.stack(
    st.card("b-0", "ex", "״חסרים באופן אקראי״ ← <bdi class=\"cl-mono\">MCAR</bdi>"),
    st.card("b-1", "ex", "״חסרים למי שנולד לפני 1980״ ← תלוי בשנת הלידה, שנמדדה"),
    st.card("b-2", "rule", "🔑 תלוי במשתנה <b>אחר</b> שנמדד ← <bdi class=\"cl-mono\">MAR</bdi>"),
    st.card("b-3", "trap", "⚠️ <bdi class=\"cl-mono\">MNAR</bdi>: תלוי בערך החסר <b>עצמו</b>"), gap=22),
   panel=w.stem(Q2["id"], "״גיל חסר באופן אקראי״ מול ״גיל חסר למי שנולד לפני 1980״: אילו שני סוגי חוסר זה ממחיש?")
         + st.options("q2", O2, notes={0: "אין MNAR", 1: "אין MNAR"}))

q3 = Scene("q3", "שאלה 3: duplicated", [
    P("שאלה שלישית: מה מתקיים לגבי הפקודה df.duplicated()?", say="שאלה שלישית: מה מתקיים לגבי הפקודה דִי אֶף דּוּפְּלִיקֵייטֵד?"),
    P("נריץ אותה על טבלה של חמש שורות ושלוש עמודות, ונראה מה חוזר.", do=show("c-code")),
    P("חוזרת Series באורך חמש: ערך True או False **לכל שורה**.", do=show("c-out", "c-v"),
      say="חוזרת סִירִיז באורך חמש: ערך טְרוּ או פוֹלְס לכל שורה."),
    P("לכן התשובה היא וקטור באורך מספר השורות.", do=show("q3-ok-1")),
    P("לא באורך מספר העמודות: לטבלה שלוש עמודות, והווקטור באורך חמש.", do=show("q3-x-2", "q3-n-2")),
    P("לא סכום: את הסכום מקבלים רק אם מוסיפים sum.", do=show("q3-x-0", "q3-n-0"),
      say="לא סכום: את הסכום מקבלים רק אם מוסיפים סָאם."),
    P("ולא True אחד לכל הטבלה: הפקודה עונה על כל שורה בנפרד.", do=show("q3-x-3", "q3-n-3"),
      say="ולא טְרוּ אחד לכל הטבלה: הפקודה עונה על כל שורה בנפרד."),
    P("בטבלה שלנו השורה השלישית זהה לגמרי לראשונה, ולכן רק היא קיבלה True.",
      say="בטבלה שלנו השורה השלישית זהה לגמרי לראשונה, ולכן רק היא קיבלה טְרוּ."),
    P("והשורה החמישית חולקת עם הראשונה את הערכים בשתי עמודות, ובכל זאת קיבלה False: עמודה אחת שונה מספיקה.",
      say="והשורה החמישית חולקת עם הראשונה את הערכים בשתי עמודות, ובכל זאת קיבלה פוֹלְס: עמודה אחת שונה מספיקה.",
      hold=0.4),
], stage=w.stack(w.code("c-code", MAKE, hidden=True, size=24), w.out("c-out", OUT3, size=28),
                 w.big("c-v", " ".join(str(v) for v in D), size=34), gap=24),
   panel=w.stem(Q3["id"], "עבור דטה פריים בשם df, מה מתקיים לגבי הפקודה df.duplicated()?")
         + st.options("q3", O3, notes={0: "צריך sum", 2: "שורות", 3: "לכל שורה"}))

recap = Scene("recap", "סיכום", [
    P("סיכום המסלול: סולם המדידה קובע מה מותר לחשב. סדר בלי מרווחים שווים: שכיח וחציון.", do=show("r-1")),
    P("חסרים מוצאים עם isnull().sum(), וממלאים לפי סוג העמודה. וסוג החוסר: אקראי, תלוי במשתנה אחר, או בערך עצמו.",
      do=show("r-2")),
    P("כפילויות: duplicated() מחזיר וקטור, אחד לכל שורה. וחריג הוא סימן לבדוק, לא שגיאה. בהצלחה במבחן!",
      do=show("r-3"), hold=0.6),
], stage=w.ladder("lr", hidden=False),
   panel=st.card("r-1", "rule", "🔑 סדר ← שכיח וחציון")
         + st.card("r-2", "rule", "🔑 MCAR · MAR · MNAR")
         + st.card("r-3", "rule", "🔑 " + w.mono("duplicated()") + " ← וקטור באורך השורות"))

SCENES = [title, plan, q1, q2, q3, recap]
w.no_latin(SCENES)
VIDEO = Video("C07", "clean", "מבחן גמר: ניקוי נתונים", SCENES, bank={"P-15": 1, "P-19": 2, "P-43": 1})

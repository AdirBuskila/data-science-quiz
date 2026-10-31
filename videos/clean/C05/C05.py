# -*- coding: utf-8 -*-
"""C05 · קידוד קטגוריות ו-binning — video script (build: tools/video/vid.py C05).

Source: courses/clean/C05.js (lesson + goal: turn a categorical variable into dummy variables, cut a continuous
variable into bins, and know what is gained and lost). Exam anchor: 26A-B-Q20 (why Pclass 1/2/3 is turned into
dummy variables although it is already numeric), which no guided quiz uses.
Avoided on purpose: the C05 quiz items (id + color -> 4 columns, the Status row, ages with bins 0/12/19/34/120,
21 and 29 in one bin, y = e^x and log; no two scores are shown sharing a bin), the boss item 26A-B-Q24 (Embarked -> 3 columns), its twin 26B-A-Q21 and
26A-B-Q19 (its key cites "a 12-year-old and a 19-year-old" in one bin, which the lesson's bins 0/12/19/… put in two
different bins). Worked data are mine: payments with 4 methods (1 + 4 = 5 columns), Israeli area codes 2/3/4 as
category labels, exam scores cut at 54 / 79. Every table and printed output is produced by running the code shown.
"""
import numpy as np
import pandas as pd

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_clean as w

# ---------------------------------------------------------------- one-hot (run)
MAKE = "df = pd.DataFrame({'amount': [40, 15, 90, 25],\n                   'pay': ['card', 'cash', 'app', 'check']})"
env, _ = w.run(MAKE)
df = env["df"]
DUM_SRC = "dum = pd.get_dummies(df, columns=['pay'], dtype=int)"
env, _ = w.run(DUM_SRC, env)
dum = env["dum"]
assert list(dum.columns) == ["amount", "pay_app", "pay_card", "pay_cash", "pay_check"] and dum.shape == (4, 5)
assert (dum.iloc[:, 1:].sum(axis=1) == 1).all() and set(np.unique(dum.iloc[:, 1:].values)) == {0, 1}
assert dum.loc[0, "pay_card"] == 1 and dum.loc[2, "pay_app"] == 1
HOT = [(i, j) for i in range(4) for j in range(1, 5) if dum.iat[i, j] == 1]
assert HOT == [(0, 2), (1, 3), (2, 1), (3, 4)]
assert all(t == bool for t in pd.get_dummies(df, columns=["pay"]).dtypes.iloc[1:])   # default dtype: True/False

# area codes as labels: a linear model weight w forces "04" to have twice the effect of "02"
AREA = {"02": "ירושלים", "03": "תל אביב", "04": "חיפה"}
wgt = 1.7
assert 4 * wgt == 2 * (2 * wgt)

# ---------------------------------------------------------------- binning (run)
CUT_SRC = "sc = pd.Series([54, 55, 79, 80, 100])\nprint(pd.cut(sc, bins=[0, 54, 79, 100]).astype(str).tolist())"
envc, CUT_OUT = w.run(CUT_SRC)
assert CUT_OUT == "['(0, 54]', '(54, 79]', '(54, 79]', '(79, 100]', '(79, 100]']"
CUT_TXT = CUT_OUT.replace(", '(", ",\n '(")

# ---------------------------------------------------------------- exam 26A-B-Q20
Q = BANK["26A-B-Q20"]
assert Q["correctIndex"] == 0 and "פי שלוש" in Q["options"][0]
pcl = pd.Series([1, 3, np.nan, 2])
pd_ = pd.get_dummies(pcl, dtype=int)
assert pd_.iloc[2].sum() == 0 and pd_.shape[1] == 3          # a missing value is not handled: an all-zero row
assert sorted(pd_.sum().tolist()) == [1, 1, 1]                 # one column per class, no order between them
OPTS = [(k, f'<span style="font-size:27px;line-height:1.3">{o}</span>') for k, o in enumerate(Q["options"])]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד להפוך עמודה של קטגוריות לעמודות של אפס ואחת."),
    P("נראה למה מספר שהוא רק שם צריך את אותו טיפול, ונחלק משתנה רציף לסלים."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">C05 · ניקוי נתונים וסולמות</div><h1>קידוד קטגוריות ו-binning</h1>'
         '<p>להמיר משתנה קטגוריאלי למשתני דמה, לחלק משתנה רציף לסלים, ולדעת מה מרוויחים ומה מפסידים.</p>',
   layout="title")

onehot = Scene("onehot", "get_dummies", [
    P("מודל למידה מחשב עם מספרים. מה עושים עם עמודה של אמצעי תשלום: כרטיס, מזומן, אפליקציה, צ׳ק?", do=show("o-a")),
    P("הפתרון: get_dummies. הוא מחליף את העמודה בעמודה **בינארית** לכל ערך.", do=show("o-code")),
    P("ארבעה ערכים, ולכן ארבע עמודות חדשות. העמודה המקורית נעלמת, ועמודת הסכום, amount, נשארת.",
      say="ארבעה ערכים, ולכן ארבע עמודות חדשות. העמודה המקורית נעלמת, ועמודת הסכום, אָמָאוּנְט, נשארת.", do=show("o-b")),
    P("בכל שורה בדיוק אחת מהן שווה אחת: זו שמתאימה לערך של השורה.", do=show(*w.ids("o-b", "h", HOT))),
    P("השיטה נקראת One-Hot. ושימו לב: היא לא מניחה שום סדר בין האמצעים.", do=show("o-c1")),
    P("ספירת עמודות: עמודה אחת שנשארה, ועוד ארבע חדשות. בסך הכול חמש.", do=show("o-c2")),
    P("עוד פרט קטן: בלי dtype שווה int, גרסאות חדשות של pandas מציגות True ו-False במקום אחת ואפס.",
      do=show("o-c3"), hold=0.3,
      say="עוד פרט קטן: בלי דִי טַייפּ שווה אִינְט, גרסאות חדשות של פַּנְדָס מציגות טְרוּ ופוֹלְס במקום אחת ואפס."),
    P("ובשאלות המבחן מתייחסים לזה כאפס ואחת."),
], stage=w.stack(w.frame("o-a", df, size=26, cw=130, hidden=True),
                 w.code("o-code", DUM_SRC, hidden=True, size=24),
                 w.frame("o-b", dum, size=24, cw=150, hidden=True), gap=22),
   panel=st.card("o-c1", "rule", "🔑 One-Hot: עמודה לכל ערך, ובכל שורה בדיוק 1 אחד")
         + st.card("o-c2", "ex", "1 עמודה שנשארה + 4 חדשות = 5")
         + st.card("o-c3", "ex", "ברירת מחדל ← " + w.mono("True / False") + "<br>עם " + w.mono("dtype=int") + " ← " + w.mono("1 / 0")))

labels = Scene("labels", "מספר שהוא שם", [
    P("ומה אם הקטגוריות כבר כתובות כמספרים? למשל קידומת טלפון: שתיים, שלוש, ארבע.", do=show("a-t")),
    P("שתיים זה ירושלים, שלוש תל אביב, וארבע חיפה. המספר הוא רק שם של אזור."),
    P("זה בדיוק סולם שמי, כמו שראינו ברמה הראשונה.", do=show("a-c0")),
    P("אבל מודל לינארי מכפיל את העמודה במשקל. ואז ההשפעה של ארבע היא פי שתיים מזו של שתיים.", do=show("a-m")),
    P("המודל ״יחליט״ שחיפה היא פעמיים ירושלים. זה לא נכון, וזה לא אומר כלום.", do=show("a-c1")),
    P("לכן גם עמודה כזו מקודדים ב-One-Hot: עמודה לכל אזור, ולכל אחת משקל משלה.", do=show("a-c2"), hold=0.3),
], stage=w.stack(
    '<table class="cl-df h" id="a-t" dir="rtl" style="font-size:32px;font-family:\'Segoe UI\'"><thead><tr><th>קידומת</th><th>אזור</th></tr></thead><tbody>'
    + "".join(f'<tr><td class="cl-mono">{k}</td><td>{v}</td></tr>' for k, v in AREA.items()) + "</tbody></table>",
    w.big("a-m", "w · 4 = 2 · (w · 2)", size=44), gap=40),
   panel=st.card("a-c0", "plain", "קידומת = <b>שם</b>, סולם שמי")
         + st.card("a-c1", "trap", "⚠️ מספר לא הופך שם לכמות: 4 אינו ״פי 2״ מ-2")
         + st.card("a-c2", "rule", "🔑 קטגוריות במספרים? גם הן ← משתני דמה"))

binning = Scene("binning", "binning", [
    P("ועכשיו הכיוון ההפוך: משתנה רציף שרוצים לחלק ל**סלים**. זה נקרא binning.", say="ועכשיו הכיוון ההפוך: משתנה רציף שרוצים לחלק לסלים. זה נקרא בִּינִינְג."),
    P("ציוני מבחן, ושלושה סלים: נכשל עד 54, עובר עד 79, וטוב עד מאה.", do=show("b-code"),
      say="ציוני מבחן, ושלושה סלים: נכשל עד חמישים וארבע, עובר עד שבעים ותשע, וטוב עד מאה."),
    P("pd.cut מחזיר לכל ציון את הסל שלו. וכל סל **כולל את הגבול העליון** שלו, ולא את התחתון.", do=show("b-out"),
      say="פִּי דִי קָאט מחזיר לכל ציון את הסל שלו. וכל סל כולל את הגבול העליון שלו, ולא את התחתון."),
    P("לכן 54 נכנס לסל הנכשלים, ו-55 כבר בסל הבא. סוגר מרובע אומר ״כולל״, סוגר עגול ״לא כולל״.", do=show("b-c1"),
      say="לכן חמישים וארבע נכנס לסל הנכשלים, וחמישים וחמש כבר בסל הבא. סוגר מרובע אומר כולל, סוגר עגול לא כולל."),
    P("מה מרוויחים? משתנה פשוט יותר, עם מעט ערכים. ומה מפסידים? **רזולוציה**.", do=show("b-c2"), hold=0.3),
], stage=w.stack(w.code("b-code", CUT_SRC, hidden=True, size=24), w.out("b-out", CUT_TXT, size=28), gap=26),
   panel=st.card("b-c1", "rule", "🔑 " + w.mono("(54, 79]") + ": בלי 54, כולל 79")
         + st.card("b-c2", "ex", "רווח: פשטות · הפסד: רזולוציה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: עמודת המחלקה בטיטניק מכילה אחת, שתיים ושלוש. למה להמיר אותה למשתני דמה?",
      do=show("x-0")),
    P("מחלקה היא סולם סדר: יש סדר, אבל 3 אינו פי 3 מ-1 והמרווחים לא מובטחים, לכן לא משאירים אותה כמספר.",
      do=show("x-1"),
      say="מחלקה היא סולם סדר: יש סדר, אבל שלוש אינו פי שלוש מאחת, והמרווחים לא מובטחים. לכן לא משאירים אותה כמספר."),
    P("בלי קידוד, המודל יסיק שמחלקה שלוש ״גדולה״ פי שלוש ממחלקה אחת. זו התשובה.", do=show("q-ok-0")),
    P("״האלגוריתם לא קורא מספרים שלמים״? הוא קורא אותם מצוין. הבעיה היא מה הם אומרים, לא הסוג שלהם.",
      do=show("q-x-1", "q-n-1")),
    P("האותיות Q, C ו-S? הן שייכות לעמודה אחרת, נמל העלייה. במחלקה יש רק מספרים.", do=show("q-x-2", "q-n-2"),
      say="האותיות קְיוּ, סִי ואֶס? הן שייכות לעמודה אחרת, נמל העלייה. במחלקה יש רק מספרים."),
    P("ו-get_dummies לא יוצר סדר. להפך: הוא מוחק אותו. וגם בחסרים הוא לא מטפל: שורה חסרה מקבלת רק אפסים.",
      do=show("q-x-3", "q-n-3", "x-2")),
    P("המלכודת: ״זה כבר מספר, אז זה בסדר״. השאלה היא תמיד מה המספר מודד.", do=show("x-t"), hold=0.5),
], stage=w.stack(
    w.stem(Q["id"], "Pclass מכילה 1, 2, 3. למה להמיר אותה למשתני דמה לפני האימון, אף שהיא כבר מספרית?"),
    st.card("x-1", "rule", "🔑 מחלקה = סולם <b>סדר</b>: 3 אינו פי 3 מ-1, המרווחים לא מובטחים"),
    w.big("x-0", "class 3 ≠ 3 × class 1", size=40),
    w.out("x-2", str(pd_), size=24, label="pd.get_dummies(pd.Series([1, 3, np.nan, 2]), dtype=int)"),
    st.card("x-t", "trap", "⚠️ ״כבר מספר״ לא אומר ״כמות״"), gap=16),
   panel=st.options("q", OPTS, notes={1: "קורא", 2: "עמודה אחרת", 3: "לא סדר"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: get_dummies מחליף עמודה קטגורית בעמודה בינארית לכל ערך, ובכל שורה בדיוק אחת דולקת.", do=show("r-1")),
    P("קטגוריות שכתובות כמספרים מקודדים בדיוק אותו דבר, כי המספר הוא רק שם.", do=show("r-2")),
    P("ו-binning: pd.cut, הסל כולל את הגבול העליון, ומשלמים ברזולוציה. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6,
      say="ובִּינִינְג: פִּי דִי קָאט, הסל כולל את הגבול העליון, ומשלמים ברזולוציה. נתראה ברמה הבאה."),
], stage=w.frame("r", dum, size=26, cw=150),
   panel=st.card("r-1", "rule", "🔑 " + w.mono("get_dummies") + " ← עמודה לכל ערך")
         + st.card("r-2", "rule", "🔑 מספר שהוא שם ← גם הוא משתני דמה")
         + st.card("r-3", "rule", "🔑 " + w.mono("pd.cut") + " ← " + w.mono("(a, b]") + " · מחיר: רזולוציה"))

SCENES = [title, onehot, labels, binning, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("C05", "clean", "קידוד קטגוריות ו-binning", SCENES, bank={"26A-B-Q20": 0})

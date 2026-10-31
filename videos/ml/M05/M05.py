# -*- coding: utf-8 -*-
"""M05 · אימון ובדיקה, KNN ושגיאת רגרסיה — video script (build: tools/video/vid.py M05).

Source: courses/ml/M05.js (lesson + goal: why we split into train and test, predicting with KNN, SSE and R²).
Exam anchor: 25A-A-Q21 (what K means in KNN: the number of neighbours taken into account), which no guided quiz uses.
Not used on purpose: the M05 quiz data (1,2,3 = A, 10,11 = B, the query 7 with k = 3 / 5; actual 3,5,7 vs 2,5,9;
actual 1,2,3,4 vs 1.5,1.5,3.5,3.5) and the boss item 26A-A-Q5 (the "not true" statement about the split). The
video explains why a test set is needed but never answers that question's statements one by one.
Worked examples (new): 1-NN scores 100% on its own training points (asserted with sklearn); a 2-D KNN with nine
training points and the query (5,5), where k = 1 says B and k = 3 says A; a line ŷ = 1 + 2x fitted (least squares)
on five training points and tested on four new ones: SSE = 4, R² = 0.875. Everything asserted against sklearn.
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_ml as w

# ---------------------------------------------------------------- KNN (verified)
A = [(4, 4), (5, 3), (2, 3), (3, 1), (1, 2)]
B = [(6, 5), (7, 7), (8, 5), (8, 8)]
TR = A + B
LB = ["A"] * len(A) + ["B"] * len(B)
Q0 = (5, 5)
d1, n1, v1, _ = w.knn_vote(TR, LB, Q0, 1)
d3, n3, v3, votes3 = w.knn_vote(TR, LB, Q0, 3)
assert v1 == "B" and v3 == "A" and votes3 == {"B": 1, "A": 2}
assert [TR[i] for i in n3] == [(6, 5), (4, 4), (5, 3)]
assert [round(d, 2) for d, _ in d3[:4]] == [1, 1.41, 2, 2.83]
for k, want in ((1, "B"), (3, "A")):
    assert KNeighborsClassifier(k).fit(np.array(TR, float), LB).predict([Q0])[0] == want
# 1-NN on its own training points: always right (each point is its own nearest neighbour, at distance 0)
assert KNeighborsClassifier(1).fit(np.array(TR, float), LB).score(np.array(TR, float), LB) == 1.0
K3_TRAIN = KNeighborsClassifier(3).fit(np.array(TR, float), LB).score(np.array(TR, float), LB)

# ---------------------------------------------------------------- regression (verified)
XT, YT = [0, 1, 2, 3, 4], [1.5, 2.5, 5, 6.5, 9.5]                # training set
lr = LinearRegression().fit(np.array(XT, float).reshape(-1, 1), YT)
assert np.isclose(lr.intercept_, 1) and np.isclose(lr.coef_[0], 2)
XS, YS = [1, 2, 3, 4], [2, 6, 6, 10]                              # test set
PRED = [1 + 2 * x for x in XS]
assert np.allclose(lr.predict(np.array(XS, float).reshape(-1, 1)), PRED) and PRED == [3, 5, 7, 9]
RES = [y - p for y, p in zip(YS, PRED)]
assert RES == [-1, 1, -1, 1]
SSE = sum(r * r for r in RES)
YBAR = sum(YS) / len(YS)
SST = sum((y - YBAR) ** 2 for y in YS)
assert SSE == 4 and YBAR == 6 and SST == 32 and 1 - SSE / SST == 0.875
assert np.isclose(r2_score(YS, PRED), 0.875)

# exam 25A-A-Q21
Q = BANK["25A-A-Q21"]
assert Q["correctIndex"] == 0 and "השכנים" in Q["options"][0] and "הקלסטרים" in Q["options"][1]
assert "עץ ההחלטה" in Q["options"][2] and "קצב הלמידה" in Q["options"][3]
OPTS = list(enumerate(Q["options"]))

# ---------------------------------------------------------------- figures
K = w.Plot("kn", (0, 10), (0, 10), w=560, h=540, xticks=range(0, 11, 2), yticks=range(0, 11, 2))
K.circle("c1", *Q0, 1.0, kind="b")
K.circle("c3", *Q0, 2.0, kind="a")
K.segs("l1", [(Q0, TR[n1[0]])], kind="b")
K.segs("l3", [(Q0, TR[i]) for i in n3], kind="a")
K.pts("pa", A, "a")
K.pts("pb", B, "b", shapes="tttt")
K.pts("q", [Q0], "ink", r=11)
K.text("tq", *Q0, "?", kind="ink", dx=-22, dy=-14)
KPLOT = K.svg()

R = w.Plot("rg", (0, 5), (0, 12), w=560, h=520, xticks=range(0, 6), yticks=range(0, 13, 2))
R.pts("tr", list(zip(XT, YT)), "mut", r=10)
R.fline("fit", 1, 2, kind="b", hidden=False)
R.segs("res", [((x, y), (x, p)) for x, y, p in zip(XS, YS, PRED)], kind="bad")
R.pts("ts", list(zip(XS, YS)), "a", hidden=True)
R.fline("mean", YBAR, 0, kind="c")
R.text("tl", 4.6, 10.2, "ŷ = 1 + 2x", kind="b", anchor="end", dy=-40)
RPLOT = R.svg()

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד למה מפצלים את הנתונים לאימון ולבדיקה."),
    P("נסווג נקודה חדשה עם KNN, ונמדוד שגיאה של רגרסיה עם SSE ועם $R^2$."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">M05 · מודלים והערכה</div><h1>אימון ובדיקה, KNN ושגיאת רגרסיה</h1>'
         '<p>להבין למה מפצלים ל-train ו-test, לחזות בעזרת KNN, ולחשב SSE ו-R².</p>', layout="title")

split = Scene("split", "אימון ובדיקה", [
    P("מודל לומד מנתונים. אבל איך יודעים אם הוא באמת טוב?"),
    P("אם בודקים אותו על אותם נתונים שהוא למד מהם, אפשר לקבל ציון מושלם, בלי שהמודל למד שום דבר אמיתי."),
    P("הנה דוגמה קיצונית: KNN עם שכן אחד, שבודקים אותו על נקודות האימון שלו.", do=show("s-1"),
      say="הנה דוגמה קיצונית: קֵיי אֶן אֶן עם שכן אחד, שבודקים אותו על נקודות האימון שלו."),
    P("כשאין נקודות כפולות, כל נקודה היא השכן הכי קרוב של עצמה, במרחק אפס. לכן הדיוק מאה אחוז.", do=show("s-2")),
    P("זה שינון, לא למידה. ומודל שמשנן את האימון ונכשל על נתונים חדשים, הוא **overfitting**.",
      say="זה שינון, לא למידה. ומודל שמשנן את האימון ונכשל על נתונים חדשים, הוא אוֹבֶרְפִיטִינְג.", do=show("s-3"), hold=0.3),
    P("בקוד, פונקציית הפיצול מחזירה ארבעה חלקים: מאפיינים ותוויות לאימון, ומאפיינים ותוויות לבדיקה.", do=show("s-4"), hold=0.4),
], stage='<div class="ml-col">' + w.code("s-c", "X_train, X_test, y_train, y_test = \\\n    train_test_split(X, y, <b>test_size=0.2</b>)", size=28)
         + w.chip("s-1", "KNN עם שכן אחד, נבדק על נקודות האימון", "info") + w.chip("s-2", "דיוק = 100%", "warn") + "</div>",
   panel=st.card("s-3", "trap", "⚠️ ציון על האימון לא מוכיח כלום: אפשר לשנן")
         + st.card("s-4", "ex", "<code>test_size=0.2</code>: עשרים אחוז מהשורות בצד"))

knn = Scene("knn", "KNN", [
    P("עכשיו KNN, שכנים קרובים. יש לנו נקודות אימון עם תוויות: עיגולים כחולים הם A, משולשים צהובים הם B.",
      say="עכשיו קֵיי אֶן אֶן, שכנים קרובים. יש לנו נקודות אימון עם תוויות: עיגולים כחולים הם אֵיי, משולשים צהובים הם בִּי."),
    P("מגיעה נקודה חדשה, חמש, חמש. מה התווית שלה?", do=show("kn-tq")),
    P("הכלל: מוצאים את k נקודות האימון **הקרובות ביותר**, והן מצביעות. התווית הנפוצה מנצחת.", do=show("n-1"),
      say="הכלל: מוצאים את קֵיי נקודות האימון הקרובות ביותר, והן מצביעות. התווית הנפוצה מנצחת."),
    P("עם k שווה אחת: השכן הכי קרוב הוא המשולש בשש, חמש, במרחק אחת. התשובה: B.", do=show("kn-c1", "kn-l1", "n-2"),
      say="עם קֵיי שווה אחת: השכן הכי קרוב הוא המשולש בשש, חמש, במרחק אחת. התשובה: בִּי."),
    P("עם k שווה שלוש מצטרפים עוד שני שכנים: עיגול במרחק שורש שתיים, ועיגול במרחק שתיים.",
      do=hide("kn-c1", "kn-l1") + show("kn-c3", "kn-l3"),
      say="עם קֵיי שווה שלוש מצטרפים עוד שני שכנים: עיגול במרחק שורש שתיים, ועיגול במרחק שתיים."),
    P("ההצבעה: שני עיגולים מול משולש אחד. התשובה עכשיו: A.", do=show("n-3"),
      say="ההצבעה: שני עיגולים מול משולש אחד. התשובה עכשיו: אֵיי.", hold=0.3),
    P("אותם נתונים, אותה נקודה, ותשובה אחרת. k הוא **מספר השכנים** שמצביעים, ובוחרים אותו אנחנו.", do=show("n-k"),
      say="אותם נתונים, אותה נקודה, ותשובה אחרת. קֵיי הוא מספר השכנים שמצביעים, ובוחרים אותו אנחנו."),
    P("ושימו לב: KNN כמעט לא עושה כלום באימון. כל החישוב קורה כשמגיעה נקודה חדשה.", do=show("n-l"), hold=0.4,
      say="ושימו לב: קֵיי אֶן אֶן כמעט לא עושה כלום באימון. כל החישוב קורה כשמגיעה נקודה חדשה."),
], stage=f'<div class="ml-rowc">{KPLOT}</div>',
   panel=st.card("n-1", "rule", "🔑 KNN: $k$ השכנים הקרובים מצביעים")
         + st.card("n-2", "ex", "$k=1$: משולש במרחק $1$ ← <b>B</b>")
         + st.card("n-3", "ex", "$k=3$: $1$, $\\sqrt{2}$, $2$ ← שני עיגולים ← <b>A</b>")
         + st.card("n-k", "rule", "🔑 $k$ = מספר השכנים שנלקחים בחשבון")
         + st.card("n-l", "ex", "KNN ״עצלן״: החישוב בזמן החיזוי"))

reg = Scene("reg", "שגיאת רגרסיה", [
    P("ועכשיו רגרסיה. על נקודות האימון האפורות התאמנו קו: $\hat{y} = 1 + 2x$.",
      say="ועכשיו רגרסיה. על נקודות האימון האפורות התאמנו קו: וַואי שווה אחת ועוד פעמיים אִקְס.", do=show("rg-tl")),
    P("בודקים אותו על ארבע נקודות חדשות, בכחול.", do=hide("rg-tr") + show("rg-ts")),
    P("בכל נקודה, השגיאה היא ההפרש בין הערך האמיתי לחזוי. כאן כל השגיאות הן אחת או מינוס אחת.", do=show("rg-res", "g-1")),
    P("**SSE** הוא סכום ריבועי השגיאות: ארבע פעמים אחת, כלומר 4.", do=show("g-2"),
      say="אֶס אֶס אִי הוא סכום ריבועי השגיאות: ארבע פעמים אחת, כלומר ארבע."),
    P("אבל האם 4 זה הרבה? משווים למודל הכי טיפשי: לחזות תמיד את הממוצע, שש.", do=show("rg-mean", "g-3"),
      say="אבל האם ארבע זה הרבה? משווים למודל הכי טיפשי: לחזות תמיד את הממוצע, שש."),
    P("סכום ריבועי ההפרשים מהממוצע: 16, אפס, אפס ו-16. יחד 32.", do=show("g-4"),
      say="סכום ריבועי ההפרשים מהממוצע: שש עשרה, אפס, אפס ושש עשרה. יחד שלושים ושתיים."),
    P("$R^2$ הוא אחת פחות היחס: אחת פחות 4 חלקי 32, כלומר 0.875.", do=show("g-5"),
      say="אָר בריבוע הוא אחת פחות היחס: אחת פחות ארבע חלקי שלושים ושתיים, כלומר אפס נקודה שמונה מאות שבעים וחמש."),
    P("כלומר, המודל מסביר 87.5 אחוז מהשונות של וַואי. אחת זה מושלם, ואפס זה לא יותר טוב מהממוצע.", do=show("g-k"),
      say="כלומר, המודל מסביר שמונים ושבעה וחצי אחוז מהשונות של וַואי. אחת זה מושלם, ואפס זה לא יותר טוב מהממוצע.", hold=0.4),
], stage=f'<div class="ml-rowc">{RPLOT}<div class="ml-col" style="width:430px">'
         + w.eq("g-1", "$y - \\hat{y}:\\ -1,\\ 1,\\ -1,\\ 1$", 32)
         + w.eq("g-2", "$\\text{SSE} = 4$", 34)
         + w.eq("g-3", "$\\bar{y} = 6$", 34)
         + w.eq("g-4", "$\\text{SS}_{tot} = 16+0+0+16 = 32$", 30)
         + w.eq("g-5", "$R^2 = 1 - \\dfrac{4}{32} = 0.875$", 34) + "</div></div>",
   panel=st.card("g-k", "rule", "🔑 $R^2 = 1 - \\dfrac{\\text{SSE}}{\\text{SS}_{tot}}$: חלק השונות שהמודל מסביר"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה המטרה של k באלגוריתם KNN?",
      say="שאלה ממבחן: מה המטרה של קֵיי באלגוריתם קֵיי אֶן אֶן?"),
    P("ראינו את זה עכשיו: k קובע כמה שכנים קרובים מצביעים. שכן אחד נתן B, שלושה נתנו A.", do=show("q-ok-0"),
      say="ראינו את זה עכשיו: קֵיי קובע כמה שכנים קרובים מצביעים. שכן אחד נתן בִּי, שלושה נתנו אֵיי.", hold=0.3),
    P("המלכודת היא ״מספר הקלסטרים״. זה ה-k של K-Means, אלגוריתם אחר לגמרי.", do=show("q-x-1", "q-n-1", "x-t"),
      say="המלכודת היא מספר הקלסטרים. זה הקֵיי של קֵיי מִינְס, אלגוריתם אחר לגמרי."),
    P("K-Means לא מונחה, ומחלק לקבוצות. KNN מונחה: הוא משתמש בתוויות של השכנים, ולא בונה קבוצות.",
      say="קֵיי מִינְס לא מונחה, ומחלק לקבוצות. קֵיי אֶן אֶן מונחה: הוא משתמש בתוויות של השכנים, ולא בונה קבוצות."),
    P("עומק העץ שייך לעץ החלטה. ב-KNN אין עץ.", do=show("q-x-2", "q-n-2"),
      say="עומק העץ שייך לעץ החלטה. בקֵיי אֶן אֶן אין עץ."),
    P("וקצב למידה שייך לאלגוריתמים שמתקדמים בצעדים באימון. KNN לא לומד בצעדים: הוא רק שומר את הנקודות.",
      do=show("q-x-3", "q-n-3"), hold=0.6,
      say="וקצב למידה שייך לאלגוריתמים שמתקדמים בצעדים באימון. קֵיי אֶן אֶן לא לומד בצעדים: הוא רק שומר את הנקודות."),
], stage=w.stem(Q["id"], "מה המטרה של K באלגוריתם KNN (K-Nearest Neighbors)?")
         + f'<div class="ml-opts">{st.options("q", OPTS, notes={1: "זה K-Means", 2: "עץ החלטה", 3: "אין צעדי אימון"})}</div>',
   panel=st.card("x-t", "trap", "⚠️ שני אלגוריתמים עם k: ב-<b>KNN</b> שכנים, ב-<b>K-Means</b> אשכולות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ציון מושלם על נקודות האימון יכול להיות שינון בלבד, כמו אצל שכן אחד.", do=show("r-1")),
    P("KNN: k השכנים הקרובים מצביעים, ו-k משנה את התשובה.", do=show("r-2"),
      say="קֵיי אֶן אֶן: קֵיי השכנים הקרובים מצביעים, וקֵיי משנה את התשובה."),
    P("SSE הוא סכום ריבועי השגיאות, ו-$R^2$ הוא אחת פחות SSE חלקי סכום הריבועים סביב הממוצע.", do=show("r-3"),
      say="אֶס אֶס אִי הוא סכום ריבועי השגיאות, ואָר בריבוע הוא אחת פחות אֶס אֶס אִי חלקי סכום הריבועים סביב הממוצע."),
    P("ו-k של KNN הוא לא ה-k של K-Means. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6,
      say="וקֵיי של קֵיי אֶן אֶן הוא לא הקֵיי של קֵיי מִינְס. נתראה ברמה הבאה."),
], stage='<div class="ml-col">' + w.eq("r-eq", "$R^2 = 1 - \\dfrac{\\sum (y-\\hat{y})^2}{\\sum (y-\\bar{y})^2}$", 46, hidden=False) + "</div>",
   panel=st.card("r-1", "trap", "⚠️ 1-NN על נקודות האימון: 100%, שינון")
         + st.card("r-2", "rule", "🔑 KNN: $k$ = מספר השכנים")
         + st.card("r-3", "rule", "🔑 SSE = $\\sum (y-\\hat{y})^2$")
         + st.card("r-4", "trap", "⚠️ $k$ של KNN ≠ $k$ של K-Means"))

VIDEO = Video("M05", "ml", "אימון ובדיקה, KNN ושגיאת רגרסיה", [title, split, knn, reg, exam, recap],
              bank={"25A-A-Q21": 0})

# -*- coding: utf-8 -*-
"""M07 · מבחן גמר: מודלים והערכה (boss) — video script (build: tools/video/vid.py M07).

A walkthrough of three exam questions that the M07 boss quiz does NOT use (its six are 24A-A-Q17, 26B-A-Q14,
25A-B-Q21, 26A-A-Q5, 25A-B-Q18, 26A-B-Q16; none of them, nor their twins 26A-A-Q21 / 24A-B-Q12, is solved here):
  26B-A-Q16  fill the blanks of a train / fit / predict snippet (key 0: fit, predicted, m, predict, X_test)
  26A-B-Q15  what the False Negative cell means for students (key 0: predicted fail, actually passed)
  25A-A-Q16  hierarchical vs non-hierarchical clustering (key 0: a tree first vs direct assignment)
Checked here: the sklearn API facts (LinearRegression has fit / predict and no fit_predict / transform /
fit_transform; fit returns the model itself; predict takes only X), the cell name of every option of 26A-B-Q15,
and that scipy's hierarchical tree is built without a number of clusters and cut afterwards. 25A-B-Q20 (FP up:
which metric won't show it) was dropped: its reasoning is the same inference as the boss item 26A-B-Q16; the video
also never says who sets K-Means' k (boss 25A-B-Q21).
"""
import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_ml as w

# ---------------------------------------------------------------- Q1: 26B-A-Q16 (verified)
Q1 = BANK["26B-A-Q16"]
assert Q1["correctIndex"] == 0 and Q1["options"][0] == "VVVV=fit; WWWW=predicted; XXXX=m; YYYY=predict; ZZZZ=X_test"
m0 = LinearRegression()
assert hasattr(m0, "fit") and hasattr(m0, "predict")
assert not any(hasattr(m0, a) for a in ("fit_predict", "fit_transform", "transform"))
rng = np.random.default_rng(0)
Xd = rng.normal(size=(50, 2))
yd = Xd @ [3, -1] + 2
X_train, X_test, y_train, y_test = train_test_split(Xd, yd, test_size=0.20, random_state=0)
assert len(X_test) == 10 and len(X_train) == 40
m = LinearRegression().fit(X_train, y_train)
assert isinstance(m, LinearRegression)                       # fit returns the fitted model itself
predicted = m.predict(X_test)
assert predicted.shape == (10,)
try:
    m.predict(X_test, y_test)                                # predict does not take the labels
    raise AssertionError("predict accepted y")
except TypeError:
    pass
OPT1 = [(i, o.replace("; ", " · ")) for i, o in enumerate(Q1["options"])]

# ---------------------------------------------------------------- Q2: 26A-B-Q15 (verified)
Q2 = BANK["26A-B-Q15"]
assert Q2["correctIndex"] == 0 and "False Negative" in Q2["question"]


def cell(pred_pos, actual_pos):
    """name of a confusion-matrix cell: second letter = the prediction, first letter = right or wrong"""
    return ("T" if pred_pos == actual_pos else "F") + ("P" if pred_pos else "N")


# positive class = passed. Each option as (predicted passed?, actually passed?)
OPT_CELLS = [(False, True), (False, False), (True, True), (True, False)]
assert [cell(*c) for c in OPT_CELLS] == ["FN", "TN", "TP", "FP"]
assert "שיכשלו" in Q2["options"][0] and "בפועל הם עברו" in Q2["options"][0]
assert "שיכשלו" in Q2["options"][1] and "בפועל הם נכשלו" in Q2["options"][1]
assert "שיעברו" in Q2["options"][2] and "בפועל הם עברו" in Q2["options"][2]
assert "שיעברו" in Q2["options"][3] and "בפועל הם נכשלו" in Q2["options"][3]
OPT2 = list(enumerate(Q2["options"]))

# ---------------------------------------------------------------- Q3: 25A-A-Q16 (verified)
Q3 = BANK["25A-A-Q16"]
assert Q3["correctIndex"] == 0 and "דמוי עץ" in Q3["options"][0] and "labeled" in Q3["options"][3]
Xc = np.array([[1], [2], [6], [7], [15]], float)
Z = linkage(Xc, "single")                                     # the whole tree, no number of clusters given
assert Z.shape == (4, 4)
assert fcluster(Z, 2, "maxclust").tolist() == [1, 1, 1, 1, 2] and fcluster(Z, 3, "maxclust").tolist() == [1, 1, 2, 2, 3]
assert "n_clusters" in KMeans().get_params()                    # k is an argument of the K-Means constructor
assert len(set(KMeans(2, n_init=10, random_state=0).fit_predict(Xc))) == 2
OPT3 = list(enumerate(Q3["options"]))

# ---------------------------------------------------------------- figures
RAST = st.raster("cr", "images/exams/26B-A-Q16.png", 900, (807, 214))
CM2 = w.cmatrix("sm", "", "", "", "", pos="עבר", neg="נכשל", size=30, values=False)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של הקורס: שלוש שאלות אמיתיות ממבחנים קודמים."),
    P("קוד של אימון וחיזוי, תא במטריצת בלבול, ושני סוגי אשכול."),
    P("בכל שאלה נבדוק כל אפשרות, ונסביר למה היא נכונה או שגויה.", hold=0.4),
], stage='<div class="kicker">M07 · מודלים והערכה</div><h1>מבחן גמר: מודלים והערכה</h1>'
         '<p>שלוש שאלות ממבחנים: train / test בקוד, מטריצת בלבול, ואשכול היררכי מול K-Means.</p>', layout="title")

q1a = Scene("q1a", "שאלה 1: הקוד", [
    P("שאלה ראשונה. בקוד הזה, רגרסיה לינארית, חסרים חמישה קטעים. צריך להשלים אותם."),
    P("שורה שלוש מפצלת: שמונים אחוז לאימון, ועשרים אחוז לבדיקה.", do=show("c-1")),
    P("בשורה ארבע מאמנים, על נתוני האימון ועל התוויות שלהם. הפעולה היא **fit**.", do=show("c-2"),
      say="בשורה ארבע מאמנים, על נתוני האימון ועל התוויות שלהם. הפעולה היא פִיט."),
    P("ו-fit מחזירה את המודל עצמו, אחרי האימון. לכן m הוא המודל המאומן.", do=show("c-3"),
      say="ופִיט מחזירה את המודל עצמו, אחרי האימון. לכן אֶם הוא המודל המאומן."),
    P("בשורה חמש חוזים: m נקודה predict, על נתוני הבדיקה בלבד, בלי התוויות.", do=show("c-4"),
      say="בשורה חמש חוזים: אֶם נקודה פְּרֶדִיקְט, על נתוני הבדיקה בלבד, בלי התוויות."),
    P("את התוויות של הבדיקה שומרים בצד, כדי להשוות אליהן את החיזוי ולמדוד שגיאה.", hold=0.4),
], stage=f'<div class="ml-col">{RAST}'
         + w.code("c-ans", "m = LinearRegression().<b>fit</b>(X_train, y_train)\n<b>predicted</b> = <b>m</b>.<b>predict</b>(<b>X_test</b>)", size=28)
         + "</div>",
   panel=st.card("c-1", "ex", "<code>test_size=0.20</code>: 20% לבדיקה")
         + st.card("c-2", "rule", "🔑 מאמנים: <b>fit</b> על train")
         + st.card("c-3", "ex", "fit מחזירה את המודל ← <b>m</b>")
         + st.card("c-4", "rule", "🔑 חוזים: <b>predict</b> על X_test בלבד"))

q1b = Scene("q1b", "שאלה 1: האפשרויות", [
    P("עכשיו האפשרויות. זו שבה fit, predicted, m, predict ו-X_test מתאימה בדיוק למה שמצאנו.", do=show("a-ok-0"),
      say="עכשיו האפשרויות. זו שבה פִיט, פְּרֶדִיקְטֶד, אֶם, פְּרֶדִיקְט, ואִקְס טֶסְט, מתאימה בדיוק למה שמצאנו."),
    P("האפשרות עם fit_predict נופלת: לרגרסיה לינארית אין פעולה כזו, ו-predict לא מקבלת את התוויות.", do=show("a-x-1", "a-n-1"),
      say="האפשרות עם פִיט פְּרֶדִיקְט נופלת: לרגרסיה לינארית אין פעולה כזו, ופְּרֶדִיקְט לא מקבלת את התוויות."),
    P("האפשרות עם fit_transform ו-transform נופלת: אלה פעולות של כלי עיבוד, כמו PCA, לא של מודל רגרסיה.", do=show("a-x-3", "a-n-3"),
      say="האפשרות עם פִיט טְרַנְסְפוֹרְם וטְרַנְסְפוֹרְם נופלת: אלה פעולות של כלי עיבוד, כמו פִּי סִי אֵיי, לא של מודל רגרסיה."),
    P("והאפשרות עם m2 מאמנת מודל **חדש** על נתוני הבדיקה. אין שם חיזוי בכלל.", do=show("a-x-2", "a-n-2"),
      say="והאפשרות עם אֶם שתיים מאמנת מודל חדש על נתוני הבדיקה. אין שם חיזוי בכלל."),
    P("ולכן נשארת רק האפשרות עם fit ו-predict.", do=show("b-t"), hold=0.6,
      say="ולכן נשארת רק האפשרות עם פִיט ופְּרֶדִיקְט."),
], stage=f'<div class="ml-opts" style="width:100%">{st.options("a", OPT1, notes={1: "אין fit_predict", 2: "מאמן על test", 3: "אין transform"})}</div>',
   panel=st.card("b-t", "trap", "⚠️ predict מקבלת רק מאפיינים, בלי תוויות"))

q2 = Scene("q2", "שאלה 2: מטריצת בלבול", [
    P("שאלה שנייה: מודל חוזה אם סטודנטים יעברו את הקורס. החיובי הוא ״עבר״. מה מייצג התא False Negative?",
      say="שאלה שנייה: מודל חוזה אם סטודנטים יעברו את הקורס. החיובי הוא עבר. מה מייצג התא, שלילי כוזב?"),
    P("קוראים את השם מהסוף. האות השנייה, N, היא מה שהמודל חזה: שלילי, כלומר ״ייכשל״.", do=show("sm-h-fn", "s-1"),
      say="קוראים את השם מהסוף. האות השנייה, אֶן, היא מה שהמודל חזה: שלילי, כלומר ייכשל."),
    P("האות הראשונה, F, אומרת שהמודל טעה. אז במציאות הסטודנט דווקא עבר.", do=show("s-2"),
      say="האות הראשונה, אֶף, אומרת שהמודל טעה. אז במציאות הסטודנט דווקא עבר."),
    P("וזו בדיוק האפשרות: חזה שייכשלו, ובפועל עברו.", do=show("o-ok-0"), hold=0.3),
    P("חזה שייכשלו ובאמת נכשלו: המודל צדק, וזה שלילי אמיתי.", do=show("o-x-1", "o-n-1")),
    P("חזה שיעברו ובאמת עברו: חיובי אמיתי.", do=show("o-x-2", "o-n-2")),
    P("וחזה שיעברו אבל נכשלו: זו טעות בכיוון ההפוך, חיובי כוזב.", do=show("o-x-3", "o-n-3")),
    P("המלכודת: ״שלילי״ מתאר את **החיזוי**, לא את המציאות.", do=show("s-t"), hold=0.6),
], stage='<div class="ml-col">' + CM2
         + st.card("s-1", "ex", "האות השנייה $N$: המודל חזה <b>נכשל</b>")
         + st.card("s-2", "ex", "האות הראשונה $F$: הוא <b>טעה</b>, כלומר עבר")
         + st.card("s-t", "trap", "⚠️ שלילי = מה שהמודל <b>חזה</b>") + "</div>",
   panel=w.stem(Q2["id"], "מה מייצג התא False Negative (FN) בהקשר של הסטודנטים והקורס?")
         + f'<div class="ml-opts">{st.options("o", OPT2, notes={1: "TN", 2: "TP", 3: "FP"})}</div>')

q3 = Scene("q3", "שאלה 3: סוגי אשכול", [
    P("שאלה שלישית: מה ההבדל בין אשכול היררכי לאשכול לא היררכי, כמו K-Means?",
      say="שאלה שלישית: מה ההבדל בין אשכול היררכי לאשכול לא היררכי, כמו קֵיי מִינְס?"),
    P("אשכול היררכי בונה קודם עץ של מיזוגים, דנדרוגרם, ורק אחר כך חותכים אותו לקבוצות.", do=show("h-1")),
    P("K-Means לא בונה עץ: הוא משייך כל נקודה ישירות לאחד מ-k המרכזים.", do=show("h-2", "h-ok-0"),
      say="קֵיי מִינְס לא בונה עץ: הוא משייך כל נקודה ישירות לאחד מקֵיי המרכזים.", hold=0.3),
    P("האפשרות שבהיררכי יש הנחה מוקדמת על מספר הקלסטרים שגויה: בהיררכי לא צריך מספר כדי לבנות את העץ. בוחרים אותו בחיתוך.",
      do=show("h-x-1", "h-n-1")),
    P("״לא היררכי רק על נתונים קטנים״: לא נכון. K-Means דווקא רץ מהר גם על הרבה נתונים.", do=show("h-x-2", "h-n-2"),
      say="לא היררכי רק על נתונים קטנים: לא נכון. קֵיי מִינְס דווקא רץ מהר גם על הרבה נתונים."),
    P("ותוויות? שני הסוגים הם אשכול, כלומר למידה לא מונחית. אף אחד מהם לא צריך תוויות.", do=show("h-x-3", "h-n-3")),
    P("המלכודת: בהיררכי העץ נבנה בלי לדעת כמה קבוצות רוצים. המספר נקבע רק כשחותכים.", do=show("h-t"), hold=0.6),
], stage=w.stem(Q3["id"], "מה ההבדל בין קלסטרינג היררכי לעומת קלסטרינג לא היררכי?")
         + f'<div class="ml-opts">{st.options("h", OPT3, notes={1: "העץ בלי מספר", 2: "לא נכון", 3: "שניהם בלי תוויות"})}</div>',
   panel=st.card("h-1", "ex", "היררכי: עץ מיזוגים ← חיתוך")
         + st.card("h-2", "ex", "K-Means: שיוך ישיר ל-k מרכזים")
         + st.card("h-t", "trap", "⚠️ היררכי: העץ נבנה בלי מספר, והמספר נקבע בחיתוך"))

recap = Scene("recap", "סיכום", [
    P("לסיכום שלוש השאלות. בקוד: fit על האימון, ו-predict על נתוני הבדיקה בלבד.", do=show("r-1"),
      say="לסיכום שלוש השאלות. בקוד: פִיט על האימון, ופְּרֶדִיקְט על נתוני הבדיקה בלבד."),
    P("במטריצת בלבול: האות השנייה היא החיזוי, והראשונה אומרת אם הוא נכון.", do=show("r-2")),
    P("ובאשכול: היררכי בונה עץ וחותך, ו-K-Means משייך כל נקודה ישירות למרכז.", do=show("r-3"),
      say="ובאשכול: היררכי בונה עץ וחותך, וקֵיי מִינְס משייך כל נקודה ישירות למרכז."),
    P("עכשיו תורכם: שש השאלות של מבחן הגמר מחכות באפליקציה. בהצלחה!", do=show("r-4"), hold=0.6),
], stage='<div class="ml-col">' + w.code("rc", "m = Model().<b>fit</b>(X_train, y_train)\npred = m.<b>predict</b>(X_test)", size=32)
         + "</div>",
   panel=st.card("r-1", "rule", "🔑 fit על train, predict על X_test")
         + st.card("r-2", "rule", "🔑 $FN$: חזה <b>שלילי</b>, וטעה")
         + st.card("r-3", "rule", "🔑 היררכי: עץ וחיתוך. K-Means: שיוך ישיר")
         + st.card("r-4", "ex", "🏆 שש שאלות גמר מחכות באפליקציה"))

VIDEO = Video("M07", "ml", "מבחן גמר: מודלים והערכה", [title, q1a, q1b, q2, q3, recap],
              bank={"26B-A-Q16": 0, "26A-B-Q15": 0, "25A-A-Q16": 0})

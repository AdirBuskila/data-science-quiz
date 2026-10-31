# -*- coding: utf-8 -*-
"""T08 · מבחן גמר: ביטויים רגולריים וטקסט — boss walkthrough (build: tools/video/vid.py T08).

Source: courses/text/T08.js (boss). The boss quiz uses P-61, P-62, P-65, 24A-B-Q4, 26A-B-Q4, 25-S-Q4: none of them is
solved here. Walkthrough of three other exam questions: 26A-B-Q9 (what ? after * or + changes), 26A-A-Q20 (what
stop words are; its twin 25A-B-Q23 is not used), 26B-A-Q12 (what a vectorizer is). T07 used 25A-A-Q23, T05 P-66.
Avoided: every quiz question of T01..T07 (own strings only) and the content twins P-63/P-64/25A-A-Q12.
Every regex result is a real re.search on the string shown; the idf numbers come from sklearn's TfidfVectorizer.
"""
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx, L

# ---------------------------------------------------------------- 26A-B-Q9: ? after * or +
Q1 = BANK["26A-B-Q9"]
assert Q1["correctIndex"] == 0
S1 = "id 2026 ok"
RUNS = [(r"\d+", "2026"), (r"\d+?", "2"), (r"\d*", ""), (r"\d*?", "")]
for p, exp in RUNS:
    assert re.search(p, S1).group() == exp, p
assert re.search(r"\d*", S1).span() == (0, 0)          # the empty match comes from *, with or without ?
assert re.search(r"\d+?", S1).span() == (3, 4)         # +? still needs one digit: never empty
assert re.fullmatch(r"\d+?", "2026")                   # and it does not force the whole string either
LAY1 = [("a1", 3, 7, "m"), ("a2", 3, 4, "g1"), ("a3", 0, 0, "nil")]
O1 = [(i, w.esc(o)) for i, o in enumerate(Q1["options"])]
O1 = [O1[i] for i in [1, 0, 3, 2]]

# ---------------------------------------------------------------- 26A-A-Q20: stop words
Q2 = BANK["26A-A-Q20"]
assert Q2["correctIndex"] == 0
DOCS = ["the sun is hot", "the moon is cold", "the sky is blue"]
tf = TfidfVectorizer().fit(DOCS)
IDF = dict(zip(tf.get_feature_names_out(), tf.idf_))
assert IDF["the"] == IDF["is"] == min(IDF.values()) < IDF["sun"]   # in every document -> the LOWEST idf
assert round(IDF["the"], 3) == 1.0 and round(IDF["sun"], 3) == 1.693
O2 = [(i, w.esc(o)) for i, o in enumerate(Q2["options"])]
O2 = [O2[i] for i in [2, 0, 3, 1]]

# ---------------------------------------------------------------- 26B-A-Q12: vectorizer
Q3 = BANK["26B-A-Q12"]
assert Q3["correctIndex"] == 0
v = Normalizer(norm="l2").fit_transform([[3.0, 4.0]])
assert np.allclose(v, [[0.6, 0.8]])                    # L1/L2 unit vectors: that is a Normalizer, not a vectorizer
O3 = [(i, w.esc(o)) for i, o in enumerate(Q3["options"])]
O3 = [O3[i] for i in [3, 1, 0, 2]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של הקורס. נעבור יחד על שלוש שאלות אמיתיות ממבחנים."),
    P("אחת על ביטויים רגולריים, ושתיים על הפיכת טקסט למספרים."),
    P("בכל שאלה נמצא את התשובה, ונפסול כל מסיח עם סיבה.", hold=0.4),
], stage='<div class="kicker">T08 · ביטויים רגולריים וטקסט</div><h1>מבחן גמר: ביטויים רגולריים וטקסט</h1>'
         '<p>שלוש שאלות ממבחנים: סימן שאלה אחרי כמת, מילות עצירה, ומהו vectorizer.</p>', layout="title")

q1 = Scene("q1", "שאלה 1", [
    P("שאלה ראשונה: מה משנה סימן שאלה שבא אחרי כוכבית או פלוס?"),
    P("ארבע אפשרויות: התאמה קצרה ביותר, ביטוי אופציונלי, התאמה ריקה, או התאמה של המחרוזת כולה.", hold=0.1),
    P("נבדוק על טקסט. ספרה ופלוס, חמדן: תופס את כל ארבע הספרות.", do=show("s1", "a1", "k-c0", "k-r0")),
    P("עם סימן שאלה אחרי הפלוס: רק ספרה אחת. ההתאמה **הקצרה ביותר** שאפשר.", do=show("a2", "k-c1", "k-r1")),
    P("הפלוס עדיין דורש לפחות ספרה אחת. סימן השאלה רק אומר לו לעצור כמה שיותר מוקדם.", hold=0.1),
    P("אז התשובה: הוא מחפש את ההתאמה הקצרה ביותר.", do=show("q1-ok-0")),
    P("האם הוא הופך את כל הביטוי לאופציונלי? לא. הוא חל רק על הכמת שלפניו, וההתאמה עדיין חייבת ספרה.", do=show("q1-x-1")),
    P("האם הוא מאפשר התאמה ריקה? נבדוק. ספרה וכוכבית, **בלי** סימן שאלה, כבר מוצאת התאמה ריקה בהתחלה.",
      do=show("a3", "k-c2", "k-r2")),
    P("עם סימן שאלה, אותו דבר. ההתאמה הריקה באה מהכוכבית, לא מסימן השאלה. ועם פלוס, ריקה אף פעם לא.",
      do=show("k-c3", "k-r3", "q1-x-2")),
    P("והתאמה של כל המחרוזת? את זה עושים כובע ודולר, לא סימן שאלה.", do=show("q1-x-3"), hold=0.6),
], stage='<div class="tx-stack">' + w.code("s1c", f's = "{S1}"', hidden=False, size=40)
         + w.strip("s1", S1, LAY1, hidden=True, cw=54)
         + w.calls("k", [(f're.search(r"{p}", s).group()', repr(e)) for p, e in RUNS]) + "</div>",
   panel='<div class="tx-dense">' + f'<div class="qstem"><span class="qid">{Q1["id"]}</span>{w.esc(Q1["question"])}</div>' + st.options("q1", O1) + "</div>")

q2 = Scene("q2", "שאלה 2", [
    L("שאלה שנייה: מהן [[stop words|סְטוֹפּ ווֹרְדְס]]?"),
    L("אלו מילים **שכיחות מאוד**, כמו [[the|דָה]] ו-[[is|אִיז]], שבדרך כלל מסננים מהטקסט לפני הניתוח.", do=show("q2-ok-0")),
    P("לא מילים שגויות דקדוקית: אלה דווקא המילים הכי תקינות ונפוצות שיש.", do=show("q2-x-1")),
    P("ולא מילים שבאות בסוף משפט. המיקום לא קובע, השכיחות קובעת.", do=show("q2-x-2")),
    P("למה מסננים אותן? כי הן מופיעות כמעט בכל מסמך, ולכן לא עוזרות להבדיל בין מסמכים.", hold=0.1),
    P("והמסיח שנשאר, ציון גבוה בשיטה שנותנת משקל למילים נדירות. נבדוק על שלושה משפטים.", do=show("tf")),
    L("המשקל של מילה יורד ככל שהיא מופיעה ביותר מסמכים. [[the|דָה]] ו-[[is|אִיז]] נמצאות בכולם, ולכן מקבלות את המשקל **הנמוך** ביותר.",
      do=show("tf-c0", "tf-r0", "tf-c1", "tf-r1")),
    P("כלומר מילות עצירה מקבלות ציון **נמוך**, לא גבוה. ולכן גם המסיח הזה נפסל.", do=show("q2-x-3"), hold=0.6),
], stage='<div class="tx-stack">' + "".join(w.code(f"d{i}", f'"{d}"', hidden=False, size=32) for i, d in enumerate(DOCS))
         + w.calls("tf", [("idf['the'], idf['is']", f"{IDF['the']:.2f}, {IDF['is']:.2f}"),
                          ("idf['sun'], idf['sky']", f"{IDF['sun']:.2f}, {IDF['sky']:.2f}")]).replace(
             'class="tx-calls"', 'class="tx-calls h"') + "</div>",
   panel='<div class="tx-dense">' + f'<div class="qstem"><span class="qid">{Q2["id"]}</span>{w.esc(Q2["question"])}</div>' + st.options("q2", O2) + "</div>")

q3 = Scene("q3", "שאלה 3", [
    L("שאלה שלישית: מהו [[vectorizer|וֶקְטוֹרַייזֶר]]?"),
    P("ראינו אותו ברמה הקודמת: הוא מקבל נתון **גולמי**, למשל טקסט, ומחזיר וקטור של מאפיינים מספריים.", do=show("v-1")),
    P("את הווקטור הזה אפשר להזין למודל של למידת מכונה. זו התשובה.", do=show("q3-ok-0")),
    P("שלושת המסיחים מתארים פעולות אמיתיות, אבל של כלים אחרים. נעבור עליהם.", hold=0.1),
    P("המרה של נתונים בסקלות שונות לאותה סקלה? זה **נרמול סקלה**, פעולה על מספרים שכבר יש.", do=show("v-2", "q3-x-1")),
    P("המרה של מטריצת נתונים? הקלט של הכלי הוא טקסט גולמי, לא מטריצה. המטריצה היא **הפלט** שלו.", do=show("q3-x-2")),
    P("והפיכת וקטורים לוקטורי יחידה? גם זה נרמול: למשל שלוש וארבע הופכים לשש עשיריות ושמונה עשיריות.",
      do=show("v-3", "q3-x-3"), hold=0.6),
], stage='<div class="tx-stack">' + st.card("v-1", "ex", "טקסט גולמי ← " + rx("vectorizer") + " ← וקטור מספרים ← מודל")
         + st.card("v-2", "plain", "נרמול סקלה: מספרים ← מספרים באותה סקלה")
         + st.card("v-3", "plain", "וקטור יחידה: " + rx("[3, 4] → [0.6, 0.8]")) + "</div>",
   panel='<div class="tx-dense">' + f'<div class="qstem"><span class="qid">{Q3["id"]}</span>{w.esc(Q3["question"])}</div>' + st.options("q3", O3) + "</div>")

recap = Scene("recap", "סיכום", [
    P("לסיכום שלוש השאלות: סימן שאלה אחרי כמת הופך אותו לעצלן, להתאמה הקצרה ביותר.", do=show("r-1")),
    P("מילות עצירה הן מילים שכיחות מאוד שמסננים, ומשקלן נמוך.", do=show("r-2")),
    P("ומה שהופך טקסט גולמי לווקטור מספרי הוא הכלי שראינו ברמה הקודמת.", do=show("r-3")),
    P("ובכל שאלת ביטוי רגולרי: מריצים את התבנית על הטקסט, משמאל לימין. בהצלחה במבחן!", do=show("r-4"), hold=0.8),
], stage='<div class="tx-stack">' + w.calls("rk", [(r're.search(r"\d+", s).group()', "'2026'"),
                                                  (r're.search(r"\d+?", s).group()', "'2'")], shown=(0, 1)) + "</div>",
   panel=st.card("r-1", "rule", "🔑 " + rx("+?") + " " + rx("*?") + " = הקצרה ביותר")
         + st.card("r-2", "rule", "🔑 " + rx("stop words") + " = שכיחות, מסוננות")
         + st.card("r-3", "rule", "🔑 " + rx("vectorizer") + ": טקסט ← וקטור")
         + st.card("r-4", "trap", "⚠️ לא מנחשים: מריצים על הטקסט"))

VIDEO = w.no_latin(Video("T08", "text", "מבחן גמר: ביטויים רגולריים וטקסט", [title, q1, q2, q3, recap],
                         bank={"26A-B-Q9": 0, "26A-A-Q20": 0, "26B-A-Q12": 0}))

# -*- coding: utf-8 -*-
"""T07 · מטקסט למספרים: Bag of Words — video script (build: tools/video/vid.py T07).

Source: courses/text/T07.js (lesson + goal). Exam anchor: 25A-A-Q23 (which NLP tool turns text into numeric data
for ML: CountVectorizer), used by no guided quiz.
Avoided on purpose: the T07 quiz documents ("the cat sat" / "the cat the dog", "red fox" / "blue fox" / "red sky",
"dog bites man") and their numbers; the vectorizer / stop-word bank items 24A-A-Q14, 26B-A-Q12, 25A-B-Q23,
26A-A-Q20 (two of them are kept for the T08 walkthrough).
Every vocabulary, count, shape and stop-word removal below comes from sklearn's CountVectorizer (the same tool the
course checker runs) on the exact documents shown.
"""
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx, L

# ---------------------------------------------------------------- the corpus (verified)
DOCS = ["big data is big", "data science is fun", "science is big"]
VOC, X = w.vectorize(DOCS)
assert VOC == ["big", "data", "fun", "is", "science"]                  # every distinct word, sorted
assert X == [[2, 1, 0, 1, 0], [0, 1, 1, 1, 1], [1, 0, 0, 1, 1]]
assert (len(X), len(VOC)) == (3, 5)                                    # shape: a row per document, a column per word
VOC2, X2 = w.vectorize(DOCS, stop_words="english")
assert VOC2 == ["big", "data", "fun", "science"] and "is" in ENGLISH_STOP_WORDS
assert [wd for wd in VOC if wd in ENGLISH_STOP_WORDS] == ["is"]
assert X2 == [[r[j] for j in (0, 1, 2, 4)] for r in X]                 # same counts, the 'is' column is gone
_, XO = w.vectorize(["data is big", "big is data"])
assert XO[0] == XO[1]                                                  # word order is lost
WORDS = [t for d in DOCS for t in d.split()]
assert sorted(set(WORDS)) == VOC and len(WORDS) == 11

# a new document through the fitted vocabulary: unknown words are dropped
from sklearn.feature_extraction.text import CountVectorizer
_cv = CountVectorizer().fit(DOCS)
NEW = "fun fun data is cool"
XN = _cv.transform([NEW]).toarray()[0].tolist()
assert XN == [0, 1, 2, 1, 0] and "cool" not in VOC                     # 'cool' has no column: ignored
assert [r[3] for r in X] == [1, 1, 1]                                  # 'is' is in every document

# ---------------------------------------------------------------- exam 25A-A-Q23
Q = BANK["25A-A-Q23"]
assert Q["correctIndex"] == 0 and Q["options"][0] == "CountVectorizer"
OPTS = [(i, rx(o)) for i, o in enumerate(Q["options"])]
OPTS = [OPTS[i] for i in [1, 2, 0, 3]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("אלגוריתם של למידת מכונה לא יודע לקרוא. הוא מקבל רק מספרים."),
    P("בסרטון הזה נראה איך הופכים מסמכים של טקסט לטבלה של מספרים, בשיטה שנקראת שק מילים."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">T07 · ביטויים רגולריים וטקסט</div><h1>מטקסט למספרים: Bag of Words</h1>'
         '<p>להבין איך CountVectorizer הופך מסמכים לווקטורים, מה גודל המטריצה, ומה עושים stop words.</p>',
   layout="title")

vocab = Scene("vocab", "אוצר המילים", [
    P("יש לנו שלושה מסמכים קצרים.", do=show("v-docs")),
    P("צעד ראשון: מפרקים כל מסמך למילים. יש כאן אחת עשרה מילים בסך הכול.", do=show("tk")
      + show(*[f"tk-w{i}" for i in range(len(WORDS))])),
    P("צעד שני: **אוצר המילים**. כל מילה **שונה** נכנסת פעם אחת, ממוינת לפי סדר האלף בית.", do=show("vc")
      + show(*[f"vc-w{i}" for i in range(len(VOC))])),
    P("יצאו חמש מילים. כל מילה כזו תהיה **עמודה** בטבלה.", do=show("v-c1"), hold=0.4),
], stage='<div class="tx-stack">' + "".join(w.code(f"v-d{i}", f'"{d}"', hidden=False, size=34) for i, d in enumerate(DOCS))
         .join(['<div id="v-docs" class="tx-stack h">', "</div>"])
         + w.chips("tk", WORDS) + '<div class="tx-cap">↓</div>' + w.chips("vc", VOC) + "</div>",
   panel=st.card("v-c1", "rule", "🔑 אוצר מילים = כל המילים <b>השונות</b>, ממוינות"))

matrix = Scene("matrix", "המטריצה", [
    L("[[CountVectorizer|קַאוּנְט וֶקְטוֹרַייזֶר]] בונה מטריצה: **שורה לכל מסמך**, ועמודה לכל מילה באוצר.", do=show("bw")),
    P("בכל תא: כמה פעמים המילה של העמודה מופיעה במסמך של השורה.", do=show("bw-row0")),
    L("במסמך הראשון, [[big|בִּיג]] מופיעה **פעמיים**. ולכן בתא שלה: שתיים.", do=show("bw-col0", "bw-v0-0")),
    P("ושאר השורה: אחת, אפס, אחת, אפס. מילה שלא מופיעה במסמך מקבלת אפס.",
      do=hide("bw-col0") + show(*[f"bw-v0-{j}" for j in range(1, 5)])),
    P("וכך לכל מסמך. השורה של המסמך היא **הווקטור** שלו.", do=hide("bw-row0") + w.row_do("bw", 1, 5) + w.row_do("bw", 2, 5)),
    L("ועכשיו נקרא עמודה: [[is|אִיז]] מופיעה פעם אחת בכל אחד משלושת המסמכים. נחזור לזה עוד מעט.", do=show("bw-col3")),
    P("ושימו לב: מספר האפסים גדל מהר. במסמכים אמיתיים יש אלפי מילים, ורוב התאים הם אפס.", do=hide("bw-col3")),
    P("גודל המטריצה: שלוש שורות, כמספר המסמכים, וחמש עמודות, כמספר המילים השונות.", do=show("m-shape", "m-c1"), hold=0.4),
], stage='<div class="tx-stack">' + w.bow("bw", DOCS, VOC, X) + w.out("m-shape", f"X.shape = {(len(X), len(VOC))}") + "</div>",
   panel=st.card("m-c1", "rule", "🔑 צורה = (מסמכים, מילים שונות)"))

stop = Scene("stop", "מילות עצירה", [
    L("יש מילים שמופיעות כמעט בכל מסמך, כמו [[is|אִיז]], [[the|דָה]] ו-[[and|אֶנְד]]. הן לא עוזרות להבדיל בין מסמכים.", do=show("s-c1")),
    L("קוראים להן [[stop words|סְטוֹפּ ווֹרְדְס]], מילות עצירה, ובדרך כלל **מסננים** אותן.", do=show("s-code")),
    L("כאן [[is|אִיז]] נמצאת ברשימה האנגלית של מילות העצירה, אז העמודה שלה נמחקת.", do=show("vs", *[f"vs-w{i}" for i in range(5)], "vs-s3")),
    P("נשארות ארבע עמודות. הספירות של שאר המילים לא משתנות.", do=show("s-out", "s-c2")),
    P("ועוד דבר ששק מילים מאבד: את **הסדר**. שני משפטים עם אותן מילים בסדר אחר מקבלים אותו וקטור בדיוק.", do=show("s-c3"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("s-code", "CountVectorizer(stop_words='english')", size=34)
         + w.chips("vs", VOC) + w.out("s-out", f"{VOC2}   shape = {(len(X2), len(VOC2))}", size=30) + "</div>",
   panel=st.card("s-c1", "ex", "מילים נפוצות מאוד: " + rx("is, the, and"))
         + st.card("s-c2", "rule", "🔑 מסננים ← אוצר מילים קטן יותר")
         + st.card("s-c3", "trap", "⚠️ שק מילים מתעלם מהסדר"))

new = Scene("new", "מסמך חדש", [
    P("ומה עם מסמך חדש, אחרי שאוצר המילים כבר נבנה?", do=show("n-code")),
    P("סופרים לפי **אותן חמש עמודות**, באותו סדר.", hold=0.1),
    L("[[fun|פַאן]] פעמיים, [[data|דֵאטָה]] ו-[[is|אִיז]] פעם אחת. ולכן הווקטור: אפס, אחת, שתיים, אחת, אפס.", do=show("nb", "n-out")),
    L("והמילה [[cool|קוּל]]? אין לה עמודה באוצר המילים, ולכן היא פשוט **לא נספרת**.", do=show("n-c1")),
    P("הווקטור תמיד באורך של אוצר המילים, לא באורך המסמך.", do=show("n-c2"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("n-code", f'cv.transform(["{NEW}"])', size=34)
         + w.bow("nb", [NEW], VOC, [XN], hide_vals=False).replace('class="tx-bow"', 'class="tx-bow h"')
         + w.out("n-out", repr(XN)) + "</div>",
   panel=st.card("n-c1", "trap", "⚠️ מילה שאינה באוצר: לא נספרת")
         + st.card("n-c2", "rule", "🔑 אורך הווקטור = גודל אוצר המילים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: איזה כלי יכול להמיר טקסט לנתונים מספריים שמתאימים ללמידת מכונה?"),
    L("זה בדיוק מה שראינו: [[CountVectorizer|קַאוּנְט וֶקְטוֹרַייזֶר]] הופך מסמכים למטריצה של ספירות.", do=show("q-ok-0")),
    L("[[Tokenizer|טוֹקְנַייזֶר]] רק **מפרק** טקסט למילים. זה הצעד הראשון, אבל התוצאה עדיין מילים, לא מספרים.", do=show("q-x-1")),
    L("[[RandomForest|רַנְדוֹם פוֹרֶסְט]] הוא **מודל**. הוא לא ממיר טקסט, אלא צריך לקבל מספרים מוכנים.", do=show("q-x-2")),
    L("ו-[[StopWords|סְטוֹפּ ווֹרְדְס]] היא רשימה של מילים להסרה. היא מקטינה את אוצר המילים, אבל לא מייצרת מספרים.", do=show("q-x-3")),
    P("המלכודת: לבחור את הפירוק למילים. הפירוק הוא חלק מהדרך. המטריצה המספרית היא התוצאה.", hold=0.6),
], stage='<div class="tx-stack">' + w.bow("ex", DOCS, VOC, X, hide_vals=False) + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>{w.esc(Q["question"])}</div>' + st.options("q", OPTS))

recap = Scene("recap", "סיכום", [
    P("לסיכום: אוצר המילים הוא כל המילים השונות, ממוינות.", do=show("r-1")),
    P("המטריצה: שורה לכל מסמך, עמודה לכל מילה, ובתא מספר ההופעות.", do=show("r-2")),
    P("מילות עצירה מסננים, והאוצר קטן.", do=show("r-3")),
    P("והסדר של המילים הולך לאיבוד. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.bow("rb", DOCS, VOC, X, hide_vals=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 אוצר = מילים שונות, ממוינות")
         + st.card("r-2", "rule", "🔑 שורה = מסמך · עמודה = מילה")
         + st.card("r-3", "rule", "🔑 " + rx("stop_words") + " ← פחות עמודות")
         + st.card("r-4", "trap", "⚠️ הסדר לא נשמר"))

VIDEO = w.no_latin(Video("T07", "text", "מטקסט למספרים: Bag of Words", [title, vocab, matrix, new, stop, exam, recap],
                         bank={"25A-A-Q23": 0}))

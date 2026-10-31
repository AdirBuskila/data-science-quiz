# -*- coding: utf-8 -*-
"""T04 · match, search, findall, split ו-sub — video script (build: tools/video/vid.py T04).

Source: courses/text/T04.js (lesson + goal). Exam part: an original "בסגנון מבחן" question (bank={}): no fresh
bank question fits. The bank's function questions are all taken: 26A-B-Q4 (match vs search) and P-65 (split) are
T08 boss items, P-61/P-62 too. Avoided on purpose: the T04 quiz (match/search "b" in "abc", split [,;] ?, sub \\d+ '#'
on "a1b22c333", findall o in "foo boo", search \\d+ in "a12b345") and the lesson's "Hello, hello." split.
Boss items 26A-B-Q4 (match vs search) and P-65 (split edge) are not stated as rules here: the behavior is only shown on
examples, with no slogan card.
Every result shown is the real return value of the re call on the exact string shown.
"""
import re

from vid import P, Scene, Video, show, hide
import stage as st
import w_text as w
from w_text import rx, L

# ---------------------------------------------------------------- one string, five functions
S = "ok 7, no 860."
PAT = r"\d+"
LS, FS = w.hits("s", PAT, S)
R_MATCH = re.match(PAT, S)
R_SEARCH = re.search(PAT, S)
R_FINDALL = re.findall(PAT, S)
R_SPLIT = re.split(PAT, S)
R_SUB = re.sub(PAT, "N", S)
assert R_MATCH is None                                   # s starts with 'o', not a digit
assert R_SEARCH.group() == "7" and R_SEARCH.start() == 3   # the first match only
assert R_FINDALL == ["7", "860"]
assert R_SPLIT == ["ok ", ", no ", "."]                  # the pieces between the matches; the digits are gone
assert R_SUB == "ok N, no N."                            # each whole run of digits -> one N
ROWS = [('re.match(r"\\d+", s)', repr(R_MATCH)),
        ('re.search(r"\\d+", s).group()', repr(R_SEARCH.group())),
        ('re.findall(r"\\d+", s)', repr(R_FINDALL)),
        ('re.split(r"\\d+", s)', repr(R_SPLIT)),
        ('re.sub(r"\\d+", "N", s)', repr(R_SUB))]
CUTS = [(f"t-cut{k}", m.start(), m.end(), "cut") for k, m in enumerate(re.finditer(PAT, S))]
PIECES = []
pos = 0
for k, m in enumerate(list(re.finditer(PAT, S)) + [None]):
    end = m.start() if m else len(S)
    PIECES.append((f"t-pc{k}", pos, end, "g1" if k % 2 == 0 else "g2"))
    pos = m.end() if m else pos
assert [S[a:b] for _, a, b, _ in PIECES] == R_SPLIT

# ---------------------------------------------------------------- the edge trap of split
S2 = ",a,b,"
R2 = re.split(",", S2)
assert R2 == ["", "a", "b", ""]                          # a separator at an edge leaves an empty string there
L2 = [(f"e-cut{k}", m.start(), m.end(), "cut") for k, m in enumerate(re.finditer(",", S2))]

# ---------------------------------------------------------------- when nothing matches
S3 = "no digits"
assert re.match(PAT, S3) is None and re.search(PAT, S3) is None
N_ROWS = [(r're.search(r"\d+", s)', repr(re.search(PAT, S3))),
          (r're.findall(r"\d+", s)', repr(re.findall(PAT, S3))),
          (r're.split(r"\d+", s)', repr(re.split(PAT, S3))),
          (r're.sub(r"\d+", "N", s)', repr(re.sub(PAT, "N", S3)))]
assert [r for _, r in N_ROWS] == ["None", "[]", "['no digits']", "'no digits'"]
try:
    re.search(PAT, S3).group()
    raise AssertionError
except AttributeError:
    pass                                                 # .group() on None: an error, not an empty string

# ---------------------------------------------------------------- exam-style question (original)
T = "a  b   c "
ANS = re.sub(r"\s+", " ", T)
assert ANS == "a b c "                                   # the trailing space is a match too: replaced, not removed
assert len(re.findall(r"\s+", T)) == 3
OPTS_RAW = ["'a b c '", "'a b c'", "'abc'", "['a', 'b', 'c']"]
assert repr(ANS) == OPTS_RAW[0]
assert repr(re.sub(r"\s+", "", T)) == OPTS_RAW[2]        # what deleting (replacing with '') would give
assert re.split(r"\s+", T.strip()) == eval(OPTS_RAW[3])  # a list is what split would give, never sub
LX, FX = w.hits("x", r"\s+", T)
OPTS = [(i, rx(o)) for i, o in enumerate(OPTS_RAW)]
OPTS = [OPTS[i] for i in [1, 3, 0, 2]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את חמש הפונקציות של המודול לביטויים רגולריים."),
    P("נריץ את כולן על אותה מחרוזת ואותה תבנית, ונראה מה כל אחת מחזירה."),
    P("ובסוף נפתור שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">T04 · ביטויים רגולריים וטקסט</div><h1>חמש הפונקציות: match, search, findall, split, sub</h1>'
         '<p>לדעת מה כל פונקציה של re מחזירה, ולחזות את הפלט שלה על טקסט נתון.</p>', layout="title")

find = Scene("find", "שלוש פונקציות שמחפשות", [
    P("המחרוזת שלנו, והתבנית: ספרה אחת או יותר.", do=show("f-code", "s")),
    P("בטקסט יש שני רצפים של ספרות: שבע, ושמונה מאות שישים.", do=w.show_hits("s", 0, 2)),
    L("[[match|מֶאץ']] מנסה להתאים את התבנית במקום הראשון של המחרוזת. כאן המקום הראשון הוא האות [[o|אוֹ]], לא ספרה.", do=show("k-c0")),
    L("ולכן היא מחזירה [[None|נַאן]]: אין התאמה, למרות שיש ספרות בהמשך.", do=show("k-r0")),
    L("[[search|סֶרְץ']] סורקת את הטקסט משמאל לימין, ועוצרת בהתאמה **הראשונה** שהיא מוצאת.", do=show("k-c1")),
    L("היא מחזירה אובייקט התאמה. את הטקסט שנתפס מוציאים עם [[group|גְרוּפּ]]: שבע.", do=show("k-r1")),
    P("שמונה מאות שישים לא מופיע, כי החיפוש כבר נעצר.", do=show("f-c2")),
    L("[[findall|פַיינְד אוֹל]] מחזירה **רשימה** של כל ההתאמות, כמחרוזות.", do=show("k-c2", "k-r2")),
    P("שימו לב להבדל בסוג: אחת מחזירה אובייקט התאמה אחד, והשנייה רשימה.", hold=0.1),
    P("ואם שואלים כמה התאמות יש בטקסט, סופרים את איברי הרשימה. כאן: שתיים.", hold=0.4),
], stage='<div class="tx-stack">' + w.code("f-code", f's = "{S}"', size=40) + w.strip("s", S, LS, hidden=True)
         + w.calls("k", ROWS) + "</div>",
   panel=st.card("f-c2", "rule", "🔑 " + rx("search") + " = ההתאמה הראשונה בלבד")
         + st.card("f-c3", "rule", "🔑 " + rx("findall") + " = רשימה של כולן"))
find.phrases[-1].do += show("f-c3")

change = Scene("change", "שתי פונקציות שמשנות", [
    L("[[split|סְפְּלִיט]] משתמשת בהתאמות כ**מפרידים**: היא חותכת את הטקסט בכל מקום שבו יש התאמה.",
      do=show("t-cut0", "t-cut1", "kk-c3")),
    P("ומחזירה רשימה של החתיכות **שביניהן**. הספרות עצמן נעלמות.", do=show("t-pc0", "t-pc1", "t-pc2", "kk-r3")),
    P("שימו לב לרווח בסוף החתיכה הראשונה, ולנקודה שנשארה לבד בסוף.", do=show("c-c1")),
    L("[[sub|סַאבּ]] מחליפה **כל** התאמה בטקסט חדש, ומחזירה **מחרוזת** חדשה.", do=show("kk-c4")),
    P("כל רצף ספרות, ארוך או קצר, הופך ל-N אחת.", do=show("kk-r4", "c-c2"), say="כל רצף ספרות, ארוך או קצר, הופך לאות אֶן אחת."),
    P("ועוד דוגמה: חותכים בפסיקים את המחרוזת הקטנה הזו.", do=show("e-code", "e")),
    P("שלושה פסיקים, ולכן ארבע חתיכות. לפני הפסיק הראשון אין כלום, וגם אחרי האחרון. תסתכלו על הפלט.",
      do=show("e-cut0", "e-cut1", "e-cut2", "e-out"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("c-code", f's = "{S}"', hidden=False, size=40)
         + w.strip("t", S, CUTS + PIECES)
         + w.calls("kk", ROWS, shown=(0, 1, 2))
         + '<div class="tx-row">' + w.code("e-code", f're.split(",", "{S2}")', size=30)
         + w.strip("e", S2, L2, hidden=True, cw=40) + "</div>" + w.out("e-out", repr(R2)) + "</div>",
   panel=st.card("c-c1", "rule", "🔑 " + rx("split") + " = החתיכות שבין ההתאמות")
         + st.card("c-c2", "rule", "🔑 " + rx("sub") + " = מחרוזת, כל התאמה מוחלפת"))

none = Scene("none", "ומה אם אין התאמה?", [
    P("ומה קורה כשאין אף התאמה? נריץ על מחרוזת בלי ספרות בכלל.", do=show("n-code")),
    L("[[search|סֶרְץ']] מחזירה [[None|נַאן]], בדיוק כמו [[match|מֶאץ']].", do=show("n-c0", "n-r0")),
    L("ואם נקרא ל-[[group|גְרוּפּ]] על [[None|נַאן]], נקבל **שגיאה**. לכן בודקים קודם שיש התאמה.", do=show("n-k1")),
    L("[[findall|פַיינְד אוֹל]] מחזירה רשימה **ריקה**.", do=show("n-c1", "n-r1")),
    L("[[split|סְפְּלִיט]] לא מצאה איפה לחתוך, ולכן מחזירה רשימה עם חתיכה אחת: כל המחרוזת.", do=show("n-c2", "n-r2")),
    L("ו-[[sub|סַאבּ]] לא מצאה מה להחליף, ומחזירה את המחרוזת כמו שהיא.", do=show("n-c3", "n-r3", "n-k2"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("n-code", f's = "{S3}"', size=40) + w.calls("n", N_ROWS) + "</div>",
   panel=st.card("n-k1", "trap", "⚠️ " + rx("None.group()") + " ← שגיאה")
         + st.card("n-k2", "rule", "🔑 אין התאמה: " + rx("[]") + " · רשימה עם הכול · אותה מחרוזת"))

exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("שאלה בסגנון מבחן: מה מחזירה הקריאה הזאת?", do=show("x-code")),
    P("התבנית: תו רווח אחד או יותר. וכל התאמה מוחלפת ברווח יחיד.", hold=0.1),
    P("נמצא את ההתאמות: שני רווחים, שלושה רווחים, ועוד רווח אחד בסוף.", do=show("x", "x-m0", "x-m1", "x-m2")),
    P("כל אחת מהן הופכת לרווח אחד. גם הרווח שבסוף: הוא **לא נמחק**, הוא מוחלף ברווח.", do=show("x-out")),
    P("איך לא לפספס? עוברים על **ההתאמות**, לא על המילים. כל התאמה מוחלפת, גם זו שבקצה.", hold=0.1),
    w.L("ולכן התשובה: [[a|אֵיי]], [[b|בִּי]], [[c|סִי]] עם רווח אחד ביניהן, ועוד רווח אחד בסוף.", do=show("q-ok-0")),
    P("בלי הרווח בסוף? זו המלכודת. התחליף הוא רווח, לא מחרוזת ריקה.", do=show("q-x-1")),
    P("בלי רווחים בכלל, היינו מקבלים רק אם התחליף היה מחרוזת ריקה.", do=show("q-x-2")),
    L("ורשימה? [[sub|סַאבּ]] תמיד מחזירה מחרוזת. רשימה מחזירות [[split|סְפְּלִיט]] ו-[[findall|פַיינְד אוֹל]].",
      do=show("q-x-3"), hold=0.6),
], stage='<div class="tx-stack">' + w.code("x-code", 're.sub(r"\\s+", " ", "a  b   c ")', size=40)
         + w.strip("x", T, LX, hidden=True, cw=54) + w.out("x-out", repr(ANS), size=44) + "</div>",
   panel='<div class="qstem"><span class="qid">בסגנון מבחן</span>מה מחזירה הקריאה '
         + rx('re.sub(r"\\s+", " ", "a  b   c ")', "sm") + "</div>" + st.options("q", OPTS))

recap = Scene("recap", "סיכום", [
    L("לסיכום, על המחרוזת שלנו: [[match|מֶאץ']] החזירה [[None|נַאן]], ו-[[search|סֶרְץ']] החזירה את ההתאמה הראשונה.", do=show("r-1")),
    L("[[findall|פַיינְד אוֹל]] מחזירה רשימה של כל ההתאמות.", do=show("r-2")),
    L("[[split|סְפְּלִיט]] מחזירה את החתיכות שבין ההתאמות.", do=show("r-3")),
    L("ו-[[sub|סַאבּ]] מחזירה מחרוזת שבה כל התאמה הוחלפה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.calls("rk", ROWS, shown=range(5)) + "</div>",
   panel=st.card("r-1", "rule", "🔑 " + rx("search") + " ← ההתאמה הראשונה")
         + st.card("r-2", "rule", "🔑 " + rx("findall") + " ← רשימה")
         + st.card("r-3", "rule", "🔑 " + rx("split") + " ← רשימת חתיכות")
         + st.card("r-4", "rule", "🔑 " + rx("sub") + " ← מחרוזת"))

VIDEO = w.no_latin(Video("T04", "text", "חמש הפונקציות: match, search, findall, split, sub", [title, find, change, none, exam, recap], bank={}))

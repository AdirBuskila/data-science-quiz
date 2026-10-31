# -*- coding: utf-8 -*-
"""T02 · כמתים: כמה פעמים? — video script (build: tools/video/vid.py T02).

Source: courses/text/T02.js (lesson + goal). Exam anchor: 24B-B-Q16 (which strings
r'^\\d+(\\.[0-9]{2})? [^aeiou]([aeiou][^aeiou])+$' can return), used by no guided quiz.
Avoided on purpose: the T02 quiz (ab+ on "ab abb a abbb", \\d{2,3} on "1 22 333 4444" and the lesson's 4444 trap,
colou?r, \\b[A-Z][a-z]*\\b on "Dan met Eli in NYC" = 24A-B-Q4, the \\w+@ e-mails) and every boss item.
Every highlight comes from re.finditer on the string shown; every exam verdict from re.search, and the colored
decomposition of each exam string is cross-checked against that verdict (decompose()).
"""
import re

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx

# ---------------------------------------------------------------- example 1: * + ? on one text
S1 = "gl gol gooool"
LP, FP = w.hits("b1", r"go+l", S1)
LS, FS = w.hits("b2", r"go*l", S1)
LQ, FQ = w.hits("b3", r"go?l", S1)
assert FP == ["gol", "gooool"]               # + : at least one o
assert FS == ["gl", "gol", "gooool"]         # * : zero o's is fine too
assert FQ == ["gl", "gol"]                   # ? : zero or one o; gooool has four
assert re.search(r"go?l", "gooool") is None

# ---------------------------------------------------------------- example 2: the quantifier binds to ONE character
S2 = "hahaha haaa"
LH, FH = w.hits("b4", r"ha+", S2)
assert FH == ["ha", "ha", "ha", "haaa"]      # + repeats the a only; greedy: haaa in one piece
assert re.findall(r"ha+", "hahaha") != ["hahaha"]

# ---------------------------------------------------------------- exam 24B-B-Q16
Q = BANK["24B-B-Q16"]
PAT = r"^\d+(\.[0-9]{2})? [^aeiou]([aeiou][^aeiou])+$"
assert Q["correctIndex"] == 0 and PAT in Q["code"]
PIECES = [("^", "התחלה"), (r"\d+", "ספרות"), (r"(\.[0-9]{2})?", "נקודה ו-2 ספרות, אופציונלי"), (" ", "רווח"),
          ("[^aeiou]", "לא תנועה"), ("([aeiou][^aeiou])+", "זוג: תנועה ואז לא, פעם או יותר"), ("$", "סוף")]
V = set("aeiou")


def decompose(s):
    """the parts of the exam pattern, as layers; asserts that 'everything consumed' == re.search verdict"""
    lay, pfx = [], None
    m = re.match(r"\d+(\.[0-9]{2})?", s)
    i = m.end()
    lay.append((0, i, "m"))
    ok = i < len(s) and s[i] == " "
    i += 1
    if ok and i < len(s) and s[i] not in V:
        lay.append((i, i + 1, "cur"))
        i += 1
        k = 0
        while i + 1 < len(s) and s[i] in V and s[i + 1] not in V:
            lay.append((i, i + 2, "g1" if k % 2 == 0 else "g2"))
            i += 2
            k += 1
        ok = k >= 1 and i == len(s)
    else:
        ok = False
    if i < len(s):
        lay.append((i, len(s), "no"))
    assert ok == (re.search(PAT, s) is not None), s
    return lay, ok


ROWS = ["20 kilos", "20.35 dolars", "1 dolar", "1.35 kilos", "3 meters", "5 shekels"]
LAY, OKS = {}, []
for r_, s in enumerate(ROWS):
    lay, ok = decompose(s)
    LAY[r_] = [(f"t-s{r_}-l{j}", a, b, k) for j, (a, b, k) in enumerate(lay)]
    OKS.append(ok)
TESTS, RES = w.tests("t", PAT, ROWS, layers=LAY)
assert RES == OKS == [True, False, True, True, False, False]
# the four options: "can return X, but cannot return Y" is true iff X matches and Y does not
CLAIMS = [("20 kilos", "20.35 dolars"), ("1 dolar", "1.35 kilos"), ("3 meters", "3.53 shekels"),
          ("5 shekels", "5.12 banana")]
TRUTH = [bool(re.search(PAT, a)) and not re.search(PAT, b) for a, b in CLAIMS]
assert TRUTH == [True, False, False, False]
for (a, b), o in zip(CLAIMS, Q["options"]):
    assert a in o and b in o


def lays(r_):
    return [l[0] for l in LAY[r_]]


OPTS = [(i, w.esc(o)) for i, o in enumerate(Q["options"])]
OPTS = [OPTS[i] for i in [1, 3, 0, 2]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד את הכמתים: הסימנים שאומרים כמה פעמים משהו חוזר."),
    P("כוכבית, פלוס, סימן שאלה וסוגריים מסולסלים."),
    P("ובסוף נפתור שאלה ממבחן שבודקת את כולם יחד.", hold=0.4),
], stage='<div class="kicker">T02 · ביטויים רגולריים וטקסט</div><h1>כמתים: כמה פעמים?</h1>'
         '<p>להשתמש ב-' + rx("* + ? {n,m}") + ' כדי לתפוס חזרות, ולחזות מה findall יחזיר.</p>', layout="title")

QPIECES = [("*", "0 פעמים או יותר"), ("+", "פעם אחת או יותר"), ("?", "0 או פעם אחת"),
           ("{3}", "בדיוק 3"), ("{2,4}", "בין 2 ל-4")]
idea = Scene("idea", "הכמתים", [
    P("ברמה הקודמת כל סימן תפס תו אחד. כמת בא **אחרי** סימן, ואומר כמה פעמים הוא חוזר.", do=show("q-p0")),
    P("כוכבית: אפס פעמים או יותר. כלומר, מותר גם שלא יופיע בכלל."),
    P("פלוס: פעם אחת או יותר. חייב להופיע לפחות פעם אחת.", do=show("q-p1")),
    P("סימן שאלה: אפס או פעם אחת. כלומר, **אופציונלי**.", do=show("q-p2")),
    P("וסוגריים מסולסלים נותנים מספר מדויק, או טווח של מינימום ומקסימום.", do=show("q-p3", "q-p4")),
    P("שני כללים. הראשון: הכמת חל רק על **התו האחד** שלפניו.", do=show("q-c1")),
    P("השני: הכמתים **חמדנים**. הם תופסים כמה שיותר חזרות.", do=show("q-c2"), hold=0.4),
], stage='<div class="tx-stack">' + w.parts("q", QPIECES) + "</div>",
   panel=st.card("q-c1", "rule", "🔑 הכמת חל על <b>התו האחד</b> שלפניו")
         + st.card("q-c2", "rule", "🔑 חמדן: כמה שיותר חזרות"))

three = Scene("three", "שלושה כמתים, טקסט אחד", [
    P("נשווה את שלושת הכמתים על אותו טקסט: gl, gol ו-gooool.", do=show("b-txt"),
      say="נשווה את שלושת הכמתים על אותו טקסט: שלוש מילים, עם אפס, אחת וארבע אותיות אוֹ באמצע."),
    w.L("קודם עם פלוס: [[g|גִ'י]], [[o|אוֹ]] אחת או יותר, ו-[[l|אֶל]].", do=show("b-c1", "b1")),
    w.L("המילה הראשונה בלי [[o|אוֹ]] בכלל, אז לא נתפסת. השתיים האחרות נתפסות, כולל כל ארבע ה-[[o|אוֹ]].",
      do=w.show_hits("b1", 0, 2) + show("b-o1")),
    P("עכשיו כוכבית: גם אפס פעמים מותר.", do=hide("b-c1", "b1", "b-o1") + show("b-c2", "b2")),
    w.L("ולכן נתפסות שלוש המילים, גם זו בלי [[o|אוֹ]].", do=w.show_hits("b2", 0, 3) + show("b-o2")),
    P("ועכשיו סימן שאלה: אפס או פעם אחת.", do=hide("b-c2", "b2", "b-o2") + show("b-c3", "b3")),
    w.L("שתי המילים הראשונות נתפסות. במילה הארוכה יש ארבע [[o|אוֹ]], יותר מאחת, ואין התאמה.",
      do=w.show_hits("b3", 0, 2) + show("b-o3")),
    P("אותו טקסט, שלוש תוצאות שונות. הכמת קובע.", hold=0.4),
], stage='<div class="tx-stack">' + w.big("b-txt", S1, hidden=True, size=46)
         + '<div class="swap" style="--swap-h:330px">'
         + "<div>" + w.code("b-c1", f're.findall(r"go+l", "{S1}")') + w.strip("b1", S1, LP, hidden=True)
         + w.out("b-o1", repr(FP)) + "</div>"
         + "<div>" + w.code("b-c2", f're.findall(r"go*l", "{S1}")') + w.strip("b2", S1, LS, hidden=True)
         + w.out("b-o2", repr(FS)) + "</div>"
         + "<div>" + w.code("b-c3", f're.findall(r"go?l", "{S1}")') + w.strip("b3", S1, LQ, hidden=True)
         + w.out("b-o3", repr(FQ)) + "</div>"
         + "</div></div>",
   panel=st.card("b-k1", "ex", rx("+") + " : לפחות פעם אחת") + st.card("b-k2", "ex", rx("*") + " : גם אפס פעמים")
         + st.card("b-k3", "ex", rx("?") + " : אפס או פעם אחת"))
# the panel cards follow the three steps
three.phrases[1].do += show("b-k1")
three.phrases[3].do += show("b-k2")
three.phrases[5].do += show("b-k3")

one = Scene("one", "על מה הכמת חל?", [
    w.L("ועכשיו הכלל הראשון בפעולה: [[h|הֵייץ']], [[a|אֵיי]], ופלוס.", do=show("h-code", "b4")),
    w.L("הפלוס יושב אחרי ה-[[a|אֵיי]], ולכן חל **רק עליה**. הוא לא חוזר על הצירוף כולו.", do=show("h-c1")),
    P("לכן המילה הראשונה לא נתפסת כיחידה אחת. היא נתפסת בשלושה חלקים, כל אחד של שני תווים.",
      do=w.show_hits("b4", 0, 3)),
    w.L("ובמילה השנייה, הפלוס החמדן תופס את כל שלוש ה-[[a|אֵיי]] ברצף.", do=w.show_hits("b4", 3, 4) + show("h-out")),
    P("רוצים לחזור על כמה תווים יחד? צריך סוגריים עגולים סביבם. נגיע לזה ברמה הבאה.", do=show("h-c2"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("h-code", f're.findall(r"ha+", "{S2}")') + w.strip("b4", S2, LH, hidden=True)
         + w.out("h-out", repr(FH)) + "</div>",
   panel=st.card("h-c1", "rule", "🔑 " + rx("ha+") + " = h ואז a אחת או יותר")
         + st.card("h-c2", "trap", "⚠️ " + rx("ha+") + " לא תופס את hahaha כיחידה אחת"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אילו מחרוזות יכול להחזיר הביטוי הזה? נפרק אותו לחלקים.", do=show("x-p0", "x-p6")),
    P("כובע בהתחלה ודולר בסוף: כל המחרוזת, מההתחלה ועד הסוף, חייבת להתאים."),
    P("ספרה ופלוס: מספר שלם, ספרה אחת או יותר.", do=show("x-p1")),
    P("אחריו בסוגריים: נקודה אמיתית ובדיוק שתי ספרות. סימן השאלה הופך את כל הקבוצה לאופציונלית.", do=show("x-p2")),
    P("רווח, ואז תו אחד שאינו תנועה. כובע **בתוך** סוגריים מרובעים פירושו: כל תו חוץ מאלה.",
      do=show("x-p3", "x-p4")),
    P("ובסוף: זוג של תנועה ואחריה תו שאינו תנועה. והפלוס על הסוגריים: זוג אחד או יותר.", do=show("x-p5"), hold=0.3),
    P("נבדוק את 20 kilos: עשרים, רווח, האות k, ואז שני זוגות שלמים. מתאים.",
      say="נבדוק את עשרים קילוס: עשרים, רווח, האות קֵיי, ואז שני זוגות שלמים. מתאים.",
      do=show("t-r0", *lays(0), "t-v0")),
    P("ב-20.35 dolars, אחרי שני זוגות נשארת s לבד. אין לה זוג, ולכן לא מתאים.",
      say="בעשרים נקודה שלושים וחמש דולרס, אחרי שני זוגות נשארת אֶס לבד. אין לה זוג, ולכן לא מתאים.",
      do=show("t-r1", *lays(1), "t-v1")),
    P("אז הטענה ״20 kilos כן, 20.35 dolars לא״ נכונה.", do=show("q-ok-0"),
      say="אז הטענה, עשרים קילוס כן, עשרים נקודה שלושים וחמש דולרס לא, נכונה."),
    P("1 dolar מתאים. אבל 1.35 kilos **גם** מתאים, כי נקודה ושתי ספרות מותרות.",
      say="אחד דולר מתאים. אבל אחד נקודה שלושים וחמש קילוס גם מתאים, כי נקודה ושתי ספרות מותרות.",
      do=show("t-r2", *lays(2), "t-v2", "t-r3", *lays(3), "t-v3")),
    P("ולכן החצי השני, ״לא יכול להחזיר״, שגוי.", do=show("q-x-1", "q-n-1")),
    P("ב-3 meters, אחרי שני זוגות נשארת s. ולכן כבר החצי הראשון שגוי.",
      say="בשלוש מיטרס, אחרי שני זוגות נשארת אֶס. ולכן כבר החצי הראשון שגוי.",
      do=show("t-r4", *lays(4), "t-v4", "q-x-2", "q-n-2")),
    P("וב-5 shekels, אחרי ה-s באה ה-h, שאינה תנועה. אין אפילו זוג אחד.",
      say="ובחמש שקלס, אחרי האֶס באה האֵייץ', שאינה תנועה. אין אפילו זוג אחד.",
      do=show("t-r5", *lays(5), "t-v5", "q-x-3", "q-n-3")),
    P("המלכודת: לבדוק רק את ההתחלה. עם הכובע והדולר, תו אחד עודף בסוף פוסל את כל המחרוזת.", hold=0.6),
], stage='<div class="tx-stack">' + w.parts("x", PIECES, PAT, small=True) + TESTS + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>אילו מחרוזות יכול להחזיר הביטוי הרגולרי הבא?<br>'
         + rx("r'" + PAT + "'", "sm") + "</div>"
         + st.options("q", OPTS, notes={1: w.nw("1.35 kilos ✓"), 2: w.nw("meters ✗"), 3: w.nw("shekels ✗")}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כוכבית זה אפס או יותר, פלוס זה אחת או יותר, וסימן שאלה זה אפס או אחת.", do=show("r-1")),
    P("סוגריים מסולסלים: מספר מדויק, או טווח.", do=show("r-2")),
    P("הכמת חל רק על התו האחד שלפניו, או על קבוצה שלמה בסוגריים עגולים.", do=show("r-3")),
    P("והכמתים חמדנים: תופסים כמה שיותר. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.parts("rp", QPIECES, hidden=False) + "</div>",
   panel=st.card("r-1", "rule", "🔑 " + rx("*") + " 0+ · " + rx("+") + " 1+ · " + rx("?") + " 0/1")
         + st.card("r-2", "rule", "🔑 " + rx("{n}") + " בדיוק · " + rx("{n,m}") + " טווח")
         + st.card("r-3", "trap", "⚠️ " + rx("ha+") + " ≠ " + rx("(ha)+"))
         + st.card("r-4", "rule", "🔑 חמדן: כמה שיותר"))

VIDEO = w.no_latin(Video("T02", "text", "כמתים: כמה פעמים?", [title, idea, three, one, exam, recap],
                         bank={"24B-B-Q16": 0}))

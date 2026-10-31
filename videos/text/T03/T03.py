# -*- coding: utf-8 -*-
"""T03 · עוגנים, או וקבוצות — video script (build: tools/video/vid.py T03).

Source: courses/text/T03.js (lesson + goal). Exam anchor: 26B-A-Q4 (which strings
r'^[A-Z][a-z]{1,} [A-Z]\\. [A-Z][a-z]+$' returns: a name with a middle initial), used by no guided quiz.
Its twin 24B-A-Q16 (same name pattern with [a-z]+) is not used anywhere else in this course's videos.
Avoided on purpose: the T03 quiz (cat$/^cat/match on "concat", cat|dog on "cat dogs bird", (\\d+)-(\\d+) on
"10-20 and 3-4", (\\w+)@(\\w+) group(2), the e-mail pattern of 24A-A-Q4 with dan.k@mail.co.il) and every boss item.
Every highlight / verdict below is a real re run on the string shown.
"""
import re

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx, L

# ---------------------------------------------------------------- anchors
ROWS1 = ["2024", "2024a", "ab2024"]
FREE = {i: [(f"a-s{i}-f", m.start(), m.end(), "cur")] for i, s in enumerate(ROWS1) for m in [re.search(r"\d+", s)]}
assert all(re.search(r"\d+", s) for s in ROWS1)                       # without anchors: digits found in all three
T1, R1 = w.tests("a", r"^\d+$", ROWS1, layers=FREE)
assert R1 == [True, False, False]
assert re.match(r"\d+", "2024a") and not re.match(r"\d+", "ab2024")    # match = an implicit ^ only, no $

# ---------------------------------------------------------------- alternation + groups
S2 = "gray grey groy"
L2, F2 = w.hits("g1", r"gr(a|e)y", S2)
assert F2 == ["gray", "grey"]                                          # group(0) of each match
assert re.findall(r"gr(a|e)y", S2) == ["a", "e"]                        # findall with a group: the group only
L3, F3 = w.hits("g2", r"gra|ey", S2)
assert F3 == ["gra", "ey"]                                             # | without parentheses splits everything
GL = [(f"g1-k{k}", m.start(1), m.end(1), "g1") for k, m in enumerate(re.finditer(r"gr(a|e)y", S2))]

# ---------------------------------------------------------------- escaped dot
S4 = "v1.5 v105"
L4a, F4a = w.hits("d1", r"v1.5", S4)
L4b, F4b = w.hits("d2", r"v1\.5", S4)
assert F4a == ["v1.5", "v105"] and F4b == ["v1.5"]

# ---------------------------------------------------------------- exam 26B-A-Q4
Q = BANK["26B-A-Q4"]
PAT = r"^[A-Z][a-z]{1,} [A-Z]\. [A-Z][a-z]+$"
assert Q["correctIndex"] == 0 and PAT in Q["code"]
PIECES = [("^", "התחלה"), ("[A-Z]", "גדולה"), ("[a-z]{1,}", "קטנות"), (" ", "רווח"), ("[A-Z]", "גדולה"),
          (r"\.", "נקודה"), (" ", "רווח"), ("[A-Z]", "גדולה"), ("[a-z]+", "קטנות"), ("$", "סוף")]
ROWS2 = ["Grace M. Hopper", "Grace Hopper", "Grace M Hopper", "grace M. Hopper"]
T2, R2 = w.tests("t", PAT, ROWS2)
assert R2 == [True, False, False, False]
assert re.fullmatch(r"[a-z]{1,}", "x") and re.fullmatch(r"[a-z]{1,}", "race")   # {1,} = one or more, like +
# the only dot the pattern accepts is the one \. ; no class in it contains a dot or '@' -> no 3-dot password,
# no '@user' handle, no sentence with its punctuation
assert PAT.count(r"\.") == 1 and "." not in PAT.replace(r"\.", "")
assert not re.search(PAT, "@grace_h") and not re.search(PAT, "Hi. I am Grace. Bye.")
OPTS = [(i, w.esc(o)) for i, o in enumerate(Q["options"])]
OPTS = [OPTS[i] for i in [2, 0, 3, 1]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד שלושה כלים: עוגנים, הסימן ״או״, וסוגריים עגולים."),
    P("ובסוף נקרא תבנית ממבחן מההתחלה ועד הסוף.", hold=0.4),
], stage='<div class="kicker">T03 · ביטויים רגולריים וטקסט</div><h1>עוגנים, או וקבוצות</h1>'
         '<p>לדעת מה ' + rx("^") + ' ו-' + rx("$") + ' מחייבים, להשתמש ב-' + rx("|")
         + ' ובסוגריים, ולקרוא תבנית שלמה.</p>', layout="title")

anchors = Scene("anchors", "עוגנים", [
    P("נתחיל בעוגנים. הם לא תופסים תו, אלא **מקום**, כמו גבול מילה.", do=show("an-c1")),
    P("הכובע: תחילת המחרוזת. הדולר: סוף המחרוזת.", do=show("an-c2")),
    P("נחפש רצף ספרות בשלוש מחרוזות, קודם בלי עוגנים.", do=show("a-r0", "a-r1", "a-r2", "an-code1")),
    P("החיפוש מוצא ספרות בכל השלוש: גם כשיש אחריהן אות, וגם כשיש לפניהן.",
      do=show("a-s0-f", "a-s1-f", "a-s2-f")),
    P("עכשיו נוסיף כובע בהתחלה ודולר בסוף.", do=hide("an-code1") + show("an-code2")),
    P("עכשיו הספרות צריכות להתחיל בתחילת המחרוזת **ולהיגמר** בסופה.", hold=0.2),
    P("רק ״2024״ עובר. בשתיים האחרות יש אות שלא נכנסת לרצף.", do=show("a-v0", "a-v1", "a-v2"),
      say="רק אלפיים עשרים וארבע עובר. בשתיים האחרות יש אות שלא נכנסת לרצף."),
    P("ככה בודקים ש**כל** המחרוזת תקינה, ולא רק חלק ממנה.", do=show("an-c3"), hold=0.4),
], stage='<div class="tx-stack"><div class="swap" style="--swap-h:80px">'
         + "<div>" + w.code("an-code1", r're.search(r"\d+", s)') + "</div>"
         + "<div>" + w.code("an-code2", r're.search(r"^\d+$", s)') + "</div></div>" + T1 + "</div>",
   panel=st.card("an-c1", "plain", "עוגן = מקום, לא תו")
         + st.card("an-c2", "rule", "🔑 " + rx("^") + " תחילת המחרוזת · " + rx("$") + " סופה")
         + st.card("an-c3", "rule", "🔑 " + rx("^...$") + " = כל המחרוזת"))

groups = Scene("groups", "או וקבוצות", [
    P("הקו האנכי הוא **או**: התבנית מצד שמאל שלו, או התבנית מצד ימין.", do=show("gr-c1")),
    L("ובלי סוגריים, הוא מפריד את **כל** התבנית: [[gra|גִ'י אָר אֵיי]] או [[ey|אִי וַואי]].", do=show("gr-code2", "g2")),
    P("ולכן נתפסים שני חלקים חסרי משמעות.", do=w.show_hits("g2", 0, 2) + show("gr-o2")),
    P("כדי שה״או״ יחול רק על אות אחת, עוטפים אותה בסוגריים עגולים.",
      do=hide("gr-code2", "g2", "gr-o2") + show("gr-code1", "g1")),
    L("עכשיו: [[gr|גִ'י אָר]], אחר כך [[a|אֵיי]] או [[e|אִי]], ואז [[y|וַואי]]. נתפסות שתי המילים הראשונות.", do=w.show_hits("g1", 0, 2)),
    P("והשלישית לא, כי אוֹ אינה אחת משתי האפשרויות.", do=show("g1-no")),
    P("אבל הסוגריים עושים עוד משהו: הם יוצרים **קבוצה**, שאפשר לשלוף לבד.", do=show("g1-k0", "g1-k1")),
    L("והמלכודת: כשיש קבוצה, [[findall|פַיינְד אוֹל]] מחזירה **רק את תוכן הקבוצה**, לא את כל ההתאמה.", do=show("gr-o1", "gr-c2")),
    P("כל ההתאמה היא קבוצה מספר אפס. הקבוצה הראשונה בסוגריים היא קבוצה מספר אחת.", do=show("gr-c3"), hold=0.4),
], stage='<div class="tx-stack"><div class="swap" style="--swap-h:330px">'
         + "<div>" + w.code("gr-code1", f're.findall(r"gr(a|e)y", "{S2}")')
         + w.strip("g1", S2, L2 + GL + [("g1-no", 10, 14, "no")], hidden=True) + w.out("gr-o1", repr(re.findall(r"gr(a|e)y", S2))) + "</div>"
         + "<div>" + w.code("gr-code2", f're.findall(r"gra|ey", "{S2}")') + w.strip("g2", S2, L3, hidden=True)
         + w.out("gr-o2", repr(F3)) + "</div></div></div>",
   panel=st.card("gr-c1", "rule", "🔑 " + rx("a|b") + " = a או b")
         + st.card("gr-c2", "trap", "⚠️ " + rx("findall") + " עם קבוצה מחזירה את הקבוצה: " + rx("['a', 'e']"))
         + st.card("gr-c3", "ex", rx("m.group(0)") + " = " + rx("'gray'") + "<br>" + rx("m.group(1)") + " = " + rx("'a'")))

dot = Scene("dot", "נקודה אמיתית", [
    P("ועוד דבר שנצטרך במבחן: נקודה בתבנית היא **כל תו**. כדי לתפוס נקודה אמיתית, שמים לפניה לוכסן הפוך.", do=show("dt-c1")),
    L("נחפש גרסה [[v1.5|וִי אחת נקודה חמש]]. עם נקודה רגילה, נתפסת גם [[v105|וִי מאה וחמש]], כי הנקודה תפסה את האפס.",
      do=show("dt-code1", "d1") + w.show_hits("d1", 0, 2)),
    P("עם לוכסן הפוך, רק הגרסה הנכונה.", do=show("dt-code2", "d2") + w.show_hits("d2", 0, 1), hold=0.4),
], stage='<div class="tx-stack">' + w.code("dt-code1", f're.findall(r"v1.5", "{S4}")') + w.strip("d1", S4, L4a, hidden=True)
         + w.code("dt-code2", f're.findall(r"v1\\.5", "{S4}")') + w.strip("d2", S4, L4b, hidden=True) + "</div>",
   panel=st.card("dt-c1", "rule", "🔑 " + rx(".") + " = כל תו · " + rx(r"\.") + " = נקודה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אילו מחרוזות יחזיר הביטוי הזה? נקרא אותו חלק אחרי חלק.", do=show("x-p0", "x-p9")),
    P("כובע ודולר: כל המחרוזת.", hold=0.1),
    P("מילה ראשונה: אות גדולה, ואחריה אות קטנה אחת או יותר. סוגריים מסולסלים עם אחת ופסיק, זה בדיוק כמו פלוס.",
      do=show("x-p1", "x-p2")),
    P("רווח, אות גדולה **אחת**, ונקודה אמיתית.", do=show("x-p3", "x-p4", "x-p5")),
    P("ועוד רווח, ומילה שנייה: אות גדולה וקטנות.", do=show("x-p6", "x-p7", "x-p8"), hold=0.3),
    P("שם פרטי, אות של שם אמצעי עם נקודה, ושם משפחה. נבדוק.", do=show("t-r0", "t-v0")),
    P("בלי השם האמצעי, אין התאמה: אחרי השם הפרטי חייבת לבוא אות גדולה ונקודה.", do=show("t-r1", "t-v1")),
    P("בלי הנקודה, אין התאמה. ועם אות קטנה בהתחלה, גם לא.", do=show("t-r2", "t-v2", "t-r3", "t-v3")),
    P("אז התשובה: שמות עם אות אמצעית ונקודה אחריה.", do=show("q-ok-0")),
    P("סיסמה עם שלוש נקודות? בתבנית יש מקום לנקודה **אחת** בלבד.", do=show("q-x-1")),
    P("כמה משפטים? אין בתבנית מקום לסימני פיסוק של סוף משפט, ובדיוק שני רווחים.", do=show("q-x-2")),
    P("ושם משתמש ברשת חברתית לא מכיל רווחים. כאן חייבים שניים.", do=show("q-x-3")),
    P("המלכודת: לא לזהות את הנקודה. עם לוכסן לפניה, זו נקודה אמיתית ולא כל תו.", hold=0.6),
], stage='<div class="tx-stack">' + w.parts("x", PIECES, PAT, small=True) + T2 + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>אילו מחרוזות יחזיר הביטוי הרגולרי הבא?<br>'
         + rx("r'" + PAT + "'", "sm") + "</div>" + st.options("q", OPTS))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כובע ודולר הם עוגנים. יחד הם מחייבים התאמה של **כל** המחרוזת.", do=show("r-1")),
    P("הקו האנכי הוא או. בלי סוגריים הוא מפריד את כל התבנית.", do=show("r-2")),
    P("סוגריים עגולים יוצרים קבוצה, ו-findall מחזירה רק את הקבוצות.", do=show("r-3"),
      say="סוגריים עגולים יוצרים קבוצה, ופַיינְד אוֹל מחזירה רק את הקבוצות."),
    P("ונקודה אמיתית כותבים עם לוכסן הפוך לפניה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.big("r-big", PAT, size=34) + "</div>",
   panel=st.card("r-1", "rule", "🔑 " + rx("^...$") + " = כל המחרוזת")
         + st.card("r-2", "trap", "⚠️ " + rx("gra|ey") + " ≠ " + rx("gr(a|e)y"))
         + st.card("r-3", "trap", "⚠️ " + rx("findall") + " + קבוצה ← תוכן הקבוצה")
         + st.card("r-4", "rule", "🔑 " + rx(r"\.") + " = נקודה אמיתית"))

VIDEO = w.no_latin(Video("T03", "text", "עוגנים, או וקבוצות", [title, anchors, groups, dot, exam, recap],
                         bank={"26B-A-Q4": 0}))

# -*- coding: utf-8 -*-
"""T05 · חמדן מול עצלן, וקבוצות — video script (build: tools/video/vid.py T05).

Source: courses/text/T05.js (lesson + goal). Exam anchor: P-66 (re.search(r'(.*)(.*?)', "A new day"): group(2) and
group(0)), used by no guided quiz.
Avoided on purpose: the T05 quiz (<.+> / <.+?> on "<a><b>", a.*?b on "xaabbby", (\\w+) (\\w+) on "A new day" with
group(2) = 'new', a.*?a on "a1a2a") and 26A-B-Q9 (kept for the T08 walkthrough). The groups example uses its own
text, and findall-with-two-groups (a T03 quiz item) is not shown.
Every span and group below is the real result of re.search / re.finditer on the string shown.
"""
import re

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx, L

# ---------------------------------------------------------------- greedy vs lazy
S1 = 'say "hi" and "bye"'
LG, FG = w.hits("gr", r'".+"', S1)
LZ, FZ = w.hits("lz", r'".+?"', S1)
assert FG == ['"hi" and "bye"']                           # greedy: up to the LAST quote
assert FZ == ['"hi"', '"bye"']                            # lazy: up to the first quote that works, twice
assert re.search(r'".+?"', S1).group() == '"hi"'
# greedy, step by step: .+ first runs to the end of the text, then gives back characters until a quote can follow
GREEDY_RUN = [("gr-run", 5, len(S1), "cur")]
assert re.fullmatch(r".+", S1[5:])                        # the dot alone could take everything after the first quote

# ---------------------------------------------------------------- ? after a character = optional
assert re.findall(r"https?", "http https") == ["http", "https"]

# ---------------------------------------------------------------- groups
S2 = "x=10, y=7"
M2 = re.search(r"(\w+)=(\d+)", S2)
assert (M2.group(0), M2.group(1), M2.group(2)) == ("x=10", "x", "10")
GL = [("g0", *M2.span(0), "m"), ("g1", *M2.span(1), "g1", "1"), ("g2", *M2.span(2), "g2", "2")]

# ---------------------------------------------------------------- exam P-66
Q = BANK["P-66"]
assert Q["correctIndex"] == 0 and "(.*)(.*?)" in Q["question"] and "A new day" in Q["question"]
S3 = "A new day"
M3 = re.search(r"(.*)(.*?)", S3)
assert M3.group(1) == S3 and M3.group(2) == "" and M3.group(0) == S3     # group(2) empty, group(0) everything
assert M3.span(2) == (len(S3), len(S3))                                    # the empty group sits at the very end
XL = [("e1", *M3.span(1), "g1", "קבוצה 1"), ("e2", *M3.span(2), "nil", "קבוצה 2: ריקה")]
OPTS = [(i, rx(o, "wr")) for i, o in enumerate(Q["options"])]
OPTS = [OPTS[i] for i in [2, 1, 0, 3]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נראה מה קורה כשסימן שאלה בא אחרי כוכבית או פלוס."),
    P("נשווה תבנית חמדנית לתבנית עצלנית, ונלמד לשלוף קבוצות מתוך התאמה."),
    P("ובסוף נפתור שאלה ממבחן שמשלבת את שני הדברים.", hold=0.4),
], stage='<div class="kicker">T05 · ביטויים רגולריים וטקסט</div><h1>חמדן מול עצלן, וקבוצות</h1>'
         '<p>להבין מה ' + rx("?") + ' משנה אחרי ' + rx("*") + ' או ' + rx("+")
         + ', ולהוציא קבוצות מתוך התאמה.</p>', layout="title")

greedy = Scene("greedy", "חמדן", [
    P("רוצים לשלוף מילה בתוך מירכאות. תבנית ראשונה: מירכאה, נקודה ופלוס, ומירכאה.", do=show("g-code", "gr")),
    P("ההתאמה מתחילה במירכאה הראשונה.", hold=0.1),
    P("עכשיו נקודה ופלוס. הם **חמדנים**: רצים כמה שיותר, עד סוף הטקסט.", do=show("gr-run")),
    P("אבל בסוף התבנית חייבת לבוא מירכאה. אז הם מחזירים תווים אחד אחד, עד שאחריהם יש מירכאה.", hold=0.1),
    P("והמירכאה הראשונה שהם פוגשים מהסוף היא **האחרונה** בטקסט.", do=hide("gr-run") + w.show_hits("gr", 0, 1)),
    P("ולכן נתפס הכול: שתי המילים, וכל מה שביניהן. לא מה שרצינו.", do=show("g-out", "g-c1"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("g-code", f"re.findall(r'\".+\"', '{S1}')")
         + w.strip("gr", S1, LG + GREEDY_RUN, hidden=True) + w.out("g-out", repr(FG)) + "</div>",
   panel=st.card("g-c1", "trap", "⚠️ חמדן: עד המירכאה <b>האחרונה</b>"))

lazy = Scene("lazy", "עצלן", [
    P("עכשיו נוסיף סימן שאלה אחרי הפלוס. זה הופך אותו ל**עצלן**.", do=show("z-code", "lz")),
    P("עצלן תופס כמה **שפחות**: אחרי כל תו הוא בודק אם אפשר כבר לסיים.", do=show("z-c1")),
    L("אחרי [[hi|הַיי]] יש מירכאה, אז ההתאמה נגמרת שם.", do=w.show_hits("lz", 0, 1)),
    L("והחיפוש ממשיך, ומוצא גם את [[bye|בַּיי]].", do=w.show_hits("lz", 1, 2) + show("z-out")),
    P("שתי מילים נפרדות, בדיוק מה שרצינו.", hold=0.3),
    L("שימו לב: סימן שאלה אחרי **תו רגיל** פירושו אופציונלי. למשל [[https?|אֵייץ' טִי טִי פִּי, ואֶס אופציונלית]].",
      do=show("z-c2")),
    P("רק אחרי כמת, כמו כוכבית או פלוס, הוא הופך אותו לעצלן.", hold=0.4),
], stage='<div class="tx-stack">' + w.code("z-code", f"re.findall(r'\".+?\"', '{S1}')")
         + w.strip("lz", S1, LZ, hidden=True) + w.out("z-out", repr(FZ)) + "</div>",
   panel=st.card("z-c1", "rule", "🔑 " + rx(".+?") + " עצלן: עד ההתאמה הראשונה האפשרית")
         + st.card("z-c2", "trap", "⚠️ " + rx("s?") + " = s אופציונלית · " + rx("+?") + " = פלוס עצלן"))

groups = Scene("groups", "קבוצות", [
    P("ועכשיו קבוצות. סוגריים עגולים בתבנית מסמנים חלק שנרצה לשלוף לבד.", do=show("k-code", "gp")),
    P("כאן: תווי מילה בסוגריים, סימן שווה, וספרות בסוגריים.", hold=0.1),
    P("קבוצה מספר אפס היא **כל ההתאמה**: אִקְס שווה עשר.", do=show("g0", "gk-c0", "gk-r0")),
    P("קבוצה מספר אחת היא הסוגריים הראשונים: אִקְס.", do=show("g1", "gk-c1", "gk-r1")),
    P("וקבוצה מספר שתיים היא הסוגריים השניים: עשר.", do=show("g2", "gk-c2", "gk-r2")),
    P("סופרים את הקבוצות לפי סדר הסוגריים הפותחים, משמאל לימין.", do=show("k-c1")),
    L("והחיפוש עצר בהתאמה הראשונה, ולכן [[y=7|וַואי שווה שבע]] לא מופיע כאן בכלל.", hold=0.4),
], stage='<div class="tx-stack">' + w.code("k-code", f'm = re.search(r"(\\w+)=(\\d+)", "{S2}")', size=32)
         + w.strip("gp", S2, GL, hidden=True, cw=54)
         + w.calls("gk", [("m.group(0)", repr(M2.group(0))), ("m.group(1)", repr(M2.group(1))),
                          ("m.group(2)", repr(M2.group(2)))]) + "</div>",
   panel=st.card("k-c1", "rule", "🔑 " + rx("group(0)") + " = הכול<br>" + rx("group(1)") + " = הסוגריים הראשונים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה ידפיס הקוד? שתי קבוצות, ונקודה וכוכבית בכל אחת.", do=show("x-code")),
    P("בראשונה הכוכבית **חמדנית**. היא תופסת את כל המחרוזת, עד הסוף.", do=show("x", "e1")),
    P("בשנייה הכוכבית **עצלנית**. היא מוכנה לתפוס גם אפס תווים, ולכן לוקחת אפס.", do=show("e2")),
    P("וזה גם מסתדר: לא נשאר שום תו בשבילה, וההתאמה מצליחה.", hold=0.1),
    P("לכן קבוצה שתיים היא מחרוזת **ריקה**, וההדפסה שלה היא שורה ריקה.", do=show("xr-c0", "xr-r0")),
    P("וקבוצה אפס היא כל ההתאמה: כל המשפט.", do=show("xr-c1", "xr-r1", "q-ok-0")),
    P("שתי שורות ריקות? לא. קבוצה אפס היא ההתאמה כולה, והיא לא ריקה.", do=show("q-x-1")),
    P("רשימה או שלישייה? לא. כל קבוצה היא מחרוזת אחת, לא רשימת מילים.", do=show("q-x-2")),
    P("ושגיאה? לא. קבוצה ריקה היא חוקית לגמרי, והתבנית תקינה.", do=show("q-x-3"), hold=0.3),
    P("המלכודת: לחשוב שהעצלנית תתפוס משהו. עצלן עם כוכבית מסתפק באפס, אם זה מספיק.", hold=0.6),
], stage='<div class="tx-stack">' + w.code("x-code", f'm = re.search(r"(.*)(.*?)", "{S3}")', size=32)
         + w.strip("x", S3, XL, hidden=True, cw=54)
         + w.calls("xr", [("m.group(2)", repr(M3.group(2))), ("m.group(0)", repr(M3.group(0)))]) + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>מה הפלט של שתי השורות?<br>'
         + rx("print(m.group(2))") + "<br>" + rx("print(m.group(0))") + "</div>"
         + st.options("q", OPTS))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כוכבית ופלוס חמדנים. הם תופסים עד ההתאמה האחרונה האפשרית.", do=show("r-1")),
    P("סימן שאלה אחריהם הופך אותם לעצלנים: עד ההתאמה הראשונה. ועם כוכבית, אפילו אפס תווים.", do=show("r-2")),
    P("סימן שאלה אחרי תו רגיל: אופציונלי.", do=show("r-3")),
    P("וקבוצות: אפס זה הכול, ואחת, שתיים לפי סדר הסוגריים. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.calls("rc", [("re.search(r'\".+\"', s).group()", repr(FG[0])),
                                                  ("re.search(r'\".+?\"', s).group()", repr(FZ[0]))], shown=(0, 1))
         + "</div>",
   panel=st.card("r-1", "rule", "🔑 " + rx(".+") + " " + rx(".*") + " חמדנים")
         + st.card("r-2", "rule", "🔑 " + rx(".+?") + " " + rx(".*?") + " עצלנים")
         + st.card("r-3", "trap", "⚠️ " + rx("u?") + " = אופציונלי")
         + st.card("r-4", "rule", "🔑 " + rx("group(0)") + " = הכול"))

VIDEO = w.no_latin(Video("T05", "text", "חמדן מול עצלן, וקבוצות", [title, greedy, lazy, groups, exam, recap],
                         bank={"P-66": 0}))

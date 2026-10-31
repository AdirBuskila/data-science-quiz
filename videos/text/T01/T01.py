# -*- coding: utf-8 -*-
"""T01 · אבני הבניין של ביטוי רגולרי — video script (build: tools/video/vid.py T01).

Source: courses/text/T01.js (lesson + goal). Exam anchor: 25A-B-Q24 (what r'\\b[a-zA-Z]+\\b' represents), used by no
guided quiz (the gate refuses quiz ids).
Avoided on purpose: the T01 quiz (mary / [A-Z] on "Dana and Dan" / \\d\\d on "a1b22c333" / \\b\\w on "hi big world" /
.a on "banana") and its twin P-64; the boss items P-61/P-62 (Dina), 25-S-Q4, 24A-B-Q4. Every example below uses new
strings, and every highlighted match comes from re.finditer on the exact string shown (w_text.hits).
"""
import re

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx

# ---------------------------------------------------------------- examples (verified)
S1 = "Cat sat AT bat"
L1, F1 = w.hits("a1", r"at", S1)
assert F1 == ["at", "at", "at"] and [l[1] for l in L1] == [1, 5, 12]       # inside Cat, sat, bat; AT is not at

S2 = "cat cut c t cot"
L2, F2 = w.hits("a2", r"c.t", S2)
assert F2 == ["cat", "cut", "c t", "cot"]                                  # the dot takes the space too

S3 = "R2-D2 and C3PO"
L3, F3 = w.hits("a3", r"[A-Z]\d", S3)
assert F3 == ["R2", "D2", "C3"]                                            # P is not followed by a digit

S4 = "on bond icon one"
L4a, F4a = w.hits("a4", r"on", S4)
L4b, F4b = w.hits("a5", r"\bon", S4)
assert len(F4a) == 4 and [l[1] for l in L4b] == [0, 13]                    # only where a word starts

# exam 25A-B-Q24
Q = BANK["25A-B-Q24"]
PAT = r"\b[a-zA-Z]+\b"
assert Q["correctIndex"] == 0 and PAT in Q["question"]
S5 = "Hi R2D2, go_now ok"
L5, F5 = w.hits("a6", PAT, S5)
assert F5 == ["Hi", "ok"]                     # R2D2 and go_now hold digits / underscore: no boundary inside them
assert re.findall(PAT, "HeLLo wOrLD") == ["HeLLo", "wOrLD"]                # any mix of upper and lower case
assert re.findall(PAT, "Bob") == ["Bob"] and re.findall(r"\bb", "Bob") == []   # \b is a place, not the letter b
assert re.fullmatch(r"[a-zA-Z]", "z") and not re.fullmatch(r"[a-zA-Z]", "zA")  # [a-zA-Z] is ONE character
OPTS = [(i, w.esc(o)) for i, o in enumerate(Q["options"])]
ORDER = [2, 0, 3, 1]
OPTS = [OPTS[i] for i in ORDER]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לקרוא את אבני הבניין של ביטוי רגולרי."),
    P("תו רגיל, נקודה, סוגריים מרובעים, הקיצורים של ספרה, מילה ורווח, וגבול מילה."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">T01 · ביטויים רגולריים וטקסט</div><h1>אבני הבניין של ביטוי רגולרי</h1>'
         '<p>לקרוא תבנית פשוטה: תו מילולי, נקודה, מחלקת תווים, ' + rx(r"\d \w \s") + ' וגבול מילה, ולדעת מה היא '
         'תופסת בטקסט.</p>', layout="title")

idea = Scene("idea", "תבנית מילולית", [
    P("ביטוי רגולרי הוא **תבנית**: תיאור של מחרוזות שאנחנו מחפשים בתוך טקסט.", do=show("i-code")),
    P("בפייתון משתמשים במודול re, והפונקציה findall מחזירה רשימה של כל ההתאמות.",
      say="בפייתון משתמשים במודול של ביטויים רגולריים, והפונקציה פַיינְד אוֹל מחזירה רשימה של כל ההתאמות."),
    P("את התבנית כותבים כמחרוזת עם r לפניה, כדי שהלוכסן ההפוך יישאר כמו שהוא.", do=show("i-c1"),
      say="את התבנית כותבים כמחרוזת עם האות אָר לפניה, כדי שהלוכסן ההפוך יישאר כמו שהוא."),
    w.L("התבנית הכי פשוטה היא תווים רגילים. כאן: האות [[a|אֵיי]] ואחריה [[t|טִי]].", do=show("a1")),
    P("סורקים את הטקסט משמאל לימין. ההתאמה הראשונה נמצאת בתוך המילה Cat.", do=show("a1-m0"),
      say="סורקים את הטקסט משמאל לימין. ההתאמה הראשונה נמצאת בתוך המילה קֶט."),
    P("השנייה בתוך sat. התבנית לא מתעניינת במילים, רק ברצף התווים.", do=show("a1-m1"),
      say="השנייה בתוך סֶט. התבנית לא מתעניינת במילים, רק ברצף התווים."),
    P("את AT באותיות גדולות היא **מדלגת**: אות גדולה היא תו אחר.", do=show("i-c2"),
      say="את המילה אֵיי טִי באותיות גדולות היא מדלגת: אות גדולה היא תו אחר."),
    P("והשלישית בתוך bat. סך הכול שלוש התאמות.", do=show("a1-m2", "i-out"), hold=0.4,
      say="והשלישית בתוך בֶּט. סך הכול שלוש התאמות."),
], stage='<div class="tx-stack">' + w.code("i-code", 're.findall(r"at", "Cat sat AT bat")')
         + w.strip("a1", S1, L1, hidden=True) + w.out("i-out", repr(F1)) + "</div>",
   panel=st.card("i-c1", "rule", "🔑 " + rx('r"..."') + ": מחרוזת גולמית, הלוכסן ההפוך נשאר")
         + st.card("i-c2", "trap", "⚠️ רגיש לאותיות גדולות וקטנות: " + rx("at") + " לא תופס " + rx("AT")))

PIECES = [(".", "תו כלשהו"), ("[aeiou]", "אחד מהקבוצה"), ("[A-Z]", "אחד מהטווח"),
          (r"\d", "ספרה"), (r"\w", "אות, ספרה או _"), (r"\s", "רווח")]
cls = Scene("one", "סימן אחד, תו אחד", [
    P("עכשיו הסימנים המיוחדים. הנקודה תופסת **תו אחד כלשהו**.", do=show("o-p0")),
    P("סוגריים מרובעים תופסים תו אחד מתוך קבוצה, למשל אחת מחמש התנועות.", do=show("o-p1")),
    w.L("ומקף בתוך הסוגריים הוא טווח: כל אות גדולה מ-[[A|אֵיי]] עד [[Z|זֶד]].", do=show("o-p2")),
    P("ויש שלושה קיצורים: ספרה, תו מילה, ורווח.", do=show("o-p3", "o-p4", "o-p5")),
    P("תו מילה הוא אות, ספרה, או קו תחתון.", do=show("o-c1")),
    P("והכלל החשוב: כל סימן כזה תופס **תו אחד בלבד**.", do=show("o-c2"), hold=0.3),
    w.L("נבדוק: האות [[c|סִי]], תו כלשהו, והאות [[t|טִי]].", do=show("o-code", "a2")),
    P("נתפסות cat, cut ו-cot: בכל אחת האות שבאמצע שונה.", do=show("a2-m0", "a2-m1", "a2-m3"),
      say="נתפסות המילים קֶט, קַט וקוֹט, ובכל אחת האות שבאמצע מתחלפת."),
    w.L("אבל גם [[c|סִי]], רווח, [[t|טִי]] נתפס. הנקודה תופסת **גם רווח**, כי רווח הוא תו.", do=show("a2-m2", "o-out")),
    P("הנקודה לא בודקת אם זו אות. היא רק דורשת שיהיה שם תו אחד.", hold=0.4),
], stage='<div class="tx-stack">' + w.parts("o", PIECES) + w.code("o-code", 're.findall(r"c.t", "cat cut c t cot")')
         + w.strip("a2", S2, L2, hidden=True) + w.out("o-out", repr(F2)) + "</div>",
   panel=st.card("o-c1", "ex", rx(r"\w") + " = אות, ספרה או קו תחתון")
         + st.card("o-c2", "rule", "🔑 כל סימן תופס <b>תו אחד</b>. שני תווים? כותבים שני סימנים"))

pair = Scene("pair", "שני סימנים ברצף", [
    P("סימנים שכתובים ברצף צריכים להתאים לתווים רצופים בטקסט.", do=show("p-code", "a3")),
    P("כאן: אות גדולה, ומיד אחריה ספרה.", do=show("p-c1")),
    P("R ו-2: אות גדולה וספרה. נתפס.", do=show("a3-m0"), say="אָר ושתיים: אות גדולה וספרה. נתפס."),
    P("המקף לא אות גדולה, אז ממשיכים. D2 נתפס.", do=show("a3-m1"), say="המקף לא אות גדולה, אז ממשיכים. דִּי ושתיים נתפס."),
    w.L("המילה [[and|אֶנְד]] באותיות קטנות לא מתאימה. [[C3|סִי ושלוש]] נתפס.", do=show("a3-m2")),
    P("ובסוף P ו-O: אחרי P בא O, שהיא לא ספרה. אין התאמה.", do=show("p-out"),
      say="ובסוף פִּי ואוֹ: אחרי הפִּי באה האות אוֹ, שהיא לא ספרה. אין התאמה."),
    P("כל התאמה כאן היא בדיוק **שני תווים**, אחד לכל סימן.", do=show("p-c2"), hold=0.4),
], stage='<div class="tx-stack">' + w.code("p-code", r're.findall(r"[A-Z]\d", "R2-D2 and C3PO")')
         + w.strip("a3", S3, L3, hidden=True) + w.out("p-out", repr(F3)) + "</div>",
   panel=st.card("p-c1", "plain", rx("[A-Z]") + " ואחריו " + rx(r"\d") + ": אות גדולה ואז ספרה")
         + st.card("p-c2", "rule", "🔑 שני סימנים = שני תווים רצופים"))

edge = Scene("edge", "גבול מילה", [
    w.L("הסימן האחרון להיום: לוכסן הפוך ואות [[b|בִּי]]. זה **גבול מילה**.", do=show("e-c1")),
    P("הוא לא תופס אף תו. הוא דורש **מקום**: מעבר בין תו מילה לתו שאינו תו מילה, או קצה הטקסט.", do=show("e-c2")),
    w.L("נחפש קודם את האותיות [[o|אוֹ]] ו-[[n|אֶן]] בלי גבול. יש ארבע התאמות.", do=show("e-code1", "a4", "a4-m0", "a4-m1", "a4-m2", "a4-m3")),
    P("גם בתוך bond, וגם בסוף icon.", say="גם בתוך המילה בּוֹנְד, וגם בסוף המילה אַייקוֹן."),
    w.L("עכשיו עם גבול מילה לפני: [[on|אוֹ ואֶן]] חייבים לפתוח מילה.", do=hide("e-code1", "a4") + show("e-code2", "a5")),
    P("בהתחלה, לפני ה-o יש קצה טקסט. זה גבול, ולכן נתפס.", do=show("a5-m0"),
      say="בהתחלה, לפני האוֹ יש קצה טקסט. זה גבול, ולכן נתפס."),
    P("בתוך bond, לפני ה-o בא b, תו מילה. אין גבול, אין התאמה.", do=show("a5-no1"),
      say="בתוך המילה בּוֹנְד, לפני האוֹ באה האות בִּי, שהיא תו מילה. אין גבול, אין התאמה."),
    P("גם בתוך icon אין גבול. אבל one מתחילה אחרי רווח, ולכן נתפסת.", do=show("a5-no2", "a5-m1", "e-out"),
      say="גם בתוך אַייקוֹן אין גבול. אבל וואן מתחילה אחרי רווח, ולכן נתפסת."),
    P("שתי התאמות במקום ארבע. גבול המילה לא נוסף לתוצאה, הוא רק סינן.", hold=0.4),
], stage='<div class="tx-stack">' + '<div class="swap" style="--swap-h:90px">'
         + "<div>" + w.code("e-code1", f're.findall(r"on", "{S4}")') + "</div>"
         + "<div>" + w.code("e-code2", rf're.findall(r"\bon", "{S4}")') + "</div>"
         + "</div>"
         + '<div class="swap" style="--swap-h:110px">'
         + "<div>" + w.strip("a4", S4, L4a, hidden=True) + "</div>"
         + "<div>" + w.strip("a5", S4, L4b + [("a5-no1", 4, 6, "no"), ("a5-no2", 10, 12, "no")], hidden=True) + "</div>"
         + "</div>" + w.out("e-out", repr(F4b)) + "</div>",
   panel=st.card("e-c1", "rule", "🔑 " + rx(r"\b") + " = גבול מילה")
         + st.card("e-c2", "ex", "לא תו, אלא <b>מקום</b>: בין תו מילה לתו שאינו תו מילה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה מייצג הביטוי הזה?", do=show("x-big")),
    P("נפרק אותו. בהתחלה ובסוף: גבול מילה.", do=show("x-p0", "x-p3")),
    P("באמצע: סוגריים מרובעים עם שני טווחים, אות קטנה או אות גדולה. זה **תו אחד**.", do=show("x-p1")),
    P("והפלוס אחריהם אומר: פעם אחת או יותר. נכיר אותו לעומק ברמה הבאה.", do=show("x-p2")),
    P("כלומר: רצף של אותיות בלבד, שמתחיל ונגמר בגבול מילה.", hold=0.3),
    P("נריץ על טקסט. המילים Hi ו-ok נתפסות.", do=show("x-s", "a6-m0", "a6-m1"),
      say="נריץ על טקסט. המילים הַיי ואוֹקֵיי נתפסות."),
    P("אבל לא R2D2 ולא go_now: הספרות והקו התחתון הם תווי מילה, אז באמצע אין גבול.", do=show("x-out"),
      say="אבל לא המילה עם הספרות, וגם לא המילה עם הקו התחתון: ספרות וקו תחתון הם תווי מילה, אז באמצע אין גבול."),
    P("ולכן התשובה: מילים שמורכבות משילוב של אותיות גדולות או קטנות.", do=show("q-ok-0")),
    P("המלכודות כולן באותו מקום: לקרוא את התבנית כאילו היא טקסט רגיל.", hold=0.2),
    w.L("לוכסן ו-[[b|בִּי]] הוא גבול, לא האות [[b|בִּי]]. לכן לא מילים שמתחילות ונגמרות ב-[[b|בִּי]].", do=show("q-x-2")),
    w.L("ובתוך הסוגריים, [[a-z|אֵיי מקף זֶד]] הוא טווח של תו אחד, לא הצירוף שלהן.", do=show("q-x-3")),
    P("וגם אין שום דרישה ל**זוגות** של קטנה ואז גדולה. כל שילוב מתאים.", do=show("q-x-1"), hold=0.6),
], stage='<div class="tx-stack">' + w.big("x-big", PAT, hidden=True)
         + w.parts("x", [(r"\b", "גבול"), ("[a-zA-Z]", "אות אחת"), ("+", "פעם או יותר"), (r"\b", "גבול")], PAT, small=True)
         + w.strip("x-s", S5, L5, hidden=True) + w.out("x-out", repr(F5)) + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>מה מייצג הביטוי הרגולרי הבא: '
         + rx("r'" + PAT + "'") + "</div>"
         + st.options("q", OPTS))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תו רגיל תופס את עצמו, ורגיש לאותיות גדולות וקטנות.", do=show("r-1")),
    P("נקודה, סוגריים מרובעים, וספרה, מילה ורווח: כל אחד תופס תו אחד בדיוק.", do=show("r-2")),
    P("נקודה תופסת גם רווח. ותו מילה כולל ספרות וקו תחתון.", do=show("r-3")),
    P("וגבול מילה לא תופס תו בכלל, רק מקום. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.parts("rp", PIECES + [(r"\b", "גבול מילה")], hidden=False, small=True) + "</div>",
   panel=st.card("r-1", "rule", "🔑 " + rx("at") + " ≠ " + rx("AT"))
         + st.card("r-2", "rule", "🔑 סימן אחד = תו אחד")
         + st.card("r-3", "trap", "⚠️ " + rx(".") + " תופסת גם רווח")
         + st.card("r-4", "trap", "⚠️ " + rx(r"\b") + " הוא מקום, לא האות " + rx("b")))

VIDEO = w.no_latin(Video("T01", "text", "אבני הבניין של ביטוי רגולרי", [title, idea, cls, pair, edge, exam, recap],
                         bank={"25A-B-Q24": 0}))

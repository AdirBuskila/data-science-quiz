# -*- coding: utf-8 -*-
"""T06 · לכתוב תבנית שתופסת בדיוק מה שצריך — video script (build: tools/video/vid.py T06).

Source: courses/text/T06.js (lesson + goal). Exam anchor: 24A-A-Q4 (what r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
returns: e-mail addresses), used by no guided quiz. It is cited in the T03 lesson; the T03 quiz item that tests
strings against the same pattern (dan.k@mail.co.il, dan@mail, @mail.com, "dan k@mail.com") is not used: the video
tests its own strings.
Avoided on purpose: the T06 quiz (phones = P-63, prices = 25A-A-Q12, AB-1234 codes, dates, hashtags) and the
lesson's CD-99999 trap; 24A-B-Q5 (its keyed option does not match the question's own examples, see the report).
Every highlight / verdict is a real re run on the string shown.
"""
import re

from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_text as w
from w_text import rx, L

# ---------------------------------------------------------------- worked example: a 7-digit licence plate 12-345-67
S = "a 12-345-67 b 12-345-678"
TRY = [r"\d+-\d+-\d+", r"\d{2}-\d{3}-\d{2}", r"\b\d{2}-\d{3}-\d{2}\b"]
L1, F1 = w.hits("p1", TRY[0], S)
L2, F2 = w.hits("p2", TRY[1], S)
L3, F3 = w.hits("p3", TRY[2], S)
assert F1 == ["12-345-67", "12-345-678"]          # too loose: the 8-digit one comes in whole
assert F2 == ["12-345-67", "12-345-67"]           # exact lengths, but a piece of the long one is caught
assert F3 == ["12-345-67"]                        # \b: after the 7 comes 8, a word character -> no boundary
assert L2[1][1:3] == (14, 23) and S[23] == "8"
NO2 = [("p2-tail", 23, 24, "no")]
assert re.findall(TRY[1], "112-345-67") == ["12-345-67"] and re.findall(TRY[2], "112-345-67") == []

# ---------------------------------------------------------------- exam 24A-A-Q4
Q = BANK["24A-A-Q4"]
PAT = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
assert Q["correctIndex"] == 0 and PAT in Q["question"]
PIECES = [("^", "התחלה"), ("[a-zA-Z0-9._%+-]+", "שם המשתמש"), ("@", "שטרודל"), ("[a-zA-Z0-9.-]+", "דומיין"),
          (r"\.", "נקודה"), ("[a-zA-Z]{2,}", "סיומת: 2 אותיות או יותר"), ("$", "סוף")]
ROWS = ["noa_levi@mail.com", "054-1234567", "www.facebook.com", "John F. Kennedy"]
TESTS, RES = w.tests("t", PAT, ROWS)
assert RES == [True, False, False, False]
assert "@" not in ROWS[1] + ROWS[2] + ROWS[3]       # phone, site, name: no '@', and the pattern demands one
assert re.fullmatch(r"[a-zA-Z0-9._%+-]", ".")       # inside [ ] the dot is a plain character
OPTS = [(i, w.esc(o)) for i, o in enumerate(Q["options"])]
OPTS = [OPTS[i] for i in [1, 3, 0, 2]]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה לא רק נקרא תבניות, אלא נבנה אחת בעצמנו."),
    P("השיטה: לא מנחשים. בודקים כל תבנית על דוגמאות, ומתקנים."),
    P("ובסוף נקרא תבנית ארוכה ממבחן, ונבדוק אותה באותה שיטה.", hold=0.4),
], stage='<div class="kicker">T06 · ביטויים רגולריים וטקסט</div><h1>לכתוב תבנית שתופסת בדיוק מה שצריך</h1>'
         '<p>לבחור או לכתוב תבנית שתופסת את כל מה שצריך ולא תופסת שום דבר אחר, על ידי בדיקה על דוגמאות.</p>',
   layout="title")

method = Scene("method", "השיטה", [
    P("שלושה צעדים. אחד: כותבים במילים מה צריך לתפוס, חלק אחרי חלק.", do=show("m-1")),
    P("שניים: לכל חלק בוחרים סימן, וכמת **מדויק**. אם האורך קבוע, סוגריים מסולסלים ולא פלוס.", do=show("m-2")),
    P("שלושה: מוסיפים גבול מילה, כדי שהתבנית לא תתפוס **חלק** ממילה או ממספר ארוך יותר.", do=show("m-3")),
    P("ואחרי כל צעד בודקים על הדוגמאות: מה נתפס שלא היה צריך, ומה לא נתפס.", do=show("m-4"), hold=0.4),
], stage='<div class="tx-stack">' + st.card("m-1", "ex", "1. במילים: מה תופסים, חלק אחרי חלק")
         + st.card("m-2", "ex", "2. סימן לכל חלק, וכמת מדויק: " + rx("{3}") + " ולא " + rx("+"))
         + st.card("m-3", "ex", "3. " + rx(r"\b") + " בקצוות, כדי לא לתפוס חלק ממשהו ארוך")
         + "</div>",
   panel=st.card("m-4", "rule", "🔑 בודקים על דוגמאות: מה נתפס סתם, ומה התפספס"))

build = Scene("build", "בונים תבנית", [
    P("משימה: למצוא בטקסט מספרי רכב של שבע ספרות: שתיים, מקף, שלוש, מקף, שתיים.", do=show("b-txt")),
    P("בטקסט יש מספר תקין אחד, ועוד מספר ארוך מדי, עם ספרה מיותרת בסוף.", hold=0.1),
    P("ניסיון ראשון: ספרות, מקף, ספרות, מקף, ספרות. עם פלוס בכל מקום.", do=show("b-c1", "p1") + w.show_hits("p1", 0, 2)),
    P("נתפסו שניהם. המספר הארוך נכנס כולו, כי לפלוס לא אכפת מהאורך.", do=show("b-o1", "b-k1")),
    P("ניסיון שני: כמת מדויק. שתיים, שלוש, ושתיים.", do=show("b-c2", "p2") + w.show_hits("p2", 0, 2)),
    P("עדיין שתי התאמות! מתוך המספר הארוך נתפס חלק, והספרה האחרונה נשארה בחוץ.", do=show("p2-tail", "b-o2", "b-k2")),
    P("ניסיון שלישי: גבול מילה בשני הקצוות.", do=show("b-c3", "p3") + w.show_hits("p3", 0, 1)),
    P("עכשיו אחרי השבע בא שמונה, שהוא תו מילה. אין שם גבול, ולכן המספר הארוך נפסל.", do=show("b-o3", "b-k3")),
    P("והגבול בהתחלה עובד באותו אופן: ממספר עם ספרה מיותרת **בהתחלה**, התבנית לא תתפוס את שבע הספרות האחרונות.", hold=0.1),
    P("מה שנשאר: בדיוק המספר התקין, ושום דבר אחר. זו המטרה.", hold=0.4),
], stage='<div class="tx-stack">' + w.code("b-txt", f's = "{S}"', size=34)
         + w.code("b-c1", f're.findall(r"{TRY[0]}", s)', size=28) + w.strip("p1", S, L1, hidden=True, cw=36)
         + w.out("b-o1", repr(F1), size=28)
         + w.code("b-c2", f're.findall(r"{TRY[1]}", s)', size=28) + w.strip("p2", S, L2 + NO2, hidden=True, cw=36)
         + w.out("b-o2", repr(F2), size=28)
         + w.code("b-c3", f're.findall(r"{TRY[2]}", s)', size=28) + w.strip("p3", S, L3, hidden=True, cw=36)
         + w.out("b-o3", repr(F3), size=28) + "</div>",
   panel=st.card("b-k1", "trap", "⚠️ " + rx("+") + " לא בודק אורך")
         + st.card("b-k2", "trap", "⚠️ אורך מדויק, אבל חלק ממספר ארוך")
         + st.card("b-k3", "rule", "🔑 " + rx(r"\b...\b") + " = רק מספר שלם"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: אילו מחרוזות יחזיר הביטוי הזה? הוא ארוך, אז נקרא אותו חלק אחרי חלק.", do=show("x-p0", "x-p6")),
    P("כובע ודולר: כל המחרוזת חייבת להתאים.", hold=0.1),
    P("חלק ראשון: אותיות, ספרות, נקודה, קו תחתון, אחוז, פלוס או מקף, פעם אחת או יותר.", do=show("x-p1")),
    P("בתוך הסוגריים המרובעים הנקודה היא סתם נקודה, וכך גם הפלוס.", hold=0.1),
    P("אחריו שטרודל, ואחריו אותיות, ספרות, נקודות ומקפים.", do=show("x-p2", "x-p3")),
    P("ובסוף: לוכסן ונקודה, כלומר נקודה אמיתית, ואז לפחות שתי אותיות.", do=show("x-p4", "x-p5"), hold=0.3),
    P("שם, שטרודל, דומיין, נקודה וסיומת. זו כתובת אימייל. נבדוק על דוגמאות.", do=show("t-r0", "t-v0")),
    P("מספר טלפון: אין בו שטרודל, והתבנית דורשת אחד. נפסל.", do=show("t-r1", "t-v1", "q-x-1")),
    P("כתובת של אתר: גם בה אין שטרודל. נפסלת.", do=show("t-r2", "t-v2", "q-x-2")),
    P("ושם מלא: יש בו רווחים, ואין שטרודל. נפסל.", do=show("t-r3", "t-v3", "q-x-3")),
    P("כלומר, מה שעובר חייב שטרודל באמצע, וסיומת של אותיות אחרי נקודה בסוף.", hold=0.1),
    P("אז התשובה: כתובות אימייל.", do=show("q-ok-0")),
    P("המלכודת: הנקודה. בתוך סוגריים מרובעים היא תו רגיל, ובחוץ צריך לוכסן כדי שתהיה נקודה אמיתית.", hold=0.6),
], stage='<div class="tx-stack">' + w.parts("x", PIECES, PAT, small=True) + TESTS + "</div>",
   panel=f'<div class="qstem"><span class="qid">{Q["id"]}</span>אילו מחרוזות יחזיר הביטוי הרגולרי הבא?<br>'
         + rx("r'" + PAT + "'", "xs") + "</div>" + st.options("q", OPTS))

recap = Scene("recap", "סיכום", [
    P("לסיכום: לא מנחשים תבנית. בודקים אותה על דוגמאות.", do=show("r-1")),
    P("פלוס לא בודק אורך. כשהאורך קבוע, כותבים כמת מדויק.", do=show("r-2")),
    P("גבול מילה בקצוות מונע לתפוס חלק ממספר או ממילה ארוכים יותר.", do=show("r-3")),
    P("ונקודה: בתוך סוגריים מרובעים היא תו רגיל, ובחוץ כותבים לוכסן ונקודה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage='<div class="tx-stack">' + w.big("r-big", TRY[2], size=44) + "</div>",
   panel=st.card("r-1", "rule", "🔑 בודקים על דוגמאות")
         + st.card("r-2", "trap", "⚠️ " + rx("+") + " לא בודק אורך: " + rx("{n}"))
         + st.card("r-3", "rule", "🔑 " + rx(r"\b") + " בקצוות")
         + st.card("r-4", "trap", "⚠️ " + rx("[.]") + " נקודה · " + rx(r"\.") + " נקודה · " + rx(".") + " כל תו"))

VIDEO = w.no_latin(Video("T06", "text", "לכתוב תבנית שתופסת בדיוק מה שצריך", [title, method, build, exam, recap],
                         bank={"24A-A-Q4": 0}))

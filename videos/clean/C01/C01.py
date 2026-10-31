# -*- coding: utf-8 -*-
"""C01 · סולמות מדידה — video script (build: tools/video/vid.py C01).

Source: courses/clean/C01.js (lesson + goal: classify a variable into one of the four scales and know which
statistic each scale allows). Exam anchor: 24B-B-Q19 (the main difference between ordinal and interval: equal
intervals), which no guided quiz uses.
Avoided on purpose: every C01 quiz variable and number (Celsius 10/20 and Kelvin, star ratings, blood type, height,
the 10.0 / 10.1 / 15.0 race) and the boss item 24A-A-Q3 (ordinal vs interval: mode / mean), plus its content twin
25A-B-Q7 (Celsius as the classic interval variable). Worked examples are my own: eye colour and jersey numbers
(nominal), shirt sizes (ordinal), calendar years (interval: the Gregorian and Hebrew calendars only move the zero),
weight in kg / lb (ratio). Every value is computed below; the ladder's operations come from w_clean.OPS, which
mirrors the course checker's rule table (tools/verify/needhelp/clean/check.py).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_clean as w

# ---------------------------------------------------------------- facts (verified)
assert w.OPS["nominal"] == ["שכיח"]
assert w.new_ops("ordinal") == ["חציון"] and w.new_ops("interval") == ["ממוצע", "הפרשים"] and w.new_ops("ratio") == ["יחסים"]

# nominal: the mode of eye colours, by the code that is shown
EYE_SRC = "eyes = pd.Series(['brown', 'blue', 'brown', 'green'])\nprint(eyes.mode()[0])"
env, EYE_OUT = w.run(EYE_SRC)
assert EYE_OUT == "brown"

# ordinal: shirt sizes, median by order; a numeric code 1..4 gives a "mean" that the sizes do not support
ORDER = ["S", "M", "L", "XL"]
SIZES = ["M", "S", "XL", "M", "L"]
srt = sorted(SIZES, key=ORDER.index)
assert srt == ["S", "M", "M", "L", "XL"] and srt[len(srt) // 2] == "M"
codes = [ORDER.index(s) + 1 for s in SIZES]
assert codes == [2, 1, 4, 2, 3] and sum(codes) / len(codes) == 2.4

# interval: calendar years. Moving the zero (Hebrew calendar = Gregorian + 3760) keeps differences, breaks ratios
G1, G2, SHIFT = 1000, 2000, 3760
H1, H2 = G1 + SHIFT, G2 + SHIFT
assert (H1, H2) == (4760, 5760)
assert G2 - G1 == H2 - H1 == 1000
assert G2 / G1 == 2 and round(H2 / H1, 2) == 1.21

# ratio: weight; a change of unit multiplies, so ratios survive
KG = (10, 5)
LB = tuple(round(k * 2.20462, 2) for k in KG)
assert LB == (22.05, 11.02) and KG[0] / KG[1] == 2 and abs(LB[0] / LB[1] - 2) < 0.01

# exam 24B-B-Q19
Q = BANK["24B-B-Q19"]
assert Q["correctIndex"] == 0 and Q["options"][0].startswith("בסולם רווח המרווחים בין הערכים שווים")
OPTS = list(enumerate(Q["options"]))

LAD = w.ladder("ld", examples={"nominal": "צבע עיניים", "ordinal": "מידת חולצה", "interval": "שנה בלוח השנה",
                               "ratio": "משקל בק״ג"})

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לסווג משתנה לאחד מארבעה סולמות מדידה."),
    P("נראה איזה חישוב מותר בכל סולם, ולמה מספר לא תמיד מתנהג כמו מספר."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">C01 · ניקוי נתונים וסולמות</div><h1>סולמות מדידה</h1>'
         '<p>לסווג משתנה לאחד מארבעת הסולמות, ולדעת איזה חישוב מותר בכל סולם.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("נתחיל בשאלה: מה הממוצע של מספרי החולצות בקבוצת כדורגל?", do=show("i-j")),
    P("אפשר לחשב אותו, אבל הוא לא אומר כלום. המספר שבע הוא רק **שם** של שחקן.", do=show("i-c1")),
    P("לכן לפני שמחשבים, שואלים: מה המספרים האלה באמת מודדים?"),
    P("התשובה נקראת **סולם המדידה** של המשתנה. יש ארבעה סולמות, מהחלש לחזק.", do=show("i-c2")),
    P("וכל סולם קובע אילו חישובים הגיוניים עליו.", hold=0.3),
], stage=w.stack(w.big("i-j", "10 · 7 · 23 · 4 · 7", size=64), gap=30),
   panel=st.card("i-c1", "trap", "⚠️ מספר חולצה: מספר, אבל רק <b>שם</b>")
         + st.card("i-c2", "rule", "🔑 סולם המדידה קובע אילו חישובים מותרים"))

lad = Scene("ladder", "ארבעה סולמות", [
    P("הסולם הראשון, והחלש ביותר: סולם **שמי**. הערכים הם רק שמות, בלי סדר ביניהם.", do=show("ld-r0")),
    P("למשל צבע עיניים. חום לא ״גדול״ מכחול. מה שמותר כאן הוא רק השכיח.", do=show("ld-x0")),
    P("מעליו סולם **סדר**: יש סדר בין הערכים, אבל המרווחים ביניהם לא בהכרח שווים.", do=show("ld-r1")),
    P("למשל מידת חולצה: קטנה, בינונית, גדולה. כאן מותר גם חציון.", do=show("ld-x1")),
    P("אחריו סולם **רווח**: המרווחים שווים, אבל אין אפס אמיתי.", do=show("ld-r2")),
    P("למשל שנה בלוח השנה. כאן מותר גם ממוצע, ומותר לחסר ולקבל הפרש בעל משמעות.", do=show("ld-x2")),
    P("ולמעלה סולם **מנה**: מרווחים שווים, **וגם** אפס אמיתי, שמשמעותו ״אין בכלל״.", do=show("ld-r3")),
    P("למשל משקל בקילוגרמים. רק כאן מותר לומר ״פי שניים״.", do=show("ld-x3")),
    P("שימו לב לכלל: כל סולם יורש את כל החישובים של הסולם שמתחתיו, ומוסיף משהו.", do=show("l-c1"), hold=0.4),
], stage=LAD,
   panel=st.card("l-c1", "rule", "🔑 שמי ← שכיח · סדר ← + חציון · רווח ← + ממוצע והפרשים · מנה ← + יחסים"))

nominal = Scene("nominal", "שמי מול סדר", [
    P("נתחיל מלמטה. בסולם שמי מחשבים שכיח, וזה גם מה ש-pandas עושה עם mode.", do=show("n-code"),
      say="נתחיל מלמטה. בסולם שמי מחשבים שכיח, וזה גם מה שפַּנְדָס עושה עם מוֹד."),
    P("ארבעה צבעי עיניים, והשכיח הוא חום, כי הוא מופיע פעמיים.", do=show("n-out")),
    P("ממוצע של צבעים? אין דבר כזה. וגם חציון אין, כי אין סדר שלפיו נמצא את האמצע.", do=show("n-c1")),
    P("עכשיו מידות חולצה. חמישה לקוחות קנו בינונית, קטנה, גדולה מאוד, בינונית וגדולה.", do=show("n-sz")),
    P("כאן **יש** סדר, ולכן אפשר למיין: מהקטנה ועד הגדולה מאוד.", do=show("n-srt")),
    P("החציון הוא הערך האמצעי, השלישי מתוך חמישה: מידה בינונית.", do=show("n-med", "n-c2"), hold=0.3),
    P("ומה עם ממוצע? נניח שנקודד את המידות כאחת, שתיים, שלוש וארבע.", do=show("n-cod")),
    P("הממוצע יוצא 2.4. אבל ההפרש בין קטנה לבינונית לא בהכרח שווה להפרש בין גדולה לגדולה מאוד.",
      do=show("n-avg"), say="הממוצע יוצא שתיים נקודה ארבע. אבל ההפרש בין קטנה לבינונית לא בהכרח שווה להפרש בין גדולה לגדולה מאוד."),
    P("המספרים כאן רק שומרים על הסדר, ולכן 2.4 לא מתאר שום מידה אמיתית: ממוצע דורש מרווחים שווים.", do=show("n-c3"),
      say="המספרים כאן רק שומרים על הסדר, ולכן שתיים נקודה ארבע לא מתאר שום מידה אמיתית: ממוצע דורש מרווחים שווים."),
], stage=w.stack(
    w.code("n-code", EYE_SRC, hidden=True, size=28),
    w.out("n-out", EYE_OUT),
    w.big("n-sz", "M · S · XL · M · L", size=44),
    w.big("n-srt", 'S · M · <b class="cl-mid">M<i id="n-med" class="cl-ringx h"></i></b> · L · XL', size=44),
    w.big("n-cod", "2 · 1 · 4 · 2 · 3", size=40),
    w.big("n-avg", "(2+1+4+2+3) / 5 = 2.4", size=36), gap=20),
   panel=st.card("n-c1", "plain", "שמי: רק <b>שכיח</b>")
         + st.card("n-c2", "ex", "סדר: אפשר למיין, ולכן יש <b>חציון</b>")
         + st.card("n-c3", "trap", "⚠️ קידוד 1, 2, 3, 4 לא הופך סדר למרווחים שווים"))

zero = Scene("zero", "רווח מול מנה", [
    P("ומה מבדיל בין רווח למנה? האפס. נבדוק את זה עם שנים בלוח השנה.", do=show("z-t")),
    P("משנת 1000 לשנת 2000 עברו אלף שנה. האם שנת 2000 ״פי שניים״ משנת 1000?",
      say="משנת אלף לשנת אלפיים עברו אלף שנה. האם שנת אלפיים פי שניים משנת אלף?"),
    P("בלוח השנה העברי אותן שתי שנים הן 4760 ו-5760, כי הספירה מתחילה בנקודה אחרת.", do=show("z-h"),
      say="בלוח השנה העברי אותן שתי שנים הן ארבעת אלפים שבע מאות שישים, וחמשת אלפים שבע מאות שישים, כי הספירה מתחילה בנקודה אחרת."),
    P("ההפרש נשאר אלף שנה בשני הלוחות. אבל היחס? בלועזי שתיים, ובעברי בערך 1.21.", do=show("z-r"),
      say="ההפרש נשאר אלף שנה בשני הלוחות. אבל היחס? בלועזי שתיים, ובעברי בערך אחת נקודה עשרים ואחת."),
    P("יחס שמשתנה כשמזיזים את האפס הוא יחס בלי משמעות. לכן שנה היא סולם **רווח**.", do=show("z-c1"), hold=0.3),
    P("עכשיו משקל: עשרה קילו וחמישה קילו. בקילוגרמים, היחס הוא שתיים.", do=show("z-w")),
    P("נעבור לליברות: בערך 22.05 ו-11.02. ושוב, היחס הוא שתיים.", do=show("z-lb"),
      say="נעבור לליברות: בערך עשרים ושתיים, ובערך אחת עשרה. ושוב, היחס הוא שתיים."),
    P("כי אפס קילו ואפס ליברות הם אותו דבר: אין משקל בכלל. זה אפס אמיתי, ולכן משקל הוא סולם **מנה**.",
      do=show("z-c2"), hold=0.4),
], stage=w.stack(
    w.frame("z-t", w.pd.DataFrame({"לועזי": [G1, G2], "עברי": [H1, H2]}), hidden=True, index=False, size=40, cw=200),
    w.big("z-h", f"{H2} − {H1} = {H2 - H1}  ·  {G2} − {G1} = {G2 - G1}", size=34),
    w.big("z-r", f"{G2} / {G1} = 2   ·   {H2} / {H1} ≈ {H2 / H1:.2f}", size=34),
    w.big("z-w", f"{KG[0]} kg / {KG[1]} kg = 2", size=36),
    w.big("z-lb", f"{LB[0]} lb / {LB[1]} lb ≈ 2", size=36), gap=22),
   panel=st.card("z-c1", "rule", "🔑 רווח: ההפרשים שומרים על משמעות, היחסים לא")
         + st.card("z-c2", "rule", "🔑 מנה: 0 פירושו ״אין בכלל״, ולכן ״פי 2״ הגיוני"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: מהו ההבדל העיקרי בין סולם סדר לסולם רווח?"),
    P("נחזור לסולם: הדבר שסולם רווח מוסיף מעל סדר הוא **מרווחים שווים**.", do=show("x-1")),
    P("בשנים, כל שנה היא אותו מרווח. במידות חולצה, אין שום הבטחה כזו.", do=show("q-ok-0")),
    P("האפשרות שסולם סדר מתיר ממוצע וסולם רווח לא, הפוכה בדיוק: הממוצע מתחיל ברווח.",
      do=show("q-x-1", "q-n-1")),
    P("מספרים שלמים מול ממשיים? זה לא קשור לסולם. מידת חולצה היא בכלל לא מספר.", do=show("q-x-2", "q-n-2")),
    P("ומספר ילדים הוא שלם, אבל יש לו אפס אמיתי, ולכן הוא אפילו בסולם מנה."),
    P("ו״אין הבדל משמעותי״ נופלת: בסולם סדר אסור ממוצע, ובסולם רווח מותר.", do=show("q-x-3", "q-n-3"), hold=0.3),
    P("וזו המלכודת: אל תבדקו אם הערכים מספרים. בדקו אם **המרווחים** ביניהם שווים.", do=show("x-t"), hold=0.5),
], stage=w.stack(w.ladder("lx", hidden=False), st.card("x-1", "rule", "🔑 סדר ← רווח: נוספים <b>מרווחים שווים</b>"),
                 st.card("x-t", "trap", "⚠️ מספרים שלמים או ממשיים לא קובעים את הסולם"), gap=18),
   panel=w.stem(Q["id"], "מהו ההבדל העיקרי בין סולם סדר (ordinal) וסולם רווח (interval)?")
         + st.options("q", OPTS, notes={1: "הפוך", 2: "לא קשור לסולם", 3: "יש הבדל"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ארבעה סולמות, וכל אחד יורש את החישובים של הקודם.", do=show("r-1")),
    P("שמי: רק שכיח. סדר: גם חציון.", do=show("r-2")),
    P("רווח: מרווחים שווים, ולכן גם ממוצע והפרשים. מנה: אפס אמיתי, ולכן גם יחסים.", do=show("r-3")),
    P("והמבחן: לא שואלים אם זה מספר, אלא מה המספר מודד. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=w.ladder("lr", hidden=False),
   panel=st.card("r-1", "rule", "🔑 כל סולם יורש את הקודם")
         + st.card("r-2", "rule", "🔑 שמי ← שכיח · סדר ← חציון")
         + st.card("r-3", "rule", "🔑 רווח ← ממוצע · מנה ← יחסים")
         + st.card("r-4", "trap", "⚠️ מספר חולצה הוא שם, לא כמות"))

SCENES = [title, idea, lad, nominal, zero, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("C01", "clean", "סולמות מדידה", SCENES, bank={"24B-B-Q19": 0})

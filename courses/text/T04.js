/* Text course · level 4 — match, search, findall, split, sub */
DS_LEVEL("text", {
  id: "T04", order: 4, icon: "🧰", title: "match, search, findall, split ו-sub",
  goal: "לדעת מה כל פונקציה של re מחזירה, ולחזות את הפלט שלה על טקסט נתון.",
  lesson: { html: `
<table>
<thead><tr><th>פונקציה</th><th>מה היא עושה ומה היא מחזירה</th></tr></thead>
<tbody>
<tr><td><code>re.match(p, s)</code></td><td>מחפשת התאמה <b>רק מתחילת</b> המחרוזת. מחזירה אובייקט התאמה או None</td></tr>
<tr><td><code>re.search(p, s)</code></td><td>מחפשת <b>בכל המחרוזת</b> ומחזירה את ההתאמה <b>הראשונה</b> בלבד</td></tr>
<tr><td><code>re.findall(p, s)</code></td><td>רשימה של <b>כל</b> ההתאמות (מחרוזות)</td></tr>
<tr><td><code>re.split(p, s)</code></td><td>רשימה של חלקי הטקסט שבין ההתאמות</td></tr>
<tr><td><code>re.sub(p, new, s)</code></td><td>מחרוזת חדשה שבה כל התאמה הוחלפה ב-new</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 ההבדל המרכזי בין match ל-search: match רק מההתחלה, search בכל מקום (26A-B-Q4). ו-<code>.group()</code> של אובייקט התאמה מחזיר את הטקסט שנתפס (P-61).</div>
<div class="lesson-ex">דוגמה: <code>re.sub(r"\\d+", "#", "a1b22c333")</code> מחליף כל רצף ספרות ב-# ומחזיר <code>'a#b#c#'</code>. ו-<code>re.split(r"[,;] ?", "a, b;c,d")</code> מחזיר <code>['a', 'b', 'c', 'd']</code>.</div>
<div class="lesson-trap">⚠️ כשיש התאמה בקצה של המחרוזת, split מחזיר מחרוזת ריקה בקצה: <code>re.split(r"\\W+", "Hello, hello.")</code> נותן <code>['Hello', 'hello', '']</code> (P-65).</div>
` },
  questions: [
    { id: "T04-Q1", question: "מה מחזירות הקריאות `re.match(\"b\", \"abc\")` ו-`re.search(\"b\", \"abc\")`?",
      options: ["match מחזירה None, ו-search מחזירה התאמה", "שתיהן מחזירות התאמה", "match מחזירה התאמה, ו-search מחזירה None", "שתיהן מחזירות None"], answer: 0,
      recap: "match = מתחילת המחרוזת בלבד",
      explanation: "המחרוזת abc מתחילה ב-a, ולכן match לא מוצאת את b. search מחפשת בכל המחרוזת ומוצאת את ה-b במקום 1." },
    { id: "T04-Q2", question: "מה הפלט של `re.split(r\"[,;] ?\", \"a, b;c,d\")`?",
      options: ["['a', 'b', 'c', 'd']", "['a,', 'b', 'c', 'd']", "['a', ' b', 'c', 'd']", "['a, b;c,d']"], answer: 0,
      recap: "split חותך בכל התאמה, וההתאמה עצמה נעלמת",
      explanation: "המפריד הוא פסיק או נקודה-פסיק ואחריהם רווח אופציונלי. בכל ארבעת המקרים (`, ` ו-`;` ו-`,`) ההפרדה מוחקת גם את הרווח, ולכן הפריטים נקיים." },
    { id: "T04-Q3", question: "מה הפלט של `re.sub(r\"\\d+\", \"#\", \"a1b22c333\")`?",
      options: ["a#b#c#", "a#b##c###", "a1b22c333", "#####"], answer: 0,
      recap: "sub מחליף כל התאמה (כל רצף ספרות) בתחליף אחד",
      explanation: "`\\d+` תופס רצף שלם של ספרות, ולכן `1`, `22` ו-`333` מוחלפים כל אחד ב-# אחד. הפלט `a#b##c###` היה מתקבל עם `\\d` בלי הפלוס, כלומר ספרה ספרה." },
    { id: "T04-Q4", question: "כמה איברים יש ברשימה `re.findall(r\"o\", \"foo boo\")`?",
      options: ["4", "2", "1", "7"], answer: 0,
      recap: "findall מחזירה את כל ההתאמות",
      explanation: "המחרוזת foo boo מכילה את האות o ארבע פעמים (שתיים ב-foo ושתיים ב-boo), ולכן ברשימה **4** איברים." },
    { id: "T04-Q5", question: "מה מחזיר `re.search(r\"\\d+\", \"a12b345\").group()`?",
      options: ["12", "345", "12345", "['12', '345']"], answer: 0,
      recap: "search מחזירה רק את ההתאמה הראשונה",
      explanation: "search עוצרת בהתאמה הראשונה משמאל, והיא `12`. כדי לקבל את שתי ההתאמות משתמשים ב-findall." },
  ],
});

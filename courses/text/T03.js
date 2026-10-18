/* Text course · level 3 — anchors, alternation and groups */
DS_LEVEL("text", {
  id: "T03", order: 3, icon: "⚓", title: "עוגנים, או וקבוצות",
  goal: "לדעת מה ^ ו-$ מחייבים, להשתמש ב-| ובסוגריים, ולקרוא תבנית של כתובת אימייל.",
  lesson: { html: `
<table>
<thead><tr><th>סימן</th><th>משמעות</th></tr></thead>
<tbody>
<tr><td><code>^</code></td><td>תחילת המחרוזת (מחוץ לסוגריים מרובעים)</td></tr>
<tr><td><code>$</code></td><td>סוף המחרוזת</td></tr>
<tr><td><code>a|b</code></td><td>או: a או b</td></tr>
<tr><td><code>(...)</code></td><td>קבוצה. מוציאים אותה עם <code>m.group(1)</code>, ו-findall עם קבוצות מחזיר את תוכן הקבוצות</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 תבנית שמתחילה ב-<code>^</code> ומסתיימת ב-<code>$</code> חייבת להתאים ל<b>כל</b> המחרוזת. כך בודקים תקינות של כתובת אימייל, למשל <code>^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$</code> (24A-A-Q4): שם, ואז @, ואז דומיין, נקודה אמיתית (<code>\\.</code>) וסיומת של אותיות.</div>
<div class="lesson-ex">דוגמה: <code>re.findall(r"(\\d+)-(\\d+)", "10-20 and 3-4")</code> מחזיר רשימת צמדים: <code>[('10', '20'), ('3', '4')]</code>, כי יש שתי קבוצות. ו-<code>re.search(r"(\\w+)@(\\w+)", "dan@site").group(2)</code> הוא <code>'site'</code>.</div>
<div class="lesson-trap">⚠️ נקודה רגילה (<code>.</code>) תופסת כל תו. כדי לתפוס נקודה אמיתית כותבים <code>\\.</code>. ו-<code>re.match</code> בודק רק מתחילת המחרוזת, כמו <code>^</code> מובנה (26A-B-Q4).</div>
` },
  questions: [
    { id: "T03-Q1", question: "איזו מהקריאות הבאות מחזירה התאמה (אובייקט שאינו None)?",
      options: ["re.search(r'cat$', 'concat')", "re.search(r'^cat', 'concat')", "re.match(r'cat', 'concat')", "re.search(r'^con$', 'concat')"], answer: 0,
      recap: "^ = תחילה, $ = סוף, match = תחילה",
      explanation: "המחרוזת concat מסתיימת ב-cat, ולכן `cat$` מתאים. `^cat` ו-`re.match('cat')` דורשים cat בתחילה, אבל המחרוזת מתחילה ב-con, ו-`^con$` דורש שכל המחרוזת תהיה con." },
    { id: "T03-Q2", question: "מה הפלט של `re.findall(r\"cat|dog\", \"cat dogs bird\")`?",
      options: ["['cat', 'dog']", "['cat', 'dogs']", "['cat dogs']", "['cat', 'dog', 'bird']"], answer: 0,
      recap: "| = או; תופס רק את מה שכתוב",
      explanation: "הביטוי תופס את המחרוזת cat או את dog. ב-dogs נתפס רק `dog` (ה-s אינה חלק מהתבנית), ו-bird אינה אחת מהאפשרויות." },
    { id: "T03-Q3", question: "מה הפלט של `re.findall(r\"(\\d+)-(\\d+)\", \"10-20 and 3-4\")`?",
      options: ["[('10', '20'), ('3', '4')]", "['10-20', '3-4']", "['10', '20', '3', '4']", "[('10-20',), ('3-4',)]"], answer: 0,
      recap: "findall עם כמה קבוצות ← רשימת צמדים",
      explanation: "כשיש שתי קבוצות בתבנית, findall מחזיר לכל התאמה **צמד** של תוכן הקבוצות. בלי קבוצות היה מוחזר הטקסט המלא `['10-20', '3-4']`." },
    { id: "T03-Q4", question: "מה מחזיר `re.search(r\"(\\w+)@(\\w+)\", \"mail dan@site now\").group(2)`?",
      options: ["site", "dan", "dan@site", "mail"], answer: 0,
      recap: "group(n) = תוכן הקבוצה ה-n; group(0) = כל ההתאמה",
      explanation: "הקבוצה השנייה היא מה שאחרי ה-@: **site**. הקבוצה הראשונה היא dan, וכל ההתאמה (group(0)) היא dan@site." },
    { id: "T03-Q5", question: "התבנית היא `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$`. איזו מחרוזת מתאימה לה במלואה?",
      options: ["dan.k@mail.co.il", "dan@mail", "@mail.com", "dan k@mail.com"], answer: 0,
      recap: "שם + @ + דומיין + נקודה + סיומת של 2 אותיות לפחות",
      explanation: "`dan.k@mail.co.il` מתאימה: שם עם נקודה, @, דומיין, ואז סיומת il. ב-`dan@mail` אין נקודה וסיומת, ב-`@mail.com` חסר השם, וב-`dan k@mail.com` יש רווח שאינו בתווים המותרים." },
  ],
});

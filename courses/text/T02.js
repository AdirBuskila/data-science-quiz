/* Text course · level 2 — quantifiers */
DS_LEVEL("text", {
  id: "T02", order: 2, icon: "🔁", title: "כמתים: כמה פעמים?",
  goal: "להשתמש ב-*, +, ?, {n,m} כדי לתפוס חזרות, ולחזות מה findall יחזיר.",
  lesson: { html: `
<p><b>כמת</b> (quantifier) בא אחרי תו או קבוצה ואומר <b>כמה פעמים</b> הוא חוזר:</p>
<table>
<thead><tr><th>כמת</th><th>משמעות</th></tr></thead>
<tbody>
<tr><td><code>*</code></td><td>0 פעמים או יותר</td></tr>
<tr><td><code>+</code></td><td>פעם אחת או יותר</td></tr>
<tr><td><code>?</code></td><td>0 או פעם אחת (אופציונלי)</td></tr>
<tr><td><code>{3}</code> · <code>{2,4}</code></td><td>בדיוק 3 · בין 2 ל-4</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 הכמת חל על <b>התו האחד שלפניו</b> בלבד: <code>ab+</code> הוא "a ואז b אחד או יותר", לא "ab חוזר". וכמתים <b>חמדנים</b>: הם תופסים כמה שיותר (24A-B-Q4, 25A-B-Q24).</div>
<div class="lesson-ex">דוגמה: <code>re.findall(r"\\b[A-Z][a-z]*\\b", "Dan met Eli in NYC")</code>. Dan ו-Eli מתחילות באות גדולה ואחריה אותיות קטנות. NYC לא נתפסת, כי אחרי N בא Y (גדולה), ולא מתקבל גבול מילה. התוצאה: <code>['Dan', 'Eli']</code>.</div>
<div class="lesson-trap">⚠️ <code>\\d{2,3}</code> על "4444" תופס "444" ונשאר "4" שלא מספיק לעוד התאמה. ו-<code>colou?r</code> תופס גם color וגם colour, כי ה-u אופציונלי.</div>
` },
  questions: [
    { id: "T02-Q1", question: "מה הפלט של `re.findall(r\"ab+\", \"ab abb a abbb\")`?",
      options: ["['ab', 'abb', 'abbb']", "['ab', 'ab', 'ab']", "['ab', 'abb', 'a', 'abbb']", "['abbb']"], answer: 0,
      recap: "b+ = b אחד או יותר, חמדן",
      explanation: "`ab+` דורש a ואחריו לפחות b אחד, וחמדן: תופס את כל ה-b-ים. לכן `ab`, `abb`, `abbb`. ה-a הבודד אין אחריו b ולכן לא נתפס." },
    { id: "T02-Q2", question: "מה הפלט של `re.findall(r\"\\d{2,3}\", \"1 22 333 4444\")`?",
      options: ["['22', '333', '444']", "['22', '333', '4444']", "['22', '333', '444', '4']", "['1', '22', '333']"], answer: 0,
      recap: "{2,3} חמדן: עד 3 ספרות, ובשארית צריך לפחות 2",
      explanation: "`1` בודדת לא מספיקה. `22` ו-`333` נתפסים במלואם. בתוך `4444` נתפסות 3 ספרות (חמדנות עד 3), והספרה הרביעית לבדה קצרה מדי. לכן `['22', '333', '444']`." },
    { id: "T02-Q3", question: "איזה ביטוי מתאים במלואו גם ל-color וגם ל-colour, אבל לא ל-colouur?",
      options: ["colou?r", "colou*r", "colo+r", "color|colouur"], answer: 0,
      recap: "? = אופציונלי: 0 או פעם אחת",
      explanation: "`colou?r` מאפשר u אחד או אף u: color ו-colour, אבל לא שני u. הביטוי `colou*r` מתאים גם ל-colouur, `colo+r` לא מתאים ל-colour בכלל (אחרי colo בא u), ו-`color|colouur` אינו מתאים ל-colour." },
    { id: "T02-Q4", question: "מה הפלט של `re.findall(r\"\\b[A-Z][a-z]*\\b\", \"Dan met Eli in NYC\")`?",
      options: ["['Dan', 'Eli']", "['Dan', 'Eli', 'NYC']", "['Dan', 'met', 'Eli', 'in']", "['D', 'E', 'N']"], answer: 0,
      recap: "אות גדולה + קטנות*, בגבולות מילה",
      explanation: "המילים Dan ו-Eli מתחילות באות גדולה ואחריה רק קטנות. NYC אינה נתפסת, כי אחרי ה-N אין גבול מילה (בא Y). המילים met ו-in מתחילות באות קטנה." },
    { id: "T02-Q5", question: "מה הפלט של `re.findall(r\"\\w+@\\w+\\.com\", \"a@b.com, x_y@site.com, bad@site.org\")`?",
      options: ["['a@b.com', 'x_y@site.com']", "['a@b.com', 'x_y@site.com', 'bad@site.org']", "['a@b.com']", "[]"], answer: 0,
      recap: "\\w+ תופס אותיות, ספרות וקו תחתון",
      explanation: "`\\w` כולל קו תחתון, ולכן `x_y` מתאים לחלק שלפני ה-@. הסיומת חייבת להיות `.com` בדיוק, ולכן `bad@site.org` לא נתפס." },
  ],
});

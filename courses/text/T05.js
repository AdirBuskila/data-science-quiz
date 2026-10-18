/* Text course · level 5 — greedy vs lazy, groups */
DS_LEVEL("text", {
  id: "T05", order: 5, icon: "🐢", title: "חמדן מול עצלן, וקבוצות",
  goal: "להבין מה ? משנה אחרי * או +, ולהוציא קבוצות מתוך התאמה.",
  lesson: { html: `
<p>כמתים כמו <code>*</code> ו-<code>+</code> הם <b>חמדנים</b> (greedy): הם תופסים כמה שיותר טקסט ורק אחר כך מוותרים. אם מוסיפים <code>?</code> אחריהם הם נהיים <b>עצלנים</b> (lazy): תופסים כמה שפחות (26A-B-Q9).</p>
<div class="lesson-rule">🔑 חמדן: <code>.+</code> · עצלן: <code>.+?</code>. על הטקסט <code>&lt;a&gt;&lt;b&gt;</code> התבנית החמדנית <code>&lt;.+&gt;</code> תופסת הכול, <code>&lt;a&gt;&lt;b&gt;</code>, והעצלנית <code>&lt;.+?&gt;</code> רק <code>&lt;a&gt;</code>.</div>
<div class="lesson-ex">דוגמה: על "xaabbby" התבנית <code>a.*b</code> תופסת <code>aabbb</code> (עד ה-b האחרון), ואילו <code>a.*?b</code> תופסת <code>aab</code> (עד ה-b הראשון שאפשר).</div>
<p><b>קבוצות:</b> אחרי <code>m = re.search(r"(\\w+) (\\w+)", "A new day")</code> מתקבל: <code>m.group(0)</code> = כל ההתאמה (<code>'A new'</code>), <code>m.group(1)</code> = <code>'A'</code>, <code>m.group(2)</code> = <code>'new'</code>. קבוצה שלא תפסה כלום מחזירה מחרוזת ריקה (P-66).</p>
<div class="lesson-trap">⚠️ <code>?</code> אחרי כמת הופך אותו לעצלן, אבל <code>?</code> אחרי תו רגיל פירושו "אופציונלי". המשמעות תלויה במה שלפניו.</div>
` },
  questions: [
    { id: "T05-Q1", question: "מה מחזיר `re.search(r\"<.+>\", \"<a><b>\").group()`?",
      options: ["<a><b>", "<a>", "<b>", "a><b"], answer: 0,
      recap: "חמדן תופס עד הסוף האפשרי האחרון",
      explanation: "`.+` חמדן, ולכן הוא תופס כמה שיותר ואז חוזר אחורה עד ה-`>` האחרון בטקסט. התוצאה היא כל המחרוזת **`<a><b>`**." },
    { id: "T05-Q2", question: "מה מחזיר `re.search(r\"<.+?>\", \"<a><b>\").group()`?",
      options: ["<a>", "<a><b>", "<b>", "a"], answer: 0,
      recap: "עצלן תופס כמה שפחות",
      explanation: "`.+?` עצלן: הוא עוצר ב-`>` הראשון שאפשר, ולכן ההתאמה היא `<a>`. זו ההתאמה הראשונה משמאל." },
    { id: "T05-Q3", question: "מה מחזיר `re.search(r\"a.*?b\", \"xaabbby\").group()`?",
      options: ["aab", "aabbb", "ab", "aabb"], answer: 0,
      recap: "עצלן: עד ה-b הראשון שאפשר",
      explanation: "ההתאמה מתחילה ב-a הראשון, והעצלן `.*?` תופס כמה שפחות עד b: זה `a` נוסף, ואז `b`. התוצאה **aab**. הגרסה החמדנית `a.*b` הייתה נותנת `aabbb`." },
    { id: "T05-Q4", question: "מה מחזיר `re.search(r\"(\\w+) (\\w+)\", \"A new day\").group(2)`?",
      options: ["new", "A", "day", "A new"], answer: 0,
      recap: "group(2) = הקבוצה השנייה",
      explanation: "התבנית תופסת שתי מילים רצופות מהתחלה: `A` ו-`new`. הקבוצה השנייה היא **new**, וההתאמה כולה (group(0)) היא `A new`." },
    { id: "T05-Q5", question: "מה אורך המחרוזת ש-`re.search(r\"a.*?a\", \"a1a2a\").group()` מחזיר?",
      options: ["3", "5", "2", "1"], answer: 0,
      recap: "עצלן: עד ה-a הבא",
      explanation: "העצלן עוצר ב-a הראשון שבא אחרי הראשון: ההתאמה היא `a1a`, באורך **3**. החמדן `a.*a` היה תופס `a1a2a`, באורך 5." },
  ],
});

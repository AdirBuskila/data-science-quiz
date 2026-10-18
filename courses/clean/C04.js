/* Cleaning course · level 4 — duplicates */
DS_LEVEL("clean", {
  id: "C04", order: 4, icon: "👯", title: "שורות כפולות",
  goal: "להבין מה duplicated מחזיר, לספור כפילויות, ולהשתמש ב-drop_duplicates עם keep ו-subset.",
  lesson: { html: `
<p>שורה כפולה (duplicate) היא שורה זהה לשורה שכבר הופיעה קודם. ב-pandas:</p>
<ul>
<li><code>df.duplicated()</code> מחזיר <b>וקטור</b> של True / False, באורך מספר <b>השורות</b> (P-43). True בשורה אומר: "שורה זהה לאחת מהשורות הקודמות" (26A-B-Q7).</li>
<li><code>df.duplicated().sum()</code> סופר כמה שורות כפולות יש.</li>
<li><code>df.drop_duplicates()</code> מוחק אותן. כברירת מחדל משאיר את ההופעה <b>הראשונה</b> (<code>keep='first'</code>). עם <code>keep='last'</code> משאיר את <b>האחרונה</b> ומוחק את השאר (P-46).</li>
<li><code>subset=['name']</code> משווה רק לפי העמודות הנבחרות.</li>
</ul>
<div class="lesson-rule">🔑 בעמודה בלי ערכים חסרים: <b>מספר הערכים הייחודיים + מספר הכפילויות = מספר השורות</b> (P-22).</div>
<div class="lesson-ex">דוגמה: 6 שורות שבהן השורה (Dan, 25) מופיעה 3 פעמים. duplicated() נותן False בהופעה הראשונה ו-True בשתי האחרות. אם שאר השורות ייחודיות, drop_duplicates() משאיר 4 שורות.</div>
<div class="lesson-trap">⚠️ <code>duplicated()</code> לא מחזיר מספר, אלא וקטור. כדי לקבל מספר מוסיפים <code>.sum()</code>. ומחיקה לפי subset יכולה למחוק שורות ששונות בעמודות האחרות.</div>
` },
  questions: [
    { id: "C04-Q1", question: "בטבלה שלמטה מריצים `df.duplicated().sum()`. מה התוצאה?",
      table: { head: ["name", "age"], rows: [["Dan", "25"], ["Eli", "30"], ["Dan", "25"], ["Noa", "22"], ["Eli", "30"], ["Dan", "25"]] },
      options: ["3", "2", "6", "4"], answer: 0,
      recap: "True בכל שורה שזהה לשורה קודמת",
      explanation: "ההופעות הראשונות של (Dan, 25), (Eli, 30) ו-(Noa, 22) הן False. שורות 2, 4 ו-5 זהות לקודמות, ולכן True: סה״כ **3**. הערך 2 היה מתקבל אילו ספרנו רק את הערכים הכפולים (Dan ו-Eli) ולא את הכפילויות." },
    { id: "C04-Q2", question: "בטבלה שלמטה מריצים `df.drop_duplicates()`. כמה שורות יישארו?",
      table: { head: ["name", "age"], rows: [["Dan", "25"], ["Eli", "30"], ["Dan", "25"], ["Noa", "22"], ["Eli", "30"], ["Dan", "25"]] },
      options: ["3", "6", "4", "2"], answer: 0,
      recap: "נשארת הופעה אחת מכל שורה ייחודית",
      explanation: "יש שלוש שורות ייחודיות: (Dan, 25), (Eli, 30) ו-(Noa, 22). נשארות **3** שורות. 6 הוא המצב לפני המחיקה." },
    { id: "C04-Q3", question: "בטבלה שלמטה מריצים `df.drop_duplicates(keep='last')`. אילו אינדקסים יישארו?",
      table: { head: ["name", "age"], rows: [["Dan", "25"], ["Eli", "30"], ["Dan", "25"], ["Noa", "22"], ["Eli", "30"], ["Dan", "25"]] },
      options: ["3, 4 ו-5", "0, 1 ו-3", "0, 1 ו-2", "2, 4 ו-5"], answer: 0,
      recap: "keep='last' משאיר את ההופעה האחרונה",
      explanation: "ההופעה האחרונה של Dan היא באינדקס 5, של Eli באינדקס 4 ושל Noa (היחיד) באינדקס 3: **3, 4 ו-5**. האינדקסים 0, 1 ו-3 היו נשארים עם ברירת המחדל keep='first'." },
    { id: "C04-Q4", question: "ב-Series s יש 10 ערכים: 5, 3, 5, 8, 3, 1, 5, 9, 2, 7 (בלי חסרים). כמה ערכי True יש ב-`s.duplicated()`?",
      options: ["3", "7", "4", "10"], answer: 0,
      recap: "ייחודיים + כפילויות = סך הערכים",
      explanation: "הערכים הייחודיים הם 5, 3, 8, 1, 9, 2, 7: **7** ערכים. לכן הכפילויות הן 10 − 7 = **3** (ההופעות השנייה והשלישית של 5, והשנייה של 3). הערך 7 הוא מספר הייחודיים ולא מספר ה-True." },
    { id: "C04-Q5", question: "בטבלה שלמטה מריצים `df.drop_duplicates(subset=['name'])`. כמה שורות יישארו?",
      table: { head: ["name", "city"], rows: [["Dan", "TLV"], ["Dan", "HFA"], ["Eli", "TLV"], ["Eli", "TLV"], ["Noa", "HFA"]] },
      options: ["3", "4", "5", "2"], answer: 0,
      recap: "subset: משווים רק לפי העמודות שנבחרו",
      explanation: "לפי העמודה name בלבד יש שלושה שמות שונים: Dan, Eli ו-Noa, ולכן נשארות **3** שורות. בלי subset נמחקת רק השורה הכפולה לגמרי (Eli, TLV) ונשארות 4." },
  ],
});

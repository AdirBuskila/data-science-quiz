/* Text course · level 7 — from text to numbers (Bag of Words) */
DS_LEVEL("text", {
  id: "T07", order: 7, icon: "🧮", title: "מטקסט למספרים: Bag of Words",
  goal: "להבין איך CountVectorizer הופך מסמכים לווקטורים, מה גודל המטריצה, ומה עושים stop words.",
  lesson: { html: `
<p>אלגוריתם למידה לא יכול לעבוד עם טקסט גולמי, ולכן ממירים אותו למספרים. השיטה הבסיסית היא <b>Bag of Words</b> (שק מילים): בונים אוצר מילים של כל המילים השונות, ולכל מסמך סופרים כמה פעמים כל מילה מופיעה בו. הכלי: <code>CountVectorizer</code> (25A-A-Q23), ו-vectorizer בכלל הוא אובייקט שמסייע להפוך מסמך טקסט לייצוג וקטורי (24A-A-Q14, 26B-A-Q12).</p>
<div class="lesson-rule">🔑 התוצאה היא מטריצה: <b>שורה לכל מסמך</b>, <b>עמודה לכל מילה</b> באוצר המילים (ממוינות לפי א"ב). הערך הוא כמה פעמים המילה מופיעה במסמך.</div>
<div class="lesson-ex">דוגמה: שני מסמכים "the cat sat" ו-"the cat the dog". אוצר המילים הממוין: cat, dog, sat, the. הווקטור של המסמך השני: [1, 1, 0, 2] (cat פעם אחת, dog פעם אחת, sat אפס, the פעמיים).</div>
<p><b>Stop words</b> הן מילים נפוצות מאוד שרגילים להסיר כי אינן תורמות, למשל the ו-and (25A-B-Q23, 26A-A-Q20). הסרתן מקטינה את אוצר המילים.</p>
<div class="lesson-trap">⚠️ Bag of Words <b>מתעלם מסדר</b> המילים. "dog bites man" ו-"man bites dog" מקבלים אותו וקטור בדיוק.</div>
` },
  questions: [
    { id: "T07-Q1", question: "מריצים CountVectorizer על שני המסמכים \"the cat sat\" ו-\"the cat the dog\". אוצר המילים הממוין הוא cat, dog, sat, the. מהו הווקטור של המסמך השני?",
      options: ["[1, 1, 0, 2]", "[1, 1, 1, 1]", "[1, 1, 0, 1]", "[0, 1, 0, 2]"], answer: 0,
      recap: "ווקטור = ספירת כל מילה באוצר המילים לפי הסדר",
      explanation: "במסמך \"the cat the dog\": cat פעם אחת, dog פעם אחת, sat אפס, ו-the פעמיים. בסדר האוצר: **[1, 1, 0, 2]**. [1, 1, 1, 1] מתעלם מכך ש-the חוזרת ומהעובדה ש-sat חסרה." },
    { id: "T07-Q2", question: "מסמכים: \"red fox\", \"blue fox\", \"red sky\". מהי הצורה (shape) של המטריצה ש-CountVectorizer מחזיר?",
      options: ["(3, 4)", "(4, 3)", "(3, 6)", "(3, 3)"], answer: 0,
      recap: "שורות = מסמכים · עמודות = מילים שונות",
      explanation: "יש 3 מסמכים ו-4 מילים שונות: blue, fox, red, sky. לכן (3, 4). (3, 6) סופר את כל המילים כולל חזרות, ו-(4, 3) הופך בין שורות לעמודות." },
    { id: "T07-Q3", question: "על המסמכים \"the cat sat\" ו-\"the cat the dog\" מוסיפים stop_words='english'. כמה מילים יהיו באוצר המילים?",
      options: ["3", "4", "2", "5"], answer: 0,
      recap: "stop words מוסרות מהאוצר",
      explanation: "המילה the נמצאת ברשימת ה-stop words האנגליות ונמחקת. נשארות cat, dog ו-sat: **3** מילים, במקום 4." },
    { id: "T07-Q4", question: "כמה פעמים מופיע the בווקטור של המסמך \"the cat the dog\" אם אוצר המילים הוא cat, dog, sat, the?",
      options: ["2", "1", "0", "4"], answer: 0,
      recap: "הערך בתא = מספר ההופעות במסמך",
      explanation: "המילה the מופיעה פעמיים במסמך, ולכן בעמודה של the הערך הוא **2**. הערך 4 הוא מספר המילים באוצר, לא מספר ההופעות." },
    { id: "T07-Q5", question: "מה נכון לגבי הווקטורים של \"dog bites man\" ו-\"man bites dog\" ב-Bag of Words?",
      options: ["הם זהים, כי הגישה מתעלמת מסדר המילים", "הם שונים, כי הסדר משפיע על הספירה", "הם זהים רק אם משמיטים את bites", "אי אפשר ליצור וקטור כשיש מילה שחוזרת"], answer: 0,
      recap: "Bag of Words מתעלם מסדר",
      explanation: "בשני המשפטים אותן שלוש מילים, כל אחת פעם אחת, ולכן הספירות זהות. הסדר לא נשמר. זה אחד החסרונות של Bag of Words." },
  ],
});

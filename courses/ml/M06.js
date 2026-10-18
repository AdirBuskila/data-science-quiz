/* ML course · level 6 — confusion matrix and metrics, cross validation */
DS_LEVEL("ml", {
  id: "M06", order: 6, icon: "🎲", title: "מטריצת בלבול, Precision, Recall ו-F1",
  goal: "לחשב דיוק, Precision, Recall ו-F1 ממטריצת בלבול, ולחשב גדלי fold ב-K-Fold.",
  lesson: { html: `
<p>במודל סיווג בינארי מסמנים מחלקה אחת כ"חיובית" (למשל חולה). מטריצת הבלבול סופרת ארבעה מצבים:</p>
<table>
<thead><tr><th></th><th>חזוי חיובי</th><th>חזוי שלילי</th></tr></thead>
<tbody>
<tr><td><b>באמת חיובי</b></td><td>TP (פגיעה)</td><td>FN (החמצה)</td></tr>
<tr><td><b>באמת שלילי</b></td><td>FP (אזעקת שווא)</td><td>TN (דחייה נכונה)</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <b>Precision</b> = TP ÷ (TP + FP) ← מכל מה שחזינו חיובי, כמה נכון (26A-A-Q13). <b>Recall</b> = TP ÷ (TP + FN) ← מכל החיוביים האמיתיים, כמה מצאנו (26A-B-Q16). <b>Accuracy</b> = (TP + TN) ÷ סך הכול. <b>F1</b> = 2·P·R ÷ (P + R) (25A-B-Q18).</div>
<div class="lesson-ex">דוגמה: TP = 30, FN = 10, FP = 10, TN = 50. Precision = 30 ÷ 40 = 0.75. Recall = 30 ÷ 40 = 0.75. Accuracy = 80 ÷ 100 = 0.8. F1 = 0.75.</div>
<p><b>K-Fold Cross Validation:</b> מחלקים את הנתונים ל-K חלקים (folds) שווים. בכל סבב fold אחד משמש לתיקוף, והשאר (K − 1 folds) לאימון. כל הנתונים משמשים לתיקוף פעם אחת (26A-A-Q14, 25A-B-Q16).</p>
<div class="lesson-trap">⚠️ מודל ש"מזהה בהצלחה 90 מתוך 100 חולים, אבל מסמן הרבה בריאים כחולים" הוא בעל <b>Recall גבוה</b> ו-Precision נמוך, כי FP גבוה.</div>
` },
  questions: [
    { id: "M06-Q1", question: "במטריצת בלבול: TP = 40, FN = 10, FP = 20, TN = 30. מהו ה-Precision, בעיגול לשתי ספרות?",
      options: ["0.67", "0.80", "0.70", "0.50"], answer: 0,
      recap: "Precision = TP ÷ (TP + FP)",
      explanation: "40 ÷ (40 + 20) = 40 ÷ 60 ≈ **0.67**. הערך 0.80 הוא ה-Recall (40 ÷ 50), והערך 0.70 הוא ה-Accuracy (70 ÷ 100)." },
    { id: "M06-Q2", question: "באותה מטריצה (TP = 40, FN = 10, FP = 20, TN = 30), מהו ה-Recall?",
      options: ["0.80", "0.67", "0.70", "0.40"], answer: 0,
      recap: "Recall = TP ÷ (TP + FN)",
      explanation: "40 ÷ (40 + 10) = 40 ÷ 50 = **0.80**. הערך 0.67 הוא ה-Precision שלה, והערך 0.70 הוא ה-Accuracy." },
    { id: "M06-Q3", question: "באותה מטריצה (TP = 40, FN = 10, FP = 20, TN = 30), מהו ה-Accuracy?",
      options: ["0.70", "0.80", "0.67", "0.40"], answer: 0,
      recap: "Accuracy = (TP + TN) ÷ הכול",
      explanation: "(40 + 30) ÷ 100 = **0.70**. הערכים 0.80 ו-0.67 הם ה-Recall וה-Precision." },
    { id: "M06-Q4", question: "מודל סיווג בעל Precision = 0.5 ו-Recall = 0.75. מהו ה-F1?",
      options: ["0.60", "0.625", "0.75", "0.50"], answer: 0,
      recap: "F1 = 2PR ÷ (P + R), ממוצע הרמוני",
      explanation: "F1 = 2 · 0.5 · 0.75 ÷ (0.5 + 0.75) = 0.75 ÷ 1.25 = **0.60**. הערך 0.625 הוא הממוצע החשבוני של P ו-R, וזה לא ה-F1." },
    { id: "M06-Q5", question: "מבצעים 5-Fold Cross Validation על 120 דוגמאות. כמה דוגמאות יש בכל אימון (בכל סבב)?",
      options: ["96", "24", "120", "5"], answer: 0,
      recap: "אימון = (K − 1) folds · תיקוף = fold אחד",
      explanation: "כל fold מכיל 120 ÷ 5 = 24 דוגמאות. בכל סבב fold אחד (24) מתקף, ו-4 האחרים, **96** דוגמאות, משמשים לאימון. הערך 24 הוא גודל התיקוף." },
  ],
});

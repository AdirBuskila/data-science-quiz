# "צריך עזרה?" plan: the four guided courses

Source: `questions.json` (280 questions, 11 sittings 2024 to 2026 plus 51 practice questions). Topics by size:
eda 77 (27%), cleaning 52, ml_python 50, acquisition 39, nlp 22, clustering 16, supervised 14, evaluation 10.
Every sitting carries 20 to 25 questions, and eda alone is 6 to 9 of them.

## Picking the hardest areas

"Hard" here means: many questions per sitting, and the question needs a calculation, a code trace or a fine
distinction rather than recall. Pure recall areas (acquisition: requests / BeautifulSoup / JSON / HTTP codes,
ml_python: pandas names, Python data structures) are left to the bank and the existing helper pages
(`json-master.html`, `scales-master.html`, `regex-master.html`).

| course | id | bank topics | why it is hard |
|---|---|---|---|
| 📐 סטטיסטיקה וגרפים | `eda` | eda | the biggest topic, with IQR / percentile / std calculations in every sitting (24A-A-Q8, 25A-A-Q2, 25-S-Q8, 26B-A-Q7), Pearson traps, histogram bins, chart choice |
| 🧹 ניקוי נתונים וסולמות | `clean` | cleaning | second largest; scales, missing-value strategy, pandas fillna / loc / get_dummies traces, outlier rules |
| 🔎 ביטויים רגולריים וטקסט | `text` | nlp | every regex question needs a mental run of the engine; match vs search, greedy vs lazy, split edge cases |
| 🤖 מודלים והערכה | `ml` | supervised, clustering, evaluation (+ the problem-type questions of ml_python) | problem-type classification, K-Means / DBSCAN / PCA behaviour, precision / recall / F1 calculations |

## Course shape

Each course is a ladder of 7 or 8 levels: a short Hebrew lesson (definitions, one recipe, one worked example,
one trap), 5 questions, and a last 🏆 boss made only of 6 real bank questions pulled by id. Pass mark 80%.
Soft unlock, progress per course in `localStorage` (`dsq_crs_<id>_v1`), separate from the bank stats.

| course | levels | original questions | boss (real) |
|---|---|---|---|
| eda | E01 center · E02 spread / std · E03 percentiles and IQR · E04 outliers · E05 histogram / box plot · E06 Pearson · E07 which chart · E08 boss | 35 | 6 |
| clean | C01 scales · C02 find missing · C03 fill missing · C04 duplicates · C05 encoding / binning · C06 outliers in code · C07 boss | 30 | 6 |
| text | T01 building blocks · T02 quantifiers · T03 anchors / groups · T04 match / search / findall / split / sub · T05 greedy vs lazy · T06 writing a pattern · T07 Bag of Words · T08 boss | 35 | 6 |
| ml | M01 problem type · M02 K-Means · M03 DBSCAN / hierarchical · M04 PCA · M05 train/test, KNN, R² · M06 confusion matrix, F1, K-Fold · M07 boss | 30 | 6 |

## Teach before you ask

Every concept a question needs is in that level's lesson or an earlier one. Lessons cite the bank ids they
teach (plain text; this app has no question peek).

## Verification

One Python script per course, `tools/verify/needhelp/<id>/check.py` (shared helpers in `common.py`). It loads the
real level files through `node tools/course_check.js --json <id>`, recomputes each answer, and fails unless the
keyed option satisfies the computed predicate and **no other option does**.

* numeric answers: numpy / pandas / scipy (course convention for quartiles: median of each half, n odd leaves the
  median out; it reproduces the bank keys of 24A-A-Q8 and 25A-A-Q2);
* code and regex options: the option text itself is evaluated (`eval` of the list / string / pattern, `findall`
  of each candidate pattern, `eval` of each pandas expression);
* ML: sklearn `KMeans`, `DBSCAN`, `PCA`, `KNeighborsClassifier`, `CountVectorizer`, `KFold`, metrics; scipy `linkage`;
* real bank questions in the bosses are re-solved too, not trusted;
* `rule` checks (scales, chart choice, problem type) compare against a rule table written in the script.

Run: `python tools/verify/needhelp/<id>/check.py` from the repo root (needs numpy, pandas, scipy, scikit-learn).

Known note: in `26A-B-Q24` the keyed option says dummies hold "only 0 and 1"; pandas 2.x returns booleans, which is
the same idea. No other option of that question is defensible.

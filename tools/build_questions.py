# -*- coding: utf-8 -*-
"""Merge all per-source JSON files into the final question dataset.

Inputs : tools/raw/<EXAM>.json  (9 exams) + tools/raw/practice-A.json, practice-B.json
Outputs: ../questions.js  (window.QUESTIONS = [...])  -- loaded by the app
         ../questions.json (same data, for reuse)
         build_report.md   (counts, exclusions, dedup)

Rules:
- Exclude questions flagged hasImage, with a blank option, <2 options, or bad correctIndex.
- De-duplicate by normalized (question + option-set); keep the best copy
  (official > derived, then exam > practice, then earlier year).
"""
import json, re, pathlib, collections

TOOLS = pathlib.Path(__file__).parent
RAW = TOOLS / "raw"
OUT = TOOLS.parent

EXAM_CODES = ["24A-A","24A-B","24B-A","24B-B","25-S","25A-A","25A-B","26A-A","26A-B"]
PRACTICE_FILES = ["practice-A.json","practice-B.json"]

TOPIC_LABEL = {
    "acquisition":"הרכשת נתונים",
    "cleaning":"ניקוי נתונים",
    "eda":"ויזואליזציה ו-EDA",
    "nlp":"ניתוח טקסט (NLP)",
    "supervised":"למידה מונחית",
    "evaluation":"הערכת מודל",
    "clustering":"אשכול",
    "ml_python":"מושגי ML ופייתון",
}
EXAM_LABEL = {
    "24A-A":"2024 סמסטר א׳ מועד א׳","24A-B":"2024 סמסטר א׳ מועד ב׳",
    "24B-A":"2024 סמסטר ב׳ מועד א׳","24B-B":"2024 סמסטר ב׳ מועד ב׳",
    "25-S":"2025 מבחן לדוגמה","25A-A":"2025 סמסטר א׳ מועד א׳","25A-B":"2025 סמסטר א׳ מועד ב׳",
    "26A-A":"2026 סמסטר א׳ מועד א׳","26A-B":"2026 סמסטר א׳ מועד ב׳",
}

def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()

def find_image(q):
    """Return a web path to a question's figure if a file has been added, else None.
    Convention: images/exams/<examCode>-Q<num>.<ext>  (e.g. images/exams/24A-A-Q9.png)."""
    code, num = q.get("examCode"), q.get("num")
    if not code or num is None: return None
    for ext in ("png","jpg","jpeg","PNG","JPG","JPEG"):
        if (OUT/"images"/"exams"/f"{code}-Q{num}.{ext}").exists():
            return f"images/exams/{code}-Q{num}.{ext}"
    return None

def has_code(q):
    return bool(str(q.get("code","")).strip())

def valid(q):
    opts = q.get("options", [])
    if len(opts) < 2: return False, "few-options"
    if any(not str(o).strip() for o in opts): return False, "blank-option"
    ci = q.get("correctIndex")
    if not isinstance(ci, int) or ci < 0 or ci >= len(opts): return False, "bad-correctIndex"
    if not str(q.get("question","")).strip(): return False, "empty-question"
    return True, None

def main():
    raw_items = []
    # exams
    for code in EXAM_CODES:
        data = json.loads((RAW / f"{code}.json").read_text(encoding="utf-8"))
        for q in data:
            q["source"]="exam"; q["examCode"]=code
            q["sourceLabel"]=EXAM_LABEL[code]
            q.setdefault("year", int("20"+code[:2]))
            q["id"]=f"{code}-Q{q.get('num')}"
            raw_items.append(q)
    # practice
    pidx=0
    for fn in PRACTICE_FILES:
        data = json.loads((RAW / fn).read_text(encoding="utf-8"))
        for q in data:
            pidx+=1
            q["source"]="practice"; q["examCode"]=None
            q["sourceLabel"]="תרגול הקורס" + (f" · {q['chapter']}" if q.get("chapter") else "")
            q["year"]=None
            q["id"]=f"P-{pidx}"
            raw_items.append(q)

    excl = collections.Counter()
    kept = []
    for q in raw_items:
        ok, why = valid(q)
        if not ok:
            excl[why]+=1; continue
        # A question flagged hasImage is only answerable once its figure (image file)
        # or transcribed code (code field) has been supplied; otherwise keep excluding it.
        if q.get("hasImage"):
            img = find_image(q)
            if not img and not has_code(q):
                excl["image-missing"]+=1; continue
            if img: q["image"]=img
            q["hasImage"]=False   # resolved: a figure/code is now attached, so it's answerable
        kept.append(q)

    # NOTE: we intentionally do NOT de-duplicate across exams. Each exam must keep its
    # full question set so "whole test" mode always shows all 20/25 questions, even when
    # a question also appears in another exam. We still count cross-exam duplicates for
    # the build report (the random/topic practice pool may show a repeat — accepted).
    seen = set()
    dup = 0
    for q in kept:
        key = norm(q["question"]) + " || " + "|".join(sorted(norm(o) for o in q["options"]))
        if key in seen: dup += 1
        else: seen.add(key)
    final = kept

    # finalize fields
    for q in final:
        q["topicLabel"]=TOPIC_LABEL.get(q["topic"], q["topic"])
        for k in ("num","chapter"):
            q.pop(k, None)
    # stable order: topic, then source, then id
    final.sort(key=lambda q:(q["topic"], q["source"], q["id"]))

    # emit
    payload = json.dumps(final, ensure_ascii=False, indent=1)
    (OUT/"questions.json").write_text(payload, encoding="utf-8")
    (OUT/"questions.js").write_text("window.QUESTIONS = "+payload+";\n", encoding="utf-8")

    # report
    by_topic=collections.Counter(q["topic"] for q in final)
    by_src=collections.Counter("official" if q["official"] else "derived" for q in final)
    by_origin=collections.Counter(q["source"] for q in final)
    lines=["# Build report — questions dataset","",
        f"- Raw items read: **{len(raw_items)}**",
        f"- Excluded: **{sum(excl.values())}**  ({dict(excl)})",
        f"- Cross-exam duplicates (kept, not merged): **{dup}**",
        f"- **Final questions: {len(final)}**","",
        "## By topic",""]
    for t,n in by_topic.most_common():
        lines.append(f"- {TOPIC_LABEL[t]} (`{t}`): {n}")
    lines += ["","## By origin",
        f"- exam: {by_origin['exam']}  ·  practice: {by_origin['practice']}",
        f"- official answer key: {by_src['official']}  ·  derived (unofficial): {by_src['derived']}",""]
    (TOOLS/"build_report.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

    print(f"final={len(final)} excluded={sum(excl.values())} {dict(excl)} dup_kept={dup}")
    print("by_topic:", dict(by_topic))
    print("by_origin:", dict(by_origin), "by_key:", dict(by_src))

if __name__=="__main__":
    main()

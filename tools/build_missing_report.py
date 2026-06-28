# -*- coding: utf-8 -*-
"""Generate ../missing-questions.html — which exam is missing which question.

A question is "missing" from its exam if it appears in tools/raw/<EXAM>.json but
NOT in the built questions.json (e.g. flagged hasImage with no figure attached, or
blank/too-few options). Output is a static RTL page grouped by exam.
"""
import json, os, pathlib, html

TOOLS = pathlib.Path(__file__).parent
RAW = TOOLS / "raw"
OUT = TOOLS.parent

EXAM_EXPECT = {
    "24A-A": 20, "24A-B": 20, "24B-A": 20, "24B-B": 20,
    "25-S": 24, "25A-A": 25, "25A-B": 25, "26A-A": 25, "26A-B": 25, "26B-A": 25,
}
EXAM_LABEL = {
    "24A-A": "2024 סמסטר א׳ מועד א׳", "24A-B": "2024 סמסטר א׳ מועד ב׳",
    "24B-A": "2024 סמסטר ב׳ מועד א׳", "24B-B": "2024 סמסטר ב׳ מועד ב׳",
    "25-S": "2025 מבחן לדוגמה", "25A-A": "2025 סמסטר א׳ מועד א׳",
    "25A-B": "2025 סמסטר א׳ מועד ב׳", "26A-A": "2026 סמסטר א׳ מועד א׳",
    "26A-B": "2026 סמסטר א׳ מועד ב׳", "26B-A": "2026 סמסטר ב׳ מועד א׳",
}


def img_exists(code, num):
    for ext in ("png", "jpg", "jpeg", "PNG", "JPG", "JPEG"):
        if (OUT / "images" / "exams" / f"{code}-Q{num}.{ext}").exists():
            return True
    return False


def reason(q, code):
    opts = q.get("options", [])
    if len(opts) < 2 or any(not str(o).strip() for o in opts):
        return "אפשרויות חסרות / פחות מ-2 אפשרויות"
    if q.get("hasImage") and not img_exists(code, q["num"]) and not str(q.get("code", "")).strip():
        return f"חסרה תמונה — נדרש קובץ images/exams/{code}-Q{q['num']}.png"
    return "לא נכלל בבנייה"


def main():
    final = json.loads((OUT / "questions.json").read_text(encoding="utf-8"))
    kept = {q["id"] for q in final}

    blocks, total_missing, incomplete = [], 0, 0
    for code in EXAM_EXPECT:
        data = json.loads((RAW / f"{code}.json").read_text(encoding="utf-8"))
        missing = [q for q in data if f"{code}-Q{q['num']}" not in kept]
        have = EXAM_EXPECT[code] - len(missing)
        if not missing:
            continue
        incomplete += 1
        total_missing += len(missing)
        rows = []
        for q in sorted(missing, key=lambda x: x["num"]):
            qt = html.escape(str(q.get("question", "")).strip() or "(אין טקסט שאלה)")
            rows.append(
                f'<div class=q><div><span class=id>{code}-Q{q["num"]}</span>'
                f'<span class=topic>{html.escape(str(q.get("topic","")))}</span></div>'
                f'<div class=qt>{qt}</div>'
                f'<div class=why>{html.escape(reason(q, code))}</div></div>'
            )
        blocks.append(
            f'<section class=exam><h2>{code} — {html.escape(EXAM_LABEL[code])} '
            f'<span class=count>{have}/{EXAM_EXPECT[code]} · חסרות {len(missing)}</span></h2>'
            + "".join(rows) + "</section>"
        )

    head = (
        "<!DOCTYPE html><html lang=he dir=rtl><head><meta charset=utf-8>"
        "<title>מבחנים חסרים — אילו שאלות חסרות</title><style>"
        "body{font-family:Segoe UI,Arial,sans-serif;background:#f4f5f7;color:#1a1a1a;margin:0;padding:24px;}"
        "h1{font-size:22px;} .sum{color:#555;margin:0 0 20px;}"
        ".exam{max-width:900px;margin:0 0 26px;}"
        ".exam h2{font-size:17px;background:#3b5bdb;color:#fff;padding:8px 14px;border-radius:10px;display:flex;justify-content:space-between;align-items:center;}"
        ".count{font-size:13px;font-weight:400;opacity:.9;}"
        ".q{background:#fff;border:1px solid #ddd;border-right:4px solid #e8590c;border-radius:10px;padding:12px 14px;margin:10px 0;box-shadow:0 1px 3px rgba(0,0,0,.06);}"
        ".id{font-weight:700;color:#3b5bdb;} .topic{color:#888;font-size:13px;margin-right:8px;}"
        ".qt{margin:6px 0;font-size:15px;line-height:1.5;} .why{color:#c92a2a;font-size:13px;font-weight:600;}"
        "</style></head><body>"
    )
    summary = (
        f"<h1>מבחנים חסרים — אילו שאלות חסרות</h1>"
        f"<p class=sum>{incomplete} מבחנים לא שלמים · {total_missing} שאלות חסרות בסך הכל. "
        f"שאלה תופיע במבחן ברגע שהקובץ images/exams/&lt;מבחן&gt;-Q&lt;מספר&gt;.png יתווסף ותורץ הבנייה.</p>"
    )
    (OUT / "missing-questions.html").write_text(
        head + summary + "".join(blocks) + "</body></html>", encoding="utf-8"
    )
    print(f"wrote missing-questions.html — {incomplete} incomplete exams, {total_missing} missing questions")


if __name__ == "__main__":
    main()

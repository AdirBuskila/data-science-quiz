# -*- coding: utf-8 -*-
"""Extract raw text from the Data-Science exam PDFs to UTF-8 files in tools/raw/.

Hebrew PDFs are finicky: pdfplumber and PyMuPDF (fitz) can each mangle RTL text
differently. We dump BOTH engines per PDF so we can compare and pick the cleaner
one. English tokens, digits and the option letters (א/ב/ג/ד) are the anchors we
rely on regardless of Hebrew quality.
"""
import sys, pathlib
import pdfplumber
import fitz  # PyMuPDF

EXAM_DIR = pathlib.Path(r"C:\Users\Adir\Desktop\BSC\שנה ב\סמסטר ב\מבוא למדעי הנתונים\מבחנים")
RAW = pathlib.Path(__file__).parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)

# (output-stem, relative pdf path) — skip the UUID duplicate copies.
PDFS = [
    ("25-S",  r"2025\מבחן לדוגמה סמסטר א 2025.pdf"),
    ("25A-A", r"2025\סמסטר א מועד א 5.2.25.pdf"),
    ("25A-B", r"2025\סמסטר א מועד ב 5.3.25.pdf"),
    ("26A-A", r"2026\סמסטר א מועד א.pdf"),
    ("26A-B", r"2026\מועד ב תשפו סמסטר א.pdf"),
]


def via_pdfplumber(path):
    out = []
    with pdfplumber.open(path) as doc:
        for i, page in enumerate(doc.pages, 1):
            out.append(f"\n----PAGE {i}----\n")
            out.append(page.extract_text() or "")
    return "".join(out)


def via_fitz(path):
    out = []
    doc = fitz.open(path)
    for i, page in enumerate(doc, 1):
        out.append(f"\n----PAGE {i}----\n")
        out.append(page.get_text("text"))
    doc.close()
    return "".join(out)


def main():
    for stem, rel in PDFS:
        pdf = EXAM_DIR / rel
        if not pdf.exists():
            print(f"MISSING: {pdf}")
            continue
        for engine, fn in (("plumber", via_pdfplumber), ("fitz", via_fitz)):
            try:
                txt = fn(str(pdf))
            except Exception as e:
                print(f"{stem} [{engine}] ERROR: {e}")
                continue
            dest = RAW / f"{stem}.{engine}.txt"
            dest.write_text(txt, encoding="utf-8")
            print(f"{stem} [{engine}] -> {dest.name}  ({len(txt)} chars)")


if __name__ == "__main__":
    main()

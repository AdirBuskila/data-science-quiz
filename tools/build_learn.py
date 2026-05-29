# -*- coding: utf-8 -*-
"""
build_learn.py — build the Learning-section data for the quiz site.

Reads the Hebrew course summary (markdown), splits it into sections
(intro + 13 chapters + cheat-sheet + principles), renders each to HTML,
appends a curated set of web-optimized images per section, and emits:

    learn.js     ->  window.LEARN = [{id, title, html}, ...]
    images/      ->  curated, downscaled images referenced by learn.js

This mirrors the questions.js pipeline: the site stays 100% static and
offline (no runtime markdown parser, no CDN). Run:

    python tools/build_learn.py
"""
import os, re, json, html, datetime
import markdown
from PIL import Image

HERE      = os.path.dirname(os.path.abspath(__file__))
ROOT      = os.path.dirname(HERE)
SUMMARY   = r"C:\Users\Adir\Desktop\Adir\busi-notes\Data-Science\course_summary.md"
SRC_IMG   = r"C:\Users\Adir\Desktop\scrape-course\out\images"
OUT_IMG   = os.path.join(ROOT, "images")
OUT_JS    = os.path.join(ROOT, "learn.js")

MAX_W   = 1400      # downscale anything wider than this
JPEG_Q  = 85
SIZE_BUDGET_KB = 700  # warn if an optimized image exceeds this

# ---- curated images: section-id -> [(source filename, Hebrew caption), ...] ----
# Hand-curated after viewing every candidate; near-duplicate taxonomy diagrams
# and navigation/forum screenshots were dropped.
CURATION = {
    "intro": [
        ("asset_block_10_steps.jpg", "חמשת שלבי העבודה של מדען הנתונים"),
    ],
    "ch2": [
        ("asset_block_http.PNG", "קודי תגובה נפוצים של HTTP"),
    ],
    "ch3": [
        ("asset_block_Crawling.jpg", "שלבי תהליך ה-Crawling"),
    ],
    "ch4": [
        ("asset_block_VarTypeInfo.png", "סוגי משתנים וסולמות מדידה"),
        ("asset_block_PFurmula.png", "נוסחת מקדם המתאם של פירסון (r)"),
    ],
    "ch6": [
        ("asset_block_info3.jpg", "ויזואליזציות חד-ממדיות נפוצות"),
        ("asset_block_info8.jpg", "ויזואליזציות רב-ממדיות: Pairplot, Heatmap ועוד"),
        ("asset_block_info7_1_.jpg", "צמצום ממדים בעזרת PCA"),
    ],
    "ch8": [
        ("asset_block_info13.jpg", "טקסונומיה: סוגי למידת מכונה"),
    ],
    "ch9": [
        ("asset_block_logi-info-2.jpg", "רגרסיה לוגיסטית — סקירה ומאפיינים"),
        ("asset_block_reggres_Sum.png", "רגרסיה ליניארית ונוסחת y = β₀ + β₁·x"),
    ],
    "ch10": [
        ("asset_block_info6.jpg", "מבנה עץ החלטה"),
        ("asset_block_info7.jpg", "בחירת מאפיין לפיצול בעץ החלטה"),
        ("asset_block_SumEx.jpg", "טבלת השוואת אלגוריתמי סיווג"),
    ],
    "ch11": [
        ("asset_block_linkage.jpg", "שיטות Linkage לחישוב מרחק בין אשכולות"),
        ("asset_block_Klas.jpg", "קלאסטרינג היררכי — גישת Bottom-up"),
        ("asset_block_k-means.png", "מיקום k-means במפת אלגוריתמי האשכול"),
    ],
    "ch12": [
        ("asset_block_MatrixToText.jpeg", "מטקסט למטריצה — שלבי העיבוד"),
        ("asset_block_regulatT.jpg", "תווי Regex — טבלת ייחוס"),
        ("asset_block_regulatU.jpg", "שימושים עיקריים בביטויים רגולריים"),
        ("asset_block_SumAdvA.jpeg", "Regex — Greedy, Flags ו-Grouping"),
    ],
}


def section_id(title):
    t = title.strip()
    m = re.match(r"^פרק\s+(\d+)", t)
    if m:
        return "ch" + m.group(1)
    if t.startswith("שלבי"):
        return "intro"
    if t.startswith("טבלת"):
        return "cheat"
    if t.startswith("עקרונות"):
        return "principles"
    # fallback slug
    return "sec-" + re.sub(r"\W+", "-", t)[:24]


def split_sections(md_text):
    """Return (page_title, [(id, title, body_md), ...])."""
    lines = md_text.splitlines()
    # page title = first H1
    page_title = "תרגול למדעי הנתונים"
    for ln in lines:
        if ln.startswith("# "):
            page_title = ln[2:].strip()
            break

    # preamble = text after H1, before first '## '
    sections = []
    cur_title, cur_buf, preamble = None, [], []
    seen_h1 = False
    for ln in lines:
        if ln.startswith("# ") and not ln.startswith("## "):
            seen_h1 = True
            continue
        if ln.startswith("## "):
            if cur_title is not None:
                sections.append((cur_title, "\n".join(cur_buf)))
            cur_title = ln[3:].strip()
            cur_buf = []
        elif cur_title is None:
            if seen_h1:
                preamble.append(ln)
        else:
            cur_buf.append(ln)
    if cur_title is not None:
        sections.append((cur_title, "\n".join(cur_buf)))

    # prepend preamble blurb to the first (intro) section
    preamble_md = "\n".join(preamble).strip()
    out = []
    for i, (title, body) in enumerate(sections):
        sid = section_id(title)
        body = body.strip().strip("-").strip()
        if i == 0 and preamble_md:
            body = preamble_md + "\n\n" + body
        out.append((sid, title, body))
    return page_title, out


def optimize_image(src_path, dst_path):
    """Resize+re-encode; returns final size in KB."""
    im = Image.open(src_path)
    if im.width > MAX_W:
        h = round(im.height * MAX_W / im.width)
        im = im.resize((MAX_W, h), Image.LANCZOS)
    ext = os.path.splitext(dst_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        if im.mode in ("RGBA", "P", "LA"):
            im = im.convert("RGB")
        im.save(dst_path, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    else:  # png
        im.save(dst_path, "PNG", optimize=True)
    return os.path.getsize(dst_path) / 1024.0


def figures_html(sid):
    items = CURATION.get(sid, [])
    if not items:
        return "", []
    figs, manifest = [], []
    for i, (src_name, caption) in enumerate(items, 1):
        src = os.path.join(SRC_IMG, src_name)
        if not os.path.exists(src):
            raise FileNotFoundError("missing source image: " + src)
        ext = os.path.splitext(src_name)[1].lower()
        ext = ".jpg" if ext in (".jpeg", ".jpg") else ext
        out_name = f"{sid}_{i}{ext}"
        kb = optimize_image(src, os.path.join(OUT_IMG, out_name))
        manifest.append((out_name, kb, caption))
        cap = html.escape(caption)
        figs.append(
            f'<figure class="learn-fig">'
            f'<img loading="lazy" src="images/{out_name}" alt="{cap}">'
            f'<figcaption>{cap}</figcaption></figure>'
        )
    block = '<div class="learn-figs">' + "".join(figs) + "</div>"
    return block, manifest


def main():
    os.makedirs(OUT_IMG, exist_ok=True)
    with open(SUMMARY, encoding="utf-8") as f:
        md_text = f.read()

    page_title, sections = split_sections(md_text)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])

    learn, all_imgs, big = [], [], []
    for sid, title, body in sections:
        md.reset()
        body_html = md.convert(body)
        fig_html, manifest = figures_html(sid)
        for name, kb, cap in manifest:
            all_imgs.append((name, kb))
            if kb > SIZE_BUDGET_KB:
                big.append((name, kb))
        learn.append({"id": sid, "title": title, "html": body_html + fig_html})

    meta = {
        "generated": datetime.date.today().isoformat(),
        "chapters": len(learn),
        "images": len(all_imgs),
    }
    payload = (
        "/* AUTO-GENERATED by tools/build_learn.py — do not edit by hand. */\n"
        "window.LEARN = " + json.dumps(learn, ensure_ascii=False) + ";\n"
        "window.LEARN_META = " + json.dumps(meta, ensure_ascii=False) + ";\n"
    )
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(payload)

    total_kb = sum(kb for _, kb in all_imgs)
    print(f"page title : {page_title}")
    print(f"sections   : {len(learn)} -> {[s['id'] for s in learn]}")
    print(f"images     : {len(all_imgs)}  total {total_kb/1024:.2f} MB")
    if big:
        print("OVER BUDGET:", [(n, round(kb)) for n, kb in big])
    else:
        print(f"all images <= {SIZE_BUDGET_KB} KB  OK")
    print(f"wrote      : {OUT_JS}")
    print(f"images dir : {OUT_IMG}")


if __name__ == "__main__":
    main()

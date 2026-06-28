# -*- coding: utf-8 -*-
"""Validate the per-exam JSON files the structuring agents produced."""
import json, pathlib, collections

RAW = pathlib.Path(__file__).parent / "raw"
CODES = ["24A-A","24A-B","24B-A","24B-B","25-S","25A-A","25A-B","26A-A","26A-B","26B-A"]
TOPICS = {"acquisition","cleaning","eda","nlp","supervised","evaluation","clustering","ml_python"}

total=usable=0
by_topic=collections.Counter(); by_official=collections.Counter()
problems=[]
for code in CODES:
    p = RAW / f"{code}.json"
    if not p.exists():
        problems.append(f"{code}: FILE MISSING"); continue
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"{code}: JSON parse error: {e}"); continue
    nimg=0
    for q in data:
        total+=1
        if len(q.get("options",[]))!=4:
            problems.append(f"{code} Q{q.get('num')}: {len(q.get('options',[]))} options")
        ci=q.get("correctIndex")
        if not isinstance(ci,int) or ci<0 or ci>3:
            problems.append(f"{code} Q{q.get('num')}: bad correctIndex {ci}")
        if q.get("topic") not in TOPICS:
            problems.append(f"{code} Q{q.get('num')}: bad topic {q.get('topic')}")
        if not q.get("question","").strip():
            problems.append(f"{code} Q{q.get('num')}: empty question")
        if any(not str(o).strip() for o in q.get("options",[])):
            problems.append(f"{code} Q{q.get('num')}: blank option")
        if q.get("hasImage"): nimg+=1
        else:
            usable+=1; by_topic[q.get("topic")]+=1
            by_official["official" if q.get("official") else "derived"]+=1
    print(f"{code}: {len(data)} questions, {nimg} image-flagged, {len(data)-nimg} usable")

print(f"\nTOTAL: {total} raw, {usable} usable (non-image)")
print("by topic (usable):", dict(by_topic))
print("by source (usable):", dict(by_official))
print(f"\nPROBLEMS ({len(problems)}):")
for x in problems: print("  -", x)

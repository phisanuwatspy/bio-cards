#!/usr/bin/env python3
"""Validate drugs.json and build ../index.html (self-contained) from template.html.

Usage:  python3 build.py
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "drugs.json").read_text(encoding="utf-8"))

errors = []
ids = [d["id"] for d in data["drugs"]]
cats = {c["id"] for c in data["categories"]}
if len(ids) != len(set(ids)):
    errors.append("duplicate drug id")
idset = set(ids)
for d in data["drugs"]:
    for k in ("id", "name", "cat", "cls", "grp", "moa", "pk", "pearl"):
        if not d.get(k):
            errors.append(f"{d.get('id')}: missing {k}")
    if d["cat"] not in cats:
        errors.append(f"{d['id']}: unknown category {d['cat']}")

for field, tags in data["tags"].items():
    for tag, t in tags.items():
        yes, maybe = set(t["yes"]), set(t["maybe"])
        if not yes:
            errors.append(f"{field}/{tag}: no 'yes' drug")
        for x in yes | maybe:
            if x not in idset:
                errors.append(f"{field}/{tag}: unknown id {x}")
        both = yes & maybe
        if both:
            errors.append(f"{field}/{tag}: in both yes and maybe {sorted(both)}")

for field in ("adr", "use"):
    covered = {x for t in data["tags"][field].values() for x in t["yes"]}
    for i in ids:
        if i not in covered:
            errors.append(f"{i}: no '{field}' tag")

if errors:
    print("\n".join(errors))
    sys.exit(1)

tpl = (HERE / "template.html").read_text(encoding="utf-8")
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = tpl.replace("/*__DATA__*/null", blob)
(HERE.parent / "index.html").write_text(html, encoding="utf-8")
n_tags = sum(len(v) for v in data["tags"].values())
print(f"OK: {len(ids)} drugs, {n_tags} tags -> {HERE.parent / 'index.html'} ({len(html)//1024} KB)")

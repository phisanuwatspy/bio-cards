#!/usr/bin/env python3
"""Build the unified Bio Cards app (biology Slide 07–13 + drugs) into the repo root and the artifact copy."""
import json, re
from pathlib import Path
SRC = Path('/home/claude/src')
BIO = [("07", "#3F8C3A", "Cell Respiration", "การสลายสารอาหารไปใช้พลังงาน"),
       ("08", "#C27A12", "Nucleic Acid", "สารพันธุกรรม: โครงสร้างและหน้าที่"),
       ("09", "#B5651D", "Gene Expression", "การควบคุมยีน และความผิดปกติของโครโมโซม"),
       ("10", "#C2364B", "Gene Disorders", "ความผิดปกติระดับยีน และกฎของ Mendel"),
       ("11", "#2F6DB0", "Cell Cycle & Mitosis", "การแบ่งเซลล์ และการเสื่อมของเซลล์"),
       ("12", "#C2408A", "Meiosis", "ไมโอซิสและการสืบพันธุ์"),
       ("13", "#0E8A7B", "Microbial Diversity", "ความหลากหลายของจุลินทรีย์")]
BADGE = {"cv": "CV", "heme": "HEM", "endo": "END", "inf": "INF", "cns": "CNS", "pain": "PAIN", "gir": "GI"}

decks, items = [], []
pairs = json.load(open(SRC / 'pairs2.json', encoding='utf-8'))
for tid, c, en, th in BIO:
    decks.append({"id": tid, "g": "bio", "name": en, "sub": th, "c": c, "badge": tid, "short": "Slide " + tid})
    if tid == "13":
        rows = [(it, it['m'], it['n']) for it in json.load(open(SRC / 'data13.json', encoding='utf-8'))]
    else:
        tr = json.load(open(SRC / f'tricks{tid}.json', encoding='utf-8'))
        rows = [(it, m, n) for n, (it, m) in enumerate(zip(pairs[tid], tr)) if not re.search(r'Pedigree ชุด|ใน pedigree', it['q'])]
    deck_items = []
    for it, m, n in rows:
        deck_items.append({"i": f"{tid}-{n}", "d": tid, "s": it['s'], "q": it['q'], "a": it['a'], "x": list(it['x']), "e": it['e'], "m": m, "k": "t"})
    # every card needs 3 wrong options for the one-tap quiz
    for it in deck_items:
        if len(it['x']) >= 3: continue
        bad = lambda o: o == it['a'] or o in it['a'] or it['a'] in o or o in it['x']
        cand = [o['a'] for o in deck_items if o['s'] == it['s'] and o is not it] + [o['a'] for o in deck_items if o['s'] != it['s']]
        for o in cand:
            if len(it['x']) >= 3: break
            if not bad(o): it['x'].append(o)
    items += deck_items

INCLUDE_DRUGS = False
drug = json.load(open('/home/claude/bio-cards/drug-quiz/src/drugs.json', encoding='utf-8'))
for c in (drug['categories'] if INCLUDE_DRUGS else []):
    decks.append({"id": "d-" + c['id'], "g": "drug", "name": c['name'], "sub": c['th'], "c": c['color'], "badge": BADGE.get(c['id'], c['id'].upper()), "short": c['name']})
if INCLUDE_DRUGS: items += json.load(open(SRC / 'drug_items.json', encoding='utf-8'))

assert len({i['i'] for i in items}) == len(items)
assert all(len(i['x']) >= 3 for i in items), [i['i'] for i in items if len(i['x']) < 3]
data = {"decks": decks, "items": items, "drugCount": len(drug['drugs'])}
js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
t = (SRC / 'template6.html').read_text(encoding='utf-8').replace('/*DATA*/', js)

art = t.replace('if(g==="drug"){const a=', 'if(false){const a=').replace('<!--PWA-HEAD-->\n', '').replace('<!--PWA-SW-->\n', '')
Path('/home/claude/index.html').write_text(art, encoding='utf-8')
head = '''<meta name="theme-color" content="#F6F4F0">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Bio Cards">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
'''
sw = '<script>if("serviceWorker" in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){})})}</script>\n'
Path('/home/claude/pwa/index.html').write_text(t.replace('<!--PWA-HEAD-->\n', head).replace('<!--PWA-SW-->\n', sw), encoding='utf-8')
s = Path('/home/claude/pwa/sw.js').read_text()
Path('/home/claude/pwa/sw.js').write_text(re.sub(r'const VERSION = "biocards-v\d+";', 'const VERSION = "biocards-v8";', s))
from collections import Counter
print(len(items), "items", Counter(DECK['g'] for DECK in decks), len(art) // 1024, "KB")

# Build a fixed question bank from drug-quiz/src/drugs.json (stable ids for spaced repetition)
import json, random
R = random.Random(42)
D = json.load(open('/home/claude/bio-cards/drug-quiz/src/drugs.json', encoding='utf-8'))
drugs = D['drugs']; byId = {d['id']: d for d in drugs}; tags = D['tags']
cats = {c['id']: c for c in D['categories']}

def linked(f, t):
    return set(tags[f][t]['yes']) | set(tags[f][t]['maybe'])
def yes_tags(d, f):
    return [t for t, v in tags[f].items() if d['id'] in v['yes']]

def prefer_same(target, pool, catfn):
    same = [x for x in pool if catfn(x) == target['cat']]; other = [x for x in pool if catfn(x) != target['cat']]
    R.shuffle(same); R.shuffle(other)
    return same + other
def take_unique(lst, key, n, avoid):
    seen = set(avoid); out = []
    for x in lst:
        k = key(x)
        if k in seen: continue
        seen.add(k); out.append(x)
        if len(out) == n: break
    return out

SEC = {'cls': 'กลุ่มยา', 'moa': 'กลไกการออกฤทธิ์', 'stem': 'ชื่อยา (stem)', 'use': 'ข้อบ่งใช้', 'adr': 'ADR', 'ci': 'ข้อห้ามใช้ & DDI'}
items = []
def add(d, kind, k, q, a, x, e):
    if len(x) < 3: return
    items.append({'i': f"d-{d['id']}-{kind}{k}", 'd': 'd-' + d['cat'], 's': SEC[kind], 'q': q, 'a': a, 'x': x[:3], 'e': e,
                  'm': d['pearl'], 'k': 'p'})

def summary(d):
    return f"\u0001{d['name']}\u0002 · {d['cls']} — {d['moa']}"

for d in drugs:
    # class
    pool = [x for x in drugs if x['grp'] != d['grp']]
    xs = take_unique(prefer_same(d, pool, lambda x: x['cat']), lambda x: x['cls'], 3, [d['cls']])
    add(d, 'cls', '', f"{d['name']} จัดอยู่ในกลุ่มยาใด", d['cls'], [x['cls'] for x in xs], summary(d))
    # mechanism -> drug
    pool = [x for x in drugs if x['grp'] != d['grp']]
    xs = take_unique(prefer_same(d, pool, lambda x: x['cat']), lambda x: x['name'], 3, [d['name']])
    add(d, 'moa', '', f"ยาใดออกฤทธิ์โดย: {d['moa']}", d['name'], [x['name'] for x in xs], summary(d))
    # stem
    if d.get('stem'):
        pool = [x for x in drugs if x.get('stem') and x['grp'] != d['grp']]
        xs = take_unique(prefer_same(d, pool, lambda x: x['cat']), lambda x: x['stem']['m'], 3, [d['stem']['m']])
        s = d['stem']['s']; where = 'ลงท้ายด้วย' if s.startswith('-') else 'ขึ้นต้นด้วย'
        it_e = f"stem \u0001{s}\u0002 = {d['stem']['m']} เช่น {d['name']}"
        add(d, 'stem', '', f"ชื่อยาที่{where} {s} บ่งบอกว่าเป็นยากลุ่มใด", d['stem']['m'], [x['stem']['m'] for x in xs], it_e)
    # drug -> tag (use 2, adr 2, ci 1)
    for f, n, qt in (('use', 2, '{} ใช้รักษาภาวะใด'), ('adr', 2, 'อาการไม่พึงประสงค์ใดสัมพันธ์กับ {}'),
                     ('ci', 1, 'ข้อใดเป็นข้อห้ามใช้หรือปฏิกิริยาระหว่างยาที่สำคัญของ {}')):
        mine = yes_tags(d, f); R.shuffle(mine)
        others = [t for t in tags[f] if d['id'] not in linked(f, t)]
        for j, t in enumerate(mine[:n]):
            def tcat(tag):
                return d['cat'] if any(byId[i]['cat'] == d['cat'] for i in tags[f][tag]['yes']) else '_'
            same = [o for o in others if tcat(o) == d['cat']]; other = [o for o in others if tcat(o) != d['cat']]
            R.shuffle(same); R.shuffle(other)
            xs = take_unique(same + other, lambda o: o, 3, [t])
            lst = ', '.join(yes_tags(d, f))
            add(d, f, j, qt.format(d['name']), t, xs, f"{summary(d)}\n{SEC[f]}: {lst}")

# sanity
ids = [i['i'] for i in items]; assert len(ids) == len(set(ids))
for it in items:
    assert it['a'] not in it['x'] and len(set(it['x'])) == 3, it
json.dump(items, open('/home/claude/src/drug_items.json', 'w', encoding='utf-8'), ensure_ascii=False)
from collections import Counter
print(len(items), Counter(i['d'] for i in items), Counter(i['s'] for i in items))
print(max(len(i['q']) for i in items), max(len(i['a']) for i in items))

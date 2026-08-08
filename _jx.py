import io, json
p = r'C:\Users\navne\.claude\projects\F--NEET-PG\7f70972e-7f7a-41c2-9f48-027968bd8703\subagents\workflows\wf_51e30430-e16\journal.jsonl'
records = []
for ln in io.open(p, encoding='utf-8'):
    ln=ln.strip()
    if not ln: continue
    try: r=json.loads(ln)
    except: continue
    records.append(r)
# inspect types
from collections import Counter
print('record types:', Counter(r.get('type') for r in records))
# sample each type's keys
for t in ['result','error']:
    rr=[r for r in records if r.get('type')==t]
    print('--- type', t, 'count', len(rr))
    for r in rr[:2]:
        print(' keys', list(r.keys())[:8])
        print(' content head:', str(r)[:300])
# result-level schema
for r in records:
    if r.get('type')=='result':
        v=r.get('value') or r.get('result')
        print('value type', type(v), 'val head', str(v)[:200])
        break

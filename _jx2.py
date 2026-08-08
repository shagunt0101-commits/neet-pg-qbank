import io, json
p = r'C:\Users\navne\.claude\projects\F--NEET-PG\7f70972e-7f7a-41c2-9f48-027968bd8703\subagents\workflows\wf_51e30430-e16\journal.jsonl'
recs=[]
for ln in io.open(p,encoding='utf-8'):
    ln=ln.strip()
    if ln:
        try: recs.append(json.loads(ln))
        except: pass
res=[r for r in recs if r.get('type')=='result']
print('results', len(res))
# full question schema sample
q=res[0]['result']['questions'][0]
print(json.dumps({k:(v if not isinstance(v,(list,dict)) else (v[:2] if isinstance(v,list) else list(v)[:4])) for k,v in q.items()}, indent=1)[:600])
subs=[r['result']['subject'] for r in res]
from collections import Counter
print('subjs:', {k:v for k,v in Counter(subs).items()})
lens={r['result']['subject']: len(r['result']['questions']) for r in res}
print('lens:', lens)

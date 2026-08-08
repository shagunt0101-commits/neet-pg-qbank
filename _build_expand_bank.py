import io, json
p = r'C:\Users\navne\.claude\projects\F--NEET-PG\7f70972e-7f7a-41c2-9f48-027968bd8703\subagents\workflows\wf_51e30430-e16\journal.jsonl'
recs=[]
for ln in io.open(p,encoding='utf-8'):
    ln=ln.strip()
    if ln:
        try: recs.append(json.loads(ln))
        except: pass
res=[r['result'] for r in recs if r.get('type')=='result']
subs={}
for r in res:
    subs[r['subject']] = r['questions']
total=0
for s,qq in subs.items():
    total+=len(qq)
print('subjects', len(subs), 'total', total)
# dedupe within each subject by q
dupes=0
for s,qq in subs.items():
    seen=set()
    for q in qq:
        k=q.get('q','').strip().lower()
        if k in seen: dupes+=1
        seen.add(k)
print('in-subj dup stems:', dupes)
# validate keys
bad=0
for s,qq in subs.items():
    for q in qq:
        if not all(k in q for k in ('q','o','a','ex','e','y')) or len(q['o'])<2 or not isinstance(q['a'],int):
            bad+=1
print('missing-key items:', bad)
io.open('research/_expand_bank.json','w',encoding='utf-8').write(json.dumps(subs,ensure_ascii=False,indent=1))
print('wrote research/_expand_bank.json')

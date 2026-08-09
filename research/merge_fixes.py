# -*- coding: utf-8 -*-
"""Merge fixed_chunk_*.json from reconstructors, sanity-verify, write fixed_records.json."""
import io, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

recs = {}
for i in range(10):
    p = r'F:\NEET PG\research\fixed_chunk_%d.json' % i
    try:
        data = json.loads(io.open(p, 'r', encoding='utf-8').read())
    except FileNotFoundError:
        print('MISSING chunk', i); continue
    assert isinstance(data, list), p
    for r in data:
        assert 'qid' in r and 'q' in r and 'o' in r and 'a' in r, r
        recs[r['qid']] = r

orig = {q['qid']: q for q in json.loads(io.open(r'F:\NEET PG\research\after_qid_unique.json', 'r', encoding='utf-8').read())}
missing = set(orig) - set(recs)
extra = set(recs) - set(orig)
print('fixed:', len(recs), 'missing:', sorted(missing), 'extra:', sorted(extra))
assert not missing and not extra

MARK = re.compile(r'\(Q-\d+\)')
problems = []
for qid, r in sorted(recs.items()):
    o = orig[qid]
    stem = r['q']
    m = MARK.search(stem)
    if not m:
        problems.append('%s: marker lost' % qid); continue
    after = stem[m.end():].strip()
    if after:
        problems.append('%s: text after marker remains: %s' % (qid, after[:80]))
    if len(r['o']) != 4:
        problems.append('%s: %d options' % (qid, len(r['o'])))
    # answer sanity: changed answers need note
    if r['a'] != o['a']:
        print('ANSWER CHANGED %s: %s -> %s' % (qid, o['a'], r['a']))
    # option sanity: must start with same first 25 chars as original (or be repaired tail-join)
    for i, (new, old) in enumerate(zip(r['o'], o['o'])):
        if not new.startswith(old[:25]):
            problems.append('%s o[%d]: start changed: %r vs %r' % (qid, i, new[:60], old[:60]))

if problems:
    print('\n'.join(problems[:60]))
    print('TOTAL PROBLEMS:', len(problems))
else:
    io.open(r'F:\NEET PG\research\fixed_records.json', 'w', encoding='utf-8').write(json.dumps([recs[k] for k in sorted(recs)], ensure_ascii=False, indent=1))
    print('merged OK -> fixed_records.json')

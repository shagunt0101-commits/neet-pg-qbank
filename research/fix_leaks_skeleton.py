# -*- coding: utf-8 -*-
"""Rebuild core_btr.js from fixed records. Input: research/fixed_records.json
(array of full records with corrected 'q' and 'o' keys). Writes questions/core_btr.js
with identical key order/encoding; asserts count/parse roundtrip."""
import io, json, sys
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'F:\NEET PG\questions\core_btr.js'
FIX = r'F:\NEET PG\research\fixed_records.json'

d = io.open(SRC, 'r', encoding='utf-8').read()
s = d.find('['); e = d.rfind('];')
bank = json.loads(d[s:e+1])
fixes = json.loads(io.open(FIX, 'r', encoding='utf-8').read())
byid = {q['qid']: q for q in fixes}

n = 0
for q in bank:
    f = byid.get(q.get('qid'))
    if f is None:
        continue
    q['q'] = f['q']
    if 'o' in f:
        q['o'] = f['o']
    if 'a' in f:
        q['a'] = f['a']
    n += 1
assert n == len(fixes), 'applied %d, expected %d' % (n, len(fixes))

# rebuild: header up to '[' + serialized + '];' tail
head = d[:s]; tail = d[e+1:]
out = head + json.dumps(bank, ensure_ascii=False, separators=(',', ':')) + tail
# roundtrip check
s2 = out.find('['); e2 = out.rfind('];')
json.loads(out[s2:e2+1])
io.open(SRC, 'w', encoding='utf-8', newline='').write(out)
print('OK applied', n, 'core_btr.js', len(out), 'bytes (was', len(d), ')')

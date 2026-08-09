# -*- coding: utf-8 -*-
"""Fix stems that leak option/answer text. 3 unique fixes across 5 questions.
Byte-level string replace (no re-serialize) to keep 82MB core_btr.js intact.

cb3975/cb4252 (core_btr.js): strip duplicated option block from stem end.
cb5908  (core_btr.js): drop garbage option[0] (=stem text), shift answer.
q2266   (bank.js): strip leaked answer suffix from stem.
"""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')

def patch(path, subs):
    d = io.open(path, 'r', encoding='utf-8', errors='replace').read()
    for old, new, must in subs:
        n = d.count(old)
        assert n == must, (path, old[:60], n, must)
        d = d.replace(old, new)
    io.open(path, 'w', encoding='utf-8', newline='').write(d)
    print('patched', path)

OLD_BLOCK = 'management? A. Induction of labour with oxytocin B. Hospitalisation and expectant management C. Immediate LSCS D. Amniotomy'
patch(r'F:\NEET PG\questions\core_btr.js', [
    # cb3975, cb4252: identical stems
    (OLD_BLOCK, 'management?', 2),
    # cb5908: drop garbage option[0], shift a 1->0
    ('"o": ["Cardiac output can be determined using the following except?", "Coronary angiography", "Cardiac MRI", "Echocardiography"], "a": 1',
     '"o": ["Coronary angiography", "Cardiac MRI", "Echocardiography"], "a": 0', 1),
])

patch(r'F:\NEET PG\questions\bank.js', [
    ('cascade is Factor VIIa (activated Factor VII).', 'cascade:', 1),
])

# ---- verify ----
import json
def load(p):
    d = io.open(p, 'r', encoding='utf-8', errors='replace').read()
    s = d.find('['); e = d.rfind('];')
    return json.loads(d[s:e+1])

data = load(r'F:\NEET PG\questions\core_btr.js')
for q in data:
    if q.get('qid') in ('cb3975', 'cb4252', 'cb5908'):
        print(q['qid'], '| Q:', q['q'][:120])
        print('      O:', json.dumps(q['o'], ensure_ascii=False)[:160])
        print('      a:', q['a'])
data2 = load(r'F:\NEET PG\questions\bank.js')
for q in data2:
    if q.get('qid') == 'q2266':
        print('q2266 | Q:', q['q'])
        print('      a:', q['a'])

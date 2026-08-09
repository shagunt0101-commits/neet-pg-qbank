# -*- coding: utf-8 -*-
"""Sweep for text mixed in AFTER the (Q-xxxxx) PDF id marker in stems.
Stem should END with (Q-xxxxx). Anything after = leaked option/question text.
"""
import io, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

def load(p):
    d = io.open(p, 'r', encoding='utf-8', errors='replace').read()
    s = d.find('['); e = d.rfind('];')
    return json.loads(d[s:e+1])

MARK = re.compile(r'\(Q-\d+\)')
hits = []
for path in [r'F:\NEET PG\questions\core_btr.js', r'F:\NEET PG\questions\bank.js', r'F:\NEET PG\questions\test_2026.js']:
    for q in load(path):
        stem = q.get('q', '')
        m = MARK.search(stem)
        if m:
            after = stem[m.end():].strip()
            if after:
                hits.append((path.split('\\')[-1], q.get('qid'), after, stem[m.start():m.end()]))

print('TOTAL:', len(hits))
for p, qid, after, mark in hits:
    print(f'--- {p} {qid} | after ({len(after)} ch): {after[:200]}')
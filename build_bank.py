# -*- coding: utf-8 -*-
# One-shot bank builder: curated(227) + workflow-expand(714) + medink fill(Pathology/Ophthalmology).
import io, json, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
def R(p):
    return os.path.join(BASE, p)

old = json.loads(io.open(R('research/_base_clean.json'), encoding='utf-8').read())
for q in old:
    q.setdefault('src', 'curated')

subs = json.loads(io.open(R('research/_expand_bank.json'), encoding='utf-8').read())
exp = []
for subj, qq in subs.items():
    for q in qq:
        item = dict(q)
        item['s'] = subj
        item['src'] = 'expand'
        exp.append(item)

qs_all = json.loads(io.open(R('research/_parsed.json'), encoding='utf-8').read())
fill = [q for q in qs_all if q['subj'] in ('Ophthalmology', 'Pathology') and q['year'] in (2023, 2024)]
for q in fill:
    q['s'] = q.pop('subj')
    q['src'] = 'medink'

bank = old + exp + fill

out = []
out.append("// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.")
out.append("// Per-item src: curated (hand-picked PYQs), expand (workflow recall Qs), medink (user-provided PYQ PDF).")
out.append("// Personal offline practice only — not for redistribution.")
out.append('window.QUESTIONS = ')
out.append(json.dumps(bank, ensure_ascii=False, indent=0))
out.append(';\n')
with io.open(R('questions/bank.js'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('total', len(bank))
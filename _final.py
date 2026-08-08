# -*- coding: utf-8 -*-
import io, json
src = io.open('questions/bank.js', encoding='utf-8').read()
old = json.loads(__import__('re').search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, __import__('re').S).group(1))
# attach src tag 'curated' to old
for q in old: q['src']='curated'
subs = json.loads(io.open('research/_expand_bank.json',encoding='utf-8').read())
exp=[]
for subj, qq in subs.items():
    for q in qq:
        qq2=dict(q); qq2['s']=subj; qq2['src']='expand'
        exp.append(qq2)
# fill path/ophth from PDF (2024-2023 only, clean source tag 'medink')
qs = json.loads(io.open('research/_parsed.json', encoding='utf-8').read())
fill=[q for q in qs if q['subj'] in ('Ophthalmology','Pathology') and q['year'] in (2023,2024)]
for q in fill:
    q['s']=q['subj']; del q['subj']; q['src']='medink'
bank = old + exp + fill
print('total', len(bank))
# write bank.js
with io.open('questions/bank.js','w',encoding='utf-8') as f:
    f.write("// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.\n")
    f.write("// Sources tagged per-item: src=\"curated\" (hand-picked PYQs), \"expand\" (workflow-generated recall Qs),\n")
    f.write("// \"medink\" (parsed from user-provided compiled PYQ PDF). Personal offline practice use only.\n")
    f.write("window.QUESTIONS = ")
    f.write(json.dumps(bank, ensure_ascii=False, indent=0))
    f.write(";\n")
print('wrote questions/bank.js')

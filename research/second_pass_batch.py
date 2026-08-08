# -*- coding: utf-8 -*-
"""Write per-subject second-pass prompt files for subagents."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
c = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
b = json.load(open(r'F:\NEET PG\research\orig_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in b}
uncovered = json.load(open(r'F:\NEET PG\research\second_pass_qids.json', encoding='utf-8'))
for subj, qids in sorted(uncovered.items()):
    lines = []
    for qid in qids:
        q = byid[qid]
        lines.append(f"{qid}\t{q['q'][:200]}\t{q['o'][q['a']] if q['a'] < len(q['o']) else '?'}\t{q['tp']}")
    open(rf'F:\NEET PG\research\second_{subj.replace(" ","_")}.tsv', 'w', encoding='utf-8').write('\n'.join(lines))
    print(subj, len(qids))

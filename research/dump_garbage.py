# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
b = json.load(open(r'F:\NEET PG\research\corrected_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in b}
h = json.load(open(r'F:\NEET PG\research\corrupt_hits.json', encoding='utf-8'))
g = [qid for qid, v in h.items() if 'garbage' in v['reasons']]
GAR = re.compile(r'NODIA|EXAMINATION PAPER|INICET Examination|=== ?page|MEDINK', re.I)
# show full text around garbage in stem cases
n = 0
for qid in sorted(g):
    q = byid[qid]
    s = q['q']
    if GAR.search(s):
        print('='*8, qid, q['s'], '/', q['tp'])
        print(s)
        print('-- o:', q['o'])
        print('-- a:', q['a'])
        print()
        n += 1
        if n >= 30: break

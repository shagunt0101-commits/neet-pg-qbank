# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
c = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
b = json.load(open(r'F:\NEET PG\research\orig_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in b}
nb = [x for a in c['audits'] for x in (a['result'].get('qidIssues') or []) if x['correctS'] in {'Anesthesia','Immunology','Neurology','Neurosurgery','Obstetrics & Gynecology','Oncology','Orthopedics','Pediatrics','Urology'}]
for x in sorted(nb, key=lambda z: z['qid']):
    q = byid[x['qid']]
    print(f"=== {x['qid']}  {x['currentS']}/{x['currentT']}  ->  {x['correctS']}")
    print('Q:', q['q'][:180])
    print('A:', (q['o'][q['a']] if q['a'] < len(q['o']) else '?'))
    print('reason:', x.get('reason',''))
    print()

# -*- coding: utf-8 -*-
import json
from collections import Counter
c = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
nonbank = {'Anesthesia','Immunology','Neurology','Neurosurgery','Obstetrics & Gynecology','Oncology','Orthopedics','Pediatrics','Urology'}
cnt = Counter()
samples = {}
for a in c['audits']:
    for x in a['result'].get('qidIssues') or []:
        if x['correctS'] in nonbank:
            cnt[x['correctS']] += 1
            samples.setdefault(x['correctS'], []).append((x['qid'], x['correctT'], x.get('reason','')))
for s, n in sorted(cnt.items()):
    print(f'== {s}: {n}')
    for qid, t, r in samples[s][:8]:
        print(f'   {qid:7s} {t[:40]:42s} | {r[:60]}')

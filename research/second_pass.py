# -*- coding: utf-8 -*-
"""Prepare second-pass batch: qids with no correction yet per subject."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
c = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
b = json.load(open(r'F:\NEET PG\research\orig_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in b}
uncovered = {}
for a in c['audits']:
    subj = a['subj']
    fixed = {x['qid'] for x in a['result'].get('qidIssues') or []}
    tn_from = [x['from'] for x in (a['result'].get('topicNormalizations') or [])]
    for q in b:
        if q['s'] == subj and q['qid'] not in fixed and q['tp'] not in tn_from:
            uncovered.setdefault(subj, []).append(q['qid'])
for s, qs in sorted(uncovered.items()):
    print(f'{s}: {len(qs)}')
tot = sum(len(v) for v in uncovered.values())
print('TOTAL:', tot)
json.dump({s: sorted(qs) for s, qs in uncovered.items()},
          open(r'F:\NEET PG\research\second_pass_qids.json', 'w', encoding='utf-8'), indent=1)

# -*- coding: utf-8 -*-
"""Apply verified corrections to orig_bank.json -> write corrected bank.

Sources: corrections.json (qidIssues per subject + subject-scoped topicNormalizations)
+ manual stem repairs + image stripping for 39 unverifiable-image questions.
"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

C = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
B = json.load(open(r'F:\NEET PG\research\orig_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in B}
assert len(B) == 2969

STATS = {'s_fixed': 0, 't_fixed': 0, 'img_stripped': 0, 'stem_fixed': 0}

# --- 1. qidIssues ---
issues = {}
for a in C['audits']:
    for x in a['result'].get('qidIssues') or []:
        issues[x['qid']] = x
for qid, x in issues.items():
    q = byid.get(qid)
    if q is None:
        print('MISSING qid in bank:', qid); continue
    if x['correctS'] != q['s']:
        q['s'] = x['correctS']; STATS['s_fixed'] += 1
    if x['correctT'] != q['tp']:
        q['tp'] = x['correctT']; STATS['t_fixed'] += 1

# --- 2. subject-scoped topicNormalizations (for questions not in qidIssues) ---
tn_applied = 0
for a in C['audits']:
    subj = a['subj']
    fixed = {x['qid'] for x in (a['result'].get('qidIssues') or [])}
    for q in B:
        if q['s'] != subj or q['qid'] in fixed:
            continue
        for t in (a['result'].get('topicNormalizations') or []):
            if t['from'] == q['tp']:
                q['tp'] = t['to']; tn_applied += 1
                break  # first match wins (dupe keys resolved by order)
print('tn applied:', tn_applied)

# --- 3. manual stem repairs ---
# q1525: two questions fused (GYN stem + milestones options/ex). Rebuild as milestones Q.
q = byid['q1525']
q['q'] = 'By what age can a child typically copy a cross, recite rhymes, and use the bathroom independently?'
q['s'] = 'Paediatrics'; q['tp'] = 'Developmental Milestones'
q['e'] = 'INI-CET'; q['y'] = 'NOV 2024'
STATS['s_fixed'] += 1; STATS['t_fixed'] += 1; STATS['stem_fixed'] += 1

# q2218: strip NODIA page garbage from stem
q = byid['q2218']
q['q'] = q['q'].replace('NODIA 472=== MEDINK EXAMINATION PAPER NOV-2022', '').strip()
STATS['stem_fixed'] += 1

# --- 4. strip images from 39 unverifiable questions (38 unclear + q1525) ---
STRIP = [i['qid'] for i in C['imgAudit']['imageIssues'] if i['severity'] == 'unclear'] + ['q1525']
for qid in STRIP:
    q = byid.get(qid)
    if q is None:
        print('MISSING img qid:', qid); continue
    if q.get('img'):
        q['img'] = False
        q.pop('imgdata', None)
        STATS['img_stripped'] += 1

# --- verify ---
assert len(B) == 2969
bad = [q['qid'] for q in B if not q['tp'] or not str(q['tp']).strip()]
print('empty tp:', bad)
imgs = [q['qid'] for q in B if q.get('img')]
print('remaining img qs:', len(imgs))
subjs = {}
for q in B:
    subjs[q['s']] = subjs.get(q['s'], 0) + 1
print('subjects:', sorted(subjs.items(), key=lambda x: -x[1]))
print('stats:', STATS)

json.dump(B, open(r'F:\NEET PG\research\corrected_bank.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('corrected_bank.json written')

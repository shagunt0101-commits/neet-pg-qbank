# -*- coding: utf-8 -*-
"""Deterministic rebuild of corrected_bank.json from orig_bank.json.

Order: apply_corrections (s/t/img/stem fixes) -> SAFE garbage strip (tokens only,
NO truncation/prefix-strip which damaged exes) -> q1725 fix -> fix_remaining (24 rebuilds).
"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# ---- step 0: corrections ----
C = json.load(open(r'F:\NEET PG\research\corrections.json', encoding='utf-8'))
B = json.load(open(r'F:\NEET PG\research\orig_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in B}
assert len(B) == 2969

issues = {}
for a in C['audits']:
    for x in a['result'].get('qidIssues') or []:
        issues[x['qid']] = x
for qid, x in issues.items():
    q = byid.get(qid)
    if q is None:
        continue
    if x['correctS'] != q['s']:
        q['s'] = x['correctS']
    if x['correctT'] != q['tp']:
        q['tp'] = x['correctT']

for a in C['audits']:
    subj = a['subj']
    fixed = {x['qid'] for x in (a['result'].get('qidIssues') or [])}
    for q in B:
        if q['s'] != subj or q['qid'] in fixed:
            continue
        for t in (a['result'].get('topicNormalizations') or []):
            if t['from'] == q['tp']:
                q['tp'] = t['to']
                break

q = byid['q1525']
q['q'] = 'By what age can a child typically copy a cross, recite rhymes, and use the bathroom independently?'
q['s'] = 'Paediatrics'; q['tp'] = 'Developmental Milestones'
q['e'] = 'INI-CET'; q['y'] = 'NOV 2024'

q = byid['q2218']
q['q'] = q['q'].replace('NODIA 472=== MEDINK EXAMINATION PAPER NOV-2022', '').strip()

STRIP = [i['qid'] for i in C['imgAudit']['imageIssues'] if i['severity'] == 'unclear'] + ['q1525']
for qid in STRIP:
    q = byid.get(qid)
    if q is None or not q.get('img'):
        continue
    q['img'] = False
    q.pop('imgdata', None)

# ---- step 1: SAFE garbage strip (tokens only) ----
TOKENS = [
    r'NODIA\s*\d*\s*={2,}\s*(?:page\s*)?\d*\s*(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'Downloaded\s+from\s+www\.pdf\.tube\s*\d*\s*={2,}\s*(?:page\s*)?\d*\s*(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'Click\s+Here\s+to\s+Buy\s+book\s+on\s+Amazon\s*\d*\s*={2,}\s*(?:page\s*)?\d*\s*(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'(?:INICET|MEDINK)\s+Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'={2,}\s*(?:page\s*)?\d*\s*(?:INICET|MEDINK)?\s*Examination\s+Paper(?:\s+[A-Z]{3}-?\d{4})?',
    r'\bNODIA\b\s*\d*\s*={2,}',
    r'\bNODIA\b',
    r'\bA\s*Ans\b',
    r'Downloaded\s+from\s+www\.pdf\.tube',
    r'Click\s+Here\s+to\s+Buy\s+book\s+on\s+Amazon',
    r'\x01',
    r'\*{4,}',
    r'EXAMINATION\s+PAPER\s+\d{4}',
]
pat = re.compile('|'.join(TOKENS), re.I)
n = 0
for q in B:
    changed = False
    for field in ('q', 'ex'):
        v = q.get(field) or ''
        v2 = pat.sub('', v)
        v2 = re.sub(r'\s{2,}', ' ', v2).strip()
        if v2 != v:
            q[field] = v2
            changed = True
    o2 = [re.sub(r'\s{2,}', ' ', pat.sub('', o)).strip() for o in q.get('o', [])]
    if o2 != q.get('o', []):
        q['o'] = o2
        changed = True
    if changed:
        n += 1
print('safe-strip cleaned:', n)

# ---- step 2: q1725 ----
q = byid['q1725']
q['q'] = 'A woman with PCOS presents with significant facial hair, infertility, and a BMI of 40. Which of the following is the most appropriate management plan?'
q['a'] = 2

# ---- step 3: fix_remaining (24 rebuilt questions) ----
from fix_remaining import FIX
for qid, (st, o, a, ex) in FIX.items():
    q = byid[qid]
    q['q'] = st
    q['o'] = o
    q['a'] = a
    q['ex'] = ex

# ---- verify ----
assert len(B) == 2969
assert all(q.get('tp') and str(q['tp']).strip() for q in B), 'empty tp'
assert all(0 <= q['a'] < len(q['o']) for q in B), 'answer oob'
assert all(len(q.get('o', [])) == 4 for q in B), 'not 4 options'
G = re.compile(r'NODIA|EXAMINATION\s+PAPER|INICET|MEDINK|pdf\.tube|AAns|Click Here to Buy|Downloaded from|\x01|\*{4,}', re.I)
import collections
resid = []
for q in B:
    s = ' '.join([q.get('q', ''), ' '.join(q.get('o', [])), q.get('ex', '')])
    for m in G.finditer(s):
        t = m.group(0)
        # false positives: xenodiagnosis (nodia), HIDA (not in regex), legit words
        if t.lower() == 'nodia' and 'xenodiag' in s[max(0, m.start()-10):m.end()+10]:
            continue
        resid.append((q['qid'], t[:25]))
print('residual token hits:', len(resid), resid[:10])
imgs = [q['qid'] for q in B if q.get('img')]
print('questions:', len(B), '| img qs:', len(imgs))
subs = collections.Counter(q['s'] for q in B)
print('subjects:', len(subs))

json.dump(B, open(r'F:\NEET PG\research\corrected_bank.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('WROTE corrected_bank.json')

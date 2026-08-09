# -*- coding: utf-8 -*-
"""Detect likely-corrupt questions in the 2969 bank (heuristics)."""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
B = json.load(open(r'F:\NEET PG\research\corrected_bank.json', encoding='utf-8'))
byid = {q['qid']: q for q in B}
GARBAGE = re.compile(r'NODIA|EXAMINATION PAPER|INICET Examination|=== ?page|MEDINK', re.I)
DANGLING = re.compile(r'\b(nodia|aans|ans)\b', re.I)

def sig(q):
    return ' '.join([q.get('q',''), ' '.join(q.get('o',[])), q.get('ex','')])

hits = {}
for q in B:
    s = sig(q)
    reasons = []
    if GARBAGE.search(s):
        reasons.append('garbage')
    if DANGLING.search(s):
        reasons.append('dangling')
    # options contain letters+digits answer-prefix noise like 'AAns'
    # explanation contains option-letter chatter
    if re.search(r'\b[ABCD]\s*\)', q.get('ex','')) and not re.search(r'option', q.get('ex',''), re.I):
        reasons.append('ex-option-noise')
    if q['a'] >= len(q['o']):
        reasons.append('answer-oob')
    if not q['q'] or len(q['q']) < 15:
        reasons.append('tiny-stem')
    # stem much shorter than expected vs ex
    if len(q.get('ex','')) > 0 and len(q['q']) < 25:
        reasons.append('tiny-stem-vs-ex')
    if reasons:
        hits[q['qid']] = reasons

print('hits:', len(hits))
for qid, rs in sorted(hits.items()):
    print(qid, rs)
json.dump({qid: {'reasons': rs, 'stem': byid[qid]['q'][:160]} for qid, rs in sorted(hits.items())},
          open(r'F:\NEET PG\research\corrupt_hits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

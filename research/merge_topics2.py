# -*- coding: utf-8 -*-
"""Merge workflow-assigned topic tags into bank.js as q['tp'], using journal per-chunk arrays.
Chunks may be short; gaps get 'General'.
"""
import io, json, re, sys

BANK_PATH = 'questions/bank.js'
JOURNAL = r'C:\Users\navne\.claude\projects\F--NEET-PG\7f70972e-7f7a-41c2-9f48-027968bd8703\subagents\workflows\wf_7046d20e-c94\journal.jsonl'

def load_bank():
    src = io.open(BANK_PATH, encoding='utf-8').read()
    m = re.search(r'window\.QUESTIONS\s*=\s*(\[.*\])\s*;', src, re.S)
    if not m:
        print('Cannot parse bank.js', file=sys.stderr)
        sys.exit(1)
    return json.loads(m.group(1))

def save_bank(bank):
    out = []
    out.append('// NEET PG / INI-CET practice bank — reconstructed from curated + deep-research expansions.')
    out.append('// Sources tagged per-item: src="curated", "expand", "medink", "generated". Topics per-item: tp.')
    out.append('window.QUESTIONS = ')
    out.append(json.dumps(bank, ensure_ascii=False, indent=0))
    out.append('\n;')
    io.open(BANK_PATH, 'w', encoding='utf-8').write('\n'.join(out))
    print('Bank saved, total', len(bank))

def main():
    # read chunks in order
    chunks = []
    with open(JOURNAL, encoding='utf-8') as f:
        for line in f:
            try:
                j = json.loads(line)
            except Exception:
                continue
            if j.get('type') == 'result' and isinstance(j.get('result'), dict):
                t = j['result'].get('topics')
                if isinstance(t, list):
                    chunks.append(t)
    print('chunks:', len(chunks))
    bank = load_bank()
    all_topics = [None] * len(bank)
    used = 0
    for ci, chunk in enumerate(chunks):
        base = ci * 200
        for j, tp in enumerate(chunk):
            idx = base + j
            if idx >= len(bank):
                continue
            tp = (tp or '').strip() or 'General'
            all_topics[idx] = tp
            used += 1
    # fill gaps
    gaps = 0
    for i in range(len(bank)):
        if not all_topics[i]:
            all_topics[i] = 'General'
            gaps += 1
    print('used:', used, 'gaps filled:', gaps)
    for i, tp in enumerate(all_topics):
        bank[i]['tp'] = tp
    save_bank(bank)

if __name__ == '__main__':
    main()

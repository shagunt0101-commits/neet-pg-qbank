# -*- coding: utf-8 -*-
"""Merge workflow-assigned topic tags into bank.js as q['tp']."""
import io, json, re, sys

BANK_PATH = 'questions/bank.js'
TAG_PATH = r'C:\Users\navne\AppData\Local\Temp\claude\F--NEET-PG\7f70972e-7f7a-41c2-9f48-027968bd8703\tasks\w769axz9r.output'

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
    raw = io.open(TAG_PATH, encoding='utf-8').read()
    data = json.loads(raw)
    tagged = data['tagged'] if 'tagged' in data else data['result']['tagged']
    print('tags:', len(tagged))
    bank = load_bank()
    # verify index alignment
    if len(tagged) != len(bank):
        print('MISMATCH: tags', len(tagged), 'bank', len(bank), file=sys.stderr)
        sys.exit(1)
    seen = {}
    for t in tagged:
        i = t['idx']
        tp = t['topic'].strip()
        if not tp:
            tp = 'General'
        bank[i]['tp'] = tp
        seen[tp] = seen.get(tp, 0) + 1
    # consistency: questions with same stem share topic (dedupe check)
    print('unique topics:', len(seen))
    print('top topics:', sorted(seen.items(), key=lambda x: -x[1])[:10])
    save_bank(bank)

if __name__ == '__main__':
    main()

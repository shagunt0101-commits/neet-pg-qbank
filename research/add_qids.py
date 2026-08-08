# -*- coding: utf-8 -*-
"""Add unique question IDs to all bank.js questions."""
import io, json, re, sys

BANK_PATH = 'questions/bank.js'

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
    bank = load_bank()
    for i, q in enumerate(bank):
        q['qid'] = f'q{i}'
    save_bank(bank)

if __name__ == '__main__':
    main()
